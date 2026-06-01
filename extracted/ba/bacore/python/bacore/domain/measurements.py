"""Measurements module."""

from datetime import date, datetime, timedelta
from dataclasses import dataclass


@dataclass(frozen=True)
class Time:
    """Class for time related settings.

    Attributes:
        now: Current date and time.
        today: Current date.
        yesterday: Yesterday's date.
        now_s: Current date and time as string.
        today_s: Current date as string.
        yesterday_s: Yesterday's date as string.
        ty: Current year as string.
        tm: Current month as string.
        td: Current day as string.
        yy: Yesterday's year as string.
        ym: Yesterday's month as string.
        yd: Yesterday's day as string.

    Methods:
        due(year: int, month: int, day: int) -> bool: Return True if due date is reached.

    Examples:
        >>> Time().due(2024, 1, 1)
        True
    """

    now = datetime.now()
    now_s = now.strftime("%Y-%m-%d %H:%M:%S")
    today = date.today()
    today_s = today.strftime("%Y-%m-%d")
    yesterday = today - timedelta(days=1)
    yesterday_s = yesterday.strftime("%Y-%m-%d")
    ty = today.strftime("%Y")
    tm = today.strftime("%m")
    td = today.strftime("%d")
    yy = yesterday.strftime("%Y")
    ym = yesterday.strftime("%m")
    yd = yesterday.strftime("%d")

    def due(self, year: int, month: int, day: int):
        """Return True if due date is reached."""
        return self.now > datetime(year, month, day)