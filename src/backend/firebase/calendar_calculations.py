import firebase
from datetime import datetime
import ast

class calendar:
    def __init__(self):
        self.schedule = []
        self.weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        self.dates = []

    def retrieve_schedule(self, name):
        curr_date = datetime.today().day
        print(curr_date)
        curr_day = datetime.today().weekday()
        print(curr_day)
        db = firebase.db
        medicine_dict = db.collection(name).document("medicine").get().to_dict()
        for key, value in medicine_dict.items():
            idxs = [self.weekdays.index(day) for day in ast.literal_eval(value[1])['days']]
            for idx in idxs:
                if idx < curr_day:
                    days_until = 7 - curr_day + idx
                    self.dates.append(curr_date + days_until)
                else:
                    days_until = idx - curr_day
                    self.dates.append(curr_date + days_until)
            time = ast.literal_eval(value[1])['time']
            self.schedule.append({key:[self.dates, time]})
#         print(self.schedule)
    
# cal = calendar()
# cal.retrieve_schedule('Sonic')