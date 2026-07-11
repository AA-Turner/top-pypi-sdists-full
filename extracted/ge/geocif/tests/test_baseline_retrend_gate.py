"""Regression test: baselines must NOT be retrended / region-anomaly re-added.

Baselines (ML_model = False: null / trend / trend_all / median / analog /
last_year) predict on the RAW ``self.target`` scale, the same scale as
``y_test`` / the stored Observed Yield. Only ML models fit on the transformed
target (detrended residual or region anomaly) and need the inverse transform.

Before the fix, ``Geocif.predict`` applied ``_retrend_predictions`` to every
model whenever ``check_yield_trend`` was on, so a raw-scale baseline got
``raw_yield + trend_value`` (roughly 2x yield) and null/trend blew up to
~90-107% MAPE while every ML model stayed correct. The fix gates the
retrend / re-add on ``self.ml_model``.

The behavioral test binds the real ``Geocif.predict`` to a light stub and
spies on ``_retrend_predictions`` so we assert it fires for ML models and is
skipped for baselines. A structural check guards the gate against regression
even where geocif's heavy deps are importable.
"""
import ast
import logging
from pathlib import Path
from types import MethodType, SimpleNamespace

import numpy as np
import pandas as pd

from geocif.geocif import Geocif


def _make_stub(ml_model):
    """Minimal surface for Geocif.predict with a spyable retrend."""
    calls = {"retrend": 0, "readd": 0}

    stub = SimpleNamespace(
        ml_model=ml_model,
        check_yield_trend=True,          # detrending active -> retrend path
        target_mode="absolute",
        _region_target_means={},
        selected_features=[],
        cat_features=[],
        target="Yield (tn per ha)",
        country="brazil",
        crop="maize",
        countries_pooled=None,
        logger=logging.getLogger("test_baseline_retrend_gate"),
        captured=SimpleNamespace(y_pred=None),
    )

    # _run_prediction returns a RAW baseline-style prediction (4.0 t/ha).
    stub._run_prediction = lambda X, dfr, sc: (np.array([4.0]), None, {})

    def _spy_retrend(y_pred, df_region, y_pred_ci):
        calls["retrend"] += 1
        return y_pred * 10.0, y_pred_ci     # obvious transform to detect

    def _spy_readd(y_pred, df_region, y_pred_ci):
        calls["readd"] += 1
        return y_pred * 10.0, y_pred_ci

    def _capture_build(df_region, X_test, y_test, y_pred, y_pred_ci,
                       best, experiment_id):
        stub.captured.y_pred = np.asarray(y_pred).copy()
        return pd.DataFrame({"y_pred": np.asarray(y_pred)})

    stub._retrend_predictions = _spy_retrend
    stub._re_add_region_mean_to_predictions = _spy_readd
    stub._build_results_dataframe = _capture_build
    stub.predict = MethodType(Geocif.predict, stub)
    return stub, calls


def _df_region():
    return pd.DataFrame({"Yield (tn per ha)": [3.5], "Region": ["A"]})


class TestBaselineRetrendGate:
    def test_baseline_not_retrended(self):
        """ML_model = False -> retrend/re-add skipped; raw prediction survives."""
        stub, calls = _make_stub(ml_model=False)
        stub.predict(_df_region())
        assert calls["retrend"] == 0
        assert calls["readd"] == 0
        assert np.allclose(stub.captured.y_pred, [4.0])   # raw, not 40.0

    def test_ml_model_still_retrended(self):
        """ML_model = True -> retrend still applied exactly as before."""
        stub, calls = _make_stub(ml_model=True)
        stub.predict(_df_region())
        assert calls["retrend"] == 1
        assert np.allclose(stub.captured.y_pred, [40.0])  # transformed


def test_predict_gates_retrend_on_ml_model_source():
    """Structural guard: in Geocif.predict the retrend / re-add block sits
    under an `if self.ml_model:` test (runs regardless of optional deps)."""
    src = (Path(__file__).resolve().parents[1]
           / "geocif" / "geocif.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    predict = next(
        n for n in ast.walk(tree)
        if isinstance(n, ast.FunctionDef) and n.name == "predict"
    )
    found = False
    for node in ast.walk(predict):
        if not isinstance(node, ast.If):
            continue
        # test is `self.ml_model`
        t = node.test
        if isinstance(t, ast.Attribute) and t.attr == "ml_model":
            calls = {
                getattr(c.func, "attr", "")
                for c in ast.walk(node) if isinstance(c, ast.Call)
            }
            if "_retrend_predictions" in calls:
                found = True
    assert found, "retrend block must be gated by `if self.ml_model:`"
