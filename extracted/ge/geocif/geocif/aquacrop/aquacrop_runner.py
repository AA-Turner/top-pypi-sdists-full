"""
aquacrop_runner.py — entry point for the AquaCrop yield pipeline.

Usage::

    from geocif.aquacrop import aquacrop_runner
    aquacrop_runner.run([
        "config/geobase.txt",
        "config/countries.txt",
        "config/crops.txt",
        "config/aquacrop.txt",
    ])

Mirrors ``geocif.geocif_runner.run``: builds the config parser via
``geocif.logger.setup_logger_parser`` (so logging + tqdm.rich integration
happen automatically), prints a Rich panel summary, then iterates
country × crop × season × year.

Per (country, crop, season, year):

    1.  Load admin boundary + crop fraction mask.
    2.  Build 5 km grid clipped to country boundary.
    3.  Read calendar (planting/harvest per calendar_region).
    4.  Build per-cell CellTask list (skip cells with low crop fraction
        or no calendar coverage).
    5.  Run grid_simulator.run_grid via mp.Pool.
    6.  Assemble cell results into a yield raster; write to disk.
    7.  Aggregate raster → admin polygons via geom_extract (AFI = mask).
    8.  Join HarvestStat observed yields via ml.stats.add_statistics.
    9.  Apply LOOCV cross-country region_anomaly calibration.
    10. Write DB row in geocif yield_outlook schema.
    11. Run validation diagnostics if validation=True.
"""

from __future__ import annotations

import ast
import datetime as _dt
import logging
import os
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from .. import __version__
from . import calendar as _cal
from . import calibration as _calib
from . import crop_mask as _cmask
from . import grid_simulator as _grid
from . import output as _out
from . import param_calibration as _paramcal
from . import param_spec as _paramspec
from . import validation as _val

logger = logging.getLogger(__name__)


# Crop name canonicalization. Local copy of the mapping from
# geoprepare.base.BaseGeo.get_crop_full_name so this module doesn't
# need to import the parser before crop names appear.
_CROP_SHORT_TO_FULL = {
    "mz": "maize", "sb": "soybean", "rc": "rice",
    "sw": "spring_wheat", "ww": "winter_wheat",
    "ml": "millet", "tf": "teff", "sr": "sorghum", "pp": "poppy",
}


# AquaCrop-OSPy v3 built-in crop names. Used to fail-fast at startup when a
# user's config maps to a name AquaCrop doesn't know — beats discovering
# the typo via "no such crop" errors per cell × per LOOCV year.
# Source: aquacrop.entities.crops.crop_params.crop_params_dict keys.
_AQUACROP_BUILTIN_CROPS = frozenset({
    "Barley", "Cotton", "DryBean", "Maize", "MaizeGDD",
    "PaddyRice", "Potato", "Quinoa", "Rice", "Sorghum",
    "Soybean", "SugarBeet", "SugarCane", "Sunflower",
    "Tef", "Tomato", "Wheat", "WheatGDD",
})


def _validate_aquacrop_crop_name(name: str, label: str = "") -> None:
    """Raise ValueError if ``name`` isn't a known AquaCrop builtin.

    Try to load AquaCrop's actual registry if available; fall back to the
    hardcoded set so this check still works in environments where the
    registry isn't importable.
    """
    builtins = _AQUACROP_BUILTIN_CROPS
    try:
        from aquacrop.entities.crops.crop_params import crop_params_dict
        builtins = frozenset(crop_params_dict.keys())
    except (ImportError, AttributeError):
        pass
    if name not in builtins:
        raise ValueError(
            f"AquaCrop crop name {name!r} not in registry "
            f"({label}). Valid names: {sorted(builtins)}"
        )


def _canonical_crop(name: str) -> str:
    """Canonicalize a crop name to geocif's 9-name vocabulary."""
    return _CROP_SHORT_TO_FULL.get(name, name).lower()


def _hvstat_crop_label(canonical: str) -> str:
    """Convert canonical crop name to the Title-Case label HarvestStat uses.

    Mirrors the geocif.ml.stats convention:
        winter_wheat → "Winter Wheat"
        maize → "Maize"
        spring_wheat → "Spring Wheat"   (note: hvstat may use "Wheat" —
            stats.add_statistics handles the "Wheat" → "Winter Wheat"
            replacement)
    """
    return canonical.replace("_", " ").title()


def _aquacrop_crop_name(parser, canonical: str, country: str) -> Optional[str]:
    """Resolve the AquaCrop builtin name for a canonical crop+country.

    Reads [AQUACROP] crop_mapping_<name>. Returns None if the mapping
    is 'skip' (millet, poppy) or missing — caller should skip the combo.
    """
    key = f"crop_mapping_{canonical}"
    if not parser.has_option("AQUACROP", key):
        logger.warning(f"No AquaCrop mapping for {canonical} — skipping")
        return None
    val = parser.get("AQUACROP", key).strip()
    if val.lower() == "skip":
        logger.info(f"Crop {canonical} configured as 'skip' — no AquaCrop run")
        return None

    # Per-country rice override: paddy vs upland
    if canonical == "rice":
        try:
            paddy_countries = ast.literal_eval(
                parser.get("AQUACROP", "paddy_rice_countries", fallback="[]")
            )
        except (ValueError, SyntaxError):
            paddy_countries = []
        if country.lower() in [c.lower() for c in paddy_countries]:
            val = "PaddyRice"
    # Validate against AquaCrop's registry so a typo in the config dies at
    # combination-build time, not 5000 cells later inside a worker.
    _validate_aquacrop_crop_name(val, label=f"{country}/{canonical}")
    return val


