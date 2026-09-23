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

Conversions live here because nothing upstream does them:

* **NDVI is stored raw.** The CSV holds MOD09 digital numbers masked to
  ``[50, 250]``; only ``geoprepare.geomerge`` applies ``(ndvi - 50) / 200``, and
  this package does not go through geomerge. Forgetting it leaves NDVI ~100x
  too large and every derivative-based transition unchanged but every
  amplitude feature meaningless.
* **ESI is stored encoded.** The extractor writes ``(ESI + 4) * 10`` so the
  anomaly's ``[-4, 4]`` range fits ``[0, 80]``; it is decoded back here.
* **GDD needs a daily mean temperature.** The original read a single
  ``.air.csv``; here it is ``(chirts_era5_tmax + chirts_era5_tmin) / 2``, both
  already in degrees Celsius in the CSV.

Two kinds of variable
---------------------
NDVI and the two temperatures are **required**: without them nothing can be
scored. Precipitation, ESI and the two SMAP soil-moisture layers are
**optional**: they feed the model comparison's features and are read over the
same years as NDVI when present, and a region without them is still scored.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd

from geocif.cropcal import naming
from geocif.cropcal.circular import N_DOY

logger = logging.getLogger(__name__)

#: MOD09 "scale_mark" byte encoding: stored = NDVI * 200 + 50.
NDVI_OFFSET, NDVI_GAIN = 50.0, 200.0

#: ESI encoding written by geoprepare's extractor: stored = (ESI + 4) * 10, so
#: the standardised anomaly's valid range [-4, 4] maps onto [0, 80].
ESI_OFFSET, ESI_GAIN = 4.0, 10.0

#: Variables the rule-based validation REQUIRES.
VAR_NDVI = "ndvi"
VAR_TMAX = "chirts_era5_tmax"
VAR_TMIN = "chirts_era5_tmin"
VARIABLES = (VAR_NDVI, VAR_TMAX, VAR_TMIN)

#: Variables the model comparison uses when present. A region missing any of
#: them is still scored; only its moisture/stress features are NaN.
VAR_PRECIP = "chirps"
VAR_ESI = "esi_4wk"
VAR_SM_SURFACE = "nsidc_surface"
VAR_SM_ROOTZONE = "nsidc_rootzone"
OPTIONAL_VARIABLES = (VAR_PRECIP, VAR_ESI, VAR_SM_SURFACE, VAR_SM_ROOTZONE)

#: Composites observed less often than daily. Their year columns are gap-filled
#: only across the composite spacing, never across a season.
WEEKLY_VARIABLES = (VAR_ESI,)
WEEKLY_INTERPOLATION_LIMIT = 10

#: Physical range per variable after :func:`rescale`; anything outside is NaN.
#: Defence in depth against CSVs extracted before geoprepare 0.6.321, which let
#: ESI reach 568 and root-zone soil moisture 1250.
PHYSICAL_RANGE = {
    VAR_NDVI: (-1.0, 1.0),
    VAR_ESI: (-4.0, 4.0),
    VAR_SM_SURFACE: (0.0, 1.0),
    VAR_SM_ROOTZONE: (0.0, 1.0),
    VAR_PRECIP: (0.0, np.inf),
}

#: Years used for the per-day median, and whether the newest is dropped.
DEFAULT_NUM_YEARS = 5

#: An optional variable with fewer years than this inside the NDVI window is
#: treated as absent rather than averaged over a different period.
MIN_OPTIONAL_YEARS = 3


class SeriesError(ValueError):
    """Not enough usable EO data to build a climatology for a region."""


