"""detrend_method = mean must retrend (2026-10-26).

compute_trend passed has_constant="add" to the fitted OLS results'
predict(), which forwards keyword arguments to RegressionModel.predict and
raised TypeError on every region, so a run with detrend_method = mean wrote
no ML predictions at all.
"""
import numpy as np
import pandas as pd
import pytest

from geocif.ml import trend


def test_mean_trend_component_is_the_training_mean():
    y = [1.0, 2.0, 3.0, 2.0, 1.5, 2.5, 3.5, 1.0, 2.0]
    df = pd.DataFrame({"Harvest Year": np.arange(2015, 2024), "y": y})
    fit = trend.detrend_dataframe(df.copy(), "y", "mean")
    assert np.asarray(fit.detrended_series, dtype=float) == pytest.approx(np.array(y) - np.mean(y))

    # Same shape as the retrend call in Geocif: per-row columns of the region frame.
    n = len(df)
    obj = trend.DetrendedData(
        fit.detrended_series,
        pd.Series([fit.trend_model] * n),
        pd.Series([fit.model_type] * n),
    )
    out = trend.compute_trend(obj, pd.Series([2024], index=["Harvest Year"]))
    assert float(out[0]) == pytest.approx(np.mean(y))
