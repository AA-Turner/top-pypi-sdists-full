# -*- coding: utf-8 -*-
"""Operational season-onset monitor runner (DESIGN.md sections 8 and 8.1).

One call scores every season that is running right now and publishes it::

    from geocif import season_monitor
    season_monitor.run([
        "/gpfs/data1/cmongp1/GEO/config/geocif/geobase.txt",
        "/gpfs/data1/cmongp1/GEO/config/geocif/countries.txt",
        "/gpfs/data1/cmongp1/GEO/config/geocif/crops.txt",
        "/gpfs/data1/cmongp1/GEO/config/geocif/geocif.txt",
    ])

Stages, in order:

1. ``refresh_inputs`` -- pull the newest CHIRPS and CHIRPS-GEFS (skipped when
   ``refresh_datasets`` is empty; never fatal).
2. As-of date -- the last CHIRPS day actually on disk. Every raster, map title
   and table states it.
3. Active seasons -- every configured (country, crop, season) whose search
   window has opened and whose harvest + validation window has not closed.
4. Per season: ensure the climatology cache (a hash hit is a no-op), score the
   season, write the rasters, render the maps, write the tables, write the
   ``lookup_plots_csvs.csv`` manifest.

Every combination runs inside its own ``try/except``: a failure is logged with
its traceback and the next combination still runs. ``os._exit`` is never called.

Output tree (``MMMM_DD_YYYY`` = the run date)::

    {PATHS:dir_output}/{project_name}/ml/analysis/{MMMM_DD_YYYY}/season_monitor/
        {country}/{crop}/s{season}_hy{harvest_year}/
            rasters/{layer}_{country}_{crop}_s{season}_hy{YEAR}_asof{YYYYMMDD}.tif
            maps/{layer}_..._hy{YEAR}_asof{YYYYMMDD}.png  + lookup_plots_csvs.csv
            csvs/{layer}_..._hy{YEAR}_asof{YYYYMMDD}.csv  + lookup_plots_csvs.csv
                 status_area_..._asof{YYYYMMDD}.csv
                 onset_summary_..._asof{YYYYMMDD}.csv
            climatology/maps/  + csvs/    the 1981-2025 reference set

The harvest year is in the path and the name because two harvest years of one
season can be active on the same day (see :func:`file_stem`).

Config: everything lives in an optional ``[SEASON_MONITOR]`` section (see
:data:`DEFAULTS` and :func:`read_config`); the section does not have to exist.
Keyword arguments to :func:`run` override it.
"""

from __future__ import annotations

import argparse
import ast
import configparser
import datetime as _dt
import logging
import traceback
from pathlib import Path
from typing import Any, Optional, Sequence

import numpy as np
import pandas as pd

from geocif.phenology import climatology, core, inputs, monitor, outputs
from geocif.phenology.refresh import refresh_inputs
from geocif.viz import phenology_maps

logger = logging.getLogger(__name__)

#: The ``[SEASON_MONITOR]`` contract (DESIGN section 8.1). Every key is
#: optional; these defaults produce a working run with no section at all.
#: ``countries = []`` means "inherit ``[DEFAULT] countries``".
DEFAULTS: dict[str, Any] = {
    "precip_threshold": 20.0,
    "window_days": 3,
    "dry_spell_days": 10,
    "dry_day_threshold": 1.0,
    "validation_days": 30,
    "search_start_days_before_planting": 30,
    "soil_whc": 100.0,
    "min_season_days": 60,
    "empty_persist_days": 5,
    "cessation_grace_days": 60,
    "forecast_days": 16,
    "use_forecast": True,
    "refresh_datasets": ["CHIRPS", "CHIRPS-GEFS"],
    "bbox_buffer": 0.5,
    "mask_to_cropland": True,
    "climatology_start_year": 1981,
    "climatology_end_year": 2025,
    "min_valid_years": 20,
    "rebuild_climatology": False,
    "n_workers": 8,
    "countries": [],
    # Per-zone start-of-season report over a window around the planting date.
    "zone_report": True,
    "zone_report_window_days": 30,
}

#: Per-crop override prefix: ``min_season_days_maize = 90``.
CROP_OVERRIDE_PREFIX: str = "min_season_days_"

# ``[SEASON_MONITOR] seasons_<country> = [1, 2]`` monitors a secondary season
# without touching the shared ``[country] seasons``, which the CID / extract /
# merge pipelines also read and which requires a merged CSV per season. This
# product reads rasters and the crop calendar directly, so it needs no such file
# -- Kenya's short rains being the case that motivated it.
SEASON_OVERRIDE_PREFIX: str = "seasons_"

#: Extra keyword arguments :func:`run` accepts that are not config keys.
RUN_ONLY_KWARGS: tuple[str, ...] = ("as_of",)

#: Sections ``_get`` consults, in order.
CONFIG_SECTIONS: tuple[str, ...] = ("SEASON_MONITOR", "DEFAULT")

#: Product directory under the date-stamped analysis folder.
PRODUCT: str = "season_monitor"

#: Layers rendered as maps, in render order.
MAP_LAYERS: tuple[str, ...] = (
    "onset_anomaly_days",
    "days_past_median",
    "p_onset_28d",
    "rain_30d_percentile",
    "fcst_trigger_days",
)


