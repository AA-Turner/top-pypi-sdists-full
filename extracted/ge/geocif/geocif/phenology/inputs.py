"""I/O for the season monitor: grid, window, crop mask, calendars, daily cubes.

DESIGN.md section 4. Everything in this module speaks ONE grid:

    EPSG:4326, 3600 rows x 7200 cols, 0.05 deg,
    Affine(0.05, 0, -180, 0, -0.05, 90)

A single :class:`rasterio.windows.Window` computed once on that grid serves
every layer (CHIRPS, CHIRTS-ERA5, NCEP-ETref, CHIRPS-GEFS, crop mask) with no
resampling. Reads are resolved against each source's *own* transform via the
window's bounds, so a source stored as an aligned sub-tile (or a source whose
extent has been trimmed) still lines up; a boundless read fills anything the
source does not cover with its nodata value, which scales to NaN.

Units and conventions
---------------------
* Longitude/latitude in decimal degrees, EPSG:4326, x increasing east,
  y decreasing south (north-up raster).
* Rain and reference ET in mm/day; temperatures in degrees Celsius. Every
  raster is returned as float32 with NaN for nodata, already scaled -- the
  scaling rules mirror :func:`geoprepare.extract.stats.get_var`.
* Crop fraction is a dimensionless 0..1 fraction (source rasters store
  percent x 100, i.e. 0..10000).
* Cubes have **time on axis 0**: ``(T, rows, cols)``, matching
  :mod:`geocif.phenology.core`.
* Calendar dates are ``numpy.datetime64[D]`` with ``NaT`` for "no calendar".
* Areas in km^2.

No icclim, no pygmt, no import of :mod:`geocif.cid.indices` anywhere here.
"""

from __future__ import annotations

import datetime as _dt
import logging
import math
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

import numpy as np
import pandas as pd
import rasterio
from affine import Affine
from rasterio.windows import Window

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# The one global grid (DESIGN.md section 1)
# ---------------------------------------------------------------------------
GRID_RES: float = 0.05
GRID_WEST: float = -180.0
GRID_NORTH: float = 90.0
GRID_WIDTH: int = 7200
GRID_HEIGHT: int = 3600
GLOBAL_TRANSFORM: Affine = Affine(0.05, 0, -180, 0, -0.05, 90)

#: CHIRPS v3 carries no data outside 60S-60N; the bbox is clipped to this band.
LAT_LIMIT: float = 60.0

#: Mean Earth radius (km) used for pixel areas -- same constant geoprepare's
#: ``cropland_timeseries.pixel_area_km2_per_row`` uses.
EARTH_R_KM: float = 6371.0087714

#: Daily variables this module knows how to path and scale.
DAILY_VARS: tuple[str, ...] = (
    "chirps",
    "etref",
    "chirts_era5_tmax",
    "chirts_era5_tmin",
)

#: Crop-mask rasters store percent x 100; divide by this for a 0..1 fraction.
MASK_SCALE: float = 10000.0

_CALENDAR_MODULE: Any = None


