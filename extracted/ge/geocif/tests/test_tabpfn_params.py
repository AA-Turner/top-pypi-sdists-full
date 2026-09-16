"""Wiring tests for the [ML] tabpfn_* overrides.

tabpfn 9.0.0 made TabPFN-3.5 the default checkpoint and added
``InferenceConfig.N_ESTIMATORS``, which is honoured only when
``n_estimators="auto"``. geocif had hard-coded ``n_estimators=8``, so it
silently overrode whatever a checkpoint asked for, and had no way to pin a
checkpoint version. These tests cover the plumbing geocif owns --
config harvest, call-site wiring, and the two literals that keep pre-9.0.0
results reproducible. Loading a real checkpoint happens on the cluster.
"""
import inspect
import re
from pathlib import Path

from geocif.ml.trainers import (
    DEFAULT_TABPFN_MODEL_VERSION,
    _TABPFN_LIBRARY_DEFAULT,
    auto_train,
)

ROOT = Path(__file__).resolve().parents[1] / "geocif"
TRAINERS = (ROOT / "ml" / "trainers.py").read_text(encoding="utf-8")
GEOCIF = (ROOT / "geocif.py").read_text(encoding="utf-8")


def test_auto_train_accepts_tabpfn_params():
    p = inspect.signature(auto_train).parameters
    assert "tabpfn_params" in p, "auto_train must accept tabpfn_params"
    assert p["tabpfn_params"].default is None, "must default to None (opt-in)"


def test_config_harvests_both_tabpfn_options():
    """Both keys are read from [ML] as STRINGS -- each accepts a non-numeric
    literal ("auto", "v3.5-fast"), so getint/getfloat would crash on them."""
    assert "self.tabpfn_params: dict = {}" in GEOCIF
    for opt in ("tabpfn_n_estimators", "tabpfn_model_version"):
        assert opt in GEOCIF, f"{opt} is never harvested from [ML]"
    block = GEOCIF.split("self.tabpfn_params: dict = {}")[1][:500]
    assert "self.parser.get(" in block, "must use .get (string), not getint"
    assert 'replace("tabpfn_", "")' in block, "tabpfn_<x> must map to <x>"


def test_auto_train_call_site_passes_tabpfn_params():
    assert 'tabpfn_params=getattr(self.obj, "tabpfn_params", None)' in GEOCIF, (
        "harvested params never reach auto_train"
    )


def test_default_n_estimators_stays_8():
    assert '_tp.get("n_estimators", 8)' in TRAINERS, (
        "default must remain 8, geocif's long-standing value"
    )


def test_default_model_version_is_v3_not_the_library_default():
    """tabpfn 9.0.0 moved its own default to v3.5. geocif pins v3 so upgrading
    the library does not silently change every archived tabpfn result."""
    assert DEFAULT_TABPFN_MODEL_VERSION == "v3", (
        "default checkpoint must be v3; changing it rewrites history"
    )
    assert '_tp.get("model_version", DEFAULT_TABPFN_MODEL_VERSION)' in TRAINERS, (
        "unset config must fall back to the pinned default, not to None"
    )


def test_unset_version_pins_rather_than_falling_through():
    """The unset path must reach create_default_for_version -- if it hit the
    plain constructor instead, the pin would be silently inert."""
    block = TRAINERS.split('_tp.get("model_version", DEFAULT_TABPFN_MODEL_VERSION)')[1][:1200]
    assert "create_default_for_version(_mv, **_tabpfn_kwargs)" in block
    # the plain-constructor branch is reserved for the explicit opt-out
    assert "_TABPFN_LIBRARY_DEFAULT" in block, (
        "plain constructor must be gated on the opt-out sentinel"
    )


def test_library_default_optout_exists_and_cannot_collide():
    """'default'/'library' mean follow the installed tabpfn. None of them may
    look like a real ModelVersion string, or a version would be unreachable."""
    assert _TABPFN_LIBRARY_DEFAULT, "an opt-out must exist"
    assert DEFAULT_TABPFN_MODEL_VERSION not in _TABPFN_LIBRARY_DEFAULT
    for sentinel in _TABPFN_LIBRARY_DEFAULT:
        assert not sentinel.startswith("v"), (
            f"{sentinel!r} could collide with a real TabPFN version string"
        )
    assert "model = _cls(**_tabpfn_kwargs)" in TRAINERS


def test_auto_is_passed_through_not_coerced_to_int():
    """int('auto') raises; the string must survive to tabpfn untouched."""
    block = TRAINERS.split('_tp.get("n_estimators", 8)')[1][:400]
    assert '"auto"' in block and "int(_n_est)" in block, (
        "n_estimators must accept both 'auto' and an int literal"
    )
    assert ".lower() ==" in block, "the 'auto' test should be case-insensitive"


def test_bad_version_raises_with_valid_list():
    block = TRAINERS.split(
        '_tp.get("model_version", DEFAULT_TABPFN_MODEL_VERSION)'
    )[1][:1400]
    assert "ModelVersion(" in block
    assert "except ValueError" in block and "raise ValueError" in block, (
        "an unknown version must fail loudly, not fall through to the default"
    )
    assert "m.value for m in ModelVersion" in block, (
        "the error should name the valid versions"
    )


def test_explicit_kwargs_still_win_over_version_defaults():
    """create_default_for_version sets n_estimators='auto'; geocif's kwargs are
    applied as **overrides so an explicit count is not silently discarded."""
    assert "create_default_for_version(_mv, **_tabpfn_kwargs)" in TRAINERS
