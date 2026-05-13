import os
import sys
import time
import random

import sqlite3
import numpy as np
import pandas as pd
import arrow as ar
from tqdm.rich import tqdm
import matplotlib.pyplot as plt


# Proper display names for ML model identifiers
MODEL_DISPLAY_NAMES = {
    "catboost": "CatBoost",
    "tabpfn": "TabPFN",
    "tabicl": "TabICL",
    "xgboost": "XGBoost",
    "lightgbm": "LightGBM",
    "linear": "Linear",
    "lasso": "Lasso",
    "ridge": "Ridge",
    "gam": "GAM",
    "cubist": "Cubist",
    "analog": "Analog",
    "median": "Median",
    "last_year": "Last Year",
    "merf": "MERF",
    "desreg": "DesReg",
}


def display_model_name(name: str) -> str:
    """Return proper display name for a model identifier."""
    return MODEL_DISPLAY_NAMES.get(name, name)


dict_growth_stages = {
    1: "Jan 1",
    2: "Jan 11",
    3: "Jan 21",
    4: "Jan 31",
    5: "Feb 10",
    6: "Feb 20",
    7: "Mar 1",
    8: "Mar 11",
    9: "Mar 21",
    10: "Mar 31",
    11: "Apr 10",
    12: "Apr 20",
    13: "Apr 30",
    14: "May 10",
    15: "May 20",
    16: "May 30",
    17: "Jun 9",
    18: "Jun 19",
    19: "Jun 29",
    20: "Jul 9",
    21: "Jul 19",
    22: "Jul 29",
    23: "Aug 8",
    24: "Aug 18",
    25: "Aug 28",
    26: "Sep 7",
    27: "Sep 17",
    28: "Sep 27",
    29: "Oct 7",
    30: "Oct 17",
    31: "Oct 27",
    32: "Nov 6",
    33: "Nov 16",
    34: "Nov 26",
    35: "Dec 6",
    36: "Dec 16",
    37: "Dec 26",
}

dict_growth_stages_biweekly = {
    1: "Jan 1",
    2: "Jan 15",
    3: "Jan 29",
    4: "Feb 12",
    5: "Feb 26",
    6: "Mar 11",
    7: "Mar 25",
    8: "Apr 8",
    9: "Apr 22",
    10: "May 6",
    11: "May 20",
    12: "Jun 3",
    13: "Jun 17",
    14: "Jul 1",
    15: "Jul 15",
    16: "Jul 29",
    17: "Aug 12",
    18: "Aug 26",
    19: "Sep 9",
    20: "Sep 23",
    21: "Oct 7",
    22: "Oct 21",
    23: "Nov 4",
    24: "Nov 18",
    25: "Dec 2",
    26: "Dec 16",
    27: "Dec 31",
}


dict_growth_stages_monthly = {
    1: "Jan 1",
    2: "Feb 1",
    3: "Mar 1",
    4: "Apr 1",
    5: "May 1",
    6: "Jun 1",
    7: "Jul 1",
    8: "Aug 1",
    9: "Sep 1",
    10: "Oct 1",
    11: "Nov 1",
    12: "Dec 1",
}

# End-date dictionaries: last day of each period (start of next period - 1 day)
dict_growth_stages_end = {
    1: "Jan 10", 2: "Jan 20", 3: "Jan 31", 4: "Feb 9", 5: "Feb 19",
    6: "Feb 28", 7: "Mar 10", 8: "Mar 20", 9: "Mar 31", 10: "Apr 9",
    11: "Apr 19", 12: "Apr 29", 13: "May 9", 14: "May 19", 15: "May 29",
    16: "Jun 8", 17: "Jun 18", 18: "Jun 28", 19: "Jul 8", 20: "Jul 18",
    21: "Jul 28", 22: "Aug 7", 23: "Aug 17", 24: "Aug 27", 25: "Sep 6",
    26: "Sep 16", 27: "Sep 26", 28: "Oct 6", 29: "Oct 16", 30: "Oct 26",
    31: "Nov 5", 32: "Nov 15", 33: "Nov 25", 34: "Dec 5", 35: "Dec 15",
    36: "Dec 25", 37: "Dec 31",
}

