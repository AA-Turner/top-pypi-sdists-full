"""Regression tests for config-driven Cubist hyperparameters.

Cubist HPs used to be hardcoded in trainers.auto_train (n_committees=10,
extrapolation=0.10). They are now overridable per-project via [ML] cubist_*
options, threaded auto_train(cubist_params=...) -> the cubist branch, with the
old values kept as fallbacks so crops that set nothing are unaffected.

These are structural (AST/text) tests so they run without the optional
`cubist` wheel or a live config on the box.
"""
import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "geocif"
TRAINERS = ROOT / "ml" / "trainers.py"
GEOCIF = ROOT / "geocif.py"


def _auto_train_def():
    tree = ast.parse(TRAINERS.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "auto_train":
            return node
    raise AssertionError("auto_train not found in trainers.py")


def test_auto_train_accepts_cubist_params():
    fn = _auto_train_def()
    names = [a.arg for a in fn.args.args + fn.args.kwonlyargs]
    assert "cubist_params" in names, "auto_train must accept a cubist_params argument"


def test_cubist_branch_merges_overrides_over_defaults():
    src = TRAINERS.read_text(encoding="utf-8")
    # defaults still present as the base dict
    assert "n_committees=10" in src and "extrapolation=0.10" in src, (
        "data-rich defaults must remain the fallback"
    )
    # overrides applied on top of the defaults
    assert re.search(r"cub\.update\(cubist_params or \{\}\)", src), (
        "cubist branch must merge cubist_params over the default dict"
    )
    # model built from the merged dict, not a fixed literal
    assert re.search(r"Cubist\(random_state=seed, \*\*cub\)", src), (
        "Cubist must be constructed from the merged **cub dict"
    )


def test_cubist_params_parsed_from_ml_config():
    src = GEOCIF.read_text(encoding="utf-8")
    assert "self.cubist_params" in src, "geocif must build self.cubist_params"
    for opt in ("cubist_n_committees", "cubist_extrapolation"):
        assert opt in src, f"{opt} must be recognized in the [ML] config parse"


def test_cubist_params_threaded_into_auto_train_call():
    src = GEOCIF.read_text(encoding="utf-8")
    assert re.search(r"cubist_params=getattr\(self\.obj, \"cubist_params\"", src), (
        "_train_base_model must pass cubist_params into auto_train"
    )
