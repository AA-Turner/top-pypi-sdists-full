# -*- coding: utf-8 -*-
"""Per-region daily EO CSVs -> a day-of-year x year matrix -> a climatology.

geoprepare's extraction writes one CSV per (region, year, variable)::

    {dir_output}/crop_t{floor}/{country}/{scale}/{crop}/{var}/
        {region_id}_{region}_{year}_{var}_{crop}.csv

    country,region,region_id,lat,lon,year,doy,<var>,total_pixels,valid_data,
    valid_data_after_masking,weight_sum,weight_sum_used

One row per day, always a complete year; days whose source raster was missing
come through as a NaN value. The reported value is already a **crop-fraction
weighted spatial mean** -- ``geom_extract`` passes the crop mask to
``np.ma.average`` as the weight array -- which is exactly the weighted mean the
original ``extract_NDVI_for_Regions.py`` computed with ``nanaverage``. That
script is therefore fully replaced, not reimplemented.

Two conversions live here because nothing upstream does them:

* **NDVI is stored raw.** The CSV holds MOD09 digital numbers masked to
  ``[50, 250]``; only ``geoprepare.geomerge`` applies ``(ndvi - 50) / 200``, and
  this package does not go through geomerge. Forgetting it leaves NDVI ~100x
  too large and every derivative-based transition unchanged but every
  amplitude feature meaningless.
* **GDD needs a daily mean temperature.** The original read a single
  ``.air.csv``; here it is ``(chirts_era5_tmax + chirts_era5_tmin) / 2``, both
  already in degrees Celsius in the CSV.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd

from geocif.cropcal import naming
from geocif.cropcal.circular import N_DOY

logger = logging.getLogger(__name__)

#: MOD09 "scale_mark" byte encoding: stored = NDVI * 200 + 50.
NDVI_OFFSET, NDVI_GAIN = 50.0, 200.0

#: Variables this package extracts.
VAR_NDVI = "ndvi"
VAR_TMAX = "chirts_era5_tmax"
VAR_TMIN = "chirts_era5_tmin"
VARIABLES = (VAR_NDVI, VAR_TMAX, VAR_TMIN)

#: Years used for the per-day median, and whether the newest is dropped.
DEFAULT_NUM_YEARS = 5


class SeriesError(ValueError):
    """Not enough usable EO data to build a climatology for a region."""


# --------------------------------------------------------------------------
# Scaling
# --------------------------------------------------------------------------
def rescale(values: np.ndarray, var: str) -> np.ndarray:
    """Apply the per-variable physical scaling geoextract leaves undone."""
    arr = np.asarray(values, dtype=float)
    if var == VAR_NDVI:
        return (arr - NDVI_OFFSET) / NDVI_GAIN
    return arr


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------
def region_dir(
    root: Path, floor: int, country: str, scale: str, crop: str, var: str
) -> Path:
    """The directory geoextract writes one variable's CSVs into.

    ``root`` is geoprepare's ``params.dir_output``, which **already ends in the
    project name** (``base.BaseGeo.parse_config`` appends it). Prepending the
    project again yields ``outputs/cropcal/cropcal/crop_t1/...`` and every
    region is reported as having no extraction -- which is exactly what happened
    on the first cluster run. Pass ``dir_output`` unchanged.
    """
    return Path(root) / f"crop_t{floor}" / country / scale / crop / var


_YEAR_RE = re.compile(r"(?<!\d)((?:19|20)\d{2})(?!\d)")


def _year_from_name(path: Path) -> Optional[int]:
    hits = _YEAR_RE.findall(path.stem)
    return int(hits[-1]) if hits else None


def load_doy_year_frame(
    directory: Path,
    var: str,
    region_id,
    *,
    years: Optional[Iterable[int]] = None,
) -> pd.DataFrame:
    """Every year of one variable for one region, as a ``366 x n_years`` frame.

    Index is day of year ``1..366``; columns are years, ascending. Missing days
    and missing years are NaN. Values are physically scaled by :func:`rescale`.

    Files are matched on the ``{region_id}_`` filename prefix, which is the
    ``num_ID`` assigned by ``geocif.data_prep.prepare_calendar_regions``.
    """
    directory = Path(directory)
    if not directory.is_dir():
        raise SeriesError(f"no extraction directory: {directory}")

    wanted = set(years) if years is not None else None
    columns: dict[int, pd.Series] = {}
    for path in sorted(directory.glob(f"{region_id}_*.csv")):
        year = _year_from_name(path)
        if year is None or (wanted is not None and year not in wanted):
            continue
        frame = pd.read_csv(path, usecols=lambda c: c in {"doy", var})
        if var not in frame.columns or "doy" not in frame.columns:
            logger.warning(f"{path.name}: no '{var}'/'doy' column; skipping")
            continue
        series = (
            frame.set_index("doy")[var]
            .groupby(level=0)
            .first()
            .reindex(range(1, N_DOY + 1))
        )
        columns[year] = pd.Series(rescale(series.to_numpy(), var), index=series.index)

    if not columns:
        raise SeriesError(f"no {var} files for region {region_id} in {directory}")
    out = pd.DataFrame(columns).sort_index(axis=1)
    out.index.name = "doy"
    return out


# --------------------------------------------------------------------------
# Climatology
# --------------------------------------------------------------------------
def select_climatology_years(
    frame: pd.DataFrame, num_years: int = DEFAULT_NUM_YEARS, *, drop_last: bool = True
) -> pd.DataFrame:
    """The last ``num_years`` complete years.

    ``drop_last`` removes the newest column before selecting, because the most
    recent year is almost always partial -- the original did this with a blunt
    ``iloc[:, -num_years - 1:-1]`` and it matters: including a year that stops
    in September drags the whole autumn of the median toward NaN.
    """
    if frame.shape[1] == 0:
        raise SeriesError("no years available")
    usable = frame.iloc[:, :-1] if drop_last and frame.shape[1] > 1 else frame
    return usable.iloc[:, -num_years:]


def per_day_median(
    frame: pd.DataFrame, num_years: int = DEFAULT_NUM_YEARS, *, drop_last: bool = True
) -> np.ndarray:
    """A ``366``-long per-day median over the selected years.

    Each year column is gap-filled by linear interpolation first, matching the
    original. ``interpolate`` does not extrapolate backwards, so a leading run
    of NaN survives and stays NaN in the median -- that is deliberate: a region
    whose record starts mid-year should not get a fabricated January.
    """
    selected = select_climatology_years(frame, num_years, drop_last=drop_last)
    filled = selected.interpolate(axis=0, limit_area="inside")
    with np.errstate(all="ignore"):
        median = filled.median(axis=1, skipna=True).to_numpy(dtype=float)
    return median


# --------------------------------------------------------------------------
# Growing degree days
# --------------------------------------------------------------------------
def growing_degree_days(
    tmean: np.ndarray, min_base_temp: float, max_base_temp: float
) -> np.ndarray:
    """Daily GDD from a daily mean temperature, in degrees Celsius.

    ``clip(T, base_min, base_max) - base_min``, floored at zero -- the original
    formulation, kept verbatim. NaN days contribute nothing.
    """
    arr = np.asarray(tmean, dtype=float)
    clipped = np.clip(arr, min_base_temp, max_base_temp)
    gdd = np.where(np.isnan(arr), np.nan, np.maximum(clipped - min_base_temp, 0.0))
    return gdd


# --------------------------------------------------------------------------
# Bundle
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class RegionClimatology:
    """Everything the curve fit and the transition rules need for one region.

    ``ndvi`` and ``gdd`` are 366-long per-day medians; ``agdd`` is the running
    accumulation of ``gdd``. ``ndvi_years`` is kept for the diagnostic figure's
    individual-year panel.
    """

    country: str
    crop: str
    region: str
    region_id: object
    ndvi: np.ndarray
    gdd: np.ndarray
    agdd: np.ndarray
    ndvi_years: pd.DataFrame
    n_years: int

    @property
    def usable(self) -> bool:
        """Is there any signal at all? Mirrors the original's all-NaN/all-zero skip."""
        return bool(
            np.isfinite(self.ndvi).any()
            and np.nanmax(np.abs(self.ndvi)) > 0
            and np.isfinite(self.agdd).any()
            and np.nanmax(self.agdd) > 0
        )


