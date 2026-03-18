"""Minimal 5-field cron expression evaluator with safety bounds.

Pure Python, no external dependencies. Supports standard cron syntax:
``*``, ranges (``1-5``), steps (``*/15``), lists (``1,15``), and
common aliases (``@hourly``, ``@daily``, ``@weekly``, ``@monthly``).

Safety layers:
1. Field range validation at parse time
2. 4-year look-ahead cap in ``next_occurrence()``
3. Minimum interval enforcement at storage time (caller responsibility)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

# Field definitions: (name, min, max)
_FIELDS = [
    ("minute", 0, 59),
    ("hour", 0, 23),
    ("day", 1, 31),
    ("month", 1, 12),
    ("dow", 0, 6),  # 0=Sunday
]

_ALIASES: dict[str, str] = {
    "@yearly": "0 0 1 1 *",
    "@annually": "0 0 1 1 *",
    "@monthly": "0 0 1 * *",
    "@weekly": "0 0 * * 0",
    "@daily": "0 0 * * *",
    "@midnight": "0 0 * * *",
    "@hourly": "0 * * * *",
}

_MAX_LOOKAHEAD_YEARS = 4


def _parse_field(token: str, min_val: int, max_val: int, field_name: str) -> frozenset[int]:
    """Parse a single cron field into a set of matching values."""
    values: set[int] = set()

    for part in token.split(","):
        part = part.strip()
        if not part:
            raise ValueError(f"Cron field {field_name!r}: empty segment")

        step = 1
        if "/" in part:
            base, step_str = part.split("/", 1)
            if not step_str.isdigit() or int(step_str) == 0:
                raise ValueError(f"Cron field {field_name!r}: invalid step {step_str!r}")
            step = int(step_str)
            part = base

        if part == "*":
            values.update(range(min_val, max_val + 1, step))
        elif "-" in part:
            lo_str, hi_str = part.split("-", 1)
            if not lo_str.isdigit() or not hi_str.isdigit():
                raise ValueError(f"Cron field {field_name!r}: invalid range {part!r}")
            lo, hi = int(lo_str), int(hi_str)
            if lo < min_val or hi > max_val or lo > hi:
                raise ValueError(f"Cron field {field_name!r}: range {lo}-{hi} outside [{min_val},{max_val}]")
            values.update(range(lo, hi + 1, step))
        else:
            if not part.isdigit():
                raise ValueError(f"Cron field {field_name!r}: invalid value {part!r}")
            val = int(part)
            if val < min_val or val > max_val:
                raise ValueError(f"Cron field {field_name!r}: value {val} outside [{min_val},{max_val}]")
            values.add(val)

    if not values:
        raise ValueError(f"Cron field {field_name!r}: resolved to empty set")
    return frozenset(values)


@dataclass(frozen=True)
class CronSchedule:
    """Parsed cron schedule with field sets for matching."""

    minutes: frozenset[int]
    hours: frozenset[int]
    days: frozenset[int]
    months: frozenset[int]
    dows: frozenset[int]
    expression: str

    def matches(self, dt: datetime) -> bool:
        """Check if a datetime matches this cron schedule."""
        return (
            dt.minute in self.minutes
            and dt.hour in self.hours
            and dt.day in self.days
            and dt.month in self.months
            and dt.weekday() in self._iso_dows()
        )

    def _iso_dows(self) -> frozenset[int]:
        """Convert cron DOW (0=Sun) to Python weekday (0=Mon)."""
        # cron: 0=Sun, 1=Mon, ..., 6=Sat
        # Python: 0=Mon, 1=Tue, ..., 6=Sun
        return frozenset((d - 1) % 7 for d in self.dows)

    def next_occurrence(self, after: datetime) -> datetime:
        """Find the next datetime matching this schedule after the given time.

        All times are UTC. Raises ValueError if no match is found within
        4 years (prevents infinite loops from impossible expressions).
        """
        cutoff = after + timedelta(days=_MAX_LOOKAHEAD_YEARS * 366)
        dt = after.replace(second=0, microsecond=0) + timedelta(minutes=1)
        iso_dows = self._iso_dows()

        while dt <= cutoff:
            if dt.month not in self.months:
                # Skip to first day of next matching month
                dt = _advance_to_next_month(dt, self.months)
                continue
            if dt.day not in self.days or dt.weekday() not in iso_dows:
                dt = dt.replace(hour=0, minute=0) + timedelta(days=1)
                continue
            if dt.hour not in self.hours:
                dt = dt.replace(minute=0) + timedelta(hours=1)
                continue
            if dt.minute not in self.minutes:
                dt += timedelta(minutes=1)
                continue
            return dt

        raise ValueError(f"No matching datetime found within {_MAX_LOOKAHEAD_YEARS} years for: {self.expression}")


def _advance_to_next_month(dt: datetime, valid_months: frozenset[int]) -> datetime:
    """Advance to the first day of the next matching month."""
    month = dt.month
    year = dt.year
    for _ in range(50):  # Safety: max ~4 years of months
        month += 1
        if month > 12:
            month = 1
            year += 1
        if month in valid_months:
            return dt.replace(year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    raise ValueError("Could not find next matching month")


def parse_cron(expression: str) -> CronSchedule:
    """Parse a 5-field cron expression into a CronSchedule.

    Supports aliases: @hourly, @daily, @weekly, @monthly, @yearly.
    """
    expr = expression.strip()
    if expr in _ALIASES:
        expr = _ALIASES[expr]

    parts = expr.split()
    if len(parts) != 5:
        raise ValueError(f"Cron expression must have 5 fields, got {len(parts)}: {expression!r}")

    fields = []
    for i, (name, min_val, max_val) in enumerate(_FIELDS):
        fields.append(_parse_field(parts[i], min_val, max_val, name))

    return CronSchedule(
        minutes=fields[0],
        hours=fields[1],
        days=fields[2],
        months=fields[3],
        dows=fields[4],
        expression=expression.strip(),
    )


def min_interval_seconds(schedule: CronSchedule) -> int:
    """Estimate the minimum interval between consecutive occurrences.

    Used for denial-of-wallet prevention at schedule registration time.
    """
    # Use next_occurrence to find two consecutive matches
    now = datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc)
    try:
        first = schedule.next_occurrence(now)
        second = schedule.next_occurrence(first)
        return int((second - first).total_seconds())
    except ValueError:
        return _MAX_LOOKAHEAD_YEARS * 366 * 86400  # Unreachable schedule
