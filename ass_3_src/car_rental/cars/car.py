import car_rental.monitor.logger as log
import car_rental.monitor.event as event

class Car:
    def __init__(self, car_id, brand, max_fuel, fe_org, max_cap, fuel = 0, fe_100 = 0, cap = 0, mlg = 0, used = False, rented = False):
        self.car_id = car_id
        self.brand = brand
        self.max_fuel = max_fuel
        self.fe_org = fe_org
        self.max_cap = max_cap
        self.fuel = fuel
        self.fe_100 = fe_100
        self.cap = cap
        self.mlg = mlg
        self.used = used
        self.rented = rented
        
        if mlg == 0:
            if self.used:
                self.fuel = self.max_fuel * 0.3
                self.mlg = 50000
            else:
                self.fuel = self.max_fuel
                self.mlg = 0
                
    def fill_up(self):
        if self.fuel != self.max_fuel:
            amount = self.max_fuel - self.fuel
            self.fuel = self.max_fuel
            print(f"{self.car_id} 차량에 {amount:.2f}리터를 주유했습니다.")
            log.Event_List.add_event(event.Fuel_Event(log.Event_List.get_json_now(), self.car_id, "fuel", amount, self.rented))
        else:
            print(f"{self.car_id} 차량에 더이상 주유할 수 없습니다.")
        
    def fill(self, amt):
        if self.fuel != self.max_fuel:
            amt_sum = self.fuel + amt
            if amt_sum <= self.max_fuel:
                self.fuel = amt_sum
                amount = amt_sum
                print(f"{self.car_id} 차량에 {amount:.2f}리터를 주유했습니다.")
            else:
                amount = self.max_fuel - self.fuel
                self.fuel = self.max_fuel
                print(f"{self.car_id} 차량의 최대치를 초과하여 {amount:.2f}리터를 주유했습니다.")
            log.Event_List.add_event(event.Fuel_Event(log.Event_List.get_json_now(), self.car_id, "fuel", amount, self.rented))
        else:
            print(f"{self.car_id} 차량에 더이상 주유할 수 없습니다.")
            
    def ride(self, num):
        if(num > 0):
            n_sum = self.cap + num
            if n_sum <= self.max_cap:
                self.cap = n_sum
                print(f"{self.car_id} 차량에 {num}명이 탑승했습니다.")
            else:
                print(f"{self.car_id} 차량의 무게 초과로 탑승 불가합니다.")
        else:
            print("양수를 입력해주세요.")
    
    def drop(self, num):
        if num > 0: 
            if num <= self.cap:
                self.cap = self.cap - num
                print(f"{self.car_id} 차량에서 {num}명이 내렸습니다.")
            else:
                print(f"{self.car_id} 차량에 탑승한 인원보다 많이 내릴 수 없습니다.")
        else:
            print("양수를 입력해주세요.")
            
    def drop_all(self):
        self.cap = 0
        print("모든 승객이 내렸습니다.")
    
    def get_range(self):
        return self.fuel * self.get_cur_fe()
    
    def get_cur_fe(self):
            return self.fe_org - (self.cap/self.max_cap) * self.fe_org * 0.1
    
    def move(self, dist:int):
        event_dict = {}
        if self.fuel != 0:
            max_dist = self.get_range()
            if self.used != True:
                self.used = True
            if dist <= max_dist:
                fuel_used = dist / self.get_cur_fe()
                self.fuel = self.fuel - fuel_used
                self.mlg = self.mlg + dist
                result = dist
                print(f"{self.car_id} 차량은 {result:.2f}km 주행했습니다.")
            else:
                self.fuel = 0
                self.mlg = self.mlg + max_dist
                result = max_dist
                print(f"{self.car_id} 차량은 {result:.2f}km 주행하다 멈췄습니다.")
            
            fe_cur = self.get_cur_fe()
            log.Event_List.add_event(event.Move_Event(log.Event_List.get_json_now(), self.car_id, "move", result, fe_cur, self.rented))
            self.set_fe_100()
        else:
            print(f"{self.car_id} 차량에 연료가 없습니다.")
        
    def set_fe_100(self):
        event_arr = log.Event_List.get_car_events(self.car_id, "move")
        n = 0
        n = len(event_arr)
        dt_sum = 0
        fe_sum = 0
        prev_sum = 0
        if(n -1) > 0:
            i = n-1    
            for i in range(n-1, -1, -1):
                dt_sum = dt_sum + event_arr[i].distance
                if dt_sum == 100:
                    fe_sum = fe_sum + (event_arr[i].fe * (event_arr[i].distance / 100))
                    break
                elif dt_sum > 100:
                    fe_sum = fe_sum + (event_arr[i].fe * ((100 - prev_sum) / 100))
                    break
                else:
                    fe_sum = fe_sum + (event_arr[i].fe * (event_arr[i].distance / 100))
                    prev_sum = dt_sum
            self.fe_100 = fe_sum
            return fe_sum
        else:
            self.fe_100 = self.get_cur_fe()
            return self.get_cur_fe()
            
    def get_fe_100(self):
        return self.fe_100
        
    def get_mlg(self):
        return self.mlg
    
    def get_fuel(self):
        return self.fuel
    
    def get_cap(self):
        return self.cap
        
