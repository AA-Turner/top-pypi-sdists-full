from __future__ import annotations

import time
from datetime import UTC, datetime

# GNU coreutils six-month rule: 15552000 seconds = 180 days.
_SIX_MONTHS_SECONDS = 15552000

_MONTHS = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


def format_date_ls(mtime: float, now: float | None = None) -> str:
    if now is None:
        now = time.time()
    dt = datetime.fromtimestamp(mtime, tz=UTC)
    month = _MONTHS[dt.month - 1]
    # Space-padded day (1 -> " 1", 10 -> "10").
    day_str = f"{dt.day:>2d}"
    delta = now - mtime
    if 0 <= delta <= _SIX_MONTHS_SECONDS:
        # "Mmm DD HH:MM" -> 12 chars
        return f"{month} {day_str} {dt.hour:02d}:{dt.minute:02d}"
    # "Mmm DD  YYYY" with two spaces before the year -> 12 chars
    return f"{month} {day_str}  {dt.year:04d}"


def format_iso_nanos(epoch: float) -> str:
    # `2026-05-07 17:54:23.000000000 +0000`
    dt = datetime.fromtimestamp(epoch, tz=UTC)
    # Build nanoseconds from the float fractional part, deterministically.
    whole = int(epoch)
    frac = epoch - whole
    if frac < 0:
        frac = 0.0
    nanos = int(round(frac * 1_000_000_000))
    if nanos >= 1_000_000_000:
        nanos = 999_999_999
    return (
        f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d} "
        f"{dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}."
        f"{nanos:09d} +0000"
    )


def format_stat_y(epoch: float) -> str:
    # `%y` from stat: same as iso_nanos.
    return format_iso_nanos(epoch)
