"""Regression test: cell_optimizer GA can optimize on the ESI signal.

`esi` must be a first-class variable (in _VAR_COLS so it's picked up from the
per-cell parquet, and in _DOY_AGG_DEFAULTS with a `min` default so the seasonal
MINIMUM ESI — i.e. MIN_ESI4WK — is what the GA fits yield against). Text-level
so it runs without the heavy cell_optimizer import graph.
"""
import ast
from pathlib import Path

SRC = (Path(__file__).resolve().parents[1] / "geocif" / "cell_optimizer.py").read_text(encoding="utf-8")


def _module_assign(name):
    """Return the ast node assigned to a top-level `name = ...`."""
    tree = ast.parse(SRC)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"{name} not found at module level")


def test_esi_in_var_cols():
    var_cols = _module_assign("_VAR_COLS")
    assert "esi" in var_cols, "cell_optimizer must allow 'esi' as a GA variable"


def test_esi_doy_agg_default_is_min():
    defaults = _module_assign("_DOY_AGG_DEFAULTS")
    assert defaults.get("esi") == "min", (
        "esi DOY aggregation must default to 'min' to reproduce MIN_ESI4WK"
    )
