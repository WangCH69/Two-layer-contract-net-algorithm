
class Task:
    
    def __init__(self, id, timeConsume, target, value, threat, defense, priority):
        
        # 基础信息
        self.id = id
        self.timeConsume = timeConsume
        self.target = target
        self.value = value
        self.threat = threat
        self.defense = defense
        self.priority = priority

        # 投标相关
        self.contracted_subnet = None           # 承接该任务的subnet
        self.contractor = None                  # 承接该任务的agent
        self.bestBid = {}                       # 承接该任务的agent对应的最佳投标值
    
        