# -*- coding: utf-8 -*-
"""Current-season onset monitor (DESIGN.md section 8).

What this module answers, per pixel, for the season that is running right now:

* has onset happened (``state``, six :class:`~geocif.phenology.core.SeasonState`
  codes), and if so on which day (``onset_idx``, ``onset_date``);
* is that early or late against the cached climatology
  (``onset_anomaly_days``, ``onset_percentile``);
* if it has NOT happened, how far past the climatological median we already are
  (``days_past_median``) and what the record says the chance is that it still
  comes in the next 14 / 28 days (``p_onset_14d``, ``p_onset_28d``);
* how wet it has been (``rain_10d``, ``rain_30d``, ``rain_30d_percentile``),
  how long the current dry run is (``dry_run_now``), how many candidates have
  already failed (``n_false_starts``) and how often they fail climatologically
  (``false_start_rate``);
* when the CHIRPS-GEFS forecast expects the trigger to be met
  (``fcst_trigger_days``) -- reported alongside the state, never folded into it.

Units and index conventions
---------------------------
* The observed cube starts at ``start_date = min(planting) -
  search_start_days_before_planting`` and ends on the **as-of day**, which is the
  last CHIRPS day actually on disk. Every ``*_idx`` layer is an integer position
  on that axis (day 0 = ``start_date``).
* Every ``*_days`` layer is in **days**; ``onset_days`` (and therefore
  ``onset_anomaly_days``, ``days_past_median`` and the conditioning day handed
  to the climatology) is in **days since THAT PIXEL's calendar planting start**,
  the same convention ``geocif.phenology.climatology`` writes its rasters in.
  Negative values are normal -- the search opens before planting.
* ``onset_anomaly_days`` is ``onset - climatological median``, so **positive =
  LATE**. ``days_past_median`` is ``as-of - climatological median`` and is
  populated only on ``NOT_STARTED`` pixels.
* ``onset_date`` is in **days since 1970-01-01** (an integer day number, so the
  layer survives a GeoTIFF round trip); rain is mm; probabilities and
  ``onset_percentile`` are shares in ``[0, 1]``; ``rain_30d_percentile`` is a
  percentile in ``[0, 100]`` because that is what
  ``geocif.viz.phenology_maps.rain_percentile_map`` draws.
* Arrays returned here are float32 with NaN nodata, except ``state`` which is
  int8 with ``-1``. :data:`MONITOR_LAYERS` carries the on-disk dtype and nodata
  for each one.

``n_false_starts`` -- which of the two meanings
----------------------------------------------
``core.season_phenology`` counts EVERY candidate episode before onset while
``core.onset_state`` counts only the INVALIDATED ones. This module reports the
**invalidated-episode** meaning everywhere: ``n_false_starts`` comes straight
from :func:`core.onset_state`, and the cached ``false_start_rate`` layer is
named for the same meaning (``climatology.py`` builds it from
``core.onset_state`` for exactly this reason). ``core.py`` is not modified.

Grid contract with the climatology cache
----------------------------------------
``climatology.build_climatology`` windows the country with
``inputs.country_bbox(parser, country)`` at its default buffer. A monitor run on
a different ``bbox_buffer`` therefore lands on a different grid; the climatology
arrays are then dropped with a warning instead of being broadcast into the wrong
place, and the run continues with the observation-only layers.

No icclim, no pygmt, no CID code is imported here.
"""

from __future__ import annotations

import ast
import datetime as _dt
import logging
from typing import Any, NamedTuple, Optional, Sequence

import numpy as np
import pandas as pd
from rasterio.windows import Window

from geocif.phenology import climatology, core, inputs, outputs

logger = logging.getLogger(__name__)

#: Day 0 of the ``onset_date`` layer.
EPOCH: np.datetime64 = np.datetime64("1970-01-01", "D")

#: Per-layer on-disk contract: name -> (dtype, nodata, units).
MONITOR_LAYERS: dict[str, tuple[str, float, str]] = {
    "state": ("int8", -1.0, "SeasonState code (-1 = no calendar or no rain)"),
    "onset_idx": ("int16", -32768.0, "days since the first day of the observed cube"),
    "onset_date": ("int32", -2147483648.0, "days since 1970-01-01"),
    "onset_days": ("int16", -32768.0, "days since pixel planting start"),
    "onset_anomaly_days": ("float32", np.nan, "days, positive = later than the median"),
    "onset_percentile": ("float32", np.nan, "share of climatology years onsetting no later, 0..1"),
    "days_past_median": ("float32", np.nan, "days past the median, NOT_STARTED pixels only"),
    "p_onset_14d": ("float32", np.nan, "conditional probability of onset within 14 days, 0..1"),
    "p_onset_28d": ("float32", np.nan, "conditional probability of onset within 28 days, 0..1"),
    "rain_10d": ("float32", np.nan, "mm in the 10 days ending on the as-of day"),
    "rain_30d": ("float32", np.nan, "mm in the 30 days ending on the as-of day"),
    "rain_30d_percentile": ("float32", np.nan, "percentile of the 30-day total, 0..100"),
    "dry_run_now": ("int16", -32768.0, "consecutive dry days ending on the as-of day"),
    "n_false_starts": ("int16", -32768.0, "count of invalidated candidate episodes"),
    "false_start_rate": ("float32", np.nan, "share of climatology years with >= 1 false start, 0..1"),
    "fcst_trigger_days": ("float32", np.nan, "days from the as-of day to the forecast trigger"),
}

