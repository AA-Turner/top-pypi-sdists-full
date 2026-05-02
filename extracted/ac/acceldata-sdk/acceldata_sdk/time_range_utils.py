from datetime import datetime, timedelta
from acceldata_sdk.models.ruleExecutionResult import ExecutionPeriod


class TimeRangeCalculator:

    def __init__(self):
        pass

    @staticmethod
    def check_int(input_str):
        try:
            int(input_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def calculate_minutes_before_time(minutes):
        """
        Calculate the time range starting before the given number of minutes from the current time.
        :param minutes: Number of minutes to subtract from the current time.
        :return: A tuple containing two datetime objects -
                 the starting time before the given minutes and
                 the ending time as the current datetime.
        """
        now = datetime.now()
        finished_before_time = now
        started_after_time = finished_before_time - timedelta(minutes=minutes)
        return started_after_time, finished_before_time

    @staticmethod
    def calculate_hours_before_time(hours):
        """
        Calculate the time range starting before the given number of hours from the current time.
        :param hours: Number of hours to subtract from the current time.
        :return: A tuple containing two datetime objects -
                 the starting time before the given hours and
                 the ending time as the current datetime.
        """
        finished_before_time = datetime.now()
        started_after_time = finished_before_time - timedelta(hours=hours)
        return started_after_time, finished_before_time

    @staticmethod
    def calculate_days_before_time(days):
        """
        Calculate the time range starting before the given number of days from today's midnight.
        :param days: Number of days to subtract from today's midnight.
        :return: A tuple containing two datetime objects -
                 the starting time before the given days from the beginning of the current day and
                 the ending time as the beginning of the current day.
        """
        now = datetime.now()
        min_time = datetime.min.time()
        started_after_time = datetime.combine((now - timedelta(days=days)).date(), min_time)
        finished_before_time = datetime.combine(now.date(), min_time)
        return started_after_time, finished_before_time

    @staticmethod
    def calculate_time_range(filter):
        if filter.period is not None:
            now = datetime.now()
            finished_before_time = now
            started_after_time = None  # Initialize to None
            if filter.period == ExecutionPeriod.Last15minutes:
                started_after_time, finished_before_time = filter.calculate_minutes_before_time(15)
            elif filter.period == ExecutionPeriod.Last30minutes:
                started_after_time, finished_before_time = filter.calculate_minutes_before_time(30)
            elif filter.period == ExecutionPeriod.Last1hour:
                started_after_time, finished_before_time = filter.calculate_hours_before_time(1)
            elif filter.period == ExecutionPeriod.Last3hours:
                started_after_time, finished_before_time = filter.calculate_hours_before_time(3)
            elif filter.period == ExecutionPeriod.Last6hours:
                started_after_time, finished_before_time = filter.calculate_hours_before_time(6)
            elif filter.period == ExecutionPeriod.Last12hours:
                started_after_time, finished_before_time = filter.calculate_hours_before_time(12)
            elif filter.period == ExecutionPeriod.Last24hours:
                started_after_time, finished_before_time = filter.calculate_hours_before_time(24)
            elif filter.period == ExecutionPeriod.Today:
                started_after_time = datetime.combine(datetime.now().date(), datetime.min.time())
            elif filter.period == ExecutionPeriod.Yesterday:
                started_after_time, finished_before_time = filter.calculate_days_before_time(1)
            elif filter.period == ExecutionPeriod.Last7days:
                started_after_time, finished_before_time = filter.calculate_days_before_time(7)
            elif filter.period == ExecutionPeriod.Thismonth:
                started_after_time = datetime(datetime.now().year, datetime.now().month, 1)
            elif filter.period == ExecutionPeriod.Last1month:
                started_after_time, finished_before_time = filter.calculate_months_before_time(1)
            elif filter.period == ExecutionPeriod.Last3month:
                started_after_time, finished_before_time = filter.calculate_months_before_time(3)
            return finished_before_time, started_after_time
