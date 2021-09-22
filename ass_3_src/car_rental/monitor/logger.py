import datetime as dt
import os
import json
import car_rental.monitor.event as event

class Event_List:
    file_name = "event_log.json"
    log_events = []
 
    @classmethod
    def save_events(cls):
        event_dict = {"Events": [obj.__dict__ for obj in cls.log_events]}
        json_str = json.dumps(event_dict)
        json_file = open(cls.file_name, "w")
        json_file.write(json_str)
        json_file.close()
            
    @classmethod
    def load_events(cls):
        cls.log_events = []
        if(os.path.isfile(cls.file_name)):
            try:
                json_file = open(cls.file_name, "r")
                data = json.loads(json_file.read())
                item = 0
                for i in data["Events"]:
                    if i["event_type"] == "fuel":
                        item = event.Fuel_Event(**i)
                    elif i["event_type"] == "move":
                        item = event.Move_Event(**i)
                    elif i["event_type"] == "rental":
                        item = event.Rental_Event(**i)
                    elif i["event_type"] == "return":
                        item = event.Return_Event(**i)
                    elif i["event_type"] == "add":
                        item = event.Add_Event(**i)
                    elif i["event_type"] == "delete":
                        item = event.Delete_Event(**i)
                    cls.log_events.append(item)
            except:
                print("파일 불러오는 중 에러가 발생했습니다.")
            json_file.close()
        else:
            print("로그 데이터가 없습니다.")
            
    @classmethod      
    def get_car_events(cls, car_id, event_type):
        temp_arr = []
        if  len(cls.log_events) != 0:
            i = 0
            for i in range(len(cls.log_events)):
                if (cls.log_events[i].get_car_id() == car_id) and (cls.log_events[i].get_event_type() == event_type):
                    temp_arr.append(cls.log_events[i])
            return temp_arr
       
    @classmethod      
    def get_events(cls, event_type):
        temp_arr = []
        if  len(cls.log_events) != 0:
            i = 0
            for i in range(len(cls.log_events)):
                if cls.log_events[i].get_event_type() == event_type:
                    temp_arr.append(cls.log_events[i])
            return temp_arr
            
    @classmethod 
    def get_user_events(cls, user, event_type = ""):
        temp_arr = []
        result_arr = []
        if event_type == "":
            temp_arr = cls.get_events("rental") + cls.get_events("return")
        elif event_type == "rental":
            temp_arr = cls.get_events("rental")
        elif event_type == "return":
            temp_arr = cls.get_events("return")
        if  len(temp_arr) != 0:
            i = 0
            for i in range(len(temp_arr)):
                if temp_arr[i].get_user() == user:
                    result_arr.append(temp_arr[i])
            return result_arr
            
    @classmethod 
    def get_user_and_car_events(cls, user, car_id, event_type = ""):
        temp_arr = []
        result_arr = []
        if event_type == "":
            temp_arr = cls.get_car_events(car_id, "rental") + cls.get_car_events(car_id, "return")
        elif event_type == "rental":
            temp_arr = cls.get_car_events(car_id, "rental")
        elif event_type == "return":
            temp_arr = cls.get_car_events(car_id, "return")
        if  len(temp_arr) != 0:
            i = 0
            for i in range(len(temp_arr)):
                if temp_arr[i].get_user() == user:
                    result_arr.append(temp_arr[i])
            return result_arr
            
    @classmethod      
    def get_events_week(cls, event_type):
        temp_arr = []
        if  len(cls.log_events) != 0:
            i = 0
            for i in range(len(cls.log_events)):
                date = cls.json_deserialize(cls.log_events[i].get_date())
                f_date = date.strftime("%Y-%m-%d")
                week = cls.get_date_prior(7).strftime("%Y-%m-%d")
                yesterday = cls.get_date_prior(1).strftime("%Y-%m-%d")
                if (cls.log_events[i].get_event_type() == event_type) and (f_date >= week) and (f_date <= yesterday):
                    temp_arr.append(cls.log_events[i])
            return temp_arr
            
    @classmethod      
    def get_events_range(cls, event_type, from_date, to_date):
        temp_arr = []
        if  len(cls.log_events) != 0:
            i = 0
            for i in range(len(cls.log_events)):
                date = cls.json_deserialize(cls.log_events[i].get_date())
                f_date = date.strftime("%Y-%m-%d")
                if (cls.log_events[i].get_event_type() == event_type) and (f_date >= from_date) and (f_date <= to_date):
                    temp_arr.append(cls.log_events[i])
            return temp_arr
    
    @classmethod
    def get_car_events_week(cls, car_id, event_type):
        temp_arr = []
        if  len(cls.log_events) != 0:
            i = 0
            for i in range(len(cls.log_events)):
                date = cls.json_deserialize(cls.log_events[i].get_date())
                f_date = date.strftime("%Y-%m-%d")
                week = cls.get_date_prior(7).strftime("%Y-%m-%d")
                yesterday = cls.get_date_prior(1).strftime("%Y-%m-%d")
                if (cls.log_events[i].get_car_id() == car_id) and (cls.log_events[i].get_event_type() == event_type) and (f_date >= week) and (f_date <= yesterday):
                    temp_arr.append(cls.log_events[i])
            return temp_arr
            
    @classmethod      
    def get_last_car_event(cls, car_id, event_type):
        event_arr = []
        event_arr = cls.get_car_events(car_id, event_type)
        try: 
            i = len(event_arr) - 1
            if i >= 0:
                return event_arr[i]
        except:
            print(f"{car_id}에 대한 이벤트가 없습니다.")
            return False
            
    @classmethod      
    def get_last_user_and_car_event(cls, user, car_id, event_type):
        event_arr = []
        event_arr = cls.get_user_and_car_events(user, car_id, event_type)
        try: 
            i = len(event_arr) - 1
            if i >= 0:
                return event_arr[i]
        except:
            return False
            
    @classmethod      
    def convert_to_date(cls, date_str):
        f_date = dt.datetime.strptime(date_str,'%Y-%m-%d')   
        return f_date.strftime('%Y-%m-%d')
            
    @classmethod      
    def get_json_now(cls):
        date = dt.datetime.now()
        f_date = date.strftime("%Y-%m-%d %H:%M")
        json_date = json.dumps(f_date)
        return json_date
        
    @classmethod      
    def get_today(cls):
        date = dt.datetime.now()
        f_date = date.strftime("%Y-%m-%d")
        formatted = dt.datetime.strptime(f_date, "%Y-%m-%d")
        return formatted
        
    @classmethod      
    def get_date_prior(cls, days):
        date = dt.datetime.now() - dt.timedelta(days)
        f_date = date.strftime("%Y-%m-%d")
        formatted = dt.datetime.strptime(f_date, "%Y-%m-%d")
        return formatted
    
    @classmethod      
    def json_deserialize(cls, d_str):
        date_str = d_str.strip('"')
        dt_obj = dt.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        return dt_obj
    
    @classmethod     
    def add_event(cls, event_class):
        cls.log_events.append(event_class)