"""
Authoritative next_due_at computation per trigger type.

This is the canonical implementation — the FE has a JS twin (cron-parser),
but the value written to the DB after a recurring run should come from here.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

from croniter import croniter

from .models import TriggerType


def compute_next_due_at(
    trigger_type: TriggerType,
    config: dict[str, Any],
    now: datetime | None = None,
) -> datetime | None:
    """
    Returns the next time this trigger should fire, in UTC.
    Returns None when the trigger is event-driven (context-match, event,
    manual, dependency).
    """
    if now is None:
        now = datetime.now(timezone.utc)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    if trigger_type == "one-shot":
        at = config.get("at")
        if not at:
            return None
        return _parse_iso(at)

    if trigger_type in ("interval", "heartbeat"):
        raw = config.get("every_seconds", 0)
        try:
            every = int(raw)
        except (TypeError, ValueError):
            return None
        if every < 1:
            return None
        return now + timedelta(seconds=every)

    if trigger_type == "cron":
        expression = config.get("expression")
        tz_name = config.get("tz", "UTC")
        if not expression:
            return None
        try:
            tz = ZoneInfo(tz_name)
        except Exception:
            tz = ZoneInfo("UTC")
        local_now = now.astimezone(tz)
        itr = croniter(expression, local_now)
        next_local = itr.get_next(datetime)
        return next_local.astimezone(timezone.utc)

    # context-match / event / manual / dependency — event-driven
    return None


def _parse_iso(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    # Force tzinfo so callers can do arithmetic without TypeError surprises.
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
