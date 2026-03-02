import os
import numpy as np
import pandas as pd
import bottleneck as bn


def number_threshold(ts, threshold, above=None, below=None):
    """

    Args:
        ts ():
        threshold ():
        above ():
        below ():

    Returns:

    """
    # Compute number of values in array that are above/below threshold
    if above:
        count = (ts > threshold).sum(axis=0)
    if below:
        count = (ts < threshold).sum(axis=0)

    return count


def consecutive_threshold(ts, threshold, above=None, below=None):
    """

    Args:
        ts ():
        threshold ():
        above ():
        below ():

    Returns:

    """
    # Find number of consecutive days above/below threshold in array ts
    from itertools import accumulate
    from collections import Counter

    vals = [0]

    groups = accumulate(
        [0] + [(a >= threshold) != (b >= threshold) for a, b in zip(ts, ts[1:])]
    )
    counts = sorted(Counter(groups).items())

    if above:
        vals = [c for n, c in counts if (n % 2 == 0) == (ts[0] >= threshold)]
    if below:
        vals = [c for n, c in counts if (n % 2 == 0) != (ts[0] >= threshold)]

    return np.sum(vals)


def compute_threshold(ts, type="median", percentile=None):
    """

    Args:
        ts ():
        type ():
        percentile ():

    Returns:

    """
    if type == "median":
        return np.nanmedian(ts)
    elif type == "mean":
        return np.nanmean(ts)
    elif type == "max":
        return np.nanmax(ts)
    elif type == "min":
        return np.nanmin(ts)
    elif type == "percentile":
        return np.nanpercentile(ts, percentile)
    else:
        raise ValueError("type must be median, mean, max or min")


def sign(x, n):
    """

    :param x:
    :param n:
    :return:
    """
    s = 0
    for k in range(n - 1):
        for j in range(k + 1, n):
            s += np.sign(x[j] - x[k])

    return s


def fe(df: pd.DataFrame, df_ml: pd.DataFrame, mask, eo_model, df_now_train):
    """

    Args:
        df ():
        df_ml ():
        mask ():

    Returns:

    """
    # Perform feature engineering for variables like NDVI
    percentiles = [
        "t10",
        "t20",
        "t30",
        "t40",
        "t50",
        "t60",
        "t70",
        "t80",
        "t90",
        "t100",
    ]

    df = df.copy()
    df_ml = df_ml.copy()

    # Create column containing percentage of rows
    df.loc[:, "fraction_of_season"] = range(1, len(df) + 1)
    df.loc[:, "fraction_of_season"] = df.loc[:, "fraction_of_season"] * 100 / len(df)

    # Obtain data for current region for years other than current season
    current_region = df["region"].unique()[0]
    current_season = df["harvest_season"].unique()[0]
    other_years_df = df_now_train[
        (df_now_train["region"] == current_region)
        & (df_now_train["harvest_season"] != current_season)
    ]

    for var in eo_model:
        if var in df:
            for idx, f in enumerate(percentiles):
                perc = int(f[1:])
                closest_years = df["fraction_of_season"].sub(perc).abs().idxmin()
                df_ml.loc[mask, f"{f}_{var}"] = df.loc[closest_years][var]

                # # cumulative sum
                # current_sum = df.loc[:closest_years][var].values.sum()
                # df_ml.loc[mask, f'cum_{f}_{var}'] = [current_sum]
                #
                # if idx != len(percentiles) - 1:
                #     next_perc = int(percentiles[idx + 1][1:])
                #     next_val = df[''fraction_of_season''].sub(next_perc).abs().idxmin()
                #
                #     # differences in cumulative values
                #     df_ml.loc[mask, f'diff_{f}_{var}'] = [df.loc[:next_val][var].values.sum() - current_sum]
                # if not is_future and f'{f}_{var}' not in self.feature_names:
                #     self.feature_names.extend([f'{f}_{var}'])
                # percentile values for entire season: min, 25th, 50th, 75, 90th, max
            df_ml.loc[mask, f"min_{var}"] = bn.nanmin(df[var].values)
            df_ml.loc[mask, f"p25_{var}"] = np.nanpercentile(df[var].values, 25)
            df_ml.loc[mask, f"p50_{var}"] = np.nanpercentile(df[var].values, 50)
            df_ml.loc[mask, f"p75_{var}"] = np.nanpercentile(df[var].values, 75)
            df_ml.loc[mask, f"p90_{var}"] = np.nanpercentile(df[var].values, 90)
            df_ml.loc[mask, f"max_{var}"] = bn.nanmax(df[var].values)

            # for threshold in [25, 50, 75, 90]:
            #     t = features.compute_threshold(other_years_df[var].values, type='percentile', percentile=threshold)
            #
            #     # Find number of days where var is > xth percentile of median from all other years
            #     df_ml.loc[mask, f'count_above_{threshold}p_{var}'] = features.number_threshold(df[var].values, t, above=True)
            #     # Find number of days where var is < xth percentile of median from all other years
            #     df_ml.loc[mask, f'count_below_{threshold}p_{var}'] = features.number_threshold(df[var].values, t, below=True)
            #     # Find number of consecutive days where var is > xth percentile of median from all other years
            #     df_ml.loc[mask, f'consecutive_above_{threshold}p_{var}'] = features.consecutive_threshold(df[var].values, t, above=True)
            #     # Find number of consecutive days where var is < xth percentile of median from all other years
            #     df_ml.loc[mask, f'consecutive_below_{threshold}p_{var}'] = features.consecutive_threshold(df[var].values, t, below=True)

            # cumulative sum
            current_sum = np.nansum(df[var].values)
            df_ml.loc[mask, f"cum_{var}"] = [current_sum]
        else:
            raise KeyError(f"{var} does not exist in dataframe")

        # df_ml.loc[mask, f'count_above_mean_{var}'] = feature_calculators.count_above_mean(df[var])
        # df_ml.loc[mask, f'mean_abs_change_{var}'] = feature_calculators.mean_abs_change(df[var])
    # Find day where NDVI is peak value
    if isinstance(df["ndvi"].idxmax(), int) or isinstance(df["ndvi"].idxmax(), float):
        # convert datetime column from object to datetime
        df.loc[:, "datetime"] = pd.to_datetime(df["datetime"])
        df = df.set_index("datetime")

    df_ml.loc[mask, "doy_peak_ndvi"] = pd.to_datetime(df["ndvi"].idxmax()).dayofyear

    # count number of days with 0 precip
    if "chirps" in df.columns:
        df_ml.loc[mask, "zero_precip"] = np.count_nonzero(df["chirps"] == 0)
    else:
        df_ml.loc[mask, "zero_precip"] = np.count_nonzero(df["cpc_precip"] == 0)

    return df_ml