#: Conditional-probability horizons (days) produced by default.
DEFAULT_HORIZONS: tuple[int, int] = (14, 28)

#: Trailing rainfall windows (days) reported at the as-of day.
RAIN_WINDOWS: tuple[int, int] = (10, 30)

#: The trailing window whose climatological percentile is computed.
RAIN_PERCENTILE_WINDOW: int = 30

#: Layers summarised per admin unit and per calendar zone in ``onset_summary``.
SUMMARY_LAYERS: tuple[str, ...] = (
    "onset_anomaly_days",
    "days_past_median",
    "p_onset_14d",
    "p_onset_28d",
)


# ---------------------------------------------------------------------------
# 8.1 Which seasons are running today
# ---------------------------------------------------------------------------
class ActiveSeason(NamedTuple):
    """One (country, crop, season, harvest year) the monitor should run.

    A plain 4-tuple, so ``("kenya", "maize", 2, 2026)`` compares equal to it.
    The season is labelled by its **harvest year** (Kenya short rains running
    Oct 2025 - Feb 2026 is harvest year 2026).
    """

    country: str
    crop: str
    season: int
    harvest_year: int


def _literal_list(parser, section: str, option: str, default: Sequence[Any]) -> list:
    """``ast.literal_eval`` of ``[section] option`` as a list, or ``default``.

    ``[DEFAULT]`` inheritance is deliberate here: ``crops`` and ``seasons`` live
    in the ``[DEFAULT]`` block of countries.txt and are overridden per country,
    which is exactly the semantics every other geocif runner uses.
    """
    if section != "DEFAULT" and not parser.has_section(section):
        # No [country] block: the configured [DEFAULT] value still applies,
        # which is how countries.txt is written (crops/seasons live there).
        logger.info(f"no [{section}] section; reading {option} from [DEFAULT]")
        section = "DEFAULT"
    if not parser.has_option(section, option):
        return list(default)
    raw = (parser.get(section, option) or "").strip()
    if not raw:
        return list(default)
    try:
        value = ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return [raw]
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def crops_for(parser, country: str) -> list[str]:
    """Crop slugs configured for ``country`` (``[country] crops``)."""
    return [str(c).strip() for c in _literal_list(parser, country, "crops", ["maize"])]


def seasons_for(
    parser, country: str, override: Optional[Sequence[Any]] = None
) -> list[int]:
    """Season numbers to monitor for ``country``.

    ``override`` (from ``[SEASON_MONITOR] seasons_<country>``) wins over the
    shared ``[country] seasons``. The shared key is read by the CID, extract and
    merge pipelines too, and those need a merged CSV per season that only exists
    for the seasons they were built for -- so adding a secondary season there to
    get it monitored would break them. This monitor reads rasters and the crop
    calendar directly and needs no such file, hence the separate key.

    Args:
        parser: the 4-file config parser.
        country: country slug.
        override: explicit season numbers, or ``None`` to use the config.

    Returns:
        Season numbers, never empty (falls back to ``[1]``).
    """
    values = (
        list(override)
        if override is not None
        else _literal_list(parser, country, "seasons", [1])
    )
    out: list[int] = []
    for value in values:
        try:
            out.append(int(value))
        except (TypeError, ValueError):
            logger.warning(f"{country}: ignoring non-numeric season {value!r}")
    return out or [1]


def season_bounds(
    flags_by_season: dict, season: int, harvest_year: int
) -> Optional[tuple[_dt.date, _dt.date]]:
    """Earliest planting start and latest harvest end over every calendar zone.

    Args:
        flags_by_season: ``season -> {zone_key: 24-bin flags}`` from
            :func:`geocif.phenology.inputs.load_calendar_zones`.
        season: 1-based season number.
        harvest_year: the year that labels the season.

    Returns:
        ``(earliest_planting, latest_harvest)`` as dates, or ``None`` when no
        zone carries this season (every row is the all ``-1`` sentinel, or the
        sheet is absent).
    """
    per_zone = flags_by_season.get(int(season), {})
    plantings: list[_dt.date] = []
    harvests: list[_dt.date] = []
    for flags in per_zone.values():
        # inputs._season_dates is the single implementation of the wrapped-block
        # / cross-year rule; re-deriving it here is how the two would drift.
        dates = inputs._season_dates(np.asarray(flags), int(season), int(harvest_year))
        if dates is None:
            continue
        plantings.append(dates[0])
        harvests.append(dates[1])
    if not plantings:
        return None
    return min(plantings), max(harvests)


