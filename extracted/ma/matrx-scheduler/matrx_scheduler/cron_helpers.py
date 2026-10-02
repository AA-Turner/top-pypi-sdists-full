"""
Cron parser helpers used by the /scheduling/validate-cron route in the host.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable
from zoneinfo import ZoneInfo

from croniter import croniter


def validate_cron(expression: str, tz: str = "UTC") -> str | None:
    """Returns None on success, error message on failure."""
    try:
        ZoneInfo(tz)
    except Exception:
        return f"unknown timezone: {tz}"
    try:
        croniter(expression, datetime.now(timezone.utc))
    except Exception as exc:  # croniter raises ValueError, KeyError, etc.
        return f"invalid cron expression: {exc}"
    return None


def next_n_fires(
    expression: str,
    tz: str,
    n: int,
    start: datetime | None = None,
) -> list[datetime]:
    """Returns the next N fire times as UTC datetimes."""
    if start is None:
        start = datetime.now(timezone.utc)
    elif start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)

    try:
        zoneinfo = ZoneInfo(tz)
    except Exception:
        zoneinfo = ZoneInfo("UTC")

    local_start = start.astimezone(zoneinfo)
    itr = croniter(expression, local_start)
    out: list[datetime] = []
    for _ in range(max(1, n)):
        local_next = itr.get_next(datetime)
        out.append(local_next.astimezone(timezone.utc))
    return out


def fire_count_in_window(
    expression: str,
    tz: str,
    start: datetime,
    end: datetime,
    limit: int = 10000,
) -> int:
    """Count how many times this cron fires between [start, end). Capped."""
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    try:
        zoneinfo = ZoneInfo(tz)
    except Exception:
        zoneinfo = ZoneInfo("UTC")
    itr = croniter(expression, start.astimezone(zoneinfo))
    count = 0
    while count < limit:
        nxt = itr.get_next(datetime)
        if nxt >= end.astimezone(zoneinfo):
            break
        count += 1
    return count
