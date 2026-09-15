"""Wiring tests for the Mitra-v2 model (model='mitra' / 'mitra_ft').

Mitra-v2 (arXiv:2609.04540) is an in-context tabular foundation model whose
backbone ships inside ``autogluon.tabular[mitra]`` -- an optional dep, so these
tests never import it. They cover the parts geocif owns: the numeric encoder,
the histogram decode (mean + quantiles), the config deltas that make a v2
checkpoint work at all, and the dispatch wiring. Heavy checkpoint round-trips
run on the cluster, not in CI.
"""
import inspect
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from geocif.ml.mitra import (
    DEPLOY_FEATURE_BUDGET,
    MITRA_V1_REGRESSOR,
    MITRA_V2_REGRESSOR,
    PRETRAIN_MAX_FEATURES,
    MitraYieldRegressor,
    _NumericEncoder,
    _numpy_seed,
    _resolve_precision,
)
from geocif.ml.trainers import auto_train, estimate_ci

ROOT = Path(__file__).resolve().parents[1] / "geocif"


# --------------------------------------------------------------------------
# sklearn surface
# --------------------------------------------------------------------------
def test_mitra_sklearn_api():
    m = MitraYieldRegressor(n_estimators=3, max_features=128)
    assert hasattr(m, "fit") and hasattr(m, "predict")
    p = m.get_params()
    assert p["n_estimators"] == 3 and p["max_features"] == 128
    assert p["hf_model"] == MITRA_V2_REGRESSOR
    assert p["fine_tune"] is False
    m.set_params(n_estimators=8, fine_tune=True)
    assert m.get_params()["n_estimators"] == 8
    assert m.get_params()["fine_tune"] is True


def test_mitra_never_exposes_a_calibrate_attribute():
    """_add_confidence_intervals_if_needed probes hasattr(model,'calibrate')
    on models trainers.estimate_ci returns unwrapped, and would call it with
    in-sample data. Same trap as BNNYieldRegressor."""
    m = MitraYieldRegressor()
    assert not hasattr(m, "calibrate")
    assert not hasattr(m, "conformalize")


def test_mitra_missing_dep_message_names_the_extra():
    """fit() must fail loudly naming the optional dependency."""
    try:
        import autogluon.tabular.models.mitra._internal.models.tab2d  # noqa: F401
    except ImportError:
        m = MitraYieldRegressor()
        X = pd.DataFrame({"a": [1.0, 2.0], "b": [3.0, 4.0]})
        with pytest.raises(ImportError, match=r"geocif\[mitra\]"):
            m.fit(X, [1.0, 2.0])
        return
    pytest.skip("autogluon mitra installed; the missing-dep path is unreachable")


# --------------------------------------------------------------------------
# numeric encoding
# --------------------------------------------------------------------------
def test_encoder_keeps_numeric_categorical_levels_ordinal():
    """Harvest Year / Region_ID arrive as pandas category dtype. Factorize
    codes would destroy the year ordering, so numeric levels stay numeric."""
    X = pd.DataFrame(
        {
            "Harvest Year": pd.Categorical([2019, 2021, 2020]),
            "Region": pd.Categorical(["iowa", "ohio", "iowa"]),
            "x": [1.0, 2.0, 3.0],
        }
    )
    enc = _NumericEncoder()
    out = enc.fit_transform(X)
    assert out.dtype == np.float32
    np.testing.assert_allclose(out[:, 0], [2019.0, 2021.0, 2020.0])
    assert "Harvest Year" in enc.numeric_levels_
    assert "Region" in enc.cat_maps_
    # nominal levels become codes in order of appearance
    np.testing.assert_allclose(out[:, 1], [0.0, 1.0, 0.0])


