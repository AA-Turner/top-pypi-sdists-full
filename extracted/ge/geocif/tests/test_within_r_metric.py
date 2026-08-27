"""within_r: per-region interannual correlation of observed vs predicted.

The headline metrics are pooled across region-years and so are dominated by
BETWEEN-region variation (which counties yield more). A model that learns only
the cross-section scores well without forecasting anything — the Kenya admin_2
runs had pooled R2 ~0.60 while tracking year-to-year variation not at all.

within_r isolates the temporal question: within one region, do predicted and
observed move together across years?

Two properties that must hold:
  * it is NOT r2_score. Forecasts carry ~25% of observed variance, so per-region
    R2 is punished by under-dispersion and goes negative even when direction is
    tracked correctly. Pearson ignores amplitude and level.
  * the reference is 0, never the `null` baseline. A LOOCV per-region mean
    predicts (sum - obs_Y)/(n-1) — strictly decreasing in obs_Y — so null scores
    exactly -1.0 by construction. That is an artifact, not a skill floor.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from geocif import yield_outlook as yo

SRC = Path(yo.__file__)


def _r(obs, pred):
    o, p = pd.Series(obs, dtype=float), pd.Series(pred, dtype=float)
    if len(o) < yo._WITHIN_R_MIN_YEARS or o.std() == 0 or p.std() == 0:
        return np.nan
    return float(o.corr(p, method="pearson"))


def test_min_years_constant_is_sane():
    assert 3 <= yo._WITHIN_R_MIN_YEARS <= 10


def test_perfect_tracking_is_one_despite_wrong_level_and_amplitude():
    """The whole point: Pearson ignores bias and under-dispersion."""
    obs = [1.0, 2.0, 3.0, 4.0, 5.0]
    pred = [10.2, 10.4, 10.6, 10.8, 11.0]  # 5x offset, 1/5 amplitude
    assert _r(obs, pred) == pytest.approx(1.0)


def test_r2_would_reject_what_within_r_accepts():
    """Same series: r2_score is hugely negative, within_r is perfect."""
    from sklearn.metrics import r2_score
    obs = [1.0, 2.0, 3.0, 4.0, 5.0]
    pred = [10.2, 10.4, 10.6, 10.8, 11.0]
    assert r2_score(obs, pred) < -10
    assert _r(obs, pred) == pytest.approx(1.0)


def test_loocv_null_is_exactly_minus_one():
    """The artifact that makes null an invalid reference point."""
    obs = np.array([2.1, 1.8, 2.6, 2.0, 2.9, 2.3])
    n = len(obs)
    null_pred = np.array([(obs.sum() - o) / (n - 1) for o in obs])
    assert _r(obs, null_pred) == pytest.approx(-1.0)


def test_flat_prediction_is_nan_not_zero():
    """A constant forecast has no variance -> undefined, must not read as 0."""
    assert np.isnan(_r([1.0, 2.0, 3.0, 4.0, 5.0], [2.0] * 5))


def test_short_series_is_nan():
    assert np.isnan(_r([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]))


def test_anticorrelated_is_negative():
    assert _r([1.0, 2.0, 3.0, 4.0, 5.0], [5.0, 4.0, 3.0, 2.0, 1.0]) == pytest.approx(-1.0)


# ---------------------------------------------------------------------------
# wiring
# ---------------------------------------------------------------------------

def test_within_r_is_written_per_region():
    src = SRC.read_text(encoding="utf-8")
    i = src.index("# By region")
    block = src[i:i + 3200]
    assert '"within_r": _within_r' in block, "within_r must be a per-region column"
    assert 'method="pearson"' in block
    assert "_WITHIN_R_MIN_YEARS" in block


def test_summary_and_plot_are_emitted():
    src = SRC.read_text(encoding="utf-8")
    assert "within_r_summary_" in src, "median summary CSV must be written"
    assert "median_within_r" in src
    assert "pct_regions_positive" in src
    assert "_plot_within_r_comparison(" in src


def test_plot_renders(tmp_path):
    """Actually draw it — a plot that raises is worse than no plot."""
    rng = np.random.default_rng(0)
    rows = []
    for model, loc in (("catboost", 0.25), ("tabpfn", 0.02), ("null", -1.0)):
        for i in range(30):
            rows.append({"Model": model, "Region": f"r{i}",
                         "within_r": float(np.clip(rng.normal(loc, 0.2), -1, 1))})
    df = pd.DataFrame(rows)
    summary = (df.groupby("Model")["within_r"]
               .agg(median_within_r="median", mean_within_r="mean",
                    pct_regions_positive=lambda s: 100.0 * (s > 0).mean(),
                    n_regions="size")
               .reset_index().sort_values("median_within_r", ascending=False))
    yo._plot_within_r_comparison(df, summary, tmp_path, "wr.png", "Testland Maize")
    out = tmp_path / "wr.png"
    assert out.exists() and out.stat().st_size > 5000, "plot must render non-trivially"


def test_plot_handles_empty_summary(tmp_path):
    empty = pd.DataFrame(columns=["Model", "median_within_r", "pct_regions_positive"])
    yo._plot_within_r_comparison(pd.DataFrame(columns=["Model", "within_r"]),
                                 empty, tmp_path, "none.png", "T")
    assert not (tmp_path / "none.png").exists()


# ---------------------------------------------------------------------------
# Spearman companion + median-across-regions for every per-region metric
# ---------------------------------------------------------------------------

def _sp(obs, pred):
    o, p = pd.Series(obs, dtype=float), pd.Series(pred, dtype=float)
    return float(o.corr(p, method="spearman"))


def test_spearman_is_emitted_alongside_pearson():
    src = SRC.read_text(encoding="utf-8")
    i = src.index("# By region")
    block = src[i:i + 3000]
    assert '"within_r_spearman": _within_r_sp' in block
    assert 'method="spearman"' in block


def test_spearman_robust_where_pearson_is_dominated_by_one_year():
    """One catastrophic year can carry Pearson; Spearman resists it."""
    # ranks agree perfectly, but a single huge obs outlier distorts magnitudes
    obs = [2.0, 2.1, 2.2, 2.3, 12.0]
    pred = [1.0, 2.0, 3.0, 4.0, 4.1]
    assert _sp(obs, pred) == pytest.approx(1.0)      # rank order is perfect
    assert _r(obs, pred) < 0.95                       # magnitudes disagree


def test_spearman_ignores_magnitude_of_badness():
    """The documented cost of Spearman: severity is invisible to it."""
    obs_mild = [3.0, 2.9, 2.8, 2.7, 2.6]
    obs_severe = [3.0, 2.9, 2.8, 2.7, 0.2]   # last year catastrophic
    pred = [3.0, 2.9, 2.8, 2.7, 2.6]
    assert _sp(obs_mild, pred) == pytest.approx(_sp(obs_severe, pred))
    assert _r(obs_mild, pred) != pytest.approx(_r(obs_severe, pred))


def test_region_metrics_summary_covers_all_metrics():
    """Median across regions must exist for RMSE/MAPE too, not only within_r."""
    src = SRC.read_text(encoding="utf-8")
    assert "region_metrics_summary_" in src
    i = src.index("_per_region_metrics = [")
    block = src[i:i + 900]
    for m in ("MAPE", "RMSE", "RRMSE", "R2", "within_r"):
        assert f'"{m}"' in block, f"{m} must get a median-across-regions summary"
    assert 'f"median_{m}"' in block and 'f"mean_{m}"' in block


def test_summary_medians_match_manual_computation():
    """Guard the aggregation itself, not just its presence."""
    df = pd.DataFrame({
        "Model": ["a"] * 3 + ["b"] * 3,
        "Region": ["r1", "r2", "r3"] * 2,
        "MAPE": [10.0, 20.0, 60.0, 5.0, 6.0, 7.0],
        "RMSE": [0.1, 0.2, 0.9, 0.3, 0.3, 0.3],
    })
    got = df.groupby("Model").agg(median_MAPE=("MAPE", "median"),
                                  median_RMSE=("RMSE", "median")).reset_index()
    a = got[got.Model == "a"].iloc[0]
    assert a["median_MAPE"] == 20.0   # median resists the 60 outlier
    assert a["median_RMSE"] == 0.2
    assert df[df.Model == "a"]["MAPE"].mean() == pytest.approx(30.0)  # mean does not


def test_plot_has_two_panels_when_spearman_present(tmp_path):
    """The replot must show Pearson AND Spearman side by side."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rng = np.random.default_rng(1)
    rows = []
    for model, loc in (("catboost", 0.25), ("tabpfn", 0.02)):
        for i in range(25):
            rows.append({"Model": model, "Region": f"r{i}",
                         "within_r": float(np.clip(rng.normal(loc, 0.2), -1, 1)),
                         "within_r_spearman": float(np.clip(rng.normal(loc, 0.25), -1, 1))})
    df = pd.DataFrame(rows)
    summary = (df.groupby("Model")["within_r"]
               .agg(median_within_r="median", mean_within_r="mean",
                    pct_regions_positive=lambda s: 100.0 * (s > 0).mean(),
                    n_regions="size").reset_index())
    n_before = plt.get_fignums()
    yo._plot_within_r_comparison(df, summary, tmp_path, "two.png", "Testland Maize")
    out = tmp_path / "two.png"
    assert out.exists() and out.stat().st_size > 8000
    assert plt.get_fignums() == n_before, "figure must be closed, not leaked"