def _cal() -> Any:
    """The shared calendar-block loader, :mod:`geocif.aquacrop.calendar`.

    Its ``BIMONTH_COLS``, ``_find_season_blocks``, ``_block_to_dates`` and
    ``_bin_to_doy`` are the single home of the half-month block logic and this
    package reuses them rather than re-deriving them.

    ``geocif.aquacrop.__init__`` eagerly imports ``aquacrop-ospy``, an optional
    extra the season monitor has no use for, so when that import fails the leaf
    module is loaded straight from its file (it has no relative imports of its
    own). Cached after the first call.
    """
    global _CALENDAR_MODULE
    if _CALENDAR_MODULE is not None:
        return _CALENDAR_MODULE
    try:
        from geocif.aquacrop import calendar as module
    except Exception as exc:  # noqa: BLE001 - optional dependency, not our problem
        import importlib.util

        logger.debug(f"geocif.aquacrop unavailable ({exc}); loading calendar.py directly")
        path = Path(__file__).resolve().parents[1] / "aquacrop" / "calendar.py"
        spec = importlib.util.spec_from_file_location("_geocif_aquacrop_calendar", path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load the calendar block logic from {path}") from exc
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    _CALENDAR_MODULE = module
    return module


#: Calendar flag codes (DESIGN.md section 1.1).
FLAG_PLANTING = 1
FLAG_GROWING = 2
FLAG_HARVEST = 3
FLAG_POST_HARVEST = 4  # sentinel, treated as off-season
FLAG_OFF = 0
FLAG_NOT_GROWN = -1  # whole row of these => the zone is nodata, NOT zero


# ---------------------------------------------------------------------------
# Small config helpers
# ---------------------------------------------------------------------------
def _dir(parser, key: str) -> Path:
    """Return ``Path(parser.get("PATHS", key))``."""
    return Path(parser.get("PATHS", key))


def _normalize(text: Any) -> str:
    """Lowercase, strip, spaces -> underscores.

    Mirrors :func:`geoprepare.georegion._normalize` (kept local so this module
    does not need geoprepare importable just to slug a string).
    """
    if text is None:
        return ""
    if isinstance(text, float) and math.isnan(text):
        return ""
    return str(text).strip().lower().replace(" ", "_")


class _MaskParams:
    """Minimal duck-type of the geoprepare ``params`` object.

    :func:`geoprepare.utils.resolve_crop_mask` only touches ``parser``,
    ``dir_crop_masks``, ``dir_intermed`` and ``logger``; building this shim
    avoids constructing a whole ``BaseGeo`` just to resolve one mask path.
    """

    def __init__(self, parser) -> None:
        self.parser = parser
        self.dir_crop_masks = _dir(parser, "dir_crop_masks")
        self.dir_intermed = _dir(parser, "dir_intermed")
        self.logger = logger


# ---------------------------------------------------------------------------
# 4.1 Country window
# ---------------------------------------------------------------------------
def snap_bbox(bbox: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    """Snap ``(w, s, e, n)`` OUTWARD to the 0.05 deg lattice anchored at (-180, -90).

    West/south are floored, east/north are ceiled, so the snapped box always
    fully contains the input and its edges are pixel edges of the global grid.
    Mirrors :func:`geoprepare.datasets.AgERA5._snap_bbox_to_grid` (which uses a
    (w, e, s, n) argument order; this one is (w, s, e, n) to match rasterio).

    Args:
        bbox: ``(west, south, east, north)`` in decimal degrees.

    Returns:
        The snapped ``(west, south, east, north)``, clipped to
        ``[-180, 180] x [-LAT_LIMIT, LAT_LIMIT]``.
    """
    west, south, east, north = (float(v) for v in bbox)
    res = GRID_RES
    west = -180.0 + math.floor((west + 180.0) / res) * res
    east = -180.0 + math.ceil((east + 180.0) / res) * res
    south = -90.0 + math.floor((south + 90.0) / res) * res
    north = -90.0 + math.ceil((north + 90.0) / res) * res

    west = max(-180.0, west)
    east = min(180.0, east)
    south = max(-LAT_LIMIT, south)
    north = min(LAT_LIMIT, north)
    # Guard against a degenerate box after the latitude clip.
    if east <= west:
        east = min(180.0, west + res)
    if north <= south:
        north = min(LAT_LIMIT, south + res)
    return (round(west, 6), round(south, 6), round(east, 6), round(north, 6))


def load_boundaries(parser, country: str):
    """Load the country's admin boundaries, USA/antimeridian corrections applied.

    Wraps :func:`geocif.utils.load_country_boundary_gdf` (config-driven column
    renames -> ``ADM0_NAME, ADM1_NAME, ADM_ID`` and optionally ``ADM2_NAME``),
    then applies the two per-call-site fixes that
    ``geocif/agmet/geoagmet.py`` carries: drop Alaska/Hawaii for the USA, and
    clip an antimeridian-spanning frame to the hemisphere holding most
    centroids.

    Args:
        parser: the 4-file config parser.
        country: country slug, e.g. ``"kenya"``.

    Returns:
        A GeoDataFrame in EPSG:4326 (reprojected if the source is not).
    """
    import geopandas as gpd
    from shapely.geometry import box

    from geocif.utils import load_country_boundary_gdf

    path = _dir(parser, "dir_boundary_files") / parser.get(country, "boundary_file")
    gdf = load_country_boundary_gdf(parser, path, country=country)
    if gdf.empty:
        raise ValueError(f"No boundary rows for country={country} in {path}")

    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)

    if _normalize(country) in ("united_states_of_america", "usa", "united_states"):
        adm1 = next((c for c in ("ADM1_NAME", "ADMIN1", "name1") if c in gdf.columns), None)
        if adm1 is not None:
            gdf = gdf[~gdf[adm1].str.lower().isin(["alaska", "hawaii"])].copy()

    bounds = gdf.total_bounds
    if bounds[2] - bounds[0] > 300:
        # Antimeridian wraparound: keep the hemisphere holding most centroids.
        centroid_x = gdf.geometry.centroid.x
        if (centroid_x >= 0).sum() > (centroid_x < 0).sum():
            clip_box = box(0, bounds[1], 180, bounds[3])
        else:
            clip_box = box(-180, bounds[1], 0, bounds[3])
        gdf = gpd.clip(gdf, clip_box)
        logger.info(f"{country}: clipped antimeridian-spanning frame to {clip_box.bounds}")

    return gdf


def country_bbox(parser, country: str, buffer_deg: float = 0.5) -> tuple[float, float, float, float]:
    """Snapped analysis bbox for a country, in decimal degrees.

    Args:
        parser: the 4-file config parser.
        country: country slug, e.g. ``"zimbabwe"``.
        buffer_deg: padding added on every side before snapping (degrees).

    Returns:
        ``(west, south, east, north)``, snapped outward to the global 0.05 deg
        lattice and clipped to ``[-180, 180] x [-60, 60]``.
    """
    gdf = load_boundaries(parser, country)
    west, south, east, north = (float(v) for v in gdf.total_bounds)
    bbox = snap_bbox(
        (west - buffer_deg, south - buffer_deg, east + buffer_deg, north + buffer_deg)
    )
    logger.info(f"{country}: bbox {bbox} (buffer {buffer_deg} deg)")
    return bbox


def window_for_bbox(
    bbox: tuple[float, float, float, float]
) -> tuple[Window, Affine, tuple[int, int]]:
    """Window on the global grid for a snapped bbox.

    Args:
        bbox: ``(west, south, east, north)`` in decimal degrees, ideally already
            snapped by :func:`snap_bbox` (an unsnapped box is snapped here).

    Returns:
        ``(window, transform, (rows, cols))`` -- the integer window on the
        global grid, the affine transform of that window, and its shape.
    """
    west, south, east, north = snap_bbox(bbox)
    col_off = int(round((west - GRID_WEST) / GRID_RES))
    row_off = int(round((GRID_NORTH - north) / GRID_RES))
    cols = int(round((east - west) / GRID_RES))
    rows = int(round((north - south) / GRID_RES))

    col_off = max(0, min(GRID_WIDTH - 1, col_off))
    row_off = max(0, min(GRID_HEIGHT - 1, row_off))
    cols = max(1, min(GRID_WIDTH - col_off, cols))
    rows = max(1, min(GRID_HEIGHT - row_off, rows))

    window = Window(col_off, row_off, cols, rows)
    transform = Affine(
        GRID_RES, 0.0, GRID_WEST + col_off * GRID_RES,
        0.0, -GRID_RES, GRID_NORTH - row_off * GRID_RES,
    )
    return window, transform, (rows, cols)


def pixel_centres(transform: Affine, shape: tuple[int, int]) -> tuple[np.ndarray, np.ndarray]:
    """Pixel-centre coordinates of a north-up window.

    Args:
        transform: affine transform of the window.
        shape: ``(rows, cols)``.

    Returns:
        ``(lon, lat)`` -- ``lon`` is float64 shape ``(cols,)`` in decimal
        degrees east, ``lat`` is float64 shape ``(rows,)`` in decimal degrees
        north, ordered north -> south (row 0 first).
    """
    rows, cols = int(shape[0]), int(shape[1])
    lon = transform.c + (np.arange(cols, dtype=np.float64) + 0.5) * transform.a
    lat = transform.f + (np.arange(rows, dtype=np.float64) + 0.5) * transform.e
    return lon, lat


def pixel_area_km2(lat: np.ndarray, res: float = GRID_RES) -> np.ndarray:
    """Area (km^2) of one grid cell at each row-centre latitude.

    Spherical-Earth band area: ``R^2 * dlon_rad * (sin(lat_top) - sin(lat_bot))``
    -- the same formula as ``geoprepare.cropland_timeseries.pixel_area_km2_per_row``,
    expressed from cell *centres* so it composes with :func:`pixel_centres`.

    Args:
        lat: row-centre latitudes in degrees north, shape ``(rows,)``.
        res: cell size in degrees (square cells).

    Returns:
        float64 array shape ``(rows,)``, km^2 per cell.
    """
    lat = np.asarray(lat, dtype=np.float64)
    d2r = np.pi / 180.0
    top = np.clip(lat + res / 2.0, -90.0, 90.0)
    bot = np.clip(lat - res / 2.0, -90.0, 90.0)
    return (EARTH_R_KM ** 2) * (res * d2r) * (np.sin(top * d2r) - np.sin(bot * d2r))


# ---------------------------------------------------------------------------
# 4.2 Windowed reads
# ---------------------------------------------------------------------------
def _window_bounds(window: Window) -> tuple[float, float, float, float]:
    """``(west, south, east, north)`` of a window on the global grid."""
    west = GRID_WEST + window.col_off * GRID_RES
    north = GRID_NORTH - window.row_off * GRID_RES
    east = west + window.width * GRID_RES
    south = north - window.height * GRID_RES
    return (west, south, east, north)


def _src_window(src, window: Window) -> Window:
    """Translate a global-grid window into ``src``'s own pixel coordinates.

    The window is resolved through its geographic bounds, so a source stored on
    the full global grid gives back the identical window, while an aligned
    sub-tile (what the unit tests build, and what a trimmed archive looks like)
    shifts by the tile's own offset. Anything the source does not cover is
    handled by the caller's boundless read.

    Resampling is out of scope: a source at a different resolution is logged and
    read as-is, which will be wrong. Every layer in DESIGN.md section 1 is
    0.05 deg.
    """
    tr = src.transform
    if abs(abs(tr.a) - GRID_RES) > 1e-9 or abs(abs(tr.e) - GRID_RES) > 1e-9:
        logger.warning(
            f"{getattr(src, 'name', '?')} is {tr.a} x {tr.e} deg, not {GRID_RES}; "
            f"no resampling is applied and the window will not line up"
        )

    west, _south, _east, north = _window_bounds(window)
    col_off = (west - tr.c) / tr.a
    row_off = (north - tr.f) / tr.e
    return Window(
        int(round(col_off)),
        int(round(row_off)),
        int(window.width),
        int(window.height),
    )


def _read_window(path: Path, window: Window) -> tuple[np.ndarray, Optional[float]]:
    """Read one band over ``window``, boundless, returning ``(raw, nodata)``.

    The array is returned in the source's own dtype; scaling is the caller's
    job so the nodata comparison happens before any division.
    """
    with rasterio.open(path) as src:
        sub = _src_window(src, window)
        nodata = src.nodata
        fill = nodata if nodata is not None else 0
        raw = src.read(1, window=sub, boundless=True, fill_value=fill)
    return raw, nodata


def scale_var(var: str, raw: np.ndarray, nodata: Optional[float]) -> np.ndarray:
    """Scale a raw daily raster to physical units, nodata -> NaN.

    Mirrors :func:`geoprepare.extract.stats.get_var` exactly:

    * ``chirps`` / ``chirps_gefs``: int32 mm x 100; ``x < 0 -> NaN`` (this
      catches both the -2147483648 file nodata and the in-band -9999),
      otherwise ``/100`` -> mm/day.
    * ``etref``: float32 mm/day, nodata -9999; ``x < 0 -> NaN``.
    * ``chirts_era5_tmax`` / ``chirts_era5_tmin``: int32 degC x 100, nodata
      -9999; ``x <= -9990 -> NaN``, otherwise ``/100`` -> degC.

    Args:
        var: one of :data:`DAILY_VARS` or ``"chirps_gefs"``.
        raw: the raw windowed array.
        nodata: the file's declared nodata (may be None).

    Returns:
        float32 array, same shape, physical units, NaN where invalid.
    """
    arr = np.asarray(raw, dtype=np.float64)
    if nodata is not None and np.isfinite(nodata):
        arr = np.where(arr == float(nodata), np.nan, arr)

    if var in ("chirps", "chirps_gefs"):
        arr = np.where(arr < 0.0, np.nan, arr / 100.0)
    elif var == "etref":
        arr = np.where(arr < 0.0, np.nan, arr)
    elif var in ("chirts_era5_tmax", "chirts_era5_tmin"):
        arr = np.where(arr <= -9990.0, np.nan, arr / 100.0)
    else:
        raise ValueError(f"Unrecognised daily variable: {var}")
    return arr.astype(np.float32)


def daily_path(parser, var: str, date: _dt.date) -> Path:
    """Absolute path of one daily global raster.

    Mirrors :func:`geoprepare.extract.extract_EO.get_var_fname` (which returns a
    path relative to ``dir_intermed/{var}/``). The CHIRPS version string is read
    from ``[CHIRPS] version`` -- ``v2 -> v2.0``, anything else -> ``v3.0``; it is
    never hardcoded outside that mapping.

    Args:
        parser: the 4-file config parser.
        var: one of :data:`DAILY_VARS`.
        date: the calendar date.

    Returns:
        ``Path`` under ``[PATHS] dir_intermed`` (existence is not checked).
    """
    dir_intermed = _dir(parser, "dir_intermed")
    year = date.year
    doy = date.timetuple().tm_yday
    year_doy = f"{year}{doy:03d}"

    if var == "chirps":
        version = parser.get("CHIRPS", "version", fallback="v2")
        version_str = "v2.0" if version == "v2" else "v3.0"
        return (
            dir_intermed / "chirps" / version / "global" / str(year)
            / f"chirps_{version_str}_{year_doy}_global.tif"
        )
    if var == "etref":
        return dir_intermed / "etref" / str(year) / f"etref_{year_doy}_global.tif"
    if var in ("chirts_era5_tmax", "chirts_era5_tmin"):
        return dir_intermed / var / str(year) / f"{var}_{year_doy}_global.tif"
    raise ValueError(f"Unrecognised daily variable: {var} (expected one of {DAILY_VARS})")


def read_cube(
    parser,
    var: str,
    dates: Sequence[_dt.date],
    window: Window,
    n_threads: int = 8,
) -> tuple[np.ndarray, list[_dt.date]]:
    """Read a daily cube over a window, scaled, with NaN for anything missing.

    One thread per file through a :class:`~concurrent.futures.ThreadPoolExecutor`
    -- rasterio releases the GIL inside ``read``, so threads (not processes)
    are the right tool and the window arrays are assembled in place.

    **Never raises on a missing or unreadable file**: that day becomes an
    all-NaN slab and its date is returned in the second element.

    Args:
        parser: the 4-file config parser.
        var: one of :data:`DAILY_VARS`.
        dates: the calendar dates, in the order they should appear on axis 0.
        window: window on the global grid (from :func:`window_for_bbox`).
        n_threads: pool size; clamped to ``[1, len(dates)]``.

    Returns:
        ``(cube, missing)`` -- ``cube`` is float32 ``(T, rows, cols)`` in
        physical units with NaN nodata, ``missing`` is the list of dates whose
        file was absent or unreadable (same order as ``dates``).
    """
    dates = list(dates)
    rows, cols = int(window.height), int(window.width)
    cube = np.full((len(dates), rows, cols), np.nan, dtype=np.float32)
    missing: list[Optional[_dt.date]] = [None] * len(dates)

    def _one(i: int) -> None:
        day = dates[i]
        path = daily_path(parser, var, day)
        if not path.is_file():
            missing[i] = day
            return
        try:
            raw, nodata = _read_window(path, window)
            cube[i] = scale_var(var, raw, nodata)
        except Exception as exc:  # noqa: BLE001 - a bad file must not kill the run
            missing[i] = day
            logger.warning(f"read_cube: {var} {day} unreadable at {path}: {exc}")

    if dates:
        workers = max(1, min(int(n_threads), len(dates)))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            list(pool.map(_one, range(len(dates))))

    missing_dates = [d for d in missing if d is not None]
    if missing_dates:
        logger.info(
            f"read_cube {var}: {len(missing_dates)}/{len(dates)} day(s) missing, "
            f"first {missing_dates[0]}, last {missing_dates[-1]}"
        )
    return cube, missing_dates


# ---------------------------------------------------------------------------
# 4.3 CHIRPS-GEFS forecast
# ---------------------------------------------------------------------------
_C3G_RE = re.compile(r"^c3g_(\d{4})\.(\d{2})\.(\d{2})\.tif$", re.IGNORECASE)
_ISSUE_RE = re.compile(r"^(\d{8})$")


def _issued_root(parser, year: int) -> Path:
    """``dir_intermed/chirps_gefs/{year}/issued`` (DESIGN.md section 9)."""
    return _dir(parser, "dir_intermed") / "chirps_gefs" / str(year) / "issued"


def latest_forecast_issue(parser, not_before: Optional[_dt.date] = None) -> Optional[_dt.date]:
    """Newest CHIRPS-GEFS issue date on disk, or None.

    Scans ``dir_intermed/chirps_gefs/{Y}/issued/{YYYYMMDD}`` for every year
    directory present and returns the newest issue date that is on or after
    ``not_before``.

    Args:
        parser: the 4-file config parser.
        not_before: earliest acceptable issue date (inclusive). ``None``
            accepts any.

    Returns:
        The issue :class:`datetime.date`, or ``None`` when nothing qualifies
        (including when the archive does not exist yet).
    """
    root = _dir(parser, "dir_intermed") / "chirps_gefs"
    if not root.is_dir():
        return None

    best: Optional[_dt.date] = None
    for year_dir in root.iterdir():
        issued = year_dir / "issued"
        if not issued.is_dir():
            continue
        for issue_dir in issued.iterdir():
            if not issue_dir.is_dir() or not _ISSUE_RE.match(issue_dir.name):
                continue
            try:
                issue = _dt.datetime.strptime(issue_dir.name, "%Y%m%d").date()
            except ValueError:
                continue
            if not_before is not None and issue < not_before:
                continue
            if best is None or issue > best:
                best = issue
    return best


def read_forecast_cube(
    parser, issue_date: _dt.date, window: Window
) -> Optional[tuple[np.ndarray, list[_dt.date]]]:
    """Read the 16-day CHIRPS-GEFS forecast for one issue date.

    Layout (DESIGN.md section 9)::

        dir_intermed/chirps_gefs/{Y}/issued/{YYYYMMDD}/c3g_YYYY.MM.DD.tif

    16 files per issue (issue day + 15). Files are int32 mm x 100 on the global
    grid and scale exactly like CHIRPS.

    Args:
        parser: the 4-file config parser.
        issue_date: the forecast issue date.
        window: window on the global grid.

    Returns:
        ``(cube, dates)`` -- float32 ``(F, rows, cols)`` mm/day with NaN nodata
        and the target dates sorted ascending -- or ``None`` when the issue
        folder is absent or holds no usable file.
    """
    folder = _issued_root(parser, issue_date.year) / issue_date.strftime("%Y%m%d")
    if not folder.is_dir():
        logger.info(f"read_forecast_cube: no issued folder at {folder}")
        return None

    found: list[tuple[_dt.date, Path]] = []
    for path in folder.iterdir():
        match = _C3G_RE.match(path.name)
        if match:
            found.append(
                (_dt.date(int(match.group(1)), int(match.group(2)), int(match.group(3))), path)
            )
    if not found:
        logger.warning(f"read_forecast_cube: {folder} holds no c3g_*.tif")
        return None

    found.sort(key=lambda item: item[0])
    rows, cols = int(window.height), int(window.width)
    cube = np.full((len(found), rows, cols), np.nan, dtype=np.float32)
    for i, (_day, path) in enumerate(found):
        try:
            raw, nodata = _read_window(path, window)
            cube[i] = scale_var("chirps_gefs", raw, nodata)
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"read_forecast_cube: {path} unreadable: {exc}")

    dates = [day for day, _path in found]
    logger.info(
        f"read_forecast_cube: issue {issue_date} -> {len(dates)} day(s) "
        f"{dates[0]} .. {dates[-1]}"
    )
    return cube, dates


