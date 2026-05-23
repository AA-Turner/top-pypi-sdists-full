"""
weather.py — assemble per-cell daily weather time series from existing
geoprepare AgERA5 and CHIRPS TIFs.

Existing geoprepare outputs we consume:

    ${dir_intermed}/agera5/{country_slug}/tif/{var}/{year}/agera5_{year}{doy}_{var}.tif
        var ∈ {Temperature_Air_2m_Max_24h, Temperature_Air_2m_Min_24h,
                Solar_Radiation_Flux, ...}
        float32 at 0.05°, country-clipped. AgERA5 native: Temperature in K,
        Solar Radiation Flux in J m-2 day-1.
        process_agERA5 reprojects but DOES NOT unit-convert.

    ${dir_intermed}/chirps/global/{year}/chirps-v3.0.{disagg}.{Y}.{M}.{D}.tif
        int32 at 0.05°, global. Native: mm × 100 (divide by 100 → mm).
        Nodata = -2147483648 (geobase [CHIRPS] fill_value).

We expose:
    WeatherReader(parser, country, country_bounds)
        .get_weather_df(lon, lat, sim_start, sim_end) → pd.DataFrame
            with columns AquaCrop expects: MinTemp, MaxTemp,
            Precipitation, ReferenceET, Date.

Per-worker design:
- One RasterCache LRU per worker (lazy open, capped at 100 datasets)
- Single-pixel reads via Window for time series
- Penman-Monteith ETo when Solar_Radiation_Flux available; Hargreaves
  fallback otherwise.
"""

from __future__ import annotations

import logging
import os
from collections import OrderedDict
from datetime import date as _date, timedelta
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import rasterio
from rasterio.windows import Window

logger = logging.getLogger(__name__)


CHIRPS_FILL = -2147483648
CHIRPS_SCALE = 0.01  # mm × 100 → mm
# AgERA5 Solar Radiation native unit (J m-2 day-1). Penman-Monteith wants
# MJ m-2 day-1 (Allen et al. 1998 FAO-56).
SR_J_TO_MJ = 1.0e-6


class RasterCache:
    """LRU cache of open rasterio datasets, keyed by file path.

    Avoids the cost of rasterio.open() inside the per-cell hot loop. One
    instance per worker process (NOT shared — rasterio file handles aren't
    fork-safe). LRU eviction triggers .close() on the oldest entry to keep
    OS file handle count bounded.

    Default size 100 balances memory vs hit rate: a 1-year, 4-variable
    daily timeseries needs 4 × 365 = 1460 opens per cell without cache.
    With size 100, most cells hit on the first dataset opens and reuse.
    """

    def __init__(self, maxsize: int = 100):
        self._cache: OrderedDict[str, rasterio.DatasetReader] = OrderedDict()
        self.maxsize = maxsize

    def get(self, path: str | Path) -> Optional[rasterio.DatasetReader]:
        key = os.fspath(path)
        if key not in self._cache:
            if not os.path.isfile(key):
                return None
            try:
                ds = rasterio.open(key)
            except (rasterio.RasterioIOError, OSError) as exc:
                logger.warning("Cannot open %s: %s", key, exc)
                return None
            self._cache[key] = ds
        else:
            self._cache.move_to_end(key)

        # Evict oldest if over capacity
        while len(self._cache) > self.maxsize:
            _, oldest = self._cache.popitem(last=False)
            try:
                oldest.close()
            except Exception:  # noqa: BLE001
                pass

        return self._cache[key]

    def close_all(self) -> None:
        for ds in self._cache.values():
            try:
                ds.close()
            except Exception:  # noqa: BLE001
                pass
        self._cache.clear()

    def __del__(self):
        self.close_all()


def _country_slug(country: str) -> str:
    """Mirror of geoprepare.datasets.AgERA5._country_slug."""
    return country.lower().replace(" ", "_")


