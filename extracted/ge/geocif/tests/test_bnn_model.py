"""Regression tests for the bnn (Ma et al. 2021 Bayesian NN) model wiring.

model='bnn' is the two-headed variational BNN from Ma, Zhang, Kang & Ozdogan
(2021, RSE 259:112408), vendored in geocif/ml/bnn.py with a geocif-facing
sklearn adapter (BNNYieldRegressor). Routing: standard-ML flags, DefaultFitter
(raw DataFrame in, categoricals one-hot inside the wrapper), native predictive
sigma via Geocif._predict_bnn_with_ci (estimate_ci early-returns it unwrapped),
and held-out-newest-year sigma recalibration inside fit (two-pass: c from
years < max, final refit on all rows).

torch normally arrives transitively via the core tabpfn dep, so the fit tests
importorskip torch; structural/wiring tests run without it.
"""
import inspect
import logging
from pathlib import Path
from types import MethodType, SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from geocif.ml.trainers import auto_train

ROOT = Path(__file__).resolve().parents[1] / "geocif"


def _make_regressor(**kw):
    torch = pytest.importorskip("torch")  # noqa: F841
    from geocif.ml.bnn import BNNYieldRegressor

    return BNNYieldRegressor(**kw)


def _tiny_budget(**kw):
    """Small training budget so fit tests run in seconds."""
    defaults = dict(epochs=60, warmup_epochs=10, n_mc=16, batch_size=64)
    defaults.update(kw)
    return defaults


def _multiyear_frame(n_regions=6, years=(2001, 2011), seed=0):
    """Panel with category-dtype Harvest Year/Region, matching what
    DefaultFitter hands the wrapper (selected_features + cat_features)."""
    rng = np.random.default_rng(seed)
    yrs = list(range(years[0], years[1] + 1))
    rows = []
    for t in yrs:
        for r in range(n_regions):
            x1, x2 = rng.normal(), rng.normal()
            noise = 0.1 + 0.5 * (r / n_regions)  # heteroscedastic by region
            rows.append(
                dict(
                    f1=x1,
                    f2=x2,
                    y=5.0 + 2.0 * x1 + rng.normal(scale=noise),
                    year=t,
                    region=f"r{r}",
                )
            )
    df = pd.DataFrame(rows)
    X = pd.DataFrame(
        {
            "f1": df["f1"],
            "f2": df["f2"],
            "Harvest Year": pd.Categorical(df["year"]),
            "Region": pd.Categorical(df["region"]),
        }
    )
    return X, df["y"].to_numpy()


# --------------------------------------------------------------------------- #
# Wrapper mechanics
# --------------------------------------------------------------------------- #
def test_bnn_sklearn_api():
    m = _make_regressor(epochs=5, kl_weight=0.1)
    assert hasattr(m, "fit") and hasattr(m, "predict")
    p = m.get_params()
    assert p["epochs"] == 5 and p["kl_weight"] == 0.1
    assert p["calibrate_sigma"] is True  # default on
    m.set_params(kl_weight=0.05)
    assert m.get_params()["kl_weight"] == 0.05
    # kl_weight default must be the working-recipe 0.05, not the paper's 1.0
    # (full KL collapses the sigma head to a near-constant).
    assert _make_regressor().get_params()["kl_weight"] == 0.05


def test_bnn_never_grows_calibrate_attr():
    """ModelTrainer._add_confidence_intervals_if_needed probes
    hasattr(model, 'calibrate') / hasattr(model, 'conformalize') on the
    UNWRAPPED bnn model (estimate_ci early-returns it) and would call the
    attribute with in-sample training data. The sigma-calibration toggle is
    therefore named calibrate_sigma, and these names must stay free."""
    m = _make_regressor()
    assert not hasattr(m, "calibrate")
    assert not hasattr(m, "conformalize")


def test_bnn_numeric_encoding():
    m = _make_regressor()
    X = pd.DataFrame(
        {
            "a": [1.0, 2, 3],
            "Region": pd.Categorical(["x", "y", "x"]),
            "b": [np.nan, 5, 6],
        }
    )
    Xn = m._numeric(X)
    assert "Region_x" in Xn.columns and "Region_y" in Xn.columns
    assert Xn.select_dtypes(include=["object", "category"]).shape[1] == 0


def test_bnn_missing_dep_message():
    """Without torch installed, the auto_train branch must raise the
    install-hint ImportError (not a bare ModuleNotFoundError)."""
    try:
        import torch  # noqa: F401

        pytest.skip("torch installed; missing-dep path not reachable")
    except ImportError:
        pass
    X = pd.DataFrame({"a": [1.0, 2, 3, 4]})
    y = pd.Series([1.0, 2.0, 3.0, 4.0])
    with pytest.raises(ImportError, match="pip install torch"):
        auto_train(
            "individual", "bnn", "REGRESSION", False, "Harvest Year",
            X.assign(y=y), X, y, feature_names=["a"], target_col="y",
        )


