"""Regression tests for the TabPFN-GSA model wiring.

TabPFN-GSA (ruid7181/TabPFN-GSA) is a selectable pipeline model
(model='tabpfn_gsa') via the TabPFNGSARegressor wrapper: lat/lon feature
columns become GSAModel's spa_cols, everything else is x_cols, K is rounded
to a perfect square, and ignore_pretraining_limits=True mirrors the plain
tabpfn branch. Routed through the tabular flags and TabPFNFitter.
tabpfn-gsa is a git-only optional dep, so wrapper-mechanics tests avoid
importing it; the roundtrip skips when it (or the TabPFN checkpoint) is
unavailable.
"""
import inspect
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from geocif.ml.trainers import TabPFNGSARegressor, auto_train

ROOT = Path(__file__).resolve().parents[1] / "geocif"


def test_gsa_sklearn_api():
    m = TabPFNGSARegressor(K=25, s=0.2)
    assert hasattr(m, "fit") and hasattr(m, "predict")
    p = m.get_params()
    assert p["K"] == 25 and p["s"] == 0.2
    m.set_params(s=0.0)
    assert m.get_params()["s"] == 0.0


def test_gsa_requires_lat_lon():
    pytest.importorskip("tabpfn_gsa")
    m = TabPFNGSARegressor()
    X = pd.DataFrame({"a": [1.0, 2, 3]})
    with pytest.raises(ValueError, match="include_lat_lon_as_feature"):
        m.fit(X, [1.0, 2.0, 3.0])


def test_gsa_missing_dep_message():
    try:
        import tabpfn_gsa  # noqa: F401
        pytest.skip("tabpfn_gsa installed; missing-dep path not reachable")
    except ImportError:
        pass
    m = TabPFNGSARegressor()
    X = pd.DataFrame({"a": [1.0], "lat": [0.0], "lon": [0.0]})
    with pytest.raises(ImportError, match="TabPFN-GSA.git"):
        m.fit(X, [1.0])


def test_gsa_fit_predict_roundtrip():
    pytest.importorskip("tabpfn_gsa")
    rng = np.random.default_rng(0)
    n = 40
    X = pd.DataFrame({
        "a": rng.normal(size=n),
        "b": rng.normal(size=n),
        "lat": rng.uniform(-4, 4, n),
        "lon": rng.uniform(34, 42, n),
    })
    y = 2.0 * X["a"] + 0.1 * X["lat"] + rng.normal(scale=0.1, size=n)
    m = TabPFNGSARegressor(K=10, s=0.1, device="cpu", seed=0)  # K -> 9 (3x3)
    try:
        m.fit(X, y)
    except Exception as exc:  # e.g. TabPFN checkpoint not downloadable here
        pytest.skip(f"TabPFN backend unavailable: {exc}")
    assert m._m.K == 9, "K must be rounded to a perfect square"
    pred = m.predict(X)
    assert pred.shape == (n,)
    assert np.all(np.isfinite(pred))
    assert np.corrcoef(pred, y)[0, 1] > 0.7


def test_gsa_nan_coords_filled_at_fit_and_predict():
    """Review finding (major): one NaN lat/lon makes tabpfn_gsa's grid
    mins/spans NaN and silently collapses every row's cell index to 0 —
    the wrapper must fill NaN coords with the train-mean location BEFORE
    GSAModel stores X internally."""
    m = TabPFNGSARegressor()
    X = pd.DataFrame({
        "a": [1.0, 2.0, 3.0, 4.0],
        "lat": [0.0, np.nan, 2.0, 4.0],
        "lon": [30.0, 32.0, np.nan, 34.0],
    })
    coord_mean = np.nanmean(X[["lat", "lon"]].to_numpy(dtype=float), axis=0)
    filled = m._fill_nan_coords(X, coord_mean)
    assert not filled[["lat", "lon"]].isna().to_numpy().any()
    assert filled.loc[1, "lat"] == pytest.approx(2.0)   # mean of 0,2,4
    assert filled.loc[2, "lon"] == pytest.approx(32.0)  # mean of 30,32,34
    # original frame untouched (copy-on-write semantics)
    assert X["lat"].isna().sum() == 1
    # fit path stores the mean and hands GSAModel a NaN-free frame
    pytest.importorskip("tabpfn_gsa")
    y = pd.Series([1.0, 2.0, 3.0, 4.0])
    try:
        m.fit(X, y)
    except Exception as exc:
        pytest.skip(f"TabPFN backend unavailable: {exc}")
    assert np.all(np.isfinite(m._coord_mean))
    stored = getattr(m._m, "X_train_", None)
    if stored is not None:
        assert not stored[["lat", "lon"]].isna().to_numpy().any()
    assert np.all(np.isfinite(m.predict(X)))