# ---------------------------------------------------------------------------
# 4.4 Crop mask
# ---------------------------------------------------------------------------
def crop_mask_path(parser, country: str, crop: str, year: Optional[int] = None) -> Path:
    """Resolve the crop-mask GeoTIFF exactly as geoextract does.

    Section = ``country`` when ``[country] use_cropland_mask`` is true, else
    ``crop``. If that section carries ``mask_dir`` the mask is annual and comes
    from :func:`geoprepare.utils.resolve_crop_mask`; otherwise it is the static
    ``[section] mask`` under ``[PATHS] dir_crop_masks``.

    Args:
        parser: the 4-file config parser.
        country: country slug.
        crop: crop slug.
        year: required only for annual (``mask_dir``) masks.

    Returns:
        ``Path`` to the mask GeoTIFF (values percent x 100).
    """
    use_cropland = parser.getboolean(country, "use_cropland_mask", fallback=False)
    section = country if use_cropland else crop
    if not parser.has_section(section):
        raise ValueError(f"Config has no section [{section}] to resolve a crop mask from")

    if parser.get(section, "mask_dir", fallback=None):
        from geoprepare.utils import resolve_crop_mask

        return Path(resolve_crop_mask(_MaskParams(parser), section, year))
    return _dir(parser, "dir_crop_masks") / parser.get(section, "mask")