def _agera5_path(intermed_dir: Path, country: str, var: str, d: _date) -> Path:
    """AgERA5 TIF path for a (country, variable, date).

    Follows the AgERA5.process_agERA5 output convention (0.6.244+):
        ${dir_intermed}/agera5/{country_slug}/tif/{var}/{year}/agera5_{YYYY}{DOY3}_{var}.tif
    """
    doy = d.timetuple().tm_yday
    return (
        intermed_dir / "agera5" / _country_slug(country)
        / "tif" / var / str(d.year)
        / f"agera5_{d.year}{doy:03d}_{var}.tif"
    )


def _chirps_path(intermed_dir: Path, d: _date, disagg: str = "sat") -> Path:
    """CHIRPS v3 TIF path.

    Follows the CHIRPS.py output convention:
        ${dir_intermed}/chirps/global/{year}/chirps-v3.0.{disagg}.{Y}.{M}.{D}.tif
    """
    return (
        intermed_dir / "chirps" / "global" / str(d.year)
        / f"chirps-v3.0.{disagg}.{d.year}.{d.month:02d}.{d.day:02d}.tif"
    )


def _read_pixel(
    cache: RasterCache, path: Path, lon: float, lat: float,
) -> Optional[float]:
    """Read a single pixel from a raster at (lon, lat). Returns None on miss."""
    ds = cache.get(path)
    if ds is None:
        return None
    try:
        col, row = ~ds.transform * (lon, lat)
        col, row = int(col), int(row)
        if not (0 <= row < ds.height and 0 <= col < ds.width):
            return None
        val = ds.read(1, window=Window(col, row, 1, 1))[0, 0]
        if val == ds.nodata:
            return None
        return float(val)
    except (ValueError, IndexError, rasterio.RasterioIOError) as exc:
        logger.debug("Pixel read failed at (%.3f, %.3f) in %s: %s",
                     lon, lat, path.name, exc)
        return None


def _eto_penman_monteith(
    tmin_c: np.ndarray, tmax_c: np.ndarray, rs_mj: np.ndarray, lat_rad: float,
    elevation_m: float = 0.0,
) -> np.ndarray:
    """FAO-56 Penman-Monteith reference ET (mm/day), short-grass surface.

    Simplified version: assumes default humidity (from Tmin = Tdew
    approximation) and 2 m wind speed = 2 m/s (FAO-56 default when no
    wind data is available). For AquaCrop this is adequate — it's the
    same default the FAO ETo Calculator uses.

    Allen et al. 1998 Eqs. 6, 8, 9, 11, 13, 14, 39 (full reference).
    """
    # Mean temperature
    tmean = 0.5 * (tmin_c + tmax_c)

    # Saturation vapour pressure (kPa) at Tmax and Tmin (Eq. 11)
    es_tmax = 0.6108 * np.exp(17.27 * tmax_c / (tmax_c + 237.3))
    es_tmin = 0.6108 * np.exp(17.27 * tmin_c / (tmin_c + 237.3))
    es = 0.5 * (es_tmax + es_tmin)

    # Actual vapour pressure: assume Tdew = Tmin (Eq. 48 fallback)
    ea = 0.6108 * np.exp(17.27 * tmin_c / (tmin_c + 237.3))

    # Slope of vapour pressure curve (Eq. 13)
    delta = 4098.0 * (0.6108 * np.exp(17.27 * tmean / (tmean + 237.3))) \
        / np.power(tmean + 237.3, 2)

    # Atmospheric pressure (Eq. 7)
    P = 101.3 * np.power((293.0 - 0.0065 * elevation_m) / 293.0, 5.26)
    # Psychrometric constant (Eq. 8)
    gamma = 0.000665 * P

    # Net radiation (simplified — full version requires Rs and Rs0).
    # Estimate Rs0 (clear-sky) as 0.75 * Ra; use 0.77 albedo factor.
    # Rns (Eq. 38, albedo 0.23 for grass)
    rns = 0.77 * rs_mj
    # Rnl (Eq. 39) — net longwave; use 0.5 Rs/Rs0 fallback when no Rs0
    sigma = 4.903e-9  # Stefan-Boltzmann (MJ K-4 m-2 day-1)
    tmax_k4 = np.power(tmax_c + 273.16, 4)
    tmin_k4 = np.power(tmin_c + 273.16, 4)
    rnl = sigma * 0.5 * (tmax_k4 + tmin_k4) \
        * (0.34 - 0.14 * np.sqrt(ea)) * 0.5  # last 0.5 = Rs/Rs0 default
    rn = np.maximum(rns - rnl, 0.0)

    # Wind speed default
    u2 = 2.0

    # Penman-Monteith (Eq. 6)
    eto = (
        0.408 * delta * rn
        + gamma * (900.0 / (tmean + 273.0)) * u2 * (es - ea)
    ) / (delta + gamma * (1.0 + 0.34 * u2))

    return np.clip(eto, 0.0, 20.0)


