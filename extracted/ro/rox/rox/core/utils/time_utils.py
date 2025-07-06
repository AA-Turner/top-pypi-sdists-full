import time
from datetime import datetime

def now_in_unix_milliseconds():
    return int(time.time() * 1000)

def string_to_date(date_as_string):
    try:
        date_time = datetime.strptime(date_as_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        short_date_as_string = date_as_string[0:19] #%Y-%m-%dT%H:%M:%S should be 19 characters long
        date_time = datetime.strptime(short_date_as_string, "%Y-%m-%dT%H:%M:%S")
    return date_time
