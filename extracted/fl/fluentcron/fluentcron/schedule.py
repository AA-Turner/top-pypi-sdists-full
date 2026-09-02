"""
Core cron schedule DSL functionality
"""

from __future__ import annotations

from typing import NamedTuple
import hashlib

from .types import (
    DayOfMonth,
    Hour,
    HourInterval,
    Minute,
    MinuteInterval,
    Weekday,
    WeekdayInt,
    WeekdayStr,
)

WEEKDAY_MAPPING: dict[WeekdayStr, WeekdayInt] = {
    # Long names
    "sunday": 0,
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
    # Short names
    "sun": 0,
    "mon": 1,
    "tue": 2,
    "wed": 3,
    "thu": 4,
    "fri": 5,
    "sat": 6,
    # uppercase long names
    "SUNDAY": 0,
    "MONDAY": 1,
    "TUESDAY": 2,
    "WEDNESDAY": 3,
    "THURSDAY": 4,
    "FRIDAY": 5,
    "SATURDAY": 6,
    # uppercase short names
    "SUN": 0,
    "MON": 1,
    "TUE": 2,
    "WED": 3,
    "THU": 4,
    "FRI": 5,
    "SAT": 6,
}


def _jitter_offset(jitter: str, modulus: int) -> int:
    h = hashlib.sha256(jitter.encode("utf-8")).hexdigest()
    return int(h, 16) % modulus


def _normalize_weekday(weekday: Weekday) -> WeekdayInt:
    # Already an int?
    if isinstance(weekday, int):
        if not (0 <= weekday <= 6):
            raise ValueError("Weekday must be between 0 (Sunday) and 6 (Saturday)")
        return weekday
    # Convert str -> int
    weekday_int = WEEKDAY_MAPPING.get(weekday)
    if weekday_int is None:
        raise ValueError("Invalid weekday name")
    return weekday_int


class CronSchedule(NamedTuple):
    """
    A fluent-interface builder for creating cron schedule expressions.
    """

    minute: str = "*"
    hour: str = "*"
    day: str = "*"
    month: str = "*"
    weekday: str = "*"

    def __str__(self) -> str:
        """Return the cron expression string."""
        return f"{self.minute} {self.hour} {self.day} {self.month} {self.weekday}"

    def to_str(self) -> str:
        """Finalize the expression by casting it to a string"""
        return str(self)

    def at(
        self, hour: Hour, minute: Minute | None = None, *, jitter: str | None = None
    ) -> CronSchedule:
        """Set the time (hour and minute)."""
        if minute is not None and jitter is not None:
            raise ValueError("Cannot specify both minute and jitter")
        if not (0 <= hour <= 23):
            raise ValueError("Hour must be between 0 and 23")
        if jitter is not None:
            resolved_minute = _jitter_offset(jitter, 60)
        elif minute is not None:
            resolved_minute = minute
        else:
            resolved_minute = 0
        if not (0 <= resolved_minute <= 59):
            raise ValueError("Minute must be between 0 and 59")

        return self._replace(hour=str(hour), minute=str(resolved_minute))

    def every_n_minutes(
        self, n: MinuteInterval, *, jitter: str | None = None
    ) -> CronSchedule:
        """Run every N minutes."""
        if not (1 <= n <= 59):
            raise ValueError("Minutes must be between 1 and 59")
        if n == 1 or jitter is None:
            minute = f"*/{n}" if n > 1 else "*"
        else:
            offset = _jitter_offset(jitter, n)
            minute = f"{offset}/{n}"
        return self._replace(minute=minute)

    def every_n_hours(
        self, n: HourInterval, *, jitter: str | None = None
    ) -> CronSchedule:
        """Run every N hours."""
        if not (1 <= n <= 23):
            raise ValueError("Hours must be between 1 and 23")
        hour = f"*/{n}" if n > 1 else "*"
        if jitter is not None:
            return self._replace(hour=hour, minute=str(_jitter_offset(jitter, 60)))
        return self._replace(hour=hour)

    def daily(self) -> CronSchedule:
        """Run daily (every day)."""
        return self._replace(day="*", weekday="*")

    def weekly(self) -> CronSchedule:
        """Run weekly. Use with on_monday(), on_tuesday(), etc."""
        return self._replace(day="*")

    def monthly(self) -> CronSchedule:
        """Run monthly. Use with on_day() to specify the day."""
        return self._replace(weekday="*")

    def on_day(self, day: DayOfMonth) -> CronSchedule:
        """Set the day of the month (1-31)."""
        if not (1 <= day <= 31):
            raise ValueError("Day must be between 1 and 31")

        return self._replace(day=str(day))

    def on_monday(self) -> CronSchedule:
        """Run on Monday."""
        return self._replace(weekday="1")

    def on_tuesday(self) -> CronSchedule:
        """Run on Tuesday."""
        return self._replace(weekday="2")

    def on_wednesday(self) -> CronSchedule:
        """Run on Wednesday."""
        return self._replace(weekday="3")

    def on_thursday(self) -> CronSchedule:
        """Run on Thursday."""
        return self._replace(weekday="4")

    def on_friday(self) -> CronSchedule:
        """Run on Friday."""
        return self._replace(weekday="5")

    def on_saturday(self) -> CronSchedule:
        """Run on Saturday."""
        return self._replace(weekday="6")

    def on_sunday(self) -> CronSchedule:
        """Run on Sunday."""
        return self._replace(weekday="0")

    def on_weekday(self, weekday: Weekday) -> CronSchedule:
        """Set the weekday (0=Sunday, 1=Monday, ..., 6=Saturday)."""
        return self._replace(weekday=str(_normalize_weekday(weekday)))
