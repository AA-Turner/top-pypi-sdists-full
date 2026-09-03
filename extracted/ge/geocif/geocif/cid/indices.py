import os
import logging
import re
import icclim
import numpy as np
import pandas as pd
from tqdm.rich import tqdm
from pathlib import Path
from typing import Iterable, NamedTuple, Union
from dateutil.relativedelta import relativedelta

from . import definitions as di  # For PHENOLOGICAL_STAGES, dict_indices, etc.
from geocif import utils  # For create_output_directory, compute_h_index, compute_biweekly_index, etc.

###############################################################################
#                          CONFIGURE LOGGING
###############################################################################
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


###############################################################################
#                          MODULE CONSTANTS
###############################################################################
# ICCLIM indices that must bypass the multi-year cache because their output
# depends on multi-year warm-up semantics. See Colab Q4: SPI3 per-year returns
# NaN for the first row (no warm-up) while a multi-year call returns valid
# values using prior-year data as warm-up — different semantics, cannot mix.
# Also reused by ``compute_indices`` to decide whether to pass ``slice_mode``:
# SPI rejects the ("season", ...) tuple and returns monthly output instead.
_ICCLIM_BYPASS_CACHE = frozenset({"SPI3", "SPI6"})

# Percentile / spell-duration indices require a 365-day-per-year base
# period because their thresholds are per-day-of-year percentiles fit on
# the baseline window — Feb 29 has ~1/4 the sample count of other DOYs
# and trips an icclim shape mismatch.  This set drives the Feb-29 drop
# in compute_indices.  Non-percentile indices (extremes/sums/counts)
# MUST keep Feb 29 in place: dropping it breaks slice_mode=("season",...)
# on leap-year seasons whose requested range spans Feb 29 — icclim emits
# NaN for the incomplete season and the wide-format fillna(0) turns the
# NaN into a false 0 (manifested as TXn=0 for every harvest year whose
# Nov-Apr window includes Feb 29; introduced 2026-04-13 in 0.4.366).
_PERCENTILE_INDICES = frozenset({
    "TG10p", "TN10p", "TX10p",
    "TG90p", "TN90p", "TX90p",
    "R75p", "R75pTOT", "R95p", "R95pTOT", "R99p", "R99pTOT",
    "CSDI",  # spell duration based on TX10p threshold
    "WSDI",  # spell duration based on TX90p threshold
})

# Memory-lean input reading. Every parallel year-task holds its own full
# copy of the merged input frame (multiprocessing, no shared memory), and at
# county scale (30M+ rows) plain object-dtype string columns dominate that
# copy: ~60-80 bytes/row/column vs 1-2 bytes as categorical codes. Reading
# the repeated-label columns as ``category`` and skipping display-only
# columns cut the per-worker frame from ~16 GB to ~5 GB on the usa_admin2
# run. Both sets are applied against the actual header (missing columns
# ignored), so inputs from any project/shape are safe.
_READ_DROP_COLS = frozenset({
    "name_month", "abbr_month", "day", "zone", "hemisphere",
    "average_temperature", "season_length_dekads", "season_start_month",
})
_READ_CATEGORY_COLS = frozenset({
    "country", "region", "adm0_name", "adm1_name", "adm2_name",
    "calendar_region", "crop", "scale",
})
# NOTE: groupbys whose keys include these categorical columns must pass
# ``observed=True`` wherever the code enumerates groups (list()/​.groups),
# otherwise pandas yields one (empty) group per unused category level —
# 3,111 county levels even in a frame filtered to a handful of regions.


# Columns kept at float64. Coordinates are matched/joined on rather than
# aggregated, so they stay exact; everything else is EO measurement data whose
# own precision is far coarser than float32.
_READ_FLOAT64_COLS = frozenset({"lat", "lon", "latitude", "longitude"})


#: rows per chunk when reading with a region filter — big enough that the
#: per-chunk overhead is irrelevant, small enough that the parse transient
#: stays a fraction of the full-file peak (13.2 GB on usa_admin2 soybean).
_READ_CHUNK_ROWS = 2_000_000

#: raw region column, in preference order (pre-standardize_dataframe names)
_REGION_COL_CANDIDATES = ("region", "adm2_name", "adm1_name")


def country_from_file_name(file_name):
    """``united_states_of_america_soybean_s1.csv`` -> ``united_states_of_america``.

    ``self.country`` is only populated by ``get_unique_country_name()`` AFTER
    the CSV has been read, but the run_regions filter has to resolve its config
    BEFORE the read (it filters during it). Deriving the country from the file
    name is the only source available at that point — an empty country silently
    falls through to [DEFAULT] and disables the filter, which is exactly the bug
    this fixes (1,759 counties written instead of 1,004).
    """
    try:
        crop, season = utils.get_crop_season(file_name)
        stem = Path(str(file_name)).stem
        suffix = f"_{crop}_s{season}"
        if crop and stem.endswith(suffix):
            return stem[: -len(suffix)]
    except Exception:
        pass
    return ""


def cid_run_region_selection(parser, country_key, crop, log=None):
    """Region names to restrict CID generation to, or None for all regions.

    Gated by ``filter_cids_to_run_regions`` (per-country section, inheriting
    [DEFAULT]; default OFF) because it couples the generated CID files to
    ``run_regions``: once filtered, adding a state later means regenerating
    that state's CIDs. The selection itself is parsed by
    ``ml.stats.parse_run_regions`` — the same function the ML frame filter
    uses, so the two cannot read the same config differently.

    Returns normalized names (lower-case, underscores -> spaces), matching
    ``ml.stats._norm_region_name``.
    """
    from geocif.ml import stats as ml_stats

    log = log or logger

    def option(name):
        for section in (country_key, "DEFAULT"):
            if section and parser.has_option(section, name):
                value = parser.get(section, name)
                if value is not None and str(value).strip():
                    return str(value).strip()
        return ""

    enabled = str(option("filter_cids_to_run_regions")).lower() in ("true", "1", "yes", "on")
    if not enabled:
        return None

    names = ml_stats.parse_run_regions(option("run_regions"), crop=crop, log=log)
    if not names:
        return None
    return {ml_stats._norm_region_name(n) for n in names}


def _region_keep_mask(regions: pd.Series, selection) -> pd.Series:
    """True where a region is selected, or is a child of a selected parent.

    Regions at admin_2 are ``state_county`` composites, so an admin_1
    selection ("illinois") keeps every ``illinois <county>``. Matching is done
    on normalized names with a single vectorized regex rather than one
    ``startswith`` pass per selected name.
    """
    from geocif.ml import stats as ml_stats

    normalized = ml_stats._norm_region_series(regions)
    pattern = "^(?:" + "|".join(re.escape(name) for name in sorted(selection)) + ")(?: |$)"
    return normalized.str.match(pattern, na=False)


def _read_input_csv(path: Union[str, Path], keep_regions=None) -> pd.DataFrame:
    """Read a merged input CSV (crop_t*/crop_p*) with category dtypes,
    float32 EO values and display-column drops.

    EO values are read as float32: measured on the usa_admin2 soybean input
    (7.6 GB, 28.4 M rows) the frame is 20.2 GB at pandas defaults, 5.3 GB with
    category dtypes, and 2.2 GB with float32 on top. The precision cost is
    ~6e-8 relative on real CID values (float32 carries ~7.2 significant
    decimal digits) — four-plus orders of magnitude below the precision of the
    satellite inputs the indices are derived from, and far below the ~9
    decimals these values are currently written out with. Coordinates are
    exempt (see _READ_FLOAT64_COLS).

    dtypes are resolved from a small probe read and passed to the full read,
    so the frame is never materialised at float64 and then downcast.
    """
    header = pd.read_csv(path, nrows=0)
    keep = [c for c in header.columns if c not in _READ_DROP_COLS]
    dtypes = {c: "category" for c in keep if c in _READ_CATEGORY_COLS}

    probe = pd.read_csv(path, usecols=keep, nrows=5000)
    for column in probe.columns:
        if column in dtypes or column in _READ_FLOAT64_COLS:
            continue
        if pd.api.types.is_float_dtype(probe[column]):
            dtypes[column] = "float32"
    del probe

    region_col = next((c for c in _REGION_COL_CANDIDATES if c in keep), None)
    if keep_regions and region_col is None:
        # Say so rather than silently returning every region — a filter that
        # quietly no-ops is exactly how the 1,759-vs-1,004 county bug hid.
        logger.warning(
            f"run_regions CID filter requested but {Path(path).name} has none of "
            f"{list(_REGION_COL_CANDIDATES)} — reading ALL regions unfiltered"
        )
    if not keep_regions or region_col is None:
        return pd.read_csv(path, usecols=keep, dtype=dtypes)

    # Filter DURING the read: dropping rows afterwards would still pay the
    # full-file parse transient, which is what actually bounds how many
    # workers fit on the node.
    parts = []
    for chunk in pd.read_csv(path, usecols=keep, dtype=dtypes,
                             chunksize=_READ_CHUNK_ROWS):
        mask = _region_keep_mask(chunk[region_col], keep_regions)
        if mask.any():
            parts.append(chunk.loc[mask])

    if not parts:
        logger.warning(
            f"region filter kept 0 rows from {Path(path).name} — check "
            f"run_regions against the region names in the input"
        )
        return pd.read_csv(path, usecols=keep, dtype=dtypes, nrows=0)

    out = pd.concat(parts, ignore_index=True)
    del parts
    # Concatenating categoricals whose category sets differ degrades them to
    # object dtype, which would undo the whole point of reading them as
    # category. Restore it on the (now much smaller) frame.
    for column in _READ_CATEGORY_COLS:
        if column in out.columns and not isinstance(out[column].dtype, pd.CategoricalDtype):
            out[column] = out[column].astype("category")
    return out


def filter_frame_to_yield_regions(df, parser, admin_zone, country_key, crop):
    """Drop regions that have zero usable yield records for (country, crop).

    CID computation is yield-agnostic, so without this every EO-covered
    region gets the full index treatment even when it can never contribute
    to training or verification (at US county scale, 20-34% of counties).
    Gated by the ``filter_regions_without_yields`` config flag (per-country
    section, inheriting [DEFAULT]; default off). Yield coverage comes from
    ml.stats.regions_with_yields, which shares its file resolution and
    name normalization with the stats join itself — the filter can never
    disagree with what add_statistics would later join.

    Scale-generic by construction: ``admin_zone`` ("admin_1"/"admin_2")
    names the production-statistics column the regions live in, so the
    same code path serves state- and county-level projects.

    Returns df unchanged when the flag is off, the frame is empty, or
    coverage is unknown (regions_with_yields -> None).
    """
    try:
        flag = parser.getboolean(
            country_key, "filter_regions_without_yields", fallback=False
        )
    except Exception:
        try:
            flag = parser.getboolean(
                "DEFAULT", "filter_regions_without_yields", fallback=False
            )
        except Exception:
            flag = False
    if not flag or df.empty or "adm1_name" not in df.columns:
        return df

    from geocif.ml import stats as ml_stats

    dir_stats = parser.get("PATHS", "dir_production_statistics")
    # Display forms matching the production-statistics 'country'/'product'
    # columns — same conversion as utils.statistics_file_path.
    country_str = country_key.title().replace("_", " ")
    crop_str = crop.title().replace("_", " ")
    keep = ml_stats.regions_with_yields(
        dir_stats, country_str, crop_str, admin_zone, parser=parser
    )
    if keep is None:
        logger.warning(
            f"filter_regions_without_yields: yield coverage unknown for "
            f"{country_str}/{crop_str} ({admin_zone}) — not filtering"
        )
        return df

    col = df["adm1_name"]
    n_before = col.nunique()
    if isinstance(col.dtype, pd.CategoricalDtype):
        # Normalize the ~few-thousand category levels, not the 30M row
        # values — then select by code position.
        cats_norm = ml_stats._norm_region_series(pd.Series(col.cat.categories))
        keep_positions = np.flatnonzero(cats_norm.isin(keep).to_numpy())
        mask = col.cat.codes.isin(keep_positions).to_numpy()
    else:
        mask = ml_stats._norm_region_series(col).isin(keep).to_numpy()

    # shallow copy: clears the chained-assignment parent link left by the
    # boolean mask without duplicating the underlying blocks
    df = df[mask].copy(deep=False)
    for c in df.columns:
        if isinstance(df[c].dtype, pd.CategoricalDtype):
            df[c] = df[c].cat.remove_unused_categories()
    n_after = df["adm1_name"].nunique() if not df.empty else 0
    logger.info(
        f"filter_regions_without_yields: {country_str}/{crop_str} "
        f"({admin_zone}): kept {n_after}/{n_before} regions "
        f"({n_before - n_after} without yield records dropped)"
    )
    return df


