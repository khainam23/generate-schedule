from typing import List
from model.task import Task

class CheckConstraint:
    def __init__(self):
        pass
    
    # Kiểm tra sự trùng lặp 
    def isDuplicate(self, dataFixed: "List[Task]", data: "List[Task]"):
        for df in dataFixed:
            for d in data:
                if (df.isDuplicate(d)):
                    print("🫠 Have duplicate in data fixed and data.")
                    return True
        return False
    
    def checkSpaceTime(self, startTime, endTime):
        # Kiểm tra có là số
        if (not (startTime.isdigit() and endTime.isdigit())):
            print("Not sure input your is number 😫")
            return False
        
        # Chuyển đổi về số để tính toán 
        nsi = int(startTime) # number start time
        nei = int(endTime) # number end time
        
        if (nsi > nei or (nei - nsi < 8)):
            print('Your input not correct or Space time is too small')
            return False
        
        return True