def test_encoder_maps_unseen_levels_to_minus_one():
    X = pd.DataFrame({"Region": pd.Categorical(["a", "b"]), "x": [1.0, 2.0]})
    enc = _NumericEncoder()
    enc.fit_transform(X)
    out = enc.transform(
        pd.DataFrame({"Region": pd.Categorical(["c", "a"]), "x": [5.0, 6.0]})
    )
    np.testing.assert_allclose(out[:, 0], [-1.0, 0.0])


def test_encoder_realigns_and_preserves_nan():
    X = pd.DataFrame({"a": [1.0, np.nan], "b": [3.0, 4.0]})
    enc = _NumericEncoder()
    enc.fit_transform(X)
    # columns arrive in a different order at predict time
    out = enc.transform(pd.DataFrame({"b": [9.0, 8.0], "a": [7.0, np.nan]}))
    np.testing.assert_allclose(out[:, 0], [7.0, np.nan])
    np.testing.assert_allclose(out[:, 1], [9.0, 8.0])


def test_encoder_does_not_mutate_the_caller_frame():
    """geocif hands the same X to several models per fold."""
    X = pd.DataFrame({"a": [1.0, np.nan, 3.0], "Region": pd.Categorical(["x", "y", "x"])})
    before = X.copy()
    _NumericEncoder().fit_transform(X)
    pd.testing.assert_frame_equal(X, before)


# --------------------------------------------------------------------------
# histogram decode -- the quality-critical delta from stock AutoGluon
# --------------------------------------------------------------------------
def _uniform_hist(n_rows, edges, probs_row):
    return np.tile(np.asarray(probs_row, float), (n_rows, 1))


def test_quantiles_from_histogram_are_exact_on_a_uniform_bin():
    """One bin holding all the mass: the q-th quantile is the linear
    interpolation inside that bin."""
    edges = np.array([0.0, 1.0, 2.0])
    probs = np.array([[0.0, 1.0]])
    q = MitraYieldRegressor._quantiles_from_histogram(edges, probs, np.array([0.25, 0.5, 0.9]))
    np.testing.assert_allclose(q[0], [1.25, 1.5, 1.9])


def test_quantiles_from_histogram_span_two_bins():
    edges = np.array([0.0, 1.0, 2.0])
    probs = np.array([[0.5, 0.5]])
    q = MitraYieldRegressor._quantiles_from_histogram(edges, probs, np.array([0.25, 0.5, 0.75]))
    np.testing.assert_allclose(q[0], [0.5, 1.0, 1.5], atol=1e-12)


def test_quantiles_are_monotone_and_bracket_the_mean():
    rng = np.random.RandomState(0)
    edges = np.linspace(-2.0, 5.0, 51)
    logits = rng.normal(size=(7, 50))
    probs = np.exp(logits) / np.exp(logits).sum(axis=1, keepdims=True)
    qs = MitraYieldRegressor._quantiles_from_histogram(edges, probs, np.array([0.1, 0.5, 0.9]))
    assert (np.diff(qs, axis=1) >= -1e-12).all()

    centres = 0.5 * (edges[:-1] + edges[1:])
    mean = (probs * centres[None, :]).sum(axis=1)
    assert ((mean >= qs[:, 0]) & (mean <= qs[:, 2])).all()


def test_extreme_quantiles_stay_inside_the_grid():
    edges = np.linspace(0.0, 10.0, 11)
    probs = np.full((3, 10), 0.1)
    qs = MitraYieldRegressor._quantiles_from_histogram(edges, probs, np.array([0.0, 1.0]))
    assert (qs[:, 0] >= edges[0] - 1e-12).all()
    assert (qs[:, 1] <= edges[-1] + 1e-12).all()


# --------------------------------------------------------------------------
# config deltas + helpers
# --------------------------------------------------------------------------
def test_precision_resolution_avoids_float32_cpu_autocast():
    """torch CPU autocast accepts bfloat16/float16 only, so float32 must be
    expressed as 'no autocast' (None), not dtype=torch.float32."""
    assert _resolve_precision("auto", "cpu") is None
    assert _resolve_precision("auto", "cuda") == "bfloat16"
    assert _resolve_precision("float32", "cuda") is None
    assert _resolve_precision("bfloat16", "cpu") == "bfloat16"