def active_seasons(
    parser,
    as_of: _dt.date,
    countries: Optional[Sequence[str]] = None,
    search_start_days_before_planting: int = 30,
    validation_days: int = 30,
    seasons_by_country: Optional[dict] = None,
) -> list[ActiveSeason]:
    """Every configured season whose monitoring window contains ``as_of``.

    A season is active when its onset search has opened -- ``as_of >=
    min(planting) - search_start_days_before_planting`` -- and its last useful
    day has not passed -- ``as_of <= max(harvest) + validation_days``. Both
    bounds are taken over the country's calendar zones, so a season is active as
    soon as its earliest zone opens and stays active until its latest zone is
    done.

    Args:
        parser: the 4-file config parser.
        as_of: the data-through date (last CHIRPS day on disk).
        countries: country slugs; ``None`` reads ``[DEFAULT] countries``.
        search_start_days_before_planting: days the search opens early (days).
        validation_days: onset look-ahead, the tail kept after harvest (days).
        seasons_by_country: ``{country: [season, ...]}`` overriding
            ``[country] seasons`` for this product only -- see
            :func:`seasons_for`. Countries absent from it use the config.

    Returns:
        Sorted list of :class:`ActiveSeason`. Harvest years ``as_of.year - 1``
        through ``as_of.year + 1`` are considered, so cross-year seasons are
        picked up from either side; a country/crop whose calendar cannot be read
        is logged and skipped, never fatal.
    """
    if countries is None:
        countries = [str(c) for c in _literal_list(parser, "DEFAULT", "countries", [])]
    out: list[ActiveSeason] = []
    for country in countries:
        country = str(country).strip()
        if not country:
            continue
        for crop in crops_for(parser, country):
            try:
                _zones, flags_by_season = inputs.load_calendar_zones(parser, country, crop)
            except Exception as exc:  # noqa: BLE001 - a missing sheet is not fatal
                logger.warning(f"active_seasons: no calendar for {country}/{crop}: {exc}")
                continue
            for season in seasons_for(
                parser, country, (seasons_by_country or {}).get(country)
            ):
                for harvest_year in (as_of.year - 1, as_of.year, as_of.year + 1):
                    bounds = season_bounds(flags_by_season, season, harvest_year)
                    if bounds is None:
                        continue
                    planting, harvest = bounds
                    opens = planting - _dt.timedelta(days=int(search_start_days_before_planting))
                    closes = harvest + _dt.timedelta(days=int(validation_days))
                    if opens <= as_of <= closes:
                        out.append(ActiveSeason(country, crop, int(season), int(harvest_year)))
                        logger.info(
                            f"active season {country}/{crop} s{season} harvest {harvest_year}: "
                            f"search opened {opens}, window closes {closes}"
                        )
    return sorted(set(out))