# --------------------------------------------------------------------------
# Scaling
# --------------------------------------------------------------------------
def rescale(values: np.ndarray, var: str) -> np.ndarray:
    """Apply the per-variable physical scaling geoextract leaves undone.

    NDVI arrives as MOD09 digital numbers, ESI as the ``(ESI + 4) * 10``
    encoding; both are decoded here. Every variable with a known physical range
    is then masked to it, so an out-of-range value from an older extraction
    becomes a gap rather than a feature.
    """
    arr = np.asarray(values, dtype=float)
    if var == VAR_NDVI:
        arr = (arr - NDVI_OFFSET) / NDVI_GAIN
    elif var == VAR_ESI:
        arr = arr / ESI_GAIN - ESI_OFFSET
    bounds = PHYSICAL_RANGE.get(var)
    if bounds is not None:
        low, high = bounds
        with np.errstate(invalid="ignore"):
            arr = np.where((arr < low) | (arr > high), np.nan, arr)
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

    Positional, deliberately: it drops the last column PRESENT. That is right
    for the variable that defines the window (NDVI) and wrong for any other,
    which must be aligned to that window instead -- see
    :func:`build_climatology`.
    """
    if frame.shape[1] == 0:
        raise SeriesError("no years available")
    usable = frame.iloc[:, :-1] if drop_last and frame.shape[1] > 1 else frame
    return usable.iloc[:, -num_years:]


def per_day_statistic(
    selected: pd.DataFrame,
    statistic: str = "median",
    *,
    interpolation_limit: Optional[int] = None,
) -> np.ndarray:
    """A ``366``-long per-day statistic over already-selected year columns.

    Each year column is gap-filled by linear interpolation first, matching the
    original. ``interpolate`` does not extrapolate, so a leading run of NaN
    survives and stays NaN in the result -- that is deliberate: a region whose
    record starts mid-year should not get a fabricated January.

    ``interpolation_limit`` bounds how many consecutive days one gap may be
    bridged: weekly composites need the 7-day spacing filled, not a whole
    cloudy monsoon or a polar winter ramped across with a straight line.

    ``statistic`` is ``"median"`` (the original's choice, right for a smooth
    variable like NDVI or temperature) or ``"mean"``. The mean is what an
    intermittent variable needs: rain falls on well under half the days even in
    a wet season, so the median of five daily values is 0 on most days, and a
    per-day-median rainfall climatology kept only ~25% of the annual total in a
    Sahel-like simulation while losing the onset and cessation shoulders
    entirely.
    """
    if selected.shape[1] == 0:
        return np.full(N_DOY, np.nan)
    filled = selected.interpolate(axis=0, limit_area="inside", limit=interpolation_limit)
    with np.errstate(all="ignore"):
        if statistic == "median":
            out = filled.median(axis=1, skipna=True)
        elif statistic == "mean":
            out = filled.mean(axis=1, skipna=True)
        else:
            raise ValueError(f"unknown statistic {statistic!r}")
    return out.to_numpy(dtype=float)


def per_day_median(
    frame: pd.DataFrame, num_years: int = DEFAULT_NUM_YEARS, *, drop_last: bool = True
) -> np.ndarray:
    """A ``366``-long per-day median over the selected years.

    Convenience wrapper: :func:`select_climatology_years` then
    :func:`per_day_statistic`. Kept for callers that hold a raw year frame
    rather than a pre-selected one.
    """
    selected = select_climatology_years(frame, num_years, drop_last=drop_last)
    return per_day_statistic(selected, "median")


def per_day_fraction_observed(selected: pd.DataFrame) -> np.ndarray:
    """Share of the selected years with a real observation on each day.

    Computed on the raw frame, BEFORE any interpolation, so a fabricated day
    never counts as observed. Retrieval availability is itself seasonal (cloud
    in the monsoon, snow and low sun at high latitude), which is why this is a
    feature and not only a quality flag.
    """
    if selected.shape[1] == 0:
        return np.full(N_DOY, np.nan)
    return selected.notna().mean(axis=1).to_numpy(dtype=float)


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
    """Everything the curve fit, the transition rules and the features need.

    ``ndvi`` and ``gdd`` are 366-long per-day medians; ``agdd`` is the running
    accumulation of ``gdd``; ``tmean`` is the per-day median mean temperature
    the GDD came from. ``ndvi_years`` is kept for the diagnostic figure's
    individual-year panel.

    The optional variables are loaded over the SAME years as NDVI
    (``years_used``), so every feature in a row describes one climatological
    window. Each is ``None`` when the region has no extraction for it, or fewer
    than :data:`MIN_OPTIONAL_YEARS` of those years; the feature builder turns
    ``None`` into NaN features plus an availability flag. ``precip`` is a
    per-day MEAN (see :func:`per_day_statistic`), the soil-moisture arrays are
    per-day medians, and ESI has no per-day level at all because it is an
    anomaly -- only its raw year frame is kept. The ``*_years`` frames are the
    selected raw year columns, for features that need per-year information
    (rain onset, moisture rise) or the interannual spread (ESI).
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
    tmean: Optional[np.ndarray] = None
    years_used: tuple = ()
    precip: Optional[np.ndarray] = None
    precip_years: Optional[pd.DataFrame] = None
    esi_years: Optional[pd.DataFrame] = None
    sm_surface: Optional[np.ndarray] = None
    sm_surface_years: Optional[pd.DataFrame] = None
    sm_rootzone: Optional[np.ndarray] = None
    sm_rootzone_years: Optional[pd.DataFrame] = None
    n_years_by_var: dict = field(default_factory=dict)

    @property
    def usable(self) -> bool:
        """Is there any signal at all? Mirrors the original's all-NaN/all-zero skip.

        Decided by NDVI and GDD only: scorability of the rule-based port must
        not depend on whether a region happens to have soil-moisture data.
        """
        return bool(
            np.isfinite(self.ndvi).any()
            and np.nanmax(np.abs(self.ndvi)) > 0
            and np.isfinite(self.agdd).any()
            and np.nanmax(self.agdd) > 0
        )

    @property
    def available(self) -> dict:
        """``{variable: bool}`` for the optional variables."""
        return {
            VAR_PRECIP: self.precip is not None,
            VAR_ESI: self.esi_years is not None,
            VAR_SM_SURFACE: self.sm_surface is not None,
            VAR_SM_ROOTZONE: self.sm_rootzone is not None,
        }


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
    optional_variables: Iterable[str] = OPTIONAL_VARIABLES,
) -> RegionClimatology:
    """Load NDVI and temperature for one region and reduce them to a climatology.

    NDVI decides the climatological window: the newest year is dropped as
    partial and the last ``num_years`` kept (see
    :func:`select_climatology_years`). Every other variable is then read over
    exactly those years. ``select_climatology_years`` is positional and drops
    the last column PRESENT, so applied per variable it would silently hand a
    variable whose feed stopped early (SMAP on a host with stale Earthdata
    credentials, ESI lagging weeks) a different five-year window from NDVI's,
    and one feature row would then mix two climatologies.
    """

    def _load(var: str) -> pd.DataFrame:
        return load_doy_year_frame(
            region_dir(root, floor, country, scale, crop, var),
            var,
            region_id,
            years=years,
        )

    ndvi_years = _load(VAR_NDVI)
    tmax_years, tmin_years = _load(VAR_TMAX), _load(VAR_TMIN)

    selected_ndvi = select_climatology_years(ndvi_years, num_years)
    years_used = tuple(int(y) for y in selected_ndvi.columns)

    def _aligned(frame: pd.DataFrame) -> pd.DataFrame:
        return frame.reindex(columns=list(years_used))

    ndvi = per_day_statistic(selected_ndvi, "median")
    tmax = per_day_statistic(_aligned(tmax_years), "median")
    tmin = per_day_statistic(_aligned(tmin_years), "median")
    tmean = (tmax + tmin) / 2.0
    gdd = growing_degree_days(tmean, params.min_base_temp, params.max_base_temp)
    agdd = np.nancumsum(np.where(np.isnan(gdd), 0.0, gdd))

    n_years_by_var = {
        VAR_NDVI: len(years_used),
        VAR_TMAX: int(_aligned(tmax_years).notna().any().sum()),
        VAR_TMIN: int(_aligned(tmin_years).notna().any().sum()),
    }

    wanted = set(optional_variables)

    def _load_optional(var: str) -> Optional[pd.DataFrame]:
        if var not in wanted:
            return None
        try:
            frame = _aligned(_load(var))
        except SeriesError as exc:
            logger.info(f"{country}/{crop}/{region}: no {var} ({exc}); its features will be NaN")
            n_years_by_var[var] = 0
            return None
        present = int(frame.notna().any().sum())
        n_years_by_var[var] = present
        if present < MIN_OPTIONAL_YEARS:
            logger.info(
                f"{country}/{crop}/{region}: {var} has {present} of the {len(years_used)} "
                f"NDVI years; treated as absent"
            )
            return None
        return frame

    precip_years = _load_optional(VAR_PRECIP)
    esi_years = _load_optional(VAR_ESI)
    sm_surface_years = _load_optional(VAR_SM_SURFACE)
    sm_rootzone_years = _load_optional(VAR_SM_ROOTZONE)

    return RegionClimatology(
        country=country,
        crop=crop,
        region=region,
        region_id=region_id,
        ndvi=ndvi,
        gdd=gdd,
        agdd=agdd,
        ndvi_years=ndvi_years,
        n_years=len(years_used),
        tmean=tmean,
        years_used=years_used,
        precip=None if precip_years is None else per_day_statistic(precip_years, "mean"),
        precip_years=precip_years,
        esi_years=esi_years,
        sm_surface=(
            None if sm_surface_years is None else per_day_statistic(sm_surface_years, "median")
        ),
        sm_surface_years=sm_surface_years,
        sm_rootzone=(
            None if sm_rootzone_years is None else per_day_statistic(sm_rootzone_years, "median")
        ),
        sm_rootzone_years=sm_rootzone_years,
        n_years_by_var=n_years_by_var,
    )
