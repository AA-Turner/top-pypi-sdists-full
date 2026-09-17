# -*- coding: utf-8 -*-
"""Per-calendar-zone start-of-season report over a window around the planting date.

The question this answers
-------------------------
For each GEOGLAM Crop Monitor calendar zone: **in the two months around the
calendar planting date, how often has the season actually started, when, and how
does the season now running compare?**

The window is the calendar planting start plus or minus ``window_days`` (30 by
default, so a two-month span centred on the date the crop calendar nominates).
Because :mod:`geocif.phenology.climatology` already stores onset as *days since
that pixel's own planting start*, the window is a plain range filter on the
cached rasters -- ``-window_days <= sos <= +window_days`` -- and needs no date
arithmetic and no recomputation. The whole report is an aggregation of the cache.

Censoring, and why the search lead matters
------------------------------------------
The onset search opens ``search_start_days_before_planting`` days early. A pixel
whose rains arrived before that is reported AT the search boundary, not at its
true date, so it is indistinguishable from one that started exactly there. When
the search lead equals the window half-width, "started at the left edge" and
"started before the window" collapse into one value and the in-window share is
overstated. Measured on Kenya maize season 1 with a 30-day lead and a 30-day
window: 18.3 % of pixel-years in the West zone and 8.5 % in Rift Valley sat at
exactly -30, while the four eastern zones sat at 0.0 %.

:func:`censoring_share` reports that fraction per zone and every table carries
it, so a reader can see when a share is a floor rather than a measurement. Give
the climatology a lead comfortably wider than the window (60 days for a 30-day
window) and the censored fraction goes to near zero.

What it produces
----------------
* :func:`zone_history` -- one row per (zone, harvest year): crop-area-weighted
  median onset, its quartiles, the share of cropland that started inside the
  window, the share that started at all, and the censored share.
* :func:`zone_climatology` -- one row per zone over the whole record: the
  typical start date and its spread, and how many years in the record started
  on time.
* :func:`current_vs_history` -- one row per zone for the season now running,
  with an explicit :class:`WindowStatus` so a partial or unopened window is
  never read as a complete one.

Units: onset values are days relative to the pixel's planting start (negative =
before it). Dates are calendar dates derived from the zone's planting date for
that harvest year. Weights are crop area in km2 (crop fraction x pixel area).
"""

from __future__ import annotations

import datetime as _dt
import json
import logging
from enum import Enum
from pathlib import Path
from typing import Any, Optional, Sequence

import numpy as np
import pandas as pd

from geocif.phenology import climatology, inputs
from geocif.phenology.outputs import _clean_weight, _weighted_median

logger = logging.getLogger(__name__)

#: Half-width of the reporting window, in days either side of the planting date.
DEFAULT_WINDOW_DAYS: int = 30

#: Minimum years with a usable value before a climatology statistic is reported.
DEFAULT_MIN_YEARS: int = 20


class WindowStatus(str, Enum):
    """How much of the window the observations actually cover.

    A share computed over a partly observed window is a floor, not a
    measurement, and must never be presented as the latter.
    """

    #: The window has closed; the value is final.
    COMPLETE = "complete"
    #: The window is open and partly observed; shares can still rise.
    PARTIAL = "partial"
    #: The window has not opened yet; nothing is measurable.
    NOT_OPEN = "not_open"


def _weighted_quantile(
    values: np.ndarray, weights: np.ndarray, q: float
) -> float:
    """Weighted quantile of ``values`` (lower interpolation), NaN when empty.

    Args:
        values: finite values.
        weights: non-negative weights, same shape.
        q: quantile in ``[0, 1]``.

    Returns:
        The smallest value whose cumulative weight reaches ``q`` of the total.
    """
    v = np.asarray(values, dtype="float64").ravel()
    w = _clean_weight(np.asarray(weights, dtype="float64").ravel())
    keep = np.isfinite(v) & (w > 0)
    if not keep.any():
        return float("nan")
    v, w = v[keep], w[keep]
    order = np.argsort(v, kind="stable")
    v, w = v[order], w[order]
    cum = np.cumsum(w)
    total = cum[-1]
    if total <= 0:
        return float("nan")
    idx = int(np.searchsorted(cum, q * total, side="left"))
    return float(v[min(idx, v.size - 1)])


def _share(mask: np.ndarray, weights: np.ndarray) -> float:
    """Weighted share of ``mask`` over all positive weight, NaN when none."""
    w = _clean_weight(np.asarray(weights, dtype="float64").ravel())
    m = np.asarray(mask).ravel()
    total = w.sum()
    if total <= 0:
        return float("nan")
    return float(w[m].sum() / total)


