import datetime


class DateTimeFormatter:

    @staticmethod
    def format_datetime(date_time):
        if date_time is None:
            return None
        if isinstance(date_time, datetime.datetime):
            return date_time.isoformat()
        else:
            raise ValueError("Input is not a valid datetime object")