dict_growth_stages_biweekly_end = {
    1: "Jan 14", 2: "Jan 28", 3: "Feb 11", 4: "Feb 25", 5: "Mar 10",
    6: "Mar 24", 7: "Apr 7", 8: "Apr 21", 9: "May 5", 10: "May 19",
    11: "Jun 2", 12: "Jun 16", 13: "Jun 30", 14: "Jul 14", 15: "Jul 28",
    16: "Aug 11", 17: "Aug 25", 18: "Sep 8", 19: "Sep 22", 20: "Oct 6",
    21: "Oct 20", 22: "Nov 3", 23: "Nov 17", 24: "Dec 1", 25: "Dec 15",
    26: "Dec 30", 27: "Dec 31",
}

dict_growth_stages_monthly_end = {
    1: "Jan 31", 2: "Feb 28", 3: "Mar 31", 4: "Apr 30", 5: "May 31",
    6: "Jun 30", 7: "Jul 31", 8: "Aug 31", 9: "Sep 30", 10: "Oct 31",
    11: "Nov 30", 12: "Dec 31",
}


def statistics_file_path(dir_out, method, country, crop):
    """Build path to the per-country statistics CSV."""
    dir_statistics = dir_out / "cid" / "indices" / method / "global"
    country_str = country.title().replace("_", " ")
    crop_str = crop.title().replace("_", " ")
    return dir_statistics / f"{country_str}_{crop_str}_statistics_{method}.csv"


def remove_last_part(s):
    # Function to remove the part after the last underscore, including the last underscore
    # e.g. 'MIN_ESI4WK_33' will return 'MIN_ESI4WK'
    # 'TNx_33' will return 'TNx'
    return "_".join(s.split("_")[:-1])


def matplotlib_setup():
    import matplotlib.pyplot as plt

    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = "Helvetica"

    # Set styles for axes
    plt.rcParams["axes.edgecolor"] = "#333F4B"
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["xtick.color"] = "#333F4B"
    plt.rcParams["ytick.color"] = "#333F4B"


def delete_empty_dirs(_dir):
    """
    Cleanup by deleting folders which have no files in them. Delete folders which only have empty subdirs
    Args:
        _dir:

    Returns:

    """
    _dirs = [x[0] for x in os.walk(_dir)]

    for _d in _dirs:
        if not len([entry for entry in os.scandir(_d) if entry.is_file()]):
            try:
                os.removedirs(_d)
            except OSError:
                pass


def compute_zscore(val1, vals):
    """

    :param vals:
    :return:
    """
    import bottleneck as bn

    # Compute z-score for the values in the column `col`
    zscore = (val1 - bn.nanmean(vals)) / bn.nanstd(vals)

    return zscore


def add_sos(df, method, group_by):
    """

    :param df:
    :param method:
    :param group_by:
    :return:
    """
    groups = df.groupby(group_by, dropna=False)

    for key, vals in tqdm(groups, desc="Adding start of season info"):
        if not vals.empty:
            df.loc[vals.index, f"sos {method}"] = vals["Stage"].unique()[0]

    return df


def compute_zscores(
    df, method, group_by, value_column, num_years=-1, year_column="Harvest Year"
):
    """

    :param df:
    :param method:
    :param group_by:
    :param value_column:
    :param num_years: Number of years to consider for computing z-scores, -1 implies all years
    :return:
    """
    from heapq import nsmallest

    groups = df.groupby(group_by, dropna=False)

    for key, vals in tqdm(
        groups, desc=f"Computing z-scores {value_column} {method} {num_years} years"
    ):
        suffix = "" if num_years == -1 else f" {num_years} years"
        closest_years = (
            len(vals[year_column].unique()) if num_years == -1 else num_years
        )
        harvest_years = vals[year_column].unique()

        for year in [
            ar.now().year - 3,
            ar.now().year,
        ]:  # HACK only compute z-score for the last 3 years
            current_year = ar.now().year
            other_years = harvest_years[harvest_years != current_year]

            # Get the closest `num_years` years
            closest = nsmallest(closest_years, other_years, key=lambda x: abs(x - year))
            vals_subset = vals[vals[year_column].isin(closest)]
            vals_other = vals[vals[year_column] == year]

            # Compute z-score
            if not vals_subset.empty and not vals_other.empty:
                zscore = compute_zscore(
                    vals_other[value_column].values, vals_subset[value_column].values
                )
                df.loc[vals_other.index, f"Z-Score {value_column}{suffix}"] = zscore[0]

    return df