def censoring_share(
    onset: np.ndarray, weights: np.ndarray, search_lead_days: int
) -> float:
    """Weighted share of onsets pinned at the search boundary.

    A value of exactly ``-search_lead_days`` means the rains arrived at or
    before the first day the algorithm was allowed to look, so the true onset is
    unknown and this value is an upper bound on the date.

    Args:
        onset: onset in days from the planting start.
        weights: crop area weights.
        search_lead_days: how many days before planting the search opened.

    Returns:
        Share in ``[0, 1]`` of onsets sitting exactly on the boundary, over the
        pixels that HAVE an onset (NaN when none do).
    """
    v = np.asarray(onset, dtype="float64").ravel()
    w = _clean_weight(np.asarray(weights, dtype="float64").ravel())
    have = np.isfinite(v) & (w > 0)
    if not have.any():
        return float("nan")
    at_edge = have & (v <= -float(search_lead_days))
    return float(w[at_edge].sum() / w[have].sum())


def zone_masks(zone_id: np.ndarray, zone_names: Sequence[str]) -> dict:
    """``{zone_name: bool mask}`` from the rasterized zone-id grid.

    ``zone_id`` uses 0 for "no zone" and ``i + 1`` for ``zone_names[i]``, the
    convention :func:`geocif.phenology.inputs.rasterize_calendar` writes.
    """
    zid = np.asarray(zone_id)
    return {name: (zid == i + 1) for i, name in enumerate(zone_names)}


def zone_history(
    stack: np.ndarray,
    years: Sequence[int],
    zone_id: np.ndarray,
    zone_names: Sequence[str],
    weights: np.ndarray,
    *,
    window_days: int = DEFAULT_WINDOW_DAYS,
    search_lead_days: int = DEFAULT_WINDOW_DAYS,
    planting_dates: Optional[dict] = None,
) -> pd.DataFrame:
    """One row per (zone, harvest year) describing that year's start of season.

    Args:
        stack: ``(n_years, rows, cols)`` onset in days from the planting start,
            NaN where the year produced none (the cached ``sos`` rasters).
        years: harvest years, in ``stack`` order.
        zone_id: rasterized calendar zones (0 = none).
        zone_names: zone names, ``zone_names[i]`` <-> ``zone_id == i + 1``.
        weights: crop area per pixel, km2.
        window_days: half-width of the window either side of planting.
        search_lead_days: days the onset search opened before planting, used to
            flag boundary censoring.
        planting_dates: optional ``{(zone, year): date}`` to turn the median
            offset into a calendar date.

    Returns:
        Columns: ``zone``, ``harvest_year``, ``crop_area_km2``,
        ``share_started`` (any onset), ``share_in_window``,
        ``share_before_window``, ``share_after_window``, ``share_censored``,
        ``onset_median_days``/``_p25``/``_p75`` (over pixels that started inside
        the window) and, when ``planting_dates`` is given, ``planting_date`` and
        ``onset_median_date``.
    """
    cube = np.asarray(stack, dtype="float64")
    if cube.shape[0] != len(years):
        raise ValueError(f"stack has {cube.shape[0]} years, got {len(years)} labels")
    masks = zone_masks(zone_id, zone_names)
    w_all = np.asarray(weights, dtype="float64")

    rows: list[dict] = []
    for name, mask in masks.items():
        cells = mask & (_clean_weight(w_all) > 0)
        if not cells.any():
            continue
        w = w_all[cells]
        for j, year in enumerate(years):
            v = cube[j][cells]
            started = np.isfinite(v)
            in_win = started & (v >= -window_days) & (v <= window_days)
            before = started & (v < -window_days)
            after = started & (v > window_days)
            row = {
                "zone": name,
                "harvest_year": int(year),
                "crop_area_km2": float(_clean_weight(w).sum()),
                "share_started": _share(started, w),
                "share_in_window": _share(in_win, w),
                "share_before_window": _share(before, w),
                "share_after_window": _share(after, w),
                "share_censored": censoring_share(v, w, search_lead_days),
                "onset_median_days": _weighted_median(v[in_win], w[in_win]),
                "onset_p25_days": _weighted_quantile(v[in_win], w[in_win], 0.25),
                "onset_p75_days": _weighted_quantile(v[in_win], w[in_win], 0.75),
            }
            if planting_dates:
                plant = planting_dates.get((name, int(year)))
                row["planting_date"] = plant.isoformat() if plant else None
                med = row["onset_median_days"]
                row["onset_median_date"] = (
                    (plant + _dt.timedelta(days=int(round(med)))).isoformat()
                    if plant is not None and np.isfinite(med)
                    else None
                )
            rows.append(row)
    return pd.DataFrame(rows)


