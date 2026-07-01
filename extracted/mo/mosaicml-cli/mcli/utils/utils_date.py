"""This Module stores utils for pretty printing Datetime objects"""
import datetime
from enum import Enum
from typing import Optional


class TimestampPrecision(Enum):
    """Enum for timestamp precision"""
    DAY = 'day'
    MINUTE = 'minute'
    SECOND = 'second'


def format_timestamp(timestamp: Optional[datetime.datetime],
                     precision: TimestampPrecision = TimestampPrecision.MINUTE,
                     timezone: Optional[datetime.tzinfo] = None,
                     default='-') -> str:
    """Format UTC timestamps into a human-readable string in the local timezone.
    The precision can be controlled by the `precision` argument.

    Args:
        timestamp: The timestamp to format, assumed to be in UTC.
        precision: The precision to use when formatting the timestamp. Defaults to `TimestampPrecision.MINUTE`.
        timezone: The timezone to use when formatting the timestamp. Defaults to the local timezone.
        default: The value to return if the timestamp is None or invalid. Defaults to '-'.

    Returns:
        The formatted timestamp string.
    """
    if not timestamp:
        return default

    dt_format = '%Y-%m-%d %I:%M %p'  # Default MINUTE precision.
    if precision == TimestampPrecision.DAY:
        dt_format = '%Y-%m-%d'
    elif precision == TimestampPrecision.MINUTE:
        dt_format = '%Y-%m-%d %I:%M %p'
    elif precision == TimestampPrecision.SECOND:
        dt_format = '%Y-%m-%d %I:%M:%S %p'

    if not timezone:
        timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo  # Get the local timezone

    try:
        return timestamp.astimezone(timezone).strftime(dt_format)
    except (OverflowError, ValueError) as _:
        return default
