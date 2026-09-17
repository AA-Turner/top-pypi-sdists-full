"""Pure-numpy season onset / cessation / length algorithms (DESIGN.md section 3).

Conventions shared by every function in this module
----------------------------------------------------
* Arrays are **cubes with time on axis 0**: ``pr[T, ...]``. Everything after
  axis 0 is the *pixel shape* and is arbitrary: ``()`` for a single pixel,
  ``(N,)`` for a list of pixels, ``(rows, cols)`` for a raster window. All
  functions reshape to ``(T, N)`` internally and restore the pixel shape.
* Per-pixel scalars (``search_start``, ``season_end``, ``search_end``,
  ``onset_idx``) are Python ints/floats or arrays broadcastable to the pixel
  shape.
* Time indices are **integer positions along axis 0** (0-based); the caller
  converts to dates. A NaN index means "none".
* Rain and PET are in **mm/day**. NaN rain contributes 0 mm to sums and is
  *not* a dry day (it breaks a dry run). NaN PET is treated as 0 mm/day.
* Outputs are float32 with NaN, int8 status codes (nodata -1), int16 counts,
  or bool flags.
* No I/O, no icclim, no pygmt. Only numpy.

Vectorisation: every step is one array operation over all pixels; the only
Python loop over time is the cessation bucket (a recurrence that cannot be
expressed as a prefix scan because of the daily floor *and* cap).

Memory: the onset pass materialises roughly ten ``(T, N)`` arrays, mostly
int32/bool with two float64 (about ``10 * 8 * T * N`` bytes worst case);
chunk large windows over pixels if that is a concern.
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Optional, Union

import numpy as np

logger = logging.getLogger(__name__)

#: Nodata value for every int8 status raster produced by this module.
NODATA_STATUS: int = -1

PixelScalar = Union[int, float, np.ndarray]


# ---------------------------------------------------------------------------
# 3.1 Parameters
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class OnsetParams:
    """Onset detector parameters (all rain quantities in mm, times in days)."""

    precip_threshold: float = 20.0  # mm in the accumulation window
    window_days: int = 3  # accumulation window length (days)
    dry_spell_days: int = 10  # consecutive dry days that invalidate a candidate
    dry_day_threshold: float = 1.0  # mm; a day strictly below this is dry
    validation_days: int = 30  # look-ahead after a candidate (days)


@dataclass(frozen=True)
class CessationParams:
    """Cessation (running bucket) parameters (mm and days)."""

    soil_whc: float = 100.0  # mm root-zone water holding capacity (hard cap)
    min_season_days: int = 60  # earliest cessation, counted from onset (days)
    empty_persist_days: int = 5  # consecutive days at S == 0 to call cessation
    initial_storage: float = 0.0  # mm in the bucket the day before onset


# ---------------------------------------------------------------------------
# 3.2 Status codes
# ---------------------------------------------------------------------------
class OnsetStatus(IntEnum):
    """Per-pixel outcome of :func:`onset_index` (int8 raster, nodata -1)."""

    OK = 0
    NO_TRIGGER = 1
    INSUFFICIENT_DATA = 2
    NO_DATA = 3


class CessationStatus(IntEnum):
    """Per-pixel outcome of :func:`cessation_index` (int8 raster, nodata -1)."""

    OK = 0
    NO_ONSET = 1
    RIGHT_CENSORED = 2
    NO_RANGE = 3


class SeasonState(IntEnum):
    """Current-season monitor state of :func:`onset_state` (int8, nodata -1)."""

    BEFORE_WINDOW = 0  # search has not opened at as-of date
    NOT_STARTED = 1  # search open, no candidate yet
    FALSE_START = 2  # candidate(s) seen, all invalidated, none pending
    PROVISIONAL = 3  # latest candidate still inside its validation window
    CONFIRMED = 4  # a candidate survived validation -> onset established
    NO_ONSET = 5  # season end passed (+validation) without onset


# ---------------------------------------------------------------------------
# 3.9 Reference 1-D implementations (test oracle; kept verbatim from the
#     prototype script, only renamed). Not vectorised, not for production.
# ---------------------------------------------------------------------------
def _onset_index_1d(
    pr,
    season_end_idx,
    precip_threshold,
    window_days,
    dry_spell_days,
    dry_day_threshold,
    validation_days,
    search_start_idx=0,
    **_,
):
    """Spec section 4 onset for ONE pixel; returns ``(index or NaN, status str)``.

    Status strings: ``"ok"``, ``"insufficient_data"`` (a candidate exists but
    lacks a full look-ahead), ``"no_trigger"``, ``"no_data"`` (empty series).
    ``search_start_idx`` is the first index (inclusive) a candidate may fall on;
    it defaults to 0, which reproduces the prototype verbatim.

    Units: ``pr`` mm/day, ``precip_threshold`` mm, every ``*_days`` in days,
    every ``*_idx`` an integer position along the single time axis.
    """
    p = np.asarray(pr, dtype="float64")
    n = p.size
    if n == 0:
        return np.nan, "no_data"
    filled = np.nan_to_num(p, nan=0.0)
    csum = np.concatenate(([0.0], np.cumsum(filled)))
    w = np.full(n, np.nan)
    if n >= window_days:
        idx = np.arange(window_days - 1, n)
        w[idx] = csum[idx + 1] - csum[idx + 1 - window_days]
    dry = (filled < dry_day_threshold) & ~np.isnan(p)
    r = np.zeros(n, dtype="int64")
    run = 0
    for t in range(n):
        run = run + 1 if dry[t] else 0
        r[t] = run
    flag = (r >= dry_spell_days).astype("int64")
    fc = np.concatenate(([0], np.cumsum(flag)))
    t_ix = np.arange(n)
    lo = np.minimum(t_ix + dry_spell_days - 1, n)
    hi = np.minimum(t_ix + validation_days, n)
    has_spell = (fc[hi] - fc[lo]) > 0
    has_lookahead = (t_ix + validation_days) <= n
    base = (
        (t_ix >= window_days - 1)
        & (t_ix >= search_start_idx)
        & (t_ix <= season_end_idx)
        & (w >= precip_threshold)
        & ~has_spell
    )
    ok = base & has_lookahead
    hits = np.flatnonzero(ok)
    if hits.size:
        return float(hits[0]), "ok"
    # would a candidate have passed had the look-ahead existed?
    return np.nan, ("insufficient_data" if np.flatnonzero(base).size else "no_trigger")


def _cessation_index_1d(
    pr,
    pet,
    onset_idx,
    search_end_idx,
    soil_whc,
    min_season_days,
    empty_persist_days,
    initial_storage=0.0,
    **_,
):
    """Spec section 5 cessation for ONE pixel; returns ``(index or NaN, status str)``.

    Status strings: ``"ok"``, ``"no_onset"``, ``"no_range"``, ``"right_censored"``.
    ``initial_storage`` (mm) is the bucket level the day before onset and
    defaults to 0.0, which reproduces the prototype verbatim.

    Units: ``pr``/``pet`` mm/day, ``soil_whc``/``initial_storage`` mm, days for
    the rest, ``*_idx`` integer positions along the single time axis.
    """
    if not np.isfinite(onset_idx):
        return np.nan, "no_onset"
    o = int(onset_idx)
    p = np.nan_to_num(np.asarray(pr, dtype="float64"), nan=0.0)
    e = np.nan_to_num(np.asarray(pet, dtype="float64"), nan=0.0)
    end = min(int(search_end_idx), p.size - 1)
    if end <= o:
        return np.nan, "no_range"
    s = float(initial_storage)
    empty_run = 0
    first_allowed = o + min_season_days
    for t in range(o, end + 1):
        s = min(max(s + p[t] - e[t], 0.0), soil_whc)
        empty_run = empty_run + 1 if s <= 0.0 else 0
        if t >= first_allowed and empty_run >= empty_persist_days:
            return float(t - empty_persist_days + 1), "ok"
    return np.nan, "right_censored"


# ---------------------------------------------------------------------------
# Shape helpers
# ---------------------------------------------------------------------------
def _to_cube(arr: Any, name: str) -> tuple[np.ndarray, tuple[int, ...], int, int]:
    """Return ``(a2d float64 (T, N), pixel_shape, T, N)`` for a time-first cube.

    A 1-D input ``(T,)`` is a single pixel: pixel shape ``()``, ``N = 1``.
    """
    a = np.asarray(arr, dtype="float64")
    if a.ndim == 0:
        raise ValueError(f"{name} must have time on axis 0, got a 0-d array")
    n_time = int(a.shape[0])
    pixel_shape = tuple(int(s) for s in a.shape[1:])
    n_pix = int(np.prod(pixel_shape, dtype="int64")) if pixel_shape else 1
    return a.reshape(n_time, n_pix), pixel_shape, n_time, n_pix


def _pixel_param(value: PixelScalar, pixel_shape: tuple[int, ...], name: str) -> np.ndarray:
    """Broadcast a per-pixel scalar (int/float or array) to ``(N,)`` float64."""
    v = np.asarray(value, dtype="float64")
    try:
        v = np.broadcast_to(v, pixel_shape)
    except ValueError as exc:
        raise ValueError(
            f"{name} with shape {v.shape} is not broadcastable to pixel shape {pixel_shape}"
        ) from exc
    return np.array(v, dtype="float64").reshape(-1)


def _rolling_sum(filled: np.ndarray, window_days: int) -> np.ndarray:
    """Trailing sum over ``window_days`` along axis 0; NaN where the window is partial.

    ``filled`` is ``(T, N)`` with NaN already replaced by 0.
    """
    n_time, n_pix = filled.shape
    csum = np.zeros((n_time + 1, n_pix), dtype="float64")
    np.cumsum(filled, axis=0, out=csum[1:])
    w = np.full((n_time, n_pix), np.nan, dtype="float64")
    if n_time >= window_days:
        w[window_days - 1 :] = csum[window_days:] - csum[: n_time + 1 - window_days]
    return w


def _dry_run(dry: np.ndarray) -> np.ndarray:
    """Consecutive-dry-day counter ``r[t]`` (int32, ``(T, N)``), reset to 0 on a wet/NaN day.

    ``r[t] = t - (index of the last non-dry day <= t)``, with -1 when none, so
    a run open since the start counts ``t + 1`` days. One prefix scan, no loop.
    """
    n_time, n_pix = dry.shape
    t_ix = np.arange(n_time, dtype="int32")[:, None]
    last_wet = np.where(dry, np.int32(-1), t_ix)
    np.maximum.accumulate(last_wet, axis=0, out=last_wet)
    return (t_ix - last_wet).astype("int32", copy=False)


def _spell_lookahead(flag: np.ndarray, dry_spell_days: int, validation_days: int) -> np.ndarray:
    """``has_spell[t] = any(flag[t + dry_spell_days - 1 .. t + validation_days - 1])``.

    ``flag[s]`` marks a qualifying dry spell ENDING at ``s``. The window is
    clipped to the array; an empty window gives False. Exact via a prefix sum.
    """
    n_time = flag.shape[0]
    fc = np.zeros((n_time + 1, flag.shape[1]), dtype="int32")
    np.cumsum(flag, axis=0, dtype="int32", out=fc[1:])
    t_ix = np.arange(n_time)
    lo = np.minimum(t_ix + dry_spell_days - 1, n_time)
    hi = np.minimum(t_ix + validation_days, n_time)
    return (fc[hi] - fc[lo]) > 0


def _first_true(mask: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """``(found (N,) bool, first index (N,) int64)`` of the first True along axis 0."""
    if mask.shape[0] == 0:
        n_pix = mask.shape[1]
        return np.zeros(n_pix, dtype=bool), np.zeros(n_pix, dtype="int64")
    found = mask.any(axis=0)
    first = np.argmax(mask, axis=0).astype("int64")
    return found, first


def _last_true(mask: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """``(found (N,) bool, last index (N,) int64)`` of the last True along axis 0."""
    n_time = mask.shape[0]
    if n_time == 0:
        n_pix = mask.shape[1]
        return np.zeros(n_pix, dtype=bool), np.zeros(n_pix, dtype="int64")
    found = mask.any(axis=0)
    last = n_time - 1 - np.argmax(mask[::-1], axis=0).astype("int64")
    return found, last


def _episode_ends(trigger: np.ndarray) -> np.ndarray:
    """True on the last day of each run of consecutive trigger days (``trigger[T] := False``)."""
    nxt = np.zeros_like(trigger)
    if trigger.shape[0] > 1:
        nxt[:-1] = trigger[1:]
    return trigger & ~nxt


def _in_window(
    n_time: int, search_start: np.ndarray, season_end: np.ndarray, window_days: int
) -> np.ndarray:
    """Bool ``(T, N)``: ``t >= window_days-1 and search_start <= t <= season_end``.

    Non-finite bounds compare False, so such pixels have no window at all.
    """
    t_ix = np.arange(n_time, dtype="float64")[:, None]
    lower = np.maximum(search_start, float(window_days - 1))[None, :]
    return (t_ix >= lower) & (t_ix <= season_end[None, :])


def _onset_components(p2d: np.ndarray, params: OnsetParams) -> dict:
    """Shared onset arrays for a ``(T, N)`` float64 rain slab (spec section 4 symbols)."""
    filled = np.nan_to_num(p2d, nan=0.0)
    isnan = np.isnan(p2d)
    w = _rolling_sum(filled, params.window_days)
    dry = (filled < params.dry_day_threshold) & ~isnan
    r = _dry_run(dry)
    flag = r >= params.dry_spell_days
    has_spell = _spell_lookahead(flag, params.dry_spell_days, params.validation_days)
    n_time = p2d.shape[0]
    has_lookahead = (np.arange(n_time) + params.validation_days) <= n_time
    return {
        "filled": filled,
        "W": w,
        "dry": dry,
        "r": r,
        "flag": flag,
        "has_spell": has_spell,
        "has_lookahead": has_lookahead,
        "allnan": isnan.all(axis=0) if n_time else np.ones(p2d.shape[1], dtype=bool),
    }


def _onset_2d(
    p2d: np.ndarray, search_start: np.ndarray, season_end: np.ndarray, params: OnsetParams
) -> dict:
    """Vectorised onset on ``(T, N)``; returns onset/status plus the trigger mask."""
    n_time = p2d.shape[0]
    comp = _onset_components(p2d, params)
    in_win = _in_window(n_time, search_start, season_end, params.window_days)
    trigger = in_win & (comp["W"] >= params.precip_threshold)
    base = trigger & ~comp["has_spell"]
    ok = base & comp["has_lookahead"][:, None]
    found, first = _first_true(ok)
    onset = np.where(found, first, np.nan).astype("float32")
    status = np.full(p2d.shape[1], int(OnsetStatus.NO_TRIGGER), dtype="int8")
    status[base.any(axis=0) & ~found] = int(OnsetStatus.INSUFFICIENT_DATA)
    status[found] = int(OnsetStatus.OK)
    nodata = comp["allnan"] | ~np.isfinite(search_start) | ~np.isfinite(season_end)
    status[nodata] = int(OnsetStatus.NO_DATA)
    onset[nodata] = np.nan
    return {
        "onset": onset,
        "status": status,
        "trigger": trigger,
        "found": found,
        "nodata": nodata,
        "comp": comp,
    }


# ---------------------------------------------------------------------------
# 3.3 Onset
# ---------------------------------------------------------------------------
def onset_index(
    pr: np.ndarray,
    search_start: PixelScalar,
    season_end: PixelScalar,
    params: OnsetParams = OnsetParams(),
) -> tuple[np.ndarray, np.ndarray]:
    """Season onset index per pixel (spec section 4, corrected).

    Parameters
    ----------
    pr : ``(T, ...)`` daily rain, mm/day, NaN = missing (counts 0 mm, breaks dry runs).
    search_start, season_end : first / last index (inclusive) a candidate may
        fall on; int or array broadcastable to the pixel shape.
    params : :class:`OnsetParams`.

    Returns
    -------
    onset_idx : float32, pixel shape, NaN where none. Index along axis 0 of
        the first ``t`` with ``t >= window_days-1``, ``search_start <= t <=
        season_end``, ``t + validation_days <= T``, ``W[t] >= precip_threshold``
        and no qualifying dry spell ending in ``[t+dry_spell_days-1,
        t+validation_days-1]``.
    status : int8 :class:`OnsetStatus`. ``INSUFFICIENT_DATA`` when a candidate
        passed every test except the full look-ahead; ``NO_TRIGGER`` otherwise;
        ``NO_DATA`` when the pixel's rain is all-NaN or a season bound is
        non-finite.
    """
    p2d, pixel_shape, _, _ = _to_cube(pr, "pr")
    ss = _pixel_param(search_start, pixel_shape, "search_start")
    se = _pixel_param(season_end, pixel_shape, "season_end")
    res = _onset_2d(p2d, ss, se, params)
    return res["onset"].reshape(pixel_shape), res["status"].reshape(pixel_shape)


# ---------------------------------------------------------------------------
# 3.4 Cessation
# ---------------------------------------------------------------------------
def cessation_index(
    pr: np.ndarray,
    pet: np.ndarray,
    onset_idx: PixelScalar,
    search_end: PixelScalar,
    params: CessationParams = CessationParams(),
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Season cessation index per pixel from a capped running bucket (spec section 5).

    Parameters
    ----------
    pr, pet : ``(T, ...)`` daily rain and PET, mm/day; NaN -> 0 in both (the
        caller logs NaN PET counts).
    onset_idx : per-pixel onset index (float, NaN = no onset), int or array.
    search_end : last index (inclusive) scanned, clipped to ``T-1``; NaN -> ``T-1``.
    params : :class:`CessationParams`.

    Returns
    -------
    cessation_idx : float32, NaN where none. ``S`` starts at
        ``initial_storage`` the day before onset; for ``t`` in
        ``onset..search_end``: ``S = min(max(S + P - PET, 0), WHC)``; cessation
        = first day of the first run of ``empty_persist_days`` days with
        ``S <= 0`` whose last day is ``>= onset + min_season_days``.
    status : int8 :class:`CessationStatus`. ``NO_ONSET`` (onset NaN),
        ``NO_RANGE`` (``search_end <= onset``), ``RIGHT_CENSORED`` (bucket never
        emptied for long enough by ``search_end``), else ``OK``.
    eos_at_floor : bool, True where ``cessation == onset + min_season_days -
        empty_persist_days + 1`` (the minimum-season gate was binding).
    """
    p2d, pixel_shape, n_time, n_pix = _to_cube(pr, "pr")
    e2d, pet_shape, _, _ = _to_cube(pet, "pet")
    if e2d.shape != p2d.shape or pet_shape != pixel_shape:
        raise ValueError(f"pet shape {(e2d.shape[0],) + pet_shape} != pr shape {(n_time,) + pixel_shape}")
    p2d = np.nan_to_num(p2d, nan=0.0)
    e2d = np.nan_to_num(e2d, nan=0.0)
    onset = _pixel_param(onset_idx, pixel_shape, "onset_idx")
    end_f = _pixel_param(search_end, pixel_shape, "search_end")
    end_f = np.where(np.isfinite(end_f), end_f, float(n_time - 1))
    end = np.minimum(np.floor(end_f), float(n_time - 1)).astype("int64")

    has_onset = np.isfinite(onset)
    o = np.where(has_onset, np.floor(onset), 0).astype("int64")
    no_range = has_onset & (end <= o)
    active_px = has_onset & ~no_range

    cess = np.full(n_pix, np.nan, dtype="float64")
    storage = np.full(n_pix, float(params.initial_storage), dtype="float64")
    empty_run = np.zeros(n_pix, dtype="int32")
    first_allowed = o + int(params.min_season_days)

    if active_px.any():
        t_start = int(o[active_px].min())
        t_stop = int(end[active_px].max())
        for t in range(t_start, t_stop + 1):
            # ``remaining`` is monotonically shrinking (``t <= end`` and "no
            # cessation yet" never become true again), so it is safe to stop on.
            # ``act`` is NOT monotone: a pixel whose onset is still in the
            # future is inactive now and active later, so skip, never break.
            remaining = active_px & (t <= end) & np.isnan(cess)
            if not remaining.any():
                break
            act = remaining & (t >= o)
            if not act.any():
                continue
            s_new = np.clip(storage + p2d[t] - e2d[t], 0.0, float(params.soil_whc))
            storage = np.where(act, s_new, storage)
            empty_run = np.where(act, np.where(storage <= 0.0, empty_run + 1, 0), empty_run)
            hit = act & (t >= first_allowed) & (empty_run >= params.empty_persist_days)
            cess = np.where(hit, float(t - params.empty_persist_days + 1), cess)

    status = np.full(n_pix, int(CessationStatus.RIGHT_CENSORED), dtype="int8")
    status[np.isfinite(cess)] = int(CessationStatus.OK)
    status[no_range] = int(CessationStatus.NO_RANGE)
    status[~has_onset] = int(CessationStatus.NO_ONSET)
    floor_idx = o + params.min_season_days - params.empty_persist_days + 1
    eos_at_floor = np.isfinite(cess) & (cess == floor_idx)
    return (
        cess.astype("float32").reshape(pixel_shape),
        status.reshape(pixel_shape),
        eos_at_floor.reshape(pixel_shape),
    )