def _setup_logger_parser(config_files: list[str]):
    """Build (logger, parser). Use geocif's setup if available, else stdlib."""
    try:
        from geocif import logger as glog  # type: ignore
        return glog.setup_logger_parser(config_files)
    except ImportError:
        from configparser import ConfigParser, ExtendedInterpolation
        parser = ConfigParser(interpolation=ExtendedInterpolation())
        parser.read(config_files)
        logging.basicConfig(
            level=parser.get("LOGGING", "level", fallback="INFO"),
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )
        return logging.getLogger("aquacrop_runner"), parser


def _build_run_combinations(parser, countries: list[str]) -> list[dict]:
    """Build (country, crop, season, year) combinations from config.

    Wheat is single-season (wheat_*: skip seasons > 1) — matches
    geomerge.create_run_combinations.
    """
    forecast_years = ast.literal_eval(
        parser.get("DEFAULT", "forecast_seasons", fallback="[2026]")
    )
    start_year = parser.getint("DEFAULT", "start_year", fallback=2001)
    end_year = parser.getint("DEFAULT", "end_year", fallback=2026)
    years = list(range(start_year, end_year + 1))

    combos = []
    for country in countries:
        if not parser.has_section(country):
            logger.warning(f"Country {country} not in countries.txt — skipping")
            continue
        try:
            crops = ast.literal_eval(parser.get(country, "crops"))
            seasons = ast.literal_eval(
                parser.get(country, "seasons", fallback="[1]")
            )
        except (ValueError, SyntaxError) as exc:
            logger.error(f"Bad crops/seasons for {country}: {exc}")
            continue

        for crop in crops:
            canonical = _canonical_crop(crop)
            ac_name = _aquacrop_crop_name(parser, canonical, country)
            if ac_name is None:
                continue
            for season in seasons:
                if canonical in ("winter_wheat", "spring_wheat") and season > 1:
                    continue
                for year in years:
                    combos.append({
                        "country": country,
                        "crop": canonical,
                        "aquacrop_crop": ac_name,
                        "season": int(season),
                        "year": int(year),
                        "is_forecast": int(year) in forecast_years,
                    })
    return combos


def _load_admin_boundary(parser, country: str):
    """Load the admin boundary GeoDataFrame with standardized columns.

    Honours geocif's per-shapefile column mapping (e.g. [adm_shapefile]
    adm0_col, adm1_col, id_col) so output columns are consistently
    ``ADM0_NAME``, ``ADM1_NAME``, ``ADM_ID``.
    """
    import geopandas as gpd

    dir_boundaries = Path(parser.get("PATHS", "dir_boundary_files"))
    boundary_file = parser.get(country, "boundary_file")
    path = dir_boundaries / boundary_file
    if not path.is_file():
        raise FileNotFoundError(f"Boundary not found: {path}")

    gdf = gpd.read_file(path)
    # Apply column mapping (stem of filename = section in geobase.txt)
    stem = path.stem
    if parser.has_section(stem):
        rename = {}
        for std_col in ("adm0_col", "adm1_col", "adm2_col", "id_col"):
            if parser.has_option(stem, std_col):
                src = parser.get(stem, std_col)
                target = {
                    "adm0_col": "ADM0_NAME", "adm1_col": "ADM1_NAME",
                    "adm2_col": "ADM2_NAME", "id_col": "ADM_ID",
                }[std_col]
                if src in gdf.columns:
                    rename[src] = target
        if rename:
            gdf = gdf.rename(columns=rename)

    # Filter to country (admin boundary files are often global / regional)
    country_label = country.replace("_", " ")
    if "ADM0_NAME" in gdf.columns:
        mask = gdf["ADM0_NAME"].str.lower().str.replace("_", " ") \
            == country_label.lower()
        if mask.any():
            gdf = gdf[mask].copy()
    return gdf


