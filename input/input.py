import json
from enum import Enum

from constraint.check_contraint import CheckConstraint
from model.task import Task
from generate.generate_schedule import GenerateSchedule
from export.export import Export

class Type(Enum):
    ENTER = "enter"
    JSON = "json"

class Input:
    def __init__(self, inputType: Type):
        self.inputType = inputType

    def run(self):
        method = getattr(self, self.inputType.value, None)
        if callable(method):
            method()

    @staticmethod
    def breakSpace(n=10):
        print('*' * n)

    @staticmethod
    def inputNumber(prompt, min_val=None, max_val=None):
        """ Nhập số nguyên và kiểm tra giới hạn nếu có """
        while True:
            try:
                num = int(input(prompt))
                if (min_val is None or num >= min_val) and (max_val is None or num <= max_val):
                    return num
            except ValueError:
                pass
            print("❌ Invalid input, try again!")

    def inputTaskList(self, numTask, fixed=False):
        """ Nhập danh sách công việc """
        tasks = []
        for _ in range(numTask):
            name = self.getNonEmptyInput("💁‍♂️ Task name: ")
            max_time = self.inputNumber("⏳ Max time (minutes): ")
            
            if fixed:
                day = self.inputNumber("📅 Day (1-7): ", 1, 7)
                hour = self.inputNumber("⏰ Hour (0-23): ", 0, 23)
                tasks.append(Task(name, max_time, day, hour))
            else:
                tasks.append(Task(name=name, maxTime=max_time))
        return tasks

    @staticmethod
    def getNonEmptyInput(prompt):
        """ Đảm bảo nhập vào không rỗng """
        value = input(prompt).strip()
        while not value:
            print("❌ This field cannot be empty!")
            value = input(prompt).strip()
        return value

    def enter(self):
        print("📅 Auto generate schedule 💁‍♂️")

        name = self.getNonEmptyInput("📝 Schedule name: ")

        validate = CheckConstraint()
        self.breakSpace()

        startTime, endTime = self.getValidTime(validate)

        numFixed = self.inputNumber("📌 Number of fixed tasks: ")
        fixedTasks = self.inputTaskList(numFixed, fixed=True)

        numDynamic = self.inputNumber("🔄 Number of dynamic tasks: ")
        dynamicTasks = self.inputTaskList(numDynamic)

        if validate.isDuplicate(dataFixed=fixedTasks, data=dynamicTasks):
            print("🤔 Sorry, your schedule has duplicate tasks.")
            return

        self.generateAndExportSchedule(name, startTime, endTime, fixedTasks, dynamicTasks)

    def json(self):
        """ Nhập dữ liệu từ file JSON """
        file_path = input("📂 Enter JSON file path: ").strip()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            name = data.get("name", "Untitled Schedule")
            start_time = data["start_time"]
            end_time = data["end_time"]
            fixed_tasks = [Task(**task) for task in data.get("fixed_tasks", [])]
            dynamic_tasks = [Task(**task) for task in data.get("dynamic_tasks", [])]

            validate = CheckConstraint()
            if validate.isDuplicate(dataFixed=fixed_tasks, data=dynamic_tasks):
                print("🤔 Sorry, your schedule has duplicate tasks.")
                return

            self.generateAndExportSchedule(name, start_time, end_time, fixed_tasks, dynamic_tasks)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ Error reading JSON file: {e}")

    def getValidTime(self, validate):
        """ Nhập và kiểm tra thời gian hợp lệ """
        while True:
            start_time = input("⏳ Start time: ").strip()
            end_time = input("⏳ End time: ").strip()
            if validate.checkSpaceTime(start_time, end_time):
                return start_time, end_time
            print("❌ Invalid time range!")

    def generateAndExportSchedule(self, name, start_time, end_time, fixed_tasks, dynamic_tasks):
        """ Khởi tạo, tạo lịch trình và xuất file """
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        gs = GenerateSchedule(days, start_time, end_time, duration=1, shortBreak=15, longBreak=60,
                              dataFixed=fixed_tasks, data=dynamic_tasks)

        schedule = gs.generate()
        print(schedule)

        Export(schedule, days, start_time, duration=1).export(type="excel")