# ---------------------------------------------------------------------------
# 8.2 Pure layer builders (no I/O -- these are what the unit tests drive)
# ---------------------------------------------------------------------------
def observed_layers(
    pr_obs: np.ndarray,
    search_start: Any,
    season_end: Any,
    params: core.OnsetParams,
    start_date: _dt.date,
    planting_offset: np.ndarray,
    pr_fcst: Optional[np.ndarray] = None,
) -> dict:
    """Run the state machine on an observed cube and date/index-shift its output.

    Args:
        pr_obs: ``(T_obs, rows, cols)`` daily rain in mm, through the as-of day.
        search_start: onset search opening index per pixel (days since
            ``start_date``), array or scalar.
        season_end: last index an onset candidate may fall on.
        params: :class:`geocif.phenology.core.OnsetParams`.
        start_date: calendar date of index 0 of ``pr_obs``.
        planting_offset: float32 ``(rows, cols)`` days from ``start_date`` to
            the pixel's planting start, NaN where the pixel has no calendar
            (:func:`geocif.phenology.climatology.planting_offset`).
        pr_fcst: optional ``(F, rows, cols)`` forecast rain for the F days after
            the as-of day.

    Returns:
        dict of pixel-shaped arrays -- int8 ``state``; float32 ``onset_idx``
        (index), ``onset_date`` (days since 1970-01-01), ``onset_days`` and
        ``as_of_days`` (days since the pixel's planting start), ``rain_10d``,
        ``rain_30d`` (mm), ``dry_run_now``, ``n_false_starts`` (counts, NaN
        where the state is nodata) and ``fcst_trigger_days`` (days from the
        as-of day).
    """
    pr = np.asarray(pr_obs, dtype=np.float32)
    n_obs = int(pr.shape[0])
    if n_obs < 1:
        raise ValueError("observed_layers needs at least one observed day")

    state_out = core.onset_state(pr, search_start, season_end, params, pr_fcst=pr_fcst)
    state = np.asarray(state_out["state"], dtype=np.int8)
    nodata = state == core.NODATA_STATUS

    offset = np.asarray(planting_offset, dtype=np.float32)
    onset_idx = np.asarray(state_out["onset_idx"], dtype=np.float32)
    day0 = float((np.datetime64(start_date, "D") - EPOCH).astype("int64"))

    as_of_idx = float(n_obs - 1)
    onset_days = (onset_idx - offset).astype(np.float32)
    as_of_days = (as_of_idx - offset).astype(np.float32)

    counts_nan = np.where(nodata, np.nan, 1.0).astype(np.float32)
    fcst_idx = np.asarray(state_out["fcst_trigger_idx"], dtype=np.float32)

    # Rain totals are NaN, not 0, where there is nothing to total.
    #
    # Two ways a 0.0 here becomes a fabricated record drought downstream:
    # (a) a pixel with no CHIRPS at all -- core.onset_state sums the
    #     NaN-filled-with-zero slab, so it returns 0.0 mm rather than "unknown",
    #     and rain_percentile then ranks that 0.0 at the driest end;
    # (b) a cube shorter than the window -- core._trailing_sum takes the last
    #     min(window, T) days, so on the day a season opens a 10-day cube yields
    #     a "30-day" total of 10 days' rain, compared against full 30-day
    #     climatological totals. A season raining at exactly the climatological
    #     rate would publish as the driest on record, at the moment the product
    #     is most likely to be read.
    def _rain(key: str, window: int) -> np.ndarray:
        values = np.asarray(state_out[key], dtype=np.float32)
        if n_obs < window:
            return np.full(values.shape, np.nan, dtype=np.float32)
        return (values * counts_nan).astype(np.float32)

    return {
        "state": state,
        "onset_idx": onset_idx,
        "onset_date": (onset_idx + day0).astype(np.float32),
        "onset_days": onset_days,
        "as_of_days": as_of_days,
        "rain_10d": _rain("rain_10d", 10),
        "rain_30d": _rain("rain_30d", RAIN_PERCENTILE_WINDOW),
        "dry_run_now": (
            np.asarray(state_out["dry_run_now"], dtype=np.float32) * counts_nan
        ).astype(np.float32),
        "n_false_starts": (
            np.asarray(state_out["n_false_starts"], dtype=np.float32) * counts_nan
        ).astype(np.float32),
        "fcst_trigger_days": (fcst_idx - as_of_idx).astype(np.float32),
    }


def climatology_layers(
    state: np.ndarray,
    onset_days: np.ndarray,
    as_of_days: np.ndarray,
    clim: Optional[dict],
    horizons: Sequence[int] = DEFAULT_HORIZONS,
    min_years: int = 20,
) -> dict:
    """Compare this season against the cached climatology.

    Args:
        state: int8 :class:`~geocif.phenology.core.SeasonState` codes.
        onset_days: this season's onset in days since the pixel's planting start
            (NaN where onset is not confirmed).
        as_of_days: the as-of day in days since the pixel's planting start.
        clim: the ``arrays`` dict from
            :func:`geocif.phenology.climatology.load_climatology`
            (``onset_median``, ``onset_stack``, ``false_start_rate``), or
            ``None`` -- in which case every layer here is all-NaN.
        horizons: conditional-probability horizons in days.
        min_years: a pixel needs this many usable years before a climatological
            answer is published (years).

    Returns:
        float32 dict: ``onset_anomaly_days`` (onset minus median, **positive =
        LATE**), ``onset_percentile`` (0..1), ``days_past_median`` (days, only
        on ``NOT_STARTED`` pixels), ``p_onset_{h}d`` for each horizon (0..1,
        NaN on CONFIRMED pixels and wherever the cache has too few years) and
        ``false_start_rate`` (0..1).
    """
    codes = np.asarray(state)
    shape = codes.shape
    nan = np.full(shape, np.nan, dtype=np.float32)
    out: dict[str, np.ndarray] = {
        "onset_anomaly_days": nan.copy(),
        "onset_percentile": nan.copy(),
        "days_past_median": nan.copy(),
        "false_start_rate": nan.copy(),
    }
    for horizon in horizons:
        out[f"p_onset_{int(horizon)}d"] = nan.copy()
    if not clim:
        logger.info("climatology_layers: no cached climatology; anomaly layers stay NaN")
        return out

    median = np.asarray(clim.get("onset_median", nan), dtype=np.float32)
    if median.shape != shape:
        logger.warning(
            f"climatology_layers: cache grid {median.shape} != monitor grid {shape}; "
            f"dropping the climatological layers"
        )
        return out

    onset = np.asarray(onset_days, dtype=np.float32)
    as_of = np.asarray(as_of_days, dtype=np.float32)
    out["onset_anomaly_days"] = (onset - median).astype(np.float32)
    out["days_past_median"] = np.where(
        codes == int(core.SeasonState.NOT_STARTED), as_of - median, np.nan
    ).astype(np.float32)

    rate = clim.get("false_start_rate")
    if rate is not None and np.shape(rate) == shape:
        out["false_start_rate"] = np.asarray(rate, dtype=np.float32)

    stack = clim.get("onset_stack")
    if stack is None or np.shape(stack)[1:] != shape:
        logger.warning("climatology_layers: no usable onset stack; percentile and p_onset stay NaN")
        return out

    stack = np.asarray(stack, dtype=np.float32)
    out["onset_percentile"] = core.onset_percentile(
        stack, onset, min_valid_years=int(min_years)
    ).astype(np.float32)
    # "P(onset arrives in the next h days | it has not arrived yet)" is only a
    # statement about a pixel that is genuinely still waiting. It is meaningless
    # where onset already happened (CONFIRMED), where the season has closed
    # without one (NO_ONSET -- the as-of day is already past season end plus the
    # validation tail), and where there are no observations at all (the nodata
    # sentinel, which still has a calendar and so still has a finite as_of).
    # Publishing a confident 0.75 for a pixel with no data is the worst of the
    # three, because nothing on the map distinguishes it.
    undefined = (
        (codes == int(core.SeasonState.CONFIRMED))
        | (codes == int(core.SeasonState.NO_ONSET))
        | (codes == core.NODATA_STATUS)
    )
    for horizon in horizons:
        p = core.conditional_onset_probability(
            stack, as_of, int(horizon), min_years=int(min_years)
        )
        out[f"p_onset_{int(horizon)}d"] = np.where(undefined, np.nan, p).astype(np.float32)
    return out