def _eto_hargreaves(
    tmin_c: np.ndarray, tmax_c: np.ndarray, lat_rad: float, doy: np.ndarray,
) -> np.ndarray:
    """Hargreaves-Samani ETo (mm/day). Fallback when Rs unavailable."""
    delta = 0.409 * np.sin(2 * np.pi * doy / 365.0 - 1.39)
    ws = np.arccos(np.clip(-np.tan(lat_rad) * np.tan(delta), -1.0, 1.0))
    dr = 1 + 0.033 * np.cos(2 * np.pi * doy / 365.0)
    ra = (24 * 60 / np.pi) * 0.0820 * dr * (
        ws * np.sin(lat_rad) * np.sin(delta)
        + np.cos(lat_rad) * np.cos(delta) * np.sin(ws)
    )
    ra_mm = ra / 2.45
    tmean = 0.5 * (tmin_c + tmax_c)
    tdiff = np.maximum(tmax_c - tmin_c, 0.1)
    return np.clip(
        0.0023 * ra_mm * (tmean + 17.8) * np.sqrt(tdiff),
        0.0, 20.0,
    )


class WeatherReader:
    """Per-worker weather assembler.

    Holds a RasterCache and intermed-directory paths; build one per process
    (NOT shared across the multiprocessing.Pool — file handles aren't
    fork-safe in rasterio).

    Bulk-cache strategy: for each (variable, year) the first cell triggers
    reading ALL 365 daily TIFs into a single (n_days, n_lat, n_lon)
    in-memory cube clipped to the country bounding box. Subsequent cells
    in the same worker slice from memory — one O(1) lookup per (cell, day,
    var) instead of a per-pixel rasterio.read. Brings per-country wall
    time from O(n_cells × 1460 file opens) down to O(365 × 4) opens total.

    Memory: typical country bbox 50×50 cells × 365 days × 4 bytes ≈ 3 MB
    per (var, year). 4 vars × 25 years ≈ 300 MB per worker.

    Args:
        parser: ConfigParser (geobase.txt + aquacrop.txt).
        country: country name used to slot per-country AgERA5 TIFs (mirror
            of the slug AgERA5.py writes under). Required.
        cache_size: RasterCache LRU capacity (kept for backward-compat with
            the per-pixel path; mostly unused once the bulk cube cache fires).
        country_bounds: (minx, miny, maxx, maxy) — when provided, daily
            TIFs are clipped to this box before stacking, cutting memory
            and IO. When None, the cube spans the whole TIF (slower).
    """

    def __init__(self, parser, country: str, cache_size: int = 100, country_bounds=None):
        self.parser = parser
        self.country = country
        self.dir_intermed = Path(parser.get("PATHS", "dir_intermed"))
        self.chirps_disagg = parser.get("CHIRPS", "disagg", fallback="sat")
        self.eto_method = parser.get(
            "AQUACROP", "eto_method", fallback="penman_monteith",
        )
        self.cache = RasterCache(maxsize=cache_size)
        self.country_bounds = country_bounds
        # Cube cache: (var, year) → (data_3d, transform, dates_list)
        self._cube_cache: dict[tuple[str, int], tuple] = {}
        # Cap so a long-running worker doesn't grow unbounded.
        # 8 entries × 4 vars × 365 days × ~3MB ≈ ~96 MB worst-case.
        self._cube_cache_max = 8

    def close(self) -> None:
        self.cache.close_all()
        self._cube_cache.clear()

    def _load_cube(self, var: str, year: int, path_fn) -> Optional[tuple]:
        """Load a (var, year) cube of daily TIFs into memory, clipped to
        country_bounds when set. Returns (data_3d, transform, dates).
        ``path_fn`` accepts a ``datetime.date`` and returns a Path.
        """
        key = (var, year)
        if key in self._cube_cache:
            # LRU touch
            val = self._cube_cache.pop(key)
            self._cube_cache[key] = val
            return val

        dates = pd.date_range(_date(year, 1, 1), _date(year, 12, 31), freq="D")
        first_path = path_fn(dates[0].date())
        if not first_path.is_file():
            return None
        try:
            with rasterio.open(first_path) as src0:
                if self.country_bounds is not None:
                    win = rasterio.windows.from_bounds(
                        *self.country_bounds, src0.transform,
                    )
                    transform = src0.window_transform(win)
                else:
                    win = None
                    transform = src0.transform
                first_arr = src0.read(1, window=win).astype(np.float32)
                if src0.nodata is not None:
                    first_arr = np.where(first_arr == src0.nodata, np.nan, first_arr)
                # Derive cube shape from the actual read — rasterio's
                # int(round(win.h)) and read(window=win).shape can disagree
                # by ±1 when bounds don't snap to pixel edges; using the
                # actual shape avoids the cube[0] = first_arr crash.
                h, w = first_arr.shape
                cube = np.full((len(dates), h, w), np.nan, dtype=np.float32)
                cube[0] = first_arr
        except (rasterio.RasterioIOError, OSError) as exc:
            logger.warning("Cube load failed for %s/%d: %s", var, year, exc)
            return None

        for i, ts in enumerate(dates[1:], start=1):
            p = path_fn(ts.date())
            if not p.is_file():
                continue
            try:
                with rasterio.open(p) as src:
                    arr = src.read(1, window=win).astype(np.float32)
                    if src.nodata is not None:
                        arr = np.where(arr == src.nodata, np.nan, arr)
                    if arr.shape != (h, w):
                        continue  # mismatched grid — skip rather than crash
                    cube[i] = arr
            except (rasterio.RasterioIOError, OSError):
                continue

        # Cache + bounded eviction
        self._cube_cache[key] = (cube, transform, list(dates))
        while len(self._cube_cache) > self._cube_cache_max:
            self._cube_cache.pop(next(iter(self._cube_cache)))
        return self._cube_cache[key]

    @staticmethod
    def _lonlat_to_rowcol(lon, lat, transform):
        col, row = ~transform * (lon, lat)
        return int(row), int(col)

    def get_weather_df(
        self,
        lon: float,
        lat: float,
        sim_start: _date,
        sim_end: _date,
    ) -> Optional[pd.DataFrame]:
        """Build an AquaCrop-compatible weather DataFrame for one cell.

        Pulls from the per-(var, year) in-memory cube cache rather than
        per-pixel rasterio.read. First cell of a (var, year) loads 365
        TIFs into a country-bbox cube; subsequent cells are pure numpy
        slices.

        Returns None if too many days have missing data (no temperature
        or no precipitation). Missing ETo on individual days is filled
        with the simulation-mean (since AquaCrop doesn't tolerate NaN).
        """
        dates = pd.date_range(sim_start, sim_end, freq="D")
        n = len(dates)

        tmax = np.full(n, np.nan, dtype=np.float32)
        tmin = np.full(n, np.nan, dtype=np.float32)
        rs = np.full(n, np.nan, dtype=np.float32)
        precip = np.full(n, np.nan, dtype=np.float32)

        # Group dates by calendar year (cubes are per (var, year))
        years_in_sim = sorted({d.year for d in (sim_start, sim_end)})
        years_in_sim.extend(int(y) for y in pd.DatetimeIndex(dates).year.unique())
        years_in_sim = sorted(set(years_in_sim))

        intermed = self.dir_intermed
        country = self.country

        def _path_agera5(var_):
            return lambda d, var_=var_: _agera5_path(intermed, country, var_, d)

        def _path_chirps():
            return lambda d: _chirps_path(intermed, d, self.chirps_disagg)

        cube_specs = [
            ("agera5", "Temperature_Air_2m_Max_24h", _path_agera5("Temperature_Air_2m_Max_24h"), tmax, "K2C"),
            ("agera5", "Temperature_Air_2m_Min_24h", _path_agera5("Temperature_Air_2m_Min_24h"), tmin, "K2C"),
        ]
        if self.eto_method == "penman_monteith":
            cube_specs.append(
                ("agera5", "Solar_Radiation_Flux", _path_agera5("Solar_Radiation_Flux"), rs, "J2MJ")
            )
        cube_specs.append(
            ("chirps", "precip", _path_chirps(), precip, "CHIRPS")
        )

        for kind, var_name, path_fn, out_arr, transform_kind in cube_specs:
            for year in years_in_sim:
                cube_tuple = self._load_cube(var_name, year, path_fn)
                if cube_tuple is None:
                    continue
                cube, transform, cube_dates = cube_tuple
                row, col = self._lonlat_to_rowcol(lon, lat, transform)
                if not (0 <= row < cube.shape[1] and 0 <= col < cube.shape[2]):
                    continue
                # Map cube dates → positions in this cell's sim_dates
                for i, ts in enumerate(dates):
                    if ts.year != year:
                        continue
                    doy = ts.timetuple().tm_yday - 1  # 0-indexed
                    if doy < 0 or doy >= cube.shape[0]:
                        continue
                    v = cube[doy, row, col]
                    if not np.isfinite(v):
                        continue
                    if transform_kind == "K2C":
                        out_arr[i] = v - 273.15
                    elif transform_kind == "J2MJ":
                        out_arr[i] = v * SR_J_TO_MJ
                    elif transform_kind == "CHIRPS":
                        if v == CHIRPS_FILL:
                            continue
                        out_arr[i] = v * CHIRPS_SCALE
                    else:
                        out_arr[i] = v

        # Data sufficiency: need at least 90% of days with temp + precip.
        # AquaCrop tolerates some interpolation, but not catastrophic loss.
        valid_temp = np.sum(np.isfinite(tmax) & np.isfinite(tmin))
        valid_precip = np.sum(np.isfinite(precip))
        if valid_temp < 0.9 * n or valid_precip < 0.9 * n:
            logger.debug(
                "Insufficient weather at (%.3f, %.3f): %d/%d temp, %d/%d precip",
                lon, lat, valid_temp, n, valid_precip, n,
            )
            return None

        # Forward-fill then back-fill remaining NaN; this only patches
        # occasional single-day gaps (AgERA5 latency, CHIRPS prelim swaps).
        tmax = pd.Series(tmax).ffill().bfill().to_numpy(dtype=np.float32)
        tmin = pd.Series(tmin).ffill().bfill().to_numpy(dtype=np.float32)
        precip = pd.Series(precip).ffill().bfill().fillna(0.0) \
            .to_numpy(dtype=np.float32)
        if self.eto_method == "penman_monteith":
            rs = pd.Series(rs).ffill().bfill().to_numpy(dtype=np.float32)

        # Compute ETo
        lat_rad = np.radians(lat)
        if self.eto_method == "penman_monteith" and np.all(np.isfinite(rs)):
            eto = _eto_penman_monteith(tmin, tmax, rs, lat_rad)
        else:
            doy = np.array([d.timetuple().tm_yday for d in dates], dtype=np.float32)
            eto = _eto_hargreaves(tmin, tmax, lat_rad, doy)

        df = pd.DataFrame({
            "MinTemp": tmin,
            "MaxTemp": tmax,
            "Precipitation": np.clip(precip, 0.0, None),
            "ReferenceET": eto,
            "Date": dates,
        })
        return df