class ProcessFileArgs(NamedTuple):
    """
    Picklable arguments for ``process_file``. Using a NamedTuple instead of a
    raw 9-tuple so fields are self-documenting, callers build by keyword, and
    multiprocessing pickling still works (NamedTuple subclasses tuple).
    """
    parser: object           # configparser.ConfigParser — forward-ref to avoid import
    process_type: str
    file_path: Union[str, Path]
    file_name: str
    admin_zone: str
    method: str
    years: Iterable[int]
    vi_var: str
    redo: bool
    show_progress: bool = True        # False in parallel mode to suppress inner tqdm
    stage_mode: str = "cumulative"    # "cumulative" or "individual"


class ProcessTaskArgs(NamedTuple):
    """
    Picklable arguments for ``process_task``.  One instance represents a
    single (file, year, region) work unit — the finest grain of parallelism.
    """
    parser: object
    process_type: str
    file_path: Union[str, Path]
    file_name: str
    admin_zone: str
    method: str
    year: int                          # single harvest year
    region: tuple                      # (adm0_name, adm1_name)
    vi_var: str
    redo: bool
    stage_mode: str = "cumulative"


# Per-process cache: avoids re-reading + standardizing the same CSV in every
# worker when a Pool reuses the same process for multiple tasks from the same
# file.  Keyed by str(file_path).
_preprocess_cache: dict = {}


###############################################################################
#                          HELPER FUNCTIONS
###############################################################################
def standardize_dataframe(df: pd.DataFrame, vi_var: str) -> pd.DataFrame:
    """
    Perform standard data cleaning and column unification.

    Args:
        df (pd.DataFrame): The raw input DataFrame.
        vi_var (str): The vegetation index column name to handle (e.g. "ndvi").

    Returns:
        pd.DataFrame: Cleaned DataFrame with standardized columns and values.
    """
    # Detect AgERA5 snow source BEFORE rename so we can convert m → cm later.
    # icclim's Snow indices (SD/SD1/SD5cm/SD50cm) expect snow depth in cm
    # (see df_to_xarray attrs); AgERA5 reports liquid-water-equivalent in m.
    _snow_from_agera5 = "agera5_snow_thickness_lwe" in df.columns

    # Rename columns to unify climate variable names
    rename_dict = {
        "original_yield": "yield",
        "datetime": "time",
        "JD": "Doy",
        "doy": "Doy",
        "cpc_tmax": "tasmax",
        "cpc_tmin": "tasmin",
        "cpc_precip": "pr",
        "chirps": "pr",  # if present, unify with "pr"
        "daymet_tmax": "tasmax",
        "daymet_tmin": "tasmin",
        "daymet_prcp": "pr",
        "chirts_era5_tmax": "tasmax",
        "chirts_era5_tmin": "tasmin",
        "snow": "snd",
        "agera5_snow_thickness_lwe": "snd",
        "esi_4wk": "esi_4wk",
        "region": "adm1_name",
        "harvest_season": "Season",
        "crop_calendar": "crop_cal",
        "month": "Month",
        "country": "adm0_name",
    }
    df = df.rename(columns=rename_dict)

    # Assign lat/lon = 0 if not present or for simplicity
    if "lat" not in df.columns:
        df["lat"] = 0
    if "lon" not in df.columns:
        df["lon"] = 0

    # Remove rows where crop_cal is "" or just a space
    df = df[df["crop_cal"] != " "]
    df = df[df["crop_cal"] != ""]

    # Convert crop_cal to float; keep only known stages (+ pre-season rows if present)
    df["crop_cal"] = df["crop_cal"].astype(float)
    valid_stages = list(di.PHENOLOGICAL_STAGES) + [0]  # include pre-season (crop_cal=0)
    df = df[df["crop_cal"].isin(valid_stages)]

    # Convert the date columns properly
    if "time" not in df.columns:
        # Use year + day of year if no time column
        df["time"] = pd.to_datetime(
            df["year"].astype(str) + df["Doy"].astype(str),
            format="%Y%j"
        )
    else:
        df["time"] = pd.to_datetime(df["time"])

    # Derive Month and Doy from time if not present
    if "Month" not in df.columns:
        df["Month"] = df["time"].dt.month
    if "Doy" not in df.columns:
        df["Doy"] = df["time"].dt.dayofyear

    # Compute "Area" if needed (example from the original code)
    if "tot_pix" in df.columns and "mean_crop" in df.columns:
        df["Area"] = df["tot_pix"] * df["mean_crop"]
    else:
        df["Area"] = np.nan

    # If "snow" didn't exist, fill with np.nan
    if "snd" not in df.columns:
        df["snd"] = np.nan
    else:
        # AgERA5 snow_thickness_lwe is in meters; icclim Snow indices expect cm.
        if _snow_from_agera5:
            df["snd"] = df["snd"] * 100.0
        df["snd"] = df["snd"].fillna(0)

    # Compute daily mean temperature
    if "tasmax" in df.columns and "tasmin" in df.columns:
        df["tg"] = (df["tasmax"] + df["tasmin"]) / 2

    # Rescale NDVI if needed
    if vi_var in df.columns:
        if df[vi_var].max() > 1:
            df[vi_var] = (df[vi_var] - 50) / 200

    # Year range is controlled by the primary loop in indices_runner.py
    # (`[DEFAULT] start_year`). No belt-and-suspenders Season filter
    # here — it would silently block legitimate widened ranges.

    return df


def add_season_information(
    df: pd.DataFrame,
    method: str
) -> pd.DataFrame:
    """
    Adds season information depending on the user-defined method.
    Supported methods: fraction_season, dekad/dekad_r, biweekly/biweekly_r, monthly/monthly_r.

    Args:
        df (pd.DataFrame): The input DataFrame with "Season", "Doy", "Month" columns, etc.
        method (str): The method used to add seasonal grouping.

    Returns:
        pd.DataFrame: Updated DataFrame with an additional grouping column.
    """
    # Group by region/Season so each region gets its own partition.
    # observed=True: adm1_name is categorical (read_crop_t0) — without it this
    # loop would visit one empty frame per unused region level.
    grps = df.groupby(["adm1_name", "Season"], dropna=False, observed=True)
    frames = []

    for key, df_adm1_season in grps:
        if method == "fraction_season":
            step = 10
            N = len(df_adm1_season)
            # Create a fraction_season column: 10,20,...,100 (integer deciles;
            # keep int dtype so the Stage label is "10_20_..." not "10.0_20.0_...").
            df_adm1_season["fraction_season"] = (
                                                    np.linspace(10, 100 + step, N + 1) // step * step
                                                )[:-1].astype(int)

        elif method in ["dekad", "dekad_r"]:
            df_adm1_season[method] = df_adm1_season["Doy"] // 10 + 1

        elif method in ["biweekly", "biweekly_r"]:
            df_adm1_season[method] = df_adm1_season.apply(utils.compute_biweekly_index, axis=1)

        elif method in ["monthly", "monthly_r"]:
            df_adm1_season[method] = df_adm1_season["Month"]

        frames.append(df_adm1_season)

    return pd.concat(frames)


def df_to_xarray(vals: pd.DataFrame):
    """
    Convert a (lat, lon, time)-indexed DataFrame to an xarray Dataset
    suitable for icclim calculations.

    Args:
        vals (pd.DataFrame): DataFrame with columns lat, lon, time, tasmax, tasmin, tg, pr, snd.

    Returns:
        (xr.Dataset, pd.DataFrame): The resulting xarray Dataset and the same data as indexed DataFrame.
    """
    vals_ix = vals.set_index(["lat", "lon", "time"])
    dx = vals_ix.to_xarray()

    # Set metadata/attributes
    for var_name in ["tasmax", "tasmin", "tg"]:
        if var_name in dx:
            dx[var_name].attrs["units"] = "C"
            dx[var_name].attrs["missing_value"] = np.nan

    if "pr" in dx:
        dx["pr"].attrs["units"] = "mm/day"
        dx["pr"].attrs["missing_value"] = np.nan

    if "snd" in dx:
        dx["snd"].attrs["units"] = "cm"
        dx["snd"].attrs["missing_value"] = np.nan

    return dx, vals_ix


def get_icclim_dates(
    df_all_years_ix: pd.DataFrame,
    df_harvest_year_ix: pd.DataFrame
) -> tuple[str, str, str, str]:
    """
    Determine time ranges for base period and time range for ICCLIM calculations.

    Args:
        df_all_years_ix (pd.DataFrame): Full dataset (indexed by lat, lon, time).
        df_harvest_year_ix (pd.DataFrame): Harvest-year-only subset (indexed).

    Returns:
        tuple[str, str, str, str]: (start_br, end_br, start_tr, end_tr)
    """
    # start_br: earliest date + 1 year
    start_br = str(df_all_years_ix.index[0][2] + relativedelta(years=1))
    # end_br: latest date - 2 years
    end_br = str(df_all_years_ix.index[-1][2] - relativedelta(years=2))

    start_tr = np.datetime_as_string(df_harvest_year_ix.index[0][2].to_datetime64())
    end_tr = np.datetime_as_string(df_harvest_year_ix.index[-1][2].to_datetime64())

    return start_br, end_br, start_tr, end_tr


# icclim indices that require a minimum number of days in the target slice
# because they apply a rolling/run-length window of that size.  When the
# time slice has fewer days, icclim raises ``ValueError: Moving window
# (=N) must between 1 and M, inclusive`` at materialization (xarray.compute).
# Pre-checked here so we skip cleanly with a warning instead of crashing
# the whole region/year task.
#
#   RX5day → rolling 5-day precip window
#   WSDI / CSDI → ≥6 consecutive days above/below 90th/10th percentile
#
# Other run-length indices (CFD/CDD/CWD/CSU) tolerate short slices and
# return 0/1.  Most other indices are per-day counts/extremes/percentiles
# and have no window requirement.
_INDEX_MIN_DAYS = {
    "RX5day": 5,
    "WSDI": 6,
    "CSDI": 6,
}


# Custom CID indices NOT in icclim's ECAD/ETCCDI catalog — computed directly
# with numpy over the (already stage/season-restricted) daily frame. Simpler
# and clearer than bending icclim's user_index to fit; ``compute_indices``
# short-circuits to ``_compute_numpy_index`` for these and returns a Dataset
# shaped like the icclim path so downstream handling is unchanged.
#   DD  — number of dry days (pr < 1 mm). Direct complement of RR1 (wet days);
#         distinct from CDD, the LONGEST dry SPELL.
#   KDD — killing degree days: sum of daily Tmax excess above KDD_THRESHOLD_C
#         (sum of max(0, Tmax - thresh)). Heat-side complement to GD4 / HD17.
KDD_THRESHOLD_C = 32.0  # killing-degree-day heat threshold (deg C)


def _cid_dry_days(pr: pd.Series) -> float:
    """DD: count of dry days (pr < 1 mm). NaN precip days are not counted."""
    v = pd.to_numeric(pr, errors="coerce").to_numpy()
    return float(np.sum(v < 1.0))


def _cid_killing_degree_days(tasmax: pd.Series) -> float:
    """KDD: sum of daily Tmax excess above KDD_THRESHOLD_C (deg C)."""
    v = pd.to_numeric(tasmax, errors="coerce").to_numpy()
    return float(np.nansum(np.clip(v - KDD_THRESHOLD_C, 0.0, None)))


# index name -> (required daily column, per-cell/season scalar reducer)
_NUMPY_INDEX_FUNCS = {
    "DD": ("pr", _cid_dry_days),
    "KDD": ("tasmax", _cid_killing_degree_days),
}