def read_crop_fraction(
    parser, country: str, crop: str, window: Window, year: Optional[int] = None
) -> np.ndarray:
    """Crop fraction over the window as a 0..1 float32 array.

    Source rasters store **percent x 100** (0..10000). Nodata and negatives
    become 0 -- an absent mask value means "no crop here", never NaN, so the
    array is safe to use directly as a weight. Values are clipped to 1.0.

    Deliberately does NOT reuse ``geocif.aquacrop.crop_mask.read_mask_array``,
    which mis-scales the percent x 100 convention.

    Args:
        parser: the 4-file config parser.
        country: country slug.
        crop: crop slug.
        window: window on the global grid.
        year: harvest/mask year, required for annual (``mask_dir``) masks.

    Returns:
        float32 ``(rows, cols)`` fraction in ``[0, 1]``.
    """
    path = crop_mask_path(parser, country, crop, year)
    raw, nodata = _read_window(Path(path), window)
    arr = np.asarray(raw, dtype=np.float64)
    if nodata is not None and np.isfinite(nodata):
        arr = np.where(arr == float(nodata), 0.0, arr)
    arr = np.where(np.isfinite(arr) & (arr > 0.0), arr, 0.0)
    frac = np.clip(arr / MASK_SCALE, 0.0, 1.0).astype(np.float32)
    logger.info(
        f"crop fraction {country}/{crop} year={year}: "
        f"{int((frac > 0).sum())} cropland cell(s) of {frac.size} from {path}"
    )
    return frac


