"""Consumption pace for a plan window — are we burning the budget faster than linear?

Pace is a simple rule of three over the whole window:
``pace = utilization% / fraction_of_window_elapsed``. So 100 = exactly on pace, 50 =
under-consuming, 200 = twice too fast. It is also the **projection**: at the current rate
the window ends at ~``pace``%. From the same linear rate we estimate **at what time** usage
will cross a target threshold (extra usage at 100%, or the configured block threshold).
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .workhours import WorkSchedule

FIVE_HOUR_SECONDS = 5 * 3600.0
WEEK_SECONDS = 7 * 86400.0
_MIN_ELAPSED_FRACTION = 0.05  # the first ~5% of the window is too noisy to rate
# Projected end-of-window utilization bands (100 = exactly on pace):
_UNDER_PACE = 60.0  # below → 🐢 sous-productif
_OVER_PACE = 110.0  # above → 🔥 sur-productif; in between → ✅ bon rythme

# 🐢 slower than ideal · ✅ on pace · 🔥 burning fast
_EMOJI = {"sous-productif": "🐢", "bon rythme": "✅", "sur-productif": "🔥"}
_FR_WEEKDAYS = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."]


@dataclass
class Pace:
    pct: float  # projected end-of-window utilization at the current rate; 100 = on pace
    label: str  # "sous-productif" | "bon rythme" | "sur-productif"
    utilization: float  # current usage %
    wall_rate_per_s: float  # % per wall-clock second
    time_to_reset: float  # seconds until the window resets
    # Worked-time model, present only when a non-empty work schedule was applied:
    schedule: WorkSchedule | None = None
    now: float = 0.0  # reference epoch for the worked-time projection
    active_rate_per_s: float | None = None  # % per worked second
    active_remaining: float | None = None  # worked seconds left before the window resets

    def eta_to(self, target_pct: float) -> float | None:
        """Wall-clock seconds until usage reaches ``target_pct`` at the wall-clock rate —
        None if already past it, rate is zero, or it would only happen after the reset.
        Used when no work schedule applies (the historical behaviour)."""
        if self.wall_rate_per_s <= 0 or target_pct <= self.utilization:
            return None
        seconds = (target_pct - self.utilization) / self.wall_rate_per_s
        return seconds if 0 <= seconds < self.time_to_reset else None

    def worked_seconds_to(self, target_pct: float) -> float | None:
        """Amount of **worked** time (seconds) still needed to reach ``target_pct`` at the
        current worked-hours rate. None when no work model, rate is zero, target already
        reached, or it can't be reached with the worked time left before the reset.

        Both schedule-aware ETAs derive from this single quantity: the 24/7 estimate lays it
        out as continuous wall time, the worked estimate spreads it across working hours only —
        so the two coincide exactly when no off hours fall in between."""
        if self.active_rate_per_s is None or self.active_remaining is None or self.active_rate_per_s <= 0:
            return None
        if target_pct <= self.utilization:
            return None
        needed = (target_pct - self.utilization) / self.active_rate_per_s
        return needed if 0 < needed <= self.active_remaining else None

    def eta_to_active(self, target_pct: float) -> float | None:
        """Wall-clock seconds until ``target_pct`` counting only worked hours (the projection
        skips off hours), or None when unreachable / no work model."""
        needed = self.worked_seconds_to(target_pct)
        if needed is None or self.schedule is None:
            return None
        eta_ts = self.schedule.advance_active_seconds(self.now, needed)
        return None if eta_ts is None else eta_ts - self.now


def compute(
    utilization: float,
    resets_at: datetime | None,
    now: float,
    window_seconds: float,
    schedule: WorkSchedule | None = None,
) -> Pace | None:
    """Pace for a window, or None when it can't be rated (no reset, no usage, too early).

    With a non-empty ``schedule`` the rhythm and the ETA are computed over worked hours only:
    the ETA is a single worked-time budget (:meth:`Pace.worked_seconds_to`) rendered two ways —
    spread across working hours, and laid out 24/7. Without a schedule the wall-clock rate is
    used and the result is identical to the historical behaviour.
    """
    if resets_at is None or utilization <= 0 or window_seconds <= 0:
        return None
    time_to_reset = resets_at.timestamp() - now
    elapsed = window_seconds - time_to_reset
    if elapsed <= 0:
        return None
    wall_rate = utilization / elapsed
    fraction = min(elapsed / window_seconds, 1.0)

    active_schedule: WorkSchedule | None = None
    active_rate: float | None = None
    active_remaining: float | None = None
    if schedule is not None and not schedule.is_empty:
        window_start = resets_at.timestamp() - window_seconds
        active_elapsed = schedule.active_seconds_between(window_start, now)
        active_total = schedule.active_seconds_between(window_start, resets_at.timestamp())
        if active_elapsed > 0 and active_total > 0:
            active_schedule = schedule
            fraction = min(active_elapsed / active_total, 1.0)
            active_rate = utilization / active_elapsed
            active_remaining = max(0.0, active_total - active_elapsed)

    if fraction < _MIN_ELAPSED_FRACTION:
        return None
    label_pct = utilization / fraction
    label = (
        "sous-productif" if label_pct < _UNDER_PACE else ("sur-productif" if label_pct > _OVER_PACE else "bon rythme")
    )
    return Pace(
        pct=label_pct,
        label=label,
        utilization=utilization,
        wall_rate_per_s=wall_rate,
        time_to_reset=max(0.0, time_to_reset),
        schedule=active_schedule,
        now=now,
        active_rate_per_s=active_rate,
        active_remaining=active_remaining,
    )


def round_to_minute(dt: datetime) -> datetime:
    """Round a datetime to the nearest minute. The usage API returns reset instants a hair
    shy of the minute (e.g. ``11:09:59.97``); truncating with ``%H:%M`` would show ``11h09``
    where the window actually resets at ``11h10`` — the value ``/usage`` displays."""
    return (dt + timedelta(seconds=30)).replace(second=0, microsecond=0)


def _when(now: float, seconds_ahead: float) -> str:
    """ETA target as ``17h30`` when it lands today, else ``ven. 04/07 à 17h30``."""
    target = round_to_minute(datetime.fromtimestamp(now + seconds_ahead, timezone.utc).astimezone())
    if target.date() == datetime.fromtimestamp(now, timezone.utc).astimezone().date():
        return target.strftime("%Hh%M")
    return f"{_FR_WEEKDAYS[target.weekday()]} {target.strftime('%d/%m')} à {target.strftime('%Hh%M')}"


def format_clock(when: datetime, now: float) -> str:
    """A fixed local clock time (not a projection): ``17h30`` when it falls on the same
    day as ``now``, else ``ven. 04/07 à 17h30``. Used for the window's start and end
    bounds shown in the notification body."""
    target = round_to_minute(when.astimezone())
    if target.date() == datetime.fromtimestamp(now, timezone.utc).astimezone().date():
        return target.strftime("%Hh%M")
    return f"{_FR_WEEKDAYS[target.weekday()]} {target.strftime('%d/%m')} à {target.strftime('%Hh%M')}"


def format_short(pace: Pace) -> str:
    """Compact rhythm for the notification title (no emoji — the caller prepends one)."""
    return f"Rythme {pace.pct:.0f}%"


def emoji(pace: Pace) -> str:
    """Rhythm pictogram for the notification title (🐢 under · ✅ on pace · 🔥 over)."""
    return _EMOJI.get(pace.label, "")


def eta_text(pace: Pace, now: float, block_at: float) -> str:
    """`` · 🔒 ≈ 17h30`` (blocage) / `` · 💸 ≈ 17h30`` (extra usage) for the next binding
    threshold, else ``""``.

    When a work schedule is applied, two estimates are given — the worked-hours one (which
    skips off hours) and the raw 24/7 one, e.g. `` · 💸 ≈ lun. 13/07 à 11h11 (ouvré) · 20h11
    (24/7)`` — unless the projection crosses no off hours, in which case they coincide and
    only one is shown.
    """
    if block_at > 0 and not (block_at > 100 and pace.utilization < 100):
        target, picto = block_at, "🔒"
    else:
        target, picto = 100.0, "💸"
    needed = pace.worked_seconds_to(target)
    if needed is None:
        if pace.active_rate_per_s is not None:
            return ""  # work model applies but target is unreachable within work hours before reset
        eta = pace.eta_to(target)  # no work model → historical wall-clock estimate
        return f" · {picto} ≈ {_when(now, eta)}" if eta is not None else ""
    worked = pace.eta_to_active(target)
    if worked is None:
        return ""
    when_worked = _when(now, worked)
    when_continuous = _when(now, needed)  # same worked time, laid out 24/7
    if when_worked == when_continuous:
        return f" · {picto} ≈ {when_worked}"
    return f" · {picto} ≈ {when_worked} (ouvré) · {when_continuous} (24/7)"