def test_numpy_seed_restores_global_state():
    """AutoGluon's Preprocessor draws its mirror augmentations from the GLOBAL
    numpy RNG; leaking that seed would perturb the rest of the pipeline."""
    np.random.seed(1234)
    before = np.random.get_state()[1][:5].copy()
    with _numpy_seed(7):
        first = np.random.rand()
    after = np.random.get_state()[1][:5]
    np.testing.assert_array_equal(before, after)

    with _numpy_seed(7):
        second = np.random.rand()
    assert first == second  # same seed -> same draw


def test_config_forces_cross_entropy_head_for_a_binned_checkpoint():
    """The whole reason ml/mitra.py exists: AutoGluon's MitraRegressor
    hardcodes regression_loss='mse' + dim_output=1, which cannot drive the
    1,000-bin Mitra-v2 regression checkpoint."""
    src = inspect.getsource(MitraYieldRegressor._build_config)
    assert "CROSS_ENTROPY" in src
    assert '"dim_output": int(dim_output)' in src
    assert "binned = dim_output > 1" in src


def test_predict_uses_the_mean_decode_not_argmax():
    src = inspect.getsource(MitraYieldRegressor.predict)
    # strip the docstring, which legitimately mentions the stock argmax decode
    code = src.split('"""')[0] + src.split('"""')[-1]
    assert "argmax" not in code
    assert "centres" in code and "sum(axis=1)" in code


def test_forward_copies_arrays_before_the_preprocessor():
    """Preprocessor.fit / transform_X impute NaN IN PLACE."""
    fwd = inspect.getsource(MitraYieldRegressor._forward)
    assert "self.X_support_.copy()" in fwd
    fit = inspect.getsource(MitraYieldRegressor.fit)
    assert "trainer.preprocessor.fit(X_num.copy()" in fit


def test_member_histogram_flips_probabilities_with_a_mirrored_grid():
    src = inspect.getsource(MitraYieldRegressor._member_histogram)
    assert "(1.0 - edges)[::-1]" in src
    assert "probs[:, ::-1]" in src


def test_pretraining_envelope_constants_match_the_paper():
    assert PRETRAIN_MAX_FEATURES == 50      # Table 1: 1-50 features
    assert DEPLOY_FEATURE_BUDGET == 256     # section 2.6 wide-table budget
    assert MITRA_V2_REGRESSOR == "autogluon/mitra-regressor-2"
    assert MITRA_V1_REGRESSOR == "autogluon/mitra-regressor"


def test_split_is_deterministic_and_non_empty():
    m = MitraYieldRegressor(val_frac=0.2)
    X = np.arange(40, dtype="float32").reshape(20, 2)
    y = np.arange(20, dtype="float32")
    a = m._split(X, y, 3)
    b = m._split(X, y, 3)
    for lhs, rhs in zip(a, b):
        np.testing.assert_array_equal(lhs, rhs)
    X_tr, y_tr, X_va, y_va = a
    assert len(X_tr) == 16 and len(X_va) == 4
    assert len(y_tr) == 16 and len(y_va) == 4


def test_split_handles_a_two_row_fold():
    m = MitraYieldRegressor(val_frac=0.2)
    X = np.zeros((2, 3), dtype="float32")
    y = np.array([1.0, 2.0], dtype="float32")
    X_tr, y_tr, X_va, y_va = m._split(X, y, 0)
    assert len(X_tr) >= 1 and len(X_va) >= 1


def test_nan_to_column_mean_fills_and_copies():
    X = np.array([[1.0, np.nan], [3.0, np.nan]], dtype="float32")
    out = MitraYieldRegressor._nan_to_column_mean(X)
    assert np.isfinite(out).all()
    np.testing.assert_allclose(out[:, 0], [1.0, 3.0])
    np.testing.assert_allclose(out[:, 1], [0.0, 0.0])  # all-NaN column -> 0
    assert np.isnan(X[0, 1])  # original untouched