# ---------------------------------------------------------------------------
# 3.5 PET
# ---------------------------------------------------------------------------
def _expand_time_axis(doy: np.ndarray, ndim: int) -> np.ndarray:
    """Reshape a ``(T,)`` vector to ``(T, 1, ..., 1)`` so it broadcasts over a cube."""
    if doy.ndim == 1 and ndim > 1:
        return doy.reshape((doy.shape[0],) + (1,) * (ndim - 1))
    return doy


def hargreaves_pet(
    tasmin: np.ndarray, tasmax: np.ndarray, doy: np.ndarray, lat_deg: PixelScalar
) -> np.ndarray:
    """FAO-56 Hargreaves reference ET, mm/day (verbatim from the prototype, broadcasting).

    Parameters
    ----------
    tasmin, tasmax : daily minimum / maximum air temperature, degC, ``(T, ...)``.
    doy : day of year (1..366) per time step, ``(T,)`` (auto-expanded to
        ``(T, 1, ...)``) or any shape broadcastable to ``tasmax``.
    lat_deg : latitude in decimal degrees, scalar or broadcastable to the
        pixel shape. A 1-D ``lat_deg`` with a 3-D ``(T, rows, cols)`` cube is
        taken as *per row* and reshaped to ``(rows, 1)``.

    ``ET0 = 0.0023 * 0.408 * Ra * (Tmean + 17.8) * sqrt(max(Tmax - Tmin, 0))``
    with ``Ra`` the extraterrestrial radiation (MJ m-2 day-1) from the FAO-56
    equations (21-24); 0.408 converts MJ m-2 day-1 to mm/day.
    """
    tmax = np.asarray(tasmax, dtype="float64")
    tmin = np.asarray(tasmin, dtype="float64")
    j = _expand_time_axis(np.asarray(doy, dtype="float64"), tmax.ndim)
    lat = np.asarray(lat_deg, dtype="float64")
    if lat.ndim == 1 and tmax.ndim == 3:
        lat = lat[:, None]
    phi = np.deg2rad(lat)
    dr = 1.0 + 0.033 * np.cos(2 * np.pi * j / 365.0)
    decl = 0.409 * np.sin(2 * np.pi * j / 365.0 - 1.39)
    ws = np.arccos(np.clip(-np.tan(phi) * np.tan(decl), -1.0, 1.0))
    ra = (
        (24 * 60 / np.pi)
        * 0.0820
        * dr
        * (ws * np.sin(phi) * np.sin(decl) + np.cos(phi) * np.cos(decl) * np.sin(ws))
    )
    tmean = (tmax + tmin) / 2.0
    td = np.clip(tmax - tmin, 0.0, None)
    return 0.0023 * 0.408 * ra * (tmean + 17.8) * np.sqrt(td)


