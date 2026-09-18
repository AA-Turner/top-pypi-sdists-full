# -*- coding: utf-8 -*-
"""Fit a smooth phenology curve, find its peaks, and clip it to the season.

Three steps, in order:

1. :func:`fit_fourier` -- an 8-harmonic Fourier series least-squares fitted to
   the per-day median NDVI.
2. :func:`detect_peaks_valleys` -- local maxima at least ``mph`` of the series
   maximum and at least ``mpd`` days apart, plus the minima between them.
3. :func:`mask_to_season` -- flatten competing peaks that belong to a different
   crop cycle, then NaN everything outside the GEOGLAM planting-to-harvest
   window, so the derivative in :mod:`geocif.cropcal.transitions` only ever sees
   the season being validated.

A note on the fit, because the original's docstring is wrong about it:
``model_fourier`` took an ``agdd`` argument but used only ``len(agdd)``, building
``t = 1..N`` and fitting harmonics in **day-index space**. It was never a
thermal-time fit. That behaviour is kept -- every published number depends on it
-- but the signature here is honest and takes no GDD at all.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, Sequence

import numpy as np
from scipy.optimize import leastsq
from scipy.signal import find_peaks

from geocif.cropcal import circular

logger = logging.getLogger(__name__)

#: Harmonics in the Fourier fit. 1 + 4*n_harm free parameters.
N_HARMONICS = 8

#: Initial value for every fitted parameter, as in the original.
INIT_PARAM = 0.5

#: Minimum peak separation, in days.
MIN_PEAK_DISTANCE = 45

#: Minimum peak height as a fraction of the series maximum. Winter wheat has a
#: much flatter, double-humped profile, so it needs a far lower bar.
MPH_FRACTION_DEFAULT = 0.5
MPH_FRACTION_WINTER_WHEAT = 0.1

#: More peaks than this and the signal is judged too noisy to validate.
MAX_PEAKS = 5


# --------------------------------------------------------------------------
# Fourier fit
# --------------------------------------------------------------------------
def fourier_series(params: Sequence[float], n_points: int, n_harm: int) -> np.ndarray:
    """Evaluate the harmonic model on ``t = 1..n_points``.

    Parameter layout, inherited: ``params[0]`` is the mean, then each harmonic
    takes four values -- cosine amplitude, cosine phase, sine amplitude, sine
    phase.
    """
    t = np.arange(1, n_points + 1, dtype=float)
    out = np.full(n_points, float(params[0]))
    w = 1
    for i in range(1, n_harm * 4, 4):
        angle = 2.0 * np.pi * w * t / n_points
        out = (
            out
            + params[i] * np.cos(angle + params[i + 1])
            + params[i + 2] * np.sin(angle + params[i + 3])
        )
        w += 1
    return out


def fit_fourier(series: np.ndarray, n_harm: int = N_HARMONICS) -> np.ndarray:
    """Least-squares fit of a Fourier series to ``series``.

    NaN days are excluded from the residual rather than propagated. The original
    fed the raw median straight in and relied on there being none, which held
    for its AMIS regions but not for sparse EW ones: a single NaN makes every
    residual NaN, ``leastsq`` gives up on the first iteration, and the returned
    curve is the flat all-``0.5`` starting vector -- a silent wrong answer, not
    an error.
    """
    values = np.asarray(series, dtype=float)
    n_points = values.size
    finite = np.isfinite(values)
    n_params = 1 + n_harm * 4
    if finite.sum() < n_params:
        raise ValueError(
            f"only {int(finite.sum())} finite points for a {n_params}-parameter fit"
        )

    def residual(params):
        return values[finite] - fourier_series(params, n_points, n_harm)[finite]

    init = [INIT_PARAM] * n_params
    solution, _flag = leastsq(residual, init, maxfev=1_000_000)
    return fourier_series(solution, n_points, n_harm)


# --------------------------------------------------------------------------
# Peaks and valleys
# --------------------------------------------------------------------------
def mph_fraction_for(crop: str) -> float:
    """Minimum-peak-height fraction for a crop."""
    return MPH_FRACTION_WINTER_WHEAT if crop == "winter_wheat" else MPH_FRACTION_DEFAULT


def detect_peaks_valleys(
    fitted: np.ndarray,
    mph_fraction: float = MPH_FRACTION_DEFAULT,
    mpd: int = MIN_PEAK_DISTANCE,
) -> tuple[np.ndarray, np.ndarray]:
    """``(peaks, valleys)`` as day indices into ``fitted``.

    ``scipy.signal.find_peaks`` replaces the vendored ``detect_peaks``. Two
    details are matched deliberately:

    * the original's ``mpd`` suppressed peaks within ``+/- mpd`` **inclusive**,
      so the true minimum separation was ``mpd + 1``; scipy's ``distance``
      enforces a separation of at least ``distance``, hence ``mpd + 1`` here;
    * valleys were detected with **no** height filter at all, only the distance
      one, so that asymmetry is kept.

    Neither can return the first or last sample, matching the original.
    """
    values = np.asarray(fitted, dtype=float)
    peak_floor = mph_fraction * np.nanmax(values)
    peaks, _ = find_peaks(values, height=peak_floor, distance=mpd + 1)
    valleys, _ = find_peaks(-values, distance=mpd + 1)
    return peaks, valleys


def select_peak(
    fitted: np.ndarray,
    peaks: Sequence[int],
    window: tuple[float, float],
    *,
    circular_distance: bool = True,
) -> Optional[int]:
    """The peak this season is about: the highest one inside the GEOGLAM window,
    or, if none is inside, the one closest to it.

    Returns ``None`` only when ``peaks`` is empty.
    """
    peaks = list(peaks)
    if not peaks:
        return None
    start, end = window

    inside = [p for p in peaks if circular.check_between(p, start, end)]
    if inside:
        return int(max(inside, key=lambda p: fitted[p]))

    distances = [
        circular.dist_from_window(p, start, end, circular=circular_distance)[1]
        for p in peaks
    ]
    return int(peaks[int(np.argmin(distances))])


def bracketing_valleys(
    peak: int, valleys: Sequence[int], n_points: int
) -> tuple[int, int]:
    """The valleys immediately before and after ``peak``.

    Falls back to the series endpoints when the peak has no valley on that side,
    as the original did.
    """
    valleys = np.asarray(sorted(valleys), dtype=int)
    before = valleys[valleys < peak]
    after = valleys[valleys > peak]
    lo = int(before.max()) if before.size else 0
    hi = int(after.min()) if after.size else n_points - 1
    return lo, hi


def all_peaks_in_window(peaks: Sequence[int], window: tuple[float, float]) -> bool:
    """Does every detected peak fall inside the GEOGLAM season?

    When it does there is nothing competing, and the curve is left alone.
    """
    start, end = window
    return all(circular.check_between(p, start, end) for p in peaks)


# --------------------------------------------------------------------------
# Season masking
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class MaskedCurve:
    """The curve the transition rules actually see."""

    values: np.ndarray
    selected_peak: Optional[int]
    depeaked: bool
    n_peaks: int


def mask_to_season(
    fitted: np.ndarray,
    peaks: Sequence[int],
    valleys: Sequence[int],
    *,
    midgreenup: float,
    midgreendown: float,
    plant: float,
    harvest: float,
    legacy_wrap_gate: bool = False,
    circular_distance: bool = True,
) -> MaskedCurve:
    """Flatten competing peaks, then clip to the planting-to-harvest window.

    De-peaking runs only when there is more than one peak and at least one sits
    outside the GEOGLAM season; otherwise the curve already describes the right
    cycle and is passed through untouched.

    ``legacy_wrap_gate=True`` restores the original's behaviour of skipping
    de-peaking entirely whenever ``midgreenup >= midgreendown`` -- that is, for
    every season crossing 1 January. The gate was invisible on the AMIS regions
    the method was tested against and is badly wrong here, where most regions
    are EW and many are southern-hemisphere wrap seasons. The default fixes it
    by doing the masking circularly.
    """
    values = np.asarray(fitted, dtype=float).copy()
    n = values.size
    window = (midgreenup, midgreendown)
    peaks = list(peaks)

    wrap_blocked = legacy_wrap_gate and not (midgreenup < midgreendown)
    depeak = len(peaks) > 1 and not wrap_blocked and not all_peaks_in_window(peaks, window)

    selected = None
    if depeak:
        selected = select_peak(values, peaks, window, circular_distance=circular_distance)
        lo, hi = bracketing_valleys(selected, valleys, n)

        peak_between = circular.check_between(selected, lo, hi)
        lo_in_season = circular.check_between(lo, midgreenup, midgreendown)
        hi_in_season = circular.check_between(hi, midgreenup, midgreendown)

        if not peak_between and not lo_in_season and not hi_in_season:
            # The bracketing pair belongs to a different cycle entirely: erase
            # the span between the two valleys and bridge across it.
            values[circular.circular_mask(n, lo, hi)] = np.nan
        else:
            # Keep only the cycle around the selected peak.
            values[~circular.circular_mask(n, lo, hi)] = np.nan

        wraps = lo > hi
        if not wraps:
            # Endpoint restoration, verbatim: np.interp cannot extrapolate, so
            # without this a leading or trailing NaN run is filled with a flat
            # copy of the nearest finite value instead of a slope.
            if np.isnan(values[0]):
                values[0] = min(fitted[0], fitted[lo])
            if np.isnan(values[n - 1]):
                values[n - 1] = min(fitted[n - 1], fitted[hi])
        values = circular.interp_nan(values, circular=wraps)

    values[~circular.circular_mask(n, int(plant), int(harvest))] = np.nan

    return MaskedCurve(
        values=values,
        selected_peak=selected,
        depeaked=bool(depeak),
        n_peaks=len(peaks),
    )
