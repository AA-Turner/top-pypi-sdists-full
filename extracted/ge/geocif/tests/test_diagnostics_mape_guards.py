"""viz/diagnostics (audit B rows): the scatter MAPE annotation used sklearn's
MAPE on unfiltered zeros (one zero-yield row -> ~1e15), and
``mape_choropleth`` painted MAPE > 100 like "no data".
"""
import matplotlib

matplotlib.use("Agg")

import numpy as np
import pandas as pd
import pytest

from geocif.viz import diagnostics as diag


def test_mape_fraction_excludes_zero_observed():
    y_obs = np.array([10.0, 0.0, 20.0])
    y_pred = np.array([11.0, 5.0, 18.0])
    # (0.1 + 0.1) / 2 over the two non-zero rows; the zero row is ignored.
    assert diag._mape_fraction(y_obs, y_pred) == pytest.approx(0.1)
    assert np.isnan(diag._mape_fraction([0.0, 0.0], [1.0, 2.0]))


def test_scatter_annotation_survives_zero_yield(tmp_path):
    df = pd.DataFrame({
        "Observed Yield (tn per ha)": [10.0, 0.0, 20.0, 15.0],
        "Predicted Yield (tn per ha)": [11.0, 5.0, 18.0, 15.0],
        "Harvest Year": [2020, 2021, 2022, 2023],
    })
    diag.scatter_obs_pred(df, "t", tmp_path, "scatter.png")
    assert (tmp_path / "scatter.png").exists()


def test_mape_for_map_caps_instead_of_blanking():
    out = diag._mape_for_map(pd.Series([12.0, 150.0, np.nan, "x"]))
    assert out.tolist()[:2] == [12.0, 100.0]
    assert np.isnan(out.iloc[2]) and np.isnan(out.iloc[3])


def test_mape_choropleth_passes_capped_values(tmp_path, monkeypatch):
    from geocif.viz import plot

    captured = {}

    def fake_plot_map(dg, df, **kwargs):
        captured["df"] = df.copy()
        captured["kwargs"] = kwargs

    monkeypatch.setattr(plot, "plot_map", fake_plot_map)
    df = pd.DataFrame({
        "Country Region": ["kenya a", "kenya b", "kenya c"],
        "Mean Absolute Percentage Error": [20.0, 180.0, 40.0],
    })
    diag.mape_choropleth(None, df, ["Kenya"], False, tmp_path, "m.png")
    vals = captured["df"]["Mean Absolute Percentage Error"].tolist()
    assert vals == [20.0, 100.0, 40.0]       # 180 is painted at the cap, not blank
    assert captured["kwargs"]["vmin"] == 0
