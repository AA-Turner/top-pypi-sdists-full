from time import sleep
from random import random, uniform, randrange
from datetime import datetime, timedelta, time
from dateutil.parser import parse
from printr import print

class SleepTimer:
    '''Sleep outside of set active hours'''
    def __init__(self, hour_to_start_at=True, hour_to_stop_at=None, sleeping_message='Sleeping'):
        if not hour_to_start_at:
            hour_to_start_at = True
            hour_to_stop_at = None
        if type(hour_to_start_at) != str:
            self.hour_to_start_at = hour_to_start_at
            self.hour_to_stop_at = hour_to_stop_at
        else:
            self.hour_to_start_at = parse(hour_to_start_at).hour
            self.hour_to_stop_at = parse(hour_to_stop_at).hour

        self.sleeping_message = sleeping_message
        self.printed_sleeping_message = False

        self.random_minute_to_start_at = randrange(0, 59)
        self.random_minute_to_end_at = randrange(0, 59) # If started after start_hour generate a random minute to end at

        self.is_active = False
    
    def current_hour_within_active_hours(self, current_hour):
        # Check within active hours
        if self.hour_to_start_at < current_hour < self.hour_to_stop_at:
            return True
        elif self.hour_to_stop_at < self.hour_to_start_at:
            if current_hour > self.hour_to_start_at:
                return True
            elif current_hour < self.hour_to_stop_at:
                return True
        return False
    
    def during_active_time(self):
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        if self.hour_to_start_at == True: # Permanently active
            return True
        elif self.hour_to_start_at == False: # Permanently inactive
            return False
        elif self.current_hour_within_active_hours(current_hour):
            self.is_active = True
            if self.random_minute_to_start_at != 0:
                self.random_minute_to_start_at = 0

            # Check after start time with randomised minute to start at
        elif current_hour == self.hour_to_start_at and current_minute >= self.random_minute_to_start_at:
            self.is_active = True

        # Check before end time including randomised minute to end at
        elif current_hour == self.hour_to_stop_at and current_minute >= self.random_minute_to_end_at:
            self.is_active = False

            if self.random_minute_to_start_at == 0:
                self.random_minute_to_start_at = randrange(0, 59)
                self.random_minute_to_end_at = randrange(0, 59)
            
            if not self.printed_sleeping_message:
                self.print_sleeping_message()
        
        if not self.is_active and not self.printed_sleeping_message:
            self.print_sleeping_message()

        return self.is_active
    
    def print_sleeping_message(self):
        current_hour = datetime.now().hour # 11:13pm would have an hour of 23
        current_minute = datetime.now().minute # 11:13pm would have a minute of 13

        number_of_hours_til_start = self.hour_to_start_at - current_hour # 8 - 23 = -15
        if self.hour_to_start_at < current_hour: # If hour to start at is tomorrow
            number_of_hours_til_start += 24 # -15 + 24 = 9
        
        # If we end at 11:13pm and start at 8:49am the difference between the minutes is more than 30 so add an exta hour
        if self.random_minute_to_start_at - current_minute > 30:
            number_of_hours_til_start += 1

        formatted_time_to_start_at = f'{self.hour_to_start_at}:{self.random_minute_to_start_at:02d}' # 8:22, must use fstring due to integers
        
        if number_of_hours_til_start == 1:
            print(self.sleeping_message, '1 hour until', formatted_time_to_start_at)
        else:
            print(self.sleeping_message, number_of_hours_til_start, 'hours until', formatted_time_to_start_at)

        self.printed_sleeping_message = True


sleep_timer = SleepTimer

