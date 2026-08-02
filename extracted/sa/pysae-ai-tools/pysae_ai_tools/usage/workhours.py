"""Working-hours calendar for pace/ETA projections.

The usage pace projects consumption linearly over **wall-clock** time, so on the weekly
window the estimate crosses nights and week-ends the user never works through (« you'll hit
extra usage tomorrow at 8am »). This module models the hours actually worked, declared per
weekday, and lets ``pace`` measure elapsed time and project an ETA over *worked* time only —
the ETA then skips the off hours and lands on a real working slot.

Pure and Pydantic-free so it stays trivially testable; the config model is converted to a
:class:`WorkSchedule` via :func:`from_config`.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Protocol

_MINUTES_PER_DAY = 24 * 60
_WEEKDAY_FIELDS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
# Cap the forward walk so a degenerate schedule can never spin forever.
_ADVANCE_HORIZON_DAYS = 60


class _WorkHoursLike(Protocol):
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str


def _parse_hhmm(token: str) -> int | None:
    """Minutes since local midnight for ``HH:MM`` (``24:00`` allowed as an end), else None."""
    parts = token.strip().split(":")
    if len(parts) != 2:
        return None
    try:
        hours, minutes = int(parts[0]), int(parts[1])
    except ValueError:
        return None
    if not (0 <= minutes < 60) or not (0 <= hours <= 24):
        return None
    total = hours * 60 + minutes
    return total if total <= _MINUTES_PER_DAY else None


def parse_ranges(spec: str) -> list[tuple[int, int]]:
    """Parse ``"09:00-12:30,14:00-18:00"`` into sorted, merged ``(start, end)`` minute pairs.

    Invalid or empty segments are ignored; overlapping segments are merged so worked time is
    never double-counted.
    """
    ranges: list[tuple[int, int]] = []
    for segment in spec.split(","):
        segment = segment.strip()
        if not segment:
            continue
        bounds = segment.split("-")
        if len(bounds) != 2:
            continue
        start = _parse_hhmm(bounds[0])
        end = _parse_hhmm(bounds[1])
        if start is None or end is None or start >= end:
            continue
        ranges.append((start, end))
    ranges.sort()
    merged: list[tuple[int, int]] = []
    for start, end in ranges:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def _local_midnight(day: date) -> datetime:
    """Local midnight (aware) of the calendar date ``day``."""
    return datetime(day.year, day.month, day.day).astimezone()


@dataclass(frozen=True)
class WorkSchedule:
    """Worked slots per weekday (index 0 = Monday … 6 = Sunday), minutes since local midnight."""

    days: tuple[tuple[tuple[int, int], ...], ...]

    @property
    def is_empty(self) -> bool:
        return not any(self.days)

    def active_seconds_between(self, start_ts: float, end_ts: float) -> float:
        """Worked seconds within ``[start_ts, end_ts)`` (wall-clock epochs)."""
        if end_ts <= start_ts or self.is_empty:
            return 0.0
        total = 0.0
        cur_date = datetime.fromtimestamp(start_ts).astimezone().date()
        end_date = datetime.fromtimestamp(end_ts).astimezone().date()
        while cur_date <= end_date:
            midnight = _local_midnight(cur_date)
            for slot_start, slot_end in self.days[cur_date.weekday()]:
                lo = max(start_ts, (midnight + timedelta(minutes=slot_start)).timestamp())
                hi = min(end_ts, (midnight + timedelta(minutes=slot_end)).timestamp())
                if hi > lo:
                    total += hi - lo
            cur_date += timedelta(days=1)
        return total

    def advance_active_seconds(self, start_ts: float, needed_active: float) -> float | None:
        """Wall-clock epoch reached after accruing ``needed_active`` worked seconds from
        ``start_ts``, or None if unreached within the safety horizon (or schedule is empty)."""
        if needed_active <= 0:
            return start_ts
        if self.is_empty:
            return None
        remaining = needed_active
        cur_date = datetime.fromtimestamp(start_ts).astimezone().date()
        horizon = start_ts + _ADVANCE_HORIZON_DAYS * 86400.0
        while True:
            midnight = _local_midnight(cur_date)
            if midnight.timestamp() > horizon:
                return None
            for slot_start, slot_end in self.days[cur_date.weekday()]:
                lo = max(start_ts, (midnight + timedelta(minutes=slot_start)).timestamp())
                hi = (midnight + timedelta(minutes=slot_end)).timestamp()
                segment = hi - lo
                if segment <= 0:
                    continue
                if remaining <= segment:
                    return lo + remaining
                remaining -= segment
            cur_date += timedelta(days=1)


def from_config(work_hours: _WorkHoursLike) -> WorkSchedule:
    """Build a :class:`WorkSchedule` from the ``[usage.work_hours]`` config model."""
    return WorkSchedule(tuple(tuple(parse_ranges(getattr(work_hours, field))) for field in _WEEKDAY_FIELDS))


# --- 5H-window priming geometry (pure; consumed by :mod:`.prime`) -----------

FIVE_HOUR_MINUTES = 5 * 60


def day_bounds(schedule: WorkSchedule, weekday: int) -> tuple[int, int] | None:
    """The worked-day envelope ``(start, end)`` in minutes since local midnight for
    ``weekday`` (0 = Monday … 6 = Sunday), or None when the day is off.

    Priming reasons over the whole working day, so a lunch break inside it is irrelevant:
    the envelope spans the first slot's start to the last slot's end (a 5H window is not
    split by a mid-day gap)."""
    slots = schedule.days[weekday]
    if not slots:
        return None
    return slots[0][0], slots[-1][1]


def resets_in_day(start: int, end: int) -> int:
    """How many 5H resets can be placed strictly inside a working day of span ``end-start``.

    Two resets need >5h of room, three need >10h, etc. — so it is ``floor((D-ε)/5h)+1``
    for a positive span. The number of windows that can overlap the day is this plus one."""
    span = end - start
    if span <= 0:
        return 0
    return (span - 1) // FIVE_HOUR_MINUTES + 1


def compute_morning_start(start: int, end: int) -> int:
    """The optimal first-window start (minutes since local midnight) that centres the 5H
    resets inside the working day ``[start, end]``, maximising the number of windows that
    overlap it.

    This is the target, not a lower bound of feasibility: priming *earlier* is
    counter-productive (a reset would fall before ``start`` and cost a window). May be
    negative for a day that starts very early — the caller clamps to the day."""
    span = end - start
    if span <= 0:
        return start
    grappe = (resets_in_day(start, end) - 1) * FIVE_HOUR_MINUTES
    return start + (span - grappe) // 2 - FIVE_HOUR_MINUTES


def target_starts(start: int, end: int) -> list[int]:
    """The full sequence of optimal window-start minutes across the working day, i.e.
    ``compute_morning_start`` then every 5H step — one entry per window that can overlap
    the day. For 09:00–18:00: ``[360, 660, 960]`` (06:00, 11:00, 16:00)."""
    first = compute_morning_start(start, end)
    return [first + i * FIVE_HOUR_MINUTES for i in range(resets_in_day(start, end) + 1)]