def categorize_zscores(df, bins, labels, cut_column, output_column):
    """

    :param df:
    :param bins:
    :param labels:
    :param cut_column:
    :param output_column:
    :return:
    """
    df.loc[:, output_column] = pd.cut(df[cut_column], bins=bins, labels=labels)

    return df


def detrend_column(df, column, group_by, detrended_column):
    """

    :param df:
    :param column:
    :param group_by:
    :param detrended_column:
    :return:
    """
    from scipy import signal

    groups = df.groupby(group_by, dropna=False)

    for key, vals in groups:
        # Drop rows where Yield is NaN
        vals = vals.dropna(subset=[column])

        # If removing values results in an empty dataframe, skip
        if not vals.empty:
            # Detrend Yield column and add to original dataframe
            detrended = signal.detrend(vals[column].values)
            df.loc[vals.index, detrended_column] = detrended

    return df


def categorize_column(
    df, column, group_by, zscore_column, categories, bins, category_column
):
    """
    HACk: Needs to be updated
    :param df:
    :param column:
    :param group_by:
    :param zscore_column:
    :param categories:
    :param bins:
    :param category_column:
    :return:
    """
    groups = df.groupby(group_by, dropna=False)

    for key, vals in groups:
        # Compute z-score for the values in the Detrended Yield column
        # and add to original dataframe
        zscore = compute_zscore(vals[column].values)
        df.loc[vals.index, zscore_column] = zscore

    # Categorize the z-scores
    categorize_zscores(
        df,
        bins,
        categories,
        cut_column=zscore_column,
        output_column=category_column,
    )

    return df


def get_crop_season(filename):
    """
    Get crop name and season from filename.

    Recognized crops are matched in priority order (longest/most-specific first
    to avoid substring collisions, e.g. "winter_wheat" before "wheat").
    """
    # Multi-word crops must come before their constituent words
    KNOWN_CROPS = [
        "winter_wheat", "spring_wheat",
        "maize", "rice", "soybean", "sorghum", "millet", "teff",
        "wheat", "barley", "cassava", "groundnut", "sesame", "cotton",
        "sugarcane", "potato", "beans", "cowpea", "sunflower", "poppy",
    ]

    crop = None
    for c in KNOWN_CROPS:
        if c in filename:
            crop = c
            break

    if crop is None:
        raise ValueError(f"Crop not found in {filename}")

    if "s1" in filename:
        season_index = 1
    elif "s2" in filename:
        season_index = 2
    else:
        season_index = 1

    return crop, season_index


def create_output_directory(method, admin_zone, country, crop, path_output):
    """

    :param method:
    :param admin_zone:
    :param country:
    :param crop:

    :return:
    """
    dir_output = path_output / "cid" / "indices" / method / admin_zone / country / crop
    os.makedirs(dir_output, exist_ok=True)

    return dir_output


def to_db(db_path, table_name, df, max_retries=10):
    """

    Args:
        db_path:
        table_name:
        df:
        max_retries:

    Returns:

    """
    from pangres import upsert
    from sqlalchemy import create_engine, event

    engine = create_engine(
        "sqlite:///" + str(db_path),
        connect_args={"timeout": 120},
    )

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA busy_timeout=120000")
        cursor.close()

    for attempt in range(max_retries):
        try:
            upsert(
                con=engine,
                df=df,
                table_name=table_name,
                if_row_exists="update",
                chunksize=20,
            )
            return
        except Exception as e:
            if "database is locked" in str(e) and attempt < max_retries - 1:
                from geocif.progress import pwrite
                wait = 2 ** attempt + random.uniform(0, 1)
                pwrite(f"DB locked writing {table_name}, retry {attempt + 1}/{max_retries} in {wait:.1f}s")
                time.sleep(wait)
            else:
                from geocif.progress import pwrite
                pwrite(f"Exception: {e}")
                return


def is_table(database, table_name):
    """
    Check if table_name exists in database. Return True if it does and False if not
    Args:
        database:
        table_name:

    Returns:

    """
    con = sqlite3.connect(database)

    query = "SELECT * FROM sqlite_master"
    df = pd.read_sql_query(query, con)
    con.close()

    if table_name in df["tbl_name"].values:
        return True
    else:
        return False


