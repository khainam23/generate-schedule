import numpy as np
import random
from typing import List
from model.task import Task

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

    def insertIntoSchedule(self, schedule, task: Task, taskPositions, fixed: bool = False):
        """ Chèn task vào lịch trình, đảm bảo không có 2 task giống nhau gần nhau (cách ít nhất 3 giờ) """
        
        if fixed:
            (day, hour) = map(int, task.getNormalInfo())
            schedule[hour][day] = task.name
            if task.name not in taskPositions:
                taskPositions[task.name] = []
            taskPositions[task.name].append((day, hour))
            return

        def isValidPosition(day, hour):
            """ Kiểm tra xem task có thể đặt vào vị trí này không """
            if not all(schedule[h][day] == 0 for h in range(hour, min(hour + int(task.maxTime), schedule.shape[0]))):
                return False

            for (prevDay, prevHour) in taskPositions.get(task.name, []):
                prevTime = self.startTime + prevHour * self.duration
                currTime = self.startTime + hour * self.duration
                if prevDay == day and abs(currTime - prevTime) < 3:
                    return False

            return True

        possible_positions = []

        for day in range(len(self.days)):
            for hour in range(0, schedule.shape[0]):
                if isValidPosition(day, hour):
                    possible_positions.append((day, hour))

        if possible_positions:
            chosen_day, chosen_hour = random.choice(possible_positions)
            schedule[chosen_hour:chosen_hour + int(task.maxTime), chosen_day] = task.name
            if task.name not in taskPositions:
                taskPositions[task.name] = []
            taskPositions[task.name].append((chosen_day, chosen_hour))

    def generate(self):
        """ Tạo lịch trình với thời gian chia theo duration """
        rows = int((self.endTime - self.startTime) / self.duration)  
        cols = len(self.days)  

        schedule = np.zeros((rows + 1, cols + 1), dtype=object)
        schedule[0, 1:] = self.days  
        schedule[1:, 0] = [self.startTime + i * self.duration for i in range(rows)]
        
        taskPositions = {}

        for task in self.dataFixed:
            self.insertIntoSchedule(schedule, task, taskPositions, True)
        
        random.shuffle(self.data)
        
        for task in self.data:
            self.insertIntoSchedule(schedule, task, taskPositions)

        return schedule