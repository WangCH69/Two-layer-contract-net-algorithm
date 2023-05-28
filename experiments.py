#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# case_1 相关信息
# 地图尺寸：50m X 50m
# 9个无人机：1个一级长机，2个子网长机，2个子网、每个子网有3个agent
# 10个任务

case_1 = {  "subnet_num": 2,
            "subnet_task_capacity": 5,
            "agent_task_capacity": 2,
            "subnet_1_agents": [ # 1号子网
                                {"id": 1, "subnet_id": 1, "speed": 2.0, "initPos": [0.0,1.5], "value": 20, "attack": 40, "defense":20, "pref": 70},
                                {"id": 2, "subnet_id": 1, "speed": 2.0, "initPos": [27.0,11.5], "value": 65, "attack": 85, "defense":35, "pref": 35},
                                {"id": 3, "subnet_id": 1, "speed": 2.0, "initPos": [15.0,18.0], "value": 30, "attack": 50, "defense":50, "pref": 55} ],
            "subnet_2_agents": [ # 2号子网
                                {"id": 4, "subnet_id": 2, "speed": 2.0, "initPos": [22.0,6.0], "value": 50, "attack": 90, "defense":45, "pref": 20},
                                {"id": 5, "subnet_id": 2, "speed": 2.0, "initPos": [5.0,8.5], "value": 25, "attack": 35, "defense":65, "pref": 60},
                                {"id": 6, "subnet_id": 2, "speed": 2.0, "initPos": [30.0,13.0], "value": 45, "attack": 65, "defense":15, "pref": 25} ],
                          
            "tasks": [ { "id": 1, "timeConsume": 25.0, "target": [50.0, 50.0], "value": 80, "threat": 70, "defense": 70, "priority": 10},
                       { "id": 2, "timeConsume": 15.0, "target": [45.0, 8.0], "value": 60, "threat": 45, "defense": 50, "priority": 9},
                       { "id": 3, "timeConsume": 12.0, "target": [40.0, 32.5], "value": 45, "threat": 40, "defense": 35, "priority": 8},
                       { "id": 4, "timeConsume": 20.0, "target": [16.5, 40.0], "value": 40, "threat": 55, "defense": 40, "priority": 7},
                       { "id": 5, "timeConsume": 10.0, "target": [21.0, 13.0], "value": 30, "threat": 30, "defense": 25, "priority": 6},
                       { "id": 6, "timeConsume": 8.0, "target": [34.0, 25.5], "value": 25, "threat": 25, "defense": 30, "priority": 5},
                       { "id": 7, "timeConsume": 6.0, "target": [18.0, 42.5], "value": 20, "threat": 8, "defense": 15, "priority": 4},
                       { "id": 8, "timeConsume": 10.0, "target": [25.0, 12.0], "value": 15, "threat": 20, "defense": 25, "priority": 3}, 
                       { "id": 9, "timeConsume": 5.0, "target": [2.0, 18.0], "value": 10, "threat": 10, "defense": 20, "priority": 2},
                       { "id": 10, "timeConsume": 5.0, "target": [8.0, 21.5], "value": 5, "threat": 15, "defense": 20, "priority": 1} ]
            } 



# case_2 相关信息
# 地图尺寸：100m X 100m
# 12个无人机：1个一级长机，3个子网长机，3个子网、每个子网有4个agent
# 20个任务

