"""Anti-drift pins for the canonical copies.

Each copied module is checked against its canonical source in this repo (or, for the
tree parser, in the v16-runner checkout when it is present next to this one). The
check is byte equality, modulo the single transformation each copy needs:

- testmu_appium._evaluation/*     ← playwright-python/testmu_helper/evaluation/*  (verbatim)
- testmu_appium._vars             ← selenium-python/testmu_selenium/_vars         (import rename)
- testmu_appium._helpers._tree    ← v16-runner mobile/perception/tree.py          (verbatim)

testmu_appium._route_failure is deliberately NOT byte-pinned against
selenium-python/testmu_selenium/_route_failure. The selenium copy keeps a module-local
pending-failure list because that binding surfaces the verdict its own way; this
binding has exactly one verdict accumulator (`_test_state`), written by both
`step(on_failure="fail-continue")` and `route_failure`, and drained by `run()`.
`test_route_failure_writes_into_the_shared_test_state` below pins the observable half
of that divergence.

The tree-parser pin lives in test_tree_parity.py, which also pins behaviour against
fixtures so the copy stays honest even when the canonical checkout is absent.
"""
import ast
import inspect
import textwrap
from pathlib import Path

import pytest

from testmu_appium import _config, _session
from testmu_appium._evaluation._evaluate import (
    evaluate_sub_checks as _canonical_evaluate_sub_checks,
)
from testmu_appium._evaluation._mobile_operators import (
    evaluate_sub_checks as _mobile_evaluate_sub_checks,
)
from testmu_appium._route_failure import route_failure
from testmu_appium._test_state import (
    has_pending_failures, pending_failures_summary, reset_test_state,
)


class _StubDriver:
    """Enough of a driver for run() to reach the verdict; nothing is asserted on it."""

    def execute_script(self, script, *args):
        pass

    def quit(self):
        pass


_PKG = Path(__file__).resolve().parents[1] / "testmu_appium"
_REPO = Path(__file__).resolve().parents[2]
_PW_EVAL = _REPO / "playwright-python" / "testmu_helper" / "evaluation"


@pytest.mark.parametrize("name", ["__init__.py", "_core.py", "_colors.py", "_evaluate.py"])
def test_evaluation_copy_is_byte_identical(name):
    canonical = _PW_EVAL / name
    if not canonical.exists():
        pytest.skip(f"canonical source not present: {canonical}")
    assert (_PKG / "_evaluation" / name).read_bytes() == canonical.read_bytes(), (
        f"_evaluation/{name} drifted from testmu_helper.evaluation — re-copy it, or "
        f"upstream the change to the canonical module first"
    )


# `_vars.py` is intentionally NOT byte-parity pinned to the selenium canonical:
# the global `_global_cache` diverged by design (feat 3ac6767, reverted from
# selenium in 222b101), so the appium copy no longer matches
# selenium-python/testmu_selenium/_vars.py modulo rename.