# ---------------------------------------------------------------------------
# 4.5 Calendars
# ---------------------------------------------------------------------------
@dataclass
class SeasonCalendar:
    """Per-pixel planting / harvest dates for one (country, crop, season, year).

    The season is labelled by its **harvest year**: Kenya short rains running
    Oct 2025 - Feb 2026 is harvest year 2026.

    Attributes:
        planting: ``datetime64[D]`` ``(rows, cols)`` -- first day of the first
            calendar bin flagged 1. ``NaT`` where the pixel has no zone, the
            zone has no calendar row, or the row is the all -1 "crop not grown"
            sentinel.
        harvest: ``datetime64[D]`` ``(rows, cols)`` -- last day of the last bin
            flagged 3. ``NaT`` in the same places as ``planting``.
        next_planting: ``datetime64[D]`` ``(rows, cols)`` -- earliest planting
            start of ANY season sheet of this crop strictly after ``harvest``
            (the cessation search cap). ``NaT`` when no later season exists.
        zone_id: int16 ``(rows, cols)`` -- 1-based index into ``zone_names``;
            ``0`` means "no calendar zone covers this pixel".
        zone_names: zone keys in ``zone_id`` order (``zone_names[i]`` has
            ``zone_id == i + 1``).
    """

    planting: np.ndarray
    harvest: np.ndarray
    next_planting: np.ndarray
    zone_id: np.ndarray
    zone_names: list[str] = field(default_factory=list)


