"""
Convenience functions for common schedules
"""

from .schedule import CronSchedule
from .types import (
    DayOfMonth,
    Hour,
    HourInterval,
    Minute,
    MinuteInterval,
    Weekday,
)


def daily_at(
    hour: Hour, minute: Minute | None = None, *, jitter: str | None = None
) -> str:
    """Create a daily schedule at the specified time."""
    return str(CronSchedule().daily().at(hour, minute, jitter=jitter))


def weekly_on(
    weekday: Weekday,
    hour: Hour,
    minute: Minute | None = None,
    *,
    jitter: str | None = None,
) -> str:
    """Create a weekly schedule on the specified weekday and time."""
    return str(
        CronSchedule().weekly().on_weekday(weekday).at(hour, minute, jitter=jitter)
    )


def monthly_on_day(
    day: DayOfMonth,
    hour: Hour,
    minute: Minute | None = None,
    *,
    jitter: str | None = None,
) -> str:
    """Create a monthly schedule on the specified day and time."""
    return str(CronSchedule().monthly().on_day(day).at(hour, minute, jitter=jitter))


def every_n_minutes(n: MinuteInterval, *, jitter: str | None = None) -> str:
    """Create a schedule that runs every N minutes."""
    return str(CronSchedule().every_n_minutes(n, jitter=jitter))


def every_n_hours(n: HourInterval, *, jitter: str | None = None) -> str:
    """Create a schedule that runs every N hours."""
    return str(CronSchedule().every_n_hours(n, jitter=jitter))


# Common presets
class CommonSchedules:
    """Common cron schedule presets."""

    EVERY_MINUTE = "* * * * *"
    EVERY_5_MINUTES = "*/5 * * * *"
    EVERY_15_MINUTES = "*/15 * * * *"
    EVERY_30_MINUTES = "*/30 * * * *"
    EVERY_HOUR = "0 * * * *"
    EVERY_2_HOURS = "0 */2 * * *"
    EVERY_6_HOURS = "0 */6 * * *"
    EVERY_12_HOURS = "0 */12 * * *"

    DAILY_MIDNIGHT = "0 0 * * *"
    DAILY_NOON = "0 12 * * *"

    WEEKLY_SUNDAY_MIDNIGHT = "0 0 * * 0"
    WEEKLY_MONDAY_MIDNIGHT = "0 0 * * 1"

    MONTHLY_FIRST_MIDNIGHT = "0 0 1 * *"
    MONTHLY_LAST_DAY = (
        "0 0 L * *"  # Note: L may not be supported by all cron implementations
    )

    YEARLY_JAN_FIRST = "0 0 1 1 *"
