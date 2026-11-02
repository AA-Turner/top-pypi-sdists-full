"""Times as this machine's clock shows them: every time the CLI prints, in the device's own zone, with the zone's name.

In one sentence: an instant the gateway sends - ISO with an offset (one without reads as UTC, as the gateway writes),
epoch seconds, or epoch milliseconds - → this machine's zone (`local_zone()`: $TZ when it names a zone, else what
/etc/localtime links to, else UTC) → a short text with the zone's abbreviation: `14:05 EDT` today, `2026-10-11 14:05 EDT`
another day, to the second or the millisecond where a line needs it; a stream of log lines gets a line naming the day and
the zone whenever the day changes, and each line just its time of day.

WHY one module: each command had its own way - `seq audit` printed the gateway's UTC cut to 19 characters and said
nothing of the zone, the `ls` lists cut it to 16, `seq policy logs` printed epoch milliseconds, the eval and capacity
lines converted to UTC and said so, `seq robot` converted to local time and did not say which - while `seq usage` and the
console show your own zone.

Usage and bills are the exception: `seq usage` and a policy's monthly budget go by the billing period, the UTC month,
and say UTC (usage_hist.py, ops_cli.py), as the console's Usage pages and invoices do.

`--json` prints what the gateway sent (ISO with offsets, epoch numbers), for scripts; nothing here touches it.
"""
from __future__ import annotations

import os
from datetime import date, datetime, timezone, tzinfo
from typing import Any


_UNITS = {"minute": "%H:%M", "second": "%H:%M:%S", "milli": "%H:%M:%S"}




_PREFS: dict[str, Any] = {"time_zone": None, "clock": None}


def use(*, time_zone: str | None = None, clock: int | None = None) -> None:
    """Show times in `time_zone` (an IANA zone; None: this machine's) on a `clock` of 12 or 24 hours (None: 24)."""
    _PREFS.update(time_zone=time_zone or None, clock=clock if clock in (12, 24) else None)


def local_zone() -> str:
    """The IANA zone times are shown in: the one you chose (use) when it names one, else this machine's - $TZ when it
    names one, else what /etc/localtime links to - else UTC."""
    from zoneinfo import ZoneInfo

    for name in (_PREFS["time_zone"] or "", os.environ.get("TZ", "").lstrip(":"), _linked_zone()):
        if name:
            try:
                ZoneInfo(name)
                return name
            except Exception:
                continue
    return "UTC"


def _linked_zone() -> str:
    """/etc/localtime → .../zoneinfo/America/New_York → America/New_York (macOS and Linux)."""
    try:
        target = os.path.realpath("/etc/localtime")
    except OSError:
        return ""
    return target.split("zoneinfo/", 1)[1] if "zoneinfo/" in target else ""


def _zone() -> tzinfo:
    """local_zone() as a tzinfo, looked up on each call: $TZ can change within one process (the tests set it)."""
    from zoneinfo import ZoneInfo

    return ZoneInfo(local_zone())


def instant(value: Any, *, ms: bool = False) -> datetime | None:
    """`value` on this machine's clock: an ISO time, a datetime, epoch seconds - or epoch milliseconds with `ms`. None
    when there is none or it cannot be read as a time."""
    if value is None or value == "" or isinstance(value, bool):
        return None
    try:
        if isinstance(value, datetime):
            t = value
        elif isinstance(value, (int, float)):
            t = datetime.fromtimestamp(float(value) / (1000.0 if ms else 1.0), timezone.utc)
        else:
            t = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except (TypeError, ValueError, OverflowError, OSError):
        return None
    return (t if t.tzinfo else t.replace(tzinfo=timezone.utc)).astimezone(_zone())


def stamp(value: Any, *, unit: str = "minute", day: str = "auto", zone: bool = True, ms: bool = False,
          now: datetime | None = None) -> str:
    """`value` (as `instant` reads it) on this machine's clock: the time of day to the `unit` ("minute" 14:05,
    "second" 14:05:09, "milli" 14:05:09.149; 2:05 PM on a 12-hour clock, use), after the date when `day` asks for it
    , and the
    zone's abbreviation (EDT) unless `zone` is False - for a table whose heading names the zone once. '—' for no time;
    the value as it came when it is not one."""
    t = instant(value, ms=ms)
    if t is None:
        return "—" if value is None or value == "" else str(value)
    twelve = _PREFS["clock"] == 12
    fmt = _UNITS.get(unit, "%H:%M")
    text = t.strftime(fmt.replace("%H", "%I") if twelve else fmt)
    if unit == "milli":
        text += f".{t.microsecond // 1000:03d}"
    if twelve:
        text = f"{text.lstrip('0') or '0'} {'AM' if t.hour < 12 else 'PM'}"
    today = (now.astimezone(t.tzinfo) if now else datetime.now(t.tzinfo)).date()
    if day == "always" or (day == "auto" and t.date() != today):
        text = f"{t:%Y-%m-%d} {text}"
    elif day == "short" and t.date() != today:
        text = f"{t:%m-%d} {text}"
    return f"{text} {t.tzname()}" if zone else text


def day_of(value: Any, *, ms: bool = False) -> str:
    """The date `value` falls on here, 2026-10-11; '—' for no time."""
    t = instant(value, ms=ms)
    return f"{t:%Y-%m-%d}" if t else ("—" if value is None or value == "" else str(value))


def zone_name(at: Any = None) -> str:
    """This machine's zone as its abbreviation at `at` (default now): EDT, or EST in winter."""
    t = instant(at) if at is not None else None
    return (t or datetime.now(_zone())).tzname() or local_zone()


class Days:
    """For a stream of log lines, each printed with its time of day only: the line to put before a line whose day (here)
    differs from the line before it - `── Mon 2026-10-12 · EDT ──` - so a date and the zone are said once a day, not on
    every line. One per stream; a stream printed in pieces (--follow) keeps the same one."""

    def __init__(self) -> None:
        self._day: date | None = None

    def head(self, t: datetime) -> str | None:
        if t.date() == self._day:
            return None
        self._day = t.date()
        return f"── {t:%a %Y-%m-%d} · {t.tzname()} ──"