case_2 = {  "subnet_num": 3,
            "subnet_task_capacity": 8,
            "agent_task_capacity": 2,
            "subnet_1_agents": [ # 1号子网
                                {"id": 1, "subnet_id": 1, "speed": 2.0, "initPos": [0.0,1.5], "value": 10, "attack": 30, "defense":20, "pref": 70},
                                {"id": 2, "subnet_id": 1, "speed": 2.0, "initPos": [27.0,11.5], "value": 65, "attack": 80, "defense":55, "pref": 35},
                                {"id": 3, "subnet_id": 1, "speed": 2.0, "initPos": [15.0,28.0], "value": 30, "attack": 50, "defense":30, "pref": 21},
                                {"id": 4, "subnet_id": 1, "speed": 2.0, "initPos": [42.0,6.0], "value": 50, "attack": 72, "defense":48, "pref": 20}  ],
            "subnet_2_agents": [ # 2号子网
                                {"id": 5, "subnet_id": 2, "speed": 2.0, "initPos": [5.0,8.5], "value": 25, "attack": 35, "defense":15, "pref": 60},
                                {"id": 6, "subnet_id": 2, "speed": 2.0, "initPos": [34.0,13.0], "value": 95, "attack": 95, "defense":75, "pref": 15},
                                {"id": 7, "subnet_id": 2, "speed": 2.0, "initPos": [45.5,37.0], "value": 40, "attack": 57, "defense":26, "pref": 46},
                                {"id": 8, "subnet_id": 2, "speed": 2.0, "initPos": [56.0,26.5], "value": 35, "attack": 49, "defense":38, "pref": 50} ],
            "subnet_3_agents": [ # 3号子网
                                {"id": 9, "subnet_id": 3, "speed": 2.0, "initPos": [9.5,36.0], "value": 80, "attack": 90, "defense":55, "pref": 10},
                                {"id": 10, "subnet_id": 3, "speed": 2.0, "initPos": [75.0,58.5], "value": 15, "attack": 25, "defense":45, "pref": 30},
                                {"id": 11, "subnet_id": 3, "speed": 2.0, "initPos": [90.0,43.0], "value": 5, "attack": 18, "defense":7, "pref": 60},
                                {"id": 12, "subnet_id": 3, "speed": 2.0, "initPos": [60.0,66.0], "value": 50, "attack": 53, "defense":28, "pref": 36}  ],
                          
            "tasks": [ { "id": 1, "timeConsume": 35.0, "target": [80.0, 80.0], "value": 80, "threat": 70, "defense": 70, "priority": 10},
                       { "id": 2, "timeConsume": 42.0, "target": [75.0, 68.0], "value": 95, "threat": 90, "defense": 80, "priority": 10},
                       { "id": 3, "timeConsume": 32.4, "target": [90.0, 32.5], "value": 75, "threat": 70, "defense": 35, "priority": 9},
                       { "id": 4, "timeConsume": 30.0, "target": [46.5, 40.1], "value": 70, "threat": 75, "defense": 40, "priority": 9},
                       { "id": 5, "timeConsume": 28.2, "target": [61.0, 13.6], "value": 68, "threat": 67, "defense": 25, "priority": 8},
                       { "id": 6, "timeConsume": 23.5, "target": [68.0, 45.2], "value": 60, "threat": 65, "defense": 30, "priority": 8},
                       { "id": 7, "timeConsume": 26.0, "target": [19.0, 92.5], "value": 62, "threat": 58, "defense": 34, "priority": 7},
                       { "id": 8, "timeConsume": 20.9, "target": [25.0, 87.7], "value": 59, "threat": 80, "defense": 45, "priority": 7}, 
                       { "id": 9, "timeConsume": 18.7, "target": [2.0, 18.0], "value": 53, "threat": 50, "defense": 20, "priority": 6},
                       { "id": 10, "timeConsume": 23.0, "target": [8.0, 21.5], "value": 47, "threat": 45, "defense": 30, "priority": 6},
                       { "id": 11, "timeConsume": 30.0, "target": [13.0, 74.5], "value": 45, "threat": 42, "defense": 27, "priority": 5},
                       { "id": 12, "timeConsume": 35.3, "target": [21.0, 59.5], "value": 40, "threat": 38, "defense": 32, "priority": 5},
                       { "id": 13, "timeConsume": 15.0, "target": [31.6, 21.5], "value": 35, "threat": 35, "defense": 24, "priority": 4},
                       { "id": 14, "timeConsume": 5.0, "target": [48.0, 33.7], "value": 29, "threat": 30, "defense": 20, "priority": 4},
                       { "id": 15, "timeConsume": 8.0, "target": [52.0, 42.5], "value": 25, "threat": 25, "defense": 17, "priority": 3},
                       { "id": 16, "timeConsume": 12.0, "target": [38.0, 66.0], "value": 18, "threat": 20, "defense": 20, "priority": 3},
                       { "id": 17, "timeConsume": 15.0, "target": [88.0, 11.5], "value": 15, "threat": 15, "defense": 19, "priority": 2},
                       { "id": 18, "timeConsume": 9.7, "target": [57.6, 51.5], "value": 8, "threat": 11, "defense": 14, "priority": 2},
                       { "id": 19, "timeConsume": 7.5, "target": [55.0, 7.5], "value": 6, "threat": 8, "defense": 10, "priority": 1},
                       { "id": 20, "timeConsume": 3.0, "target": [28.0, 6.5], "value": 5, "threat": 5, "defense": 4, "priority": 1} ]
            } 