def _build_cell_tasks(
    parser, country: str, canonical_crop: str, aquacrop_crop: str,
    season: int, year: int, gdf_admin, mask_path: Path,
) -> tuple[list[_grid.CellTask], np.ndarray, np.ndarray, tuple]:
    """Build the per-cell task list for one (country, crop, season, year).

    Returns:
        (tasks, lons_1d, lats_1d, bounds) — lons/lats define the 5 km grid
        used by the output raster; bounds is (minx, miny, maxx, maxy).
    """
    # 1. Determine grid bounds + 5 km resolution
    minx, miny, maxx, maxy = gdf_admin.total_bounds
    # 0.05 degree = ~5 km; match AgERA5/CHIRPS native resolution exactly
    res = 0.05
    # Snap bounds to multiples of resolution for clean grid alignment
    minx = np.floor(minx / res) * res
    miny = np.floor(miny / res) * res
    maxx = np.ceil(maxx / res) * res
    maxy = np.ceil(maxy / res) * res

    n_cols = int(round((maxx - minx) / res))
    n_rows = int(round((maxy - miny) / res))
    lons = minx + res * (np.arange(n_cols) + 0.5)
    lats = maxy - res * (np.arange(n_rows) + 0.5)  # north → south

    # 2. Read & resample crop mask to this grid
    mask_arr, mask_profile = _cmask.read_mask_array(
        mask_path, bounds=(minx, miny, maxx, maxy),
    )
    # Resample to the canonical 5 km grid if needed
    from rasterio.transform import from_bounds
    target_transform = from_bounds(minx, miny, maxx, maxy, n_cols, n_rows)
    mask_5km = _cmask.aggregate_to_5km(
        mask_arr, mask_profile, target_transform, (n_rows, n_cols),
    )

    # 3. Load calendar (per calendar_region planting/harvest)
    try:
        cal_df = _cal.load_calendar(parser, country, canonical_crop,
                                    season, year)
    except (FileNotFoundError, ValueError) as exc:
        logger.warning(
            f"Calendar load failed for {country}/{canonical_crop}/"
            f"season={season}/year={year}: {exc}"
        )
        return [], lons, lats, (minx, miny, maxx, maxy)

    # 4. Build CellTask list, filtering by min_crop_fraction and admin extent
    min_frac = parser.getfloat("AQUACROP", "min_crop_fraction", fallback=0.01)

    # Per-cell calendar lookup: rasterize each admin polygon with an integer
    # ID, then map admin_id → calendar_row. Falls back to the first
    # calendar row for cells in admins not present in the calendar Excel
    # (mirrors the country-mean default that used to apply to every cell).
    import rasterio.features as _rf
    fallback_row = cal_df.iloc[0]
    admin_col_name = (
        "ADM2_NAME" if "ADM2_NAME" in gdf_admin.columns
        and gdf_admin["ADM2_NAME"].notna().any()
        else "ADM1_NAME"
    )
    cal_by_region = {
        str(r["calendar_region"]).lower().strip(): r
        for _, r in cal_df.iterrows()
    }

    # Burn an admin index (1-based) per cell; 0 = outside any admin polygon
    admin_idx_grid = _rf.rasterize(
        ((geom, idx + 1) for idx, geom in enumerate(gdf_admin.geometry)),
        out_shape=(n_rows, n_cols),
        transform=target_transform,
        fill=0,
        all_touched=False,
        dtype=np.int32,
    )
    # Per-admin-index calendar row (1-indexed to match the burn above)
    admin_cal_rows = []
    for _, admin_row in gdf_admin.iterrows():
        admin_name = str(admin_row.get(admin_col_name, "")).lower().strip()
        admin_cal_rows.append(cal_by_region.get(admin_name, fallback_row))

    tasks = []
    for i in range(n_rows):
        for j in range(n_cols):
            admin_idx = int(admin_idx_grid[i, j])
            if admin_idx == 0:
                continue
            frac = float(mask_5km[i, j])
            if not np.isfinite(frac) or frac < min_frac:
                continue
            cal_row = admin_cal_rows[admin_idx - 1]
            tasks.append(_grid.CellTask(
                row=i, col=j,
                lon=float(lons[j]),
                lat=float(lats[i]),
                crop_fraction=frac,
                calendar_region=str(cal_row["calendar_region"]),
                sim_start=cal_row["planting_date"],
                sim_end=(cal_row["harvest_date"] + _dt.timedelta(days=14)),
                crop_aquacrop_name=aquacrop_crop,
                planting_date_str=cal_row["planting_date"].strftime("%m/%d"),
                harvest_year=cal_row["harvest_date"].year,
            ))
    return tasks, lons, lats, (minx, miny, maxx, maxy)


def _join_harveststat(
    df_outlook: pd.DataFrame, parser, country: str, canonical_crop: str,
    admin_zone: str,
) -> pd.DataFrame:
    """Join HarvestStat observed yields onto the outlook DataFrame.

    Uses ``geocif.ml.stats.add_statistics`` directly so all the country-
    specific special cases (Kenya/Malawi Maize → Annual fallback, etc.)
    are preserved.
    """
    try:
        from geocif.ml.stats import add_statistics  # type: ignore
    except ImportError:
        logger.warning(
            "geocif.ml.stats not importable — observed yields will be NaN"
        )
        return df_outlook

    dir_stats = Path(parser.get("PATHS", "dir_production_statistics"))
    title_country = country.replace("_", " ").title()
    title_crop = _hvstat_crop_label(canonical_crop)
    # Pass the country's configured `method` (e.g. "monthly_r") rather than
    # hardcoded "aquacrop" — `add_statistics` forwards `method` to the
    # GEOGLAM fallback path which builds a real file path, and "aquacrop"
    # would land it on a non-existent file for any country routed through
    # add_GEOGLAM_statistics (Bangladesh Rice, etc.).
    method = parser.get(country, "method", fallback="monthly_r")

    return add_statistics(
        dir_stats=dir_stats,
        df=df_outlook,
        country=title_country,
        crop=title_crop,
        admin_zone=admin_zone,
        stats=["Yield (tn per ha)", "Area (ha)", "Production (tn)"],
        method=method,
        target_col="Observed Yield (tn per ha)",
        parser=parser,
        label=f"{country}/{canonical_crop}",
    )


def _snap_country_bounds(gdf_admin, res: float = 0.05) -> tuple:
    """Compute (minx, miny, maxx, maxy) snapped to the AgERA5/CHIRPS grid.

    Identical to the snap inside ``_build_cell_tasks`` — kept here so the
    runner can pass the same bounds into the per-country Pool initializer
    *before* any combo runs, so all workers' weather cubes are clipped to
    the same box.
    """
    minx, miny, maxx, maxy = gdf_admin.total_bounds
    return (
        float(np.floor(minx / res) * res),
        float(np.floor(miny / res) * res),
        float(np.ceil(maxx / res) * res),
        float(np.ceil(maxy / res) * res),
    )