def rain_percentile(stack: np.ndarray, current: np.ndarray, min_years: int = 5) -> np.ndarray:
    """Percentile (0..100) of ``current`` within a ``(Y, rows, cols)`` stack.

    Args:
        stack: the same accumulation window in each climatology year, mm.
        current: this season's accumulation at the as-of day, mm.
        min_years: minimum usable years, below which the answer is NaN.

    Returns:
        float32 ``(rows, cols)``: the share of years whose total was at or below
        ``current``, times 100. ``geocif.viz.phenology_maps.rain_percentile_map``
        draws 0..100, which is why this is not left as a 0..1 share.
    """
    if stack is None or np.size(stack) == 0:
        return np.full(np.shape(current), np.nan, dtype=np.float32)
    # onset_percentile is units-agnostic: "share of valid years at or below the
    # given value". Reused rather than re-implemented.
    share = core.onset_percentile(
        np.asarray(stack, dtype=np.float32),
        np.asarray(current, dtype=np.float32),
        min_valid_years=int(min_years),
    )
    return (share.astype(np.float32) * 100.0).astype(np.float32)


# ---------------------------------------------------------------------------
# 8.3 I/O helpers
# ---------------------------------------------------------------------------
def _shift_year(day: _dt.date, years: int) -> _dt.date:
    """``day`` moved by whole years, Feb 29 falling back to Feb 28."""
    year = day.year + int(years)
    try:
        return day.replace(year=year)
    except ValueError:
        return _dt.date(year, day.month, day.day - 1)


def rain_window_stack(
    parser,
    window: Window,
    as_of: _dt.date,
    harvest_year: int,
    years: Sequence[int],
    days: int = RAIN_PERCENTILE_WINDOW,
    n_threads: int = 8,
) -> tuple[np.ndarray, list[int]]:
    """Trailing rainfall totals over the SAME calendar window in past seasons.

    The anchor moves with the season, not with the calendar year: the as-of day
    sits ``as_of.year - harvest_year`` years from the harvest year, so harvest
    year ``y`` of the climatology is compared at ``as_of`` shifted by
    ``y - harvest_year`` years. For a cross-year season monitored in November of
    harvest year 2026 that means November of ``y - 1``, which is the same point
    of the season rather than the same point of the year.

    Args:
        parser: the 4-file config parser.
        window: window on the global grid.
        as_of: the data-through date.
        harvest_year: harvest year of the season being monitored.
        years: harvest years of the climatology.
        days: accumulation length (days).
        n_threads: pool size handed to :func:`geocif.phenology.inputs.read_cube`.

    Returns:
        ``(stack, years_used)`` -- float32 ``(Y, rows, cols)`` totals in mm (NaN
        rain contributes 0, a year with no file at all is all-NaN) and the
        harvest years in stack order.
    """
    rows, cols = int(window.height), int(window.width)
    stack: list[np.ndarray] = []
    used: list[int] = []
    for year in sorted({int(y) for y in years}):
        anchor = _shift_year(as_of, int(year) - int(harvest_year))
        dates = [anchor - _dt.timedelta(days=i) for i in range(int(days) - 1, -1, -1)]
        cube, missing = inputs.read_cube(parser, "chirps", dates, window, n_threads=n_threads)
        if len(missing) == len(dates):
            logger.info(f"rain_window_stack: no CHIRPS at all for {anchor}; year {year} dropped")
            stack.append(np.full((rows, cols), np.nan, dtype=np.float32))
        else:
            stack.append(np.nan_to_num(cube, nan=0.0).sum(axis=0).astype(np.float32))
        used.append(int(year))
    if not stack:
        return np.zeros((0, rows, cols), dtype=np.float32), []
    logger.info(
        f"rain_window_stack: {len(used)} year(s) of {int(days)}-day totals ending "
        f"{as_of} (season-aligned)"
    )
    return np.stack(stack).astype(np.float32), used


