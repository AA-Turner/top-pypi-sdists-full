"""
time_utils.py

This module provides utility functions for working with timestamps and time-related operations.

Usage:
    import abstract_utilities.time_utils as time_utils

Functions:
- get_sleep(sleep_timer): Pause the execution of the program for a specified duration.
- get_time_stamp() -> float: Returns the current timestamp in seconds.
- get_milisecond_time_stamp() -> float: Returns the current timestamp in milliseconds.
- get_day(now=get_time_stamp()) -> str: Returns the current day of the week.
- get_time(now=get_time_stamp()) -> str: Returns the current time.
- get_date(now=get_time_stamp()) -> str: Returns the current date.
- save_last_time(now=get_time_stamp()) -> str: Saves the last timestamp to a file.
- get_day_seconds() -> float: Returns the number of seconds in a day.
- get_week_seconds() -> float: Returns the number of seconds in a week.
- get_hour_seconds() -> float: Returns the number of seconds in an hour.
- get_minute_seconds() -> float: Returns the number of seconds in a minute.
- get_second() -> float: Returns the value of one second.
- get_24_hr_start(now=get_time_stamp()) -> int: Returns the timestamp for the start of the current day.

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""

from .imports import *
def sleep_count_down(sleep_time):
    while sleep_time>float(0):
        sleep_time -= float(1)
        print(f"{max(sleep_time,0)} seconds till start")
        get_sleep(1)
def sleep_timer(last_time: Union[str, float], wait_limit: Union[float, int] = 0) -> None:
    """
    Pause execution for a specified amount of time, calculated based on time differences.

    Parameters:
    last_time (str or float): The reference time or timestamp.
    wait_limit (float or int, optional): The maximum wait time in seconds. Defaults to 0.

    Returns:
    None
    """
    curr_time = get_time_stamp()
    time_difference = curr_time - float(last_time)
    if time_difference < wait_limit:
        sleep_length = float(wait_limit - time_difference)
        get_sleep(sleep_timer=sleep_length)
def get_sleep(sleep_timer: Union[int, float] = 0):
    """
    Pause the execution of the program for a specified duration.

    This function pauses the program's execution for the given amount of time
    before continuing. The sleep duration can be specified in seconds as an integer
    or a floating-point number.

    Args:
        sleep_timer (int or float, optional): The duration in seconds to pause the execution.
            If not provided or set to 0, the function does nothing.

    Example:
        get_sleep(2)  # Pause the program for 2 seconds.
    """
    if isinstance(sleep_timer,int):
        sleep_timer=float(sleep_timer)
    if isinstance(sleep_timer,float):
        time.sleep(sleep_timer)
def get_time_stamp() -> float:
    """
    Returns the current timestamp in seconds.

    Returns:
        float: The current timestamp.
    """
    return datetime.now().timestamp()
def get_date_time_str(date_str,military_time_str):
    return f"{date_str} {military_time_str}"
def get_time_obj(date_time_str):
    return datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
def get_current_year() -> int:
    """
    Get the current year.

    Returns:
        int: The current year as an integer.
    """
    now = datetime.now()
    current_year = now.year
    return current_year

def get_24_hr_start(now=get_time_stamp()) -> int:
    """
    Returns the timestamp for the start of the current day.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        int: The timestamp for the start of the current day.
    """
    return int(now) - int(get_day_seconds())

def create_timestamp(date_str, military_time_str):
    """
    Converts a date string and military time string to a timestamp.

    Args:
        date_str (str): The date string in the format 'YYYY-MM-DD'.
        military_time_str (str): The military time string in the format 'HH:MM'.

    Returns:
        int: The timestamp corresponding to the date and time.
    """
    date_time_str = get_date_time_str(date_str,military_time_str)
    return int(get_time_obj(date_time_str).timestamp())

def get_milisecond_time_stamp():
    """
    Returns the current timestamp in milliseconds.

    Returns:
        float: The current timestamp in milliseconds.
    """
    return datetime.now().timestamp() * 1000

def get_day(now=get_time_stamp()):
    """
    Returns the current day of the week.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        str: The current day of the week.
    """
    return datetime.fromtimestamp(now).strftime("%A")

def get_time(now=get_time_stamp()):
    """
    Returns the current time.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        str: The current time.
    """
    return str(datetime.fromtimestamp(now))[10:]

def get_date(now=get_time_stamp()):
    """
    Returns the current date.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        str: The current date.
    """
    return str(datetime.fromtimestamp(now))[:10]

def save_last_time(now=get_time_stamp()):
    """
    Saves the last timestamp to a file.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        str: The filename where the timestamp is saved.
    """
    return pen(str(now), 'last.txt')

def get_day_seconds():
    """
    Returns the number of seconds in a day.

    Returns:
        float: The number of seconds in a day.
    """
    return float(24 * 60 * 60)

def get_week_seconds():
    """
    Returns the number of seconds in a week.

    Returns:
        float: The number of seconds in a week.
    """
    return float(7 * 24 * 60 * 60)

def get_hour_seconds():
    """
    Returns the number of seconds in an hour.

    Returns:
        float: The number of seconds in an hour.
    """
    return float(60 * 60)

def get_minute_seconds():
    """
    Returns the number of seconds in a minute.

    Returns:
        float: The number of seconds in a minute.
    """
    return float(60)

def get_second():
    """
    Returns the value of one second.

    Returns:
        float: The value of one second.
    """
    return float(1)

def all_combinations_of_strings(strings):
    """
    Generate all possible combinations of the input strings.
    Each combination is a concatenation of the input strings in different orders.

    :param strings: A list of strings for which we want to generate all combinations.
    :return: A list of strings representing all possible combinations.
    """
    from itertools import permutations

    # Generate all permutations of the input list
    all_perms = permutations(strings)

    # Concatenate strings in each permutation to form the combinations
    combinations = [''.join(perm) for perm in all_perms]

    return combinations
def all_date_formats():
    date_formats=[]
    for part in all_combinations_of_strings(list("Ymd")):
        for seperator in ['/','-','_']:
            date_range='%'
            for piece in list(str(part)):
                date_range+=f"{piece}{seperator}%"
            for times in ["%H:%M:%S.%f","%H:%M:%S"]:
                date_format = f"{date_range[:-2]} {times}"
                if date_format not in date_formats:
                    date_formats.append(date_format)
    return date_formats

def get_time_string(data):
    strin = 0
    for string in ["Timestamp","Data_Time_Stamp"]:
        strings = data.get(string)
        if strin:
            pass
    return strings
def convert_date_to_timestamp(date_string,date_format=[]):
    date_formats = all_date_formats()
    date_string = str(date_string)
    date_formats = make_list(date_format)+date_formats
    for date_format in date_formats:
        try:
            date_object = datetime.strptime(date_string, date_format)
            return date_object.timestamp()
        except ValueError:
            continue
    print(f"Date format not recognized: {date_string}")
    return None
def get_rounded_hour_datetime(timeStamp=None,hours=0):
    """
    Returns the current datetime rounded down to the nearest hour,
    with an optional adjustment by a specified number of hours.
    
    :param hours: Number of hours to adjust the rounded datetime by.
                  Defaults to 0 (no adjustment).
    :return: A datetime object for the adjusted, rounded-down hour.
    """
    now = get_convert_timestamp_to_datetime(timeStamp or datetime.now())
    # Round down to the nearest hour
    rounded_hour = now.replace(minute=0, second=0, microsecond=0)
    # Adjust by the specified number of hours
    adjusted_datetime = rounded_hour + timedelta(hours=hours)
    return adjusted_datetime

def get_current_time_with_delta(days=0, hours=0, minutes=0, seconds=0,milliseconds=0):
    # Get the current datetime
    current_time = get_time_stamp()

    # Create a timedelta with the specified duration
    delta = timedelta(days=days, hours=hours, minutes=minutes,seconds=seconds, milliseconds=milliseconds)
    
    # Add the delta to the current time
    new_time = current_time + delta
    
    return new_time
def get_time_stamp_date():
    return datetime.now()

def get_time_stamp_now():
    return datetime.datetime.now()
    
def get_timestamp():
    return time.time()

def get_hours_ago_datetime(hours=1):
    return get_time_stamp() - get_time_delta_hour(hours=hours)

def get_hours_ago(hours=1):
    hours_ago = get_hours_ago_datetime(hours=1)
    return hours_ago.timestamp()

def get_daily_output(timeStamp=None):
    timeStamp = get_convert_timestamp_to_datetime(convert_date_to_timestamp(timeStamp or get_time_stamp()))
    return timeStamp.strftime('%m-%d-%Y')

def get_hourly_output(timeStamp=None):
    timeStamp = get_convert_timestamp_to_datetime(convert_date_to_timestamp(timeStamp or get_time_stamp()))
    return timeStamp.strftime('%H') + '00'

def get_hour_time_stamp(hours=0):
    return convert_date_to_timestamp(f"{get_rounded_hour_datetime(hours=hours)}")

def get_variable_time_stamp(days=0,hours=0,minutes=0,seconds=0):
    return convert_date_to_timestamp(f"{get_daily_output()} 0:0:00")+(days*(60*60*24))+(hours*(60*60))+(minutes*60)+seconds

def get_variable_datetime(days=0,hours=0,minutes=0,seconds=0):
    timeStamp = get_variable_time_stamp(days=0,hours=0,minutes=0,seconds=0)
    return get_convert_timestamp_to_datetime(timeStamp)
def get_convert_datetime_to_timeStamp(timeStamp):
    timeStamp = timeStamp or get_timestamp()
    if not is_number(timeStamp):
        timeStamp = convert_date_to_timestamp(timeStamp)
    return timeStamp
def get_convert_timestamp_to_datetime(timeStamp=None):
    timeStamp = timeStamp or get_time_stamp()
    if is_number(timeStamp):
        timeStamp = datetime.fromtimestamp(timeStamp)
    return timeStamp
def is_within_day(timeStamp):
    return is_between_range(get_convert_timestamp(timeStamp),get_day_time_stamp(),get_day_time_stamp(days=1))
def is_within_hour(timeStamp):
    return is_between_range(get_convert_timestamp(timeStamp),get_hour_time_stamp(),get_hour_time_stamp(hours=1))

def is_between_range(target,start,end):
    if target >= start and target <=end:
        return True
    return False
def get_creation_time_of_file(file_path):
    if os.path.isfile(file_path):
        creation_time = os.path.getctime(file_path)
        return datetime.datetime.fromtimestamp(creation_time)

def timestamp_to_milliseconds(timestamp):
    try:
        t = datetime.strptime(timestamp, "%H:%M:%S.%f")
        return (t.hour * 3600 + t.minute * 60 + t.second) * 1000 + int(t.microsecond / 1000)
    except ValueError:
        raise ValueError(f"Invalid timestamp format: {timestamp}")

def parse_timestamp(ts_str):
    parts = ts_str.split(":")
    return (int(parts[0]) * 60 + int(parts[1])) * 1000 if len(parts) == 2 else int(parts[0]) * 1000
def format_timestamp(ms):
    """Convert milliseconds to a formatted timestamp (HH:MM:SS.mmm)."""
    td = timedelta(milliseconds=ms)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def get_time_now_iso():
    return datetime.now().isoformat()
def is_valid_time(comp_timestamp, timestamp=None, before=True):
    if timestamp is None:
        return True
    return (timestamp >= comp_timestamp) if before else (timestamp <= comp_timestamp)

# Function: get_time_stamp
# Function: get_milisecond_time_stamp
# Function: get_day
# Function: get_time
# Function: get_date
# Function: save_last_time
# Function: get_day_seconds
# Function: get_week_seconds
# Function: get_hour_seconds
# Function: get_minute_seconds
# Function: get_second
# Function: get_24_hr_start
