import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant


class DetrendedData:
    """
    A class to store the detrended series, the model used for detrending,
    and the type of model ('mean', 'linear', 'quadratic', 'difference', 'gaussian').
    """

    def __init__(self, detrended_series, trend_model, model_type):
        self.detrended_series = detrended_series
        self.trend_model = trend_model
        self.model_type = model_type


def detrend_dataframe(df, column_name="y", model_type="gaussian"):
    """
    Removes the trend from the specified column of a DataFrame using the specified method
    (mean, linear, quadratic, difference, gaussian) or the method that results in the
    lowest AIC value ('best').

    The 'gaussian' method applies a low-frequency Gaussian filter (sigma=5 years) and
    returns percent anomalies: 100 * (Yi - Yei) / Yei

    Parameters:
    - df: pandas DataFrame containing the time series data.
    - column_name: string name of the column to detrend.
    - model_type: string specifying which model to use for detrending ('mean', 'linear',
                  'quadratic', 'difference', 'gaussian', or 'best' for automatic selection
                  based on AIC among OLS models).

    Returns:
    - DetrendedData object containing the detrended series, the statistical model,
      and the model type.
    """
    if model_type == "gaussian":
        return _detrend_gaussian(df, column_name)

    df["t"] = np.array(df["Harvest Year"])

    # Mean method
    mean_model = OLS(df[column_name], np.ones(len(df))).fit()

    # Linear trend model
    X_linear = add_constant(df["t"])
    linear_model = OLS(df[column_name], X_linear).fit()

    # Quadratic trend model
    X_quad = add_constant(np.column_stack((df["t"], df["t"] ** 2)))
    quad_model = OLS(df[column_name], X_quad).fit()

    # Differencing method
    diff_series = df[column_name].diff().dropna()
    diff_model = OLS(diff_series, np.ones(len(diff_series))).fit()

    models = {
        "mean": mean_model,
        "linear": linear_model,
        "quadratic": quad_model,
        "difference": diff_model
    }

    if model_type == "best":
        best_model_type = min(models, key=lambda x: models[x].aic)
    else:
        best_model_type = model_type

    best_model = models[best_model_type]

    if best_model_type == "mean":
        detrended = df[column_name] - mean_model.predict(np.ones(len(df)))
    elif best_model_type == "linear":
        detrended = df[column_name] - linear_model.predict(X_linear)
    elif best_model_type == "quadratic":
        detrended = df[column_name] - quad_model.predict(X_quad)
    else:  # difference
        detrended = df[column_name].diff().dropna()

    return DetrendedData(detrended, best_model, best_model_type)


def _detrend_gaussian(df, column_name, sigma=5):
    """
    Detrend using a low-frequency Gaussian filter and return percent anomalies.

    Yai = 100 * (Yi - Yei) / Yei

    where Yei is the expected yield from the Gaussian filter.

    Parameters:
    - df: DataFrame with 'Harvest Year' and the target column.
    - column_name: the yield column name.
    - sigma: kernel standard deviation in years (default 5).

    Returns:
    - DetrendedData with percent anomalies, a dict model, and model_type='gaussian'.
    """
    yields = df[column_name].values.astype(float)
    years = df["Harvest Year"].values.astype(float)

    # Interpolate NaN values before filtering (gaussian_filter1d propagates NaN)
    nan_mask = np.isnan(yields)
    yields_filled = yields.copy()
    if nan_mask.any() and not nan_mask.all():
        valid = ~nan_mask
        yields_filled[nan_mask] = np.interp(
            years[nan_mask], years[valid], yields[valid]
        )

    expected = gaussian_filter1d(yields_filled, sigma=sigma)

    # Avoid division by zero
    safe_expected = np.where(expected == 0, np.nan, expected)
    pct_anomaly = 100.0 * (yields - expected) / safe_expected

    # Restore NaN positions
    pct_anomaly[nan_mask] = np.nan

    # Fit a linear model on the Gaussian-filtered expected yields so we can
    # extrapolate Yei for future (unseen) years.  Force ``has_constant='add'``
    # so ``X`` always has 2 columns even when ``years`` has a single unique
    # value (statsmodels' default would skip the constant column, producing
    # a 1-param model that mismatches the 2-column predict-time X built at
    # geocif.py _retrend_predictions).
    X = add_constant(years, has_constant="add")
    extrap_model = OLS(expected, X).fit()

    model = {
        "sigma": sigma,
        "expected_yields": pd.Series(expected, index=df.index),
        "years": years,
        "extrap_model": extrap_model,
    }

    detrended = pd.Series(pct_anomaly, index=df.index)
    return DetrendedData(detrended, model, "gaussian")


