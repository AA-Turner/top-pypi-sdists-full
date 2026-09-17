# -*- coding: utf-8 -*-
"""Multi-year pixel phenology climatology (DESIGN.md sections 7 and 11.1).

What this module produces
-------------------------
For one ``(country, crop, season)`` and a list of **harvest years** it builds

* per year, seven GeoTIFFs of the season as it actually ran -- ``sos``, ``eos``,
  ``lgs``, ``first_candidate`` and ``n_false_starts`` (int16), ``sos_status``
  and ``eos_status`` (int8);
* one summary stack over those years -- ``onset_median``, ``onset_p25``,
  ``onset_p75``, ``onset_std``, ``onset_n_valid``, ``onset_frac_no_onset``,
  ``false_start_rate``, ``eos_median``, ``lgs_median``, ``eos_frac_censored``,
  ``eos_frac_at_floor``;
* ``pet_calibration.tif``, the 12-band per-month Hargreaves-to-``etref``
  correction of DESIGN section 11.1;
* ``manifest.json`` describing the build.

Units and index conventions
---------------------------
* **Every day layer is in days since THAT PIXEL's own calendar planting start**
  (``sos = 0`` means onset on the planting date, ``sos = -12`` means twelve days
  before it -- the search opens ``search_start_days_before_planting`` days early,
  so negative values are normal). ``lgs = eos - sos`` in days. int16 rasters use
  ``-32768`` for nodata, int8 status rasters use ``-1``.
* Status rasters carry :class:`geocif.phenology.core.OnsetStatus` /
  :class:`~geocif.phenology.core.CessationStatus` codes, except ``-1`` which
  means "no calendar covers this pixel" (distinct from ``NO_DATA = 3``, which
  means the calendar is there but the rain is not).
* Rain and PET are mm/day; PET calibration factors ``k`` are dimensionless.
* Fractions (``*_frac_*``, ``false_start_rate``) are shares in ``[0, 1]``;
  ``onset_n_valid`` is a count of years.

``n_false_starts`` -- which of the two meanings
----------------------------------------------
``core.season_phenology`` counts **every** candidate episode before onset while
``core.onset_state`` counts only the **invalidated** ones (a candidate followed
by a qualifying dry spell inside its look-ahead). The two disagree by the onset
episode itself and by any episode whose look-ahead ran off the end of the array.
This module uses the **invalidated-episode** meaning everywhere -- it is the one
the monitor reports and the one ``false_start_rate`` is named after -- so the
per-year count comes from ``core.onset_state`` even though every other layer
comes from ``core.season_phenology``. ``core.py`` is not modified.

Caching
-------
The cache directory is **not** date-stamped::

    ${PATHS:dir_output}/{project_name}/phenology/climatology/{country}/{crop}/s{season}/
        manifest.json
        pet_calibration.tif
        onset_median.tif ... eos_frac_at_floor.tif
        years/sos_1999.tif ...

``manifest.json`` carries a params hash over the algorithm parameters, the year
list, the grid and the identity of the run; :func:`build_climatology` rebuilds
when ``rebuild=True`` or that hash differs, and otherwise returns the paths that
are already on disk. Years are processed in a
:class:`~concurrent.futures.ProcessPoolExecutor`; a year that fails is logged
and skipped, never fatal.

No icclim, no pygmt, no CID code is imported here.
"""

from __future__ import annotations

import calendar as _calendar
import datetime as _dt
import hashlib
import json
import logging
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

import numpy as np
import rasterio
from affine import Affine
from rasterio.windows import Window

from geocif.phenology import core, inputs
from geocif.phenology.outputs import write_geotiff

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
#: Nodata for every int16 day / count raster written here.
INT16_NODATA: int = -32768

#: Nodata for the int8 status rasters ("no calendar covers this pixel").
STATUS_NODATA: int = int(core.NODATA_STATUS)

#: Hard clip on the monthly PET calibration factor (DESIGN section 11.1).
PET_K_MIN: float = 0.5
PET_K_MAX: float = 2.0

#: Factor used where a month has no usable record anywhere in the window.
PET_K_FALLBACK: float = 1.0

MANIFEST_FILE: str = "manifest.json"
PET_CALIBRATION_FILE: str = "pet_calibration.tif"
YEAR_SUBDIR: str = "years"

#: Per-year layers, in write order: name -> (dtype, nodata).
YEAR_LAYERS: dict[str, tuple[str, float]] = {
    "sos": ("int16", INT16_NODATA),
    "eos": ("int16", INT16_NODATA),
    "lgs": ("int16", INT16_NODATA),
    "sos_status": ("int8", STATUS_NODATA),
    "eos_status": ("int8", STATUS_NODATA),
    "first_candidate": ("int16", INT16_NODATA),
    "n_false_starts": ("int16", INT16_NODATA),
}

#: Summary layers, in write order: name -> (dtype, nodata).
SUMMARY_LAYERS: dict[str, tuple[str, float]] = {
    "onset_median": ("float32", np.nan),
    "onset_p25": ("float32", np.nan),
    "onset_p75": ("float32", np.nan),
    "onset_std": ("float32", np.nan),
    "onset_n_valid": ("int16", INT16_NODATA),
    "onset_frac_no_onset": ("float32", np.nan),
    "false_start_rate": ("float32", np.nan),
    "eos_median": ("float32", np.nan),
    "lgs_median": ("float32", np.nan),
    "eos_frac_censored": ("float32", np.nan),
    "eos_frac_at_floor": ("float32", np.nan),
}

#: Units written into every raster's GeoTIFF tags.
LAYER_UNITS: dict[str, str] = {
    "sos": "days since pixel planting start",
    "eos": "days since pixel planting start",
    "lgs": "days",
    "sos_status": "OnsetStatus code (-1 = no calendar)",
    "eos_status": "CessationStatus code (-1 = no calendar)",
    "first_candidate": "days since pixel planting start",
    "n_false_starts": "count of invalidated candidate episodes",
    "onset_median": "days since pixel planting start",
    "onset_p25": "days since pixel planting start",
    "onset_p75": "days since pixel planting start",
    "onset_std": "days",
    "onset_n_valid": "count of years",
    "onset_frac_no_onset": "share of years in 0..1",
    "false_start_rate": "share of years with at least one invalidated candidate, 0..1",
    "eos_median": "days since pixel planting start",
    "lgs_median": "days",
    "eos_frac_censored": "share of onset years right-censored, 0..1",
    "eos_frac_at_floor": "share of cessation years at the minimum-season floor, 0..1",
}