def test_bnn_classification_raises():
    with pytest.raises(ValueError, match="REGRESSION only"):
        auto_train(
            "individual", "bnn", "CLASSIFICATION", False, "Harvest Year",
            pd.DataFrame(), pd.DataFrame(), pd.Series(dtype=float),
            feature_names=[], target_col="y",
        )


# --------------------------------------------------------------------------- #
# Fit / predict
# --------------------------------------------------------------------------- #
def test_bnn_fit_predict_roundtrip():
    m = _make_regressor(calibrate_sigma=False, **_tiny_budget())
    rng = np.random.default_rng(0)
    n = 200
    x1 = rng.normal(size=n)
    x2 = rng.normal(size=n)
    y = 3.0 + 2.0 * x1 + rng.normal(scale=0.1 + 0.5 * np.abs(x2), size=n)
    X = pd.DataFrame({"x1": x1, "x2": x2})
    m.fit(X, y)

    mu = m.predict(X)
    assert mu.shape == (n,) and np.all(np.isfinite(mu))
    assert np.corrcoef(mu, y)[0, 1] > 0.7

    out = m.predict(X, return_std=True)
    assert len(out) == 4
    mu2, sd_tot, sd_alea, sd_epis = out
    assert all(a.shape == (n,) for a in out)
    assert np.all(sd_tot >= 0) and np.all(sd_alea >= 0) and np.all(sd_epis >= 0)
    np.testing.assert_allclose(
        sd_tot**2, sd_alea**2 + sd_epis**2, rtol=1e-5, atol=1e-8
    )
    # MC determinism: predict reseeds per call, so the point path and the CI
    # path of the pipeline see identical mu for identical X.
    np.testing.assert_array_equal(mu, mu2)
    np.testing.assert_array_equal(m.predict(X), mu)


def test_bnn_tiny_fold_smaller_than_batch():
    m = _make_regressor(calibrate_sigma=False, **_tiny_budget(epochs=15, batch_size=512))
    X = pd.DataFrame({"a": np.linspace(0, 1, 12), "b": np.linspace(1, 0, 12)})
    y = np.linspace(2, 4, 12)
    mu = m.fit(X, y).predict(X)
    assert mu.shape == (12,) and np.all(np.isfinite(mu))


def test_bnn_handles_all_nan_column_and_unseen_categories():
    m = _make_regressor(calibrate_sigma=False, **_tiny_budget(epochs=15))
    X, y = _multiyear_frame(n_regions=3, years=(2005, 2008))
    X["dead"] = np.nan  # all-NaN column: NaN median -> fillna(0.0) fallback
    m.fit(X, y)
    X_new = X.head(4).copy()
    X_new["Region"] = pd.Categorical(["r99"] * 4)  # unseen region
    X_new["Harvest Year"] = pd.Categorical([2030] * 4)  # unseen year
    mu = m.predict(X_new)
    assert mu.shape == (4,) and np.all(np.isfinite(mu))


# --------------------------------------------------------------------------- #
# Sigma recalibration
# --------------------------------------------------------------------------- #
def test_bnn_sigma_calibration_multiyear():
    m = _make_regressor(cal_min_rows=3, cal_min_train_rows=10, **_tiny_budget())
    X, y = _multiyear_frame(n_regions=6, years=(2001, 2011))
    m.fit(X, y)
    assert np.isfinite(m.sigma_scale_) and m.sigma_scale_ > 0
    # Final model must be the ALL-rows refit (two-pass recipe), not the
    # calibration fit on years < max.
    assert m._core.n_train_ == len(y)
    # Predicted sd scales linearly with sigma_scale_.
    _, sd_before, _, _ = m.predict(X, return_std=True)
    m.sigma_scale_ = m.sigma_scale_ * 3.0
    _, sd_after, _, _ = m.predict(X, return_std=True)
    np.testing.assert_allclose(sd_after, sd_before * 3.0, rtol=1e-6)


@pytest.mark.parametrize(
    "mutate",
    [
        "single_year",       # < 3 distinct years
        "drop_year_column",  # no Harvest Year at all
        "tiny_cal_year",     # cal-year rows < cal_min_rows
    ],
)
def test_bnn_sigma_calibration_skipped(mutate):
    m = _make_regressor(cal_min_rows=5, cal_min_train_rows=10, **_tiny_budget(epochs=15))
    X, y = _multiyear_frame(n_regions=6, years=(2001, 2008))
    if mutate == "single_year":
        X["Harvest Year"] = pd.Categorical([2008] * len(X))
    elif mutate == "drop_year_column":
        X = X.drop(columns=["Harvest Year"])
    elif mutate == "tiny_cal_year":
        # keep only 2 rows of the newest year (< cal_min_rows=5)
        is_cal = (X["Harvest Year"].astype(str) == "2008").to_numpy()
        keep = ~is_cal | (np.cumsum(is_cal) <= 2)
        X, y = X[keep].reset_index(drop=True), y[keep]
    m.fit(X, y)
    assert m.sigma_scale_ == 1.0
    assert m._core.n_train_ == len(y)


