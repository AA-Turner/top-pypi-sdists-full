"""Regression tests for the correlation-plot caching in Geocif.

Guards against the "same PNG written under every model dir" regression:
the correlation compute is model-agnostic, so subsequent model workers
should hit a disk cache and skip both the compute and plot render. Also
verifies the plot output dir no longer includes self.model_name.
"""

from pathlib import Path
import pandas as pd

from geocif import geocif as geocif_mod


def _make_stub_geocif(tmp_path: Path, model_name: str = "catboost"):
    """Build a minimally-initialised Geocif with just the attributes the
    correlation-cache helpers touch. Avoids the full dataclass init."""
    obj = geocif_mod.Geocif.__new__(geocif_mod.Geocif)
    obj.country = "brazil"
    obj.crop = "soybean"
    obj.model_name = model_name
    obj.forecast_season = 2026
    obj.dir_analysis = tmp_path / "ml" / "analysis" / "Jul_07"
    obj.dir_analysis.mkdir(parents=True, exist_ok=True)
    obj.simulation_stages = [("10", "11", "12")]
    obj.correlation_plots = True
    obj.target = "Yield (tn per ha)"
    obj.all_stages = []
    obj.method = "monthly_r"
    obj.national_correlation = False
    obj.correlation_plot_groupby = "Region_ID"
    obj.cluster_strategy = "single"
    obj.dg_country = None
    obj.combined_dict = {}
    obj.plot_map_for_correlation_plot = False
    obj.correlation_threshold = 0.0
    obj.correlation_metric = "both"
    obj.plot_correlation_scatter = False

    class _StubLogger:
        def info(self, *a, **k): pass
        def warning(self, *a, **k): pass
    obj.logger = _StubLogger()
    return obj


def test_correlation_dir_output_omits_model_name(tmp_path):
    """dir_output must NOT include model_name — otherwise the same PNG
    gets written 5 times under catboost/, cubist/, tabpfn/, trend/, null/."""
    obj_a = _make_stub_geocif(tmp_path, model_name="catboost")
    obj_b = _make_stub_geocif(tmp_path, model_name="tabpfn")

    kwargs_a = obj_a._build_correlation_kwargs()
    kwargs_b = obj_b._build_correlation_kwargs()

    assert kwargs_a["dir_output"] == kwargs_b["dir_output"], (
        f"Different model_name produced different dir_output: "
        f"{kwargs_a['dir_output']} != {kwargs_b['dir_output']}"
    )
    assert "catboost" not in str(kwargs_a["dir_output"])
    assert "tabpfn" not in str(kwargs_a["dir_output"])
    assert str(obj_a.forecast_season) in str(kwargs_a["dir_output"])


def test_correlation_cache_roundtrip(tmp_path):
    """Save then load must return the same tuple."""
    obj = _make_stub_geocif(tmp_path)
    cache_path = obj._correlation_cache_path(tmp_path)

    payload = (
        {1: pd.DataFrame({"CID": ["A", "B"], "Median": [0.4, 0.7]})},
        {1: {"NDVI": "MEAN_NDVI Jan"}},
    )
    obj._save_correlation_cache(cache_path, payload)
    assert cache_path.exists()

    loaded = obj._load_correlation_cache(cache_path)
    assert loaded is not None
    assert set(loaded[0].keys()) == {1}
    assert loaded[1] == payload[1]
    pd.testing.assert_frame_equal(loaded[0][1], payload[0][1])


def test_correlation_cache_hit_short_circuits(tmp_path, monkeypatch):
    """Second model with the same (country, crop, season, stages) must NOT
    call all_correlated_feature_by_time — the cache short-circuits."""
    obj_first = _make_stub_geocif(tmp_path, model_name="catboost")
    obj_second = _make_stub_geocif(tmp_path, model_name="tabpfn")

    computed = {"count": 0}
    expected = (
        {1: pd.DataFrame({"CID": ["X"], "Median": [0.9]})},
        {1: {"NDVI": "MEAN_NDVI Feb"}},
    )

    def _fake_all(df, **kwargs):
        computed["count"] += 1
        return expected

    monkeypatch.setattr(
        geocif_mod.correlations, "all_correlated_feature_by_time", _fake_all
    )

    r1 = obj_first._generate_correlation_plots(pd.DataFrame({"a": [1, 2]}))
    assert computed["count"] == 1
    r2 = obj_second._generate_correlation_plots(pd.DataFrame({"a": [1, 2]}))
    assert computed["count"] == 1, (
        "Second model recomputed correlations — cache miss regression"
    )
    assert r2[1] == r1[1]


def test_correlation_disabled_returns_empty(tmp_path):
    """correlation_plots=False must short-circuit without touching disk."""
    obj = _make_stub_geocif(tmp_path)
    obj.correlation_plots = False
    result = obj._generate_correlation_plots(pd.DataFrame({"a": [1]}))
    assert result == ({}, {})


def test_cache_key_differs_by_simulation_stages(tmp_path):
    """Different simulation_stages must produce different cache paths so
    multi-step / pre-season pipelines don't corrupt each other's cache."""
    obj_a = _make_stub_geocif(tmp_path)
    obj_a.simulation_stages = [("10", "11")]
    obj_b = _make_stub_geocif(tmp_path)
    obj_b.simulation_stages = [("10", "11", "12")]

    dir_out = tmp_path / "out"
    path_a = obj_a._correlation_cache_path(dir_out)
    path_b = obj_b._correlation_cache_path(dir_out)
    assert path_a != path_b, "Same cache path for different simulation_stages"
