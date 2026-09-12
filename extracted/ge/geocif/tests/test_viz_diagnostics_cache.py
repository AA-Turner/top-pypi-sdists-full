"""Regression tests for two diagnostics.py bugs fixed together.

1. ``cid_vs_yield_scatters`` used to return early when ANY PNG already
   existed in out_dir. But the same function writes pearson_summary.csv /
   pearson_corr_matrix.csv — model-selection INPUTS read by
   ``utils.auto_select_cids`` and the top_n_ models — so those CSVs
   silently went stale whenever data or config changed while old PNGs sat
   on disk. The fix: the Pearson statistics are recomputed and the two
   CSVs rewritten on EVERY call; only the slow figure rendering (and the
   per-CID CSVs paired with those figures) is skipped when PNGs exist.

2. ``mape_choropleth`` / ``metric_choropleth`` accepted an
   ``annotate_regions`` parameter but hardcoded ``annotate_regions=True,
   annotate_values=True`` in their plot_map calls, silently discarding
   ``annotate_regions=False`` from callers (e.g. classification_outputs).
   The fix forwards the caller's flag to both kwargs.
"""
import sys
import types

import matplotlib

matplotlib.use("Agg")  # headless — rendering tests must not need a display

import matplotlib.figure
import numpy as np
import pandas as pd
import pytest

# ``geocif.viz.plot`` is imported inside the choropleth functions; it needs
# no heavy geo deps at import time (cartopy/pygeoutil are lazy), but stub
# pygeoutil defensively so the tests run in any environment (same pattern
# as tests/test_outlook_metric_maps.py).
try:  # pragma: no cover - environment dependent
    import pygeoutil  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover
    _pg = types.ModuleType("pygeoutil")
    _rgeo = types.ModuleType("pygeoutil.rgeo")
    _rgeo.get_country_lat_lon_extent = lambda *a, **k: [-180, 180, -90, 90]
    _pg.rgeo = _rgeo
    sys.modules["pygeoutil"] = _pg
    sys.modules["pygeoutil.rgeo"] = _rgeo

from geocif.viz import diagnostics

TARGET = "Yield (tn per ha)"


def _synthetic_df(gdd_sign=1.0):
    """Two regions x ten years; GDD is exactly ±linear in yield (Pearson
    r = ±1 pooled), PRCPTOT is close-to-linear so the dedup step has a
    highly-correlated pair to prune."""
    years = np.arange(2000, 2010, dtype=float)
    base_yield = np.array([2.1, 2.5, 1.9, 3.0, 2.7, 2.2, 3.3, 2.9, 2.4, 3.1])
    frames = []
    for i, region in enumerate(["north", "south"]):
        y = base_yield + 0.3 * i
        frames.append(pd.DataFrame({
            "Region": region,
            "Harvest Year": years,
            TARGET: y,
            "GDD Apr 1-Nov 30": gdd_sign * (100.0 * y) + 5.0,
            "PRCPTOT Apr 1-Nov 30": 400.0 - 50.0 * y + np.linspace(0.0, 3.0, len(y)),
        }))
    return pd.concat(frames, ignore_index=True)


