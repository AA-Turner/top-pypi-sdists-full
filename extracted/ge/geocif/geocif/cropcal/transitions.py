# -*- coding: utf-8 -*-
"""Remote-sensing transition days from the masked phenology curve.

Mid-greenup is the steepest rise of the fitted NDVI curve and mid-greendown the
steepest fall, after which four corrections may move them:

* **winter wheat, temperate, northern** -- greenup is the earlier of the
  derivative maximum and the day thermal accumulation resumes;
* **winter wheat, temperate, southern** -- greenup is the day after the coldest
  ten-day window;
* **every other crop** -- greenup must be at least 100 GDD after the calendar
  planting date;
* **every crop** -- accumulated GDD between the two transitions must lie inside
  the crop's ``[min_gdd, max_gdd]``, scaled by 0.75 outside the tropics.

Each correction is reproduced from ``util_cal.get_rs_calendar_info``. Where the
original could crash or return a silently wrong day, the failure is converted
into a recorded note and the date is left alone; see ``DEVIATIONS.md`` and the
``notes`` field of :class:`Transitions`.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from geocif.cropcal import circular, naming

logger = logging.getLogger(__name__)

#: Window, in days, for the southern-hemisphere winter-wheat GDD moving average.
MOVING_WINDOW_SIZE = 10

#: Minimum GDD between the calendar planting date and remote-sensing greenup.
MIN_GDD_AFTER_PLANTING = 100.0

#: Winter wheat, northern hemisphere: greenup may not precede this day.
WINTER_WHEAT_GREENUP_FLOOR = 60

#: Which day with GDD > 0 counts as "thermal accumulation has resumed". The
#: original used index 5 -- the sixth such day, not the first.
GDD_RESUME_INDEX = 5

#: A leading run of identical NDVI values shorter than this is treated as noise
#: rather than a genuine flat winter.
MIN_FLAT_RUN = 30


class TransitionError(ValueError):
    """The masked curve carries no usable signal."""


@dataclass
class Transitions:
    """Remote-sensing transition days, with a record of what moved them."""

    midgreenup: int
    midgreendown: int
    notes: list[str] = field(default_factory=list)

    def note(self, text: str) -> None:
        self.notes.append(text)


def moving_average(values: np.ndarray, window: int) -> np.ndarray:
    """Trailing-aligned moving average, ``'valid'`` mode, as in the original."""
    weights = np.repeat(1.0, window) / window
    return np.convolve(np.asarray(values, dtype=float), weights, "valid")


def leading_flat_run(values: np.ndarray) -> int:
    """Length of the leading run of exactly-equal values.

    ``group_consecutives(fitted, stepsize=0.0)`` in the original, which tests
    ``np.diff(...) != 0.0`` for **exact float equality** on a Fourier-fitted
    curve. In practice that run is one sample long, so the caller's ``< 30``
    guard always fires and the constraint it guards is inert. Reproduced
    deliberately -- see :func:`_winter_wheat_northern`.
    """
    arr = np.asarray(values, dtype=float)
    changes = np.flatnonzero(np.diff(arr) != 0.0)
    return int(changes[0] + 1) if changes.size else arr.size


def _derivative_transitions(curve_values: np.ndarray) -> tuple[int, int]:
    """Steepest rise and steepest fall of the masked curve.

    Tie-breaking is asymmetric and inherited: the rise takes the **last**
    occurrence of the maximum, the fall takes the **first** occurrence of the
    minimum. Both indices refer to ``np.diff``, so each is the day before the
    extremum of the rate of change.
    """
    diff = np.diff(np.asarray(curve_values, dtype=float)[: circular.N_DOY])
    if not np.isfinite(diff).any():
        raise TransitionError("masked curve is entirely NaN")

    greenup = int(np.flatnonzero(diff == np.nanmax(diff))[-1])
    greendown = int(np.nanargmin(diff))
    return greenup, greendown


def _winter_wheat_northern(
    greenup: int, curve_values: np.ndarray, gdd: np.ndarray, out: Transitions
) -> int:
    """Greenup is the earlier of the derivative maximum and the thermal restart."""
    positive = np.flatnonzero(np.asarray(gdd, dtype=float) > 0.0)
    if positive.size <= GDD_RESUME_INDEX:
        # The original indexed [5] unconditionally and raised IndexError on any
        # region with five or fewer thawing days.
        out.note("winter_wheat_N: fewer than 6 days with GDD > 0; GDD rule skipped")
        return greenup

    resume = max(int(positive[GDD_RESUME_INDEX]), WINTER_WHEAT_GREENUP_FLOOR)
    if resume < greenup:
        out.note(f"winter_wheat_N: greenup pulled back to GDD restart {resume}")
        greenup = resume

    flat_run = leading_flat_run(curve_values)
    if flat_run < MIN_FLAT_RUN:
        # Inert by construction on a fitted curve; kept so the port matches.
        flat_run = circular.N_DOY
    if greenup > flat_run:
        out.note(f"winter_wheat_N: greenup pushed to first NDVI change {flat_run + 1}")
        greenup = flat_run + 1
    return greenup


def _winter_wheat_southern(gdd: np.ndarray, out: Transitions) -> int:
    """Greenup is the day after the coldest ``MOVING_WINDOW_SIZE``-day window."""
    smoothed = moving_average(gdd, MOVING_WINDOW_SIZE)
    if not np.isfinite(smoothed).any():
        out.note("winter_wheat_S: GDD all NaN; derivative greenup kept")
        return -1
    greenup = int(np.nanargmin(smoothed)) + MOVING_WINDOW_SIZE
    out.note(f"winter_wheat_S: greenup set to coldest-window end {greenup}")
    return greenup


def _enforce_gdd_after_planting(
    greenup: int, plant: int, gdd: np.ndarray, out: Transitions, *, fix_offset: bool
) -> int:
    """Greenup must follow planting by at least :data:`MIN_GDD_AFTER_PLANTING`.

    The original applies this only when ``greenup >= plant`` -- it computes the
    accumulation for the cross-year case and then discards it -- and it adds the
    day offset to ``greenup`` rather than to ``plant``, overshooting by roughly
    ``greenup - plant``. Both quirks are reproduced by default;
    ``fix_offset=True`` anchors the offset to the planting date instead, which
    is what the comment in the source says it intends.
    """
    arr = np.asarray(gdd, dtype=float)
    if greenup < plant:
        out.note("gdd100: greenup precedes planting (cross-year); rule not applied")
        return greenup

    accumulated = np.nansum(arr[plant:greenup])
    if accumulated >= MIN_GDD_AFTER_PLANTING:
        return greenup

    running = np.nancumsum(arr[plant : circular.N_DOY])
    offset = int(running.searchsorted(MIN_GDD_AFTER_PLANTING))
    if offset >= running.size:
        out.note(
            f"gdd100: only {accumulated:.0f} GDD available after planting; greenup kept"
        )
        return greenup

    if fix_offset:
        moved = plant + offset
        out.note(f"gdd100: greenup moved to {moved} ({offset} d after planting)")
    else:
        moved = greenup + offset
        if moved >= circular.N_DOY:
            moved = offset - (circular.N_DOY - greenup)
        out.note(f"gdd100: greenup moved {offset} d to {moved} (legacy offset)")
    return int(moved)


def _clamp_season_gdd(
    greenup: int,
    greendown: int,
    gdd: np.ndarray,
    params: naming.CropParams,
    tropical: bool,
    out: Transitions,
) -> int:
    """Force accumulated GDD between the transitions into the crop's range.

    The maximum is applied first and the minimum re-evaluated against the
    possibly-already-moved date, as in the original -- the order matters.
    """
    scale = 1.0 if tropical else naming.EXTRATROPICAL_GDD_SCALE
    upper, lower = params.max_gdd * scale, params.min_gdd * scale

    total = circular.sum_between(gdd, greenup, greendown)
    if total > upper:
        moved = circular.find_doy_for_gdd(gdd, greenup, upper)
        if moved is None:
            out.note(f"gdd_max: {upper:.0f} GDD never reached; greendown kept")
        else:
            out.note(f"gdd_max: greendown {greendown} -> {moved} ({total:.0f} > {upper:.0f})")
            greendown = moved

    total = circular.sum_between(gdd, greenup, greendown)
    if total < lower:
        moved = circular.find_doy_for_gdd(gdd, greenup, lower)
        if moved is None:
            # The original returned day 0 here, producing a ~365-day delta that
            # looked like a measurement rather than a failure.
            out.note(f"gdd_min: {lower:.0f} GDD never reached; greendown kept")
        else:
            out.note(f"gdd_min: greendown {greendown} -> {moved} ({total:.0f} < {lower:.0f})")
            greendown = moved

    return greendown


def rs_transitions(
    curve_values: np.ndarray,
    gdd: np.ndarray,
    *,
    plant: int,
    crop: str,
    params: naming.CropParams,
    climate_zone: str,
    hemisphere: str,
    fix_gdd100_offset: bool = False,
) -> Transitions:
    """Mid-greenup and mid-greendown for one region.

    Args:
        curve_values: the season-masked fitted NDVI curve, 366 long.
        gdd: daily growing degree days, 366 long (not accumulated).
        plant: the GEOGLAM planting day.
        crop: crop slug, e.g. ``"winter_wheat"``.
        params: thermal parameters from :mod:`geocif.cropcal.naming`.
        climate_zone: ``"Tropical"`` or ``"Temperate"``.
        hemisphere: ``"N"`` or ``"S"``.
        fix_gdd100_offset: anchor the 100-GDD offset to the planting date rather
            than reproducing the original's overshoot.

    Raises:
        TransitionError: the masked curve has no finite values.
    """
    greenup, greendown = _derivative_transitions(curve_values)
    out = Transitions(midgreenup=greenup, midgreendown=greendown)

    is_winter_wheat = crop == "winter_wheat"
    temperate = climate_zone == "Temperate"
    tropical = climate_zone == "Tropical"

    if is_winter_wheat and temperate:
        if hemisphere == "N":
            greenup = _winter_wheat_northern(greenup, curve_values, gdd, out)
        else:
            southern = _winter_wheat_southern(gdd, out)
            if southern >= 0:
                greenup = southern
    elif not is_winter_wheat:
        greenup = _enforce_gdd_after_planting(
            greenup, int(plant), gdd, out, fix_offset=fix_gdd100_offset
        )

    greendown = _clamp_season_gdd(greenup, greendown, gdd, params, tropical, out)

    out.midgreenup = int(greenup) % circular.N_DOY
    out.midgreendown = int(greendown) % circular.N_DOY
    return out
