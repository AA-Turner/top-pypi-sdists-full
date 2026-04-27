import os
import logging
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

    # Convert crop_cal to float; keep only known stages
    df["crop_cal"] = df["crop_cal"].astype(float)
    df = df[df["crop_cal"].isin(di.PHENOLOGICAL_STAGES)]

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
        df["snd"] = df["snd"].fillna(0)

    # Compute daily mean temperature
    if "tasmax" in df.columns and "tasmin" in df.columns:
        df["tg"] = (df["tasmax"] + df["tasmin"]) / 2

    # Rescale NDVI if needed
    if vi_var in df.columns:
        if df[vi_var].max() > 1:
            df[vi_var] = (df[vi_var] - 50) / 200

    # HACK Exclude seasons before 2001
    df = df[df["Season"] >= 2001]

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
    # Group by region/Season so each region gets its own partition
    grps = df.groupby(["adm1_name", "Season"])
    frames = []

    for key, df_adm1_season in grps:
        if method == "fraction_season":
            step = 10
            N = len(df_adm1_season)
            # Create a fraction_season column: 10,20,...,100
            df_adm1_season["fraction_season"] = (
                                                    np.linspace(10, 100 + step, N + 1) // step * step
                                                )[:-1]

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

    # Drop Feb 29 to avoid leap year shape mismatch in percentile indices
    _leap = lambda d: (d["time"].dt.month == 2) & (d["time"].dt.day == 29)
    df_base_period = df_base_period[~_leap(df_base_period)]
    df_time_period = df_time_period[~_leap(df_time_period)]

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
    if index_name not in _ICCLIM_BYPASS_CACHE:
        kwargs["slice_mode"] = ("season", (season_start, season_end))

    try:
        ds = icclim.index(**kwargs)
    except Exception as e:
        logger.error(
            f"Error computing {index_name} for {start_tr} to {end_tr}: {e}"
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
        try:
            df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            return pd.DataFrame()

        # Clean up columns, rename, unify climate vars, etc.
        df = standardize_dataframe(df, vi_var)

        # For certain methods, add extra columns (fraction_season, dekad, etc.)
        if self.method in [
            "fraction_season",
            "dekad", "dekad_r",
            "biweekly", "biweekly_r",
            "monthly", "monthly_r"
        ]:
            df = self.add_season_information(df)

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
        groups = list(self.df_country_crop.groupby(["adm0_name", "adm1_name"]))

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
                try:
                    ds = compute_indices(
                        df_time_period, df_base_period, index_name,
                        logs_verbosity=icclim_verbosity,
                    )
                except Exception as e:
                    logger.error(
                        f"Error computing {index_name} for {key}: {e}"
                    )
                    continue

                if ds is None:
                    continue

                df_out = ds.to_dataframe().reset_index()
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
            eo_vars = ["GCVI", "NDVI", "ESI4WK", "H-INDEX", "AEF"]
            if any(c.startswith("fldas_") for c in df_group.columns):
                eo_vars.append("FLDAS")
            if any(c.startswith("s2s_") for c in df_group.columns):
                eo_vars.append("S2S")
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
        df["Stage"] = "_".join(map(str, stage)) if len(stage) else None
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
        elif var == "H-INDEX":
            dict_eo = di.dict_hindex
        elif var == "AEF":
            dict_eo = di.dict_aef
        elif var == "FLDAS":
            dict_eo = di.dict_fldas
        elif var == "S2S":
            dict_eo = di.dict_s2s
        else:
            return pd.DataFrame()  # unknown var

        # Each dict is: "NDVI_MEAN" -> ("EO", "NDVI mean over period"), etc.
        for iname, (itype, idesc) in dict_eo.items():
            # Map index name to actual column in df_time_period
            if iname.startswith("AEF_"):
                col_name = iname.lower()  # AEF_1 → aef_1
            elif iname in di.fldas_col_map:
                col_name = di.fldas_col_map[iname]
            elif iname in di.s2s_col_map:
                col_name = di.s2s_col_map[iname]
            elif "NDVI" in iname.upper():
                col_name = "ndvi"
            elif "ESI4WK" in iname.upper():
                col_name = "esi_4wk"
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
            if var in ("FLDAS", "S2S") and "Month" in df_time_period.columns:
                if df_time_period.empty:
                    continue
                # Latest init-month row by absolute time (handles year-wrap
                # seasons like Nov-Jul where max(Month) is wrong).
                if "time" in df_time_period.columns:
                    latest_idx = df_time_period["time"].idxmax()
                else:
                    latest_idx = df_time_period["Month"].idxmax()
                latest_row = df_time_period.loc[latest_idx]
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
            if "MIN" in iname.upper():
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
                "Stage": "_".join(map(str, stage)) if len(stage) else None,
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

    regions_written = obj.process_data_by_region_and_stage()
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
    return list(df.groupby(["adm0_name", "adm1_name"]).groups.keys())


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
        df_result = obj.process_group(df_group, args.region)
    except Exception as e:
        logger.error(
            f"Error in process_task for {args.file_name} yr {args.year} rgn {adm1}: {e}"
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
