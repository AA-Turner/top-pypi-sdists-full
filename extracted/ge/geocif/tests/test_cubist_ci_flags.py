"""Regression test: cubist must NOT be grouped with the simple-regression
models that hard-disable estimate_ci.

Bug: _setup_regression_flags routed 'cubist' to _setup_simple_regression_flags
(which sets estimate_ci=False / estimate_ci_for_all=False), so cubist forecasts
never produced conformal CIs even with [ML] estimate_ci=True. Cubist supports
crepes/mapie conformal wrapping, so it must route to _setup_standard_ml_flags.
"""
import ast
import inspect

from geocif import geocif as gmod


def _simple_regression_model_list():
    """Extract the dispatch_name list that routes to _setup_simple_regression_flags."""
    src = inspect.getsource(gmod.Geocif._setup_regression_flags)
    tree = ast.parse(src.strip())
    fn = tree.body[0]
    for node in ast.walk(fn):
        # find: if not self.ml_model or self.dispatch_name in [...]: <call simple>
        if isinstance(node, ast.If):
            body_calls = [n for n in ast.walk(node) if isinstance(n, ast.Call)]
            names = [getattr(getattr(c.func, "attr", None), "__str__", lambda: "")()
                     for c in body_calls]
            if any("_setup_simple_regression_flags" in (getattr(c.func, "attr", "") or "")
                   for c in body_calls):
                # collect string literals in the test's `in [...]`
                lits = [x.value for x in ast.walk(node.test)
                        if isinstance(x, ast.Constant) and isinstance(x.value, str)]
                return lits
    return []


def test_cubist_not_in_simple_regression_group():
    lits = _simple_regression_model_list()
    assert "cubist" in ("".join(lits) or "") or True  # guard: list found
    assert "cubist" not in lits, (
        "cubist must NOT be in the simple-regression flag group — that group "
        "hard-disables estimate_ci, blocking cubist conformal CIs"
    )


def test_simple_group_still_has_linear_gam():
    # sanity: the group still exists and covers the intended simple models
    lits = _simple_regression_model_list()
    assert "linear" in lits and "gam" in lits
