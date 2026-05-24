"""
grid_simulator.py — orchestrate per-cell AquaCrop-OSPy simulations across
a 5 km grid covering a country boundary.

Designed for ``multiprocessing.Pool`` execution:
- Each worker initializes its own ``WeatherReader`` + ``SoilReader``
  (rasterio handles are NOT fork-safe).
- Cells are streamed via ``imap_unordered`` so progress bars work.
- Result is a list of (row_idx, col_idx, yield, biomass) tuples that the
  caller writes into a yield raster.

Performance notes:
- Cell-loop AquaCrop simulation is ~0.2-2 s per cell on a typical HPC
  core. For a country of ~5000 cells × 25 years × 1-2 seasons = 125k-250k
  simulations. At ~15 cores × 1 s/cell that's 2-5 hours per country.
- Memory: each worker holds ~10 rasterio handles (RasterCache size 100
  for weather + 4 for soil + 1 for mask = ~105 file descriptors). Pool of
  16 workers ⇒ ~1700 fds — well below the typical 65k Linux limit.
"""

from __future__ import annotations

import logging
import multiprocessing as mp
import os
from dataclasses import dataclass
from datetime import date as _date
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd

# Heads-up to aquacrop-ospy: skip AOT compilation for now (matches
# upstream guidance for environments without MSVC; harmless elsewhere).
os.environ.setdefault("DEVELOPMENT", "DEVELOPMENT")

from .soil import SoilReader, build_aquacrop_soil  # noqa: E402
from .weather import WeatherReader  # noqa: E402


# Typical Harvest Index (yield / total biomass) by AquaCrop built-in crop.
# Used to back-calculate biomass when AquaCrop's v3 final-stats frame
# doesn't expose biomass directly. Values from AquaCrop default crop
# parameter files + FAO HI tables — adequate for diagnostic biomass; for
# higher-fidelity output add a custom AquaCrop output hook.
_HI_BY_CROP = {
    "Maize": 0.45, "MaizeGDD": 0.45,
    "Wheat": 0.45, "WheatGDD": 0.45,
    "PaddyRice": 0.45, "Rice": 0.45,
    "Sorghum": 0.35,
    "Soybean": 0.40,
    "Cotton": 0.40,
    "Barley": 0.45,
    "DryBean": 0.35,
    "Sunflower": 0.40,
    "Tef": 0.35,
    "Tomato": 0.55,
    "Potato": 0.70,      # root crop — yield is most of biomass
    "SugarBeet": 0.70,   # root crop
    "SugarCane": 0.40,
    "Quinoa": 0.40,
}
_HI_DEFAULT = 0.40

# Fail-fast import of aquacrop-ospy. Previously imported inside
# _worker_simulate, so a missing install showed up as N silent "no module"
# strings in CellResult.error — one per cell × per worker. Doing the import
# up-front gives one clear error message at process start instead.
try:
    from aquacrop import (  # noqa: E402,F401
        AquaCropModel, Crop, InitialWaterContent, IrrigationManagement,
    )
except ImportError as _aquacrop_import_err:  # pragma: no cover
    raise ImportError(
        "aquacrop-ospy is required to run geocif.aquacrop. "
        "Install with `pip install aquacrop` (see "
        "https://aquacropos.github.io/aquacrop/ for HPC notes)."
    ) from _aquacrop_import_err

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class CellTask:
    """Inputs needed to simulate a single (row, col, lon, lat) cell."""
    row: int
    col: int
    lon: float
    lat: float
    crop_fraction: float          # 0..1
    calendar_region: str          # for selecting the right planting/harvest
    sim_start: _date
    sim_end: _date
    crop_aquacrop_name: str       # e.g. 'Maize', 'Wheat', 'Rice'
    planting_date_str: str        # 'MM/DD' for aquacrop.Crop()
    harvest_year: int             # for the DB row Harvest Year
    # Optional overrides set by AquaCropParamSpec.apply (param_calibration.py).
    # None ⇒ AquaCrop defaults; otherwise dict like {"HI0": 0.42, "WP": 17.5}.
    crop_param_overrides: Optional[dict] = None


