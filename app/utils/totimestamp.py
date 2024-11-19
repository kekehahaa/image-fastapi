from datetime import datetime

def time_str_to_seconds(time_str: str):
    if time_str.count(":") == 1: 
        time_obj = datetime.strptime(time_str, "%M:%S")
        seconds = time_obj.minute * 60 + time_obj.second
    elif time_str.count(":") == 2:  
        time_obj = datetime.strptime(time_str, "%H:%M:%S")
        seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    else:
        raise ValueError("Неверный формат строки времени")
    return seconds
