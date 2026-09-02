"""
Cron Schedule Builder - A simple DSL for creating readable cron expressions.

This module provides a fluent interface for building cron schedule strings
without requiring third-party libraries. It uses only Python's standard library.

Example usage:
    from fluentcron import CronSchedule

    # Daily at 5:00 AM
    schedule = CronSchedule().daily().at(5, 0)

    # Weekly on Monday at 5:00 AM
    schedule = CronSchedule().weekly().on_monday().at(5, 0)

    # Every 30 minutes
    schedule = CronSchedule().every_n_minutes(30)

    # Monthly on the 1st at 5:00 AM
    schedule = CronSchedule().monthly().on_day(1).at(5, 0)
"""

from .schedule import CronSchedule
from .shortcuts import (
    CommonSchedules,
    daily_at,
    every_n_hours,
    every_n_minutes,
    monthly_on_day,
    weekly_on,
)
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

__all__ = [
    "CronSchedule",
    "HourInterval",
    "MinuteInterval",
    "Hour",
    "Minute",
    "DayOfMonth",
    "WeekdayInt",
    "WeekdayStr",
    "Weekday",
    "daily_at",
    "weekly_on",
    "monthly_on_day",
    "every_n_minutes",
    "every_n_hours",
    "CommonSchedules",
]
