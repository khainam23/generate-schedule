import numpy as np
from typing import List
from task import Task

class GenerateSchedule:
    def __init__(self, days: List[str], startTime, endTime, duration, shortBreak, longBreak, dataFixed: List[Task], data: List[Task]):
        self.days = days
        self.startTime = float(startTime)
        self.endTime = float(endTime)
        self.duration = float(duration)
        self.shortBreak = float(shortBreak)
        self.longBreak = float(longBreak)
        self.dataFixed = dataFixed
        self.data = data

    def insertIntoSchedule(self, schedule, task: Task, fixed: bool = False):
        """ Chèn task vào lịch trình, ưu tiên ngày đầu nếu maxTime <= 4 """
        if fixed:
            day, hour = map(int, task.getNormalInfo())
            schedule[day][hour] = task.name
            return
        
        max_limit = 4
        priority_days = [0] if task.maxTime <= max_limit else range(len(self.days))

        for day in priority_days:
            for hour in range(0, schedule.shape[1], int(self.duration)):
                if all(schedule[day][h] == 0 for h in range(hour, min(hour + int(task.maxTime), schedule.shape[1]))):
                    if all(schedule[day][h] == 0 for h in range(max(0, hour - 3), hour)):  
                        schedule[day][hour:hour + int(task.maxTime)] = task.name
                        return

        # Nếu không tìm được vị trí, xét lại các ngày còn lại
        for day in range(1, len(self.days)):  
            for hour in range(0, schedule.shape[1], int(self.duration)):
                if all(schedule[day][h] == 0 for h in range(hour, min(hour + int(task.maxTime), schedule.shape[1]))):
                    if all(schedule[day][h] == 0 for h in range(max(0, hour - 3), hour)):  
                        schedule[day][hour:hour + int(task.maxTime)] = task.name
                        return

    def generate(self):
        """ Tạo lịch trình với thời gian chia theo duration """
        rows = int((self.endTime - self.startTime) / self.duration)  
        cols = len(self.days)  

        schedule = np.zeros((rows + 1, cols + 1), dtype=object)
        schedule[0, 1:] = self.days  
        schedule[1:, 0] = [self.startTime + i * self.duration for i in range(rows)]  

        for task in self.dataFixed:
            self.insertIntoSchedule(schedule, task, True)
        
        for task in self.data:
            self.insertIntoSchedule(schedule, task)

        return schedule