# ---------------------------------------------------------------------------
# 7.1 Parameters
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ClimatologyParams:
    """Everything that changes the numbers, and therefore the cache hash.

    Attributes:
        onset: onset detector parameters (mm, days).
        cessation: bucket-model cessation parameters (mm, days).
        search_start_days_before_planting: the onset search opens this many days
            before the pixel's calendar planting start (days).
        cessation_grace_days: the cessation search may run this many days past
            the calendar harvest date (days); it is additionally capped at the
            next season's planting start minus one day and at the last day of
            the cube.
        min_valid_years: a pixel needs this many years with an onset before the
            median / quartile layers are written (years).
        pet_calibration_years: calendar years of the etref-vs-Hargreaves
            overlap used to fit the monthly factor.
        pet_calibration_min_years: a pixel-month needs this many valid years
            before its own factor is used; below it the window median stands in.
        pet_calibration_min_days_per_month: a pixel-year-month needs this many
            days with both etref and Hargreaves finite to count as valid.
        max_missing_day_fraction: reject a harvest year when more than this
            share of its daily CHIRPS files are absent. A gap is NOT harmless:
            a missing day reads as NaN, which adds 0 mm to the accumulation but
            does not count as a dry day, so it can break the dry spell that
            would have invalidated a false start and turn it into a confident
            onset tens of days early.
        pet_calibration_day_stride: read every Nth day of each month when
            fitting the factor (1 = every day).
    """

    onset: core.OnsetParams = core.OnsetParams()
    cessation: core.CessationParams = core.CessationParams()
    search_start_days_before_planting: int = 30
    cessation_grace_days: int = 60
    min_valid_years: int = 20
    pet_calibration_years: tuple[int, ...] = tuple(range(2001, 2021))
    pet_calibration_min_years: int = 5
    pet_calibration_min_days_per_month: int = 5
    pet_calibration_day_stride: int = 1
    max_missing_day_fraction: float = 0.05

    def to_dict(self) -> dict:
        """JSON-ready nested dict of every parameter (units per the docstring)."""
        out = asdict(self)
        out["pet_calibration_years"] = [int(y) for y in self.pet_calibration_years]
        return out

    @classmethod
    def from_parser(cls, parser, crop: Optional[str] = None) -> "ClimatologyParams":
        """Read ``[SEASON_MONITOR]`` (DESIGN section 8.1); every option is optional.

        ``min_season_days_{crop}`` overrides ``min_season_days`` for ``crop``.
        """

        def _f(key: str, default: float) -> float:
            return float(parser.get("SEASON_MONITOR", key, fallback=default))

        def _i(key: str, default: int) -> int:
            return int(float(parser.get("SEASON_MONITOR", key, fallback=default)))

        min_season = _i("min_season_days", core.CessationParams.min_season_days)
        if crop:
            min_season = _i(f"min_season_days_{crop}", min_season)
        onset = core.OnsetParams(
            precip_threshold=_f("precip_threshold", core.OnsetParams.precip_threshold),
            window_days=_i("window_days", core.OnsetParams.window_days),
            dry_spell_days=_i("dry_spell_days", core.OnsetParams.dry_spell_days),
            dry_day_threshold=_f("dry_day_threshold", core.OnsetParams.dry_day_threshold),
            validation_days=_i("validation_days", core.OnsetParams.validation_days),
        )
        cessation = core.CessationParams(
            soil_whc=_f("soil_whc", core.CessationParams.soil_whc),
            min_season_days=min_season,
            empty_persist_days=_i("empty_persist_days", core.CessationParams.empty_persist_days),
            initial_storage=_f("initial_storage", core.CessationParams.initial_storage),
        )
        return cls(
            onset=onset,
            cessation=cessation,
            search_start_days_before_planting=_i("search_start_days_before_planting", 30),
            cessation_grace_days=_i("cessation_grace_days", 60),
            min_valid_years=_i("min_valid_years", 20),
        )


def params_hash(
    params: ClimatologyParams,
    country: str,
    crop: str,
    season: int,
    years: Sequence[int],
    shape: tuple[int, int],
    bounds: tuple[float, float, float, float],
) -> str:
    """Stable sha256 of everything a cached build depends on.

    Covers the algorithm parameters, the identity of the run, the harvest-year
    list and the grid, so one equality test against the manifest answers "may I
    reuse this cache?".
    """
    payload = {
        "params": params.to_dict(),
        "country": str(country),
        "crop": str(crop),
        "season": int(season),
        "years": [int(y) for y in years],
        "shape": [int(shape[0]), int(shape[1])],
        "bounds": [round(float(b), 9) for b in bounds],
    }
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def params_hash_for(
    parser,
    country: str,
    crop: str,
    season: int,
    years: Sequence[int],
    params: ClimatologyParams,
) -> Optional[str]:
    """:func:`params_hash` for a run, deriving the grid the way the build does.

    The hash covers the window, which only :func:`build_climatology` normally
    computes. A caller that wants to check a cache before trusting it -- rather
    than re-deriving the bbox and risking a different answer -- uses this.

    Returns:
        The hash, or ``None`` when the window cannot be derived (no boundary
        file, unreadable config); the caller should then skip the check rather
        than treat it as a mismatch.
    """
    try:
        bbox = inputs.country_bbox(parser, country)
        _window, transform, shape = inputs.window_for_bbox(bbox)
    except Exception as exc:  # noqa: BLE001 - "cannot check" is not "mismatch"
        logger.warning(f"cannot derive the grid for {country}: {exc}")
        return None
    return params_hash(
        params, country, crop, season, years, shape, _bounds_of(transform, shape)
    )


def climatology_dir(parser, country: str, crop: str, season: int) -> Path:
    """The (not date-stamped) cache directory for one country / crop / season.

    ``${PATHS:dir_output}/{project_name}/phenology/climatology/{country}/{crop}/s{season}``,
    with ``project_name`` from ``[DEFAULT] project_name`` (``geocif`` if absent).
    """
    root = Path(parser.get("PATHS", "dir_output"))
    project = parser.get("DEFAULT", "project_name", fallback="geocif")
    return root / project / "phenology" / "climatology" / country / crop / f"s{int(season)}"


# ---------------------------------------------------------------------------
# 7.2 Small raster / date helpers
# ---------------------------------------------------------------------------
def _bounds_of(transform: Affine, shape: tuple[int, int]) -> tuple[float, float, float, float]:
    """``(west, south, east, north)`` in degrees of a north-up window."""
    rows, cols = int(shape[0]), int(shape[1])
    west = float(transform.c)
    north = float(transform.f)
    east = west + cols * float(transform.a)
    south = north + rows * float(transform.e)
    return (west, south, east, north)