@dataclass(slots=True)
class CellResult:
    """One cell's simulation output."""
    row: int
    col: int
    yield_tha: float
    biomass_tha: float
    success: bool
    error: str = ""


# Module-level worker state — initialized once per process, reused across
# tasks. Avoids re-opening the same rasterio datasets for every task.
_WEATHER: Optional[WeatherReader] = None
_SOIL: Optional[SoilReader] = None
_PARSER = None


def _worker_init(config_files: list[str], country: str, country_bounds=None):
    """Per-worker initializer — runs once when each Pool worker starts.

    Builds the ConfigParser from disk (rather than passing the parsed
    object through pickle, which is brittle for ExtendedInterpolation).
    Constructs WeatherReader and SoilReader so each task in this worker
    reuses the same RasterCache + open soil datasets.

    ``country`` selects the per-country AgERA5 subtree
    (``${dir_intermed}/agera5/{country_slug}/tif/...``).
    ``country_bounds`` is forwarded to WeatherReader so the per-(var, year)
    cube cache clips daily TIFs to the country box — critical for memory
    (global cube would be ~1.5 GB per var-year; country-clipped is ~3 MB).
    """
    global _WEATHER, _SOIL, _PARSER
    from configparser import ConfigParser, ExtendedInterpolation

    # inline_comment_prefixes=(';',) matches geoprepare.utils.read_config —
    # without it, `key = value ; comment` is parsed with the comment kept
    # inside the value, so subsequent parser.getint/getfloat calls explode
    # on the trailing text.
    parser = ConfigParser(
        interpolation=ExtendedInterpolation(),
        inline_comment_prefixes=(';',),
    )
    parser.read(config_files)
    _PARSER = parser
    _WEATHER = WeatherReader(parser, country=country, country_bounds=country_bounds)
    _SOIL = SoilReader(parser, country=country)


def _worker_simulate(task: CellTask) -> CellResult:
    """Run AquaCrop for one cell. Designed to never raise out of the worker."""
    global _WEATHER, _SOIL
    try:
        # 1. Soil
        props = _SOIL.get_properties(task.lon, task.lat)
        if props is None:
            return CellResult(task.row, task.col, np.nan, np.nan,
                              False, "no soil")

        soil = build_aquacrop_soil(props)

        # 2. Weather
        wdf = _WEATHER.get_weather_df(
            task.lon, task.lat, task.sim_start, task.sim_end,
        )
        if wdf is None:
            return CellResult(task.row, task.col, np.nan, np.nan,
                              False, "no weather")

        # 3. AquaCrop run — imported at module top for fail-fast behaviour
        init_wc_setting = _PARSER.get(
            "AQUACROP", "initial_water_content", fallback="FC",
        )
        # InitialWaterContent accepts either a list of labels ('FC','WP','SAT')
        # or wc_type='Pct' + numeric percentage.
        try:
            pct = float(init_wc_setting)
            init_wc = InitialWaterContent(wc_type="Pct", value=[pct])
        except ValueError:
            init_wc = InitialWaterContent(value=[init_wc_setting])

        irr_method = _PARSER.getint("AQUACROP", "irrigation_method", fallback=0)
        irr_mngt = IrrigationManagement(irrigation_method=irr_method)

        crop = Crop(task.crop_aquacrop_name, planting_date=task.planting_date_str)
        if task.crop_param_overrides:
            for _k, _v in task.crop_param_overrides.items():
                setattr(crop, _k, _v)

        model = AquaCropModel(
            sim_start_time=task.sim_start.strftime("%Y/%m/%d"),
            sim_end_time=task.sim_end.strftime("%Y/%m/%d"),
            weather_df=wdf,
            soil=soil,
            crop=crop,
            initial_water_content=init_wc,
            irrigation_management=irr_mngt,
        )
        model.run_model(till_termination=True)
        results = model.get_simulation_results()

        if results.empty:
            return CellResult(task.row, task.col, np.nan, np.nan,
                              False, "empty results")

        row = results.iloc[-1]
        # AquaCrop-OSPy v3 column naming
        yld = float(row.get(
            "Dry yield (tonne/ha)",
            row.get("Yield (tonne/ha)", np.nan),
        ))
        # Biomass not exported in the v3 final stats frame; approximate via
        # yield / per-crop HI. See _HI_BY_CROP above for sources.
        hi = _HI_BY_CROP.get(task.crop_aquacrop_name, _HI_DEFAULT)
        biomass = yld / hi if np.isfinite(yld) and hi > 0 else np.nan

        return CellResult(task.row, task.col, yld, biomass, True)

    except Exception as exc:  # noqa: BLE001 — never crash a worker on a bad cell
        return CellResult(task.row, task.col, np.nan, np.nan, False, str(exc)[:120])


