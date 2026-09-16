"""Wiring tests for model='tabicl_gsa' (TabICL as GSA's local estimator).

tabicl and tabpfn-gsa are optional deps, so these never import them. They
cover what geocif owns: the sklearn surface, the GSA function-backend wiring,
the n_estimators key-collision guard across the three *_gsa arms, and the CI
contract (tabicl_gsa must be conformal-wrapped, unlike plain tabicl).
"""
import inspect
import re
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.ml.trainers import (
    TabICLGSARegressor,
    _tabicl_gsa_fit_fn,
    _tabicl_gsa_predict_fn,
    auto_train,
)

ROOT = Path(__file__).resolve().parents[1] / "geocif"
TRAINERS = (ROOT / "ml" / "trainers.py").read_text(encoding="utf-8")
GEOCIF = (ROOT / "geocif.py").read_text(encoding="utf-8")


def test_sklearn_surface():
    m = TabICLGSARegressor(K=16, s=0.2, n_estimators=4, seed=7)
    assert hasattr(m, "fit") and hasattr(m, "predict")
    p = m.get_params()
    assert p["K"] == 16 and p["s"] == 0.2 and p["n_estimators"] == 4 and p["seed"] == 7
    m.set_params(K=25)
    assert m.get_params()["K"] == 25


def test_defaults_match_the_other_gsa_arms():
    """Grid geometry must match tabpfn_gsa/tabfm_gsa or the arms aren't comparable."""
    p = TabICLGSARegressor().get_params()
    assert p["K"] == 64 and p["s"] == 0.1 and p["device"] == "auto"
    assert p["n_estimators"] == 8


def test_hooks_are_module_level_picklable():
    """GSAModel pickles fit_fn/predict_fn into pool workers; closures break."""
    for fn in (_tabicl_gsa_fit_fn, _tabicl_gsa_predict_fn):
        assert fn.__qualname__ == fn.__name__, f"{fn.__name__} must be module-level"


def test_fit_fn_signature_carries_tabicl_preprocessing():
    sig = inspect.signature(_tabicl_gsa_fit_fn).parameters
    for k in ("n_estimators", "device", "seed", "norm_methods", "outlier_threshold"):
        assert k in sig, f"fit hook missing {k}"
    body = TRAINERS.split("def _tabicl_gsa_fit_fn")[1].split("def _tabicl_gsa_predict_fn")[0]
    # mirrors the plain 'tabicl' branch so the arms differ only in the sampler
    assert '"none", "power", "quantile", "robust"' in body
    assert "TabICLRegressor(" in body


def test_no_object_cast_unlike_tabfm():
    """TabICL accepts pandas category dtype directly; casting to object would
    be a silent behaviour difference from the plain 'tabicl' branch."""
    body = TRAINERS.split("def _tabicl_gsa_fit_fn")[1].split("class TabICLGSARegressor")[0]
    assert "_tabfm_cast_category_to_object" not in body


def test_branch_exists_and_requires_coords():
    assert 'elif model_name == "tabicl_gsa":' in TRAINERS
    assert 'PyGRFRegressor._require_coords(X, model_label="tabicl_gsa")' in TRAINERS
    assert "model = TabICLGSARegressor(seed=int(seed), **gsa)" in TRAINERS


def test_coords_filled_at_fit_time():
    """GSAModel stores X and reuses those coords when building the predict
    grid, so NaN coords must be filled at fit, not only at predict."""
    body = TRAINERS.split("class TabICLGSARegressor")[1]
    fit = body.split("def fit")[1].split("def predict")[0]
    assert "self._coord_mean" in fit and "_fill_nan_coords" in fit


def test_n_estimators_key_cannot_leak_between_gsa_arms():
    """tabfm_gsa_n_estimators and tabicl_gsa_n_estimators share gsa_params.
    Each branch must take its own and pop the other, or one arm silently
    inherits the other's ensemble width."""
    assert 'self.gsa_params["tabicl_n_estimators"]' in GEOCIF
    assert "tabicl_gsa_n_estimators" in GEOCIF
    for arm in ("TabPFNGSARegressor", "TabFMGSARegressor"):
        seg = TRAINERS.split(f"model = {arm}(seed=int(seed), **gsa)")[0]
        tail = seg[-400:]
        assert 'gsa.pop("tabicl_n_estimators", None)' in tail, (
            f"{arm} branch must drop the tabicl key or it TypeErrors"
        )
    icl = TRAINERS.split('elif model_name == "tabicl_gsa":')[1].split("elif model_name")[0]
    assert 'gsa.pop("tabicl_n_estimators")' in icl and '"n_estimators"' in icl