def zone_climatology(
    history: pd.DataFrame, *, min_years: int = DEFAULT_MIN_YEARS
) -> pd.DataFrame:
    """Collapse :func:`zone_history` to one row per zone over the record.

    Args:
        history: the per-(zone, year) frame.
        min_years: fewer usable years than this and the statistics are NaN --
            reported anyway, with ``n_years``, so the gap is visible.

    Returns:
        Columns: ``zone``, ``n_years``, ``n_years_with_onset``,
        ``share_in_window_mean`` (how often the zone starts on time),
        ``onset_median_days`` (typical offset), ``onset_days_p25``/``_p75`` and
        ``onset_days_iqr`` (its year-to-year spread), ``share_started_mean``,
        ``share_censored_mean``.
    """
    if history.empty:
        return pd.DataFrame()
    out: list[dict] = []
    for zone, grp in history.groupby("zone", sort=True):
        med = grp["onset_median_days"].to_numpy(dtype="float64")
        usable = np.isfinite(med)
        n_usable = int(usable.sum())
        enough = n_usable >= int(min_years)
        out.append(
            {
                "zone": zone,
                "n_years": int(len(grp)),
                "n_years_with_onset": n_usable,
                "share_in_window_mean": float(grp["share_in_window"].mean(skipna=True)),
                "share_started_mean": float(grp["share_started"].mean(skipna=True)),
                "share_censored_mean": float(grp["share_censored"].mean(skipna=True)),
                "onset_median_days": float(np.median(med[usable])) if enough else float("nan"),
                "onset_days_p25": float(np.percentile(med[usable], 25)) if enough else float("nan"),
                "onset_days_p75": float(np.percentile(med[usable], 75)) if enough else float("nan"),
                "onset_days_iqr": (
                    float(np.percentile(med[usable], 75) - np.percentile(med[usable], 25))
                    if enough
                    else float("nan")
                ),
                "min_years": int(min_years),
            }
        )
    return pd.DataFrame(out)


def window_status(
    as_of: _dt.date, planting: _dt.date, window_days: int
) -> tuple[WindowStatus, int, int]:
    """Where ``as_of`` sits relative to the window around ``planting``.

    Returns:
        ``(status, days_observed, days_total)``. ``days_observed`` is clamped to
        ``[0, days_total]``; ``days_total`` is ``2 * window_days + 1``.
    """
    total = 2 * int(window_days) + 1
    opens = planting - _dt.timedelta(days=int(window_days))
    closes = planting + _dt.timedelta(days=int(window_days))
    if as_of < opens:
        return WindowStatus.NOT_OPEN, 0, total
    observed = min((as_of - opens).days + 1, total)
    if as_of >= closes:
        return WindowStatus.COMPLETE, total, total
    return WindowStatus.PARTIAL, observed, total