class TestRouteFailureDivergence:
    """The divergence from the selenium _route_failure copy.

    `route_failure` writes into the shared verdict state that `run()` drains.
    """

    FAIL_CONTINUE = "Fail but continue executing"
    WARN_CONTINUE = "Warn but continue executing"

    @pytest.fixture(autouse=True)
    def _clean_state(self):
        reset_test_state()
        yield
        reset_test_state()

    def test_route_failure_writes_into_the_shared_test_state(self):
        route_failure(self.FAIL_CONTINUE, RuntimeError("boom"), "Tap Go")
        assert has_pending_failures()
        assert "Tap Go" in pending_failures_summary()
        assert "boom" in pending_failures_summary()

    def test_the_canonical_short_tokens_route_like_their_long_twins(self):
        """The Appium generator normalises failure conditions to the short
        canonical tokens (the same pair step(on_failure=...) accepts); the
        router treats them exactly like the recorded long enum strings."""
        route_failure("fail-continue", RuntimeError("boom"), "Tap Go")
        assert has_pending_failures()
        route_failure("warn-continue", RuntimeError("boom"), "Warn step")
        assert "Warn step" not in pending_failures_summary()

    def test_unknown_tokens_still_fail_closed(self):
        with pytest.raises(RuntimeError):
            route_failure("continue", RuntimeError("boom"), "Tap Go")
        with pytest.raises(RuntimeError):
            route_failure("bogus", RuntimeError("boom"), "Tap Go")

    def test_a_routed_failure_fails_the_session(self, monkeypatch):
        """A fail-continue route inside the test body makes run() raise at session
        end."""
        driver = _StubDriver()
        monkeypatch.setattr(_config, "run_target", "local")
        monkeypatch.setattr(_config, "smart", False)
        monkeypatch.setattr(_session.webdriver, "Remote", lambda **kw: driver)

        def body(_driver):
            try:
                raise RuntimeError("boom")
            except RuntimeError as exc:
                route_failure(self.FAIL_CONTINUE, exc, "Tap Go")

        with pytest.raises(RuntimeError) as excinfo:
            _session.run(body)
        assert "Tap Go" in str(excinfo.value)

    def test_warn_continue_does_not_touch_the_verdict(self):
        route_failure(self.WARN_CONTINUE, RuntimeError("boom"), "Tap Go")
        assert not has_pending_failures()

    @pytest.mark.parametrize("condition", ["Fail test immediately", "", None, "nonsense"])
    def test_unknown_and_empty_conditions_still_fail_closed(self, condition):
        with pytest.raises(RuntimeError):
            route_failure(condition, RuntimeError("boom"), "Tap Go")
        assert not has_pending_failures()

    def test_the_module_keeps_no_accumulator_of_its_own(self):
        """There must be no module-level pending-failure state here for run() to
        miss."""
        import testmu_appium._route_failure as module

        assert not hasattr(module, "_pending_failures")


class TestEvaluateSubChecksFork:
    """_mobile_operators.evaluate_sub_checks is a HAND-FORK of the canonical
    _evaluate.evaluate_sub_checks — same transform/composite pipeline, with the
    json_*-aware comparer swapped in. Byte pins do not reach it (it lives outside the
    copied modules on purpose), so it is pinned by source equality instead: an
    upstream change to the canonical pipeline must reach the mobile fork too.

    The ONE permitted difference is the comparer rename `_compare` → `compare`.
    """

    RENAME = ("_compare(", "compare(")

    @staticmethod
    def _normalised(fn) -> str:
        """The function's source as an AST dump, docstring removed.

        Comparing text would fail on wording; comparing the AST fails only when the
        pipeline actually differs.
        """
        tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
        func = tree.body[0]
        body = func.body
        if (body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)):
            func.body = body[1:]
        return ast.unparse(tree)

    def test_the_fork_matches_the_canonical_pipeline_modulo_the_rename(self):
        canonical = self._normalised(_canonical_evaluate_sub_checks)
        expected = canonical.replace(*self.RENAME)
        assert self._normalised(_mobile_evaluate_sub_checks) == expected, (
            "_mobile_operators.evaluate_sub_checks drifted from the canonical "
            "_evaluate.evaluate_sub_checks; the only permitted difference is the "
            "_compare → compare rename. Re-fork it, or upstream the change first."
        )

    def test_the_rename_is_actually_present(self):
        """Guards the guard: if the canonical source stopped calling _compare, the
        replace above would be a no-op and the pin would compare nothing."""
        assert self.RENAME[0] in self._normalised(_canonical_evaluate_sub_checks)
        assert self.RENAME[1] in self._normalised(_mobile_evaluate_sub_checks)

    def test_the_two_agree_on_the_shared_operator_set(self):
        """Behavioural half: for operators BOTH implement, the answers must match."""
        sub_checks = [
            {"extracted_value": "hello world", "expected_value": "world",
             "operator": "contains"},
            {"extracted_value": " 10 ", "expected_value": "10",
             "operator": "equals", "transforms": ["strip"]},
            {"extracted_value": "3", "expected_value": "10", "operator": "lt"},
        ]
        for composite in ("and", "or"):
            assert (_mobile_evaluate_sub_checks("", composite, sub_checks)
                    == _canonical_evaluate_sub_checks("", composite, sub_checks))


def test_evaluation_is_stdlib_only():
    """The copy must not pull appium/selenium in — it is imported by value helpers
    that run with no driver."""
    for path in (_PKG / "_evaluation").glob("*.py"):
        source = path.read_text()
        for forbidden in ("import appium", "import selenium", "import httpx"):
            assert forbidden not in source, f"{path.name} imports {forbidden}"