class Sonata(Car):   
    def __init__(self, car_id, brand = "Sonata", max_fuel = 55, fe_org = 12, max_cap = 4, fuel = 0, fe_100 = 0, cap = 0, mlg = 0, used = False, rented = False):
        super().__init__(car_id, brand, max_fuel, fe_org, max_cap, fuel, fe_100, cap, mlg, used, rented)

    def show_dash(self):
        print(f"{self.car_id}의 대시보드")
        print(f"총 운행거리 : {self.get_mlg():.2f}km")
        print(f"현재 연료량 : {self.get_fuel():.2f}리터")
        print(f"현재 연료량으로 주행 가능 거리 : {self.get_range():.2f}km")
        print(f"최근 100km 주행 간 연비 : {self.get_fe_100():.2f}km/l")
        print(f"탑승인원 : {self.get_cap()}명")
        print()
        
    def show_state(self):
        if self.used == True:
            used_state = "중고"
        else:
            used_state = "신차"
        print(f"id: {self.car_id}, 차종: {self.brand}, 최대 연료량: {self.max_fuel}리터, 연비: {self.fe_org}km/l, 최대 탑승인웡: {self.max_cap}명, 렌탈여부: {self.rented}, 마일리지: {self.mlg}km, 상태: {used_state}")
        
class Tucson(Car):
    def __init__(self, car_id, brand = "Tucson", max_fuel = 60, fe_org = 10, max_cap = 5, fuel = 0, fe_100 = 0, cap = 0, mlg = 0, used = False, rented = False, max_load = 500, load = 0):
        super().__init__(car_id, brand, max_fuel, fe_org, max_cap, fuel, fe_100, cap, mlg, used, rented)
        self.max_load = max_load
        self.load = load
        
    def ride(self, cap:int, load:int):
        if (cap >= 0 ) and (load >= 0):
            cap_sum = self.cap + cap
            load_sum = self.load + load
            if cap_sum <= self.max_cap and load_sum <= self.max_load:
                self.cap = cap_sum
                self.load = load_sum
                print(f"{self.car_id} 차량에 {cap}명이 타고 {load}kg을 적재했습니다.")
            else:
                print(f"{self.car_id} 차량의 무게 초과로 탑승 불가합니다.")
        else:
            print("양수를 입력해주세요.")
            
    def drop(self, cap:int, load:int):
        if (cap >= 0 ) and (load >= 0):
            if (cap <= self.cap) and (load <= self.load):
                self.cap = self.cap - cap
                self.load = self.load - load
                print(f"{self.car_id} 차량에서 {cap}명과 {load}kg을 내렸습니다.")
            else:
                print(f"{self.car_id} 차량에 탑승/적재된 인원/무게보다 많은 인원/무게를 내릴 수 없습니다.")
        else:
            print("양수를 입력해주세요.")
            
    def drop_all(self):
        self.cap = 0
        self.load = 0
        print("모든 승객과 적재물을 내렸습니다.")
            
    def get_cur_fe(self):
        calc_a = ((self.cap / self.max_cap) * self.fe_org * 0.1) * 0.5
        calc_b = ((self.load / self.max_load) * self.fe_org * 0.1) * 0.5
        return self.fe_org - (calc_a + calc_b)
    
    def show_dash(self):
        print(f"{self.car_id}의 대시보드")
        print(f"총 운행거리 : {self.get_mlg():.2f}km")
        print(f"현재 현재 연료량 : {self.get_fuel():.2f}리터")
        print(f"현재 현재 연료량으로 주행 가능 거리 : {self.get_range():.2f}km")
        print(f"최근 100km 주행 간 연비 : {self.get_fe_100():.2f}km/l")
        print(f"탑승인원 및 적재무게: {self.get_cap()}명, {self.load}kg")
        print()
        
    def show_state(self):
        if self.used == True:
            used_state = "중고"
        else:
            used_state = "신차"
        print(f"id: {self.car_id}, 차종: {self.brand}, 최대 연료량: {self.max_fuel}리터, 연비: {self.fe_org}km/l, 최대 탑승인웡: {self.max_cap}명, 최대 적재무게: {self.max_load}kg, 렌탈여부: {self.rented}, 마일리지: {self.mlg}km, 상태: {used_state}")
        
