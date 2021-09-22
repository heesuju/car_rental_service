class Event:
    def __init__(self, date, car_id, event_type):
        self.date = date
        self.car_id = car_id
        self.event_type = event_type    

    def get_date(self):
        return self.date

    def get_car_id(self):
        return self.car_id
        
    def get_event_type(self):
        return self.event_type

class Fuel_Event(Event):
    def __init__(self, date, car_id, event_type, amount, rented):
        super().__init__(date, car_id, event_type)
        self.amount = amount
        self.rented = rented
        
class Move_Event(Event):
    def __init__(self, date, car_id, event_type, distance, fe, rented):
        super().__init__(date, car_id, event_type)
        self.distance = distance
        self.fe = fe
        self.rented = rented
        
class Rental_Event(Event):
    def __init__(self, date, car_id, event_type, user):
        super().__init__(date, car_id, event_type)
        self.user = user
        
    def get_user(self):
        return self.user
        
class Return_Event(Event):
    def __init__(self, date, car_id, event_type, user):
        super().__init__(date, car_id, event_type)
        self.user = user
        
    def get_user(self):
        return self.user
        
class Add_Event(Event):
    pass
        
class Delete_Event(Event):
    pass