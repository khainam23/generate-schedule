from check_contraint import CheckConstraint
from task import Task
from generate_schedule import GenerateSchedule
from export import Export

def breakSpace(n = 10):
    print('*' * n)
    
def inputNumberTask(n, type: bool = False):
    data = []
    for i in n:
        # Tên công việc
        name = input("💁‍♂️ Your name for task: ")
        
        # Thứ trong tuần thực hiện
        if type:
            day = input("Your day work taks: ")
            while(not (day.isdigit() and 1 < int(day) < 8)):
                print("Hmm, may be i not found this")
                day = input("Write day again: ")
            
        # Thời gian tối đa dự đoán 
        maxTime = input("Your max time for this task: ")
        while(not maxTime.isdigit()):
            print("No that is not a number")
            maxTime = input("Try agin, enter max time for this task: ")
            
        # Giờ thực hiện 
        if type:
            hour = input("Hour (0 - 24): ")
            while(not (hour.isdigit() and 0 < int(hour) < 24)):
                print("That is not a number")
                hour = input("Try agin, enter hour for this task: ")
        
        if type:
            data.append(Task(name, maxTime, day, hour))
        else:
            data.append(Task(name=name, maxTime=maxTime))
            
    return data

def __main__():
    # Câu chào ban đầu
    print('Auto generate schedule 💁‍♂️')
    
    # Tên của thời biểu 
    name = input('Your name schedule: ')
    while(not name):
        print("Opps, it's empty 😓")
        name = input('Please enter your name again: ')
        
    # Khởi tạo kiểm tra ràng buộc
    validate = CheckConstraint()
    
    breakSpace()
    
    # Thời gian dự tính
    startTime = input("Start time: ")
    endTime = input("End time: ")
    while(not validate.checkSpaceTime(startTime, endTime)):
        print("🐧 Your enter not correct!!!")
        startTime = input("Enter start time again: ")
        endTime = input("Enter end time again: ")
        
    # Nhập khung thời gian cố định
    ntf = input('Your number tasks fixed: ') # number tasks fixed
    while(not ntf.isdigit()):
        print("You can't enter input not a number here 😡")
        ntf = input('Please enter number for tasks fixed: ')
    dataFixed = inputNumberTask(ntf, type=True)
    
    # Nhập khung thời gian linh động
    ntd = input('Your number tasks dynamic: ') # number tasks dynamic
    while(not ntd.isdigit()):
        print("I tired, please enter number 🙂")
        ntd = input("Number tasks dynamic again: ")
    data = inputNumberTask(ntd)
    
    # Kiểm tra có bị trùng lên nhau 
    if validate.isDuplicate(dataFixed=dataFixed, data=data):
        print('🤔 Sorry but schedule of you is duplicate.')
        return
        
    # Khởi tạo class tạo ra thời biểu 
    days = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thurday',
        'Friday',
        'Staturday',
        'Sunday'
    ]
    duration = 1
    shortBreak = 15 # minutes
    longBreak = 1 # hour
    gs = GenerateSchedule(days, startTime, endTime, duration, shortBreak, longBreak, dataFixed, data) # generate schedule
    
    # Sinh ra thời biểu 
    schedule = gs.generate()
    
    print(schedule)
    
    # Khởi tạo công cụ xuất
    export = Export(schedule, days, startTime, duration)
    
    # Lựa chọn nguồn xuất
    export.export(type = "excel")
    
__main__()