# --------------------------------------------------------------------------- #
# Pipeline wiring
# --------------------------------------------------------------------------- #
def test_predict_bnn_with_ci_shape():
    """_predict_bnn_with_ci must emit the (n, 2, 1) CI layout used by the
    tabpfn/tabicl paths — _retrend_predictions and
    _re_add_region_mean_to_predictions index y_pred_ci[ri, 0, 0]/[ri, 1, 0],
    and the ngboost-style (n, 3) layout would store the mean as 'upper CI'."""
    from geocif import utils
    from geocif.geocif import Geocif

    n = 9
    mu = np.linspace(4.0, 8.0, n)
    sd = np.linspace(0.2, 1.1, n)

    class _Stub:
        def predict(self, X, return_std=False):
            assert return_std
            return mu, sd, sd * 0.8, sd * 0.6

        def get_params(self):
            return {"epochs": 700}

    obj = SimpleNamespace(
        alpha=0.1,
        model=_Stub(),
        logger=logging.getLogger("test_bnn_ci"),
    )
    obj._predict_bnn_with_ci = MethodType(Geocif._predict_bnn_with_ci, obj)

    y_pred, y_pred_ci, hp = obj._predict_bnn_with_ci(pd.DataFrame(np.zeros((n, 2))))
    z = utils.get_z_value(0.1)
    assert y_pred_ci.shape == (n, 2, 1)
    np.testing.assert_allclose(y_pred, mu)
    np.testing.assert_allclose(y_pred_ci[:, 0, 0], mu - z * sd)
    np.testing.assert_allclose(y_pred_ci[:, 1, 0], mu + z * sd)
    assert np.all(y_pred_ci[:, 0, 0] <= y_pred) and np.all(y_pred <= y_pred_ci[:, 1, 0])
    assert hp == {"epochs": 700}


def test_auto_train_bnn_branch():
    assert "bnn_params" in inspect.signature(auto_train).parameters
    src = inspect.getsource(auto_train)
    assert 'model_name == "bnn"' in src
    assert "bnn.update(bnn_params or {})" in src


def test_estimate_ci_returns_bnn_unwrapped():
    """bnn carries its own calibrated sigma; crepes/mapie must not wrap it —
    and strip_variant_prefix runs first, so curated_bnn inherits this."""
    from geocif.ml.trainers import estimate_ci

    sentinel = object()
    assert estimate_ci("REGRESSION", "bnn", sentinel) is sentinel
    assert estimate_ci("REGRESSION", "curated_bnn", sentinel) is sentinel
    assert estimate_ci("REGRESSION", "top10_bnn", sentinel) is sentinel


def test_geocif_wiring_for_bnn():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    # [ML] bnn_* config parse + threading into auto_train
    assert "self.bnn_params" in src
    assert 'bnn_params=getattr(self.obj, "bnn_params"' in src
    for opt in ("bnn_epochs", "bnn_kl_weight", "bnn_calibrate_sigma"):
        assert opt in src, f"{opt} must be recognized in the [ML] config parse"
    # CI dispatch keys on dispatch_name (variants route through the same path)
    assert 'self.dispatch_name == "bnn"' in src
    assert "def _predict_bnn_with_ci" in src
    # the (n, 2, 1) stack, inside _predict_bnn_with_ci
    bnn_ci = src.split("def _predict_bnn_with_ci")[1].split("def ")[0]
    assert "np.stack([lower, upper], axis=1)[:, :, np.newaxis]" in bnn_ci
    # bnn must NOT join the scaled-models tuples (self-contained wrapper route)
    assert '"gpr", "george", "bnn"' not in src

    trainers_src = (ROOT / "ml" / "trainers.py").read_text(encoding="utf-8")
    assert '"tabicl_ft", "bnn"]' in trainers_src  # estimate_ci early-return

    utils_src = (ROOT / "utils.py").read_text(encoding="utf-8")
    assert '"bnn": "BNN"' in utils_src

    xai_src = (ROOT / "ml" / "xai.py").read_text(encoding="utf-8")
    assert '"bnn"' in xai_src.split("_MODEL_AGNOSTIC_XAI = ")[1].split("\n")[0]
