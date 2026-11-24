"""
Authoritative next_due_at computation per trigger type.

This is the canonical implementation — the FE has a JS twin (cron-parser),
but the value written to the DB after a recurring run should come from here.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, UTC
from typing import Any
from zoneinfo import ZoneInfo

from croniter import croniter

from .models import TriggerType

log = logging.getLogger(__name__)


class InvalidTriggerTiming(ValueError):
    """A trigger's time expression the scheduler cannot read (a cron expression, a timezone, an
    interval, a one-shot time). Refused at every write door as 422 naming what is wrong — never a
    500, and never a stored trigger that silently never fires (CGU-10, 2026-11-09)."""


class InvalidCronExpression(InvalidTriggerTiming):
    """A cron trigger's expression croniter cannot read (out-of-range field, wrong column count,
    not a string, or a date that never comes such as ``0 0 31 2 *``).

    Still a ``ValueError`` so every existing caller behaves as before; the HTTP doors catch it
    and answer 422 naming the expression instead of crashing with a 500."""

    def __init__(self, expression: str, reason: str) -> None:
        self.expression = expression
        self.reason = reason
        super().__init__(f"invalid cron expression {expression!r}: {reason}")


class InvalidCronTimezone(InvalidCronExpression):
    """A cron trigger's ``tz`` is not an IANA zone name. Refused at the write doors (422)."""

    def __init__(self, tz_name: str) -> None:
        self.tz_name = tz_name
        ValueError.__init__(self, f"unknown cron timezone {tz_name!r}: use an IANA name like 'America/Los_Angeles'")
        self.expression = ""
        self.reason = f"unknown timezone {tz_name!r}"


def require_valid_cron(expression: Any, tz_name: Any = "UTC", *, now: datetime | None = None) -> datetime:
    """THE one cron check: every door (``POST /scheduler/cron/validate`` included) asks this.

    Returns the next fire in UTC; raises ``InvalidCronTimezone`` / ``InvalidCronExpression`` for
    anything the scanner could not fire — a non-string, a malformed or out-of-range expression,
    or one whose next date never comes (croniter raises that only on ``get_next``)."""
    if not isinstance(expression, str) or not expression.strip():
        raise InvalidCronExpression(str(expression or ""), "a cron trigger needs config.expression, e.g. '0 9 * * 1-5'")
    if not isinstance(tz_name, str) or not tz_name:
        raise InvalidCronTimezone(str(tz_name))
    try:
        tz = ZoneInfo(tz_name)
    except Exception as exc:
        raise InvalidCronTimezone(tz_name) from exc
    base = (now or datetime.now(UTC)).astimezone(tz)
    try:
        return croniter(expression, base).get_next(datetime).astimezone(UTC)
    except Exception as exc:  # croniter raises ValueError, KeyError, TypeError, AttributeError
        raise InvalidCronExpression(expression, str(exc) or type(exc).__name__) from exc


def validate_trigger_timing(trigger_type: Any, config: dict[str, Any] | None) -> None:
    """Refuse, at a write door, a trigger time the scheduler would crash on or never fire.

    cron: ``require_valid_cron``. interval/heartbeat: ``every_seconds`` a whole number >= 1.
    one-shot: ``at`` an ISO-8601 time. Event-driven types carry no time and pass."""
    config = config or {}
    if trigger_type == "cron":
        require_valid_cron(config.get("expression"), config.get("tz", "UTC"))
    elif trigger_type in ("interval", "heartbeat"):
        raw = config.get("every_seconds")
        if isinstance(raw, bool) or not isinstance(raw, (int, float, str)):
            raise InvalidTriggerTiming(f"{trigger_type} trigger needs config.every_seconds, a whole number of seconds >= 1")
        try:
            every = int(raw)
        except (TypeError, ValueError):
            every = 0
        if every < 1:
            raise InvalidTriggerTiming(
                f"{trigger_type} trigger every_seconds {raw!r} is not a whole number of seconds >= 1"
            )
    elif trigger_type == "one-shot":
        if _parse_iso(config.get("at")) is None:
            raise InvalidTriggerTiming(
                f"one-shot trigger at {config.get('at')!r} is not an ISO-8601 time, e.g. '2030-01-01T12:00:00Z'"
            )


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
        now = datetime.now(UTC)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=UTC)

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
            # Stored before the write doors refused it: keep firing, but never silently.
            log.warning("cron trigger tz %r is not a known timezone; computing in UTC", tz_name)
            tz = ZoneInfo("UTC")
        local_now = now.astimezone(tz)
        try:
            next_local = croniter(expression, local_now).get_next(datetime)
        except Exception as exc:  # bad syntax, a non-string, or a date that never comes
            raise InvalidCronExpression(str(expression), str(exc) or type(exc).__name__) from exc
        return next_local.astimezone(UTC)

    # context-match / event / manual / dependency — event-driven
    return None


def _parse_iso(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    # Force tzinfo so callers can do arithmetic without TypeError surprises.
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