# ---------------------------------------------------------------------------
# config
# ---------------------------------------------------------------------------
def _parsers(path_config_files: Sequence[Any]):
    """The interpolating parser plus the set of options each section OWNS.

    ``configparser`` exposes every ``[DEFAULT]`` key from every section, so
    ``parser.has_option("SEASON_MONITOR", "start_year")`` is True for a key that
    is really a ``[DEFAULT]`` key of geocif.txt. The probe re-parses with a
    default-section name no file uses, which turns ``[DEFAULT]`` into an ordinary
    section and makes ownership answerable. Values still come from the
    interpolating parser (``dir_output = ${dir_base}/outputs`` must resolve).
    """
    paths = [str(p) for p in path_config_files]
    parser = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        inline_comment_prefixes=(";",),
    )
    parser.read(paths)
    probe = configparser.ConfigParser(
        default_section="__season_monitor_no_default__",
        interpolation=None,
        inline_comment_prefixes=(";",),
    )
    probe.read(paths)
    own = {sec: set(probe.options(sec)) for sec in probe.sections()}
    # The real [DEFAULT] is an ordinary section to the probe, so its own keys
    # are readable without the ones it lends to every other section.
    own["DEFAULT"] = set(probe.options("DEFAULT")) if probe.has_section("DEFAULT") else set()
    return parser, own


def _coerce(raw: str, default: Any) -> Any:
    """Turn a config string into the type of ``default`` (lists via literal_eval)."""
    text = str(raw).strip()
    if isinstance(default, bool):
        return text.lower() in ("1", "true", "yes", "on")
    if isinstance(default, (list, tuple)):
        try:
            value = ast.literal_eval(text)
        except (ValueError, SyntaxError):
            return [text] if text else list(default)
        if isinstance(value, (list, tuple, set)):
            return list(value)
        return [value]
    if isinstance(default, float):
        return float(text)
    if isinstance(default, int):
        return int(float(text))
    return text


def _get(
    parser,
    own: dict,
    option: str,
    default: Any,
    sections: Sequence[str] = CONFIG_SECTIONS,
) -> Any:
    """First section that LITERALLY carries ``option``, coerced; else ``default``.

    Args:
        parser: the interpolating parser.
        own: section -> set of options that section literally declares.
        option: config key.
        default: value and type template.
        sections: search order, ``("SEASON_MONITOR", "DEFAULT")`` by default.

    Returns:
        The configured value, or ``default``.
    """
    for section in sections:
        if option in own.get(section, ()):
            try:
                return _coerce(parser.get(section, option), default)
            except (configparser.Error, ValueError) as exc:
                logger.warning(f"[{section}] {option} unreadable ({exc}); using {default!r}")
                return default
    return default


def read_config(path_config_files: Sequence[Any], **overrides: Any) -> dict:
    """Parse the 4-file config list into every setting this runner needs.

    ``[SEASON_MONITOR]`` (all optional, defaults in :data:`DEFAULTS`)::

        [SEASON_MONITOR]
        precip_threshold = 20.0
        window_days = 3
        dry_spell_days = 10
        dry_day_threshold = 1.0
        validation_days = 30
        search_start_days_before_planting = 30
        soil_whc = 100.0
        min_season_days = 60          ; per-crop: min_season_days_maize = 90
        empty_persist_days = 5
        cessation_grace_days = 60
        forecast_days = 16
        use_forecast = True
        refresh_datasets = ['CHIRPS', 'CHIRPS-GEFS']
        bbox_buffer = 0.5
        mask_to_cropland = True
        climatology_start_year = 1981
        climatology_end_year = 2025
        min_valid_years = 20
        rebuild_climatology = False
        n_workers = 8
        countries = ['kenya']         ; unset -> [DEFAULT] countries
        seasons_kenya = [1, 2]        ; per-country; unset -> [country] seasons

    Args:
        path_config_files: the geobase / countries / crops / geocif list.
        **overrides: any key of :data:`DEFAULTS`, plus ``as_of`` (a ``date`` or
            ``YYYY-MM-DD`` string) -- these win over the file.

    Returns:
        dict of every setting plus ``parser``, ``config_files``, ``dir_output``,
        ``project``, ``crop_min_season_days`` and ``as_of``.

    Raises:
        TypeError: on an unknown override key.
    """
    unknown = set(overrides) - set(DEFAULTS) - set(RUN_ONLY_KWARGS)
    if unknown:
        raise TypeError(
            f"season_monitor.run got unexpected keyword argument(s) {sorted(unknown)}; "
            f"valid keys are {sorted(set(DEFAULTS) | set(RUN_ONLY_KWARGS))}"
        )
    parser, own = _parsers(path_config_files)

    cfg: dict[str, Any] = {}
    for key, default in DEFAULTS.items():
        cfg[key] = _get(parser, own, key, default)
    for key, value in overrides.items():
        if key in DEFAULTS:
            cfg[key] = value

    crop_overrides: dict[str, int] = {}
    season_overrides: dict[str, list] = {}
    for option in sorted(own.get("SEASON_MONITOR", ())):
        if option.startswith(CROP_OVERRIDE_PREFIX) and option != CROP_OVERRIDE_PREFIX:
            crop = option[len(CROP_OVERRIDE_PREFIX):]
            crop_overrides[crop] = int(float(parser.get("SEASON_MONITOR", option)))
        elif option.startswith(SEASON_OVERRIDE_PREFIX) and option != SEASON_OVERRIDE_PREFIX:
            country = option[len(SEASON_OVERRIDE_PREFIX):]
            raw = parser.get("SEASON_MONITOR", option)
            try:
                value = ast.literal_eval(raw)
            except (ValueError, SyntaxError):
                logger.warning(
                    f"[SEASON_MONITOR] {option}={raw!r} is not a list; ignoring"
                )
                continue
            if not isinstance(value, (list, tuple)):
                value = [value]
            season_overrides[country] = [int(v) for v in value]
    cfg["crop_min_season_days"] = crop_overrides
    cfg["country_seasons"] = season_overrides

    as_of = overrides.get("as_of")
    if isinstance(as_of, str):
        as_of = _dt.date.fromisoformat(as_of)
    if isinstance(as_of, _dt.datetime):
        as_of = as_of.date()
    cfg["as_of"] = as_of

    cfg["parser"] = parser
    cfg["config_files"] = [str(p) for p in path_config_files]
    cfg["dir_output"] = Path(parser.get("PATHS", "dir_output"))
    cfg["dir_intermed"] = Path(parser.get("PATHS", "dir_intermed"))
    cfg["project"] = parser.get("DEFAULT", "project_name", fallback="geocif")
    if not cfg["countries"]:
        cfg["countries"] = [
            str(c) for c in monitor._literal_list(parser, "DEFAULT", "countries", [])
        ]
    return cfg