def _forecast_slab(
    parser,
    window: Window,
    as_of: _dt.date,
    forecast_days: int,
    issue_lookback_days: int = 2,
) -> tuple[Optional[np.ndarray], Optional[_dt.date], list[_dt.date]]:
    """Newest CHIRPS-GEFS forecast for the days strictly after ``as_of``.

    The cube must start on ``as_of + 1`` once past days are dropped; a gap makes
    the forecast unusable (index ``T_obs`` of the concatenated series would not
    be tomorrow) and it is skipped with a warning.

    Returns:
        ``(cube, issue_date, dates)`` -- float32 ``(F, rows, cols)`` mm/day, or
        ``(None, issue_date_or_None, [])`` when there is nothing usable.
    """
    not_before = as_of - _dt.timedelta(days=int(issue_lookback_days))
    issue = inputs.latest_forecast_issue(parser, not_before=not_before)
    if issue is None:
        logger.info(f"no CHIRPS-GEFS issue on or after {not_before}; running without a forecast")
        return None, None, []
    read = inputs.read_forecast_cube(parser, issue, window)
    if read is None:
        return None, issue, []
    cube, dates = read
    keep = [i for i, day in enumerate(dates) if day > as_of]
    if not keep:
        logger.info(f"CHIRPS-GEFS issue {issue} holds no day after {as_of}")
        return None, issue, []
    first = dates[keep[0]]
    if first != as_of + _dt.timedelta(days=1):
        logger.warning(
            f"CHIRPS-GEFS issue {issue} starts at {first}, not {as_of + _dt.timedelta(days=1)}; "
            f"skipping the forecast rather than misaligning it"
        )
        return None, issue, []
    keep = keep[: max(0, int(forecast_days))]
    return cube[keep].astype(np.float32), issue, [dates[i] for i in keep]