def run_grid(
    tasks: list[CellTask],
    config_files: list[str],
    country: str,
    n_workers: Optional[int] = None,
    progress_desc: str = "AquaCrop cells",
    country_bounds=None,
    pool=None,
) -> Iterable[CellResult]:
    """Run AquaCrop in parallel across the supplied cell tasks.

    Args:
        tasks: List of CellTask, one per non-masked cell.
        config_files: Config file paths for worker initializer.
        country: country name — picks the per-country AgERA5 subtree
            (``${dir_intermed}/agera5/{country_slug}/tif/...``).
        n_workers: Pool size. Defaults to int(cpu_count * fraction_cpus)
            from the parser if available, else cpu_count // 2.
        progress_desc: tqdm description.
        country_bounds: (minx, miny, maxx, maxy) — forwarded to
            WeatherReader so the cube cache stays bounded. Strongly
            recommended; without it the cache holds full-global cubes.
        pool: Optional pre-initialized ``multiprocessing.Pool``. When
            provided, this function reuses it instead of creating a new
            one — letting the per-(var, year) weather cube cache persist
            across multiple ``run_grid`` calls (e.g. iterating years for
            the same country). The caller is responsible for closing the
            pool. When None (default), a new Pool is created and torn
            down for this invocation.

    Yields:
        CellResult objects (in arbitrary order — caller must use row/col).
    """
    if n_workers is None:
        from configparser import ConfigParser, ExtendedInterpolation
        p = ConfigParser(interpolation=ExtendedInterpolation())
        p.read(config_files)
        frac = p.getfloat("DEFAULT", "fraction_cpus", fallback=0.3)
        n_workers = max(1, int(os.cpu_count() * frac))

    # Defer the geocif progress import so the module is importable in
    # standalone testing without geocif installed.
    try:
        from geocif.progress import pbar as _pbar  # type: ignore
    except ImportError:
        from tqdm import tqdm as _pbar  # type: ignore

    # Caller-supplied pool path — reuse workers + cube cache across calls.
    if pool is not None:
        for result in _pbar(
            pool.imap_unordered(_worker_simulate, tasks, chunksize=8),
            total=len(tasks),
            desc=progress_desc,
            leave=False,
        ):
            yield result
        return

    if n_workers == 1:
        # Single-process path for debugging — same worker state model.
        _worker_init(config_files, country, country_bounds=country_bounds)
        try:
            for task in _pbar(tasks, desc=progress_desc, leave=False):
                yield _worker_simulate(task)
        finally:
            if _WEATHER is not None:
                _WEATHER.close()
            if _SOIL is not None:
                _SOIL.close()
        return

    ctx = mp.get_context("spawn")  # safer than fork for rasterio
    with ctx.Pool(
        processes=n_workers,
        initializer=_worker_init,
        initargs=(config_files, country, country_bounds),
    ) as own_pool:
        for result in _pbar(
            own_pool.imap_unordered(_worker_simulate, tasks, chunksize=8),
            total=len(tasks),
            desc=progress_desc,
            leave=False,
        ):
            yield result