def test_gsa_declares_categorical_indices():
    """tabpfn_gsa must tell the backend TabPFN which columns are categorical,
    exactly as the plain `tabpfn` branch does.

    Without it, tabpfn treats string columns as suspected FREE TEXT and warns
    they "usually add noise rather than signal" -- minor for admin_1 Region
    (~39 states) but material at admin_2 (~919 counties), and it made the
    tabpfn_gsa-vs-tabpfn comparison unfair since only tabpfn got the hint.

    Index space matters: GSAModel fits on model_columns_ = [*x_cols, *spa_cols],
    so the indices must be relative to x_cols (lat/lon appended last).
    """
    pytest.importorskip("tabpfn_gsa")
    rng = np.random.default_rng(0)
    n = 30
    X = pd.DataFrame({
        "a": rng.normal(size=n),
        "Region": pd.Categorical([f"c{i % 7}" for i in range(n)]),
        "lat": rng.uniform(38, 44, n),
        "b": rng.normal(size=n),
        "State": [f"s{i % 3}" for i in range(n)],
        "lon": rng.uniform(-98, -88, n),
    })
    y = pd.Series(2.0 * X["a"] + rng.normal(scale=0.1, size=n))

    m = TabPFNGSARegressor(K=4, s=0.1, device="cpu", seed=0)
    try:
        m.fit(X, y)
    except Exception as exc:
        pytest.skip(f"TabPFN backend unavailable: {exc}")

    x_cols = [c for c in X.columns if c not in ("lat", "lon")]
    expected = [i for i, c in enumerate(x_cols)
                if hasattr(X[c], "cat") or pd.api.types.is_string_dtype(X[c])]
    got = m._m.model_kwargs.get("categorical_features_indices")
    assert got == expected, f"{got} != {expected}"

    # the indices must resolve to the categorical names in GSA's own column space
    mc = list(m._m.model_columns_)
    assert [mc[i] for i in got] == ["Region", "State"]
    # and lat/lon must NOT be flagged categorical
    assert not {mc[i] for i in got} & {"lat", "lon"}


def test_auto_train_gsa_branch():
    assert "gsa_params" in inspect.signature(auto_train).parameters
    src = inspect.getsource(auto_train)
    assert 'model_name == "tabpfn_gsa"' in src


def test_wrapper_prefix_regex_leaves_tabpfn_gsa_alone():
    """The curated_/auto_/top<N>_ strip in auto_train must NOT reroute
    'tabpfn_gsa' to another branch (it strips prefixes only)."""
    import re
    name = "tabpfn_gsa"
    assert not name.startswith(("curated_", "auto_"))
    assert re.match(r"^top\d+_(.+)$", name) is None


def test_geocif_wiring_for_tabpfn_gsa():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    assert '"exaone", "tabpfn_gsa"]' in src  # tabular flags dispatch
    assert '"tabpfn_gsa": TabPFNFitter(self.obj)' in src
    assert "self.gsa_params" in src
    assert "tabpfn_gsa_K" in src and "tabpfn_gsa_s" in src
    assert 'gsa_params=getattr(self.obj, "gsa_params"' in src
    # do_xai has no explainer path for GSAModel — must be forced off with a
    # warning inside _setup_tabular_flags (review finding)
    assert 'self.dispatch_name == "tabpfn_gsa"' in src
    assert "disabling XAI for this model" in src