def combine_pet(
    etref: np.ndarray,
    tasmin: Optional[np.ndarray],
    tasmax: Optional[np.ndarray],
    doy: Optional[np.ndarray],
    lat_deg: Optional[PixelScalar],
) -> np.ndarray:
    """Reference ET cube, mm/day: ``etref`` where finite, else Hargreaves from CHIRTS.

    Returns float64 ``(T, ...)``. NaN remains where ``etref`` is NaN and the
    Hargreaves inputs are NaN (or not supplied). Logs the fill count.
    """
    et = np.asarray(etref, dtype="float64")
    missing = ~np.isfinite(et)
    if not missing.any() or tasmin is None or tasmax is None:
        n_missing = int(missing.sum())
        if n_missing:
            logger.warning(
                f"combine_pet: {n_missing} NaN etref values and no CHIRTS fallback supplied"
            )
        return et
    hg = hargreaves_pet(tasmin, tasmax, doy, lat_deg)
    hg = np.broadcast_to(hg, et.shape)
    out = np.where(missing, hg, et)
    n_filled = int((missing & np.isfinite(hg)).sum())
    logger.info(
        f"combine_pet: filled {n_filled} of {int(missing.sum())} NaN etref values with Hargreaves"
    )
    return out


# ---------------------------------------------------------------------------
# 3.6 Whole-season wrapper
# ---------------------------------------------------------------------------
def season_phenology(
    pr: np.ndarray,
    pet: np.ndarray,
    search_start: PixelScalar,
    season_end: PixelScalar,
    search_end: PixelScalar,
    onset_params: OnsetParams = OnsetParams(),
    cessation_params: CessationParams = CessationParams(),
) -> dict:
    """Onset, cessation and length of one season for every pixel.

    Returns a dict of pixel-shaped arrays:

    * ``sos``, ``eos``, ``lgs`` : float32 indices (days since index 0), NaN
      where undefined; ``lgs = eos - sos`` exactly.
    * ``sos_status`` : int8 :class:`OnsetStatus`; ``eos_status`` : int8
      :class:`CessationStatus`.
    * ``eos_at_floor`` : bool, minimum-season gate was binding.
    * ``first_candidate`` : float32, first ``t`` in the search window with
      ``W[t] >= precip_threshold`` whether or not it validated (NaN if none).
    * ``n_false_starts`` : int16, number of candidate EPISODES (runs of
      consecutive trigger days) that ended before the onset day; when there is
      no onset, every episode in the window counts.
    """
    p2d, pixel_shape, _, _ = _to_cube(pr, "pr")
    ss = _pixel_param(search_start, pixel_shape, "search_start")
    se = _pixel_param(season_end, pixel_shape, "season_end")
    res = _onset_2d(p2d, ss, se, onset_params)
    onset = res["onset"]
    trigger = res["trigger"]
    n_time = p2d.shape[0]

    cand_found, cand_first = _first_true(trigger)
    first_candidate = np.where(cand_found, cand_first, np.nan).astype("float32")
    first_candidate[res["nodata"]] = np.nan

    ends = _episode_ends(trigger)
    t_ix = np.arange(n_time, dtype="float64")[:, None]
    onset_or_inf = np.where(res["found"], onset.astype("float64"), np.inf)[None, :]
    n_false = (ends & (t_ix < onset_or_inf)).sum(axis=0).astype("int16")
    n_false[res["nodata"]] = 0

    eos, eos_status, eos_at_floor = cessation_index(
        pr, pet, onset.reshape(pixel_shape), search_end, cessation_params
    )
    sos = onset.reshape(pixel_shape)
    return {
        "sos": sos,
        "eos": eos,
        "lgs": (eos - sos).astype("float32"),
        "sos_status": res["status"].reshape(pixel_shape),
        "eos_status": eos_status,
        "eos_at_floor": eos_at_floor,
        "first_candidate": first_candidate.reshape(pixel_shape),
        "n_false_starts": n_false.reshape(pixel_shape),
    }