def _maybe_calibrate_params(
    parser,
    country: str,
    country_combos: list[dict],
    gdf_admin,
    country_bounds: tuple,
    pool,
    config_files: list[str],
) -> dict[str, dict[str, float]]:
    """Run PyGMO PSO calibration of AquaCrop crop parameters per crop.

    Returns ``{aquacrop_crop_name: {param: value}}``. Empty dict means
    calibration is off or unavailable — callers should treat that as
    "use AquaCrop defaults".

    Controlled by ``[AQUACROP_CALIBRATION] param_calibration`` (none/pso).
    Skips fitting if a JSON cache exists and ``reuse_fitted_params`` is True.
    """
    mode = parser.get(
        "AQUACROP_CALIBRATION", "param_calibration", fallback="none",
    ).lower()
    if mode == "none":
        return {}
    if mode != "pso":
        logger.warning(
            f"Unknown param_calibration={mode!r} — falling back to AquaCrop defaults"
        )
        return {}

    reuse = parser.getboolean(
        "AQUACROP_CALIBRATION", "reuse_fitted_params", fallback=True,
    )
    try:
        params_list = ast.literal_eval(
            parser.get("AQUACROP_CALIBRATION", "params",
                       fallback="['HI0', 'WP', 'CCx']")
        )
    except (ValueError, SyntaxError):
        params_list = ["HI0", "WP", "CCx"]

    dir_output = Path(parser.get("PATHS", "dir_output"))
    project = parser.get("DEFAULT", "project_name", fallback="geocif")

    overrides_by_crop: dict[str, dict[str, float]] = {}
    crops_in_country = sorted({c["aquacrop_crop"] for c in country_combos})

    for ac_crop in crops_in_country:
        canonical = next(
            c["crop"] for c in country_combos if c["aquacrop_crop"] == ac_crop
        )
        json_path = _paramcal.fitted_params_path(
            dir_output / project, country, ac_crop,
        )

        if reuse:
            cached = _paramcal.load_fitted_overrides(json_path)
            if cached and ac_crop in cached:
                overrides_by_crop[ac_crop] = cached[ac_crop]
                logger.info(
                    f"Loaded cached AquaCrop params for {country}/{ac_crop} (skipping refit)"
                )
                continue

        # Build a calibration problem for this (country, crop). Returns
        # None on any setup failure (missing observed yields, no training
        # cells, etc.) so the run can still proceed with defaults.
        result = _build_and_run_param_calibration(
            parser, country, canonical, ac_crop, country_combos,
            gdf_admin, country_bounds, pool, config_files,
            params_list,
        )
        if result is None:
            logger.warning(
                f"Calibration skipped for {country}/{ac_crop} — defaults will be used"
            )
            continue
        spec, best_fitness = result
        overrides_by_crop[ac_crop] = spec.overrides_dict() or {}
        _paramcal.save_fitted_json(
            json_path, [spec], best_fitness,
            metadata={
                "country": country,
                "canonical_crop": canonical,
                "aquacrop_crop": ac_crop,
                "fitted_at": _dt.datetime.utcnow().isoformat() + "Z",
            },
        )

    return overrides_by_crop