def current_vs_history(
    current: np.ndarray,
    history: pd.DataFrame,
    zone_id: np.ndarray,
    zone_names: Sequence[str],
    weights: np.ndarray,
    *,
    as_of: _dt.date,
    planting_dates: dict,
    harvest_year: int,
    window_days: int = DEFAULT_WINDOW_DAYS,
    search_lead_days: int = DEFAULT_WINDOW_DAYS,
) -> pd.DataFrame:
    """Compare the season now running against the record, per zone.

    Args:
        current: onset for the running season, days from the planting start,
            NaN where onset has not been confirmed.
        history: the frame from :func:`zone_history` (past years only).
        zone_id, zone_names, weights: as in :func:`zone_history`.
        as_of: last observed day.
        planting_dates: ``{(zone, harvest_year): date}``; the running season's
            entry decides the window status.
        harvest_year: the running season's harvest year.
        window_days, search_lead_days: window geometry.

    Returns:
        One row per zone: the window status and its coverage, this season's
        in-window share and median onset, and how those rank against the record
        (``share_percentile``, ``onset_percentile``, both over past years, NaN
        when the window is not complete enough to rank honestly).
    """
    cur = np.asarray(current, dtype="float64")
    masks = zone_masks(zone_id, zone_names)
    w_all = np.asarray(weights, dtype="float64")
    past = history[history["harvest_year"] != int(harvest_year)] if not history.empty else history

    rows: list[dict] = []
    for name, mask in masks.items():
        cells = mask & (_clean_weight(w_all) > 0)
        if not cells.any():
            continue
        w = w_all[cells]
        v = cur[cells]
        plant = planting_dates.get((name, int(harvest_year)))
        if plant is None:
            status, observed, total = WindowStatus.NOT_OPEN, 0, 2 * window_days + 1
        else:
            status, observed, total = window_status(as_of, plant, window_days)

        started = np.isfinite(v)
        in_win = started & (v >= -window_days) & (v <= window_days)
        share_in = _share(in_win, w) if status is not WindowStatus.NOT_OPEN else float("nan")
        med = (
            _weighted_median(v[in_win], w[in_win])
            if status is not WindowStatus.NOT_OPEN
            else float("nan")
        )

        zone_past = past[past["zone"] == name] if not past.empty else past
        # Rank only against a window that has actually closed: a partial share
        # can still rise, so ranking it against complete years reads low.
        rankable = status is WindowStatus.COMPLETE and not zone_past.empty
        share_pct = onset_pct = float("nan")
        if rankable:
            hs = zone_past["share_in_window"].to_numpy(dtype="float64")
            hs = hs[np.isfinite(hs)]
            if hs.size and np.isfinite(share_in):
                share_pct = float(np.mean(hs <= share_in) * 100.0)
            hm = zone_past["onset_median_days"].to_numpy(dtype="float64")
            hm = hm[np.isfinite(hm)]
            if hm.size and np.isfinite(med):
                onset_pct = float(np.mean(hm <= med) * 100.0)

        rows.append(
            {
                "zone": name,
                "harvest_year": int(harvest_year),
                "as_of": as_of.isoformat(),
                "planting_date": plant.isoformat() if plant else None,
                "window_opens": (
                    (plant - _dt.timedelta(days=window_days)).isoformat() if plant else None
                ),
                "window_closes": (
                    (plant + _dt.timedelta(days=window_days)).isoformat() if plant else None
                ),
                "window_status": status.value,
                "window_days_observed": int(observed),
                "window_days_total": int(total),
                "crop_area_km2": float(_clean_weight(w).sum()),
                "share_started": (
                    _share(started, w) if status is not WindowStatus.NOT_OPEN else float("nan")
                ),
                "share_in_window": share_in,
                "share_censored": (
                    censoring_share(v, w, search_lead_days)
                    if status is not WindowStatus.NOT_OPEN
                    else float("nan")
                ),
                "onset_median_days": med,
                "onset_median_date": (
                    (plant + _dt.timedelta(days=int(round(med)))).isoformat()
                    if plant is not None and np.isfinite(med)
                    else None
                ),
                "share_percentile_vs_history": share_pct,
                "onset_percentile_vs_history": onset_pct,
                "n_history_years": int(len(zone_past)) if not zone_past.empty else 0,
            }
        )
    return pd.DataFrame(rows)


def planting_dates_by_zone(
    parser, country: str, crop: str, season: int, years: Sequence[int]
) -> dict:
    """``{(zone_name, harvest_year): planting date}`` from the crop calendar.

    Reads the calendar once and rasterizes nothing: the planting date is a
    property of the zone and the harvest year, so it is taken straight from the
    24-bin flag row through the same block logic the rasterizer uses.
    """
    zones_gdf, flags_by_season = inputs.load_calendar_zones(parser, country, crop)
    per_zone = flags_by_season.get(int(season), {})
    out: dict = {}
    for zone_key, flags in per_zone.items():
        for year in years:
            dates = inputs._season_dates(flags, int(season), int(year))
            if dates and dates[0] is not None:
                out[(zone_key, int(year))] = dates[0]
    return out


def load_onset_stack(cache_dir: Any) -> tuple[np.ndarray, list[int]]:
    """Load the per-year ``sos`` rasters from a climatology cache.

    Returns:
        ``(stack, years)`` with ``stack`` float32 ``(n_years, rows, cols)`` in
        ascending year order and NaN where a year had no onset.

    Raises:
        FileNotFoundError: when the cache has no manifest.
    """
    cache = Path(cache_dir)
    manifest_path = cache / climatology.MANIFEST_FILE
    if not manifest_path.is_file():
        raise FileNotFoundError(f"no climatology manifest at {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    years = [int(y) for y in manifest.get("years", [])]
    layers = [
        climatology._read_raster(cache / climatology.YEAR_SUBDIR / f"sos_{y}.tif")
        for y in years
    ]
    return np.stack(layers).astype("float32"), years