# ---------------------------------------------------------------------------
# 3.7 Monitor state machine
# ---------------------------------------------------------------------------
def _trailing_sum(filled: np.ndarray, days: int) -> np.ndarray:
    """Sum of the last ``min(days, T)`` rows of a ``(T, N)`` slab (NaN already 0)."""
    if filled.shape[0] == 0:
        return np.zeros(filled.shape[1], dtype="float64")
    return filled[-days:].sum(axis=0)


def onset_state(
    pr_obs: np.ndarray,
    search_start: PixelScalar,
    season_end: PixelScalar,
    params: OnsetParams = OnsetParams(),
    pr_fcst: Optional[np.ndarray] = None,
) -> dict:
    """Current-season onset state per pixel, as-of the last observed day.

    Parameters
    ----------
    pr_obs : ``(T_obs, ...)`` observed daily rain (mm/day) through the as-of
        day ``T_obs - 1``.
    search_start, season_end : candidate window bounds (indices on the same
        axis), int or arrays broadcastable to the pixel shape.
    params : :class:`OnsetParams`.
    pr_fcst : optional ``(F, ...)`` forecast rain for days ``T_obs .. T_obs+F-1``.

    Candidate days are trigger days (``W >= precip_threshold`` inside the
    window). A candidate is CONFIRMED when ``t + validation_days <= T_obs``
    and no qualifying dry spell ends in ``[t+dry_spell_days-1,
    t+validation_days-1]``; INVALIDATED when a spell ends before ``T_obs``
    inside that window; PENDING otherwise. Runs of consecutive trigger days
    form one episode. State precedence: CONFIRMED (onset = first confirmed
    day) > PROVISIONAL (latest trigger day pending) > FALSE_START (candidates
    exist, none pending) > NOT_STARTED (``search_start <= T_obs-1``) >
    BEFORE_WINDOW; NO_ONSET replaces any non-confirmed state when
    ``T_obs-1 > season_end + validation_days``. The forecast never changes
    the state.

    Returns a dict of pixel-shaped arrays:

    * ``state`` int8 :class:`SeasonState`, -1 where rain is all-NaN or a bound
      is non-finite;
    * ``onset_idx`` float32 (confirmed, NaN otherwise);
    * ``candidate_idx`` float32 latest trigger day, ``days_since_candidate``
      float32 ``= T_obs-1 - candidate_idx``, ``days_to_confirm`` float32
      ``= candidate_idx + validation_days - T_obs`` (PROVISIONAL only, NaN elsewhere);
    * ``dry_run_now`` int16 ``r[T_obs-1]``; ``n_false_starts`` int16 invalidated
      episodes (before the onset when confirmed);
    * ``rain_10d``, ``rain_30d`` float32 trailing sums at as-of (mm, NaN counts 0);
    * ``fcst_trigger_idx`` float32: first ``t`` in ``[T_obs, T_obs+F)`` inside
      the search window with ``W[t] >= precip_threshold`` on the concatenated
      observed+forecast series (NaN if none or no forecast).
    """
    p2d, pixel_shape, n_obs, n_pix = _to_cube(pr_obs, "pr_obs")
    ss = _pixel_param(search_start, pixel_shape, "search_start")
    se = _pixel_param(season_end, pixel_shape, "season_end")
    comp = _onset_components(p2d, params)
    in_win = _in_window(n_obs, ss, se, params.window_days)
    trigger = in_win & (comp["W"] >= params.precip_threshold)
    look = comp["has_lookahead"][:, None]
    confirmed_day = trigger & look & ~comp["has_spell"]
    invalidated_day = trigger & comp["has_spell"]
    pending_day = trigger & ~look & ~comp["has_spell"]

    found_conf, first_conf = _first_true(confirmed_day)
    onset = np.where(found_conf, first_conf, np.nan).astype("float32")
    found_cand, last_cand = _last_true(trigger)
    candidate = np.where(found_cand, last_cand, np.nan).astype("float32")
    as_of = float(n_obs - 1)

    # latest trigger day's fate decides PROVISIONAL vs FALSE_START (within an
    # episode a later invalidated day implies every earlier day is invalidated)
    latest_pending = np.zeros(n_pix, dtype=bool)
    if n_obs:
        last_idx = np.where(found_cand, last_cand, 0)
        latest_pending = found_cand & pending_day[last_idx, np.arange(n_pix)]

    state = np.full(n_pix, int(SeasonState.BEFORE_WINDOW), dtype="int8")
    state[ss <= as_of] = int(SeasonState.NOT_STARTED)
    state[found_cand] = int(SeasonState.FALSE_START)
    state[latest_pending] = int(SeasonState.PROVISIONAL)
    state[(as_of > se + params.validation_days) & ~found_conf] = int(SeasonState.NO_ONSET)
    state[found_conf] = int(SeasonState.CONFIRMED)

    days_since = np.where(found_cand, as_of - candidate, np.nan).astype("float32")
    provisional = state == int(SeasonState.PROVISIONAL)
    days_to_confirm = np.where(
        provisional, candidate + params.validation_days - n_obs, np.nan
    ).astype("float32")

    ends = _episode_ends(trigger)
    t_ix = np.arange(n_obs, dtype="float64")[:, None]
    onset_or_inf = np.where(found_conf, onset.astype("float64"), np.inf)[None, :]
    n_false = (ends & invalidated_day & (t_ix < onset_or_inf)).sum(axis=0).astype("int16")

    dry_run_now = (
        comp["r"][-1].astype("int16") if n_obs else np.zeros(n_pix, dtype="int16")
    )
    rain_10d = _trailing_sum(comp["filled"], 10).astype("float32")
    rain_30d = _trailing_sum(comp["filled"], 30).astype("float32")

    fcst_trigger = np.full(n_pix, np.nan, dtype="float32")
    if pr_fcst is not None:
        f2d, f_shape, n_f, _ = _to_cube(pr_fcst, "pr_fcst")
        if f_shape != pixel_shape:
            raise ValueError(f"pr_fcst pixel shape {f_shape} != pr_obs pixel shape {pixel_shape}")
        if n_f > 0:
            both = np.nan_to_num(np.concatenate([p2d, f2d], axis=0), nan=0.0)
            w_all = _rolling_sum(both, params.window_days)
            in_win_all = _in_window(n_obs + n_f, ss, se, params.window_days)
            trig_f = in_win_all[n_obs:] & (w_all[n_obs:] >= params.precip_threshold)
            found_f, first_f = _first_true(trig_f)
            fcst_trigger = np.where(found_f, first_f + n_obs, np.nan).astype("float32")

    nodata = comp["allnan"] | ~np.isfinite(ss) | ~np.isfinite(se)
    state[nodata] = NODATA_STATUS
    for arr in (onset, candidate, days_since, days_to_confirm, fcst_trigger):
        arr[nodata] = np.nan
    n_false[nodata] = 0

    return {
        "state": state.reshape(pixel_shape),
        "onset_idx": onset.reshape(pixel_shape),
        "candidate_idx": candidate.reshape(pixel_shape),
        "days_since_candidate": days_since.reshape(pixel_shape),
        "days_to_confirm": days_to_confirm.reshape(pixel_shape),
        "dry_run_now": dry_run_now.reshape(pixel_shape),
        "n_false_starts": n_false.reshape(pixel_shape),
        "rain_10d": rain_10d.reshape(pixel_shape),
        "rain_30d": rain_30d.reshape(pixel_shape),
        "fcst_trigger_idx": fcst_trigger.reshape(pixel_shape),
    }