def _compute_numpy_index(index_name: str, df_time_period: pd.DataFrame):
    """Compute a custom numpy index over the target window (no icclim).

    Reduces per (lat, lon[, Season]) group to a scalar and returns a Dataset
    whose only data variable is ``index_name`` — so the caller's
    ``ds.to_dataframe().reset_index()`` yields an ``index_name`` column exactly
    like the icclim path (``process_row`` then collapses via ``iloc[0]``).
    Returns None when the required daily column is missing/empty.
    """
    req_col, reducer = _NUMPY_INDEX_FUNCS[index_name]
    if df_time_period.empty or req_col not in df_time_period.columns:
        return None
    keys = [c for c in ("lat", "lon", "Season") if c in df_time_period.columns]
    if keys:
        vals = df_time_period.groupby(keys, dropna=False)[req_col].apply(reducer)
        return vals.rename(index_name).to_frame().to_xarray()
    return pd.DataFrame({index_name: [reducer(df_time_period[req_col])]}).to_xarray()


def _reindex_daily_continuous(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing daily dates (per lat/lon) with NaN precip so icclim SPI
    can infer a uniform timestep. The season-1 merged CSVs drop out-of-season
    days, giving ~1-month yearly gaps that icclim.SPI rejects with "source
    timestep can't be inferred from the data". Reindexing to a continuous
    daily calendar with NaN-fill preserves the original in-season signal
    while satisfying icclim's uniform-frequency requirement.
    """
    if df.empty or "time" not in df.columns:
        return df
    df = df.copy()
    df["time"] = pd.to_datetime(df["time"])

    def _fill_one_cell(sub: pd.DataFrame) -> pd.DataFrame:
        sub = sub.drop_duplicates(subset=["time"]).sort_values("time")
        full_dates = pd.date_range(sub["time"].min(), sub["time"].max(), freq="D")
        sub = sub.set_index("time").reindex(full_dates)
        # Restore constant columns that reindex NaN-ed (lat, lon)
        for col in ("lat", "lon", "adm0_name", "adm1_name"):
            if col in sub.columns:
                sub[col] = sub[col].bfill().ffill()
        sub.index.name = "time"
        return sub.reset_index()

    if {"lat", "lon"}.issubset(df.columns):
        parts = [_fill_one_cell(g) for _, g in df.groupby(["lat", "lon"], dropna=False)]
        return pd.concat(parts, ignore_index=True)
    return _fill_one_cell(df)


def compute_indices(
    df_time_period: pd.DataFrame,
    df_base_period: pd.DataFrame,
    index_name: str,
    logs_verbosity: str = "LOW"
):
    """
    Compute climate indices using icclim. Uses slice_mode=("season", tuple) for
    non-SPI indices so cross-year harvest windows (Southern Hemisphere) aggregate
    into one row per harvest year natively, without a time-shift hack.

    Args:
        df_time_period (pd.DataFrame): DataFrame for the target/harvest year sub-period.
            May span multiple harvest years when called through the ICCLIM cache
            — icclim will emit one row per season window in that case.
        df_base_period (pd.DataFrame): DataFrame for the baseline reference period.
        index_name (str): The name of the index to compute (e.g., "SPI3", "SU", etc.).

    Returns:
        xr.Dataset or None: The computed Dataset if successful, else None.
    """
    ds = None

    # Custom numpy-computed indices (DD, KDD): computed directly over the
    # stage/season-restricted target frame — no icclim. Returned as a Dataset
    # so the downstream ds.to_dataframe() -> process_row flow is identical to
    # the catalog-index path.
    if index_name in _NUMPY_INDEX_FUNCS:
        return _compute_numpy_index(index_name, df_time_period)

    # Drop Feb 29 ONLY for percentile / spell-duration indices that need
    # a 365-day per-year base period.  Leaving Feb 29 in place for
    # non-percentile indices avoids breaking slice_mode=("season",...)
    # on leap-year seasons that span Feb 29 — see _PERCENTILE_INDICES.
    if index_name in _PERCENTILE_INDICES:
        _leap = lambda d: (d["time"].dt.month == 2) & (d["time"].dt.day == 29)
        df_base_period = df_base_period[~_leap(df_base_period)]
        df_time_period = df_time_period[~_leap(df_time_period)]

    # Skip windowed indices when the target slice is shorter than the
    # rolling/spell window — icclim would otherwise raise at compute time.
    # The caller (process_group) is responsible for logging with full
    # file/year/region context; we just return None silently here.
    min_days = _INDEX_MIN_DAYS.get(index_name)
    if min_days is not None:
        n_days = df_time_period["time"].dt.normalize().nunique()
        if n_days < min_days:
            return None

    # icclim SPI needs a uniform daily timestep to compute its missing-values
    # mask. The season-1 merged CSV drops non-growing-season days, leaving
    # ~1-month gaps per year. Reindex df_base_period (which for SPI is the
    # full multi-year df_group per process_group) to a continuous daily
    # calendar, filling missing days' pr with NaN. Non-SPI indices skip
    # this — their season/stage-restricted flow doesn't need continuous
    # time and the reindex would add spurious NaN rows to their windows.
    if index_name in _ICCLIM_BYPASS_CACHE:
        df_base_period = _reindex_daily_continuous(df_base_period)

    dx, vals_ix = df_to_xarray(df_base_period)
    start_br, end_br, start_tr, end_tr = get_icclim_dates(vals_ix, df_time_period.set_index(["lat", "lon", "time"]))

    # Derive the season window from a representative single harvest year so that
    # cross-year seasons (e.g. Oct–Jun winter wheat) get the correct end date
    # from the second calendar year.  Sampling by first calendar year alone
    # would stop at Dec 31 and produce the wrong slice_mode tuple.
    rep_season = df_time_period["Season"].iloc[0]
    rep_sample = (
        df_time_period[df_time_period["Season"] == rep_season]
        .sort_values("time")
    )
    season_start = rep_sample["time"].iloc[0].strftime("%d %B")
    season_end = rep_sample["time"].iloc[-1].strftime("%d %B")

    kwargs = dict(
        index_name=index_name,
        in_files=dx,
        base_period_time_range=[start_br, end_br],
        time_range=[start_tr, end_tr],
        logs_verbosity=logs_verbosity,
    )
    # SPI rejects slice_mode entirely and returns monthly output. Every other
    # index gets the ("season", ...) tuple so cross-year harvest windows
    # aggregate into one row per harvest year natively.
    orig_start_tr, orig_end_tr = start_tr, end_tr
    if index_name not in _ICCLIM_BYPASS_CACHE:
        kwargs["slice_mode"] = ("season", (season_start, season_end))
    else:
        # icclim SPI fits a gamma distribution over the full time_range
        # window and only produces valid values when it has enough data
        # points (empirically >=~2 years). A stage-restricted time_range
        # (Feb-Apr = 3 months) produces all-NaN even with a valid
        # base_period_time_range — the fit collapses on the narrow slice.
        # icclim also rejects slice_mode=... entirely for SPI3/SPI6, so we
        # can't ask it for monthly aggregation directly.
        #
        # Fix: hand icclim the FULL in_files time span as time_range so its
        # internal fit has plenty of data. Then trim the returned monthly
        # SPI series back to the original stage window (Python-side .sel)
        # before returning. process_row aggregates those monthly values to
        # the stage-level mean.
        idx0 = vals_ix.index[0][2]
        idx_last = vals_ix.index[-1][2]
        kwargs["time_range"] = [
            pd.Timestamp(idx0).strftime("%Y-%m-%d"),
            pd.Timestamp(idx_last).strftime("%Y-%m-%d"),
        ]

    try:
        ds = icclim.index(**kwargs)
    except Exception as e:
        logger.error(
            f"Error computing {index_name} for {start_tr} to {end_tr}: {e}"
        )
        return None

    # Trim the internal extension so only the target stage window's monthly
    # SPI values reach process_row. process_row then aggregates these to a
    # single stage-level CID (mean).
    if index_name in _ICCLIM_BYPASS_CACHE and ds is not None:
        try:
            ds = ds.sel(time=slice(str(orig_start_tr), str(orig_end_tr)))
        except (KeyError, ValueError) as e:
            logger.warning(
                f"Could not trim {index_name} output to {orig_start_tr}..{orig_end_tr}: {e}"
            )

    return ds


def aggregate_eo_values(eo_vals: np.ndarray, agg_type: str) -> float:
    """
    Apply a specified aggregation (min, max, mean, std, AUC, H-INDEX) to an array of values.

    Args:
        eo_vals (np.ndarray): Input array of EO or climate variable values.
        agg_type (str): The aggregation type (MIN, MAX, MEAN, STD, AUC, H-INDEX).

    Returns:
        float: The computed aggregated value (NaN if empty or invalid).
    """
    eo_vals = eo_vals[~np.isnan(eo_vals)]
    if not len(eo_vals):
        return float('nan')

    agg_type = agg_type.upper()
    if agg_type == "MIN":
        return np.nanmin(eo_vals)
    elif agg_type == "MAX":
        return np.nanmax(eo_vals)
    elif agg_type == "MEAN":
        return np.nanmean(eo_vals)
    elif agg_type == "STD":
        return np.nanstd(eo_vals)
    elif agg_type == "AUC":
        return np.trapezoid(eo_vals)
    elif agg_type == "H-INDEX":
        # Example: multiply by 10 for the h-index logic
        return utils.compute_h_index(eo_vals * 10)
    # --- drought depth/duration/spread family (pure per-window functions) ---
    # P<nn>: nn-th percentile (robust drought depth for low nn).
    elif agg_type.startswith("P") and agg_type[1:].isdigit():
        return float(np.nanpercentile(eo_vals, int(agg_type[1:])))
    # AUCDEF<t>: mean deficit below threshold t = mean(max(0, t - x)) — how far
    # below t and for how much of the window (integrated drought magnitude).
    elif agg_type.startswith("AUCDEF"):
        thr = float(agg_type[6:])
        return float(np.nanmean(np.clip(thr - eo_vals, 0, None)))
    # FRACLO<t>: fraction of the window below threshold t (drought duration).
    elif agg_type.startswith("FRACLO"):
        thr = float(agg_type[6:])
        return float(np.mean(eo_vals < thr))
    elif agg_type == "CV":
        m = np.nanmean(eo_vals)
        return float(np.nanstd(eo_vals) / m) if m else float("nan")
    elif agg_type == "IQR":
        return float(np.nanpercentile(eo_vals, 75) - np.nanpercentile(eo_vals, 25))
    elif agg_type == "RANGE":
        return float(np.nanmax(eo_vals) - np.nanmin(eo_vals))
    else:
        raise ValueError(f"Invalid aggregation type: {agg_type}")


METHOD_TO_COLUMN = {
    "phenological_stages": "crop_cal",
    "full_season": "crop_cal",
    "fraction_season": "fraction_season",
    "dekad": "dekad",
    "dekad_r": "dekad_r",
    "biweekly": "biweekly",
    "biweekly_r": "biweekly_r",
    "monthly": "monthly",
    "monthly_r": "monthly_r"
}


###############################################################################
#                          MAIN CLASS CIDs
###############################################################################
class CIDs:
    """
    The main class orchestrating the extraction and computation of climate
    and environmental indices (CIDs) for a given country/crop/season dataset.
    """

    def __init__(
        self,
        parser,
        process_type: str,
        file_path: str,
        file_name: str,
        admin_zone: str,
        method: str,
        harvest_year: int,
        redo: bool
    ) -> None:
        """
        Initialize the CIDs class with relevant parameters and placeholders.

        Args:
            parser: Config parser or similar object to fetch base directories.
            process_type (str): Indicates the process type (e.g. with or without Fall info).
            file_path (str): Full path to the CSV file being processed.
            file_name (str): The name of the CSV file (used for crop/season extraction).
            admin_zone (str): The admin zone level ("admin_1", "admin_2", etc.).
            method (str): The method for splitting seasons (full_season, fraction_season, etc.).
            harvest_year (int): The year of harvest.
            redo (bool): If True, force re-computation even if files exist.
        """
        self.parser = parser
        self.process_type = process_type
        self.file_path = file_path
        self.file_name = file_name
        self.admin_zone = admin_zone
        self.method = method
        self.harvest_year = harvest_year
        self.redo = redo

        # Will be assigned later (placeholders; set by get_unique_country_name
        # and _run_one_year before use).
        self.country: str = ""
        self.crop: str = ""
        self.season: int = 0

        # Directories
        self.dir_output = None
        self.dir_intermediate = None

        # DataFrames
        self.df_country_crop = pd.DataFrame()
        self.df_harvest_year = pd.DataFrame()

        # Controls whether inner tqdm bars are shown (disabled in parallel mode
        # to avoid garbled output from multiple child processes).
        self.show_progress: bool = True

        # Stage combination mode: "cumulative" (all contiguous sub-sequences)
        # or "individual" (full season + each single stage).
        self.stage_mode: str = "cumulative"

        # Paths — include project_name so output lands under {dir_output}/{project_name}/
        project_name = self.parser.get("DEFAULT", "project_name")
        self.dir_base = Path(self.parser.get("PATHS", "dir_output")) / project_name

        # icclim log suppression
        if self.parser.has_option("DEFAULT", "suppress_icclim_logs"):
            self.suppress_icclim_logs = self.parser.getboolean("DEFAULT", "suppress_icclim_logs")
        else:
            self.suppress_icclim_logs = False

        # Pre-season mode: extract FLDAS/S2S from init-month rows for all leads.
        # "auto" also needs pre-season extraction (alongside in-season CIDs).
        self.pre_season_mode: bool = (
            self.parser.get("ML", "run_time_steps", fallback="latest") in ("pre_season", "auto")
        )

        # Compute engineered forecast aggregates (SUM, AVG, REV, MAR) from leads
        self.compute_forecast_aggregates: bool = (
            self.parser.getboolean("ML", "compute_forecast_aggregates", fallback=True)
        )

    def get_unique_country_name(
        self,
        df: pd.DataFrame = None,
        col: str = "adm0_name"
    ) -> None:
        """
        Extract a single country name from the provided DataFrame and set it as 'self.country'.

        Args:
            df (pd.DataFrame): If None, uses self.df_harvest_year.
            col (str): The column name containing the country name.
        """
        if df is None:
            df = self.df_harvest_year
        if df.empty:
            raise ValueError("Dataframe is empty. Cannot extract country name.")
        self.country = df[col].unique()[0].lower().replace(" ", "_")

    def add_season_information(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Wrapper to add season columns to the data, based on self.method.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: Updated DataFrame with additional grouping column(s).
        """
        return add_season_information(df, self.method)

    def preprocess_input_df(self, vi_var: str = "ndvi") -> pd.DataFrame:
        """
        Main entry point for reading and standardizing the input CSV.

        Args:
            vi_var (str): The vegetation index column name (default: "ndvi").

        Returns:
            pd.DataFrame: The standardized input DataFrame.
        """
        # Restrict to run_regions at READ time when the project opted in, so
        # neither the parse transient nor the cached frame ever holds regions
        # this project will not model (usa_admin2: 2038 -> 919 counties).
        try:
            keep_regions = cid_run_region_selection(
                self.parser,
                # NOT self.country — it is still "" until the CSV is read.
                self.country or country_from_file_name(self.file_name),
                self.crop or utils.get_crop_season(self.file_name)[0],
            )
        except Exception as e:
            logger.warning(f"run_regions CID filter skipped: {type(e).__name__}: {e}")
            keep_regions = None

        try:
            df = _read_input_csv(self.file_path, keep_regions=keep_regions)
            if keep_regions:
                logger.info(
                    f"CID region filter: {Path(self.file_path).name} restricted to "
                    f"{len(keep_regions)} selected parent region(s) -> "
                    f"{df['region'].nunique() if 'region' in df.columns else '?'} regions, "
                    f"{len(df):,} rows"
                )
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            return pd.DataFrame()

        # Clean up columns, rename, unify climate vars, etc.
        df = standardize_dataframe(df, vi_var)

        # Optionally drop regions with zero yield records BEFORE any further
        # work (config: filter_regions_without_yields, default off). Non-fatal:
        # on any problem the frame passes through unfiltered.
        try:
            country_key = (
                str(df["adm0_name"].iloc[0]).lower().replace(" ", "_")
                if "adm0_name" in df.columns and not df.empty
                else self.country
            )
            crop_for_filter = self.crop or utils.get_crop_season(self.file_name)[0]
            df = filter_frame_to_yield_regions(
                df, self.parser, self.admin_zone, country_key, crop_for_filter
            )
        except Exception as e:
            logger.warning(
                f"no-yield region filter skipped: {type(e).__name__}: {e}"
            )

        # For certain methods, add extra columns (fraction_season, dekad, etc.)
        if self.method in [
            "fraction_season",
            "dekad", "dekad_r",
            "biweekly", "biweekly_r",
            "monthly", "monthly_r"
        ]:
            df = self.add_season_information(df)

        # ENSO teleconnection scalars: one value per calendar year, broadcast
        # to every row of that year (all regions, all DOYs). Network fetch is
        # cached under self.dir_base / "enso" with 7-day TTL, so the same
        # request across (file, harvest_year, region) tasks in one run hits
        # local disk. Fetch failure (no network on cluster) is non-fatal:
        # ENSO columns simply won't appear and compute_eo_indices will skip
        # the ENSO branch.
        try:
            from . import enso
            enso_years = df["Season"].dropna().astype(int).unique() \
                if "Season" in df.columns else df["year"].dropna().astype(int).unique()
            enso_frame = enso.get_enso_frame(
                dir_cache=self.dir_base / "enso",
                years=sorted(int(y) for y in enso_years),
            )
            # Join on calendar year, not Season, so pre-season rows get the
            # correct prev-year values (harvest year Y always uses Y-1 for
            # ONI_prev_* regardless of which DOY row we're on).
            key_col = "Season" if "Season" in df.columns else "year"
            df = df.merge(
                enso_frame.reset_index().rename(columns={"year": key_col}),
                on=key_col, how="left",
            )
        except Exception as e:
            logger.warning(f"ENSO ingestion skipped: {type(e).__name__}: {e}")

        # CCI (USDA NASS crop-condition index): monthly-mean per (state, year),
        # broadcast onto rows by (adm1_name, year, Month). The source CSV
        # covers maize, soybean, rice, winter_wheat, spring_wheat, sorghum,
        # cotton (see geoprepare.datasets.CROP_CONDITION) -- NASS reports no
        # CONDITION series for other geocif crops, which get an empty frame
        # and this merge becomes a no-op (no 'cci' column, so
        # compute_eo_indices skips the CCI branch).
        # Config: [DEFAULT] cci_file = path to the cleaned condition CSV.
        try:
            from . import cci as _cci
            cci_path = self.parser.get("DEFAULT", "cci_file", fallback="").strip()
            if cci_path and "adm1_name" in df.columns and "Month" in df.columns:
                key_col = "Season" if "Season" in df.columns else "year"
                yrs = sorted(int(y) for y in df[key_col].dropna().astype(int).unique())
                # self.crop is often still "" here: preprocess_input_df runs via
                # the per-file cache (process_task) and discover_regions BEFORE
                # obj.crop is assigned, so passing self.crop directly filters the
                # CCI frame on crop=="" -> empty -> no 'cci' column, silently.
                # Derive the crop from the file name instead.
                crop_for_cci = self.crop or utils.get_crop_season(self.file_name)[0]
                cci_frame = _cci.get_cci_frame(cci_path, crop_for_cci, years=yrs)
                if cci_frame is not None and not cci_frame.empty:
                    # CCI is reported at the state (admin_1) level. For an
                    # admin_1 run, adm1_name IS the state -> join directly. For
                    # an admin_2 run, adm1_name is the county, so map each
                    # county's region_id (= boundary ADM_ID) to its parent state
                    # and broadcast that state's CCI onto every county of it.
                    cci_frame = cci_frame.rename(columns={"year": key_col})
                    if self.admin_zone == "admin_2" and "region_id" in df.columns:
                        country = (
                            str(df["adm0_name"].iloc[0]).lower().replace(" ", "_")
                            if "adm0_name" in df.columns and not df.empty
                            else self.country
                        )
                        shp = self.parser.get(
                            country, "boundary_file", fallback=""
                        ).strip()
                        state_map = (
                            _cci.get_region_state_map(
                                self.parser, country,
                                Path(self.parser.get("PATHS", "dir_boundary_files")) / shp,
                            )
                            if shp else {}
                        )
                        if state_map:
                            df["_cci_state"] = (
                                df["region_id"].map(_cci._norm_id).map(state_map)
                            )
                            df = df.merge(
                                cci_frame.rename(columns={"region": "_cci_state"}),
                                on=["_cci_state", key_col, "Month"], how="left",
                            ).drop(columns=["_cci_state"])
                        else:
                            logger.warning(
                                f"CCI: admin_2 run but no county->state map "
                                f"(country={country!r}); skipping CCI merge."
                            )
                    else:
                        df = df.merge(
                            cci_frame.rename(columns={"region": "adm1_name"}),
                            on=["adm1_name", key_col, "Month"], how="left",
                        )
        except Exception as e:
            logger.warning(f"CCI ingestion skipped: {type(e).__name__}: {e}")

        return df

    def filter_data_for_harvest_year(self) -> pd.DataFrame:
        """
        Keep only rows matching self.harvest_year in 'Season', ignoring future dates.

        Returns:
            pd.DataFrame: Subset for the harvest year.
        """
        mask = self.df_country_crop["Season"] == self.harvest_year
        df_filtered = self.df_country_crop[mask]

        # If you want to filter out future times:
        df_filtered = df_filtered[df_filtered["time"] <= pd.to_datetime("today")]

        # Exclude pre-season synthetic rows (monthly, crop_cal=0) from
        # in-season extraction — they cause icclim frequency mismatches.
        # Pre-season extraction reads from df_country_crop directly.
        if "crop_cal" in df_filtered.columns:
            df_filtered = df_filtered[df_filtered["crop_cal"] != 0]

        return df_filtered

    def prepare_directories(self) -> None:
        """
        Build the output and intermediate directories based on self.country/crop and other config.
        """
        self.dir_output = utils.create_output_directory(
            self.method, self.admin_zone, self.country, self.crop, self.dir_base
        )
        self.dir_intermediate = (
            self.dir_base
            / "cid"
            / "input"
            / self.method
            / self.admin_zone
            / self.country
        )

        os.makedirs(self.dir_output, exist_ok=True)
        os.makedirs(self.dir_intermediate, exist_ok=True)

    def manage_existing_files(self) -> Path | None:
        """
        Check if final CID file already exists. If we do not need to redo,
        skip processing for older years.

        Returns:
            Path or None: Path to the intermediate file if we continue, else None.
        """
        intermediate_file = (
            self.dir_intermediate
            / f"{self.country}_{self.crop}_s{self.season}_{self.harvest_year}.csv"
        )
        cid_file = (
            self.dir_output
            / f"{self.country}_{self.crop}_s{self.season}_{self.harvest_year}.csv"
        )
        current_year = pd.Timestamp.now().year

        if not self.redo:
            # If harvest_year is older than last year and file exists, skip
            if (self.harvest_year < (current_year - 1)) and cid_file.is_file():
                logger.info(f"CID file exists, skipping: {cid_file}")
                return None

        return intermediate_file

    def process_data_by_region_and_stage(self) -> int:
        """
        Group the big DataFrame by (adm0_name, adm1_name) and compute indices
        for each subset, across each stage or method partition.  Results are
        appended to the output CSV after each region completes.

        Returns:
            int: Number of regions that produced results.
        """
        regions_written = 0
        # observed=True: keys are categorical (_read_input_csv) — without it,
        # list() enumerates one empty group per unused region level.
        groups = list(
            self.df_country_crop.groupby(["adm0_name", "adm1_name"], observed=True)
        )

        pbar = tqdm(groups, desc=f"Year {self.harvest_year}", unit="rgn",
                    leave=False, disable=not self.show_progress, mininterval=5)
        for key, df_group in pbar:
            pbar.set_description(f"Year {self.harvest_year} | {key[1]}")
            try:
                df_result = self.process_group(df_group, key)
                if not df_result.empty:
                    self._append_csv(df_result)
                    regions_written += 1
            except Exception as e:
                logger.error(f"Error in process_group for {key}: {e}")

        return regions_written

    def process_data_pre_season(self, init_month: int) -> int:
        """Extract FLDAS/S2S features for pre-season mode (no stage windows).

        For each region, reads the single row whose ``Month == init_month``
        and extracts every FLDAS and S2S lead column value as an individual
        CID row with ``Stage = "PS"``.

        Args:
            init_month: Calendar month (1-12) to use as the forecast
                initialization month.

        Returns:
            Number of regions that produced results.
        """
        regions_written = 0
        # observed=True: categorical keys — see process_data.
        groups = list(
            self.df_country_crop.groupby(["adm0_name", "adm1_name"], observed=True)
        )

        pbar = tqdm(groups, desc=f"Pre-season {self.harvest_year}", unit="rgn",
                    leave=False, disable=not self.show_progress, mininterval=5)
        for key, df_group in pbar:
            pbar.set_description(f"Pre-season {self.harvest_year} | {key[1]}")
            try:
                df_result = self._extract_pre_season_features(key, init_month)
                if not df_result.empty:
                    self._append_csv(df_result)
                    regions_written += 1
            except Exception as e:
                logger.error(f"Error in pre-season extraction for {key}: {e}")

        return regions_written

    def _extract_pre_season_features(
        self,
        key,
        init_month: int,
    ) -> pd.DataFrame:
        """Extract all FLDAS/S2S lead values from a single init-month row.

        Args:
            key: (country_name, region_name).
            init_month: Calendar month to read forecast data from.

        Returns:
            DataFrame with one row per (variable, lead) in standard CID format.
        """
        # For pre-season, read from the FULL dataset (not harvest-year
        # filtered) because pre-season months fall outside the crop calendar
        # and won't appear in df_harvest_year.
        df_region = self.df_country_crop[self.df_country_crop["adm1_name"] == key[1]]
        if df_region.empty:
            logger.debug(f"Pre-season: no data for region {key[1]}")
            return pd.DataFrame()

        if "Month" not in df_region.columns:
            logger.debug(f"Pre-season: no Month column for {key[1]}")
            return pd.DataFrame()

        # Determine the correct calendar year for this init month.
        # Walk the pre-season month list chronologically, starting at
        # harvest_year-1 and incrementing when crossing Dec→Jan.
        # This handles both same-year (Togo: Sep-Feb → Mar) and
        # cross-year (Malawi: Apr-Sep → Oct) seasons correctly.
        import arrow as ar
        pre_months = self._get_pre_season_months(ar.utcnow().month)
        year = self.harvest_year - 1
        prev_m = pre_months[0] if pre_months else init_month
        month_to_year = {}
        for m in pre_months:
            if m < prev_m:  # crossed Dec→Jan boundary
                year += 1
            month_to_year[m] = year
            prev_m = m
        target_year = month_to_year.get(init_month, self.harvest_year)

        df_init = df_region[
            (df_region["Month"] == init_month) &
            (df_region["time"].dt.year == target_year)
        ]
        if df_init.empty:
            # Fallback: try without year filter
            df_init = df_region[df_region["Month"] == init_month]
        if df_init.empty:
            logger.debug(
                f"Pre-season: no data for month {init_month} "
                f"(year {target_year}) in {key[1]}, harvest_year {self.harvest_year}"
            )
            return pd.DataFrame()

        # Read previous init month's row for revision features
        prev_init = (init_month - 2) % 12 + 1  # month before init_month
        prev_year = month_to_year.get(prev_init, target_year)
        df_prev = df_region[
            (df_region["Month"] == prev_init) &
            (df_region["time"].dt.year == prev_year)
        ]
        if not df_prev.empty:
            if "time" in df_prev.columns:
                prev_row = df_prev.loc[df_prev["time"].idxmax()]
            else:
                prev_row = df_prev.iloc[0]
        else:
            prev_row = None

        # Use latest row by time if multiple rows exist for the month
        if "time" in df_init.columns:
            latest_idx = df_init["time"].idxmax()
        else:
            latest_idx = df_init.index[0]
        row = df_init.loc[latest_idx]

        area = df_region["Area"].unique()[0] if "Area" in df_region.columns else 0

        # Debug: log first FLDAS column value for this row
        _first_fldas = di.fldas_col_map.get("MEAN_FLDAS_SoilMoist_tavg_LEAD0")
        _has_col = _first_fldas in row.index if _first_fldas else False
        _val = row[_first_fldas] if _has_col else "MISSING_COL"
        logger.debug(
            f"Pre-season extract: region={key[1]}, month={init_month}, "
            f"year={target_year}, fldas_col={_first_fldas}, "
            f"in_index={_has_col}, value={_val}, "
            f"row_time={row.get('time','?')}, row_crop_cal={row.get('crop_cal','?')}"
        )

        rows = []
        # Forecast lead features — one loop per registered (dict, col_map)
        # family: FLDAS, S2S, CHIRPS-MFC. Adding a family = registering it in
        # definitions.py; nothing here changes.
        _forecast_families = [
            (di.dict_fldas, di.fldas_col_map),
            (di.dict_s2s, di.s2s_col_map),
            (di.dict_chirps_mfc, di.chirps_mfc_col_map),
        ]
        for _fam_dict, _fam_map in _forecast_families:
            for iname, (itype, idesc) in _fam_dict.items():
                col_name = _fam_map.get(iname)
                if col_name and col_name in row.index:
                    val = float(row[col_name])
                    rows.append({
                        "Description": idesc,
                        "CID": val,
                        "Country": key[0].replace("_", " ").title(),
                        "Region": key[1].replace("_", " ").title(),
                        "Area": area,
                        "Crop": self.crop.replace("_", " ").title(),
                        "Season": self.season,
                        "Method": self.method,
                        "Stage": f"PS_{init_month}",
                        "Harvest Year": self.harvest_year,
                        "Index": iname,
                        "Type": itype,
                    })

        # --- Engineered aggregate features (guarded by config flag) ---
        if not self.compute_forecast_aggregates:
            return pd.DataFrame(rows)
        def _make_row(index_name, val, itype):
            # Sanitize: replace inf with NaN
            if not np.isfinite(val):
                val = np.nan
            desc = (di.dict_fldas_engineered.get(index_name,
                    di.dict_s2s_engineered.get(index_name, ["", ""]))[1])
            return {
                "Description": desc,
                "CID": val,
                "Country": key[0].replace("_", " ").title(),
                "Region": key[1].replace("_", " ").title(),
                "Area": area,
                "Crop": self.crop.replace("_", " ").title(),
                "Season": self.season,
                "Method": self.method,
                "Stage": f"PS_{init_month}",
                "Harvest Year": self.harvest_year,
                "Index": index_name,
                "Type": itype,
            }

        # 1. Sum precipitation across leads
        fldas_precip = [row.get(f"fldas_totalprecip_tavg_lead{i}", np.nan) for i in range(6)]
        if not all(np.isnan(v) for v in fldas_precip if isinstance(v, float)):
            rows.append(_make_row("SUM_FLDAS_TotalPrecip", float(np.nansum(fldas_precip)), "FLDAS"))

        s2s_precip = [row.get(f"s2s_tprate_lead{i}", np.nan) for i in range(1, 7)]
        if not all(np.isnan(v) for v in s2s_precip if isinstance(v, float)):
            rows.append(_make_row("SUM_S2S_tprate", float(np.nansum(s2s_precip)), "S2S"))

        # 2. Average non-precipitation variables across leads
        for var, idx_name, itype in [
            ("soilmoist_tavg", "AVG_FLDAS_SoilMoist", "FLDAS"),
            ("tair_tavg", "AVG_FLDAS_Tair", "FLDAS"),
            ("evap_tavg", "AVG_FLDAS_Evap", "FLDAS"),
            ("tws_tavg", "AVG_FLDAS_TWS", "FLDAS"),
        ]:
            vals = [row.get(f"fldas_{var}_lead{i}", np.nan) for i in range(6)]
            if not all(np.isnan(v) for v in vals if isinstance(v, float)):
                rows.append(_make_row(idx_name, float(np.nanmean(vals)), itype))

        s2s_t2m = [row.get(f"s2s_t2m_lead{i}", np.nan) for i in range(1, 7)]
        if not all(np.isnan(v) for v in s2s_t2m if isinstance(v, float)):
            rows.append(_make_row("AVG_S2S_t2m", float(np.nanmean(s2s_t2m)), "S2S"))

        # 3a. Within-year forecast revision (needs prev_row)
        if prev_row is not None:
            for var, idx_name, itype, leads, prefix in [
                ("SoilMoist_tavg", "REV_FLDAS_SoilMoist_tavg", "FLDAS", range(6), "fldas"),
                ("TotalPrecip_tavg", "REV_FLDAS_TotalPrecip_tavg", "FLDAS", range(6), "fldas"),
                ("Tair_tavg", "REV_FLDAS_Tair_tavg", "FLDAS", range(6), "fldas"),
                ("Evap_tavg", "REV_FLDAS_Evap_tavg", "FLDAS", range(6), "fldas"),
                ("TWS_tavg", "REV_FLDAS_TWS_tavg", "FLDAS", range(6), "fldas"),
                ("t2m", "REV_S2S_t2m", "S2S", range(1, 7), "s2s"),
                ("tprate", "REV_S2S_tprate", "S2S", range(1, 7), "s2s"),
            ]:
                # Compare overlapping target months between current and previous init
                diffs = []
                for lead in leads:
                    col = f"{prefix}_{var.lower()}_lead{lead}"
                    curr_val = row.get(col, np.nan)
                    # Previous init month's lead+1 targets the same month
                    prev_lead = lead + 1
                    prev_col = f"{prefix}_{var.lower()}_lead{prev_lead}"
                    prev_val = prev_row.get(prev_col, np.nan)
                    try:
                        if not (np.isnan(curr_val) or np.isnan(prev_val)):
                            diffs.append(abs(float(curr_val) - float(prev_val)))
                    except (TypeError, ValueError):
                        pass
                if diffs:
                    rows.append(_make_row(idx_name, float(np.mean(diffs)), itype))

        # 3b. MAR — Multi-year Mean Absolute Revision (static per-region)
        # Computed from ALL years in df_region for this region.
        # For each variable, compute average |consecutive-month revision|
        # across all available years.
        for var, idx_name, itype, leads, prefix in [
            ("SoilMoist_tavg", "MAR_FLDAS_SoilMoist_tavg", "FLDAS", range(6), "fldas"),
            ("TotalPrecip_tavg", "MAR_FLDAS_TotalPrecip_tavg", "FLDAS", range(6), "fldas"),
            ("Tair_tavg", "MAR_FLDAS_Tair_tavg", "FLDAS", range(6), "fldas"),
            ("Evap_tavg", "MAR_FLDAS_Evap_tavg", "FLDAS", range(6), "fldas"),
            ("TWS_tavg", "MAR_FLDAS_TWS_tavg", "FLDAS", range(6), "fldas"),
            ("t2m", "MAR_S2S_t2m", "S2S", range(1, 7), "s2s"),
            ("tprate", "MAR_S2S_tprate", "S2S", range(1, 7), "s2s"),
        ]:
            all_diffs = []
            # Group by year and compute revision across consecutive months
            for yr in df_region["time"].dt.year.unique():
                df_yr = df_region[df_region["time"].dt.year == yr]
                months_in_yr = sorted(df_yr["Month"].unique())
                for m_idx in range(1, len(months_in_yr)):
                    m_curr = months_in_yr[m_idx]
                    m_prev = months_in_yr[m_idx - 1]
                    r_curr = df_yr[df_yr["Month"] == m_curr]
                    r_prev = df_yr[df_yr["Month"] == m_prev]
                    if r_curr.empty or r_prev.empty:
                        continue
                    rc = r_curr.iloc[0]
                    rp = r_prev.iloc[0]
                    for lead in leads:
                        col = f"{prefix}_{var.lower()}_lead{lead}"
                        try:
                            cv = float(rc.get(col, np.nan))
                            pv_col = f"{prefix}_{var.lower()}_lead{lead + 1}"
                            pv = float(rp.get(pv_col, np.nan))
                            if not (np.isnan(cv) or np.isnan(pv)):
                                all_diffs.append(abs(cv - pv))
                        except (TypeError, ValueError):
                            pass
            if all_diffs:
                rows.append(_make_row(idx_name, float(np.mean(all_diffs)), itype))

        return pd.DataFrame(rows)

    def _get_planting_month(self) -> int:
        """Return the planting month: the mode of the months where ``crop_cal``
        transitions from off-season (0 or 4) into planting (1).

        Mode rather than ``min(Month)`` because for cross-year seasons
        (e.g. Malawi maize: Nov → April) the in-season window wraps months
        ``{11, 12, 1, 2, 3, 4}`` and ``.min()`` would return 1.  Mode rather
        than "first transition" because the pre-season padding rows at the
        very start of the merged CSV produce a spurious ``cc=0 → cc=1``
        transition at January 1 of the first data year (the planting-phase
        label is sticky from Nov of the prior year, but the padding rows
        before it carry ``cc=0``).  The real Nov transition repeats every
        region every year and overwhelms the one-off artifact.
        """
        if "crop_cal" not in self.df_country_crop.columns:
            return 1
        df = self.df_country_crop
        sort_cols = [c for c in ("time", "year", "doy") if c in df.columns]
        if sort_cols:
            df = df.sort_values(sort_cols)
        # Per-region shift so prev_cc doesn't bleed across region boundaries
        if "adm1_name" in df.columns:
            prev_cc = df.groupby("adm1_name")["crop_cal"].shift(1)
        elif "region" in df.columns:
            prev_cc = df.groupby("region")["crop_cal"].shift(1)
        else:
            prev_cc = df["crop_cal"].shift(1)
        transitions = df[(df["crop_cal"] == 1) & prev_cc.isin([0, 4])]
        if not transitions.empty and "Month" in transitions.columns:
            return int(transitions["Month"].mode().iloc[0])
        # Fallback: pathological data with no off-season → planting transition
        if "Month" in df.columns:
            in_season = df[df["crop_cal"].isin([1, 2, 3])]
            if not in_season.empty:
                return int(in_season["Month"].min())
        return 1

    def _get_pre_season_months(self, current_month: int) -> list[int]:
        """Pre-season init months for the CID stage.

        Thin wrapper around :func:`geocif.utils.get_pre_season_init_months` —
        single source of truth shared with the ML stage to avoid drift.
        """
        import ast
        from geocif.utils import get_pre_season_init_months, is_forecast_only

        try:
            use_cids = ast.literal_eval(
                self.parser.get("DEFAULT", "use_cids", fallback="['all']")
            )
        except (ValueError, SyntaxError):
            use_cids = ["all"]
        forecast_only = is_forecast_only(use_cids)
        return get_pre_season_init_months(
            self._get_planting_month(),
            extend_to_month=current_month if forecast_only else None,
        )

    def _canonical_season_months(self, key: tuple[str, str]) -> set:
        """
        Return the set of calendar months that comprise the full crop season
        for ``key = (adm0, adm1)``, drawn from the most recent **completed**
        historical harvest year.

        This is used to widen the FLDAS in-season mask so that forecast leads
        (LEAD1..LEAD5) targeting future months still pass the mask when the
        current harvest-year slice has been truncated to today by
        ``filter_data_for_harvest_year``.

        Returns an empty set if no completed historical data exists; caller
        should fall back to ``set(df_harvest_year_region["Month"].unique())``.
        """
        region_hist = self.df_country_crop[
            (self.df_country_crop["adm1_name"] == key[1]) &
            (self.df_country_crop["Season"] < self.harvest_year)
        ]
        if region_hist.empty:
            return set()
        last_complete = int(region_hist["Season"].max())
        ref_slice = region_hist[region_hist["Season"] == last_complete]
        return set(int(m) for m in ref_slice["Month"].unique())

    def determine_stages_and_column(self, df: pd.DataFrame):
        """
        Figure out which column we’re grouping by (crop_cal, fraction_season, etc.)
        and which stage values are valid.

        Args:
            df (pd.DataFrame): Harvest-year subset.

        Returns:
            tuple[list, list|None, str]: stages, valid_stages, column_name
        """
        col = METHOD_TO_COLUMN.get(self.method)
        if not col:
            raise ValueError(f"Unknown method: {self.method}")

        stages = df[col].unique()
        valid_stages = None

        if self.method == "phenological_stages":
            valid_stages = [1, 2, 3]
        elif self.method.startswith("biweekly"):
            valid_stages = range(1, 27)
        elif self.method.startswith("dekad"):
            valid_stages = range(1, 38)
        elif self.method.startswith("monthly"):
            valid_stages = range(1, 13)
        elif self.method == "fraction_season":
            valid_stages = range(10, 110, 10)
        elif self.method == "full_season":
            pass  # no stage-based filtering needed

        return stages, valid_stages, col

    def filter_data_for_stage(
        self, df_all_years: pd.DataFrame, df_harvest_year_region: pd.DataFrame,
        col: str, stages: list
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Given a subset of data (all years, harvest year region only),
        return the sub-data for whichever "stages" or intervals we want.

        Args:
            df_all_years (pd.DataFrame): The complete multi-year dataset.
            df_harvest_year_region (pd.DataFrame): Subset for the harvest year & region.
            col (str): The column to filter by (crop_cal, fraction_season, etc.).
            stages (list): The list of stage values to keep.

        Returns:
            (pd.DataFrame, pd.DataFrame): (df_time_period, df_base_period)
        """
        if self.method == "full_season":
            # No sub-selection for full_season
            return df_harvest_year_region, df_all_years

        mask_harvest = df_harvest_year_region[col].isin(stages)
        df_time_period = df_harvest_year_region[mask_harvest]

        mask_all = df_all_years[col].isin(stages)
        df_base_period = df_all_years[mask_all]

        return df_time_period, df_base_period

    def process_group(
        self,
        df_group: pd.DataFrame,
        key: tuple[str, str]
    ) -> pd.DataFrame:
        """
        Compute CIDs for a single (adm0_name, adm1_name) subset, iterating
        across each stage or stage combination (depending on method).

        Args:
            df_group (pd.DataFrame): The multi-year subset for this region.
            key (tuple[str, str]): (country_name, region_name)

        Returns:
            pd.DataFrame: The computed CIDs for this region across all stages.
        """
        frames_group = []

        # Harvest-year data for this region only
        df_harvest_year_region = self.df_harvest_year[self.df_harvest_year["adm1_name"] == key[1]]
        stages, valid_stages, col = self.determine_stages_and_column(df_harvest_year_region)

        # Build stage combinations
        extended_stages_list = []
        if self.stage_mode == "individual":
            # Full season + each individual stage
            extended_stages_list.append(list(stages))
            for s in stages:
                extended_stages_list.append([s])
        elif self.method in ["phenological_stages", "fraction_season", "full_season"]:
            extended_stages_list.append(stages)
        elif self.method in ["dekad_r", "biweekly_r", "monthly_r"]:
            # reversed stage combos
            stages = stages[::-1]
            for start_index in range(len(stages)):
                for end_index in range(start_index + 1, len(stages) + 1):
                    extended_stages_list.append(stages[start_index:end_index])
        else:
            # forward combos
            for end_index in range(1, len(stages) + 1):
                extended_stages_list.append(stages[:end_index])

        # Dedup set scoped to this (region, harvest_year) group: tracks
        # (fldas_col, lead, init_month) tuples already emitted so the FLDAS
        # branch in compute_eo_indices can skip bit-identical duplicates that
        # arise when the cumulative stage window grows without advancing
        # max(time) — common for ``monthly_r``/``dekad_r``/``biweekly_r``.
        emitted_fldas_inits: set = set()

        # For each stage combination, compute climate indices and EO stats
        stage_iter = tqdm(extended_stages_list, desc=f"Stages [{key[1]}]", unit="stg",
                          leave=False, disable=not self.show_progress, mininterval=5)
        for extended_stage in stage_iter:
            stage_iter.set_description(f"Stage {extended_stage} [{key[1]}]")
            # df_time_period is the harvest-year slice (for EO aggregates and
            # for the SPI per-year code path). df_base_period is the full
            # multi-year baseline shared across all years for this file via
            # self.icclim_cache — no separate df_time_multi alias needed.
            df_time_period, df_base_period = self.filter_data_for_stage(
                df_group, df_harvest_year_region, col, extended_stage
            )

            # 1) ICCLIM-based indices
            icclim_verbosity = "SILENT" if self.suppress_icclim_logs else "LOW"
            idx_iter = tqdm(di.dict_indices.items(), desc=f"CID [{key[1]}]", unit="idx",
                            leave=False, disable=not self.show_progress, mininterval=5)
            for index_name, (index_type, index_details) in idx_iter:
                idx_iter.set_description(f"{index_name} [{key[1]}]")

                # Pre-check window-needing indices and log with full
                # file/year/region/stage context if the slice is too short.
                min_days = _INDEX_MIN_DAYS.get(index_name)
                if min_days is not None:
                    n_days = df_time_period["time"].dt.normalize().nunique()
                    if n_days < min_days:
                        logger.warning(
                            f"Skipping {index_name} for "
                            f"{self.file_name} | {self.harvest_year} | "
                            f"{key[1]} | stage={extended_stage}: "
                            f"slice has {n_days} day(s), needs >= {min_days}"
                        )
                        continue

                # Rolling-window indices (SPI3/SPI6) need continuous multi-year
                # monthly precip to compute the 3/6-month standardized deficit.
                # The stage-restricted df_base_period has 8-month gaps between
                # years that icclim rejects with "overlapping depth 5 is larger
                # than your array 4". Feed the full multi-year df_group instead;
                # time_range in compute_indices still bounds SPI output to the
                # target harvest year window.
                base_period_for_index = (
                    df_group
                    if index_name in _ICCLIM_BYPASS_CACHE
                    else df_base_period
                )

                try:
                    ds = compute_indices(
                        df_time_period, base_period_for_index, index_name,
                        logs_verbosity=icclim_verbosity,
                    )
                except Exception as e:
                    logger.error(
                        f"Error computing {index_name} for {key}: {e}"
                    )
                    continue

                if ds is None:
                    continue

                # ds is dask-backed — actual computation happens here.  The
                # explicit minimum-window pre-check above covers known
                # windowed indices; this catches any other one that raises
                # ``ValueError: Moving window`` at compute time, so a single
                # bad index doesn't kill the whole region/year task.
                try:
                    df_out = ds.to_dataframe().reset_index()
                except ValueError as e:
                    if "Moving window" in str(e):
                        logger.warning(
                            f"Skipping {index_name} for "
                            f"{self.file_name} | {self.harvest_year} | "
                            f"{key[1]} | stage={extended_stage}: {e}"
                        )
                        continue
                    raise
                df_processed = self.process_row(
                    df_out,
                    df_harvest_year_region,
                    extended_stage,
                    key,
                    index_name,
                    index_type,
                    index_details,
                )
                if not df_processed.empty:
                    frames_group.append(df_processed)
            # 2) EO indices (NDVI, ESI, GCVI, H-INDEX, etc.)
            # H-INDEX trimmed 2026-07-09 to Precip only: the Tmax/Tmin/Tmean
            # variants collapse to TXx/TNx/TG (bit-identical values seen in
            # Brazil DF 2016 diagnostic), and the NDVI/ESI/GCVI variants have
            # scale-dependent semantics (values in the 4-6 or 300+ range that
            # depend on input scaling, not the intended h-index definition).
            # H-INDEX_Precip is kept because it's semantically distinct (N days
            # with rain >= N mm) and was the top-selected H-INDEX at 540 gOMP
            # picks. See dict_hindex in definitions.py for the trim.
            eo_vars = ["GCVI", "NDVI", "ESI4WK", "ETREF", "H-INDEX", "AEF"]
            if any(c.startswith("fldas_") for c in df_group.columns):
                eo_vars.append("FLDAS")
            if any(c.startswith("s2s_") for c in df_group.columns):
                eo_vars.append("S2S")
            if any(c.startswith(("ONI_", "MEI_")) for c in df_group.columns):
                eo_vars.append("ENSO")
            if "cci" in df_group.columns:
                eo_vars.append("CCI")
            if "cci_ge" in df_group.columns:
                eo_vars.append("CCIGE")
            # NOTE: static per-region variables (aridity, soil_*) are NOT
            # emitted as staged CID rows — they carry no time dimension, so
            # per-stage rows would only duplicate one constant. They reach
            # the ML frame via geocif._add_static_eo_features (post-pivot
            # Region join from the crop_t0 CSV) as bare stage-less columns.
            for eo_var in eo_vars:
                df_eo = self.compute_eo_indices(
                    df_time_period,
                    df_harvest_year_region,
                    eo_var,
                    key,
                    extended_stage,
                    emitted_fldas_inits=emitted_fldas_inits,
                )
                if not df_eo.empty:
                    frames_group.append(df_eo)

        if frames_group:
            return pd.concat(frames_group, ignore_index=True)
        return pd.DataFrame()

    def process_row(
        self,
        df: pd.DataFrame,
        df_harvest_year_region: pd.DataFrame,
        stage: list,
        key: tuple[str, str],
        index_name: str,
        index_type: str,
        index_details: str
    ) -> pd.DataFrame:
        """
        Post-process the xarray->DataFrame conversion for an ICCLIM index result.

        Args:
            df (pd.DataFrame): The ICCLIM result as a DataFrame.
            df_harvest_year_region (pd.DataFrame): The subset for area calculations, etc.
            stage (list): The list of stage values used.
            key (tuple[str, str]): (country, region).
            index_name (str): The computed index name.
            index_type (str): e.g. "climate_index".
            index_details (str): A human-readable description of the index.

        Returns:
            pd.DataFrame: A single-row DataFrame (if successful).
        """
        if df.empty:
            return pd.DataFrame()

        # Typically, ICCLIM data might have multiple lat/lon/time rows
        # but if it collapses them, you might only get 1 row.
        # Some indices produce a single value after bounding.
        if "bounds" in df.columns:
            df = df[df["bounds"] == 1]

        df = df.drop(columns=[c for c in ["time", "bounds", "time_bounds"] if c in df], errors="ignore")

        if df.empty:
            return pd.DataFrame()

        # Rolling-window indices (SPI3/SPI6) emit one row per month within the
        # requested time_range. For a multi-month stage window that's multiple
        # rows — the iloc[[0]] below would silently keep only the first month
        # and drop the rest. Aggregate to a single stage-level value.
        #
        # MIN (most negative SPI = worst drought month) chosen over MEAN
        # because empirically the MEAN aggregation dilutes the drought signal:
        # in Brazil 2016 DF the strongest SPI6 values were in specific months
        # of the growing window (-2.7 in Mar) while others were milder (-1.4
        # in Jan) — the mean (~-1.5) is a weaker signal than the min (-2.7).
        # Feature-selection also biases toward features with sharp per-year
        # extremes, so MIN gives gOMP a stronger discriminator to pick up.
        # Yield_outlook SPI-mean run (0.4.829): tabpfn on all-years maize
        # 16.44 → 17.08 MAPE, cubist 16.82 → 17.65 — both regressions vs
        # pre-SPI. Switching to MIN.
        if index_name in _ICCLIM_BYPASS_CACHE and len(df) > 1 and index_name in df.columns:
            agg_val = df[index_name].min(skipna=True)
            df = df.iloc[[0]].copy()
            df[index_name] = agg_val

        # For safety, pick the first row or use mean if needed:
        df = df.iloc[[0]]  # keep as DataFrame

        # Add metadata
        df["CID"] = df[index_name]
        df.drop(columns=[index_name], inplace=True)

        df["Description"] = index_details
        df["Index"] = index_name
        df["Type"] = index_type
        df["Country"] = key[0].replace("_", " ").title()
        df["Region"] = key[1].replace("_", " ").title()
        df["Area"] = df_harvest_year_region["Area"].unique()[0]
        df["Crop"] = self.crop.replace("_", " ").title()
        df["Season"] = self.season
        df["Method"] = self.method
        df["Stage"] = "_".join(str(int(s)) for s in stage) if len(stage) else None
        df["Harvest Year"] = self.harvest_year

        return df[[
            "Description", "CID", "Country", "Region", "Area",
            "Crop", "Season", "Method", "Stage", "Harvest Year",
            "Index", "Type"
        ]]

    def compute_eo_indices(
        self,
        df_time_period: pd.DataFrame,
        df_harvest_year_region: pd.DataFrame,
        var: str,
        key: tuple[str, str],
        stage: list,
        emitted_fldas_inits: set = None,
    ) -> pd.DataFrame:
        """
        Compute "environmental observation" indices (NDVI, GCVI, ESI, H-INDEX, etc.).

        Args:
            df_time_period (pd.DataFrame): Subset for time period.
            df_harvest_year_region (pd.DataFrame): Harvest-year data for region (for area, etc.).
            var (str): Which EO variable to compute indices from.
            key (tuple[str, str]): (country, region).
            stage (list): The list of stage values used.
            emitted_fldas_inits (set): Per-(region, harvest_year) set of
                ``(var, lead, init_month)`` tuples already written for FLDAS.
                Used to dedupe duplicate cumulative-stage rows when the latest
                init-month row is unchanged (common for ``monthly_r``-style
                reverse stage chains). When None, no dedup is performed.

        Returns:
            pd.DataFrame: DataFrame with aggregated stats for that variable.
        """
        df_result = []
        # Map 'var' to the dictionary of definitions
        # e.g. NDVI -> di.dict_ndvi, GCVI -> di.dict_gcvi, etc.
        if var == "NDVI":
            dict_eo = di.dict_ndvi
        elif var == "GCVI":
            dict_eo = di.dict_gcvi
        elif var == "ESI4WK":
            dict_eo = di.dict_esi4wk
        elif var == "ETREF":
            dict_eo = di.dict_etref
        elif var == "H-INDEX":
            dict_eo = di.dict_hindex
        elif var == "AEF":
            dict_eo = di.dict_aef
        elif var == "FLDAS":
            dict_eo = di.dict_fldas
        elif var == "S2S":
            dict_eo = di.dict_s2s
        elif var == "ENSO":
            dict_eo = di.dict_enso
        elif var == "CCI":
            dict_eo = di.dict_cci
        elif var == "CCIGE":
            dict_eo = di.dict_ccige
        else:
            return pd.DataFrame()  # unknown var

        # Each dict is: "NDVI_MEAN" -> ("EO", "NDVI mean over period"), etc.
        for iname, (itype, idesc) in dict_eo.items():
            # ENSO features are static per (region, harvest year) -- the
            # scalar value is identical across every stage window. Emit
            # each ENSO CID exactly once per (region, year) so the wide-
            # format pivot produces one column per CID instead of one per
            # (CID, stage-window) tuple, all carrying the same value.
            # Reuses the FLDAS dedup set with an "__enso__" sentinel.
            if var == "ENSO" and emitted_fldas_inits is not None:
                enso_key = ("__enso__", iname)
                if enso_key in emitted_fldas_inits:
                    continue
                emitted_fldas_inits.add(enso_key)
            # Map index name to actual column in df_time_period
            if iname.startswith("AEF_"):
                col_name = iname.lower()  # AEF_1 → aef_1
            elif iname.endswith("_CCIGE"):
                col_name = "cci_ge"  # %Good+Excellent share (farmdoc metric)
            elif iname.endswith("_CCI"):
                col_name = "cci"  # MEAN_CCI/MAX_CCI/MIN_CCI -> merged 'cci' column
            elif iname in di.fldas_col_map:
                col_name = di.fldas_col_map[iname]
            elif iname in di.s2s_col_map:
                col_name = di.s2s_col_map[iname]
            elif iname in di.enso_col_map:
                # ENSO columns are pre-joined by year in preprocess_input_df.
                # Name matches raw column exactly (ONI_prev_JJA etc.).
                col_name = di.enso_col_map[iname]
            elif "NDVI" in iname.upper():
                col_name = "ndvi"
            elif "ESI4WK" in iname.upper():
                col_name = "esi_4wk"
            elif "ETREF" in iname.upper():
                col_name = "etref"
            elif "GCVI" in iname.upper():
                col_name = "gcvi"
            elif "TMAX" in iname.upper():
                col_name = "tasmax"
            elif "TMIN" in iname.upper():
                col_name = "tasmin"
            elif "TMEAN" in iname.upper():
                col_name = "tg"
            elif "PRECIP" in iname.upper():
                col_name = "pr"
            else:
                logger.warning(f"Unrecognized EO index name: {iname}")
                continue

            if col_name not in df_time_period.columns:
                continue

            eo_vals = df_time_period[col_name].values

            # FLDAS: restrict to the single most-recent init-month row in
            # the cumulative stage window, then drop the value entirely if
            # its forecast target month falls outside the crop season.
            #
            # Per FF2 STM §6.1.1, each FLDAS file is the forecast issued at
            # that month's initialization: lead-N targets month init+N. The
            # user-facing semantic is "use the latest FLDAS file", i.e. for
            # stage window [Apr..Jul] the row we care about is Jul's file
            # and its six lead columns describe Jul..Dec target months.
            #
            # Previously this branch computed a MEAN over every init-month
            # row in the window, which mixed multiple forecast targets into
            # a single feature and introduced a train/inference sample-count
            # asymmetry on the current year (df_harvest_year_region is
            # capped at time <= today by filter_data_for_harvest_year, so
            # the inference mean averaged fewer months than the training
            # mean). Restricting to the latest init row removes both
            # problems: a single value per (stage, lead), with a deterministic
            # target month independent of how much of the season has elapsed.
            if var in ("FLDAS", "S2S"):
                # Pick the init-source frame. Normal path: the in-season
                # slice for this region. Still-pre-season fallback: when
                # df_time_period is empty because this region's planting
                # hasn't reached the current stage's calendar window yet
                # (e.g. Gauteng with Nov planting at the country's Oct
                # stage), but the region DOES have in-season data later
                # in the harvest year, source the latest init-month row
                # from the broader harvest-year slice bounded by the
                # country-level latest time at this stage. This injects
                # forecast features so the ML model still produces a
                # prediction for late-planting regions at early stages.
                df_init_src = df_time_period
                if df_init_src.empty:
                    if "crop_cal" not in df_harvest_year_region.columns or \
                            not (df_harvest_year_region["crop_cal"] == 1).any():
                        # No in-season data anywhere this year — skip.
                        continue
                    stage_col = METHOD_TO_COLUMN.get(self.method)
                    country_stage = self.df_harvest_year[
                        self.df_harvest_year[stage_col].isin(stage)
                    ] if stage_col else pd.DataFrame()
                    if country_stage.empty:
                        continue
                    # Bound by time when available so cross-year-wrap
                    # seasons (Nov-Jul etc.) don't pull future inits.
                    if "time" in country_stage.columns and \
                            "time" in df_harvest_year_region.columns:
                        cap_time = country_stage["time"].max()
                        df_init_src = df_harvest_year_region[
                            df_harvest_year_region["time"] <= cap_time
                        ]
                    elif "Month" in country_stage.columns and \
                            "Month" in df_harvest_year_region.columns:
                        cap_month = int(country_stage["Month"].max())
                        df_init_src = df_harvest_year_region[
                            df_harvest_year_region["Month"] <= cap_month
                        ]
                    else:
                        continue
                    if df_init_src.empty:
                        continue
                if "Month" not in df_init_src.columns:
                    continue
                # Latest init-month row by absolute time (handles year-wrap
                # seasons like Nov-Jul where max(Month) is wrong).
                if "time" in df_init_src.columns:
                    latest_idx = df_init_src["time"].idxmax()
                else:
                    latest_idx = df_init_src["Month"].idxmax()
                latest_row = df_init_src.loc[latest_idx]
                init_month = int(latest_row["Month"])

                lead = int(iname.rsplit("LEAD", 1)[1])
                canonical = self._canonical_season_months(key)
                if canonical:
                    season_months = canonical
                else:
                    # Fallback: no historical data available — preserve legacy behavior
                    season_months = set(df_harvest_year_region["Month"].unique())
                target_month = ((init_month - 1 + lead) % 12) + 1
                if target_month not in season_months:
                    continue  # forecast target outside crop season

                # Dedup across cumulative stages: if an earlier (smaller) stage
                # already emitted a row with the same (var, lead, init_month),
                # this stage's extraction is bit-identical. Common for the
                # ``monthly_r``/``dekad_r``/``biweekly_r`` reverse stage chains
                # where growing the window backward in time does not advance
                # max(time). Skip writing to keep feature columns unique.
                if emitted_fldas_inits is not None:
                    init_key = (col_name, lead, init_month)
                    if init_key in emitted_fldas_inits:
                        continue
                    emitted_fldas_inits.add(init_key)

                eo_vals = np.array([latest_row[col_name]], dtype=float)

            # Derive the numeric aggregator from iname: e.g. if it ends with MIN, MAX, etc.
            aggregator = None
            # New drought depth/duration/spread family: parse the exact prefix
            # (token before the first "_") FIRST, so e.g. AUCDEF40 is not
            # swallowed by the "AUC" substring test, MAXRUN by "MAX", etc.
            _pref = iname.split("_")[0].upper()
            if _pref and _pref[0] == "P" and _pref[1:].isdigit():
                aggregator = _pref                         # P05, P10, P20, P30, P70, P90
            elif _pref.startswith("AUCDEF"):
                aggregator = _pref                         # AUCDEF40, AUCDEF50
            elif _pref.startswith("FRACLO"):
                aggregator = _pref                         # FRACLO30, FRACLO40
            elif _pref in ("CV", "IQR", "RANGE"):
                aggregator = _pref
            elif "MIN" in iname.upper():
                aggregator = "MIN"
            elif "MAX" in iname.upper():
                aggregator = "MAX"
            elif "MEAN" in iname.upper():
                aggregator = "MEAN"
            elif "STD" in iname.upper():
                aggregator = "STD"
            elif "AUC" in iname.upper():
                aggregator = "AUC"
            elif "H-INDEX" in iname.upper():
                aggregator = "H-INDEX"

            # AEF bands are static per region (no temporal variation),
            # so default to MEAN which returns the constant value.
            if aggregator is None and iname.startswith("AEF_"):
                aggregator = "MEAN"
            # ENSO scalars are constant across every row of a harvest year;
            # MEAN of the constant returns the scalar cleanly.
            if aggregator is None and (iname.startswith("ONI_") or iname.startswith("MEI_")):
                aggregator = "MEAN"

            if aggregator:
                val = aggregate_eo_values(eo_vals, aggregator)
            else:
                val = float('nan')

            row = {
                "Description": idesc,
                "CID": val,
                "Country": key[0].replace("_", " ").title(),
                "Region": key[1].replace("_", " ").title(),
                "Area": df_harvest_year_region["Area"].unique()[0],
                "Crop": self.crop.replace("_", " ").title(),
                "Season": self.season,
                "Method": self.method,
                "Stage": "_".join(str(int(s)) for s in stage) if len(stage) else None,
                "Harvest Year": self.harvest_year,
                "Index": iname,
                "Type": itype
            }
            df_result.append(row)

        return pd.DataFrame(df_result)

    def _output_path(self) -> Path:
        """Return the output CSV path for this country/crop/season/year."""
        fname = f"{self.country}_{self.crop}_s{self.season}_{self.harvest_year}.csv"
        return self.dir_output / fname

    def _append_csv(self, df: pd.DataFrame) -> None:
        """Append region results to the output CSV, writing the header only on first call."""
        out_path = self._output_path()
        write_header = not out_path.exists()
        df.to_csv(out_path, index=False, mode="a", header=write_header)


###############################################################################
#                            MAIN PROCESS FUNCTION
###############################################################################
def _run_one_year(obj: "CIDs") -> None:
    """
    Run the per-harvest-year pipeline on a ``CIDs`` instance whose
    ``df_country_crop`` and ``icclim_cache`` have already been populated by
    the caller. Extracted so ``process_file`` can amortize CSV read and ICCLIM
    result caching across many years for one file.
    """
    obj.df_harvest_year = obj.filter_data_for_harvest_year()
    if obj.df_harvest_year.empty:
        logger.warning(
            f"No data for harvest year {obj.harvest_year}. Skipping."
        )
        return

    obj.crop, obj.season = utils.get_crop_season(obj.file_name)
    obj.get_unique_country_name()
    obj.prepare_directories()

    intermediate_file = obj.manage_existing_files()
    if not intermediate_file:
        return

    obj.df_harvest_year.to_csv(intermediate_file, index=False)

    # Remove stale output so incremental appends start fresh.
    out_path = obj._output_path()
    if out_path.exists():
        out_path.unlink()

    rts = obj.parser.get("ML", "run_time_steps", fallback="latest")
    regions_written = 0

    if obj.pre_season_mode:
        import arrow as ar
        current_month = ar.utcnow().month
        init_months = obj._get_pre_season_months(current_month)
        planting = obj._get_planting_month()
        n_preseason_rows = len(obj.df_country_crop[obj.df_country_crop["crop_cal"] == 0])
        logger.info(
            f"Pre-season extraction: planting_month={planting}, "
            f"init_months={init_months}, "
            f"pre-season rows in data={n_preseason_rows}, "
            f"total rows={len(obj.df_country_crop)}"
        )
        for init_month in init_months:
            regions_written += obj.process_data_pre_season(init_month)

    # In-season CIDs: always extract unless run_time_steps is pre_season only
    if rts != "pre_season":
        regions_written += obj.process_data_by_region_and_stage()
    if regions_written:
        logger.info(f"Saved CID results to {out_path} ({regions_written} regions)")
    else:
        logger.warning(
            f"No results produced for {obj.file_name} year {obj.harvest_year}"
        )


###############################################################################
#                     FLAT (FILE, YEAR, REGION) PARALLELISM
###############################################################################
def discover_regions(parser, process_type, file_path, file_name,
                     admin_zone, method, vi_var) -> list[tuple[str, str]]:
    """Preprocess a file and return list of (adm0_name, adm1_name) tuples."""
    obj = CIDs(parser=parser, process_type=process_type, file_path=file_path,
               file_name=file_name, admin_zone=admin_zone, method=method,
               harvest_year=2001, redo=False)
    df = obj.preprocess_input_df(vi_var)
    if df.empty:
        return []
    # observed=True: categorical keys — .groups would otherwise list every
    # unused region level as a phantom (empty) region.
    return list(
        df.groupby(["adm0_name", "adm1_name"], observed=True).groups.keys()
    )


def process_task(args: ProcessTaskArgs) -> tuple:
    """
    Process a single (file, year, region) task.
    Returns (output_path_str, df_result, task_description).
    Called from Pool workers or sequentially.
    """
    # Suppress icclim logs in this worker process
    if args.parser.getboolean("DEFAULT", "suppress_icclim_logs", fallback=False):
        for _name in ("icclim", "xclim", "pint", "pint.util"):
            logging.getLogger(_name).setLevel(logging.ERROR)
        logging.getLogger().setLevel(logging.WARNING)
        logger.setLevel(logging.INFO)

    task_desc = f"{args.file_name} | {args.year} | {args.region[1]}"

    # Per-process cache: read + preprocess CSV once per file per worker
    file_key = str(args.file_path)
    if file_key not in _preprocess_cache:
        # Keep only the CURRENT file's frame. Tasks are dispatched grouped by
        # file (indices_runner builds them file -> year -> region), so a worker
        # needs one at a time — but this dict was never evicted, so after the
        # maize->soybean boundary every worker held BOTH preprocessed frames
        # for the rest of the run, doubling per-worker RSS. Clearing first also
        # frees the old frame before the new one is built, so peak stays at one.
        _preprocess_cache.clear()
        obj_tmp = CIDs(parser=args.parser, process_type=args.process_type,
                       file_path=args.file_path, file_name=args.file_name,
                       admin_zone=args.admin_zone, method=args.method,
                       harvest_year=args.year, redo=args.redo)
        try:
            _preprocess_cache[file_key] = obj_tmp.preprocess_input_df(args.vi_var)
        except Exception as e:
            logger.error(f"preprocess_input_df failed for {args.file_path}: {e}")
            return ("", pd.DataFrame(), task_desc)

    df_country_crop = _preprocess_cache[file_key]
    if df_country_crop.empty:
        return ("", pd.DataFrame(), task_desc)

    # Build CIDs instance for this year
    obj = CIDs(parser=args.parser, process_type=args.process_type,
               file_path=args.file_path, file_name=args.file_name,
               admin_zone=args.admin_zone, method=args.method,
               harvest_year=args.year, redo=args.redo)
    obj.df_country_crop = df_country_crop
    obj.show_progress = False
    obj.stage_mode = args.stage_mode

    # Year-level setup
    obj.df_harvest_year = obj.filter_data_for_harvest_year()
    if obj.df_harvest_year.empty:
        return ("", pd.DataFrame(), task_desc)

    obj.crop, obj.season = utils.get_crop_season(obj.file_name)
    obj.get_unique_country_name()
    obj.prepare_directories()

    # Get this region's data
    adm0, adm1 = args.region
    df_group = df_country_crop[
        (df_country_crop["adm0_name"] == adm0) &
        (df_country_crop["adm1_name"] == adm1)
    ]
    if df_group.empty:
        return ("", pd.DataFrame(), task_desc)

    try:
        rts = args.parser.get("ML", "run_time_steps", fallback="latest")
        frames = []

        if obj.pre_season_mode:
            import arrow as ar
            current_month = ar.utcnow().month
            for init_month in obj._get_pre_season_months(current_month):
                df_ps = obj._extract_pre_season_features(args.region, init_month)
                if not df_ps.empty:
                    frames.append(df_ps)

        # In-season CIDs: always extract unless pre_season only
        if rts != "pre_season":
            df_insn = obj.process_group(df_group, args.region)
            if not df_insn.empty:
                frames.append(df_insn)

        df_result = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    except Exception as e:
        import traceback
        logger.error(
            f"Error in process_task for {args.file_name} yr {args.year} rgn {adm1}: {e}\n"
            f"{traceback.format_exc()}"
        )
        return ("", pd.DataFrame(), task_desc)

    return (str(obj._output_path()), df_result, task_desc)


###############################################################################
#                     LEGACY FILE-LEVEL ENTRY POINTS
###############################################################################
def process_file(row) -> None:
    """
    One task = one file × all requested harvest years. Reads the CSV exactly
    once (shared across years) and processes each year independently.

    Args:
        row: A ``ProcessFileArgs`` instance, or a raw 9-tuple in the same
            field order (legacy callers).
    """
    args = row if isinstance(row, ProcessFileArgs) else ProcessFileArgs(*row)

    if args.parser.getboolean("DEFAULT", "suppress_icclim_logs", fallback=False):
        for _logger_name in ("icclim", "xclim", "pint", "pint.util"):
            logging.getLogger(_logger_name).setLevel(logging.ERROR)
        # Suppress noisy "Choice not found" INFO from root logger during icclim
        # init, but keep our own logger at INFO so geocif messages still appear.
        logging.getLogger().setLevel(logging.WARNING)
        logger.setLevel(logging.INFO)

    years = list(args.years)
    if not years:
        return

    def _build_cids(harvest_year: int) -> "CIDs":
        return CIDs(
            parser=args.parser,
            process_type=args.process_type,
            file_path=args.file_path,
            file_name=args.file_name,
            admin_zone=args.admin_zone,
            method=args.method,
            harvest_year=harvest_year,
            redo=args.redo,
        )

    # Read + standardize + add season columns exactly once for this file.
    try:
        df_country_crop = _build_cids(years[0]).preprocess_input_df(args.vi_var)
    except Exception as e:
        logger.error(f"preprocess_input_df failed for {args.file_path}: {e}")
        return
    if df_country_crop.empty:
        logger.warning(f"No data after preprocessing. Skipping {args.file_name}.")
        return

    show_progress = args.show_progress
    year_iter = (
        tqdm(years, desc=f"{args.file_name}", unit="yr", leave=False, mininterval=5)
        if show_progress else years
    )
    for year in year_iter:
        try:
            obj = _build_cids(year)
            # Inject the pre-loaded dataframe. Everything else (directories,
            # df_harvest_year, paths) is reset cleanly by ``CIDs.__init__``
            # so no per-year state leaks.
            obj.df_country_crop = df_country_crop
            obj.show_progress = show_progress
            obj.stage_mode = args.stage_mode
            _run_one_year(obj)
        except Exception as e:
            logger.error(
                f"Error in process_file for {args.file_path} year {year}: {e}"
            )


def process(row) -> None:
    """
    Back-compat entry point for callers that dispatch one task per
    ``(file, harvest_year)``. Wraps ``process_file`` with a single-element
    years list.

    Args:
        row: Raw 9-tuple ``(parser, process_type, file_path, file_name,
            admin_zone, method, harvest_year, vi_var, redo)``.
    """
    parser, process_type, file_path, file_name, admin_zone, method, harvest_year, vi_var, redo = row
    process_file(ProcessFileArgs(
        parser=parser,
        process_type=process_type,
        file_path=file_path,
        file_name=file_name,
        admin_zone=admin_zone,
        method=method,
        years=[harvest_year],
        vi_var=vi_var,
        redo=redo,
    ))


def validate_index_definitions():
    """
    Simple sanity check to ensure your dictionary keys do not have spaces.
    """
    for dict_name in [
        di.dict_indices,
        di.dict_ndvi,
        di.dict_esi4wk,
        di.dict_hindex,
        di.dict_gcvi
    ]:
        for key in dict_name.keys():
            if " " in key:
                raise ValueError(f"Space found in {dict_name} key: {key}")
