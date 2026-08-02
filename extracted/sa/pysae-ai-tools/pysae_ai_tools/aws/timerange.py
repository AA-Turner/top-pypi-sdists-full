"""Shared time-range parsing for the AWS spot commands.

Two ways to define a window, both capped at CloudTrail's 90-day history:

* relative — ``--period 7d`` / ``24h`` / ``2w`` / ``1m`` (month = 30 days);
* absolute — ``--from 2026-05-01 [--to 2026-05-31]`` (``--to`` defaults to now).
"""

from datetime import datetime, timedelta, timezone

MAX_HISTORY_DAYS = 90


def parse_period(period: str) -> timedelta:
    """Parse a duration like ``7d``, ``24h``, ``2w``, ``1m`` (month = 30 days).

    A bare integer is interpreted as days. Raises ``ValueError`` otherwise.
    """
    period = period.strip().lower()
    if period.isdigit():
        return timedelta(days=int(period))
    unit = period[-1]
    try:
        value = int(period[:-1])
    except ValueError as exc:
        raise ValueError(f"invalid period {period!r} (use forms like 7d, 24h, 2w, 1m)") from exc
    if value <= 0:
        raise ValueError(f"period must be positive, got {period!r}")
    multipliers = {"h": timedelta(hours=1), "d": timedelta(days=1), "w": timedelta(weeks=1), "m": timedelta(days=30)}
    if unit not in multipliers:
        raise ValueError(f"unknown period unit {unit!r} in {period!r} (use h, d, w, or m)")
    return value * multipliers[unit]


def parse_date(value: str) -> datetime:
    """Parse ``YYYY-MM-DD`` or a full ISO timestamp into a UTC-aware datetime."""
    text = value.strip()
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"invalid date {value!r} (use YYYY-MM-DD or an ISO timestamp)") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_window(
    period: str,
    since: str,
    until: str,
    *,
    now: datetime,
    max_days: int = MAX_HISTORY_DAYS,
) -> tuple[str, str]:
    """Resolve a (start_iso, end_iso) window from ``--period`` or ``--from/--to``.

    ``since`` (absolute) takes precedence over ``period`` (relative). ``until``
    defaults to ``now``. Raises ``ValueError`` on an empty/inverted window or one
    longer than ``max_days``.
    """
    if since:
        start = parse_date(since)
        end = parse_date(until) if until else now
    else:
        if until:
            raise ValueError("--to requires --from (use --period for a relative window).")
        end = now
        start = now - parse_period(period)

    if end <= start:
        raise ValueError(f"empty window: end ({_iso(end)}) is not after start ({_iso(start)}).")
    if end - start > timedelta(days=max_days):
        raise ValueError(
            f"window spans more than {max_days} days — CloudTrail's event history only goes back {max_days} days."
        )
    return _iso(start), _iso(end)