def plot(X, labels, probabilities=None, parameters=None, ground_truth=False, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 4))
    labels = labels if labels is not None else np.ones(X.shape[0])
    probabilities = probabilities if probabilities is not None else np.ones(X.shape[0])
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    # The probability of a point belonging to its labeled cluster determines
    # the size of its marker
    proba_map = {idx: probabilities[idx] for idx in range(len(labels))}
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_index = np.where(labels == k)[0]
        for ci in class_index:
            try:
                ax.plot(
                    X[ci, 0],
                    X[ci, 1],
                    "x" if k == -1 else "o",
                    markerfacecolor=tuple(col),
                    markeredgecolor="k",
                    markersize=4 if k == -1 else 1 + 5 * proba_map[ci],
                )
            except:
                breakpoint()
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    preamble = "True" if ground_truth else "Estimated"
    title = f"{preamble} number of clusters: {n_clusters_}"
    if parameters is not None:
        parameters_str = ", ".join(f"{k}={v}" for k, v in parameters.items())
        title += f" | {parameters_str}"
    ax.set_title(title)
    plt.tight_layout()
    plt.show()


def pairwise_rmse(df1, df2):
    return np.sqrt(((df1 - df2) ** 2).mean())


def nse(observed, simulated, weights=None):
    """
    Compute Weighted Nash-Sutcliffe Efficiency
    :param observed: Array of observed values
    :param simulated: Array of simulated values
    :param weights: Optional array of weights
    :return: NSE value
    """
    if weights is None:
        weights = np.ones_like(observed)

    weighted_sq_diff = np.sum(weights * (observed - simulated) ** 2)
    weighted_variance = np.sum(
        weights * (observed - np.average(observed, weights=weights)) ** 2
    )

    return 1 - (weighted_sq_diff / weighted_variance)


def mape(observed, simulated, weights=None):
    """
    Compute Weighted Mean Absolute Percentage Error
    :param observed: Array of observed values
    :param forecast: Array of forecast values
    :param weights: Optional array of weights
    :return: MAPE value
    """
    if weights is None:
        weights = np.ones_like(observed)

    weighted_abs_percent_error = weights * np.abs((observed - simulated) / observed)

    return np.sum(weighted_abs_percent_error) / np.sum(weights) * 100


def pbias(observed, simulated, weights=None):
    """
    Compute Weighted Percent Bias
    :param observed: Array of observed values
    :param simulated: Array of simulated values
    :param weights: Optional array of weights
    :return: PBIAS value
    """
    if weights is None:
        weights = np.ones_like(observed)

    weighted_diff_sum = np.sum(weights * (observed - simulated))
    weighted_obs_sum = np.sum(weights * observed)

    return (weighted_diff_sum / weighted_obs_sum) * 100


# Function to remove trend
def detrend(data):
    return data.diff().dropna()


# Function to add trend back
def retrend(original_data, detrended_data):
    try:
        retrended_data = detrended_data.cumsum() + original_data.iloc[0]
    except:
        breakpoint()

    return retrended_data


def linregress(x, y):
    """ """
    # Fit a linear regression model using statsmodels
    import statsmodels.api as sm

    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()

    # Get the slope, intercept, p-value of the trendline
    intercept = model.params[0]
    slope = model.params[1]
    p = model.f_pvalue

    if p < 0.05:
        # Significant, therefore add * to the equation
        eqn = f"y = {slope:.3f}x + {intercept:.2f} *"
    else:
        eqn = f"y = {slope:.3f}x + {intercept:.2f}"

    return eqn


def slope(x, y):
    """ """
    from scipy.stats import mstats
    import pymannkendall as mk

    # Reset index to ensure x and y are aligned
    x = x.reset_index(drop=True)
    y = y.reset_index(drop=True)

    # Note that we are getting slope from one library and intercept from another
    # This is because pymannkendall reports intercept of the Kendall-Theil Robust Line
    # and theilslopes reports intercept of the Theil-Sen estimator, we want the latter
    try:
        trend, h, p, z, Tau, s, var_s, slope, intercept = mk.original_test(y)
        slope, intercept = mstats.theilslopes(y, x)[0], mstats.theilslopes(y, x)[1]
    except (ValueError, ZeroDivisionError):
        slope = np.nan
        intercept = np.nan
        p = np.nan

    return slope, intercept, p


def is_trending(x, y, threshold=0.05):
    """ """
    import pymannkendall as mk

    # Reset index to ensure x and y are aligned
    x = x.reset_index(drop=True)
    y = y.reset_index(drop=True)

    trend, h, p, z, Tau, s, var_s, slope, intercept = mk.original_test(y)

    if p < threshold:
        return True
    else:
        return False


