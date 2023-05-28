

import numpy as np


# 子网中执行任务的agent的类
class Agent:
    
    def __init__(self, id, subnet_id, speed, initPos, value, attack, defense, task_capacity, pref):
        # 基础信息
        self.id = id
        self.subnet_id = subnet_id
        self.speed = speed                      # 自身速度，默认2.0m/s
        self.pos = initPos
        self.value = value                      # 自身价值，取值范围为[0,100]
        self.attack = attack                    # 自身攻击力，取值范围为[0,100]
        self.defense = defense                  # 自身防御力，取值范围为[0,100]
        self.P_destroy = {}                     # 执行任务时agent摧毁目标的概率，取值范围为[0,100]
        self.P_get_destroyed = {}               # 执行任务时agent被摧毁的概率，取值范围为[0,100] (在Subnet中通过determine_agent_Bid_list()函数确定)

        # 任务相关
        self.task_capacity = task_capacity      # agent的任务容量
        self.pref = pref                        # agent可以承受的被摧毁概率
        self.Bid_list = []                      # 满足agent任务偏好的任务列表（即为要投标的任务列表）
                                                # 如果执行该任务时agent的被摧毁概率(P_get_destroyed)超过pref（即威胁度超出agent承受范围），则在投标时直接拒绝、不予考虑
        self.contracted_list = []               # agent最终中标的任务列表
        self.T_load = 0.0                       # agent的工作负载 （完成contracted_list中已有任务的所需时间）
        self.CT = 0.0                           # agent的工作负载系数
        
        # 投标状态与投标值
        self.states = {}                        # 投标状态与投标值都是字典类型变量，元素形式为：任务id：“state” 或 任务id：Bid
        self.currentBid = {}                    # agent对任务的当前投标值
    

    # 将agent对某任务的投标状态还原为“等待（WAITING）”
    def clean_states(self, task):
        self.states[task.id] = "WAITING"

    # 计算工作负载
    def calculate_T_load(self):
        self.T_load = 0.0
        for task in self.contracted_list:
            self.T_load += task.timeConsume

    # 计算两点距离
    def calculate_points_distance(self, p1, p2):
        vec_p = np.array([p2[0]-p1[0], p2[1]-p1[1]])
        distance = np.linalg.norm(vec_p)
        return distance


    # 根据agent对任务的当前投标状态确定下一步的投标状态
    def determine_states(self, task):                                    
        if self.states[task.id] == "WAITING":
            self.states[task.id] = "PRE_BID"
        elif self.states[task.id] == "DEF_BID":
            task.contractor = self.id
            self.states[task.id] = "CONTRACTOR"
            self.contracted_list.append(task)


    # 主体：计算投标值
    def calculate_Bid(self, task, T_load_ave):
        # 1、计算agent与该新增任务点之间的距离dis
        if len(self.contracted_list) != 0:
            # 若此前contracted_list中已有若干待执行的任务，则agent到该新增任务点的距离是agent经过所有任务点时的距离
            dis = self.calculate_points_distance(self.pos, self.contracted_list[0].target)
            for i in range(len(self.contracted_list) - 1):
                dis += self.calculate_points_distance(self.contracted_list[i].target, self.contracted_list[i+1].target)
            dis += self.calculate_points_distance(self.contracted_list[-1].target, task.target)    
        else:
            # 若此前contracted_list中没有待执行的任务，则直接计算agent到该任务点的距离
            dis = self.calculate_points_distance(self.pos, task.target)

        # 2、计算执行此任务的收益价值reward
        self.P_destroy[task.id] = self.attack - task.defense                      # 任务目标被摧毁的概率
        reward = task.value * self.P_destroy[task.id] / 100
        
        # 3、计算执行此任务的开销成本cost
        k1 = 0.6
        k2 = 1.0 - k1
        kd = 0.5                             # kd为将距离变量dis进行单位统一化处理过程中的系数；战场为正方形，边长范围为[0,100]，最长距离(对角线)为140米
        self.P_get_destroyed[task.id] = task.threat - self.defense                # agent被摧毁的概率
        if self.P_get_destroyed[task.id] < 0:
            self.P_get_destroyed[task.id] = 0
        cost = k1*(self.value * self.P_get_destroyed[task.id] / 100) + k2*kd*dis

        # 4、计算执行此任务的净效能profit
        profit = (reward - cost) * task.priority                # task.priority为任务的优先级，取值范围为[0,10]

        # 5、计算agent的工作负载系数CT
        self.calculate_T_load
        if abs(T_load_ave) <= 10e-9:
            # 若T_load_ave为0，则子网中所有无人机都没有任务，负载系数设为1、所有无人机平等竞争
            self.CT = 1.0
        else:
            # 若T_load_ave不为0，则根据无人机自身的工作负载情况计算工作负载系数；工作负载越轻，则系数越高
            self.CT = 1.0 - (self.T_load / T_load_ave)            # 若工作负载系数大于1，说明此agent的负荷比网络平均水平要高，不适合接收新的任务

        # 6、计算对此任务的投标值Bid
        Bid = profit * self.CT

        # 7、将投标值取整
        self.currentBid[task.id] = int(np.ceil(Bid))

        return self.currentBid[task.id]