def climatology_params(cfg: dict, crop: str) -> climatology.ClimatologyParams:
    """Build :class:`~geocif.phenology.climatology.ClimatologyParams` from ``cfg``.

    Mirrors ``ClimatologyParams.from_parser`` but reads the already-resolved
    ``cfg`` so that keyword overrides handed to :func:`run` reach the
    climatology build too (``from_parser`` would re-read the file and ignore
    them). ``min_season_days_<crop>`` overrides ``min_season_days``.
    """
    return climatology.ClimatologyParams(
        onset=core.OnsetParams(
            precip_threshold=float(cfg["precip_threshold"]),
            window_days=int(cfg["window_days"]),
            dry_spell_days=int(cfg["dry_spell_days"]),
            dry_day_threshold=float(cfg["dry_day_threshold"]),
            validation_days=int(cfg["validation_days"]),
        ),
        cessation=core.CessationParams(
            soil_whc=float(cfg["soil_whc"]),
            min_season_days=int(cfg["crop_min_season_days"].get(crop, cfg["min_season_days"])),
            empty_persist_days=int(cfg["empty_persist_days"]),
        ),
        search_start_days_before_planting=int(cfg["search_start_days_before_planting"]),
        cessation_grace_days=int(cfg["cessation_grace_days"]),
        min_valid_years=int(cfg["min_valid_years"]),
    )


# ---------------------------------------------------------------------------
# output tree
# ---------------------------------------------------------------------------
def analysis_stamp(day: Optional[_dt.date] = None) -> str:
    """Date-stamped analysis folder name, ``September_16_2026``."""
    return (day or _dt.date.today()).strftime("%B_%d_%Y")


