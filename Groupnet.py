
import math
import numpy as np
import copy


# 组网的类
class Groupnet:
    
    def __init__(self, subnets, total_tasks):          
        self.subnets = subnets                          # 组网中的子网
        self.total_tasks = total_tasks                  # 组网的全部任务
        

    # 合同网第一级协商：确定各个子网接收的任务
    def first_layer_BID(self):    
        for task in self.total_tasks:
            # 1、计算子网对所有任务的投标值
            for subnet in self.subnets:
                # 判断：如果子网任务容量已满，则退出投标
                #print(len(subnet.subnet_tasks))
                if len(subnet.subnet_tasks) == subnet.task_capacity:
                    subnet.currentBid[task.id] = -(math.inf)
                    continue
                # 如果容量未满，则进入投标
                else:
                    subnet.calculate_subnet_Bid(task)               # 计算子网对该任务的投标值
                    #print(subnet.currentBid[task.id])

            # 2、确定最佳子网
            bestBid = -(math.inf)
            bestSubnet = None
            for subnet in self.subnets:
                if subnet.currentBid[task.id] > bestBid:
                    bestBid = subnet.currentBid[task.id]
                    bestSubnet = subnet.id
                    continue
            
            # 3、为最佳子网分配任务
            for subnet in self.subnets:
                if subnet.id == bestSubnet:
                    subnet.subnet_tasks.append(task)
                    task.contracted_subnet = subnet.id
    


    # 在正常的两层协商之后，为没有分配到agent的任务进行重新分配
    def Reallocation(self):
        self.realloc_tasks = []
        for task in self.total_tasks:
            if task.contractor == None:
                # 如果该任务已在两层协商中被分给了某个subnet，则从该subnet中将该任务删除
                if task.contracted_subnet != None:
                    for subnet in self.subnets:
                        if task.contracted_subnet == subnet.id:
                            subnet.subnet_tasks.remove(task)
                # 同时将该任务的contracted_subnet设为None
                task.contracted_subnet = None
                self.realloc_tasks.append(task)

        for task in self.realloc_tasks:
            # 找出待执行任务列表未满的agent；每进行一轮搜索就要重新确定一次，因为部分agent有可能在中途任务量变满。
            self.realloc_agents = []
            for subnet in self.subnets:
                for agent in subnet.subnet_agents:
                    if len(agent.contracted_list) != agent.task_capacity:
                        self.realloc_agents.append(agent)

            bestBid = -(math.inf)
            bestAgent = None
            # 寻找bestAgent
            for agent in self.realloc_agents:
                self.subnets[agent.subnet_id - 1].calculate_T_load_ave()
                agent.calculate_Bid(task, self.subnets[agent.subnet_id - 1].T_load_ave)           # 计算投标值

                if(agent.currentBid[task.id] > bestBid):
                    bestBid = agent.currentBid[task.id]
                    bestAgent = agent.id
                                    
            # 确定bestAgent的最终投标状态
            flag = 0
            if bestAgent != None:
                for subnet in self.subnets:
                    for agent in subnet.subnet_agents:     
                        if agent.id == bestAgent:
                            # A、更新subnets中最佳agent的相关信息
                            agent.states[task.id] = "DEF_BID"                # 如果是bestAgent，则该agent中标
                            agent.determine_states(task)                     # 最后更新一次该agent的状态，如果状态是DEF_BID，则确定为contractor
                            # B、更新subnet的接收任务列表
                            subnet.subnet_tasks.append(task)

                            # 注意：agent.determine_states(task)这一步的task.contractor = self一句更改的是realloc_tasks列表中的task信息，需要进一步更新全局变量total_tasks列表中的task信息
                            for task_1 in self.total_tasks:
                                if task_1.id == task.id:
                                    task_1.contractor = agent.id
                                    task_1.contracted_subnet = subnet.id
                                    task_1.bestBid[agent.id] = bestBid

                                    flag = 1            # 为flag赋值，准备跳出循环
                                    break
                        if flag == 1:                   # 如果之前flag没有赋值而在这一步直接判断，则会出问题，会导致只在第一个subnet中循环搜索agent，导致task 17无法被分配到它的bestAgent(agent 11)上
                            break
                    if flag == 1:                   
                        break



    # 在正常的两层协商之后，针对分配不合理的任务进行任务调整（例如A执行任务1、B执行任务2的效益比A执行任务2、B执行任务1的效益低；或由于偏好原因只有一个agent可以接收某任务，但投标值为负数）
    def Exchange(self):
        # 1、找出最佳投标值为负数的任务
        self.NegativeBid_tasks = []                 # NegativeBid_tasks列表中保存的是没有交换前的投标值为负数的待交换任务（用于summary时的结果展示）
        self.best_Exchange_tasks = []               # best_Exchange_tasks列表中保存的是与之对应的没有交换前的被交换任务（用于summary时的结果展示）

        for subnet_1 in self.subnets:                                                # subnet_1为待交换任务task_1对应的contracted_subnet
            for agent_1 in subnet_1.subnet_agents:                                   # agent_1为待交换任务task_1对应的contractor
                flag = 0
                for task_1 in agent_1.contracted_list:
                    # 如果flag为1，则agent_1.contracted_list中有任务被替换，需要重新从第一个任务开始遍历
                    if flag == 1:
                        task_1 = agent_1.contracted_list[0]
                        flag = 0

                    if task_1.bestBid[task_1.contractor] < 0 :
                        task_1_copy = copy.deepcopy(task_1)               
                        task_1_copy_2 = copy.deepcopy(task_1_copy)
                        self.NegativeBid_tasks.append(task_1_copy)            # NegativeBid_tasks列表中保存的是没有交换前的投标值为负数的所有任务（用于summary时的结果展示）

                        # 注意：如果直接将task加入NegativeBid_tasks列表或使用task_copy = task后再将task_copy加入列表，则NegativeBid_tasks列表中的任务的地址与全局变量total_tasks中的任务的地址是一样的，
                        #      对total_tasks中的任务进行改动，也会影响NegativeBid_tasks列表中任务的相关信息，会导致后续展示交换结果时任务的agent与subnet信息变为交换后的而非交换前的。
                        # 正确方法：使用deepcopy对变量task进行深拷贝，生成不同地址的变量task_copy，再加入NegativeBid_tasks列表中

                        # 遍历所有子网的所有agent的所有待执行任务，找到与之对应的最佳调换任务
                        best_Exchange_task = None
                        best_Exchange_agent = None
                        Exchange_search_time = 0
                        for subnet_2 in self.subnets:                                       # subnet_2为被交换任务task_2对应的contracted_subnet
                            for agent_2 in subnet_2.subnet_agents:                          # agent_2为被交换任务task_2对应的contractor
                                if agent_1.id != agent_2.id:
                                    for task_2 in agent_2.contracted_list:
                                        if task_2 != None:
                                            Bid_1_pre = task_1.bestBid[task_1.contractor]                # 对调agent之前，task_1的执行者对task_1的投标值
                                            Bid_2_pre = task_2.bestBid[task_2.contractor]                # 对调agent之前，task_2的执行者对task_2的投标值

                                            # 将第一次搜索的两个任务的当前最佳投标值之和作为best_Exchange_Bid的基础值，后续在这个基础上进行比较
                                            if Exchange_search_time == 0:
                                                best_Exchange_Bid = Bid_1_pre + Bid_2_pre

                                            subnet_1.calculate_T_load_ave()
                                            subnet_2.calculate_T_load_ave()

                                            Bid_1_aft = agent_2.calculate_Bid(task_1, subnet_2.T_load_ave)            # 对调agent之后，task_2的执行者对task_1的投标值
                                            Bid_2_aft = agent_1.calculate_Bid(task_2, subnet_1.T_load_ave)            # 对调agent之后，task_1的执行者对task_2的投标值

                                            # 更新最佳调换对象
                                            if Bid_1_aft + Bid_2_aft > best_Exchange_Bid:
                                                best_Exchange_task = task_2
                                                best_Exchange_agent = agent_2
                                                best_Exchange_Bid_1 = Bid_1_aft             # 调换后task_1的最佳投标值
                                                best_Exchange_Bid_2 = Bid_2_aft             # 调换后task_2的最佳投标值
                                                best_Exchange_Bid = Bid_1_aft + Bid_2_aft
                                            
                                            # if task_1.id == 4:
                                            #     print("exchange: subnet ",subnet_2.id, " agent ",agent_2.id, " task ", task_2.id, "  || bid: ", Bid_1_aft + Bid_2_aft)

                                        elif task_2 == None:            # 如果agent_2没有待执行任务，task_2为None
                                            Bid_1_pre = task_1.bestBid[task_1.contractor]                # 对调agent之前，task_1的执行者对task_1的投标值
                                            Bid_2_pre = 0                                                # 对调agent之前，task_2的执行者对task_2的投标值

                                            # 将第一次搜索的两个任务的当前最佳投标值之和作为best_Exchange_Bid的基础值，后续在这个基础上进行比较
                                            if Exchange_search_time == 0:
                                                best_Exchange_Bid = Bid_1_pre + Bid_2_pre

                                            subnet_2.calculate_T_load_ave()

                                            Bid_1_aft = agent_2.calculate_Bid(task_1, subnet_2.T_load_ave)            # 对调agent之后，task_2的执行者对task_1的投标值
                                            Bid_2_aft = 0                                                             # 对调agent之后，task_1的执行者对task_2的投标值

                                            # 更新最佳调换对象
                                            if Bid_1_aft + Bid_2_aft > best_Exchange_Bid:
                                                best_Exchange_task = "No_task"
                                                best_Exchange_agent = agent_2
                                                best_Exchange_Bid_1 = Bid_1_aft             # 调换后task_1的最佳投标值
                                                best_Exchange_Bid_2 = Bid_2_aft             # 调换后task_2的最佳投标值
                                                best_Exchange_Bid = Bid_1_aft + Bid_2_aft

                                        Exchange_search_time += 1

                        # 搜索结束，如果没找到调换的最佳agent与最佳task，则在列表中去除本任务(不再考虑对本任务进行交换)，进行下一个任务的搜索
                        if best_Exchange_task == None:
                            for task_1_copy in self.NegativeBid_tasks:
                                if task_1.id == task_1_copy.id:
                                    self.NegativeBid_tasks.remove(task_1_copy)
                                    break       
                        
                        # 搜索结束，如果找到的最佳调换agent_2并没有任务，则将agent_1的task_1直接转移给agent_2
                        elif best_Exchange_task == "No_task" and best_Exchange_agent != None:
                            self.best_Exchange_tasks.append(best_Exchange_agent)                # 此时加入列表的是best_Exchange_agent，展示结果时需要单独处理

                            for task in subnet_1.subnet_tasks:
                                if task.id == task_1.id:
                                    subnet_1.subnet_tasks.remove(task)
                                    break

                            for task in agent_1.contracted_list:
                                if task.id == task_1.id:
                                    agent_1.contracted_list.remove(task)
                                    agent_1.states[task.id] = "DEF_REJ"
                                    break
                            
                            for subnet_2 in self.subnets:
                                if subnet_2.id == best_Exchange_agent.subnet_id:
                                    task_1.contracted_subnet = subnet_2
                                    subnet_2.subnet_tasks.append(task_1)

                                    for agent_2 in subnet_2.subnet_agents:
                                        if agent_2.id == best_Exchange_agent:
                                            task_1.contractor = agent_2
                                            agent_2.contracted_list.append(task_1)
                                            agent_2.states[task.id] = "CONTRACTOR"
                                            agent_2.currentBid[task.id] = Bid_1_aft
                                            break
                                    break


                        # 搜索结束，如果找到了调换的最佳agent与最佳task，则进行调换
                        # 需要调换的对象：A、subnet对应的任务；B、agent对应的任务；C、任务对应的subnet；D、任务对应的agent
                        elif best_Exchange_task != None:
                            best_Exchange_task_copy = copy.deepcopy(best_Exchange_task)
                            best_Exchange_task_copy_2 = copy.deepcopy(best_Exchange_task_copy)
                            self.best_Exchange_tasks.append(best_Exchange_task_copy)
                            
                            for subnet_2 in self.subnets:
                                # A、如果两个任务所属subnet不同，则调换两个subnet对应的任务
                                if subnet_1.id != best_Exchange_task.contracted_subnet:
                                    for task in subnet_1.subnet_tasks:
                                        if task.id == task_1_copy_2.id:
                                            subnet_1.subnet_tasks.remove(task)
                                            best_Exchange_task_copy_2.contracted_subnet = subnet_1.id              # C、调换两个任务对应的subnet
                                            subnet_1.subnet_tasks.append(best_Exchange_task_copy_2)                 # 使用另一个相同内容不同地址的变量best_Exchange_task_copy_2来进行后续操作
                                            break
                                    
                                    if subnet_2.id == best_Exchange_task.contracted_subnet:
                                        for task in subnet_2.subnet_tasks:
                                            if task.id == best_Exchange_task_copy_2.id:
                                                subnet_2.subnet_tasks.remove(task)
                                                task_1_copy_2.contracted_subnet = subnet_2.id 
                                                subnet_2.subnet_tasks.append(task_1_copy_2)
                                                break
                        
                                # B、调换两个agent对应的任务
                                for task in agent_1.contracted_list:
                                    if task.id == task_1_copy_2.id:
                                        agent_1.contracted_list.remove(task)
                                        del agent_1.currentBid[task.id]
                                        best_Exchange_task_copy_2.contractor = agent_1.id                             # D、调换两个任务对应的agent
                                        best_Exchange_task_copy_2.bestBid[agent_1.id] = best_Exchange_Bid_2
                                        agent_1.contracted_list.append(best_Exchange_task_copy_2)
                                        agent_1.states[best_Exchange_task_copy_2.id] = "CONTRACTOR"
                                        break
                                
                                for agent_2 in subnet_2.subnet_agents:
                                    if agent_2.id == best_Exchange_agent.id:
                                        for task in agent_2.contracted_list:
                                            if task.id == best_Exchange_task_copy_2.id:
                                                agent_2.contracted_list.remove(task)
                                                del agent_2.currentBid[task.id]
                                                task_1_copy_2.contractor = agent_2.id 
                                                task_1_copy_2.bestBid[agent_2.id] = best_Exchange_Bid_1
                                                agent_2.contracted_list.append(task_1_copy_2)
                                                agent_2.states[task_1_copy_2.id] = "CONTRACTOR"
                                                break
                                
                            flag = 1