def process_subsets(df, custom_function, **kwargs):
    """
    Processes subsets of the dataframe based on unique values in two columns and
    applies a given custom function

    :param df (pd.DataFrame): The dataframe to process
    :param custom_function: A function to apply to each subsubset dataframe
    :param **kwargs  Additional keyword arguments to pass to the operation function
    """
    frames = []
    for i, value1 in enumerate(df[kwargs["column1"]].unique()):
        subset_df = df[df[kwargs["column1"]] == value1]

        if not subset_df.empty:
            if kwargs["column2"]:
                for j, value2 in enumerate(subset_df[kwargs["column2"]].unique()):
                    subsubset_df = subset_df[subset_df[kwargs["column2"]] == value2]

                    results = custom_function(subsubset_df, i, j, **kwargs)
                    frames.append(results)
            else:
                results = custom_function(subsubset_df, i, i, **kwargs)
                frames.append(results)

    df_results = pd.concat(frames)

    return df_results


def compute_dataframe_transformation(df, group_by=[], column=None, stat="mean"):
    """

    :param df:
    :param group_by:
    :param column:
    :param stat:
    """
    if stat == "mean":
        df = df.groupby(group_by, dropna=False)[column].mean().reset_index()
    else:
        raise NotImplementedError(f"stat {stat} not implemented")

    # Drop any rows where column is NaN
    df = df.dropna(subset=[column])

    return df