# ---------------------------------------------------------------------------
# 3.8 Climatology statistics (years on axis 0, NaN = that year had no onset)
# ---------------------------------------------------------------------------
def onset_climatology(stack: np.ndarray, min_valid_years: int = 20) -> dict:
    """Per-pixel climatology of a ``(Y, ...)`` stack of yearly indices.

    Returns float32 ``median``, ``p25``, ``p75``, ``std`` (sample, ddof=1; NaN
    where ``n_valid < max(min_valid_years, 2)``), int16 ``n_valid`` (finite
    years) and float32 ``frac_no_onset = 1 - n_valid / Y`` (NaN when ``Y == 0``).
    ``median``/``p25``/``p75`` are NaN where ``n_valid < min_valid_years``.
    Units follow the input (days since planting start).
    """
    s2d, pixel_shape, n_years, n_pix = _to_cube(stack, "stack")
    valid = np.isfinite(s2d)
    n_valid = valid.sum(axis=0).astype("int16")
    out_nan = np.full(n_pix, np.nan, dtype="float64")
    if n_years == 0:
        med = p25 = p75 = std = out_nan.copy()
        frac = out_nan.copy()
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            med = np.nanmedian(s2d, axis=0)
            p25 = np.nanpercentile(s2d, 25, axis=0)
            p75 = np.nanpercentile(s2d, 75, axis=0)
            std = np.nanstd(s2d, axis=0, ddof=1)
        enough = n_valid >= min_valid_years
        med = np.where(enough, med, np.nan)
        p25 = np.where(enough, p25, np.nan)
        p75 = np.where(enough, p75, np.nan)
        std = np.where(enough & (n_valid >= 2), std, np.nan)
        frac = 1.0 - n_valid.astype("float64") / n_years
    return {
        "median": med.astype("float32").reshape(pixel_shape),
        "p25": p25.astype("float32").reshape(pixel_shape),
        "p75": p75.astype("float32").reshape(pixel_shape),
        "std": std.astype("float32").reshape(pixel_shape),
        "n_valid": n_valid.reshape(pixel_shape),
        "frac_no_onset": frac.astype("float32").reshape(pixel_shape),
    }