# ---------------------------------------------------------------------------
# 8.4 One season
# ---------------------------------------------------------------------------
def monitor_season(
    parser,
    country: str,
    crop: str,
    season: int,
    harvest_year: int,
    as_of: _dt.date,
    params: climatology.ClimatologyParams,
    clim: Optional[dict] = None,
    clim_years: Optional[Sequence[int]] = None,
    use_forecast: bool = True,
    forecast_days: int = 16,
    bbox_buffer: float = 0.5,
    horizons: Sequence[int] = DEFAULT_HORIZONS,
    n_threads: int = 8,
) -> dict:
    """Score one (country, crop, season, harvest year) as of ``as_of``.

    Args:
        parser: the 4-file config parser.
        country: country slug, e.g. ``"kenya"``.
        crop: crop slug, e.g. ``"maize"``.
        season: 1-based season number.
        harvest_year: the year that labels the season.
        as_of: the data-through date -- the last CHIRPS day on disk. The
            observed cube ends here and every output is stamped with it.
        params: :class:`geocif.phenology.climatology.ClimatologyParams`; only the
            onset parameters and ``search_start_days_before_planting`` /
            ``min_valid_years`` are used (cessation is a climatology concern).
        clim: ``arrays`` from
            :func:`geocif.phenology.climatology.load_climatology`, or ``None``.
        clim_years: harvest years behind ``clim``, used for the rainfall
            percentile; ``None`` skips ``rain_30d_percentile``.
        use_forecast: read the newest CHIRPS-GEFS issue and report
            ``fcst_trigger_days``.
        forecast_days: how many forecast days to keep (days).
        bbox_buffer: country bbox buffer in degrees; must match the buffer the
            climatology cache was built on (its default) or the cached layers
            are dropped.
        horizons: conditional-probability horizons (days).
        n_threads: raster read threads.

    Returns:
        dict with ``layers`` (every name in :data:`MONITOR_LAYERS`, float32 with
        NaN except int8 ``state``), the grid (``transform``, ``window``,
        ``shape``, ``lon``, ``lat``), the weights (``crop_fraction``,
        ``pixel_area_km2``, ``weight`` = fraction x area in km^2), the zone
        rasters (``id_grid``, ``lookup``, ``zone_id``, ``zone_lookup``) and
        ``meta`` (dates, missing days, forecast issue, counts).

    Raises:
        ValueError: when no calendar zone carries this season, or the search
            window has not opened by ``as_of``.
    """
    bbox = inputs.country_bbox(parser, country, buffer_deg=float(bbox_buffer))
    window, transform, shape = inputs.window_for_bbox(bbox)
    lon, lat = inputs.pixel_centres(transform, shape)

    zones_gdf, flags_by_season = inputs.load_calendar_zones(parser, country, crop)
    calendar = inputs.rasterize_calendar(
        zones_gdf, flags_by_season, int(season), int(harvest_year), transform, shape
    )
    bounds = season_bounds(flags_by_season, int(season), int(harvest_year))
    if bounds is None:
        raise ValueError(
            f"{country}/{crop} s{season} harvest {harvest_year}: no calendar zone carries "
            f"this season"
        )
    planting, harvest = bounds
    start_date = planting - _dt.timedelta(days=int(params.search_start_days_before_planting))
    if as_of < start_date:
        raise ValueError(
            f"{country}/{crop} s{season} harvest {harvest_year}: the search opens {start_date}, "
            f"after the as-of date {as_of}"
        )

    dates = [start_date + _dt.timedelta(days=i) for i in range((as_of - start_date).days + 1)]
    cube, missing = inputs.read_cube(parser, "chirps", dates, window, n_threads=n_threads)
    n_obs = len(dates)
    logger.info(
        f"{country}/{crop} s{season} {harvest_year}: {n_obs} observed day(s) "
        f"{start_date} -> {as_of}, {len(missing)} missing"
    )

    search_start, season_end, _search_end = climatology.season_indices(
        calendar, start_date, n_obs, params
    )
    offset = climatology.planting_offset(calendar, start_date)

    fcst_cube: Optional[np.ndarray] = None
    issue: Optional[_dt.date] = None
    fcst_dates: list[_dt.date] = []
    if use_forecast:
        fcst_cube, issue, fcst_dates = _forecast_slab(
            parser, window, as_of, int(forecast_days)
        )

    layers = observed_layers(
        cube,
        search_start,
        season_end,
        params.onset,
        start_date,
        offset,
        pr_fcst=fcst_cube,
    )
    as_of_days = layers.pop("as_of_days")
    layers.update(
        climatology_layers(
            layers["state"],
            layers["onset_days"],
            as_of_days,
            clim,
            horizons=horizons,
            min_years=int(params.min_valid_years),
        )
    )

    if clim_years:
        stack, years_used = rain_window_stack(
            parser,
            window,
            as_of,
            int(harvest_year),
            clim_years,
            days=RAIN_PERCENTILE_WINDOW,
            n_threads=n_threads,
        )
        layers[f"rain_{RAIN_PERCENTILE_WINDOW}d_percentile"] = rain_percentile(
            stack,
            layers[f"rain_{RAIN_PERCENTILE_WINDOW}d"],
            min_years=int(params.min_valid_years),
        )
    else:
        years_used = []
        layers[f"rain_{RAIN_PERCENTILE_WINDOW}d_percentile"] = np.full(
            shape, np.nan, dtype=np.float32
        )

    fraction = inputs.read_crop_fraction(parser, country, crop, window, year=int(harvest_year))
    area = inputs.pixel_area_km2(lat)
    weight = (fraction * area[:, None]).astype(np.float32)
    id_grid, lookup = inputs.rasterize_admin(parser, country, transform, shape)
    zone_lookup = pd.DataFrame(
        {
            "id": np.arange(1, len(calendar.zone_names) + 1, dtype=np.int32),
            "ADM1_NAME": [str(name) for name in calendar.zone_names],
        }
    )

    for name in MONITOR_LAYERS:
        layers.setdefault(name, np.full(shape, np.nan, dtype=np.float32))

    meta = {
        "country": country,
        "crop": crop,
        "season": int(season),
        "harvest_year": int(harvest_year),
        "as_of": as_of,
        "data_through": as_of.isoformat(),
        "start_date": start_date.isoformat(),
        "planting_start": planting.isoformat(),
        "harvest_end": harvest.isoformat(),
        "n_obs_days": int(n_obs),
        "n_missing_days": int(len(missing)),
        "missing_days": [d.isoformat() for d in missing],
        "forecast_issue": issue.isoformat() if issue else None,
        "forecast_days": len(fcst_dates),
        "climatology_years": [int(y) for y in (clim_years or [])],
        "rain_percentile_years": years_used,
        "bbox": [float(b) for b in bbox],
        "shape": [int(shape[0]), int(shape[1])],
    }
    counts = {
        member.name.lower(): int((layers["state"] == int(member)).sum())
        for member in core.SeasonState
    }
    logger.info(
        f"{country}/{crop} s{season} {harvest_year} as of {as_of}: "
        + ", ".join(f"{k}={v}" for k, v in counts.items())
    )

    return {
        "layers": layers,
        "meta": meta,
        "state_counts": counts,
        "transform": transform,
        "window": window,
        "shape": shape,
        "lon": lon,
        "lat": lat,
        "crop_fraction": fraction,
        "pixel_area_km2": area,
        "weight": weight,
        "id_grid": id_grid,
        "lookup": lookup,
        "zone_id": calendar.zone_id.astype(np.int32),
        "zone_lookup": zone_lookup,
        "calendar": calendar,
    }


