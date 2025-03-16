class Task:
    def __init__(self, name, maxTime, day = 0, hour = 0):
        self.name = name 
        self.day = day
        self.maxTime = float(maxTime)
        self.hour = hour
        
    def getNormalInfo(self):
        return (
            self.day,
            self.hour
        )
        
    # Kiểm tra về sự trùng lặp thông tin với task khác 
    def isDuplicate(self, other: "Task"):
        return self.getNormalInfo() == other.getNormalInfo()