def _crop_sheet_names(sheet_names: Iterable[str], crop: str) -> dict[int, str]:
    """Map season number -> sheet name for one crop.

    ``geoprepare.base.BaseGeo.get_calendar_sheet_name`` names sheets
    ``"<crop>_<season>"``, except winter_wheat / spring_wheat which are the bare
    crop name (single season -> season 1).
    """
    out: dict[int, str] = {}
    for name in sheet_names:
        low = str(name).strip().lower()
        if low == crop:
            out.setdefault(1, str(name))
            continue
        if low.startswith(f"{crop}_"):
            suffix = low[len(crop) + 1:]
            if suffix.isdigit():
                out[int(suffix)] = str(name)
    return out


def load_calendar_zones(parser, country: str, crop: str):
    """Load calendar zone polygons and the 24-bin flag row for every season.

    Args:
        parser: the 4-file config parser.
        country: country slug, e.g. ``"kenya"``.
        crop: crop slug, e.g. ``"maize"``.

    Returns:
        ``(zones_gdf, flags_by_season)``.

        ``zones_gdf`` is a GeoDataFrame **in EPSG:4326** (the shipped
        ``GlobalCM_Regions_2025-11.shp`` is EPSG:3857, so it is reprojected
        here) filtered to the country, with a ``calendar_region`` column
        holding the normalised zone key.

        ``flags_by_season`` maps ``season_number -> {zone_key: flags}`` where
        ``flags`` is an int array of length 24 over
        ``geocif.aquacrop.calendar.BIMONTH_COLS``. A row of all ``-1`` is kept
        as-is so the caller
        can tell "crop not grown here" from "off-season".
    """
    import geopandas as gpd

    from geoprepare.utils import harmonize_df

    country_key = _normalize(country)

    # --- calendar workbook ------------------------------------------------
    cal_path = _dir(parser, "dir_crop_calendars") / parser.get(country, "calendar_file")
    if not Path(cal_path).is_file():
        raise FileNotFoundError(f"Calendar workbook not found: {cal_path}")

    # Context-managed: an open ExcelFile keeps a Windows file handle on the
    # workbook, which blocks any later rename/delete of it.
    with pd.ExcelFile(cal_path) as book:
        sheets = _crop_sheet_names(book.sheet_names, crop)
        if not sheets:
            raise ValueError(
                f"No sheet for crop={crop} in {cal_path} "
                f"(have {list(book.sheet_names)[:8]})"
            )
        raw_sheets = {season: book.parse(sheet) for season, sheet in sheets.items()}

    bimonth_cols = _cal().BIMONTH_COLS
    flags_by_season: dict[int, dict[str, np.ndarray]] = {}
    for season, sheet in sorted(sheets.items()):
        df = harmonize_df(raw_sheets[season])
        country_col = "country2" if "country2" in df.columns else "country"
        if country_col not in df.columns:
            raise ValueError(f"Sheet {sheet} of {cal_path} has no country column")
        key_col = "admin" if "admin" in df.columns else "calendar_region"
        if key_col not in df.columns:
            raise ValueError(f"Sheet {sheet} of {cal_path} has no admin column")

        missing_cols = [c for c in bimonth_cols if c not in df.columns]
        if missing_cols:
            raise ValueError(
                f"Sheet {sheet} of {cal_path} missing half-month columns: "
                f"{missing_cols[:5]}"
            )

        sub = df[df[country_col].map(_normalize) == country_key]
        per_zone: dict[str, np.ndarray] = {}
        for _idx, row in sub.iterrows():
            raw = row[bimonth_cols].to_numpy(dtype=float)
            # NaN is off-season (0). A -1 stays -1 so the all--1 sentinel row
            # survives to rasterize_calendar and becomes NaT, not zero.
            flags = np.where(np.isnan(raw), float(FLAG_OFF), raw).astype(int)
            per_zone[_normalize(row[key_col])] = flags
        flags_by_season[int(season)] = per_zone
        logger.info(
            f"calendar {country}/{crop} season {season} (sheet {sheet}): "
            f"{len(per_zone)} zone row(s)"
        )

    # --- zone polygons ----------------------------------------------------
    shp_path = _dir(parser, "dir_boundary_files") / parser.get(country, "shp_region")
    if not Path(shp_path).exists():
        raise FileNotFoundError(f"Calendar zone shapefile not found: {shp_path}")
    zones = gpd.read_file(shp_path, engine="pyogrio")

    adm0_col = next(
        (c for c in ("ADM0_NAME", "ADMIN0", "name0", "COUNTRY", "Country") if c in zones.columns),
        None,
    )
    if adm0_col is None:
        raise ValueError(f"{shp_path} has no country column (looked for ADM0_NAME/ADMIN0/name0)")
    zones = zones[zones[adm0_col].map(_normalize) == country_key].copy()
    if zones.empty:
        raise ValueError(f"No calendar zones for country={country} in {shp_path}")

    name_col = next(
        (c for c in ("Name", "NAME", "name", "REGION", "Region") if c in zones.columns), None
    )
    if name_col is None:
        raise ValueError(f"{shp_path} has no zone-name column (looked for Name/NAME/name)")
    zones["calendar_region"] = zones[name_col].map(_normalize)

    if zones.crs is not None and zones.crs.to_epsg() != 4326:
        logger.info(f"calendar zones {country}: reprojecting {zones.crs} -> EPSG:4326")
        zones = zones.to_crs(epsg=4326)

    return zones, flags_by_season