def _write_multiband(
    path: Any,
    arr: np.ndarray,
    transform: Affine,
    nodata: float,
    dtype: str,
    tags: Optional[dict] = None,
    crs: str = "EPSG:4326",
) -> Path:
    """Write a ``(bands, rows, cols)`` cube to one tiled, LZW-compressed GeoTIFF."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = np.asarray(arr)
    if data.ndim != 3:
        raise ValueError(f"_write_multiband expects a 3-D array, got shape {data.shape}")
    if np.issubdtype(data.dtype, np.floating) and np.isfinite(nodata):
        data = np.where(np.isfinite(data), data, nodata)
    data = data.astype(dtype, copy=False)
    bands, height, width = data.shape
    profile = {
        "driver": "GTiff",
        "dtype": dtype,
        "width": width,
        "height": height,
        "count": bands,
        "crs": crs,
        "transform": transform,
        "nodata": nodata,
        "compress": "lzw",
        "tiled": True,
        "blockxsize": 256,
        "blockysize": 256,
    }
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(data)
        if tags:
            dst.update_tags(**{str(k): str(v) for k, v in tags.items()})
    logger.info(f"wrote {path} ({bands} band(s) {height}x{width} {dtype})")
    return path


def _read_raster(path: Any, band: int = 1, to_float: bool = True) -> np.ndarray:
    """Read one band, turning the declared nodata into NaN when ``to_float``."""
    with rasterio.open(Path(path)) as src:
        data = src.read(band)
        nodata = src.nodata
    if not to_float:
        return data
    out = data.astype(np.float32)
    if nodata is not None and np.isfinite(nodata):
        out = np.where(data == nodata, np.nan, out).astype(np.float32)
    return out


def last_available_day(
    parser,
    var: str = "chirps",
    not_after: Optional[_dt.date] = None,
    max_lookback_days: int = 800,
) -> Optional[_dt.date]:
    """Latest day on or before ``not_after`` whose daily raster exists on disk.

    Args:
        parser: the 4-file config parser.
        var: one of :data:`geocif.phenology.inputs.DAILY_VARS`.
        not_after: search starts here and walks backwards (default: today).
        max_lookback_days: give up after this many days (days).

    Returns:
        The date, or ``None`` when nothing was found inside the lookback window.
    """
    day = not_after or _dt.date.today()
    for _ in range(int(max_lookback_days) + 1):
        if inputs.daily_path(parser, var, day).is_file():
            return day
        day -= _dt.timedelta(days=1)
    logger.warning(
        f"last_available_day: no {var} file within {max_lookback_days} day(s) of "
        f"{not_after or 'today'}"
    )
    return None


# ---------------------------------------------------------------------------
# 7.3 PET calibration (DESIGN section 11.1)
# ---------------------------------------------------------------------------
def load_pet_calibration(path: Any) -> Optional[np.ndarray]:
    """Load a cached ``pet_calibration.tif`` as float32 ``(12, rows, cols)``.

    Returns ``None`` when the file is missing, unreadable or not 12-band.
    """
    path = Path(path)
    if not path.is_file():
        return None
    try:
        with rasterio.open(path) as src:
            if src.count != 12:
                logger.warning(f"{path} has {src.count} band(s), expected 12; ignoring it")
                return None
            return src.read().astype(np.float32)
    except Exception as exc:  # noqa: BLE001 - a bad cache must not kill the build
        logger.warning(f"could not read the PET calibration at {path}: {exc}")
        return None


def build_pet_calibration(
    parser,
    country: str,
    window: Window,
    transform: Affine,
    shape: tuple[int, int],
    years: Iterable[int] = range(2001, 2021),
    min_years: int = 5,
    *,
    cache_path: Optional[Any] = None,
    rebuild: bool = False,
    n_threads: int = 8,
    day_stride: int = 1,
    min_days_per_month: int = 5,
) -> np.ndarray:
    """Per-month Hargreaves-to-``etref`` correction factor for one country window.

    For each calendar month, ``k = mean(etref) / mean(hargreaves)`` over every
    day of the record where **both** are finite (the ratio of sums over that
    common day set, which is the ratio of the means). A pixel-year-month counts
    only when it has at least ``min_days_per_month`` such days; a pixel needs
    ``min_years`` counted years before its own factor is used. ``k`` is clipped
    to ``[0.5, 2.0]`` and, where still undefined, replaced by the median of the
    defined factors of that month across the window (``1.0`` if the month has
    none anywhere).

    Why: measured over Kenya, raw Hargreaves runs -0.5 .. -1.9 mm/day against
    the ``etref`` rasters with near-zero spatial correlation; the fitted monthly
    factor takes the bias to -0.17 mm/day and the correlation to 0.66 out of
    sample (DESIGN section 11.1). Raw Hargreaves drains the soil bucket too
    slowly and biases cessation late.

    Args:
        parser: the 4-file config parser.
        country: country slug (logging and GeoTIFF tags only).
        window: window on the global 0.05 deg grid.
        transform: affine transform of that window.
        shape: ``(rows, cols)``.
        years: calendar years of the fitting record.
        min_years: minimum counted years per pixel-month.
        cache_path: when given, read it if it exists (unless ``rebuild``) and
            write the result to it (12 bands, float32, nodata NaN).
        rebuild: ignore an existing cache.
        n_threads: threads per daily cube read.
        day_stride: read every Nth day of each month.
        min_days_per_month: minimum overlapping days per pixel-year-month.

    Returns:
        float32 ``(12, rows, cols)``, dimensionless; band ``m - 1`` holds month
        ``m``. Every value is finite and inside ``[0.5, 2.0]``.
    """
    rows, cols = int(shape[0]), int(shape[1])
    if cache_path is not None and not rebuild:
        cached = load_pet_calibration(cache_path)
        if cached is not None and cached.shape == (12, rows, cols):
            logger.info(f"PET calibration for {country} read from {cache_path}")
            return cached

    year_list = [int(y) for y in years]
    stride = max(1, int(day_stride))
    lat = inputs.pixel_centres(transform, shape)[1]

    sum_et = np.zeros((12, rows, cols), dtype=np.float64)
    sum_hg = np.zeros((12, rows, cols), dtype=np.float64)
    n_year = np.zeros((12, rows, cols), dtype=np.int32)

    for year in year_list:
        for month in range(1, 13):
            n_days = _calendar.monthrange(year, month)[1]
            days = [_dt.date(year, month, d) for d in range(1, n_days + 1)][::stride]
            if not days:
                continue
            etref, _ = inputs.read_cube(parser, "etref", days, window, n_threads=n_threads)
            if not np.isfinite(etref).any():
                continue
            tmin, _ = inputs.read_cube(
                parser, "chirts_era5_tmin", days, window, n_threads=n_threads
            )
            tmax, _ = inputs.read_cube(
                parser, "chirts_era5_tmax", days, window, n_threads=n_threads
            )
            doy = np.array([d.timetuple().tm_yday for d in days], dtype=np.float64)
            hg = core.hargreaves_pet(tmin, tmax, doy, lat)
            both = np.isfinite(etref) & np.isfinite(hg) & (hg > 0.0)
            count = both.sum(axis=0)
            ok = count >= int(min_days_per_month)
            if not ok.any():
                continue
            sum_et[month - 1] += np.where(ok, np.where(both, etref, 0.0).sum(axis=0), 0.0)
            sum_hg[month - 1] += np.where(ok, np.where(both, hg, 0.0).sum(axis=0), 0.0)
            n_year[month - 1] += ok.astype(np.int32)
        logger.info(f"PET calibration {country}: year {year} folded in")

    enough = (n_year >= int(min_years)) & (sum_hg > 0.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        k = np.where(enough, sum_et / np.where(sum_hg > 0.0, sum_hg, 1.0), np.nan)
    k = np.clip(k, PET_K_MIN, PET_K_MAX)  # NaN survives the clip

    for month in range(12):
        plane = k[month]
        defined = np.isfinite(plane)
        median = float(np.nanmedian(plane)) if bool(defined.any()) else float("nan")
        if not np.isfinite(median):
            median = PET_K_FALLBACK
        k[month] = np.where(defined, plane, median)
        logger.info(
            f"PET calibration {country} month {month + 1}: "
            f"{int(defined.sum())}/{plane.size} pixel(s) fitted, median {median:.3f}"
        )

    k32 = k.astype(np.float32)
    if cache_path is not None:
        _write_multiband(
            cache_path,
            k32,
            transform,
            float("nan"),
            "float32",
            tags={
                "layer": "pet_calibration",
                "units": "dimensionless factor; band m-1 holds month m",
                "country": country,
                "years": f"{min(year_list)}-{max(year_list)}" if year_list else "",
                "min_years": min_years,
                "clip": f"[{PET_K_MIN}, {PET_K_MAX}]",
            },
        )
    return k32


def calibrated_pet(
    etref_cube: Optional[np.ndarray],
    tmin_cube: Optional[np.ndarray],
    tmax_cube: Optional[np.ndarray],
    dates: Sequence[_dt.date],
    lat: np.ndarray,
    k: Optional[np.ndarray],
) -> tuple[np.ndarray, int]:
    """PET cube in mm/day: ``etref`` where finite, else **calibrated** Hargreaves.

    Args:
        etref_cube: ``(T, rows, cols)`` reference ET in mm/day with NaN gaps, or
            ``None`` when no etref exists at all (the source has been stalled
            since 2026 DOY 176, so the current season is exactly that case).
        tmin_cube, tmax_cube: ``(T, rows, cols)`` daily minimum / maximum air
            temperature in degC with NaN gaps, or ``None`` for no fallback.
        dates: the T calendar dates of axis 0, in order -- they give the day of
            year for Hargreaves and the month that selects the calibration band.
        lat: row-centre latitudes in degrees north, shape ``(rows,)``.
        k: ``(12, rows, cols)`` factors from :func:`build_pet_calibration`, or
            ``None`` for a factor of 1 (raw Hargreaves -- biased low, see
            DESIGN section 11.1).

    Returns:
        ``(pet, n_hargreaves_filled)`` -- ``pet`` is float32 ``(T, rows, cols)``
        in mm/day, NaN where neither source exists; ``n_hargreaves_filled``
        counts the pixel-days that came from Hargreaves.
    """
    date_list = list(dates)
    n_time = len(date_list)
    if etref_cube is not None:
        et = np.asarray(etref_cube, dtype=np.float64)
    elif tmax_cube is not None:
        et = np.full(np.asarray(tmax_cube).shape, np.nan, dtype=np.float64)
    else:
        raise ValueError("calibrated_pet needs at least one of etref_cube / tmax_cube")
    if et.shape[0] != n_time:
        raise ValueError(f"{n_time} date(s) but a cube with {et.shape[0]} time step(s)")

    missing = ~np.isfinite(et)
    if not missing.any() or tmin_cube is None or tmax_cube is None:
        if missing.any():
            logger.warning(
                f"calibrated_pet: {int(missing.sum())} NaN etref pixel-day(s) "
                f"and no CHIRTS fallback"
            )
        return et.astype(np.float32), 0

    doy = np.array([d.timetuple().tm_yday for d in date_list], dtype=np.float64)
    hg = core.hargreaves_pet(tmin_cube, tmax_cube, doy, lat)
    if k is not None:
        months = np.array([d.month for d in date_list], dtype=np.int64) - 1
        hg = hg * np.asarray(k, dtype=np.float64)[months]
    out = np.where(missing, hg, et)
    n_filled = int((missing & np.isfinite(hg)).sum())
    logger.info(
        f"calibrated_pet: {n_filled} of {int(missing.sum())} missing etref pixel-day(s) "
        f"filled with calibrated Hargreaves"
    )
    return out.astype(np.float32), n_filled


# ---------------------------------------------------------------------------
# 7.4 Calendar -> per-pixel window indices
# ---------------------------------------------------------------------------
def planting_offset(season_calendar, start_date: _dt.date) -> np.ndarray:
    """Days from ``start_date`` to each pixel's planting start.

    Args:
        season_calendar: a :class:`geocif.phenology.inputs.SeasonCalendar`.
        start_date: the calendar date of index 0 of the cube.

    Returns:
        float32 ``(rows, cols)``: ``planting - start_date`` in days, NaN where
        the pixel has no calendar (``NaT`` planting).
    """
    origin = np.datetime64(start_date, "D")
    plant = np.asarray(season_calendar.planting, dtype="datetime64[D]")
    valid = ~np.isnat(plant)
    delta = (plant - origin).astype("int64").astype(np.float64)
    return np.where(valid, delta, np.nan).astype(np.float32)


def season_indices(
    season_calendar,
    start_date: _dt.date,
    n_time: int,
    params: ClimatologyParams,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-pixel onset / cessation window bounds as indices into the cube.

    All three are **indices along axis 0**, i.e. days since ``start_date``:

    * ``search_start = planting - search_start_days_before_planting`` (floored at 0);
    * ``season_end   = harvest`` -- the last day an onset candidate may fall on;
    * ``search_end   = min(harvest + cessation_grace_days, next_planting - 1, n_time - 1)``.

    That middle term is the cap that stops a cessation search from running into
    the next planting window -- it is why the Kenya short rains do not run into
    the long rains.

    Args:
        season_calendar: a :class:`geocif.phenology.inputs.SeasonCalendar`.
        start_date: the calendar date of index 0.
        n_time: number of days in the cube.
        params: build parameters (the two day offsets, in days).

    Returns:
        ``(search_start, season_end, search_end)``, each float32 ``(rows, cols)``
        with NaN where the pixel has no planting or no harvest date.
    """
    origin = np.datetime64(start_date, "D")
    plant = np.asarray(season_calendar.planting, dtype="datetime64[D]")
    harvest = np.asarray(season_calendar.harvest, dtype="datetime64[D]")
    nxt = np.asarray(season_calendar.next_planting, dtype="datetime64[D]")

    valid = ~np.isnat(plant) & ~np.isnat(harvest)
    plant_off = (plant - origin).astype("int64").astype(np.float64)
    harvest_off = (harvest - origin).astype("int64").astype(np.float64)
    next_off = (nxt - origin).astype("int64").astype(np.float64)
    has_next = ~np.isnat(nxt)

    search_start = np.maximum(plant_off - float(params.search_start_days_before_planting), 0.0)
    season_end = harvest_off
    search_end = harvest_off + float(params.cessation_grace_days)
    search_end = np.where(has_next, np.minimum(search_end, next_off - 1.0), search_end)
    search_end = np.minimum(search_end, float(n_time - 1))

    nan = np.full(plant.shape, np.nan, dtype=np.float64)
    return (
        np.where(valid, search_start, nan).astype(np.float32),
        np.where(valid, season_end, nan).astype(np.float32),
        np.where(valid, search_end, nan).astype(np.float32),
    )


