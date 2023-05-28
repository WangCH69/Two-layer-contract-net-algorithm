#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy as np

# 子网的类
class Subnet:
        
    def __init__(self, id, subnet_agents, subnet_task_capacity):
        # 基础信息
        self.id = id
        self.subnet_agents = subnet_agents
        self.agents_num = len(subnet_agents)
        self.T_load_ave = 0.0

        # 任务相关
        self.currentBid = {}                             # 第一层协商中，子网对各个任务的当前投标值
        self.subnet_tasks = []                           # 本子网最终确定接收的任务
        self.task_capacity = subnet_task_capacity               # 本子网的任务容量
        

    # 计算子网中的平均负载
    def calculate_T_load_ave(self):
        self.T_load_ave = 0.0
        for agent in self.subnet_agents:
            agent.calculate_T_load()
            self.T_load_ave += agent.T_load
        self.T_load_ave = self.T_load_ave / self.agents_num


    # 确定符合agent任务喜好的任务列表
    def determine_agent_Bid_list(self):
        for task in self.subnet_tasks:
            for agent in self.subnet_agents:
                agent.P_get_destroyed[task.id] = task.threat - agent.defense          # agent被摧毁的概率
                if agent.P_get_destroyed[task.id] < agent.pref:
                    agent.Bid_list.append(task)             # 将符合偏好的任务加入任务列表
                    agent.states[task.id] = "WAITING"        # 初始化agents对该任务的投标状态为“等待（WAITING）”
                

    # 根据子网中所有agent的相关信息大致计算子网的攻防能力
    def calculate_subnet_AD_ability(self):
        self.value = 0.0                        # 子网价值，取值范围为[0,100]
        self.attack = 0.0                       # 子网攻击力，取值范围为[0,100]
        self.defense = 0.0                      # 子网防御力，取值范围为[0,100]

        for agent in self.subnet_agents:
            self.value += agent.value                        
            self.attack += agent.attack               
            self.defense += agent.defense

        self.value = self.value / len(self.subnet_agents)
        self.attack = self.attack / len(self.subnet_agents)            
        self.defense = self.defense / len(self.subnet_agents)                       


    # 根据子网的攻防能力，大致计算子网对某任务的总效能函数/投标值
    def calculate_subnet_Bid(self, task):
        # 计算子网的攻防能力
        self.calculate_subnet_AD_ability()

        # 计算执行此任务的收益价值reward
        P_destroy = self.attack - task.defense                # 任务目标被摧毁的概率
        reward = task.value * P_destroy / 100  

        # 计算执行此任务的开销成本cost
        P_get_destroyed = task.threat - self.defense               # 子网agent被摧毁的概率
        if P_get_destroyed < 0:
            P_get_destroyed = 0
        cost = self.value * P_get_destroyed / 100                          # 因为是大致计算，所以这里省略了距离因素

        # 计算执行此任务的净效能profit
        profit = (reward - cost) * task.priority

        # 计算对此任务的投标值
        self.currentBid[task.id] = profit


    # 合同网第二级协商：遍历所有子网任务，为每个任务分配一个bestAgent作为contractor
    def second_layer_BID(self):
        # 确定每个agent的待投标任务列表
        self.determine_agent_Bid_list()

        for task in self.subnet_tasks:
            if task.contractor == None:
                bestBid = -(math.inf)
                bestAgent = None
                BID_agents = []
                self.calculate_T_load_ave

                # A、确定参与投标的agent
                for agent in self.subnet_agents:
                    # 判断1：如果该任务不在agent的待投标任务列表中，则退出投标
                    if task not in agent.Bid_list:
                        continue
                    # 判断2：如果agent任务容量已满，则退出投标
                    elif len(agent.contracted_list) == agent.task_capacity:
                        agent.states[task.id] == "DEF_REJ"
                        agent.currentBid[task.id] = -(math.inf)
                        continue
                    # 符合条件的待投标agent，进入投标环节
                    else:
                        # 每个agent进行一次判断，更改投标状态和计算投标值
                        agent.determine_states(task)
                        # 如果该agent的状态是“预投标（PRE_BID）”，则将其加入投标列表BID_agents
                        if agent.states[task.id] == "PRE_BID": 
                            BID_agents.append(agent)
                        # print("agent ", agent.id, " 's state for task ", task.id, " is: ", agent.states[task.id])
                        # 计算投标值
                        agent.calculate_Bid(task, self.T_load_ave)   
                        # print("agent ", agent.id, " 's bid for task ", task.id, " is: ", agent.currentBid[task.id])             
        
                # B、确定bestAgent
                for agent in BID_agents:
                    if(agent.currentBid[task.id] > bestBid):
                        bestBid = agent.currentBid[task.id]
                        bestAgent = agent.id
                                
                # C、确定bestAgent的最终投标状态
                if(bestAgent != None):
                    for agent in BID_agents:
                        if agent.id == bestAgent:                       
                            agent.states[task.id] = "DEF_BID"                # 如果是bestAgent，则该agent中标
                            task.bestBid[agent.id] = bestBid
                        else:
                            agent.states[task.id] = "DEF_REJ"                # 如果不是bestAgent，则该agent流标

                # D、最后更新一次所有agent的状态，如果状态是DEF_BID，则确定为contractor
                for agent in BID_agents:
                    agent.determine_states(task)