def _block_index(blocks: list, season: int) -> Optional[int]:
    """Which in-season block a season number selects.

    Season selection follows :func:`geocif.aquacrop.calendar.load_calendar`:
    :func:`_find_season_blocks` returns the in-season blocks sorted by the bin
    carrying flag 1, and the requested season picks **block index
    ``season - 1``** (season 1 = primary = first block).

    One documented deviation from that loader. The GEOGLAM sheets are already
    per-season (``maize_1``, ``maize_2``), and a per-season row usually holds a
    SINGLE block -- Kenya ``maize_2`` Central is
    ``2 2 3 4 4 4 0 ... 0 1 1 1 1 1``, whose jan/feb tail merges with the
    oct-dec head into one wrapped block. Plain ``season - 1`` indexing would
    then run off the end and return no dates at all for every Kenya short-rains
    zone, contradicting DESIGN.md section 1.1 (which states those dates
    explicitly). So the index is clamped to the last block:
    ``min(season - 1, len(blocks) - 1)``. When a row really does carry two
    blocks the behaviour is unchanged.

    Args:
        blocks: output of :func:`_find_season_blocks`.
        season: 1-based season number.

    Returns:
        The block index, or ``None`` when there are no blocks at all.
    """
    if not blocks:
        return None
    index = max(0, int(season) - 1)
    if index >= len(blocks):
        index = len(blocks) - 1
    return index


def _season_dates(
    flags: np.ndarray, season: int, harvest_year: int
) -> Optional[tuple[_dt.date, _dt.date]]:
    """Planting and harvest dates of one season block, labelled by harvest year.

    Block selection: see :func:`_block_index`. Planting is the first day of the
    first bin flagged 1, harvest the last day of the last bin flagged 3 --
    :func:`_block_to_dates` semantics, reused rather than re-derived.

    Cross-year handling: a season whose harvest bin precedes its planting bin
    inside the single 24-bin row is planted in ``harvest_year - 1``. We call
    ``_block_to_dates`` with ``harvest_year`` first; if that lands the harvest
    in ``harvest_year + 1`` the block is cross-year, so we re-run it anchored at
    ``harvest_year - 1`` and the harvest falls in ``harvest_year``.

    Args:
        flags: the 24-bin int flag row.
        season: 1-based season number.
        harvest_year: the year that labels the season.

    Returns:
        ``(planting_date, harvest_date)`` or ``None`` when the row is the all
        ``-1`` "crop not grown" sentinel or holds no in-season block.
    """
    if flags.size != 24 or np.all(flags == FLAG_NOT_GROWN):
        return None
    blocks = _cal()._find_season_blocks(flags)
    index = _block_index(blocks, season)
    if index is None:
        return None

    planting, harvest, _days = _cal()._block_to_dates(blocks[index], flags, harvest_year)
    if harvest.year != harvest_year:
        planting, harvest, _days = _cal()._block_to_dates(blocks[index], flags, harvest_year - 1)
    return planting, harvest


def _planting_only(flags: np.ndarray, season: int, year: int) -> Optional[_dt.date]:
    """Planting start of one season block anchored at calendar ``year``.

    Used to build ``next_planting``: unlike :func:`_season_dates` the anchor is
    the *planting* year, so no harvest-year correction is applied.
    """
    if flags.size != 24 or np.all(flags == FLAG_NOT_GROWN):
        return None
    blocks = _cal()._find_season_blocks(flags)
    index = _block_index(blocks, season)
    if index is None:
        return None
    start, end = blocks[index]
    block_bins = [k % 24 for k in range(start, end + 1)]
    plant_bin = next((k for k in block_bins if flags[k] == FLAG_PLANTING), block_bins[0])
    doy = _cal()._bin_to_doy(plant_bin, year, edge="start")
    return _dt.date(year, 1, 1) + _dt.timedelta(days=doy - 1)


