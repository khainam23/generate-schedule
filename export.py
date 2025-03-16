import pandas as pd

class Export:
    def __init__(self, schedule, days, startTime, duration):
        # Có thể xem cấu tạo của schedule ở `data.json`
        self.schedule = schedule
        self.days = days
        self.startTime = float(startTime)
        self.duration = float(duration)
        
    def export(self, fileName = '', type = "excel"):
        if type == "excel":
            return self.excel()
        pass
        
    def excel(self, fileName = "schedule_excel.xlsx"):
        sheetName = "Schedule"
        
        dataExcel = pd.DataFrame(self.schedule)
        
        dataExcel.to_excel(
            fileName,
            sheet_name=sheetName
        )