class random_timeout:
    '''Random timeout between from and to values'''
    def __init__(self, from_seconds=None, to_seconds=None, from_minutes=None, to_minutes=None, from_hours=None, to_hours=None, from_days=None, to_days=None, silent=False):
        if from_seconds is not None:
            if from_seconds == 0:
                minimum = random()
            elif from_seconds > 1:
                minimum = from_seconds - random() # Random float between 0 and 1
            else:
                minimum = from_seconds
            if to_seconds:
                maximum = to_seconds
                if to_seconds > 1:
                    maximum += random()
            else:
                maximum = from_seconds
        elif from_minutes is not None:
            if from_minutes == 0:
                minimum = random()
            else:
                minimum = (from_minutes - random()) * 60 # Random float between 0 and 1
            if to_minutes:
                maximum = (to_minutes + random()) * 60
            else:
                maximum = from_minutes + random()
        elif from_hours is not None:
            if from_hours == 0:
                minimum = random()
            else:
                minimum = (from_hours - random()) * 3600 # Random float between 0 and 1
            if to_hours:
                maximum = (to_hours + random()) * 3600
            else:
                maximum = from_hours + random()
        elif from_days is not None:
            if from_days == 0:
                minimum = random()
            else:
                minimum = (from_days - random()) * 86400 # Random float between 0 and 1
            if to_days:
                maximum = (to_days + random()) * 86400
            else:
                maximum = from_days + random()
                
        timeout_in_seconds = uniform(minimum, maximum) # Random float between minimum and maximum
        if not silent:
            if timeout_in_seconds < 60:
                print('Sleeping', timeout_in_seconds, 'seconds', level='debug')
            elif timeout_in_seconds > 86400:
                timeout_in_days = round(timeout_in_seconds / 86400) # Convert sleep time in seconds to days
                til = datetime.now() + timedelta(seconds=timeout_in_seconds)
                til = til.strftime('%A, %B %e')
                if timeout_in_days == 1:
                    print('Sleeping 1 day until', til)
                else:
                    print('Sleeping', timeout_in_days, 'days until', til)
            elif timeout_in_seconds > 3600:
                timeout_in_hours = round(timeout_in_seconds / 3600) # Convert sleep time in seconds to hours
                til = datetime.now() + timedelta(seconds=timeout_in_seconds)
                til = til.strftime('%H:%M')
                if timeout_in_hours == 1:
                    print('Sleeping 1 hour until', til)
                else:
                    print('Sleeping', timeout_in_hours, 'hours until', til)
            elif timeout_in_seconds >= 60:
                timeout_in_minutes = round(timeout_in_seconds / 60) # Convert sleep time in seconds to minutes
                til = datetime.now() + timedelta(seconds=timeout_in_seconds)
                til = til.strftime('%H:%M')
                if timeout_in_minutes == 1:
                    print('Sleeping 1 minute until', til)
                else:
                    print('Sleeping', timeout_in_minutes, 'minutes until', til)

        wait(timeout_in_seconds)

wait = sleep
class sleep:
    '''Sleep amount of time in minutes, hours or days and prints when it will continue'''
    def __init__(self, seconds=None, minutes=None, hours=None, days=None, silent=False):
        if seconds:
            timeout_in_seconds = seconds
        if minutes:
            timeout_in_seconds = minutes * 60
        elif hours:
            timeout_in_seconds = hours * 3600
        elif days:
            timeout_in_seconds = days * 86400

        if not silent:
            if timeout_in_seconds < 60:
                print('Sleeping', timeout_in_seconds, 'seconds', level='debug')
            elif timeout_in_seconds > 86400:
                timeout_in_days = round(timeout_in_seconds / 86400) # Convert sleep time in seconds to days
                til = datetime.now() + timedelta(seconds=timeout_in_seconds)
                til = til.strftime('%A, %B %e')
                if timeout_in_days == 1:
                    print('Sleeping 1 day until', til)
                else:
                    print('Sleeping', timeout_in_days, 'days until', til)
            elif timeout_in_seconds > 3600:
                timeout_in_hours = round(timeout_in_seconds / 3600) # Convert sleep time in seconds to hours
                til = datetime.now() + timedelta(seconds=timeout_in_seconds)
                til = til.strftime('%H:%M')
                if timeout_in_hours == 1:
                    print('Sleeping 1 hour until', til)
                else:
                    print('Sleeping', timeout_in_hours, 'hours until', til)
            elif timeout_in_seconds >= 60:
                timeout_in_minutes = round(timeout_in_seconds / 60) # Convert sleep time in seconds to minutes
                til = datetime.now() + timedelta(seconds=timeout_in_seconds)
                til = til.strftime('%H:%M')
                if timeout_in_minutes == 1:
                    print('Sleeping 1 minute until', til)
                else:
                    print('Sleeping', timeout_in_minutes, 'minutes until', til)

        wait(timeout_in_seconds)

class sleep_for:
    '''Sleep amount of time in minutes, hours or days and prints when it will continue'''
    def __init__(self, seconds=None, minutes=None, hours=None, days=None, silent=False):
        sleep(seconds, minutes, hours, days, silent)