def loop_fe(df: pd.DataFrame, df_ml: pd.DataFrame, mask, eo_model, df_now_train):
    """
    Perform feature engineering
    Args:
        df:
        df_ml:
        mask: mask to get data from specific year and adm1

    Returns:

    """
    # get yield for adm1, year combination
    values = df["yield"].values

    if np.isnan(
        values
    ).all():  # If all target (yield) values are NaN, then just use NaN
        df_ml.loc[mask, "yield"] = np.nan
    elif np.isnan(values).any():  # If non NaN values exist, then use last non NaN value
        df_ml.loc[mask, "yield"] = pd.unique(values[~np.isnan(values)])[-1]
    else:  # No NaNs, get the last unique value
        df_ml.loc[mask, "yield"] = pd.unique(values)[-1]

    # Compute features
    df_ml = fe(df, df_ml, mask, eo_model, df_now_train)

    return df_ml


def mk_test(x, alpha=0.05):
    """
    @author: Michael Schramm
    https://github.com/mps9506/Mann-Kendall-Trend/blob/master/mk_test.py
    This function is derived from code originally posted by Sat Kumar Tomer
    (satkumartomer@gmail.com)
    See also: http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm
    The purpose of the Mann-Kendall (MK) test (Mann 1945, Kendall 1975, Gilbert
    1987) is to statistically assess if there is a monotonic upward or downward
    trend of the variable of interest over time. A monotonic upward (downward)
    trend means that the variable consistently increases (decreases) through
    time, but the trend may or may not be linear. The MK test can be used in
    place of a parametric linear regression analysis, which can be used to test
    if the slope of the estimated linear regression line is different from
    zero. The regression analysis requires that the residuals from the fitted
    regression line be normally distributed; an assumption not required by the
    MK test, that is, the MK test is a non-parametric (distribution-free) test.
    Hirsch, Slack and Smith (1982, page 107) indicate that the MK test is best
    viewed as an exploratory analysis and is most appropriately used to
    identify stations where changes are significant or of large magnitude and
    to quantify these findings.
    Input:
        x:   a vector of data
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p value of the significance test
        z: normalized test statistics
    Examples
    --------
      >>> x = np.random.rand(100)
      >>> trend,h,p,z = mk_test(x,0.05)
    """
    from scipy.stats import norm

    n = len(x)

    # calculate S
    s = sign(x, n)

    # calculate the unique data
    unique_x = np.unique(x)
    g = len(unique_x)

    # calculate the var(s)
    if n == g:  # there is no tie
        var_s = (n * (n - 1) * (2 * n + 5)) / 18
    else:  # there are some ties in data
        tp = np.bincount(np.searchsorted(unique_x, x))
        var_s = (n * (n - 1) * (2 * n + 5) - np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18

    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s == 0:
        z = 0
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)

    # calculate the p_value
    p = 2 * (1 - norm.cdf(abs(z)))  # two tail test
    h = abs(z) > norm.ppf(1 - alpha / 2)

    if (z < 0) and h:
        trend = "decreasing"
    elif (z > 0) and h:
        trend = "increasing"
    else:
        trend = "no trend"

    return trend, h, p, z


if __name__ == "__main__":
    pass
