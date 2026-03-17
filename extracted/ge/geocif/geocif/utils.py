import os
import sys
import time
import random

import sqlite3
import numpy as np
import pandas as pd
import arrow as ar
from tqdm.auto import tqdm
import matplotlib.pyplot as plt


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
    Get crop name and season from filename
    """
    if "winter_wheat" in filename:
        crop = "winter_wheat"
        season_index = 1
    elif "spring_wheat" in filename:
        crop = "spring_wheat"
        season_index = 1
    elif "maize" in filename:
        crop = "maize"
    elif "rice" in filename:
        crop = "rice"
    elif "soybean" in filename:
        crop = "soybean"
    elif "sorghum" in filename:
        crop = "sorghum"
    elif "millet" in filename:
        crop = "sorghum"
    elif "teff" in filename:
        crop = "teff"
    else:
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


def to_db(db_path, table_name, df, max_retries=5):
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
        connect_args={"timeout": 60},
    )

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
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
                wait = 2 ** attempt + random.uniform(0, 1)
                print(f"DB locked writing {table_name}, retry {attempt + 1}/{max_retries} in {wait:.1f}s")
                time.sleep(wait)
            else:
                print(f"Exception: {e}")
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
        title: Header string (e.g. "GeoCIF ML Runner" or "CEI Indices Runner")
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