# ---------------------------------------------------------------------------
# 8.5 Tables
# ---------------------------------------------------------------------------
def status_area_frame(result: dict) -> pd.DataFrame:
    """Cropland-area share of every season state, per Admin 1.

    Args:
        result: the dict :func:`monitor_season` returned.

    Returns:
        :func:`geocif.phenology.outputs.status_area_table` plus the identity
        columns (``country``, ``crop``, ``season``, ``harvest_year``,
        ``data_through``). Shares are of the CROP AREA (fraction x km^2), not of
        the pixel count, and sum to 1 per unit over the valid weight.
    """
    meta = result["meta"]
    table = outputs.status_area_table(
        result["layers"]["state"], result["weight"], result["id_grid"], result["lookup"]
    )
    return _stamp(table, meta)


def onset_summary_frame(result: dict) -> pd.DataFrame:
    """Weighted onset summary by Admin 1 AND by calendar zone.

    One row per unit per zone type, with the crop-area weighted mean, weighted
    median and valid-weight share of every layer in :data:`SUMMARY_LAYERS`
    (anomaly and days-past-median in days, positive = late; probabilities 0..1).

    Args:
        result: the dict :func:`monitor_season` returned.

    Returns:
        A DataFrame with ``zone_type`` (``admin_1`` or ``calendar_zone``),
        ``unit_id``, ``unit_name``, ``display_name``, ``{layer}_weighted_mean``,
        ``{layer}_weighted_median``, ``{layer}_valid_weight_share``,
        ``total_weight_km2`` and the identity columns.
    """
    meta = result["meta"]
    frames: list[pd.DataFrame] = []
    for zone_type, grid, lookup, name_col in (
        ("admin_1", result["id_grid"], result["lookup"], "ADM1_NAME"),
        ("calendar_zone", result["zone_id"], result["zone_lookup"], "ADM1_NAME"),
    ):
        if lookup is None or lookup.empty:
            continue
        merged: Optional[pd.DataFrame] = None
        for layer in SUMMARY_LAYERS:
            table = outputs.zonal_table(
                result["layers"][layer], result["weight"], grid, lookup
            )
            keep = table[
                ["id", name_col, outputs.DISPLAY_COL, "weighted_mean", "weighted_median",
                 "valid_weight_share", "total_weight_km2"]
            ].rename(
                columns={
                    "weighted_mean": f"{layer}_weighted_mean",
                    "weighted_median": f"{layer}_weighted_median",
                    "valid_weight_share": f"{layer}_valid_weight_share",
                }
            )
            if merged is None:
                merged = keep
            else:
                merged = merged.merge(
                    keep.drop(columns=[name_col, outputs.DISPLAY_COL, "total_weight_km2"]),
                    on="id",
                    how="left",
                )
        if merged is None:
            continue
        merged = merged.rename(columns={"id": "unit_id", name_col: "unit_name"})
        merged.insert(0, "zone_type", zone_type)
        frames.append(merged)
    if not frames:
        return _stamp(pd.DataFrame(columns=["zone_type", "unit_id", "unit_name"]), meta)
    return _stamp(pd.concat(frames, ignore_index=True), meta)


def _stamp(table: pd.DataFrame, meta: dict) -> pd.DataFrame:
    """Prepend the identity + data-vintage columns every table carries."""
    out = table.copy()
    for col, value in (
        ("data_through", meta["data_through"]),
        ("harvest_year", meta["harvest_year"]),
        ("season", meta["season"]),
        ("crop", meta["crop"]),
        ("country", meta["country"]),
    ):
        out.insert(0, col, value)
    return out


__all__ = [
    "EPOCH",
    "MONITOR_LAYERS",
    "DEFAULT_HORIZONS",
    "RAIN_WINDOWS",
    "RAIN_PERCENTILE_WINDOW",
    "SUMMARY_LAYERS",
    "ActiveSeason",
    "crops_for",
    "seasons_for",
    "season_bounds",
    "active_seasons",
    "observed_layers",
    "climatology_layers",
    "rain_percentile",
    "rain_window_stack",
    "monitor_season",
    "status_area_frame",
    "onset_summary_frame",
]