def _build_and_run_param_calibration(
    parser, country: str, canonical: str, ac_crop: str,
    country_combos: list[dict], gdf_admin, country_bounds, pool,
    config_files: list[str], params_list: list[str],
):
    """Set up + execute one (country, crop) PSO calibration.

    Returns (fitted AquaCropParamSpec, best_fitness) on success, None on
    setup failure. Designed to never raise — calibration failures should
    degrade gracefully to "use defaults" rather than killing the whole run.
    """
    try:
        # Year cutoff: only use years up to and including this for calibration.
        cutoff = parser.getint(
            "AQUACROP_CALIBRATION", "calibration_year_cutoff", fallback=2023,
        )
        train_combos = [
            c for c in country_combos
            if c["aquacrop_crop"] == ac_crop
            and c["year"] <= cutoff
            and not c["is_forecast"]
        ]
        if not train_combos:
            logger.warning(
                f"No training years <= {cutoff} for {country}/{ac_crop}"
            )
            return None

        # 1. Build cell tasks for ONE representative training year to get
        #    the cell grid + admin map. We'll replicate across all training
        #    years below.
        anchor_combo = train_combos[0]
        try:
            mask_path = _cmask.resolve_mask_path(parser, country, canonical)
        except Exception as exc:
            logger.warning(f"Mask missing for {country}/{canonical}: {exc}")
            return None

        anchor_tasks, _, _, _ = _build_cell_tasks(
            parser, country, canonical, ac_crop,
            anchor_combo["season"], anchor_combo["year"],
            gdf_admin, mask_path,
        )
        if not anchor_tasks:
            logger.warning(f"No tasks built for {country}/{ac_crop} anchor year")
            return None

        # 2. Build cell→admin map for aggregation (admin_id == ADM_ID column).
        admin_level = parser.get(country, "admin_level", fallback="admin_1")
        admin_col = "ADM1_NAME" if admin_level == "admin_1" else "ADM2_NAME"
        id_col = "ADM_ID" if "ADM_ID" in gdf_admin.columns else admin_col

        # Use the same rasterize approach as _build_cell_tasks so the
        # (row, col) → admin_id map matches what the cells came from.
        import rasterio.features as _rf
        minx, miny, maxx, maxy = country_bounds
        res = 0.05
        n_cols = int(round((maxx - minx) / res))
        n_rows = int(round((maxy - miny) / res))
        from rasterio.transform import from_bounds
        target_transform = from_bounds(minx, miny, maxx, maxy, n_cols, n_rows)
        admin_idx_grid = _rf.rasterize(
            ((geom, idx + 1) for idx, geom in enumerate(gdf_admin.geometry)),
            out_shape=(n_rows, n_cols), transform=target_transform,
            fill=0, all_touched=False, dtype=np.int32,
        )
        admin_ids = gdf_admin[id_col].tolist()
        cell_to_admin = {
            (t.row, t.col): admin_ids[admin_idx_grid[t.row, t.col] - 1]
            for t in anchor_tasks
            if 0 < int(admin_idx_grid[t.row, t.col]) <= len(admin_ids)
        }

        # 3. Subsample cells (production-weighted, stratified).
        cells_df = pd.DataFrame([
            {
                "task_idx": k,
                "row": t.row, "col": t.col,
                "admin_id": cell_to_admin.get((t.row, t.col)),
                "crop_fraction": t.crop_fraction,
                "cell_area_km2": 25.0,  # 5km × 5km, constant for AgERA5 grid
            }
            for k, t in enumerate(anchor_tasks)
            if (t.row, t.col) in cell_to_admin
        ])

        n_total = parser.getint(
            "AQUACROP_CALIBRATION", "calibration_sample_size", fallback=150,
        )
        mult = parser.getfloat(
            "AQUACROP_CALIBRATION", "sample_density_multiplier", fallback=1.0,
        )
        min_per = parser.getint(
            "AQUACROP_CALIBRATION", "min_cells_per_admin", fallback=1,
        )
        max_per = parser.getint(
            "AQUACROP_CALIBRATION", "max_cells_per_admin", fallback=0,
        )
        min_frac = parser.getfloat(
            "AQUACROP_CALIBRATION", "min_crop_fraction_for_calibration",
            fallback=0.05,
        )
        strategy = parser.get(
            "AQUACROP_CALIBRATION", "sampling_strategy",
            fallback="production_weighted",
        )
        seed = parser.getint(
            "AQUACROP_CALIBRATION", "calibration_seed", fallback=42,
        )

        sample_df = _paramcal.stratified_production_subsample(
            cells_df, n_total=n_total, density_multiplier=mult,
            min_cells_per_admin=min_per, max_cells_per_admin=max_per,
            min_crop_fraction=min_frac, strategy=strategy, seed=seed,
        )
        if sample_df.empty:
            logger.warning(f"Empty subsample for {country}/{ac_crop}")
            return None
        sampled_idx = set(sample_df["task_idx"].astype(int).tolist())
        sampled_anchor_tasks = [t for k, t in enumerate(anchor_tasks) if k in sampled_idx]
        logger.info(
            f"Calibration subsample: {len(sampled_anchor_tasks)} cells across "
            f"{sample_df['admin_id'].nunique()} admins (from {len(anchor_tasks)} total cells)"
        )

        # 4. Replicate subsample across all training years (per-year calendar).
        base_tasks_by_year: dict[int, list[_grid.CellTask]] = {}
        for combo in train_combos:
            y_tasks, _, _, _ = _build_cell_tasks(
                parser, country, canonical, ac_crop,
                combo["season"], combo["year"], gdf_admin, mask_path,
            )
            # Keep only cells present in our subsample (match by row, col).
            keep_keys = {(t.row, t.col) for t in sampled_anchor_tasks}
            base_tasks_by_year[combo["year"]] = [
                t for t in y_tasks if (t.row, t.col) in keep_keys
            ]

        # 5. Load observed yields via HarvestStat.
        # Build a dummy outlook frame with (Country, Region, Region_ID,
        # Harvest Year) so add_statistics can join observed yields.
        dummy_rows = []
        for year in base_tasks_by_year.keys():
            for _, ar in gdf_admin.iterrows():
                dummy_rows.append({
                    "Country": country.replace("_", " ").title(),
                    "Region": str(ar.get(admin_col, "")),
                    "Region_ID": ar.get(id_col, ""),
                    "Harvest Year": int(year),
                    "Predicted Yield (tn per ha)": np.nan,
                })
        dummy_df = pd.DataFrame(dummy_rows)
        observed_df = _join_harveststat(
            dummy_df, parser, country, canonical, admin_zone=admin_level,
        )
        # Pivot to (admin_id, year) → observed_yield (tn/ha). Region_ID
        # here is the same ADM_ID the cell_to_admin map uses.
        if "Observed Yield (tn per ha)" not in observed_df.columns:
            logger.warning(f"No observed yields joined for {country}/{ac_crop}")
            return None
        obs = observed_df.dropna(subset=["Observed Yield (tn per ha)"])
        obs = obs.rename(columns={
            "Region_ID": "admin_id",
            "Harvest Year": "year",
            "Observed Yield (tn per ha)": "observed_yield",
        })[["admin_id", "year", "observed_yield"]]
        obs = obs.set_index(["admin_id", "year"])
        if obs.empty:
            logger.warning(f"Empty observed yields for {country}/{ac_crop}")
            return None

        # 6. Build run_grid_fn closure that uses the per-country pool +
        #    bounds the caller already holds.
        def _run_grid_fn(tasks, pool=pool):
            return _grid.run_grid(
                tasks, config_files, country,
                n_workers=None,
                progress_desc=f"calib/{country}/{ac_crop}",
                country_bounds=country_bounds,
                pool=pool,
            )

        # 7. Build spec + problem + calibrator.
        spec = _paramspec.AquaCropParamSpec(ac_crop, params=params_list)
        problem = _paramcal.AquaCropPygmoProblem(
            specs=[spec],
            base_tasks_by_year=base_tasks_by_year,
            observed=obs,
            run_grid_fn=_run_grid_fn,
            pool=pool,
            cell_to_admin=cell_to_admin,
        )
        calibrator = _paramcal.AquaCropCalibrator(problem)
        calibrator.init()  # default pg.pso_gen
        pop = parser.getint(
            "AQUACROP_CALIBRATION", "pso_population_size", fallback=16,
        )
        gens = parser.getint(
            "AQUACROP_CALIBRATION", "pso_generations", fallback=30,
        )
        calibrator.optimize(population_size=pop, generations=gens)
        calibrator.apply_best()
        return spec, calibrator.best_fitness

    except Exception as exc:  # noqa: BLE001 — never kill the run on calibration failure
        logger.exception(
            "Parameter calibration failed for %s/%s: %s — defaults will be used",
            country, ac_crop, exc,
        )
        return None


