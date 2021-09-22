import car_rental.cars.fleet as fleet
import car_rental.monitor.logger as log
import car_rental.monitor.event as event
import datetime as dt
import json
import os

class Customer:
    def __init__(self, user_name = "anonymous", rented_cars = []):
        self.user_name = user_name
        self.rented_cars = rented_cars

    def get_rental_period(self, car_id):
        count = 0
        event_rent = log.Event_List.get_last_user_and_car_event(self.user_name, car_id, "rental")
        event_return = log.Event_List.get_last_user_and_car_event(self.user_name, car_id, "return")
        if event_rent:
            date_rent = event_rent.get_date()
            f_date_rent = log.Event_List.json_deserialize(date_rent)
            if event_return:
                date_return = event_return.get_date()
                f_date_return = log.Event_List.json_deserialize(date_return)
                if f_date_rent <= f_date_return:
                    print(f"{self.user_name} 고객님은 {f_date_rent}부터 {f_date_return}까지 {car_id}를 총 {(f_date_return.day - f_date_rent.day) + 1}일 동안 렌탈했습니다.")
                else:
                    print(f"{self.user_name} 고객님은 {f_date_rent}에 {car_id} 차량을 렌탈했지만 반환되지 않아 {(log.Event_List.get_today().day - f_date_rent.day) + 1}일 동안 렌탈하고 있습니다.")
                    return 
            else: 
                print(f"{self.user_name} 고객님은 {f_date_rent}에 {car_id} 차량을 렌탈했지만 반환되지 않아 {(log.Event_List.get_today().day - f_date_rent.day) + 1}일 동안 렌탈하고 있습니다.")
        else:
            print(f"{self.user_name} 고객님은 {car_id}를 대여하지 않았습니다.")

class Customers:
    def __init__(self, parent):
        self.users = []
        self.parent = parent
        self.load_clients()
        
    def save_clients(self):
        customer_dict = {"Customer":[ob1.__dict__ for ob1 in self.users]}
        json_str = json.dumps(customer_dict)
        json_file = open("user_data.json", "w")
        json_file.write(json_str)
        json_file.close()

    def load_clients(self):
        if(os.path.isfile("user_data.json")):
            try:
                json_file = open("user_data.json", "r")
                data = json.loads(json_file.read())
                for i in data["Customer"]:
                    item = Customer(**i)
                    self.users.append(item)
                json_file.close()
            except:
                print("파일 불러오는 중 에러가 발생했습니다.")
        else:
            print("불러올 데이터가 없습니다.")
            
    def create_user(self, user_name):
        init_arr = []
        self.users.append(Customer(user_name, init_arr))
        
    def delete_user(self, user_name):
        i = 0
        deleted = False
        for i in range(len(self.users)):
            if self.users[i].user_name == user_name:
                if len(self.users[i].rented_cars) > 0:
                    print("차량을 반환할 때까지 사용자 삭제 불가합니다.")
                    deleted = True
                    break
                else:
                    del self.users[i]
                    print(f"{user_name}님을 삭제했습니다.")
                    deleted = True
                    break
        if deleted == False:
            print("해당 사용자는 존재하지 않습니다.")
    
    def show_users(self):
        for user in self.users:
            print(f"사용자명: {user.user_name}, 렌탈차: {user.rented_cars}")
    
    def get_user(self, user_name):
        count = 0
        for user in self.users:
            if user.user_name == user_name:
                count = count + 1
                return user
        if count == 0:
            print(f"{user_name}이라는 사용자는 없습니다.")
    
    def rent_car(self, user_name, car_id, schedule = ""):
        customer = self.get_user(user_name)
        target = self.parent.fleet.get_car(car_id)
        if target != False:
            if(target.rented == False):
                target.rented = True
                if(target.used == False):
                    target.used = True
                customer.rented_cars.append(target.car_id)
                log.Event_List.add_event(event.Rental_Event(log.Event_List.get_json_now(), car_id, "rental", customer.user_name))
                print(f"{user_name} 고객님이 {car_id} 차량을 렌탈했습니다.")
            else:
                print("이미 렌탈된 차량입니다.")
        else:
            print("해당 아이디의 차가 존재하지 않습니다.")
            
    def return_car(self, user_name, car_id):
        result = False
        customer = self.get_user(user_name)
        target = self.parent.fleet.get_car(car_id)
        if target != False:
            if target.rented == True:
                target.rented = False
                for i in range(len(customer.rented_cars)):
                    if customer.rented_cars[i] == car_id:
                        del customer.rented_cars[i]
                        result = True
                        break
                if (result == True):
                    print(f"{user_name} 고객님이 {car_id} 차량을 반환했습니다.")
                    self.parent.fleet.get_car(car_id).drop_all()
                    log.Event_List.add_event(event.Return_Event(log.Event_List.get_json_now(), car_id, "return", customer.user_name))
                else:
                    print(f"해당 사용자는 {car_id}를 대여하지 않았습니다.")
            
