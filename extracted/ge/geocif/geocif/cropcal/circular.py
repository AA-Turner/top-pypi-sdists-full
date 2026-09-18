# -*- coding: utf-8 -*-
"""Day-of-year arithmetic on a circle.

Every wrap-around test, distance and sum in this package goes through here.
The original GEOGLAM code spread the same ideas across ``util_cal.py`` and
ended up defining ``check_between`` **twice**, at lines 57 and 662, with
different return types (an integer width vs. a boolean); the later definition
silently shadowed the earlier one at import. Keeping the arithmetic in one
module is the reason that cannot happen here.

Convention, inherited from the source so the numbers stay comparable: the
year is treated as **365** days for wrap tests and differences, while the
series themselves are 366 long (index 0..365). See ``DEVIATIONS.md``.
"""
from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

#: Period used for every wrap test and circular difference.
DAYS_IN_YEAR = 365

#: Length of the day-of-year series this package works with (index 0..365).
N_DOY = 366


def check_between(value: float, start: float, end: float) -> bool:
    """Is ``value`` inside the circular window ``[start, end]``, inclusive?

    When ``start <= end`` the window is an ordinary interval. When
    ``start > end`` the window wraps 1 January, and membership means
    ``value >= start or value <= end``.

    This is the live definition from ``util_cal.py:662`` -- the boolean one
    that every caller actually expected.
    """
    if start <= end:
        return bool(start <= value <= end)
    return bool(value >= start or value <= end)


def dist_from_window(
    doy: float, start: float, end: float, *, circular: bool = True
) -> tuple[bool, float]:
    """``(is_inside, distance)`` for a day relative to a circular window.

    ``distance`` is meaningful only when ``is_inside`` is False: it is how far
    the day sits outside the window, used to pick the least-bad peak when no
    peak falls inside the GEOGLAM season.

    ``circular=True`` (the default) measures that gap the short way round, so a
    day just past 31 December is close to a window opening in early January.
    The original measured ``abs(doy - start) + abs(doy - end)`` on a straight
    line, which scores such a day as maximally distant -- harmless for the
    northern-hemisphere AMIS regions it was tested on, actively wrong for the
    wrap-season EW regions that now make up most of the population. Pass
    ``circular=False`` to reproduce the original for a reference comparison.
    """
    inside = check_between(doy, start, end)
    if inside:
        # The original returns the window width here. Nothing consumes the
        # distance when the day is inside, so the value is arbitrary; keeping
        # it makes a side-by-side diff against the source trivial.
        return True, float(abs(start - end))

    if not circular:
        return False, float(abs(doy - start) + abs(doy - end))

    return False, float(min(circular_gap(doy, start), circular_gap(doy, end)))


def circular_gap(a: float, b: float, period: float = DAYS_IN_YEAR) -> float:
    """Unsigned distance between two days, the short way round. In ``[0, P/2]``."""
    gap = abs(a - b) % period
    return float(min(gap, period - gap))


def signed_difference(a: float, b: float, period: int = DAYS_IN_YEAR) -> float:
    """Signed circular ``a - b``, wrapped into ``(-P/2, P/2]``.

    Positive means ``a`` is later than ``b``. Unlike :func:`legacy_difference`
    this is a true signed quantity, so it can be averaged, mapped or used for a
    bias statistic.
    """
    if not np.isfinite(a) or not np.isfinite(b):
        return float("nan")
    half = period // 2
    return float(((a - b + half) % period) - half)


def legacy_difference(a: float, b: float) -> float:
    """The original ``util_cal.diff_GEOGLAM_RS``, reproduced exactly.

    ``a`` is the GEOGLAM day, ``b`` the remote-sensing day::

        |a - b| > 180  ->  365 - max(a, b) + min(a, b)     # always >= 0
        otherwise      ->  a - b                            # signed

    The wrap branch discards the sign, so roughly half the population is forced
    positive and the column cannot be used for bias analysis. It is kept
    because every published figure and threshold is expressed in it; use
    :func:`signed_difference` for anything that needs a real sign.
    """
    if not np.isfinite(a) or not np.isfinite(b):
        return float("nan")
    if abs(a - b) > 180:
        return float(DAYS_IN_YEAR - max(a, b) + min(a, b))
    return float(a - b)