def output_dirs(
    cfg: dict, season: monitor.ActiveSeason, stamp: Optional[str] = None
) -> dict[str, Path]:
    """Create and return the ``rasters`` / ``maps`` / ``csvs`` directories.

    Args:
        cfg: the dict :func:`read_config` returned.
        season: the combination being written.
        stamp: analysis folder name; defaults to today's.

    Returns:
        ``{"root": ..., "rasters": ..., "maps": ..., "csvs": ...}``.
    """
    root = (
        Path(cfg["dir_output"])
        / cfg["project"]
        / "ml"
        / "analysis"
        / (stamp or analysis_stamp())
        / PRODUCT
        / season.country
        / season.crop
        # Two harvest years of one season can be active on the same day (see
        # file_stem), so the year is part of the directory as well as the name.
        / f"s{int(season.season)}_hy{int(season.harvest_year)}"
    )
    dirs = {
        "root": root,
        "rasters": root / "rasters",
        "maps": root / "maps",
        "csvs": root / "csvs",
        # The climatology set gets its own {maps,csvs} pair because
        # phenology_maps writes lookup_plots_csvs.csv into whichever directory
        # it is handed: rendering both sets into one directory would leave the
        # second manifest overwriting the first.
        "clim_maps": root / "climatology" / "maps",
        "clim_csvs": root / "climatology" / "csvs",
        "zone_plots": root / "zones" / "plots",
        "zone_csvs": root / "zones" / "csvs",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def file_stem(layer: str, season: monitor.ActiveSeason, as_of: _dt.date) -> str:
    """``{layer}_{country}_{crop}_s{season}_hy{YEAR}_asof{YYYYMMDD}``.

    The harvest year is part of the name because two of them can be active on
    one as-of date: :func:`geocif.phenology.monitor.active_seasons` keeps year Y
    alive until ``max(harvest) + validation_days`` and opens Y+1 at
    ``min(planting) - search_start_days_before_planting``, so any season whose
    calendar zones span at least ``365 - search_start - validation`` days
    overlaps itself. Real GEOGLAM rows do: DRC maize spans 472 days, Mexico
    maize 639, USA winter wheat 319. Without the year both runs wrote the same
    files and the second silently overwrote the first.
    """
    return (
        f"{layer}_{season.country}_{season.crop}_s{int(season.season)}"
        f"_hy{int(season.harvest_year)}_asof{as_of.strftime('%Y%m%d')}"
    )


def write_rasters(
    result: dict, dir_rasters: Path, season: monitor.ActiveSeason
) -> list[Path]:
    """Write every layer of :data:`geocif.phenology.monitor.MONITOR_LAYERS`.

    Each GeoTIFF carries its units, the data-through date and the run identity
    in its tags.
    """
    meta = result["meta"]
    as_of = meta["as_of"]
    written: list[Path] = []
    for layer, (dtype, nodata, units) in monitor.MONITOR_LAYERS.items():
        array = result["layers"].get(layer)
        if array is None:
            continue
        written.append(
            outputs.write_geotiff(
                Path(dir_rasters) / f"{file_stem(layer, season, as_of)}.tif",
                array,
                result["transform"],
                nodata,
                dtype,
                tags={
                    "layer": layer,
                    "units": units,
                    "country": season.country,
                    "crop": season.crop,
                    "season": season.season,
                    "harvest_year": season.harvest_year,
                    "data_through": meta["data_through"],
                    "start_date": meta["start_date"],
                    "n_missing_days": meta["n_missing_days"],
                    "forecast_issue": meta["forecast_issue"],
                },
            )
        )
    logger.info(f"season monitor: {len(written)} raster(s) -> {dir_rasters}")
    return written


def map_tables(result: dict, status: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Companion tables for the maps: Admin 1 zonal summaries per mapped layer."""
    tables: dict[str, pd.DataFrame] = {"state": status}
    keys = {
        "onset_anomaly_days": "onset_anomaly_days",
        "days_past_median": "days_past_median",
        "p_onset": "p_onset_28d",
        "rain_percentile": "rain_30d_percentile",
        "fcst_trigger_days": "fcst_trigger_days",
    }
    for key, layer in keys.items():
        array = result["layers"].get(layer)
        if array is None:
            continue
        table = outputs.zonal_table(
            array, result["weight"], result["id_grid"], result["lookup"]
        )
        table.insert(0, "layer", layer)
        tables[key] = monitor._stamp(table, result["meta"])
    return tables


def render_maps(
    cfg: dict,
    result: dict,
    season: monitor.ActiveSeason,
    dirs: dict[str, Path],
    tables: dict[str, pd.DataFrame],
) -> list[tuple[str, str, str]]:
    """Render the monitor map set and write ``lookup_plots_csvs.csv``.

    Layers are computed on every land pixel and masked to cropland here, so the
    mask can change without recomputing (DESIGN section 8.1).
    """
    parser = cfg["parser"]
    try:
        admin_gdf = inputs.load_boundaries(parser, season.country)
    except Exception as exc:  # noqa: BLE001 - outlines are decoration, not data
        logger.warning(f"no admin outlines for {season.country}: {exc}")
        admin_gdf = None

    keep = None
    if cfg["mask_to_cropland"]:
        keep = np.asarray(result["crop_fraction"]) > 0.0

    ctx = phenology_maps.MapContext(
        lon=result["lon"],
        lat=result["lat"],
        dir_plots=dirs["maps"],
        dir_csvs=dirs["csvs"],
        country=season.country,
        crop=season.crop,
        season=int(season.season),
        harvest_year=int(season.harvest_year),
        asof=result["meta"]["as_of"],
        admin_gdf=admin_gdf,
    )
    layers = result["layers"]
    masked = {
        name: phenology_maps.mask_display(layers[name], keep)
        for name in MAP_LAYERS
        if name in layers
    }
    state = phenology_maps.mask_display(
        phenology_maps.state_to_float(layers["state"]), keep
    )
    fcst = masked.get("fcst_trigger_days")
    if fcst is not None and not np.any(np.isfinite(fcst)):
        fcst = None  # no forecast trigger anywhere: an empty map would mislead
    return phenology_maps.monitor_maps(
        ctx,
        state=state,
        onset_anomaly_days=masked.get("onset_anomaly_days"),
        days_past_median=masked.get("days_past_median"),
        p_onset=masked.get("p_onset_28d"),
        rain_percentile=masked.get("rain_30d_percentile"),
        fcst_trigger_days=fcst,
        horizon_days=28,
        rain_window_days=monitor.RAIN_PERCENTILE_WINDOW,
        tables=tables,
    )


def render_climatology_maps(
    cfg: dict,
    result: dict,
    season: monitor.ActiveSeason,
    dirs: dict[str, Path],
    clim: Optional[dict],
    clim_years: Sequence[int],
) -> list[tuple[str, str, str]]:
    """Render the six climatology maps into their own ``climatology/`` subtree.

    These describe the 1981-2025 reference, not the current season, so they are
    published once per cache alongside the monitor output rather than mixed into
    it -- and in a separate directory because each map set writes its own
    ``lookup_plots_csvs.csv``.

    ``onset_median`` is stored as days since the pixel's planting start, so the
    colourbar is labelled with dates anchored on this season's earliest planting
    day (``meta["planting_start"]``).

    Returns:
        The manifest rows, empty when there is no climatology to draw.
    """
    if not clim:
        return []
    needed = ("onset_median", "onset_p25", "onset_p75", "eos_median", "lgs_median")
    if not any(name in clim for name in needed):
        return []

    parser = cfg["parser"]
    try:
        admin_gdf = inputs.load_boundaries(parser, season.country)
    except Exception as exc:  # noqa: BLE001 - outlines are decoration, not data
        logger.warning(f"no admin outlines for {season.country}: {exc}")
        admin_gdf = None

    keep = None
    if cfg["mask_to_cropland"]:
        keep = np.asarray(result["crop_fraction"]) > 0.0

    shape = tuple(result["shape"])

    def _layer(name: str) -> Optional[np.ndarray]:
        """Cached layer masked for display, or None when absent or misshaped."""
        array = clim.get(name)
        if array is None:
            return None
        array = np.asarray(array, dtype="float64")
        if array.shape != shape:
            logger.warning(
                f"climatology layer {name} is {array.shape}, expected {shape}; skipping"
            )
            return None
        return phenology_maps.mask_display(array, keep)

    spread = None
    p25, p75 = _layer("onset_p25"), _layer("onset_p75")
    if p25 is not None and p75 is not None:
        spread = p75 - p25

    # The cached day layers are days since EACH pixel's own planting date, but a
    # date-labelled colourbar can only carry ONE anchor. Re-base them onto the
    # earliest planting date in the country so that "reference + value days" is
    # the true calendar date everywhere. Without this, a pixel in a late-planting
    # zone is labelled too early by that zone's offset -- 106 days for Tanzania
    # maize, 61 for Nigeria, 31 for Kenya. Durations (lgs, the p75-p25 spread)
    # need no anchor and are left alone.
    reference = _dt.date.fromisoformat(result["meta"]["planting_start"])
    planting = getattr(result.get("calendar"), "planting", None)
    shift = None
    if planting is not None:
        offset = (
            np.asarray(planting, dtype="datetime64[D]")
            - np.datetime64(reference, "D")
        ).astype("float64")
        shift = np.where(np.isnat(np.asarray(planting, dtype="datetime64[D]")), np.nan, offset)

    def _to_common_origin(array: Optional[np.ndarray]) -> Optional[np.ndarray]:
        """Days since the pixel's planting -> days since ``reference``."""
        if array is None or shift is None:
            return array
        return (array + shift).astype(np.float64)

    years = (
        (int(min(clim_years)), int(max(clim_years))) if len(clim_years) else None
    )
    ctx = phenology_maps.MapContext(
        lon=result["lon"],
        lat=result["lat"],
        dir_plots=dirs["clim_maps"],
        dir_csvs=dirs["clim_csvs"],
        country=season.country,
        crop=season.crop,
        season=int(season.season),
        harvest_year=None,   # the reference set spans many years, not one season
        asof=None,
        years=years,
        admin_gdf=admin_gdf,
    )
    return phenology_maps.climatology_maps(
        ctx,
        planting_reference=reference,
        onset_median=_to_common_origin(_layer("onset_median")),
        onset_p75_minus_p25=spread,
        eos_median=_to_common_origin(_layer("eos_median")),
        lgs_median=_layer("lgs_median"),
        false_start_rate=_layer("false_start_rate"),
        onset_n_valid=_layer("onset_n_valid"),
    )


def build_zone_report(
    cfg: dict,
    result: dict,
    season: monitor.ActiveSeason,
    dirs: dict[str, Path],
    params,
) -> list[tuple[str, str, str]]:
    """Per-calendar-zone start of season over a window around the planting date.

    Answers, per zone: in the two months centred on the calendar planting date,
    how often has the season started historically, when, and how does the season
    now running compare. It is an aggregation of the cached per-year onset
    rasters, so it costs no recomputation.

    The window half-width is ``zone_report_window_days``. When the onset search
    lead is not comfortably wider than it, onsets that beat the search are
    pinned at its boundary and the in-window share becomes a floor; every table
    carries ``share_censored`` and the chart draws the boundary, so that case is
    visible rather than silent.

    Returns:
        Manifest rows; empty when the cache or the calendar is unavailable.
    """
    from geocif.phenology import zone_report as zr
    from geocif.viz import zone_onset

    parser = cfg["parser"]
    window_days = int(cfg.get("zone_report_window_days", zr.DEFAULT_WINDOW_DAYS))
    lead = int(cfg["search_start_days_before_planting"])
    cache_dir = climatology.climatology_dir(
        parser, season.country, season.crop, int(season.season)
    )
    try:
        stack, years = zr.load_onset_stack(cache_dir)
    except FileNotFoundError as exc:
        logger.warning(f"zone report: no climatology to summarise ({exc})")
        return []
    if not years:
        logger.warning("zone report: the climatology holds no years")
        return []

    calendar = result.get("calendar")
    if calendar is None or not getattr(calendar, "zone_names", None):
        logger.warning("zone report: no calendar zones for this combination")
        return []
    if stack.shape[1:] != tuple(result["shape"]):
        logger.warning(
            f"zone report: cached grid {stack.shape[1:]} != monitor grid "
            f"{tuple(result['shape'])}; skipping"
        )
        return []

    weights = np.asarray(result["weight"], dtype="float64")
    plant = zr.planting_dates_by_zone(
        parser, season.country, season.crop, int(season.season),
        list(years) + [int(season.harvest_year)],
    )
    history = zr.zone_history(
        stack, years, calendar.zone_id, calendar.zone_names, weights,
        window_days=window_days, search_lead_days=lead, planting_dates=plant,
    )
    if history.empty:
        logger.warning("zone report: no zone overlaps the cropland mask")
        return []
    clim = zr.zone_climatology(history, min_years=int(cfg["min_valid_years"]))
    current = zr.current_vs_history(
        result["layers"]["onset_days"], history, calendar.zone_id,
        calendar.zone_names, weights, as_of=result["meta"]["as_of"],
        planting_dates=plant, harvest_year=int(season.harvest_year),
        window_days=window_days, search_lead_days=lead,
    )

    dir_plots, dir_csvs = Path(dirs["zone_plots"]), Path(dirs["zone_csvs"])
    as_of = result["meta"]["as_of"]
    stem = (
        f"{season.country}_{season.crop}_s{int(season.season)}"
        f"_hy{int(season.harvest_year)}_asof{as_of.strftime('%Y%m%d')}"
    )
    for name, frame in (
        ("zone_history", history), ("zone_climatology", clim), ("zone_current", current)
    ):
        frame.to_csv(dir_csvs / f"{name}_{stem}.csv", index=False)

    crop_label = phenology_maps._display_name(season.crop)
    country_label = phenology_maps._display_name(season.country)
    rows: list[tuple[str, str, str]] = []
    png, csv = zone_onset.window_dotplot(
        history, current, dir_plots / f"onset_window_{stem}",
        window_days=window_days, search_lead_days=lead,
        title=f"{country_label} {crop_label} Season {int(season.season)} Onset vs "
              f"Calendar Window, {years[0]}-{years[-1]}",
    )
    csv.replace(dir_csvs / csv.name)
    rows.append((png.name, csv.name, "Onset against the calendar window, by zone and year"))

    png, csv = zone_onset.in_window_bars(
        clim, current, dir_plots / f"in_window_share_{stem}",
        title=f"{country_label} {crop_label} Cropland Starting Within "
              f"{window_days} Days of the Calendar Date",
    )
    csv.replace(dir_csvs / csv.name)
    rows.append((png.name, csv.name, "Share of cropland starting inside the window, by zone"))

    from geocif.viz.aggregation import _write_lookup
    _write_lookup(rows, dir_plots, dir_csvs)
    n_open = int((current["window_status"] != "not_open").sum()) if not current.empty else 0
    logger.info(
        f"zone report: {len(current)} zone(s) for {country_label} {crop_label} "
        f"season {int(season.season)}, {n_open} with the window open "
        f"(+/-{window_days} d, search lead {lead} d)"
    )
    return rows


def write_tables(
    result: dict,
    dirs: dict[str, Path],
    season: monitor.ActiveSeason,
    status: pd.DataFrame,
    summary: pd.DataFrame,
) -> list[Path]:
    """Write ``status_area`` and ``onset_summary`` into ``csvs/``."""
    as_of = result["meta"]["as_of"]
    written: list[Path] = []
    for name, frame in (("status_area", status), ("onset_summary", summary)):
        path = Path(dirs["csvs"]) / f"{file_stem(name, season, as_of)}.csv"
        frame.to_csv(path, index=False)
        written.append(path)
        logger.info(f"wrote {path} ({len(frame)} row(s))")
    return written


# ---------------------------------------------------------------------------
# banner
# ---------------------------------------------------------------------------
def _esc(value: Any) -> str:
    """Escape ``[`` so Rich does not eat a config list as markup."""
    return str(value).replace("[", r"\[")


def _banner(cfg: dict, seasons: Sequence[monitor.ActiveSeason], out_root: Path) -> None:
    """Print the Rich startup banner: what will run, on what, with which knobs."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    try:
        from geocif import __version__ as version
    except Exception:  # noqa: BLE001 - a banner must never break a run
        version = "unknown"

    crops = sorted({s.crop for s in seasons})
    combos = ", ".join(
        f"{s.country}/{s.crop} s{s.season} hy{s.harvest_year}" for s in seasons
    )
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column()
    table.add_row("Version", f"geocif {version}")
    table.add_row("Usage", r"from geocif import season_monitor; season_monitor.run(cfg)")
    table.add_row("Countries", _esc(", ".join(cfg["countries"]) or "(none)"))
    table.add_row("Crops", _esc(", ".join(crops) or "(none active)"))
    table.add_row("Active seasons", _esc(combos or "(none)"))
    table.add_row("As-of (data through)", _esc(cfg["as_of"]))
    table.add_row(
        "Onset",
        _esc(
            f"{cfg['precip_threshold']:g} mm / {cfg['window_days']} d, "
            f"dry spell {cfg['dry_spell_days']} d below {cfg['dry_day_threshold']:g} mm, "
            f"validation {cfg['validation_days']} d"
        ),
    )
    table.add_row(
        "Search window",
        _esc(f"opens {cfg['search_start_days_before_planting']} d before planting"),
    )
    table.add_row(
        "Climatology",
        _esc(
            f"{cfg['climatology_start_year']}-{cfg['climatology_end_year']}, "
            f"min_valid_years {cfg['min_valid_years']}, "
            f"rebuild {cfg['rebuild_climatology']}, n_workers {cfg['n_workers']}"
        ),
    )
    table.add_row(
        "Forecast",
        _esc(
            f"use_forecast {cfg['use_forecast']}, {cfg['forecast_days']} d"
            if cfg["use_forecast"]
            else "disabled"
        ),
    )
    table.add_row(
        "Display",
        _esc(f"mask_to_cropland {cfg['mask_to_cropland']}, bbox_buffer {cfg['bbox_buffer']:g} deg"),
    )
    table.add_row("Refresh", _esc(cfg["refresh_datasets"] or "disabled"))
    table.add_row("Input root", _esc(cfg["dir_intermed"]))
    table.add_row("Output root", _esc(out_root))
    Console().print(Panel(table, title="GEOCIF season monitor", border_style="cyan"))


# ---------------------------------------------------------------------------
# the run
# ---------------------------------------------------------------------------
def _ensure_climatology(cfg: dict, season: monitor.ActiveSeason, params) -> tuple[Optional[dict], list[int]]:
    """Build-or-reuse the climatology cache and load it.

    A cache whose params hash matches is a no-op; a mismatch rebuilds. A build
    that fails is logged and the monitor proceeds without the climatological
    layers rather than losing the state map as well.

    Returns:
        ``(arrays, years)`` from
        :func:`geocif.phenology.climatology.load_climatology`, or
        ``(None, [])``.
    """
    parser = cfg["parser"]
    cache_dir = climatology.climatology_dir(
        parser, season.country, season.crop, int(season.season)
    )
    years = list(
        range(int(cfg["climatology_start_year"]), int(cfg["climatology_end_year"]) + 1)
    )
    try:
        climatology.build_climatology(
            parser,
            season.country,
            season.crop,
            int(season.season),
            years,
            params,
            cache_dir,
            n_workers=int(cfg["n_workers"]),
            rebuild=bool(cfg["rebuild_climatology"]),
        )
    except Exception as exc:  # noqa: BLE001 - a bad cache must not lose the monitor
        logger.warning(
            f"climatology unavailable for {season.country}/{season.crop} "
            f"s{season.season}: {exc}"
        )
    # Hand load_climatology the hash we asked for. A failed rebuild leaves the
    # PREVIOUS cache on disk, and using it would silently compare this season's
    # onset against a reference computed with other parameters -- a systematic
    # bias invisible on the map. Better to publish the state map with no anomaly
    # than an anomaly measured against the wrong yardstick.
    expect = climatology.params_hash_for(
        parser, season.country, season.crop, int(season.season), years, params
    )
    loaded = climatology.load_climatology(
        cache_dir, with_stack=True, expect_hash=expect
    )
    if loaded is None:
        return None, []
    arrays, manifest = loaded
    return arrays, [int(y) for y in manifest.get("years", [])]


def _process(cfg: dict, season: monitor.ActiveSeason, stamp: str) -> dict:
    """Run one combination end to end and return its summary record."""
    params = climatology_params(cfg, season.crop)
    clim, clim_years = _ensure_climatology(cfg, season, params)
    result = monitor.monitor_season(
        cfg["parser"],
        season.country,
        season.crop,
        int(season.season),
        int(season.harvest_year),
        cfg["as_of"],
        params,
        clim=clim,
        clim_years=clim_years,
        use_forecast=bool(cfg["use_forecast"]),
        forecast_days=int(cfg["forecast_days"]),
        bbox_buffer=float(cfg["bbox_buffer"]),
        n_threads=max(1, int(cfg["n_workers"])),
    )
    dirs = output_dirs(cfg, season, stamp)
    rasters = write_rasters(result, dirs["rasters"], season)

    status = monitor.status_area_frame(result)
    summary = monitor.onset_summary_frame(result)
    tables = map_tables(result, status)

    rows: list[tuple[str, str, str]] = []
    try:
        rows = render_maps(cfg, result, season, dirs, tables)
    except Exception as exc:  # noqa: BLE001 - tables must survive a drawing failure
        logger.error(
            f"map rendering failed for {season.country}/{season.crop} s{season.season}: "
            f"{exc}\n{traceback.format_exc()}"
        )
    clim_rows: list[tuple[str, str, str]] = []
    try:
        clim_rows = render_climatology_maps(cfg, result, season, dirs, clim, clim_years)
    except Exception as exc:  # noqa: BLE001 - the reference set is secondary to the monitor
        logger.error(
            f"climatology map rendering failed for {season.country}/{season.crop} "
            f"s{season.season}: {exc}\n{traceback.format_exc()}"
        )
    zone_rows: list[tuple[str, str, str]] = []
    if cfg.get("zone_report", True):
        try:
            zone_rows = build_zone_report(cfg, result, season, dirs, params)
        except Exception as exc:  # noqa: BLE001 - secondary to the monitor itself
            logger.error(
                f"zone report failed for {season.country}/{season.crop} "
                f"s{season.season}: {exc}\n{traceback.format_exc()}"
            )
    csvs = write_tables(result, dirs, season, status, summary)
    return {
        "country": season.country,
        "crop": season.crop,
        "season": int(season.season),
        "harvest_year": int(season.harvest_year),
        "ok": True,
        "error": None,
        "dir": str(dirs["root"]),
        "n_rasters": len(rasters),
        "n_maps": len(rows),
        "n_climatology_maps": len(clim_rows),
        "n_zone_report_files": len(zone_rows),
        "n_tables": len(csvs),
        "climatology_years": len(clim_years),
        "state_counts": result["state_counts"],
        "data_through": result["meta"]["data_through"],
    }


def run(path_config_files: Optional[Sequence[Any]] = None, **overrides: Any) -> dict:
    """Score every active season and publish rasters, maps and tables.

    Args:
        path_config_files: the 4-file geocif config list.
        **overrides: any ``[SEASON_MONITOR]`` key (see :data:`DEFAULTS`) plus
            ``as_of`` (``date`` or ``YYYY-MM-DD``) -- these win over the file.

    Returns:
        ``{"as_of", "stamp", "refresh", "active", "results", "n_ok", "n_failed"}``.
        ``results`` holds one record per combination, failures included with
        their message. Nothing here ever raises out of a single combination and
        ``os._exit`` is never called.

    Raises:
        ValueError: when no config list is given, or no CHIRPS day is on disk.
    """
    if not path_config_files:
        raise ValueError("season_monitor.run needs the 4-file geocif config list")
    cfg = read_config(path_config_files, **overrides)

    refresh: dict = {}
    if cfg["refresh_datasets"]:
        refresh = refresh_inputs(
            cfg["config_files"],
            datasets=tuple(cfg["refresh_datasets"]),
            logger=logger,
        )
        logger.info(f"refresh: {refresh}")
    else:
        logger.info("refresh skipped: refresh_datasets is empty")

    if cfg["as_of"] is None:
        cfg["as_of"] = climatology.last_available_day(cfg["parser"], "chirps")
    if cfg["as_of"] is None:
        raise ValueError(
            "no CHIRPS day found on disk; the monitor has no as-of date to report"
        )

    seasons = monitor.active_seasons(
        cfg["parser"],
        cfg["as_of"],
        countries=cfg["countries"],
        search_start_days_before_planting=int(cfg["search_start_days_before_planting"]),
        validation_days=int(cfg["validation_days"]),
        seasons_by_country=cfg.get("country_seasons"),
    )
    stamp = analysis_stamp()
    out_root = (
        Path(cfg["dir_output"]) / cfg["project"] / "ml" / "analysis" / stamp / PRODUCT
    )
    _banner(cfg, seasons, out_root)
    if not seasons:
        logger.warning(f"no active season for {cfg['countries']} as of {cfg['as_of']}")

    results: list[dict] = []
    for season in seasons:
        try:
            results.append(_process(cfg, season, stamp))
        except Exception as exc:  # noqa: BLE001 - one bad combination, not the run
            logger.error(
                f"season monitor failed for {season.country}/{season.crop} "
                f"s{season.season} hy{season.harvest_year}: {exc}\n{traceback.format_exc()}"
            )
            results.append(
                {
                    "country": season.country,
                    "crop": season.crop,
                    "season": int(season.season),
                    "harvest_year": int(season.harvest_year),
                    "ok": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    n_ok = sum(1 for r in results if r.get("ok"))
    logger.info(
        f"season monitor done: {n_ok}/{len(results)} combination(s) written to "
        f"{out_root} (data through {cfg['as_of']})"
    )
    return {
        "as_of": cfg["as_of"],
        "stamp": stamp,
        "out_root": out_root,
        "refresh": refresh,
        "active": list(seasons),
        "results": results,
        "n_ok": n_ok,
        "n_failed": len(results) - n_ok,
    }


def main(argv: Optional[Sequence[str]] = None) -> dict:
    """CLI: ``python -m geocif.season_monitor --config ... [--as-of YYYY-MM-DD]``."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--config",
        action="append",
        required=True,
        help="geocif config file (repeatable: geobase, countries, crops, geocif)",
    )
    parser.add_argument(
        "--as-of",
        default=None,
        help="data-through date YYYY-MM-DD (default: the last CHIRPS day on disk)",
    )
    parser.add_argument(
        "--country",
        action="append",
        default=None,
        help="country slug to monitor (repeatable; default: the configured list)",
    )
    parser.add_argument("--no-refresh", action="store_true", help="skip the data refresh")
    parser.add_argument(
        "--no-forecast", action="store_true", help="ignore CHIRPS-GEFS entirely"
    )
    parser.add_argument(
        "--rebuild-climatology",
        action="store_true",
        help="rebuild the climatology cache even when its params hash matches",
    )
    parser.add_argument("--workers", type=int, default=None, help="process/thread pool size")
    args = parser.parse_args(argv)

    overrides: dict[str, Any] = {}
    if args.as_of:
        overrides["as_of"] = args.as_of
    if args.country:
        overrides["countries"] = list(args.country)
    if args.no_refresh:
        overrides["refresh_datasets"] = []
    if args.no_forecast:
        overrides["use_forecast"] = False
    if args.rebuild_climatology:
        overrides["rebuild_climatology"] = True
    if args.workers:
        overrides["n_workers"] = int(args.workers)
    return run(args.config, **overrides)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    main()
