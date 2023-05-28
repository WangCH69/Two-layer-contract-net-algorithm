#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Agent import Agent
from Task import Task
from Subnet import Subnet
from Groupnet import Groupnet
import experiments as ep


class Simulation:
    # 初始化仿真对象
    def __init__(self, config):
        self.config = config
        self.subnet_num = config["subnet_num"]

        # 定义任务列表
        self.total_tasks = []
        for t in config["tasks"]:
            self.total_tasks.append(Task(t["id"], t["timeConsume"], t["target"], t["value"], t["threat"], t["defense"], t["priority"]))

        # 定义子网列表subnets
        self.subnets = []
        subnet_task_capacity = config["subnet_task_capacity"]
        agent_task_capacity = config["agent_task_capacity"]
        for id in range(1, self.subnet_num+1):
            name_string = "subnet_" + str(id) + "_agents"
            subnet_agents = []
            for a in config[name_string]:
                subnet_agents.append(Agent(a["id"], a["subnet_id"], a["speed"], a["initPos"], a["value"], a["attack"], a["defense"], agent_task_capacity, a["pref"]))
            # 构建一个子网
            self.subnets.append(Subnet(id, subnet_agents, subnet_task_capacity))
    
        # 定义子网集群groupnet
        self.groupnet = Groupnet(self.subnets, self.total_tasks)


    # 执行两层合同网算法
    def contractNet_algorithm(self):
        print("Phase 1 starts\n")
        # 进行第一层协商
        self.groupnet.first_layer_BID()
        print("———————— Fisrt-Layer finished\n")

        # 进行第二层协商               这里最好用多线程方法同步进行
        for i in range(self.subnet_num):
            print("subnet ", self.subnets[i].id, " is running")
            self.subnets[i].second_layer_BID()
        print("———————— Second-Layer finished\n")
        print("Phase 1 ends\n")

        # 展示结果1
        self.print_summary_1()
        
        # 进行重分配
        print("Phase 2 starts\n")
        self.groupnet.Reallocation()
        print("———————— Reallocation finished\n")
        self.print_Phase_2_Reallocation_summary()

        # 进行任务交换
        self.groupnet.Exchange()
        print("\n———————— Exchange finished\n")
        self.print_Phase_2_Exchange_summary()
        print("Phase 2 ends\n")

        # 展示最终结果
        self.print_Final_summary()


    # 算法结果展示：正常两层合同网协商之后的结果
    def print_summary_1(self):
        print("----------------------------   Phase 1 summary   ----------------------------")

        # 1、子网接收任务的情况
        print("1、subnet tasks allocation:")
        for subnet in self.subnets:
            print("subnet ", subnet.id, " receives tasks: ", end="")
            for task in subnet.subnet_tasks:
                print(task.id, " ", end="")
            print()
        print("-----------------------------------------------------------------------------")

        # 2、各子网的agent任务分配的情况
        print("2、subnet agent tasks allocation:")
        for subnet in self.subnets:
            for agent in subnet.subnet_agents:
                print("Subnet ", subnet.id, " Agent ", agent.id, " is contracted with tasks: ", end="")
                for task in agent.contracted_list:
                    print(task.id, " ", end="")
                print()
            print()
        print("-----------------------------------------------------------------------------")
        
        # 3、未分配的任务的情况
        print("3、unallocated tasks:")
        realloc_tasks = []
        for task in self.total_tasks:
            if task.contractor == None:
                realloc_tasks.append(task)
                print("Task ", task.id, " is contracted to: no one")
        print("----------------------------         end         ----------------------------\n\n")



    # 任务重分配后的结果
    def print_Phase_2_Reallocation_summary(self):
        print("----------------------------   Phase 2 Reallocation summary   ----------------------------")

        # 4、任务重分配的情况
        print("4、Reallocated tasks:")
        for task_1 in self.groupnet.realloc_tasks:
            for task in self.groupnet.total_tasks:
                if task.id == task_1.id:
                    print("Previously unallocated Task ", task.id, " is now contracted to: subnet ", task.contracted_subnet, " agent ", task.contractor)
        print("-------------------------------------------------------------------------------------------")



    # 任务交换后的总结
    def print_Phase_2_Exchange_summary(self):
        print("----------------------------   Phase 2 Exchange summary   ----------------------------")

        # 5、任务交换的情况
        print("5、Exchanged tasks:")
        for i in range(len(self.groupnet.NegativeBid_tasks)):
            task_1 = self.groupnet.NegativeBid_tasks[i]
            task_2 = self.groupnet.best_Exchange_tasks[i]
            
            if isinstance(task_2, Task):
                # 如果task_2是Task类的对象，说明是两个任务交换
                print("subnet ", task_1.contracted_subnet, " agent ", task_1.contractor, " task ", task_1.id, "is exchanged with ", end="")
                print("subnet ", task_2.contracted_subnet, " agent ", task_2.contractor, " task ", task_2.id)

                print("      ---->  subnet ", task_1.contracted_subnet, " agent ", task_1.contractor, " task ", task_2.id)
                print("      ---->  subnet ", task_2.contracted_subnet, " agent ", task_2.contractor, " task ", task_1.id, "\n")
            else:
                # 如果task_2不是Task类的对象，而是某个agent，说明是任务转移
                print("subnet ", task_1.contracted_subnet, " agent ", task_1.contractor, " task ", task_1.id, "is transfered to ", end="")
                print("subnet ", task_2.subnet_id, " agent ", task_2.id)

                print("      ---->  subnet ", task_1.contracted_subnet, " agent ", task_1.contractor, " task None")
                print("      ---->  subnet ", task_2.subnet_id, " agent ", task_2.id, " task ", task_1.id, "\n")

        print("--------------------------------------------------------------------------------------")
        
       

    # 最终总结
    def print_Final_summary(self):
        # 6、最终的任务分配情况
        print("\n\n----------------------------  Final summary   ----------------------------")
        print("Final tasks allocation:")
        print("A、subnet tasks allocation:")
        # 子网接收任务的情况
        for subnet in self.subnets:
            print("subnet ", subnet.id, " receives tasks: ", end="")
            for task in subnet.subnet_tasks:
                print(task.id, " ", end="")
            print()
        print("--------------------------------------------------------------------------")

        # 各子网的agent任务分配的情况
        print("B、subnet agent tasks allocation:")
        for subnet in self.subnets:
            for agent in subnet.subnet_agents:
                print("Subnet ", subnet.id, " Agent ", agent.id, " is contracted with tasks: ", end="")
                for task in agent.contracted_list:
                    print(task.id, " ", end="")
                print()
            print()
        print("------------------------------     end     -------------------------------")



# 主函数
if __name__ == '__main__':

    print("sim starts\n")


    # 定义仿真案例，进行合同网算法仿真
    # sim = Simulation(ep.case_1)
    sim = Simulation(ep.case_2)
    sim.contractNet_algorithm()

    print("sim ends\n")