def _run_one_combination(
    parser,
    combo: dict,
    db_path: Path,
    config_files: list[str],
    *,
    gdf_admin=None,
    pool=None,
    crop_param_overrides: Optional[dict] = None,
) -> Optional[pd.DataFrame]:
    """Run the full pipeline for one (country, crop, season, year).

    ``config_files`` is forwarded to ``grid_simulator.run_grid`` so worker
    subprocesses can rebuild their own ConfigParser from disk (avoids
    pickling ExtendedInterpolation).

    ``gdf_admin`` and ``pool`` are pre-built per country by the caller so
    all (crop, season, year) combos for one country share an admin
    boundary read + a worker pool with hot weather-cube caches. Passing
    these is optional — when ``None``, this function builds its own.
    """
    country = combo["country"]
    canonical_crop = combo["crop"]
    aquacrop_crop = combo["aquacrop_crop"]
    season = combo["season"]
    year = combo["year"]
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")

    logger.info(
        f"=== AquaCrop {country}/{canonical_crop} season={season} year={year} ==="
    )

    # Resolve admin level (admin_1 / admin_2) → boundary column for aggregation
    admin_level = parser.get(country, "admin_level", fallback="admin_1")
    admin_col = "ADM1_NAME" if admin_level == "admin_1" else "ADM2_NAME"

    # 1. Admin boundary — reuse caller-supplied gdf_admin when available
    # (the per-country loop in run() loads it once and threads it through
    # all combos for that country to skip repeated GPKG reads).
    if gdf_admin is None:
        try:
            gdf_admin = _load_admin_boundary(parser, country)
        except FileNotFoundError as exc:
            logger.error(f"Boundary missing for {country}: {exc}")
            return None
        if gdf_admin.empty:
            logger.error(f"Empty boundary for {country}")
            return None

    # 2. Crop mask path
    try:
        mask_path = _cmask.resolve_mask_path(parser, country, canonical_crop)
    except (FileNotFoundError, Exception) as exc:
        logger.error(f"Mask missing for {country}/{canonical_crop}: {exc}")
        return None

    # 3. Build cell tasks
    tasks, lons, lats, bounds = _build_cell_tasks(
        parser, country, canonical_crop, aquacrop_crop, season, year,
        gdf_admin, mask_path,
    )
    if not tasks:
        logger.warning(
            f"No cells to simulate for {country}/{canonical_crop}/"
            f"s{season}/{year} — likely calendar issue"
        )
        return None
    logger.info(f"Built {len(tasks)} cell tasks")

    # Apply calibrated crop parameter overrides if provided. Each task
    # gets the same dict (dataclass copy via dataclasses.replace would
    # be safer, but `slots=True` makes attribute assignment fine here).
    if crop_param_overrides:
        for _t in tasks:
            _t.crop_param_overrides = crop_param_overrides
        logger.info(
            f"Applied calibrated overrides to all {len(tasks)} tasks: {crop_param_overrides}"
        )

    # 4. Run grid simulator — config_files come in via the function arg so
    # worker subprocesses can rebuild their own ConfigParser from disk.
    if not config_files:
        logger.error("No config_files passed to _run_one_combination — cannot init workers")
        return None

    n_rows = len(lats)
    n_cols = len(lons)
    yield_grid = np.full((n_rows, n_cols), np.nan, dtype=np.float32)

    parallel = parser.getboolean("DEFAULT", "parallel_aquacrop", fallback=True)
    frac_cpus = parser.getfloat("DEFAULT", "fraction_cpus", fallback=0.3)
    n_workers = max(1, int((os.cpu_count() or 1) * frac_cpus)) if parallel else 1

    n_success = 0
    for result in _grid.run_grid(
        tasks, config_files, country, n_workers=n_workers,
        progress_desc=f"{country}/{canonical_crop}/{year}",
        country_bounds=bounds,
        pool=pool,
    ):
        if result.success and np.isfinite(result.yield_tha):
            yield_grid[result.row, result.col] = result.yield_tha
            n_success += 1
    logger.info(f"AquaCrop simulations: {n_success}/{len(tasks)} successful")

    if n_success == 0:
        return None

    # 5. Write raster
    write_raster = parser.getboolean("AQUACROP", "write_raster", fallback=True)
    raster_path = None
    if write_raster:
        dir_output = Path(parser.get("PATHS", "dir_output"))
        raster_path = (
            dir_output / project_name / "aquacrop" / "raster"
            / f"{country}_{canonical_crop}_{year}_s{season}.tif"
        )
        _out.write_yield_raster(
            yield_grid, bounds, raster_path,
            crop=canonical_crop, country=country,
            year=year, season=season,
        )
        logger.info(f"Wrote yield raster: {raster_path}")

    # 6. Aggregate to admin polygons
    if raster_path is None:
        # Need a raster on disk for geom_extract — write to a temp location
        # under the project's raster dir.
        dir_output = Path(parser.get("PATHS", "dir_output"))
        raster_path = (
            dir_output / project_name / "aquacrop" / "raster"
            / f"{country}_{canonical_crop}_{year}_s{season}.tif"
        )
        _out.write_yield_raster(
            yield_grid, bounds, raster_path,
            crop=canonical_crop, country=country, year=year, season=season,
        )

    agg_df = _out.aggregate_raster_to_admin(
        yield_raster_path=raster_path,
        mask_raster_path=mask_path,
        admin_gdf=gdf_admin,
        region_col=admin_col,
        region_id_col="ADM_ID" if "ADM_ID" in gdf_admin.columns else admin_col,
        context_prefix=f"{country}/{canonical_crop}/{year}",
    )
    logger.info(f"Aggregated to {len(agg_df)} admin regions")

    # 7. Build outlook DataFrame in geocif schema
    cal_df = _cal.load_calendar(parser, country, canonical_crop, season, year)
    plant_date = cal_df.iloc[0]["planting_date"]
    harvest_date = cal_df.iloc[0]["harvest_date"]
    # Match geocif stage convention so downstream residuals_vs_cid /
    # compare_forecasts joins on (Country, Region, Harvest Year, Stage Name)
    # find AquaCrop rows alongside CatBoost / TabPFN rows:
    #   Stage_ID  = harvest_month_down_to_plant_month (monthly_r ordering)
    #              e.g. Apr→Jul = "7_6_5_4"
    #   Stage Name = "<plant_mon> 1-<harvest_mon> <last_day>" no spaces around dash
    #              e.g. "Apr 1-Jul 31"
    def _months_in_span(start, end):
        months = []
        cur_y, cur_m = start.year, start.month
        end_y, end_m = end.year, end.month
        while (cur_y, cur_m) <= (end_y, end_m):
            months.append(cur_m)
            cur_m += 1
            if cur_m > 12:
                cur_m = 1
                cur_y += 1
        return months
    _span_months = _months_in_span(plant_date, harvest_date)
    stage_id = "_".join(str(m) for m in reversed(_span_months))
    # Last day of the harvest month (matches geocif Stage Name convention
    # "<plant_mon> 1-<harvest_mon> <last_day>"). Bin index for the second
    # half of month m is m*2 - 1 under the bi-monthly schema (jan_15=1,
    # feb_15=3, ..., jul_15=13, ...), and edge="end" gives that bin's
    # last DOY = the month's last day.
    _last_dom = _cal._bin_to_doy(harvest_date.month * 2 - 1, harvest_date.year, edge="end")
    _last_dom_date = _dt.date(harvest_date.year, 1, 1) + _dt.timedelta(days=_last_dom - 1)
    stage_name = (
        f"{plant_date.strftime('%b')} 1-"
        f"{harvest_date.strftime('%b')} {_last_dom_date.day}"
    )

    df_outlook = _out.build_db_dataframe(
        agg_df=agg_df,
        country=country,
        crop=canonical_crop,
        harvest_year=year,
        season=season,
        stage_name=stage_name,
        stage_id=stage_id,
        model_name=parser.get("AQUACROP", "model_name", fallback="aquacrop"),
        experiment_name=parser.get(
            "AQUACROP", "experiment_name", fallback="aquacrop_v1",
        ),
    )

    # 8. Join HarvestStat
    admin_zone_col = admin_level if admin_level in ("admin_1", "admin_2") else "admin_1"
    df_outlook = _join_harveststat(
        df_outlook, parser, country, canonical_crop, admin_zone_col,
    )

    # 9. Write DB row (uncalibrated — calibration happens after LOOCV
    # aggregates across years). One row per (country, region, year, season).
    write_db = parser.getboolean("AQUACROP", "write_db_rows", fallback=True)
    if write_db:
        _out.write_db_rows(df_outlook, db_path, country, canonical_crop)
        logger.info(f"Wrote {len(df_outlook)} rows to {db_path}")

    return df_outlook


