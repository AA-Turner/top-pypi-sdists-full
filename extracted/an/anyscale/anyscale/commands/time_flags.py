"""Shared parsing and rendering for the time flags of the observability commands.

`anyscale <resource> events` and `anyscale metrics ...` take the same inputs:

- a point in time is ISO 8601, e.g. ``2026-09-01T10:00:00Z``. A trailing ``Z`` or an
  explicit offset is accepted, a date-only value is accepted, and a value without a
  timezone is taken as UTC;
- a duration is a number followed by ``s``, ``m``, ``h`` or ``d``, e.g. ``30m``, ``2h``,
  ``1d``.

Every parser raises ``click.UsageError`` naming the flag, so the user sees which flag
was wrong and what it accepts.
"""

from datetime import datetime, timedelta, timezone
import re
from typing import Optional, Tuple

import click


_DURATION_PATTERN = re.compile(r"^(\d+)([smhd])$")
_DURATION_UNITS = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days"}


def parse_duration(value: str, flag: str = "--since") -> timedelta:
    """``30m`` -> 30 minutes. Raises UsageError naming ``flag`` on anything else."""
    match = _DURATION_PATTERN.match(value.strip())
    if not match:
        raise click.UsageError(
            f"Invalid {flag} value {value!r}. Use a number followed by s, m, h or d, "
            "e.g. 30m or 2h."
        )
    amount, unit = match.groups()
    return timedelta(**{_DURATION_UNITS[unit]: int(amount)})


def parse_timestamp(value: Optional[str], flag: str) -> Optional[datetime]:
    """ISO 8601 -> timezone-aware datetime (UTC when none is given). None stays None."""
    if value is None:
        return None
    text = value.strip()
    # Python 3.9's fromisoformat does not accept a trailing "Z".
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        raise click.UsageError(
            f"Invalid {flag} value {value!r}. Use ISO 8601, e.g. 2026-09-01T10:00:00Z."
        ) from None
    # A timestamp without a timezone is taken as UTC.
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def format_timestamp(value: datetime) -> str:
    """Render as ``2026-09-01T10:00:00Z``: UTC, second precision."""
    utc = value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return utc.strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_window(
    since: Optional[str], start_time: Optional[str], end_time: Optional[str]
) -> Tuple[Optional[datetime], Optional[datetime]]:
    """Turn ``--since`` / ``--start-time`` / ``--end-time`` into one (start, end) pair.

    ``--since`` expands to (now - duration, now) and cannot be combined with the other
    two. A flag that was not given stays None.
    """
    if since is not None and (start_time is not None or end_time is not None):
        raise click.UsageError("--since cannot be combined with --start-time or --end-time.")

    if since is not None:
        now = datetime.now(timezone.utc)
        return now - parse_duration(since, "--since"), now

    return parse_timestamp(start_time, "--start-time"), parse_timestamp(end_time, "--end-time")