# ---------------------------------------------------------------------------
# 7.5 One harvest year
# ---------------------------------------------------------------------------
@dataclass
class _YearPayload:
    """Everything one worker process needs for one harvest year (all picklable)."""

    parser: Any
    country: str
    crop: str
    season: int
    year: int
    window: Window
    transform: Affine
    shape: tuple[int, int]
    zones_gdf: Any
    flags_by_season: dict
    params: ClimatologyParams
    k: Optional[np.ndarray]
    n_threads: int = 8


def _build_year_payload(payload: _YearPayload) -> dict:
    """Run one harvest year and return its pixel layers (no file is written here).

    Raises on anything that makes the year impossible (no calendar dates, no
    rain on disk, an empty date range); :func:`build_climatology` catches that,
    logs it and carries on with the other years.

    Returns:
        dict with float32 ``sos``/``eos``/``lgs``/``first_candidate`` in **days
        since the pixel's planting start** (NaN = none), int8 ``sos_status`` /
        ``eos_status`` (-1 = no calendar), bool ``eos_at_floor``, int16
        ``n_false_starts`` (invalidated episodes, -32768 = no calendar), plus a
        ``meta`` dict describing the cube that produced them.
    """
    params = payload.params
    parser = payload.parser
    year = int(payload.year)

    season_calendar = inputs.rasterize_calendar(
        payload.zones_gdf,
        payload.flags_by_season,
        payload.season,
        year,
        payload.transform,
        payload.shape,
    )
    plant = np.asarray(season_calendar.planting, dtype="datetime64[D]")
    harvest = np.asarray(season_calendar.harvest, dtype="datetime64[D]")
    valid = ~np.isnat(plant) & ~np.isnat(harvest)
    if not valid.any():
        raise ValueError(f"harvest year {year}: no pixel has both a planting and a harvest date")

    start_date = plant[valid].min().item() - _dt.timedelta(
        days=int(params.search_start_days_before_planting)
    )
    wanted_end = harvest[valid].max().item() + _dt.timedelta(days=int(params.cessation_grace_days))
    data_through = last_available_day(parser, "chirps", not_after=wanted_end)
    if data_through is None:
        raise ValueError(f"harvest year {year}: no CHIRPS file on or before {wanted_end}")
    end_date = min(wanted_end, data_through)
    if end_date < start_date:
        raise ValueError(
            f"harvest year {year}: data ends {end_date}, before the cube start {start_date}"
        )

    dates = [start_date + _dt.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    n_time = len(dates)
    logger.info(
        f"{payload.country}/{payload.crop} s{payload.season} {year}: "
        f"{n_time} day(s) {dates[0]} -> {dates[-1]}"
    )

    pr, missing_pr = inputs.read_cube(
        parser, "chirps", dates, payload.window, n_threads=payload.n_threads
    )
    if not np.isfinite(pr).any():
        raise ValueError(f"harvest year {year}: no finite CHIRPS value in {n_time} day(s)")

    # Reject a year with too many absent daily files. A missing day reads as an
    # all-NaN slab, and NaN contributes 0 mm to the accumulation while NOT
    # counting as a dry day -- so a gap silently BREAKS the dry spell that would
    # have invalidated a false start. Measured: a 200-day year with a candidate
    # on day 12 whose 10-day dry spell ends on day 22 (inside the look-ahead)
    # correctly resolves to onset day 62; punch 24 days of holes in it and the
    # same year reports onset day 12 with status OK -- 50 days early, at full
    # weight, in the median that every anomaly is measured against.
    missing_fraction = len(missing_pr) / float(max(n_time, 1))
    if missing_fraction > payload.params.max_missing_day_fraction:
        raise ValueError(
            f"harvest year {year}: {len(missing_pr)} of {n_time} CHIRPS day(s) "
            f"missing ({missing_fraction:.1%} > "
            f"{payload.params.max_missing_day_fraction:.1%}); a gap can break the dry spell "
            f"that invalidates a false start, so this year is not usable"
        )

    etref, missing_et = inputs.read_cube(
        parser, "etref", dates, payload.window, n_threads=payload.n_threads
    )
    tmin = tmax = None
    if not np.isfinite(etref).all():
        # CHIRTS is only read when etref actually has gaps to fill.
        tmin, _ = inputs.read_cube(
            parser, "chirts_era5_tmin", dates, payload.window, n_threads=payload.n_threads
        )
        tmax, _ = inputs.read_cube(
            parser, "chirts_era5_tmax", dates, payload.window, n_threads=payload.n_threads
        )
    lat = inputs.pixel_centres(payload.transform, payload.shape)[1]
    pet, n_hargreaves_filled = calibrated_pet(etref, tmin, tmax, dates, lat, payload.k)

    search_start, season_end, search_end = season_indices(
        season_calendar, start_date, n_time, params
    )
    result = core.season_phenology(
        pr, pet, search_start, season_end, search_end, params.onset, params.cessation
    )
    # ``result["n_false_starts"]`` counts EVERY candidate episode before onset,
    # while ``core.onset_state`` counts only the INVALIDATED ones. This package
    # reports the invalidated meaning everywhere (``false_start_rate`` is named
    # for it), so the count comes from the state machine instead; core.py is a
    # fixed contract and is not touched. The second pass costs one more onset
    # sweep over the cube and nothing else.
    state = core.onset_state(pr, search_start, season_end, params.onset)

    offset = planting_offset(season_calendar, start_date)
    sos = (result["sos"] - offset).astype(np.float32)
    eos = (result["eos"] - offset).astype(np.float32)
    lgs = result["lgs"].astype(np.float32)  # a difference: the offset cancels
    first_candidate = (result["first_candidate"] - offset).astype(np.float32)

    sos_status = np.asarray(result["sos_status"], dtype=np.int8).copy()
    eos_status = np.asarray(result["eos_status"], dtype=np.int8).copy()
    n_false = np.asarray(state["n_false_starts"], dtype=np.int16).copy()
    eos_at_floor = np.asarray(result["eos_at_floor"], dtype=bool).copy()

    nocal = ~valid
    sos[nocal] = np.nan
    eos[nocal] = np.nan
    lgs[nocal] = np.nan
    first_candidate[nocal] = np.nan
    sos_status[nocal] = STATUS_NODATA
    eos_status[nocal] = STATUS_NODATA
    n_false[nocal] = INT16_NODATA
    eos_at_floor[nocal] = False

    meta = {
        "year": year,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "n_days": n_time,
        "n_missing_chirps": len(missing_pr),
        "n_missing_etref": len(missing_et),
        "n_hargreaves_filled": int(n_hargreaves_filled),
        "n_calendar_pixels": int(valid.sum()),
        "n_onset_pixels": int(np.isfinite(sos).sum()),
    }
    return {
        "sos": sos,
        "eos": eos,
        "lgs": lgs,
        "sos_status": sos_status,
        "eos_status": eos_status,
        "first_candidate": first_candidate,
        "n_false_starts": n_false,
        "eos_at_floor": eos_at_floor,
        "meta": meta,
    }


# ---------------------------------------------------------------------------
# 7.6 Summary over the years
# ---------------------------------------------------------------------------
def summarize_years(years: Sequence[int], per_year: dict, min_valid_years: int) -> dict:
    """Stack the yearly layers into the eleven summary layers.

    Args:
        years: harvest years in stack order.
        per_year: ``{year: layer dict}`` as returned by ``_build_year_payload``.
        min_valid_years: gate on the median / quartile / std layers (years).

    Returns:
        dict of the :data:`SUMMARY_LAYERS` names -> arrays, float32 in days or
        shares, except ``onset_n_valid`` which is int16 years. Definitions:

        * ``onset_*`` from :func:`geocif.phenology.core.onset_climatology` on the
          ``sos`` stack (days since planting start);
        * ``false_start_rate`` = share of usable years with at least one
          **invalidated** candidate episode; a year is usable where its
          ``sos_status`` is not the ``-1`` no-calendar sentinel;
        * ``eos_median``, ``lgs_median`` = medians under the same year gate;
        * ``eos_frac_censored`` = share of the years that had an onset whose
          cessation was right-censored;
        * ``eos_frac_at_floor`` = share of the years with a cessation where the
          minimum-season gate was binding.
    """
    year_list = [int(y) for y in years]
    sos = np.stack([per_year[y]["sos"] for y in year_list]).astype(np.float32)
    eos = np.stack([per_year[y]["eos"] for y in year_list]).astype(np.float32)
    lgs = np.stack([per_year[y]["lgs"] for y in year_list]).astype(np.float32)
    sos_status = np.stack([per_year[y]["sos_status"] for y in year_list]).astype(np.int8)
    eos_status = np.stack([per_year[y]["eos_status"] for y in year_list]).astype(np.int8)
    n_false = np.stack([per_year[y]["n_false_starts"] for y in year_list]).astype(np.int16)
    at_floor = np.stack([per_year[y]["eos_at_floor"] for y in year_list]).astype(bool)

    onset = core.onset_climatology(sos, min_valid_years=int(min_valid_years))
    eos_clim = core.onset_climatology(eos, min_valid_years=int(min_valid_years))
    lgs_clim = core.onset_climatology(lgs, min_valid_years=int(min_valid_years))

    usable = sos_status != STATUS_NODATA
    n_usable = usable.sum(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        false_rate = np.where(
            n_usable > 0, (usable & (n_false > 0)).sum(axis=0) / np.maximum(n_usable, 1), np.nan
        )

    had_onset = (
        (eos_status == int(core.CessationStatus.OK))
        | (eos_status == int(core.CessationStatus.RIGHT_CENSORED))
        | (eos_status == int(core.CessationStatus.NO_RANGE))
    )
    n_onset_years = had_onset.sum(axis=0)
    n_censored = (eos_status == int(core.CessationStatus.RIGHT_CENSORED)).sum(axis=0)
    n_ok = (eos_status == int(core.CessationStatus.OK)).sum(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        frac_censored = np.where(
            n_onset_years > 0, n_censored / np.maximum(n_onset_years, 1), np.nan
        )
        frac_at_floor = np.where(n_ok > 0, at_floor.sum(axis=0) / np.maximum(n_ok, 1), np.nan)

    return {
        "onset_median": onset["median"].astype(np.float32),
        "onset_p25": onset["p25"].astype(np.float32),
        "onset_p75": onset["p75"].astype(np.float32),
        "onset_std": onset["std"].astype(np.float32),
        "onset_n_valid": onset["n_valid"].astype(np.int16),
        "onset_frac_no_onset": onset["frac_no_onset"].astype(np.float32),
        "false_start_rate": false_rate.astype(np.float32),
        "eos_median": eos_clim["median"].astype(np.float32),
        "lgs_median": lgs_clim["median"].astype(np.float32),
        "eos_frac_censored": frac_censored.astype(np.float32),
        "eos_frac_at_floor": frac_at_floor.astype(np.float32),
    }


# ---------------------------------------------------------------------------
# 7.7 The build
# ---------------------------------------------------------------------------
def _year_path(out_dir: Path, layer: str, year: int) -> Path:
    """``{out_dir}/years/{layer}_{year}.tif``."""
    return Path(out_dir) / YEAR_SUBDIR / f"{layer}_{int(year)}.tif"


def _existing_paths(out_dir: Path, manifest: dict) -> dict[str, Path]:
    """The path dict a cached build would have returned (only files that exist)."""
    out_dir = Path(out_dir)
    paths: dict[str, Path] = {}
    for layer in SUMMARY_LAYERS:
        path = out_dir / f"{layer}.tif"
        if path.is_file():
            paths[layer] = path
    for year in manifest.get("years", []):
        for layer in YEAR_LAYERS:
            path = _year_path(out_dir, layer, int(year))
            if path.is_file():
                paths[f"{layer}_{int(year)}"] = path
    pet = out_dir / PET_CALIBRATION_FILE
    if pet.is_file():
        paths["pet_calibration"] = pet
    manifest_path = out_dir / MANIFEST_FILE
    if manifest_path.is_file():
        paths["manifest"] = manifest_path
    return paths


def build_climatology(
    parser,
    country: str,
    crop: str,
    season: int,
    years: Sequence[int],
    params: ClimatologyParams,
    out_dir: Any,
    n_workers: int = 8,
    rebuild: bool = False,
) -> dict[str, Path]:
    """Build (or reuse) the cached phenology climatology for one country/crop/season.

    Per harvest year: rasterize the calendar, read CHIRPS (plus etref and, only
    where etref has gaps, CHIRTS) from ``min(planting) -
    search_start_days_before_planting`` to ``max(harvest) +
    cessation_grace_days`` clipped to the last day on disk, compute calibrated
    PET, run :func:`geocif.phenology.core.season_phenology`, and write the seven
    yearly rasters in **days since that pixel's planting start**. Then write the
    eleven summary layers and ``manifest.json``.

    Years run in a :class:`~concurrent.futures.ProcessPoolExecutor` of
    ``n_workers`` (``n_workers <= 1`` runs them in this process). A year that
    raises is logged, listed in the manifest under ``failed_years`` and skipped;
    it never aborts the build.

    Args:
        parser: the 4-file config parser.
        country: country slug, e.g. ``"kenya"``.
        crop: crop slug, e.g. ``"maize"``.
        season: 1-based season number.
        years: harvest years to build.
        params: :class:`ClimatologyParams`.
        out_dir: cache directory (see :func:`climatology_dir`); created here.
        n_workers: process pool size.
        rebuild: rebuild even when the cached params hash matches.

    Returns:
        ``{key: Path}`` for everything on disk -- one key per summary layer,
        ``"{layer}_{year}"`` per yearly raster, plus ``"pet_calibration"`` and
        ``"manifest"``. Raises ``RuntimeError`` only when *every* year failed.
    """
    out_dir = Path(out_dir)
    year_list = [int(y) for y in years]
    bbox = inputs.country_bbox(parser, country)
    window, transform, shape = inputs.window_for_bbox(bbox)
    bounds = _bounds_of(transform, shape)
    wanted_hash = params_hash(params, country, crop, season, year_list, shape, bounds)

    manifest_path = out_dir / MANIFEST_FILE
    if not rebuild and manifest_path.is_file():
        try:
            cached = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - a corrupt manifest just means "rebuild"
            logger.warning(f"unreadable manifest at {manifest_path}: {exc}; rebuilding")
            cached = {}
        if cached.get("params_hash") == wanted_hash:
            # A cache is only a hit if it also holds every year it was asked
            # for. Without this, one transient /gpfs outage that kills 44 of 45
            # years freezes that crippled cache in place for good: the hash
            # still matches, so the lost years are never retried and every
            # published anomaly is drawn from the surviving handful (or is
            # all-NaN once min_valid_years bites).
            cached_years = {int(y) for y in cached.get("years", [])}
            still_missing = sorted(set(year_list) - cached_years)
            if still_missing:
                logger.info(
                    f"climatology cache for {country}/{crop} s{season} matches on "
                    f"parameters but is missing {len(still_missing)} of "
                    f"{len(year_list)} year(s) "
                    f"(e.g. {still_missing[:5]}); rebuilding to retry them"
                )
            else:
                logger.info(
                    f"climatology cache hit for {country}/{crop} s{season} at {out_dir} "
                    f"({len(cached_years)} year(s), hash {wanted_hash[:12]})"
                )
                return _existing_paths(out_dir, cached)
        if cached:
            logger.info(
                f"climatology params hash changed for {country}/{crop} s{season} "
                f"({str(cached.get('params_hash'))[:12]} -> {wanted_hash[:12]}); rebuilding"
            )
    out_dir.mkdir(parents=True, exist_ok=True)

    k = build_pet_calibration(
        parser,
        country,
        window,
        transform,
        shape,
        years=params.pet_calibration_years,
        min_years=params.pet_calibration_min_years,
        cache_path=out_dir / PET_CALIBRATION_FILE,
        rebuild=rebuild,
        day_stride=params.pet_calibration_day_stride,
        min_days_per_month=params.pet_calibration_min_days_per_month,
    )

    zones_gdf, flags_by_season = inputs.load_calendar_zones(parser, country, crop)
    payloads = [
        _YearPayload(
            parser=parser,
            country=country,
            crop=crop,
            season=int(season),
            year=year,
            window=window,
            transform=transform,
            shape=shape,
            zones_gdf=zones_gdf,
            flags_by_season=flags_by_season,
            params=params,
            k=k,
        )
        for year in year_list
    ]

    per_year: dict[int, dict] = {}
    failed: dict[int, str] = {}
    workers = max(1, int(n_workers))
    if workers == 1:
        for payload in payloads:
            try:
                per_year[int(payload.year)] = _build_year_payload(payload)
            except Exception as exc:  # noqa: BLE001 - one bad year must not stop the build
                failed[int(payload.year)] = f"{type(exc).__name__}: {exc}"
                logger.warning(f"harvest year {payload.year} skipped: {exc}")
    else:
        with ProcessPoolExecutor(max_workers=min(workers, len(payloads) or 1)) as pool:
            futures = {
                pool.submit(_build_year_payload, payload): int(payload.year)
                for payload in payloads
            }
            for future, year in futures.items():
                try:
                    per_year[year] = future.result()
                except Exception as exc:  # noqa: BLE001 - same, across the process boundary
                    failed[year] = f"{type(exc).__name__}: {exc}"
                    logger.warning(f"harvest year {year} skipped: {exc}")

    built_years = sorted(per_year)
    if not built_years:
        raise RuntimeError(
            f"climatology {country}/{crop} s{season}: every one of {len(year_list)} year(s) failed "
            f"({'; '.join(f'{y}: {m}' for y, m in sorted(failed.items()))})"
        )
    if failed:
        logger.warning(
            f"climatology {country}/{crop} s{season}: {len(failed)} of {len(year_list)} "
            f"year(s) skipped -> {sorted(failed)}"
        )

    paths: dict[str, Path] = {}
    common_tags = {"country": country, "crop": crop, "season": season}
    for year in built_years:
        layers = per_year[year]
        for layer, (dtype, nodata) in YEAR_LAYERS.items():
            paths[f"{layer}_{year}"] = write_geotiff(
                _year_path(out_dir, layer, year),
                layers[layer],
                transform,
                nodata,
                dtype,
                tags={
                    **common_tags,
                    "layer": layer,
                    "harvest_year": year,
                    "units": LAYER_UNITS[layer],
                    "start_date": layers["meta"]["start_date"],
                    "end_date": layers["meta"]["end_date"],
                    "n_hargreaves_filled": layers["meta"]["n_hargreaves_filled"],
                },
            )

    summary = summarize_years(built_years, per_year, params.min_valid_years)
    for layer, (dtype, nodata) in SUMMARY_LAYERS.items():
        paths[layer] = write_geotiff(
            out_dir / f"{layer}.tif",
            summary[layer],
            transform,
            nodata,
            dtype,
            tags={
                **common_tags,
                "layer": layer,
                "units": LAYER_UNITS[layer],
                "years": f"{built_years[0]}-{built_years[-1]}",
                "n_years": len(built_years),
                "min_valid_years": params.min_valid_years,
            },
        )
    pet_path = out_dir / PET_CALIBRATION_FILE
    if pet_path.is_file():
        paths["pet_calibration"] = pet_path

    year_meta = {str(year): per_year[year]["meta"] for year in built_years}
    data_through = max(meta["end_date"] for meta in year_meta.values())
    manifest = {
        "country": country,
        "crop": crop,
        "season": int(season),
        "params_hash": wanted_hash,
        "params": params.to_dict(),
        "years": built_years,
        "years_requested": year_list,
        "failed_years": {str(y): m for y, m in sorted(failed.items())},
        "bounds": [float(b) for b in bounds],
        "shape": [int(shape[0]), int(shape[1])],
        "transform": [float(v) for v in transform.to_gdal()],
        "data_through": data_through,
        "summary_layers": list(SUMMARY_LAYERS),
        "year_layers": list(YEAR_LAYERS),
        "n_hargreaves_filled": int(
            sum(meta["n_hargreaves_filled"] for meta in year_meta.values())
        ),
        "year_meta": year_meta,
        "geocif_version": _geocif_version(),
        "created": _dt.datetime.now().isoformat(timespec="seconds"),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    paths["manifest"] = manifest_path
    logger.info(
        f"climatology {country}/{crop} s{season}: {len(built_years)} year(s) "
        f"-> {out_dir} (data through {data_through})"
    )
    return paths


def _geocif_version() -> str:
    """``geocif.__version__``, or ``"unknown"`` when the package will not import."""
    try:
        import geocif

        return str(getattr(geocif, "__version__", "unknown"))
    except Exception:  # noqa: BLE001 - version stamping must never break a build
        return "unknown"


def load_climatology(
    out_dir: Any, with_stack: bool = True, expect_hash: Optional[str] = None
) -> Optional[tuple[dict, dict]]:
    """Load a cached climatology.

    Args:
        out_dir: the cache directory written by :func:`build_climatology`.
        with_stack: also load the per-year ``sos`` rasters as ``onset_stack``.
        expect_hash: the caller's :func:`params_hash`. When given and the cache
            was built with different parameters, this returns ``None`` instead
            of a reference the caller would silently misuse -- an anomaly
            computed as ``onset(25 mm trigger) - median(20 mm trigger)`` is a
            systematic bias with nothing on the map to reveal it. Pass ``None``
            only when the parameters genuinely do not matter (inspection).

    Returns:
        ``(arrays, manifest)`` or ``None`` when the directory holds no readable
        manifest, the manifest was built with other parameters, or a summary
        layer is missing.

        ``arrays`` holds every name in :data:`SUMMARY_LAYERS` as a
        ``(rows, cols)`` array -- float32 with NaN for nodata, except int16
        ``onset_n_valid`` -- plus, when present, ``pet_calibration``
        ``(12, rows, cols)`` float32 and, when ``with_stack``, ``onset_stack``
        float32 ``(n_years, rows, cols)`` in ``manifest["years"]`` order (NaN
        where that year had no onset). Day layers are in days since the pixel's
        planting start.
    """
    out_dir = Path(out_dir)
    manifest_path = out_dir / MANIFEST_FILE
    if not manifest_path.is_file():
        logger.info(f"no climatology manifest at {manifest_path}")
        return None
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - unreadable cache == no cache
        logger.warning(f"unreadable manifest at {manifest_path}: {exc}")
        return None

    if expect_hash is not None and manifest.get("params_hash") != expect_hash:
        logger.warning(
            f"climatology at {out_dir} was built with different parameters "
            f"(hash {str(manifest.get('params_hash'))[:12]}, wanted "
            f"{str(expect_hash)[:12]}); refusing to use it as the reference"
        )
        return None

    arrays: dict[str, np.ndarray] = {}
    for layer, (dtype, _nodata) in SUMMARY_LAYERS.items():
        path = out_dir / f"{layer}.tif"
        if not path.is_file():
            logger.warning(f"climatology at {out_dir} is missing {layer}.tif")
            return None
        if dtype == "int16":
            arrays[layer] = _read_raster(path, to_float=False).astype(np.int16)
        else:
            arrays[layer] = _read_raster(path).astype(np.float32)

    pet = load_pet_calibration(out_dir / PET_CALIBRATION_FILE)
    if pet is not None:
        arrays["pet_calibration"] = pet

    if with_stack:
        stack = []
        for year in manifest.get("years", []):
            path = _year_path(out_dir, "sos", int(year))
            if not path.is_file():
                logger.warning(f"climatology at {out_dir} is missing {path.name}")
                return None
            stack.append(_read_raster(path).astype(np.float32))
        if stack:
            arrays["onset_stack"] = np.stack(stack).astype(np.float32)

    logger.info(
        f"loaded climatology {manifest.get('country')}/{manifest.get('crop')} "
        f"s{manifest.get('season')} from {out_dir} "
        f"({len(manifest.get('years', []))} year(s), data through {manifest.get('data_through')})"
    )
    return arrays, manifest


__all__ = [
    "ClimatologyParams",
    "INT16_NODATA",
    "LAYER_UNITS",
    "PET_CALIBRATION_FILE",
    "PET_K_MAX",
    "PET_K_MIN",
    "STATUS_NODATA",
    "SUMMARY_LAYERS",
    "YEAR_LAYERS",
    "build_climatology",
    "build_pet_calibration",
    "calibrated_pet",
    "climatology_dir",
    "last_available_day",
    "load_climatology",
    "load_pet_calibration",
    "params_hash",
    "planting_offset",
    "season_indices",
    "summarize_years",
]
