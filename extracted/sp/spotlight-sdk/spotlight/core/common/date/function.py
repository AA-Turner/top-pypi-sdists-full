"""
Date and time functions.
"""

import calendar
from datetime import date, datetime, time

import pytz

from spotlight.core.common.type import Datetime


def current_timestamp() -> int:
    """ """
    now = datetime.now()
    return datetime_to_timestamp(now)


def date_to_timestamp(as_of_date: date) -> int:
    """
    Convert date to epoch timestamp in milliseconds.

    Args:
        as_of_date (date): Python date

    Returns:
        int: Epoch timestamp in milliseconds
    """
    return calendar.timegm(as_of_date.timetuple()) * 1000


def datetime_to_timestamp(dt: datetime) -> int:
    """
    Convert datetime to epoch timestamp in milliseconds.

    Args:
        dt (datetime): Python datetime

    Returns:
        int: Epoch timestamp in milliseconds
    """
    return calendar.timegm(dt.utctimetuple()) * 1000


def datetime_to_utc(dt: datetime) -> datetime:
    """
    Standardize datetime to UTC. Assume that datetime where `tzinfo=None` is already in UTC.

    Args:
        dt (datetime): Python datetime

    Returns:
        datetime: Python datetime with standardized UTC timezone (`tzinfo=None`)
    """
    # assume that datetime without timezone is already in UTC
    if dt.tzinfo is None:
        return dt
    return dt.astimezone(pytz.utc).replace(tzinfo=None)


def date_to_datetime(
    as_of_date: date, as_of_time: time = datetime.min.time()
) -> datetime:
    """
    Convert date and optional time to datetime. NOTE: time should not contain a timezone or else offset may not be
    correct.

    Args:
        as_of_date (date): Python date
        as_of_time (time): Python time

    Returns:
        datetime: Python datetime
    """
    return datetime.combine(as_of_date, as_of_time)


def standardize_date_or_datetime(as_of_date: Datetime) -> datetime:
    """
    Convert Datetime (Union[date, datetime]) to standardized UTC datetime.

    Args:
        as_of_date (date): Datetime

    Returns:
        datetime: Python UTC datetime
    """
    if isinstance(as_of_date, datetime):
        return datetime_to_utc(as_of_date)

    return date_to_datetime(as_of_date)


def timestamp_to_datetime(timestamp: int) -> datetime:
    """
    Transform epoch timestamp in milliseconds to datetime.

    Args:
        timestamp (int): Epoch timestamp in milliseconds

    Returns:
        datetime: Python datetime
    """
    return datetime.fromtimestamp(timestamp / 1000)
