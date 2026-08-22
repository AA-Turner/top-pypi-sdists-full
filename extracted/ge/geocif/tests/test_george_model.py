"""Regression tests for the george (GP regression) model wiring.

george (dfm/george) is a selectable pipeline model (model='george') via the
sklearn-style GeorgeGPRegressor wrapper, routed like 'gpr': simple-regression
flags, StandardScaler path, GPRFitter. george itself is an optional extra
(no aarch64 wheels), so wrapper-mechanics tests avoid importing it and the
end-to-end fit/predict test skips when it isn't installed.
"""
import inspect
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from geocif.ml.trainers import GeorgeGPRegressor, auto_train

ROOT = Path(__file__).resolve().parents[1] / "geocif"


def test_george_sklearn_api():
    m = GeorgeGPRegressor(kernel="matern32", jitter=1e-2)
    assert hasattr(m, "fit") and hasattr(m, "predict")
    p = m.get_params()
    assert p["kernel"] == "matern32" and p["jitter"] == 1e-2
    m.set_params(kernel="expsquared")
    assert m.get_params()["kernel"] == "expsquared"


def test_george_numeric_encoding():
    m = GeorgeGPRegressor()
    X = pd.DataFrame({"a": [1.0, 2, 3],
                      "Region": pd.Categorical(["x", "y", "x"]),
                      "b": [np.nan, 5, 6]})
    Xn = m._numeric(X)
    assert "Region_x" in Xn.columns and "Region_y" in Xn.columns
    assert Xn.select_dtypes(include=["object", "category"]).shape[1] == 0


def test_george_missing_dep_message():
    """Without george installed, fit must raise the install-hint ImportError
    (not a bare ModuleNotFoundError deep in the stack)."""
    try:
        import george  # noqa: F401
        pytest.skip("george installed; missing-dep path not reachable")
    except ImportError:
        pass
    m = GeorgeGPRegressor()
    X = pd.DataFrame({"a": [1.0, 2, 3, 4], "b": [0.5, 1, 2, 4]})
    y = np.array([1.0, 2.0, 3.0, 4.0])
    with pytest.raises(ImportError, match="geocif\\[george\\]"):
        m.fit(X, y)


def test_george_fit_predict_roundtrip():
    george = pytest.importorskip("george")  # noqa: F841
    rng = np.random.default_rng(0)
    n, d = 60, 5
    X = rng.normal(size=(n, d))
    y = X[:, 0] * 2.0 + np.sin(X[:, 1]) + rng.normal(scale=0.1, size=n)
    m = GeorgeGPRegressor().fit(X, y)
    pred = m.predict(X)
    assert pred.shape == (n,)
    assert np.all(np.isfinite(pred))
    # exact GP interpolates its own training data reasonably well
    assert np.corrcoef(pred, y)[0, 1] > 0.9
    # ndarray predict on unseen rows works and predict_std returns pairs
    X_new = rng.normal(size=(7, d))
    mu, std = m.predict_std(X_new)
    assert mu.shape == (7,) and std.shape == (7,)
    assert np.all(std >= 0)


def test_auto_train_george_branch():
    assert "george_params" in inspect.signature(auto_train).parameters
    src = inspect.getsource(auto_train)
    assert 'model_name == "george"' in src


def test_geocif_wiring_for_george():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    # simple-regression flag routing + scaler + preprocess + fitter map
    assert '"gpr", "george"]' in src
    assert '"george": GPRFitter(self.obj)' in src
    assert "self.george_params" in src
    assert 'george_params=getattr(self.obj, "george_params"' in src
    # scaler + test-preprocess must key on dispatch_name (not model_name) so
    # curated_/top<N>_/auto_ variants get the StandardScaler consistently
    # with the dispatch-keyed fitter map (review finding)
    assert src.count('self.dispatch_name in ("linear", "gpr", "george")') == 2
    assert 'self.model_name in ("linear", "gpr", "george")' not in src