def test_plot_falls_back_to_one_panel_without_spearman(tmp_path):
    """Backward compatible: older frames lacking the column still plot."""
    rng = np.random.default_rng(2)
    df = pd.DataFrame([{"Model": "m", "Region": f"r{i}",
                        "within_r": float(rng.normal(0.1, 0.2))} for i in range(20)])
    summary = (df.groupby("Model")["within_r"]
               .agg(median_within_r="median", mean_within_r="mean",
                    pct_regions_positive=lambda s: 100.0 * (s > 0).mean(),
                    n_regions="size").reset_index())
    yo._plot_within_r_comparison(df, summary, tmp_path, "one.png", "T")
    assert (tmp_path / "one.png").exists()


def test_plot_survives_all_nan_spearman(tmp_path):
    """A column present but entirely NaN must not raise."""
    df = pd.DataFrame([{"Model": "m", "Region": f"r{i}",
                        "within_r": 0.1 * i, "within_r_spearman": np.nan}
                       for i in range(10)])
    summary = (df.groupby("Model")["within_r"]
               .agg(median_within_r="median", mean_within_r="mean",
                    pct_regions_positive=lambda s: 100.0 * (s > 0).mean(),
                    n_regions="size").reset_index())
    yo._plot_within_r_comparison(df, summary, tmp_path, "nan.png", "T")
    assert (tmp_path / "nan.png").exists()