# --------------------------------------------------------------------------
# trainers / geocif wiring
# --------------------------------------------------------------------------
def test_auto_train_mitra_branch():
    assert "mitra_params" in inspect.signature(auto_train).parameters
    src = inspect.getsource(auto_train)
    assert 'model_name in ("mitra", "mitra_ft")' in src
    # the fine-tune switch is the model NAME, so one [ML] block runs both arms
    assert 'mitra["fine_tune"] = model_name == "mitra_ft"' in src


def test_estimate_ci_leaves_mitra_unwrapped():
    """Native 1,000-bin intervals must not be replaced by conformal ones."""
    sentinel = object()
    for name in ("mitra", "mitra_ft"):
        # estimate_ci(model_type, model_name, model, alpha, ci_method)
        assert estimate_ci("REGRESSION", name, sentinel, 0.2, "crepes") is sentinel


def test_wrapper_prefix_regex_leaves_mitra_alone():
    for name in ("mitra", "mitra_ft"):
        assert not name.startswith(("curated_", "auto_"))
        assert re.match(r"^top\d+_(.+)$", name) is None
        assert re.match(r"^last\d+m_(.+)$", name) is None


def test_geocif_wiring_for_mitra():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    assert '"tabfm_gsa", "mitra", "mitra_ft"]' in src        # tabular flags
    assert '"mitra": TabPFNFitter(self.obj)' in src           # fitter map
    assert '"mitra_ft": TabPFNFitter(self.obj)' in src
    assert 'self.dispatch_name in ("mitra", "mitra_ft")' in src   # CI dispatch
    assert "def _predict_mitra_with_ci" in src
    assert "self.mitra_params" in src                         # [ML] overrides
    assert 'mitra_params=getattr(self.obj, "mitra_params"' in src


def test_mitra_ci_emits_the_n_2_1_shape():
    """_retrend_predictions indexes y_pred_ci[ri, 0, 0] / [ri, 1, 0]; the
    ngboost (n, 3) layout stores the MEAN as 'upper' and must not be copied."""
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    body = src.split("def _predict_mitra_with_ci")[1].split("def _predict_tabpfn")[0]
    assert "np.stack([lower, upper], axis=1)[:, :, np.newaxis]" in body
    assert "np.vstack" not in body


def test_mitra_ci_path_uses_one_forward_pass():
    """predict() + predict_quantiles() would run the transformer twice over
    the same query rows; the CI path must derive both from one distribution."""
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    body = src.split("def _predict_mitra_with_ci")[1].split("def _predict_tabpfn")[0]
    assert "predict_with_quantiles" in body
    assert hasattr(MitraYieldRegressor, "predict_with_quantiles")


def test_mitra_is_model_agnostic_for_xai():
    from geocif.ml.xai import _MODEL_AGNOSTIC_XAI

    assert {"mitra", "mitra_ft"} <= _MODEL_AGNOSTIC_XAI


def test_config_has_mitra_sections():
    """Both names need a [<model>] section with ML_model -- geocif.py reads
    parser.getboolean(model_name, 'ML_model') at init and raises
    NoSectionError without it."""
    cfg = Path(__file__).resolve().parents[2] / "GEO" / "config" / "geocif" / "geocif.txt"
    if not cfg.exists():
        pytest.skip(f"config not checked out at {cfg}")
    text = cfg.read_text(encoding="utf-8")
    for section in ("[mitra]", "[mitra_ft]"):
        assert section in text, f"{section} missing from {cfg}"


def test_pyproject_declares_the_mitra_extra():
    pyproject = (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text(
        encoding="utf-8"
    )
    assert "mitra = [" in pyproject
    assert "autogluon.tabular[mitra]" in pyproject