class Bongo(Car):
    def __init__(self, car_id, brand = "Bongo", max_fuel = 55, fe_org = 11, max_cap = 0, fuel = 0, fe_100 = 0, cap = 0, mlg = 0, used = False, rented = False, max_load = 700, load = 0):
        super().__init__(car_id, brand, max_fuel, fe_org, max_cap, fuel, fe_100, cap, mlg, used, rented)
        self.max_load = max_load
        self.load = load
        
    def ride(self, load:int):
        if load >= 0:
            load_sum = self.load + load
            if load_sum <= self.max_load:
                self.load = load_sum
                print(f"{self.car_id} 차량에 {load}kg을 적재했습니다.")
            else:
                print(f"{self.car_id} 차량의 무게 초과로 적재 불가합니다.")
        else:
            print("양수를 입력해주세요.")
            
    def drop(self, load:int):
        if load >= 0:
            if load <= self.load:
                self.load = self.load - load
                print(f"{self.car_id} 차량에서 {load}kg을 내렸습니다.")
            else:
                print(f"{self.car_id} 차량에 적재된 무게보다 많은 무게를 내릴 수 없습니다.")
        else:
            print("양수를 입력해주세요.")
    
    def drop_all(self):
        self.load = 0
        print("모든 적재물을 내렸습니다.")
        
    def get_cur_fe(self):
        calc_b = ((self.load / self.max_load) * self.fe_org * 0.1)
        return self.fe_org - calc_b
       
    def show_dash(self):
        print(f"{self.car_id}의 대시보드")
        print(f"총 운행거리 : {self.get_mlg():.2f}km")
        print(f"현재 연료량 : {self.get_fuel():.2f}리터")
        print(f"현재 연료량으로 주행 가능 거리 : {self.get_range():.2f}km")
        print(f"최근 100km 주행 간 연비 : {self.get_fe_100():.2f}km/l")
        print(f"적재무게 : {self.get_cap()}kg")
        print()
        
    def show_state(self):
        if self.used == True:
            used_state = "중고"
        else:
            used_state = "신차"
        print(f"id: {self.car_id}, 차종: {self.brand}, 최대 연료량: {self.max_fuel}리터, 연비: {self.fe_org}km/l, 최대 적재무게: {self.max_cap}kg, 렌탈여부: {self.rented}, 마일리지: {self.mlg}km, 상태: {used_state}")
        
class Tesla_S(Car):
    def __init__(self, car_id, brand = "Tesla_S", max_fuel = 450, fe_org = 1, max_cap = 5, fuel = 0, fe_100 = 0, cap = 0, mlg = 0, used = False, rented = False):
        super().__init__(car_id, brand, max_fuel, fe_org, max_cap, fuel, fe_100, cap, mlg, used, rented)

    def show_dash(self):
        print(f"{self.car_id}의 대시보드")
        print(f"총 운행거리 : {self.get_mlg():.2f}km")
        print(f"현재 배터리 충전량 : {self.get_fuel():.2f}kwh")
        print(f"현재 배터리 량으로 주행 가능 거리 : {self.get_range():.2f}km")
        print(f"최근 100km 주행 간 연비 : {self.get_fe_100():.2f}km/kwh")
        print(f"탑승인원 : {self.get_cap()}명")
        print()
        
    def show_state(self):
        if self.used == True:
            used_state = "중고"
        else:
            used_state = "신차"
        print(f"id: {self.car_id}, 차종: {self.brand}, 최대 배터리량: {self.max_fuel}kwh, 연비: {self.fe_org}km/kwh, 최대 탑승인웡: {self.max_cap}명, 렌탈여부: {self.rented}, 마일리지: {self.mlg}km, 상태: {used_state}")