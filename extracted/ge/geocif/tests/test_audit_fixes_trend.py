"""Gaussian retrend must use the same reference curve as the training
anomalies (2026-09-30 audit, B "gaussian retrend mismatch").

Training anomalies are 100 * (Y - Yei) / Yei with Yei the LOCAL Gaussian
smooth; the hindcast retrend used the global OLS line through the smooth
instead, so on a plateau-then-rise series train and test disagreed on the
reference by tens of percent.
"""
import numpy as np
import pandas as pd
import pytest
from statsmodels.tools.tools import add_constant

from geocif.geocif import Geocif
from geocif.ml import trend


def _plateau_then_rise(skip_year=None):
    years = np.arange(2000, 2020)
    yields = np.where(years < 2010, 2.0, 2.0 + 0.3 * (years - 2009))
    df = pd.DataFrame({"Harvest Year": years, "y": yields})
    if skip_year is not None:
        df = df[df["Harvest Year"] != skip_year].reset_index(drop=True)
    return df


def _ols(model, year):
    X = add_constant(np.array([float(year)]), has_constant="add")
    return float(model["extrap_model"].predict(X)[0])


def test_training_year_reproduces_its_own_smooth_value():
    df = _plateau_then_rise()
    model = trend.detrend_dataframe(df.copy(), "y", "gaussian").trend_model
    smooth = np.asarray(model["expected_yields"], dtype=float)
    assert trend.gaussian_expected_for_year(model, 2003) == pytest.approx(smooth[3])
    assert trend.gaussian_expected_for_year(model, 2000) == pytest.approx(smooth[0])
    # The OLS line (the old reference) is a different curve: on the plateau
    # start it sits well below the smooth.
    assert abs(_ols(model, 2000) - smooth[0]) > 0.1


def test_loocv_hole_is_interpolated_between_neighbours():
    df = _plateau_then_rise(skip_year=2012)
    model = trend.detrend_dataframe(df.copy(), "y", "gaussian").trend_model
    smooth = pd.Series(np.asarray(model["expected_yields"], dtype=float),
                       index=df["Harvest Year"].values)
    expected = 0.5 * (smooth[2011] + smooth[2013])
    assert trend.gaussian_expected_for_year(model, 2012) == pytest.approx(expected)


def test_years_beyond_the_fit_extrapolate_with_the_ols_line():
    df = _plateau_then_rise()
    model = trend.detrend_dataframe(df.copy(), "y", "gaussian").trend_model
    assert trend.gaussian_expected_for_year(model, 2025) == pytest.approx(_ols(model, 2025))
    assert trend.gaussian_expected_for_year(model, 1995) == pytest.approx(_ols(model, 1995))


def test_retrend_predictions_uses_the_local_smooth():
    df = _plateau_then_rise(skip_year=2012)
    model = trend.detrend_dataframe(df.copy(), "y", "gaussian").trend_model
    obj = Geocif.__new__(Geocif)
    obj.target = "y"
    obj.df_train = pd.DataFrame(
        {"Region": ["R"] * len(df), "Detrended Model Type": "gaussian"}
    )
    obj.detrend_models = {"R": model}
    df_region = pd.DataFrame(
        {"Region": ["R"], "Harvest Year": [2012], "Detrended Model Type": [None]}
    )
    # a 0 % anomaly must come back as the reference yield itself
    y_pred, ci = obj._retrend_predictions(np.array([0.0]), df_region, None)
    assert ci is None
    assert y_pred[0] == pytest.approx(trend.gaussian_expected_for_year(model, 2012))
