import car_rental.monitor.logger as log

class Monitor:
    def __init__(self, parent):
        self.parent = parent
    
    def show_rented_event_count_week(self, event_type):
        total = 0
        event_arr = []
        event_arr = log.Event_List.get_events_week(event_type)
        if event_type == "fuel":
            for event in event_arr:
                if event.rented == True:
                    total = total + event.amount
            print(f"7일 동안 렌탈된 차량의 총 주유량은 {total:.2f}리터입니다.")
        else:
            for event in event_arr:
                if event.rented == True:
                    total = total + event.distance
            print(f"7일 동안 렌탈된 차량의 총 운행거리는 {total:.2f}km입니다.")
        
    def show_rented_event_count_all(self, event_type):
        total = 0
        event_arr = []
        event_arr = log.Event_List.get_events(event_type)
        if event_type == "fuel":
            for event in event_arr:
                if event.rented == True:
                    total = total + event.amount
            print(f"렌탈된 차량의 총 주유량은 {total:.2f}리터입니다.")
        elif event_type == "move":
            for event in event_arr:
                if event.rented == True:
                    total = total + event.distance
            print(f"렌탈된 차량의 총 운행거리는 {total:.2f}km입니다.")
        else:
            print("이벤트명이 존재하지 않습니다.")
        
    def show_rented_event_count_range(self, event_type, date_from, date_to):
        total = 0
        event_arr = []
        try:
            f_date_from = log.Event_List.convert_to_date(date_from)
            f_date_to = log.Event_List.convert_to_date(date_to)
            if f_date_from <= f_date_to:
                event_arr = log.Event_List.get_events_range(event_type, f_date_from, f_date_to)
                if event_type == "fuel":
                    for event in event_arr:
                        if event.rented == True:
                            total = total + event.amount
                    print(f"{date_from}부터 {date_to}까지 렌탈된 차량의 총 주유량은 {total:.2f}리터입니다.")
                elif event_type == "move":
                    for event in event_arr:
                        if event.rented == True:
                            total = total + event.distance
                    print(f"{date_from}부터 {date_to}까지 렌탈된 차량의 총 운행거리는 {total:.2f}km입니다.")
                else:
                    print("이벤트명이 존재하지 않습니다.")
            else:
                print("시작 날짜가 끝 날짜보다 미래로 입력되었습니다.")
        except:
            print(f"{log.Event_List.get_today()}와 같은 형식으로 입력해주세요.")
       
    def show_event_count_week(self, event_type):
        total = 0
        event_arr = log.Event_List.get_events_week(event_type)

        if event_type == "fuel":
            for item in event_arr:
                total = total + item.amount
            print(f"7일 동안 주유량은 {total}리터입니다.")
        elif event_type == "move":
            for item in event_arr:
                total = total + item.distance
            print(f"7일 동안 운행거리는 {total}km입니다.")
        elif event_type == "add":
            for item in event_arr:
                total = total + 1
            print(f"7일 동안 추가된 차량의 개수는 {total}대입니다.")
        elif event_type == "delete":
            for item in event_arr:
                total = total + 1
            print(f"7일 동안 폐차된 차량의 개수는 {total}대입니다.")
        elif event_type == "rental":
            for item in event_arr:
                total = total + 1
            print(f"7일 동안 렌탈 횟수는 {total}개입니다.")
        elif event_type == "return":
            for item in event_arr:
                total = total + 1
            print(f"7일 동안 반환 횟수는 {total}개입니다.")
        else:
            print("이벤트명이 존재하지 않습니다.")

    def show_event_count_all(self, event_type):
        total = 0
        event_arr = log.Event_List.get_events(event_type)

        if event_type == "fuel":
            for item in event_arr:
                total = total + item.amount
            print(f"총 주유량은 {total}리터입니다.")
        elif event_type == "move":
            for item in event_arr:
                total = total + item.distance
            print(f"총 운행거리는 {total}km입니다.")
        elif event_type == "add":
            for item in event_arr:
                total = total + 1
            print(f"추가된 차량의 총 개수는 {total}대입니다.")
        elif event_type == "delete":
            for item in event_arr:
                total = total + 1
            print(f"폐차된 차량의 총 개수는 {total}대입니다.")
        elif event_type == "rental":
            for item in event_arr:
                total = total + 1
            print(f"렌탈 총 횟수는 {total}개입니다.")
        elif event_type == "return":
            for item in event_arr:
                total = total + 1
            print(f"반환 총 횟수는 {total}개입니다.")
        else:
            print("이벤트명이 존재하지 않습니다.")

    def show_event_count_range(self, event_type, date_from, date_to):
        total = 0
        try:
            f_date_from = log.Event_List.convert_to_date(date_from)
            f_date_to = log.Event_List.convert_to_date(date_to)
            if f_date_from <= f_date_to:
                event_arr = log.Event_List.get_events_range(event_type, f_date_from, f_date_to)
                if event_type == "fuel":
                    for item in event_arr:
                        total = total + item.amount
                    print(f"{date_from}부터 {date_to}까지 총 주유량은 {total:.2f}리터입니다.")
                elif event_type == "move":
                    for item in event_arr:
                        total = total + item.distance
                    print(f"{date_from}부터 {date_to}까지 총 운행거리는 {total:.2f}km입니다.")
                elif event_type == "add":
                    for item in event_arr:
                        total = total + 1
                    print(f"{date_from}부터 {date_to}까지 추가된 차량의 총 개수는 {total}대입니다.")
                elif event_type == "delete":
                    for item in event_arr:
                        total = total + 1
                    print(f"{date_from}부터 {date_to}까지 폐차된 차량의 총 개수는 {total}대입니다.")
                elif event_type == "rental":
                    for item in event_arr:
                        total = total + 1
                    print(f"{date_from}부터 {date_to}까지 렌탈 횟수는 {total}개입니다.")
                elif event_type == "return":
                    for item in event_arr:
                        total = total + 1
                    print(f"{date_from}부터 {date_to}까지 반환 횟수는 {total}개입니다.")
                else:
                    print("이벤트명이 존재하지 않습니다.")
            else:
                print("시작 날짜가 끝 날짜보다 미래로 입력되었습니다.")
        except:
            print(f"{log.Event_List.get_today()}와 같은 형식으로 입력해주세요.")
            
    def show_event_car_week(self, event_type):
        event_arr = log.Event_List.get_events_week(event_type)
        event_set = set()
        count = 0
        label = ""
        if event_type == "fuel":
            label = "7일 내 주유한 차량: "
        elif event_type == "move":
            label = "7일 내 운행한 차량: "
        elif event_type == "rental":
            label = "7일 내 렌탈된 차량: "
        elif event_type == "return":
            label = "7일 내 반환된 차량: "
        elif event_type == "add":
            label = "7일 내 추가된 차량: "
        elif event_type == "delete":
            label = "7일 내 폐차된 차량: "
        if label != "":
            print(label, end = "")
            for item in event_arr:
                count = count + 1
                event_set.add(item.car_id)
            for i in event_set:
                print(i, end = " ")
            if count == 0:
                print("해당되는 차량이 없습니다.")
            else:
                print()
        else:
            print("이벤트명이 존재하지 않습니다.")
            
    def show_event_car_all(self, event_type):
        event_arr = log.Event_List.get_events(event_type)
        event_set = set()
        count = 0
        label = ""
        if event_type == "fuel":
            label = "현재까지 주유한 차량: "
        elif event_type == "move":
            label = "현재까지 운행한 차량: "
        elif event_type == "rental":
            label = "현재까지 렌탈된 차량: "
        elif event_type == "return":
            label = "현재까지 반환된 차량: "
        elif event_type == "add":
            label = "현재까지 추가된 차량: "
        elif event_type == "delete":
            label = "현재까지 폐차된 차량: "
        if label != "":
            print(label, end = "")
            for item in event_arr:
                count = count + 1
                event_set.add(item.car_id)
            for i in event_set:
                print(i, end = " ")
            if count == 0:
                print("해당되는 차량이 없습니다.")
            else:
                print()
        else:
            print("이벤트명이 존재하지 않습니다.")
            
    def show_event_car_range(self, event_type, date_from, date_to):
        event_arr = []
        event_set = set()
        count = 0
        label = ""
        try:
            f_date_from = log.Event_List.convert_to_date(date_from)
            f_date_to = log.Event_List.convert_to_date(date_to)
            if f_date_from <= f_date_to:
                event_arr = log.Event_List.get_events_range(event_type, f_date_from, f_date_to)
            else:
                print("시작 날짜가 끝 날짜보다 미래로 입력되었습니다.")
        except:
            print(f"{log.Event_List.get_today()}와 같은 형식으로 입력해주세요.")
        if event_type == "fuel":
            print(f"{date_from}부터 {date_to}까지 주유한 차량: ", end = "")
        elif event_type == "move":
            print(f"{date_from}부터 {date_to}까지 운행한 차량: ", end = "")
        elif event_type == "rental":
            print(f"{date_from}부터 {date_to}까지 렌탈된 차량: ", end = "")
        elif event_type == "return":
            print(f"{date_from}부터 {date_to}까지 반환된 차량: ", end = "")
        elif event_type == "add":
            print(f"{date_from}부터 {date_to}까지 추가된 차량: ", end = "")
        elif event_type == "delete":
            print(f"{date_from}부터 {date_to}까지 폐차된 차량: ", end = "")
        else:
            print("이벤트명이 존재하지 않습니다.")
        for item in event_arr:
            count = count + 1
            event_set.add(item.car_id)
        for i in event_set:
            print(i, end = " ")
        if count == 0:
            print("해당되는 차량이 없습니다.")
        else:
            print()