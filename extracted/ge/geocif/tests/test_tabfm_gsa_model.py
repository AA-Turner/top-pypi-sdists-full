"""Wiring tests for the TabFM-GSA model (model='tabfm_gsa').

GSA spatial context sampler (ruid7181/TabPFN-GSA) with Google Research's
TabFM as the local in-context estimator, plugged in through GSAModel's
fit_fn/predict_fn function backend. Shares [ML] tabpfn_gsa_K / tabpfn_gsa_s
with tabpfn_gsa; adds [ML] tabfm_gsa_n_estimators (TabFM inner-ensemble
width, default 8). tabfm and tabpfn-gsa are optional deps, so the tests
here avoid importing them (fit is lazy); heavy roundtrips run on the
cluster GPU nodes, not in CI.
"""
import inspect
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from geocif.ml.trainers import (
    TabFMGSARegressor,
    TabPFNGSARegressor,
    _tabfm_cast_category_to_object,
    _tabfm_gsa_fit_fn,
    _tabfm_gsa_predict_fn,
    auto_train,
)

ROOT = Path(__file__).resolve().parents[1] / "geocif"


def test_tabfm_gsa_sklearn_api():
    m = TabFMGSARegressor(K=25, s=0.2, n_estimators=4)
    assert hasattr(m, "fit") and hasattr(m, "predict")
    p = m.get_params()
    assert p["K"] == 25 and p["s"] == 0.2 and p["n_estimators"] == 4
    m.set_params(s=0.0, n_estimators=8)
    assert m.get_params()["s"] == 0.0
    assert m.get_params()["n_estimators"] == 8


def test_tabfm_gsa_missing_dep_messages():
    """fit() must fail loudly naming the missing optional dep."""
    m = TabFMGSARegressor()
    X = pd.DataFrame({"a": [1.0], "lat": [0.0], "lon": [0.0]})
    try:
        import tabpfn_gsa  # noqa: F401
    except ImportError:
        with pytest.raises(ImportError, match="TabPFN-GSA.git"):
            m.fit(X, [1.0])
        return
    try:
        import tabfm  # noqa: F401
    except ImportError:
        with pytest.raises(ImportError, match="pip install tabfm"):
            m.fit(X, [1.0])
        return
    pytest.skip("both optional deps installed; missing-dep paths unreachable")


def test_tabfm_gsa_hooks_are_module_level():
    """The fit/predict hooks must be module-level functions (not closures)
    so GSAModel instances survive pickling into pool workers."""
    for fn in (_tabfm_gsa_fit_fn, _tabfm_gsa_predict_fn):
        assert fn.__qualname__ == fn.__name__, "must not be a closure/method"
    assert "n_estimators" in inspect.signature(_tabfm_gsa_fit_fn).parameters
    assert "device" in inspect.signature(_tabfm_gsa_fit_fn).parameters
    assert "seed" in inspect.signature(_tabfm_gsa_fit_fn).parameters


def test_tabfm_cast_category_to_object():
    """TabFM's tokenizer misreads CategoricalDtype as numeric codes —
    the hooks must cast category columns back to object, copy-safely."""
    X = pd.DataFrame({
        "Region": pd.Categorical(["a", "b", "a"]),
        "x": [1.0, 2.0, 3.0],
    })
    out = _tabfm_cast_category_to_object(X)
    assert out["Region"].dtype == object
    assert out["x"].dtype == float
    assert isinstance(X["Region"].dtype, pd.CategoricalDtype)  # original untouched


def test_tabfm_gsa_nan_coords_reuse_tabpfn_gsa_fill():
    """Same silent-grid-collapse hazard as tabpfn_gsa: NaN coords must be
    fillable with the train-mean location before GSAModel stores X."""
    X = pd.DataFrame({
        "a": [1.0, 2.0, 3.0, 4.0],
        "lat": [0.0, np.nan, 2.0, 4.0],
        "lon": [30.0, 32.0, np.nan, 34.0],
    })
    coord_mean = np.nanmean(X[["lat", "lon"]].to_numpy(dtype=float), axis=0)
    filled = TabPFNGSARegressor._fill_nan_coords(X, coord_mean)
    assert not filled[["lat", "lon"]].isna().to_numpy().any()
    assert X["lat"].isna().sum() == 1  # original untouched


def test_auto_train_tabfm_gsa_branch():
    src = inspect.getsource(auto_train)
    assert 'model_name == "tabfm_gsa"' in src
    # tabpfn_gsa branch must tolerate the tabfm-only n_estimators key so
    # both models can run from one config sharing gsa_params
    assert 'gsa.pop("n_estimators", None)' in src


def test_wrapper_prefix_regex_leaves_tabfm_gsa_alone():
    name = "tabfm_gsa"
    assert not name.startswith(("curated_", "auto_"))
    assert re.match(r"^top\d+_(.+)$", name) is None


def test_geocif_wiring_for_tabfm_gsa():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    # tabular flags dispatch
    assert '"tabpfn_gsa", "tabfm_gsa"]' in src
    # fitter map
    assert '"tabfm_gsa": TabPFNFitter(self.obj)' in src
    # lat/lon requirement gate + coord-degeneracy warning cover tabfm_gsa
    assert '("pygrf", "tabpfn_gsa", "tabfm_gsa")' in src
    # inner-ensemble width config key
    assert "tabfm_gsa_n_estimators" in src
    # XAI force-off covers tabfm_gsa
    assert 'self.dispatch_name in ("tabpfn_gsa", "tabfm_gsa")' in src
