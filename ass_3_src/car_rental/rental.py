import car_rental.cars.fleet as flt
import car_rental.users.customer as clientbase
import car_rental.monitor.monitor as monitor
import car_rental.monitor.logger as log

class Rental:
    def __init__(self):
        self.fleet = flt.Fleet()
        self.clients = clientbase.Customers(self)
        self.monitor = monitor.Monitor(self)
        log.Event_List.load_events()
        
    def save(self):
        self.fleet.save_fleet()
        self.clients.save_clients()
        log.Event_List.save_events()