def sum_between(values: Sequence[float], start: int, end: int) -> float:
    """Sum ``values`` over the circular window ``[start, end]``, both inclusive.

    NaNs are ignored. Mirrors ``util_cal.sum_between``, including its
    inclusivity on both ends and its use of index 365 as the wrap point.
    """
    arr = np.asarray(values, dtype=float)
    if not np.isfinite(start) or not np.isfinite(end):
        return float("nan")
    start, end = int(start), int(end)
    if start <= end:
        return float(np.nansum(arr[start : end + 1]))
    return float(np.nansum(arr[start : DAYS_IN_YEAR + 1]) + np.nansum(arr[0 : end + 1]))


def find_doy_for_gdd(
    gdd: Sequence[float], start: int, target: float
) -> Optional[int]:
    """First day, walking forward from ``start``, at which accumulated GDD
    reaches ``target``.

    Returns ``None`` when the target is never reached in a full circuit.

    The original returned ``0`` in that case (``doy_at_peak_gdd`` was
    initialised to 0 and only overwritten inside the ``break``), so a region too
    cold to accumulate its crop's minimum GDD silently had its mid-greendown
    set to day 0 and reported a delta of roughly +/-365 -- a hard failure
    dressed up as a measurement. Returning ``None`` lets the caller leave the
    date alone and record why.

    The traversal order is inherited verbatim: ``np.roll(np.arange(1, 366),
    -start)`` visits ``start+1 ... 365, 1 ... start``, so day 0 is never
    examined and accumulation begins the day *after* ``start``.
    """
    arr = np.asarray(gdd, dtype=float)
    if not np.isfinite(start) or not np.isfinite(target):
        return None

    order = np.roll(np.arange(1, DAYS_IN_YEAR + 1), -int(start))
    running = 0.0
    for doy in order:
        value = arr[doy]
        if np.isfinite(value):
            running += value
        if running >= target:
            return int(doy)
    return None


def circular_mask(length: int, start: int, end: int) -> np.ndarray:
    """Boolean mask over ``range(length)``, True inside the circular window.

    ``[start, end]`` inclusive on both ends; when ``start > end`` the window
    wraps the end of the array. This is what lets the season masking in
    :mod:`geocif.cropcal.curve` treat wrap-around seasons the same way as
    contained ones -- the original used bare slices, which silently produced an
    inverted mask for any season crossing 1 January.
    """
    idx = np.arange(length)
    if start <= end:
        return (idx >= start) & (idx <= end)
    return (idx >= start) | (idx <= end)


def interp_nan(values: np.ndarray, *, circular: bool = False) -> np.ndarray:
    """Fill NaNs by linear interpolation, optionally wrapping the year.

    ``circular=False`` reproduces the original: ``np.interp`` does not
    extrapolate, so leading and trailing NaNs are filled with the first and last
    finite value. ``circular=True`` treats the series as a loop, so a gap
    spanning 31 December is interpolated across the year boundary rather than
    flattened to a constant.
    """
    arr = np.asarray(values, dtype=float).copy()
    nans = np.isnan(arr)
    if not nans.any() or nans.all():
        return arr

    positions = np.flatnonzero(~nans)
    if not circular:
        arr[nans] = np.interp(np.flatnonzero(nans), positions, arr[positions])
        return arr

    # Tile one period either side so np.interp sees the wrap as ordinary
    # interior, then read the middle period back out.
    n = arr.size
    xp = np.concatenate([positions - n, positions, positions + n])
    fp = np.tile(arr[positions], 3)
    arr[nans] = np.interp(np.flatnonzero(nans), xp, fp)
    return arr