def segment_aware_trend(train_years, train_yields, *,
                        cp_threshold=0.5,
                        tcp_minmax=(0, 8),
                        tseg_minlength=5,
                        mcmc_seed=42,
                        min_segment=5):
    """Fit a linear trend on the segment after the most-recent strong BEAST
    changepoint.  Caller MUST pass the training-only series (forecast year
    excluded) so we don't leak.

    Returns ``(intercept, slope, cp_used_year_or_None, n_used)``.

    - Builds a contiguous annual series with NaN gaps (BEAST needs that).
    - Runs ``Rbeast.beast`` with the supplied params.
    - Picks the LATEST (max-year) CP whose posterior probability
      ``>= cp_threshold``.
    - Fits OLS on years ``>= that CP``.  If post-CP segment has
      ``< min_segment`` observations, or no strong CP exists, fits OLS on
      the full series.
    """
    import Rbeast as rb

    years = np.asarray(train_years, dtype=float)
    yields = np.asarray(train_yields, dtype=float)
    valid = ~np.isnan(yields) & ~np.isnan(years)
    if valid.sum() < 2:
        return (
            float(np.nanmean(yields)) if valid.any() else np.nan,
            0.0, None, int(valid.sum()),
        )

    y0 = int(years[valid].min())
    y1 = int(years[valid].max())
    full = np.full(y1 - y0 + 1, np.nan, dtype=float)
    for yr, val in zip(years[valid].astype(int), yields[valid]):
        full[yr - y0] = val

    o = rb.beast(
        full, start=y0, deltat=1, season="none",
        tcp_minmax=list(tcp_minmax), tseg_minlength=tseg_minlength,
        mcmc_seed=mcmc_seed,
        quiet=True, print_param=False,
        print_progress=False, print_warning=False,
    )
    cp_arr = np.atleast_1d(o.trend.cp)
    cp_pr = np.atleast_1d(o.trend.cpPr)
    ok = np.isfinite(cp_arr)
    cp_years_all = cp_arr[ok]
    cp_probs_all = cp_pr[ok]
    strong = cp_probs_all >= cp_threshold

    seg_mask = valid.copy()
    cp_used = None
    if strong.any():
        cp_year = int(cp_years_all[strong].max())
        candidate = valid & (years >= cp_year)
        if candidate.sum() >= min_segment:
            seg_mask = candidate
            cp_used = cp_year

    x = years[seg_mask]
    y = yields[seg_mask]
    if len(x) == 1:
        return float(y[0]), 0.0, cp_used, 1
    X = np.column_stack([np.ones_like(x), x])
    intercept, slope = np.linalg.lstsq(X, y, rcond=None)[0]
    return float(intercept), float(slope), cp_used, int(seg_mask.sum())


def compute_trend(detrended_data, future_time_points=None):
    """
    Adds the trend back to a detrended series, useful for forecasting or visualization.

    For gaussian detrending, returns the expected yield Yei at the given time points
    (extrapolated via linear fit on the Gaussian-filtered series).

    Parameters:
    - detrended_data: DetrendedData object containing the detrended series and the model.
    - future_time_points: array of time points for which to compute the trend component.

    Returns:
    - The trend component (expected yield for gaussian, OLS prediction for others).
    """
    future_time_points = np.array(future_time_points)

    model_type = detrended_data.model_type.unique()[0]
    model = detrended_data.trend_model.unique()[0]

    if model_type == "gaussian":
        X = add_constant(future_time_points, has_constant="add")
        trend_component = model["extrap_model"].predict(X)
    elif model_type == "mean":
        trend_component = model.predict(
            np.ones(len(future_time_points)), has_constant="add"
        )
    elif model_type == "linear":
        X_linear = add_constant(future_time_points, has_constant="add")
        trend_component = model.predict(X_linear)
    elif model_type == "quadratic":
        X_quad = add_constant(
            np.column_stack((future_time_points, future_time_points**2)),
            has_constant="add",
        )
        trend_component = model.predict(X_quad)
    else:  # difference
        trend_component = pd.Series(np.nan, index=future_time_points)
        trend_component.iloc[0] = model.params[0]  # Add mean of differenced series

    return trend_component