def run(path_config_files: list[str]) -> None:
    """Main entry point.

    Args:
        path_config_files: List of config file paths (typically
            [geobase.txt, countries.txt, crops.txt, aquacrop.txt]).
    """
    logger_, parser = _setup_logger_parser(path_config_files)
    # Worker subprocesses can't pickle the ConfigParser (ExtendedInterpolation
    # isn't pickle-clean) — they rebuild from disk. So we keep the file paths
    # around and pass them through to _run_one_combination → run_grid as a
    # plain list of strings.
    config_file_strings = [str(p) for p in path_config_files]

    # Print Rich panel summary (geocif convention)
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        console = Console()
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style="bold cyan", no_wrap=True)
        table.add_column()
        table.add_row("Version", f"geocif {__version__}")
        table.add_row("Usage", "from geocif.aquacrop import aquacrop_runner; aquacrop_runner.run(cfg)")
        table.add_row("cfg", str([str(p) for p in path_config_files]))
        countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
        table.add_row("Countries", str(countries))
        table.add_row(
            "Years",
            f"{parser.getint('DEFAULT', 'start_year')} - "
            f"{parser.getint('DEFAULT', 'end_year')}",
        )
        table.add_row("Calibration", parser.get("AQUACROP", "calibration"))
        table.add_row("Calibration pool", parser.get("AQUACROP", "calibration_pool"))
        console.print(Panel(
            table, title="[bold bright_white]AquaCrop-OSPy Runner[/]",
            border_style="bright_green", padding=(1, 2),
        ))
    except ImportError:
        pass

    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    combos = _build_run_combinations(parser, countries)
    logger_.info(f"Built {len(combos)} (country, crop, season, year) combinations")

    db_path = _out.make_db_path(
        parser,
        project_name=parser.get("DEFAULT", "project_name", fallback="geocif"),
    )
    logger_.info(f"DB path: {db_path}")

    # Group combos by country so each country gets ONE Pool with ONE
    # set of worker weather-cube caches that persist across all years.
    # Saves ~25× spawn overhead + 25× cube reloads for a 25-year run.
    import multiprocessing as mp

    combos_by_country: dict[str, list[dict]] = {}
    for c in combos:
        combos_by_country.setdefault(c["country"], []).append(c)

    parallel = parser.getboolean("DEFAULT", "parallel_aquacrop", fallback=True)
    frac_cpus = parser.getfloat("DEFAULT", "fraction_cpus", fallback=0.3)
    n_workers = max(1, int((os.cpu_count() or 1) * frac_cpus)) if parallel else 1

    all_outlook = []
    for country, country_combos in combos_by_country.items():
        # Load admin boundary once per country
        try:
            gdf_admin = _load_admin_boundary(parser, country)
        except FileNotFoundError as exc:
            logger_.error(f"Boundary missing for {country}: {exc} — skipping country")
            continue
        if gdf_admin.empty:
            logger_.error(f"Empty boundary for {country} — skipping country")
            continue

        country_bounds = _snap_country_bounds(gdf_admin)

        # Open one Pool per country with bounds-aware worker init —
        # workers and their weather-cube caches persist across all
        # (crop, season, year) combos for this country.
        own_pool = None
        if parallel and n_workers > 1:
            ctx = mp.get_context("spawn")
            own_pool = ctx.Pool(
                processes=n_workers,
                initializer=_grid._worker_init,
                initargs=(config_file_strings, country, country_bounds),
            )
            logger_.info(
                f"Opened pool for {country}: {n_workers} workers, "
                f"country_bounds={country_bounds}"
            )

        # Optional: PyGMO PSO calibration of internal AquaCrop crop params
        # against HarvestStat observed yields. Returns a per-crop overrides
        # dict; if empty (off / cached miss / fit failure), all cells use
        # AquaCrop defaults exactly as before.
        try:
            param_overrides = _maybe_calibrate_params(
                parser, country, country_combos, gdf_admin,
                country_bounds, own_pool, config_file_strings,
            )
        except Exception as exc:  # noqa: BLE001 — never kill the run on calibration
            logger_.exception(
                "Param calibration phase crashed for %s: %s — using defaults",
                country, exc,
            )
            param_overrides = {}

        try:
            for combo in country_combos:
                df = _run_one_combination(
                    parser, combo, db_path, config_file_strings,
                    gdf_admin=gdf_admin,
                    pool=own_pool,
                    crop_param_overrides=param_overrides.get(combo["aquacrop_crop"]),
                )
                if df is not None:
                    all_outlook.append(df)
        finally:
            if own_pool is not None:
                own_pool.close()
                own_pool.join()
                logger_.info(f"Closed pool for {country}")

    if not all_outlook:
        logger_.warning("No successful AquaCrop runs — nothing to calibrate")
        return

    # LOOCV calibration across the full multi-year dataset
    cal_mode = parser.get("AQUACROP", "calibration", fallback="region_anomaly")
    if cal_mode != "none":
        pool = parser.get("AQUACROP", "calibration_pool", fallback="cross_country")
        logger_.info(f"Applying LOOCV {cal_mode} calibration (pool={pool})")
        combined = pd.concat(all_outlook, ignore_index=False)

        # Cross-country pooling never spans crops. Fit one model per crop
        # (residuals between maize and rice are not exchangeable), then
        # pool across countries within that crop.
        cal_frames = []
        for crop_name, crop_block in combined.groupby("Crop"):
            cal_frames.append(_calib.loocv_calibrate(crop_block, pool=pool))
        calibrated = pd.concat(cal_frames, ignore_index=False).sort_index()

        # Re-write DB rows with calibrated predictions under a
        # '<experiment_name>_calibrated' experiment.
        cal_exp = parser.get(
            "AQUACROP", "experiment_name", fallback="aquacrop_v1",
        ) + "_calibrated"
        calibrated["Experiment Name"] = cal_exp

        # Group by (Country, Crop) and write one chunk per table — matches
        # the geocif yield_outlook table-per-(country, crop) convention.
        n_written = 0
        for (country_name, crop_name), chunk in calibrated.groupby(["Country", "Crop"]):
            if parser.getboolean("AQUACROP", "write_db_rows", fallback=True):
                _out.write_db_rows(chunk, db_path, country_name, crop_name)
                n_written += len(chunk)
        logger_.info(
            f"Wrote {n_written} calibrated rows under experiment '{cal_exp}'"
        )

        # Use calibrated frame for downstream validation so diagnostics
        # reflect the published (calibrated) outputs.
        validation_df = calibrated
    else:
        validation_df = pd.concat(all_outlook, ignore_index=False)

    # Validation diagnostics
    if parser.getboolean("AQUACROP", "validation", fallback=True):
        dir_output = Path(parser.get("PATHS", "dir_output"))
        project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
        diag_dir = dir_output / project_name / "aquacrop" / "diagnostics"
        # One diagnostic suite per (country, crop) so plots scoped properly.
        for (country_name, crop_name), chunk in validation_df.groupby(["Country", "Crop"]):
            label = f"aquacrop_{country_name}_{crop_name}"
            summary = _val.run_full_diagnostics(chunk, diag_dir, label=label)
            logger_.info(
                f"{label} pooled metrics:\n{summary['pooled'].to_string(index=False)}"
            )
        # Cross-country pooled summary too
        pooled_summary = _val.run_full_diagnostics(
            validation_df, diag_dir, label="aquacrop_pooled",
        )
        logger_.info(
            f"Cross-country pooled metrics:\n{pooled_summary['pooled'].to_string(index=False)}"
        )

    logger_.info("AquaCrop run complete.")


if __name__ == "__main__":
    import sys
    cfgs = sys.argv[1:] if len(sys.argv) > 1 else [
        "config/geobase.txt", "config/countries.txt",
        "config/crops.txt", "config/aquacrop.txt",
    ]
    run(cfgs)
