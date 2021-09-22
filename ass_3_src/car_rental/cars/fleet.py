import json
import os
import car_rental.cars.car as base
import car_rental.monitor.logger as log
import car_rental.monitor.event as event
import datetime as dt

class Fleet:
    def __init__(self):
        self.cars = []
        self.load_fleet()

    def save_fleet(self):
        fleet_dict = {"Fleet":[ob1.__dict__ for ob1 in self.cars]}
        json_str = json.dumps(fleet_dict)
        json_file = open("car_data.json", "w")
        json_file.write(json_str)
        json_file.close()

    def load_fleet(self):
        if(os.path.isfile("car_data.json")):
            try:
                self.cars = []
                json_file = open("car_data.json", "r")
                data = json.loads(json_file.read())
                for i in data["Fleet"]:
                    if(i["brand"] == "Sonata"):
                        item = base.Sonata(**i)
                    elif(i["brand"] == "Tucson"):
                        item = base.Tucson(**i)
                    elif(i["brand"] == "Bongo"):
                        item = base.Bongo(**i)
                    elif(i["brand"] == "Tesla_S"):
                        item = base.Tesla_S(**i)
                    self.cars.append(item)
                json_file.close()
            except:
                print("파일 불러오는 중 에러가 발생했습니다.")
        else:
            print("불러올 데이터가 없습니다.")
        
    def add_car(self, car_id, brand, used_state = False):
        event_dict = {}
        if(brand == "Sonata"):
            self.cars.append(base.Sonata(car_id, used = used_state))
            log.Event_List.add_event(event.Add_Event(log.Event_List.get_json_now(), car_id, "add"))
            print(f"{car_id} 차량이 추가되었습니다.")
        elif(brand == "Tucson"):
            self.cars.append(base.Tucson(car_id, used = used_state))
            log.Event_List.add_event(event.Add_Event(log.Event_List.get_json_now(), car_id, "add"))
            print(f"{car_id} 차량이 추가되었습니다.")
        elif(brand == "Bongo"):
            self.cars.append(base.Bongo(car_id, used = used_state))
            log.Event_List.add_event(event.Add_Event(log.Event_List.get_json_now(), car_id, "add"))
            print(f"{car_id} 차량이 추가되었습니다.")
        elif(brand == "Tesla_S"):
            self.cars.append(base.Tesla_S(car_id, used = used_state))
            log.Event_List.add_event(event.Add_Event(log.Event_List.get_json_now(), car_id, "add"))
            print(f"{car_id} 차량이 추가되었습니다.")
        else:
            print("자동차 브랜드는 Sonata, Tucson, Bongo, Tesla_S 중에서만 선택 가능합니다.")
        
    
    def del_car(self, car_id):
        i = 0
        for i in range(len(self.cars)):
            if(self.cars[i].car_id == car_id):
                if(self.cars[i].rented == False):
                    del self.cars[i]
                    log.Event_List.add_event(event.Delete_Event(log.Event_List.get_json_now(), car_id, "delete"))
                    print(f"{car_id} 차량이 폐차되었습니다.")
                    break;
                else:
                    print("현재 렌털된 차량으로 폐차할 수 없습니다.")
                    break;
                    
    def get_car(self, car_id):
        result = False
        for car in self.cars:
            if car.car_id == car_id:
                result = True
                return car
        if result == False:
            return False
                
    def get_rented_week(self):
        temp_arr = []
        event_arr = []
        event_arr = log.Event_List.get_events_week("rental")
        for car in self.cars:
            if car.rented == True:
                event_date = log.Event_List.json_deserialize(log.Event_List.get_last_car_event(car.car_id, "rental").get_date())
                f_date = event_date.strftime("%Y-%m-%d")
                n_date = dt.datetime.now().strftime("%Y-%m-%d")
                if f_date != n_date:
                    temp_arr.append(car)
            else:
                for event in event_arr:
                    if event.get_car_id() == car.car_id:
                        temp_arr.append(car)
        return temp_arr
        
    def show_all(self):
        print("모든 차량 목록: ")
        for car in self.cars:
            if car.used:
                status = "중고"
            else:
                status = "신차"
            car.show_state()
            
    def show_available(self):
        print("대여 가능한 차량 목록: ")
        for car in self.cars:
            if car.rented == False:
                if car.used:
                    status = "중고"
                else:
                    status = "신차"
                car.show_state()
                
    def show_rented(self):
        print("대여 중인 차량 목록: ")
        for car in self.cars:
            if car.rented == True:
                if car.used:
                    status = "중고"
                else:
                    status = "신차"
                car.show_state()
                
    def get_best_match(self, brand = "", fuel = "", fuel_economy = "", mileage = "", used_state = "", passengers = "", load = ""):
        points = []
        for i in range(len(self.cars)):
            val = 0
            if self.cars[i].rented == False:
                val = val + 1
                if brand != "":
                    if self.cars[i].brand == brand:
                        val = val + 1
                if fuel != "":
                    if self.cars[i].max_fuel >= fuel:
                        val = val + 1
                if fuel_economy != "":
                    if self.cars[i].fe_org >= fuel_economy:
                        val = val + 1
                if mileage != "":
                    if self.cars[i].mlg <= mileage:
                        val = val + 1
                if used_state != "":
                    if self.cars[i].used == used_state:
                        val = val + 1
                if passengers != "" and load != "":
                    if self.cars[i].cap >= passengers:
                        val = val + 0.5
                    if self.cars[i].load >= load:
                        val = val + 0.5
                elif passengers == "" and load != "":
                    if self.cars[i].load >= load:
                        val = val + 1                   
                elif passengers != "" and load == "":
                    if self.cars[i].cap >= passengers:
                        val = val + 1                    
            points.append(val)
        index = points.index(max(points))
        if max(points) == 0:
            print(f"고객님의 요구사항과 맞는 차량이 없거나 모두 렌탈 중입니다.")
        else:
            print(f"고객님의 요구사항과 가장 맞는 차량은 {self.cars[index].car_id}입니다.")
        