def _build(gsa_params):
    """Run the real auto_train dispatch and dig out the TabICLGSARegressor.

    Constructing the class does NOT import tabicl (only .fit does), so this
    exercises the actual branch logic instead of a copy of it -- which is the
    whole point: the previous string-grep test passed while the n_estimators
    leak was live.
    """
    X = pd.DataFrame(np.zeros((6, 3)), columns=["lat", "lon", "f"])
    y = pd.Series(np.arange(6, dtype=float))
    _, m = auto_train(
        cluster_strategy="single", model_name="tabicl_gsa",
        model_type="REGRESSION", use_loocv=False, loocv_var=None,
        df_train=X, X_train=X, y_train=y, feature_names=list(X.columns),
        target_col="y", gsa_params=gsa_params,
    )
    while not isinstance(m, TabICLGSARegressor):
        nxt = getattr(m, "estimator", None) or getattr(m, "learner", None)
        assert nxt is not None, f"could not unwrap {type(m).__name__}"
        m = nxt
    return m


def test_tabfm_width_does_not_leak_into_tabicl_gsa():
    """BEHAVIOURAL. tabfm_gsa_n_estimators arrives under the plain
    "n_estimators" key. With no tabicl key set, tabicl_gsa must fall back to
    its OWN default of 8 -- not silently adopt tabfm's width (which would
    change predictions and multiply GPU prefill cost)."""
    assert _build({"n_estimators": 32}).get_params()["n_estimators"] == 8


def test_tabicl_gsa_takes_its_own_width_when_set():
    m = _build({"n_estimators": 32, "tabicl_n_estimators": 16})
    assert m.get_params()["n_estimators"] == 16


def test_default_width_is_8_with_no_config():
    assert _build(None).get_params()["n_estimators"] == 8


def test_shared_grid_geometry_still_flows_through():
    m = _build({"K": 25, "s": 0.3})
    p = m.get_params()
    assert p["K"] == 25 and p["s"] == 0.3


def test_foreign_key_is_dropped_unconditionally_in_source():
    """The leak was a one-directional guard: it renamed its own key but never
    dropped the foreign one. Assert the unconditional pop is present."""
    icl = TRAINERS.split('elif model_name == "tabicl_gsa":')[1].split("elif model_name")[0]
    assert 'gsa.pop("n_estimators", None)' in icl


def test_registered_in_every_dispatch_guard():
    """Each of these guards already lists BOTH sibling *_gsa arms; omitting
    tabicl_gsa gives it a silently different code path. The include_lat_lon one
    is the dangerous case -- without it every region's fit raises inside
    loop_ml's per-region catch and a whole multi-hour run stores zero
    predictions while reporting success.

    Matched on whitespace-collapsed source so reformatting the tuples does not
    break these, but a missing name still does.
    """
    flat = re.sub(r"\s+", " ", GEOCIF)
    for needle, what in (
        ('not in ("pygrf", "tabpfn_gsa", "tabfm_gsa", "tabicl_gsa"): return',
         "centroid-degeneracy detector"),
        ('in ("pygrf", "tabpfn_gsa", "tabfm_gsa", "tabicl_gsa") and not self.include_lat_lon_as_feature',
         "include_lat_lon_as_feature fail-fast guard"),
        ('"tabfm_gsa", "tabicl_gsa", "mitra"',
         "tabular-flags dispatch list"),
        ('do_xai and self.dispatch_name in ("tabpfn_gsa", "tabfm_gsa", "tabicl_gsa")',
         "GSA XAI disable guard"),
    ):
        assert needle in flat, f"tabicl_gsa missing from the {what}"


def test_fitter_is_tabicl_not_tabpfn():
    """TabICL needs sklearn transform_output pinned -- that is the entire
    reason TabICLFitter exists. TabPFNFitter/DefaultFitter would drop it."""
    assert '"tabicl_gsa": TabICLFitter(self.obj),' in GEOCIF


def test_local_fit_hook_pins_transform_output():
    """The outer fitter's pin is process-global and does NOT reach GSAModel's
    pool workers, so the hook must pin and restore too."""
    body = TRAINERS.split("def _tabicl_gsa_fit_fn")[1].split("def _tabicl_gsa_predict_fn")[0]
    assert 'sklearn.set_config(transform_output="default")' in body
    assert "finally:" in body and "sklearn.set_config(transform_output=prev)" in body


def test_tabicl_gsa_is_conformal_wrapped_unlike_plain_tabicl():
    """GSA's function backend returns point predictions only, so tabicl_gsa
    must NOT be in the unwrapped list even though plain tabicl is."""
    block = TRAINERS.split('"ngboost", "tabpfn", "tabpfn_ft"')[1][:220]
    assert '"tabicl"' in block, "plain tabicl should still be unwrapped"
    assert '"tabicl_gsa"' not in block, (
        "tabicl_gsa has no native quantiles - it must get the conformal wrapper"
    )