def list_directories(directory_path):
    """
    Lists all directories within the specified directory path.

    Parameters:
    - directory_path: A string representing the path to the directory you want to explore.

    Returns:
    - A list of directory names found within the specified directory.
    """
    try:
        # List all entries in the directory given by "directory_path"
        directory_contents = os.listdir(directory_path)

        # Filter out the directories from all entries
        directories = [
            d
            for d in directory_contents
            if os.path.isdir(os.path.join(directory_path, d))
        ]

        return directories
    except FileNotFoundError:
        print(f"Error: The directory '{directory_path}' was not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied to access the directory '{directory_path}'.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def compute_biweekly_index(row):
    """
    Compute the index of the biweekly period for a given day of the year.

    The first biweekly period of the year starts on January 1st.
    Args:
    - row (pd.Series): A row from the DataFrame containing 'year' and 'doy' columns.

    Returns:
    - int: The biweekly period index (starting from 1).
    """
    # Calculate the day of the year, adjusting to start from 0
    day_of_year_zero_indexed = int(row["Doy"]) - 1
    # Compute the biweekly index, adjusting so the first period is index 1
    biweekly_index = (day_of_year_zero_indexed // 14) + 1

    return biweekly_index


def is_leap_year(year):
    """Check if the specified year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def compute_time_periods(df_inp, period_type, year):
    """
    Compute the starting and ending time-periods for a given period type ('dekad', 'biweekly', 'monthly')
    in either a leap or non-leap year.

    Parameters:
    - df: DataFrame with a 'Doy' column.
    - period_type: String indicating the period type ('dekad', 'biweekly', 'monthly').
    - year: The year for the Doy values, used to handle leap years.

    Returns:
    - A tuple with starting and ending periods for the specified period type.
    """
    # Adjust the origin based on whether the year is a leap year
    df = df_inp.copy()
    df["Date"] = pd.to_datetime(
        df["Doy"], unit="D", origin=pd.Timestamp(f"{year}-01-01")
    )

    if period_type.startswith("dekad"):
        df["Period"] = ((df["Date"].dt.dayofyear - 1) // 10) + 1
    elif period_type.startswith("biweekly"):
        df["Period"] = ((df["Date"].dt.dayofyear - 1) // 14) + 1
    elif period_type.startswith("monthly"):
        df["Period"] = df["Month"]
    else:
        return "Invalid period type. Choose 'dekad', 'biweekly', or 'monthly'."

    start_period = df.iloc[0]["Period"]
    end_period = df.iloc[-1]["Period"]

    return start_period, end_period


def compute_h_index(values):
    # Sort the array in descending order
    sorted_value = np.sort(values)[::-1]

    # Iterate through the sorted array to find the h-index
    h_index = 0

    for i, value in enumerate(sorted_value, start=1):
        if value >= i:
            h_index = value
        else:
            break

    return h_index


def get_z_value(alpha):
    """
    Calculate the z-value for a given alpha level.

    Parameters:
    alpha (float): The significance level (e.g., 0.05 for a 95% confidence interval)

    Returns:
    float: The corresponding z-value
    """
    from scipy.stats import norm

    return norm.ppf(1 - alpha / 2)


def wait_or_keypress(seconds=20):
    """Wait for *seconds* or until the user presses any key (cross-platform)."""
    try:
        if sys.platform == "win32":
            import msvcrt
            for remaining in range(seconds, 0, -1):
                print(f"\r  Starting in {remaining}s ... (press any key to start now) ", end="", flush=True)
                deadline = time.monotonic() + 1.0
                while time.monotonic() < deadline:
                    if msvcrt.kbhit():
                        msvcrt.getch()
                        print("\r" + " " * 60 + "\r", end="", flush=True)
                        return
                    time.sleep(0.05)
        else:
            import select
            for remaining in range(seconds, 0, -1):
                print(f"\r  Starting in {remaining}s ... (press Enter to start now) ", end="", flush=True)
                rlist, _, _ = select.select([sys.stdin], [], [], 1.0)
                if rlist:
                    sys.stdin.readline()
                    print("\r" + " " * 60 + "\r", end="", flush=True)
                    return
    except Exception:
        time.sleep(seconds)

    print("\r" + " " * 60 + "\r", end="", flush=True)


def display_run_summary(title, params, wait=20):
    """
    Print a rich-formatted summary of run parameters, then wait.

    Args:
        title: Header string (e.g. "GeoCIF ML Runner" or "CID Indices Runner")
        params: list of (label, value) tuples to display
        wait: seconds to wait before starting (0 to skip)
    """
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from geocif import __version__

    console = Console()
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column()

    table.add_row("version", __version__)
    for label, value in params:
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        table.add_row(label, str(value))

    console.print()
    console.print(
        Panel(
            table,
            title=f"[bold bright_white]{title}[/bold bright_white]",
            border_style="bright_blue",
            padding=(1, 2),
        )
    )
    console.print()

    if wait > 0:
        wait_or_keypress(wait)


def detect_seasons_from_calendar(calendar_path, country, crop, max_season=3):
    """Auto-detect valid seasons for a country/crop from the crop calendar Excel file.

    Checks for sheets named ``{crop}_{N}`` (or just ``{crop}`` for wheat).
    A season is valid when the sheet exists AND the country has at least one
    row with positive calendar values (> 0).  Values of -1 or all-zero
    indicate the crop/season is not grown in that country.

    Args:
        calendar_path: Path to the crop calendar Excel file (.xlsx).
        country: Country name (as it appears in the calendar's "country" column).
        crop: Full crop name (e.g. "soybean", "maize", "winter_wheat").
        max_season: Maximum season number to probe.

    Returns:
        Sorted list of valid season integers (e.g. [1] or [1, 2]).
        Returns [1] if calendar cannot be read or no seasons found.
    """
    from pathlib import Path

    calendar_path = Path(calendar_path)
    if not calendar_path.exists():
        return [1]

    try:
        xl = pd.ExcelFile(calendar_path)
        sheet_names = xl.sheet_names
    except Exception:
        return [1]

    # Wheat has a single season with sheet name = crop name
    if crop in ("winter_wheat", "spring_wheat"):
        if crop in sheet_names:
            return [1]
        xl.close()
        return [1]

    country_lower = country.lower().replace("_", " ")
    found = []

    for s in range(1, max_season + 1):
        sheet = f"{crop}_{s}"
        if sheet not in sheet_names:
            continue

        try:
            df = pd.read_excel(xl, sheet_name=sheet)
        except Exception:
            continue

        # Find country column
        country_col = next(
            (c for c in df.columns if c.lower() == "country"), None
        )
        if country_col is None:
            continue

        # Filter to this country
        rows = df[df[country_col].str.lower().str.strip() == country_lower]
        if rows.empty:
            continue

        # Check for positive calendar values (1=planting, 2=growing, 3=harvest)
        cal_cols = [c for c in df.columns if c not in ("admin", "country", "Country2", "Admin2")]
        if (rows[cal_cols] > 0).any(axis=None):
            found.append(s)

    xl.close()
    return found if found else [1]


def remove_interior_rings(geom):
    """Strip interior rings from a polygon geometry.

    After dissolving admin_2 → admin_1, tiny gaps between the original
    polygons create hundreds of interior rings (holes).  This removes
    them, keeping only the exterior boundary.
    """
    from shapely.geometry import Polygon, MultiPolygon

    if geom is None:
        return geom
    if geom.geom_type == "Polygon":
        return Polygon(geom.exterior)
    elif geom.geom_type == "MultiPolygon":
        return MultiPolygon([Polygon(p.exterior) for p in geom.geoms])
    return geom


# Season name priority lists — used by ml/stats.py and fdw_export.py
# to map CID season numbers (1, 2) to hvstat season_name values.
PRIMARY_SEASON_NAMES = [
    "Long", "Gu", "Season A", "First", "1st Season",
    "Main", "Meher", "Main harvest", "Summer", "Wet",
]
SECONDARY_SEASON_NAMES = [
    "Short", "Deyr", "Season B", "Second", "2nd Season",
    "Winter", "Dry", "Main-off", "Cold-off",
]


def dissolve_to_admin1(gdf):
    """Dissolve admin_2 polygons to admin_1 and clean up geometry.

    Merges sub-polygons by (ADM0_NAME, ADM1_NAME) and removes interior
    rings caused by tiny gaps between original admin_2 boundaries.
    No-op if ADM2_NAME or ADM1_NAME columns are missing.

    Returns the dissolved GeoDataFrame (or original if no dissolve needed).
    """
    if "ADM2_NAME" not in gdf.columns or "ADM1_NAME" not in gdf.columns:
        return gdf
    gdf = gdf.dissolve(by=["ADM0_NAME", "ADM1_NAME"], as_index=False)
    gdf["geometry"] = gdf.geometry.apply(remove_interior_rings)
    return gdf


def display_name(name):
    """Convert underscore-separated lowercase name to title case display.

    ``"united_states_of_america"`` → ``"United States Of America"``
    ``"winter_wheat"`` → ``"Winter Wheat"``
    """
    return name.title().replace("_", " ") if name else name


_MONTH_SHORT_TO_FULL = {
    "Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
    "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
    "Sep": "September", "Oct": "October", "Nov": "November", "Dec": "December",
}


def friendly_stage_label(stage_name):
    """Convert internal stage names to human-readable labels.

    ``"Mar 1-Mar 31"`` → ``"March"``
    ``"Apr 1-Mar 31"`` → ``"March - April"``
    ``"Aug 1-Mar 31"`` → ``"March - August"``

    For ``_r`` methods the first part is the latest month and the second
    is the earliest (planting), so the display order is reversed to show
    planting first.
    """
    if not stage_name:
        return stage_name
    if stage_name.startswith(("Pre-Season", "In-Season")):
        return stage_name
    parts = stage_name.split("-")
    if len(parts) != 2:
        return stage_name
    start_month = parts[0].strip().split()[0]
    end_month = parts[1].strip().split()[0]
    start_full = _MONTH_SHORT_TO_FULL.get(start_month, start_month)
    end_full = _MONTH_SHORT_TO_FULL.get(end_month, end_month)
    if start_month == end_month:
        return start_full
    return f"{end_full} - {start_full}"


def filter_cid_columns(df, fixed_cols, target, stat_cols):
    """Get CID feature column names, excluding fixed/target/meta/engineered columns.

    Args:
        df: DataFrame with wide-format CID columns.
        fixed_cols: List of fixed metadata columns (e.g. Country, Region, ...).
        target: Target column name (e.g. "Yield (tn per ha)").
        stat_cols: Statistics columns (e.g. ["Area (ha)", "Production (tn)"]).

    Returns:
        List of CID column names.
    """
    exclude = set(
        list(fixed_cols)
        + [target]
        + list(stat_cols)
        + [
            f"{target}_class",
            "Region_ID", "lat", "lon", "Country Region", "Country__Region",
            f"Detrended {target}", "Detrended Model", "Detrended Model Type",
            "Stage Names", "Stage_ID", "Stage Range", "Starting Stage", "Ending Stage",
            "Percentage Season",
            "Analogous Year", "Analogous Year Yield",
        ]
    )
    skip_prefixes = (
        f"Median {target}",
        f"Last Year {target}",
        "t - ",
        "nbr_",
    )
    return [
        col for col in df.columns
        if col not in exclude and not col.startswith(skip_prefixes)
    ]


def get_pre_season_init_months(
    planting_month: int,
    *,
    extend_to_month: int | None = None,
    max_lead: int = 6,
) -> list[int]:
    """Return ordered list of init months whose forecasts can reach the season.

    Single source of truth for the pre-season month sequence used by both the
    CID stage (``cid.indices._get_pre_season_months``) and the ML stage
    (``geocif._get_pre_season_init_months``).  Keeping the logic in one place
    so the two stages don't drift apart (which previously caused the CID file
    to contain ``PS_7..PS_12`` while the ML loop iterated ``PS_5..PS_10``,
    leaving only their 4-month overlap usable).

    Args:
        planting_month: First month of the growing season (1-12).
        extend_to_month: If given, walk past ``planting_month - 1`` through
            this calendar month (forecast-only mode where in-season months
            also need init-month rows).  ``None`` = stop at ``planting_month - 1``.
        max_lead: Longest forecast lead in months.  Default ``6`` = the cap
            shared by FLDAS LEAD0..5 and NOAA S2S LEAD1..6.

    Returns:
        Ordered list of int calendar months ``[earliest .. stop_month]``,
        wrapping across the year boundary when needed.
    """
    earliest = (planting_month - max_lead - 1) % 12 + 1
    if extend_to_month is not None:
        stop_month = extend_to_month
    else:
        stop_month = (planting_month - 1) if planting_month > 1 else 12

    months = []
    m = earliest
    while True:
        months.append(m)
        if m == stop_month:
            break
        m = m % 12 + 1
        if len(months) > 12:
            break
    return months


# CID types that come from forecast products rather than observed data.
# Used by both the CID stage (when deciding the pre-season month range)
# and the ML stage (when picking which run_time_steps to execute).
_FORECAST_CID_TYPES = frozenset({"FLDAS", "S2S"})


def is_forecast_only(use_cids) -> bool:
    """``True`` iff ``use_cids`` is non-empty and every entry is a forecast type.

    Centralised so the CID, ML, and outlook stages all answer the same way.
    """
    return "all" not in use_cids and all(c in _FORECAST_CID_TYPES for c in use_cids)


def has_forecast(use_cids) -> bool:
    """``True`` if ``use_cids`` includes any forecast type (or the ``'all'`` token)."""
    return "all" in use_cids or any(c in _FORECAST_CID_TYPES for c in use_cids)


def load_country_boundary_gdf(parser, shapefile_path, *, country=None):
    """Read a boundary shapefile, apply config-driven column renames, fix the
    Tanzania short-name, drop columns that would duplicate after rename, and
    optionally filter to a single country.

    Single home for the load+rename pattern so per-country corrections (e.g.
    ``Tanzania`` -> ``United Republic of Tanzania``) and conflict-drop rules
    stay consistent across analysis, geocif, agmet, and yield_outlook.

    Per-call-site extras (Alaska/Hawaii exclusion, antimeridian clipping,
    dissolve to admin_1) remain in the caller — only the load+rename block
    is centralised.

    Args:
        parser: ConfigParser carrying the boundary-column mapping sections.
        shapefile_path: Path or str to the shapefile.
        country: If given, filter to rows whose ADM0_NAME matches this
            (case- and underscore-insensitive).

    Returns:
        GeoDataFrame with standardised column names.
    """
    import geopandas as gpd
    from geoprepare.georegion import get_boundary_col_mapping

    gdf = gpd.read_file(shapefile_path, engine="pyogrio")
    rename = get_boundary_col_mapping(parser, shapefile_path)

    # Apply country-name corrections BEFORE renaming so we find the source column
    adm0_src = next((k for k, v in rename.items() if v == "ADM0_NAME"), "ADM0_NAME")
    if adm0_src in gdf.columns:
        gdf[adm0_src] = gdf[adm0_src].replace(
            "Tanzania", "United Republic of Tanzania"
        )

    # Drop columns that would create duplicates after rename
    # (e.g. shapefile has both name0 and ADM0_NAME; renaming name0->ADM0_NAME would duplicate)
    targets = set(rename.values())
    sources = set(rename.keys())
    conflicting = [c for c in gdf.columns if c in targets and c not in sources]
    if conflicting:
        gdf = gdf.drop(columns=conflicting)
    gdf = gdf.rename(columns=rename)

    if country is not None:
        country_norm = country.replace("_", " ").lower()
        adm0_col = next(
            (c for c in ("ADM0_NAME", "ADMIN0", "name0") if c in gdf.columns), None
        )
        if adm0_col:
            mask = gdf[adm0_col].str.lower().str.replace("_", " ") == country_norm
            gdf = gdf[mask].copy()
    return gdf