def build_climatology(
    root: Path,
    floor: int,
    country: str,
    scale: str,
    crop: str,
    region: str,
    region_id,
    *,
    params: naming.CropParams,
    years: Optional[Iterable[int]] = None,
    num_years: int = DEFAULT_NUM_YEARS,
) -> RegionClimatology:
    """Load NDVI and temperature for one region and reduce them to a climatology."""

    def _load(var: str) -> pd.DataFrame:
        return load_doy_year_frame(
            region_dir(root, floor, country, scale, crop, var),
            var,
            region_id,
            years=years,
        )

    ndvi_years = _load(VAR_NDVI)
    tmax_years, tmin_years = _load(VAR_TMAX), _load(VAR_TMIN)

    ndvi = per_day_median(ndvi_years, num_years)
    tmean = (per_day_median(tmax_years, num_years) + per_day_median(tmin_years, num_years)) / 2.0
    gdd = growing_degree_days(tmean, params.min_base_temp, params.max_base_temp)
    agdd = np.nancumsum(np.where(np.isnan(gdd), 0.0, gdd))

    return RegionClimatology(
        country=country,
        crop=crop,
        region=region,
        region_id=region_id,
        ndvi=ndvi,
        gdd=gdd,
        agdd=agdd,
        ndvi_years=ndvi_years,
        n_years=select_climatology_years(ndvi_years, num_years).shape[1],
    )
