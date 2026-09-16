"""Wiring tests for the Causilo model (model='causilo').

Causilo (Nums AI) is a pretrained tabular foundation model in the TabPFN/Mitra
family. Its weights are NOT freely licensed (Causilo License v1.0,
non-commercial research), and the package is an optional dep, so these tests
never import it. They cover the parts geocif owns: dispatch, the config
harvest, the native-quantile CI contract, and the guards. Real checkpoint
round-trips run on the cluster.
"""
import inspect
from pathlib import Path

from geocif.ml.trainers import auto_train

ROOT = Path(__file__).resolve().parents[1] / "geocif"
TRAINERS = (ROOT / "ml" / "trainers.py").read_text(encoding="utf-8")
GEOCIF = (ROOT / "geocif.py").read_text(encoding="utf-8")


def test_auto_train_accepts_causilo_params():
    p = inspect.signature(auto_train).parameters
    assert "causilo_params" in p
    assert p["causilo_params"].default is None


def test_causilo_branch_exists_and_uses_the_regressor():
    assert 'elif model_name == "causilo":' in TRAINERS
    assert "from causilo import CausiloRegressor" in TRAINERS
    assert "model = CausiloRegressor(**_cz)" in TRAINERS


def test_seed_is_geocif_fold_seed_not_config():
    """random_state must be geocif's fold seed so causilo permutes in step with
    every other model; a config override would silently decouple the folds."""
    assert '_cz["random_state"] = int(seed)' in TRAINERS, (
        "random_state must be forced from the fold seed"
    )
    block = GEOCIF.split("self.causilo_params: dict = {}")[1][:600]
    assert "causilo_random_state" not in block, (
        "random_state must NOT be harvested from config"
    )


def test_config_harvest_and_call_site():
    assert "self.causilo_params: dict = {}" in GEOCIF
    for opt in ("causilo_n_estimators", "causilo_device", "causilo_use_kv_cache"):
        assert opt in GEOCIF, f"{opt} never harvested"
    assert 'causilo_params=getattr(self.obj, "causilo_params", None)' in GEOCIF


def test_estimate_ci_leaves_causilo_unwrapped():
    """Causilo has 999 native quantiles; a conformal wrapper would replace a
    real predictive distribution with one global marginal width."""
    block = TRAINERS.split('"ngboost", "tabpfn", "tabpfn_ft"')[1][:200]
    assert '"causilo"' in block, "causilo must be in the unwrapped-CI list"


def test_ci_dispatch_routes_to_native_quantiles():
    assert 'elif self.dispatch_name == "causilo":' in GEOCIF
    assert "return self._predict_causilo_with_ci(X_test)" in GEOCIF
    assert "def _predict_causilo_with_ci" in GEOCIF


def test_ci_uses_one_call_and_the_median_as_point_estimate():
    """Bounds and point estimate must come off the SAME quantile vector, or a
    skewed posterior can put the prediction outside its own interval."""
    body = GEOCIF.split("def _predict_causilo_with_ci")[1].split("def ")[0]
    assert 'output_type="quantiles"' in body
    assert "quantiles=[lower_q, 0.5, upper_q]" in body, (
        "must request lower/median/upper together in one forward pass"
    )
    assert "lower, y_pred, upper = q[:, 0], q[:, 1], q[:, 2]" in body


def test_ci_emits_the_n_2_1_shape_not_ngboost_n_3():
    """_retrend_predictions indexes y_pred_ci[ri, 0, 0] / [ri, 1, 0]."""
    body = GEOCIF.split("def _predict_causilo_with_ci")[1].split("def ")[0]
    assert "np.stack([lower, upper], axis=1)[:, :, np.newaxis]" in body
    assert "np.vstack" not in body, "the ngboost (n, 3) layout must not be copied"


def test_quantile_failure_degrades_to_points_not_crash():
    body = GEOCIF.split("def _predict_causilo_with_ci")[1].split("def ")[0]
    assert "except Exception as exc:" in body
    assert "return (" in body and "None," in body, (
        "a missing quantile head must yield points with no interval"
    )
    assert "q.shape[1] != 3" in body, "a wrong-shaped return must be caught"


def test_classification_is_refused_loudly():
    block = TRAINERS.split('elif model_name == "causilo":')[1][:2600]
    assert 'if model_type != "REGRESSION":' in block
    assert "raise ValueError" in block


def test_weights_licence_is_documented_at_the_call_site():
    """The weights are non-commercial research only -- that constraint must be
    visible where someone would enable the model, not only in a memo."""
    block = TRAINERS.split('elif model_name == "causilo":')[1][:2600]
    assert "Causilo License" in block and "non-commercial" in block.lower()