class TestPearsonCsvsAlwaysRefresh:
    """Bug 1: stats CSVs must track the CURRENT data even when PNGs exist."""

    def test_stale_pngs_do_not_freeze_pearson_summary(self, tmp_path, monkeypatch):
        out_dir = tmp_path / "eda" / "kenya" / "maize"
        csv_dir = out_dir / "csvs"
        csv_dir.mkdir(parents=True)
        # Simulate a previous run: a cached figure + a stale summary CSV.
        (out_dir / "GDD.png").write_bytes(b"")
        (csv_dir / "pearson_summary.csv").write_text(
            "cid,n,pearson_r\nSTALE,1,0.0\n"
        )

        # Any figure render would call Figure.savefig — ban it to PROVE the
        # slow path is skipped while the stats path still runs.
        def _no_render(*a, **k):  # pragma: no cover - failure path
            raise AssertionError("figure rendering must be skipped when PNGs exist")
        monkeypatch.setattr(matplotlib.figure.Figure, "savefig", _no_render)

        # NEW data: GDD correlation flipped negative vs whatever ran before.
        n = diagnostics.cid_vs_yield_scatters(
            _synthetic_df(gdd_sign=-1.0), TARGET, tmp_path / "eda",
            "kenya", "maize",
        )

        assert n == 0  # figures skipped -> nothing "plotted"
        # No figure files appeared (scatters, by_region, pearson_summary.png).
        assert sorted(p.name for p in out_dir.glob("*.png")) == ["GDD.png"]
        # Per-CID CSVs are paired with the (skipped) figures — not rewritten.
        assert not (csv_dir / "GDD.csv").exists()

        # THE fix: pearson_summary.csv reflects the new data, not the cache.
        summary = pd.read_csv(csv_dir / "pearson_summary.csv")
        assert "STALE" not in set(summary["cid"])
        assert set(summary["cid"]) == {"GDD", "PRCPTOT"}
        gdd_r = float(summary.loc[summary["cid"] == "GDD", "pearson_r"].iloc[0])
        assert gdd_r == pytest.approx(-1.0, abs=1e-6)
        # Dedup columns (read by the top_n_ models) are present too.
        assert {"kept", "redundant_with", "mutual_r"} <= set(summary.columns)
        # ... and the pairwise matrix companion is (re)written as well.
        assert (csv_dir / "pearson_corr_matrix.csv").exists()

    def test_fresh_dir_writes_both_csvs_and_figures(self, tmp_path):
        n = diagnostics.cid_vs_yield_scatters(
            _synthetic_df(gdd_sign=1.0), TARGET, tmp_path / "eda",
            "kenya", "maize",
        )
        out_dir = tmp_path / "eda" / "kenya" / "maize"
        csv_dir = out_dir / "csvs"

        assert n == 2  # GDD + PRCPTOT
        pngs = {p.name for p in out_dir.glob("*.png")}
        assert {"GDD.png", "GDD_by_region.png",
                "PRCPTOT.png", "PRCPTOT_by_region.png",
                "pearson_summary.png"} <= pngs
        # Plot-CSV pairing rule: each scatter has its companion CSV.
        assert (csv_dir / "GDD.csv").exists()
        assert (csv_dir / "PRCPTOT.csv").exists()

        summary = pd.read_csv(csv_dir / "pearson_summary.csv")
        gdd_r = float(summary.loc[summary["cid"] == "GDD", "pearson_r"].iloc[0])
        assert gdd_r == pytest.approx(1.0, abs=1e-6)
        corr = pd.read_csv(csv_dir / "pearson_corr_matrix.csv", index_col=0)
        assert set(corr.columns) == {"GDD", "PRCPTOT"}


class TestChoroplethAnnotateForwarding:
    """Bug 2: annotate_regions must be forwarded to plot_map, not hardcoded."""

    @staticmethod
    def _capture_plot_map(monkeypatch):
        from geocif.viz import plot
        captured = {}
        monkeypatch.setattr(plot, "plot_map",
                            lambda *a, **k: captured.update(k))
        return captured

    def test_mape_choropleth_forwards_false(self, tmp_path, monkeypatch):
        captured = self._capture_plot_map(monkeypatch)
        df = pd.DataFrame({
            "Country Region": ["kenya nakuru", "kenya meru"],
            "Mean Absolute Percentage Error": [10.0, 20.0],
        })
        diagnostics.mape_choropleth(None, df, ["Kenya"], False,
                                    tmp_path, "mape.png")
        assert captured["annotate_regions"] is False
        assert captured["annotate_values"] is False  # values follow names

    def test_mape_choropleth_forwards_true(self, tmp_path, monkeypatch):
        captured = self._capture_plot_map(monkeypatch)
        df = pd.DataFrame({
            "Country Region": ["kenya nakuru", "kenya meru"],
            "Mean Absolute Percentage Error": [10.0, 20.0],
        })
        diagnostics.mape_choropleth(None, df, ["Kenya"], True,
                                    tmp_path, "mape.png")
        assert captured["annotate_regions"] is True
        assert captured["annotate_values"] is True

    def test_metric_choropleth_forwards_false(self, tmp_path, monkeypatch):
        captured = self._capture_plot_map(monkeypatch)
        df = pd.DataFrame({
            "Country Region": ["kenya nakuru", "kenya meru"],
            "RMSE": [0.4, 0.6],
        })
        diagnostics.metric_choropleth(None, df, ["Kenya"], False,
                                      tmp_path, "rmse.png",
                                      col="RMSE", label="RMSE")
        assert captured["annotate_regions"] is False
        assert captured["annotate_values"] is False