def conditional_onset_probability(
    stack: np.ndarray, d: PixelScalar, horizon: int, min_years: int = 5
) -> np.ndarray:
    """``P(d < onset <= d + horizon | onset > d or never)`` from a ``(Y, ...)`` stack.

    ``d`` is an index (days since planting start), scalar or per-pixel;
    ``horizon`` in days. Numerator = years with ``d < onset <= d + horizon``;
    denominator = years with ``onset > d`` or NaN (no onset). Returns float32,
    NaN where the denominator is below ``min_years`` (or where ``d`` is NaN).
    """
    s2d, pixel_shape, _, _ = _to_cube(stack, "stack")
    d_px = _pixel_param(d, pixel_shape, "d")[None, :]
    later = s2d > d_px
    num = (later & (s2d <= d_px + float(horizon))).sum(axis=0)
    den = (later | np.isnan(s2d)).sum(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        p = np.where(den >= max(int(min_years), 1), num / den, np.nan)
    p = np.where(np.isfinite(d_px[0]), p, np.nan)
    return p.astype("float32").reshape(pixel_shape)


def onset_percentile(stack: np.ndarray, value: PixelScalar, min_valid_years: int = 1) -> np.ndarray:
    """Share of past valid years with ``onset <= value`` (float32 in 0..1).

    ``value`` is an index on the same axis, scalar or per-pixel; NaN ``value``
    -> NaN. Years without onset (NaN) are excluded from the denominator; NaN
    where fewer than ``min_valid_years`` valid years exist.
    """
    s2d, pixel_shape, _, _ = _to_cube(stack, "stack")
    v_px = _pixel_param(value, pixel_shape, "value")[None, :]
    valid = np.isfinite(s2d)
    n_valid = valid.sum(axis=0)
    n_le = (valid & (s2d <= v_px)).sum(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        share = np.where(n_valid >= max(int(min_valid_years), 1), n_le / n_valid, np.nan)
    share = np.where(np.isfinite(v_px[0]), share, np.nan)
    return share.astype("float32").reshape(pixel_shape)


__all__ = [
    "NODATA_STATUS",
    "OnsetParams",
    "CessationParams",
    "OnsetStatus",
    "CessationStatus",
    "SeasonState",
    "onset_index",
    "cessation_index",
    "hargreaves_pet",
    "combine_pet",
    "season_phenology",
    "onset_state",
    "onset_climatology",
    "conditional_onset_probability",
    "onset_percentile",
]