def _next_planting_after(
    flags_by_season: dict[int, dict[str, np.ndarray]],
    zone_key: str,
    harvest: _dt.date,
) -> Optional[_dt.date]:
    """Earliest planting start of ANY season of this crop strictly after ``harvest``.

    Candidate anchors are the harvest year and its neighbours, so both "the
    other season of the same year" and "this season again next year" are
    considered.
    """
    best: Optional[_dt.date] = None
    for season, per_zone in flags_by_season.items():
        flags = per_zone.get(zone_key)
        if flags is None:
            continue
        for year in (harvest.year - 1, harvest.year, harvest.year + 1):
            planting = _planting_only(flags, season, year)
            if planting is None or planting <= harvest:
                continue
            if best is None or planting < best:
                best = planting
    return best


def rasterize_calendar(
    zones_gdf,
    flags_by_season: dict[int, dict[str, np.ndarray]],
    season: int,
    harvest_year: int,
    transform: Affine,
    shape: tuple[int, int],
) -> SeasonCalendar:
    """Burn calendar zones onto the window and attach per-pixel season dates.

    Args:
        zones_gdf: zone polygons in EPSG:4326 with a ``calendar_region`` key
            column (from :func:`load_calendar_zones`).
        flags_by_season: ``season -> {zone_key: 24-bin flags}``.
        season: 1-based season number (block index ``season - 1``).
        harvest_year: the year that labels the season.
        transform: affine transform of the window.
        shape: ``(rows, cols)``.

    Returns:
        A :class:`SeasonCalendar`. Pixels outside every zone get ``zone_id == 0``
        and ``NaT`` dates; so do zones whose calendar row is the all ``-1``
        sentinel or that have no block for this season.
    """
    import rasterio.features as rio_features

    rows, cols = int(shape[0]), int(shape[1])
    zones_gdf = zones_gdf.reset_index(drop=True)
    zone_names = [str(k) for k in zones_gdf["calendar_region"].tolist()]

    if len(zone_names) > np.iinfo(np.int16).max:
        raise ValueError(f"{len(zone_names)} calendar zones exceeds the int16 zone_id range")

    zone_id = rio_features.rasterize(
        ((geom, idx + 1) for idx, geom in enumerate(zones_gdf.geometry)),
        out_shape=(rows, cols),
        transform=transform,
        fill=0,
        all_touched=False,
        dtype=np.int32,
    ).astype(np.int16)

    nat = np.datetime64("NaT", "D")
    # Index 0 = "no zone"; zone i occupies slot i + 1.
    plant_lut = np.full(len(zone_names) + 1, nat, dtype="datetime64[D]")
    harvest_lut = np.full(len(zone_names) + 1, nat, dtype="datetime64[D]")
    next_lut = np.full(len(zone_names) + 1, nat, dtype="datetime64[D]")

    per_zone = flags_by_season.get(int(season), {})
    n_dated = 0
    for idx, key in enumerate(zone_names):
        flags = per_zone.get(key)
        if flags is None:
            continue
        dates = _season_dates(np.asarray(flags), season, harvest_year)
        if dates is None:
            continue
        planting, harvest = dates
        plant_lut[idx + 1] = np.datetime64(planting, "D")
        harvest_lut[idx + 1] = np.datetime64(harvest, "D")
        nxt = _next_planting_after(flags_by_season, key, harvest)
        if nxt is not None:
            next_lut[idx + 1] = np.datetime64(nxt, "D")
        n_dated += 1

    logger.info(
        f"rasterize_calendar season {season} harvest_year {harvest_year}: "
        f"{n_dated}/{len(zone_names)} zone(s) dated, "
        f"{int((zone_id > 0).sum())}/{zone_id.size} pixel(s) inside a zone"
    )

    index = np.clip(zone_id.astype(np.int64), 0, len(zone_names))
    return SeasonCalendar(
        planting=plant_lut[index],
        harvest=harvest_lut[index],
        next_planting=next_lut[index],
        zone_id=zone_id,
        zone_names=zone_names,
    )


# ---------------------------------------------------------------------------
# 4.6 Admin rasterisation
# ---------------------------------------------------------------------------
def rasterize_admin(
    parser, country: str, transform: Affine, shape: tuple[int, int]
) -> tuple[np.ndarray, pd.DataFrame]:
    """Burn admin polygons onto the window and return the id lookup.

    Args:
        parser: the 4-file config parser.
        country: country slug.
        transform: affine transform of the window.
        shape: ``(rows, cols)``.

    Returns:
        ``(id_grid, lookup)`` -- ``id_grid`` is int32 ``(rows, cols)`` holding a
        1-based row index into ``lookup`` (``0`` = outside every polygon), and
        ``lookup`` is a DataFrame with columns ``id``, ``ADM_ID``,
        ``ADM1_NAME`` and, when the boundary file carries it, ``ADM2_NAME``.
    """
    import rasterio.features as rio_features

    gdf = load_boundaries(parser, country).reset_index(drop=True)
    rows, cols = int(shape[0]), int(shape[1])

    id_grid = rio_features.rasterize(
        ((geom, idx + 1) for idx, geom in enumerate(gdf.geometry)),
        out_shape=(rows, cols),
        transform=transform,
        fill=0,
        all_touched=False,
        dtype=np.int32,
    )

    lookup = pd.DataFrame({"id": np.arange(1, len(gdf) + 1, dtype=np.int32)})
    for col in ("ADM_ID", "ADM1_NAME", "ADM2_NAME"):
        if col in gdf.columns:
            lookup[col] = gdf[col].to_numpy()
    if "ADM1_NAME" not in lookup.columns:
        lookup["ADM1_NAME"] = [f"unit_{i}" for i in lookup["id"]]

    logger.info(
        f"rasterize_admin {country}: {len(lookup)} unit(s), "
        f"{int((id_grid > 0).sum())}/{id_grid.size} pixel(s) inside"
    )
    return id_grid, lookup
