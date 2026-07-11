"""Regression tests for the ``[ML] make_maps`` figure-rendering gate.

``make_maps`` (default False) is the master switch for ALL yield_outlook PNG
rendering. When off, the ML fit / DB / outlook CSVs are still produced but no
figures are drawn, so metric-only reruns are fast.

The behavioral test needs the full yield_outlook import (heavy geo deps that
only exist on the cluster), so it is guarded by ``importorskip``. The
structural tests parse the source with ``ast`` and run anywhere, guarding the
gate's wiring against regressions even where the deps are absent.
"""
import ast
from pathlib import Path

import pytest

_SRC_PATH = Path(__file__).resolve().parents[1] / "geocif" / "yield_outlook.py"
_SRC = _SRC_PATH.read_text(encoding="utf-8")
_TREE = ast.parse(_SRC)


def _func(tree, name):
    return next(
        n for n in ast.walk(tree)
        if isinstance(n, ast.FunctionDef) and n.name == name
    )


class TestMakeMapsWiring:
    """Source-level guards — run regardless of optional geo dependencies."""

    def test_module_defines_default_flag(self):
        assigns = [
            n for n in _TREE.body
            if isinstance(n, ast.Assign)
            and any(getattr(t, "id", "") == "_MAKE_MAPS" for t in n.targets)
        ]
        assert assigns, "module must define a module-level _MAKE_MAPS default"
        assert assigns[0].value.value is True, "default must be True (back-compat)"

    def test_run_reads_flag_and_sets_global(self):
        run = _func(_TREE, "run")
        # global declaration present
        assert any(
            isinstance(n, ast.Global) and "_MAKE_MAPS" in n.names
            for n in ast.walk(run)
        ), "run() must declare `global _MAKE_MAPS`"
        # reads [ML] make_maps with fallback False
        got_default = None
        for call in ast.walk(run):
            if (
                isinstance(call, ast.Call)
                and getattr(call.func, "attr", "") == "getboolean"
                and len(call.args) >= 2
                and getattr(call.args[0], "value", None) == "ML"
                and getattr(call.args[1], "value", None) == "make_maps"
            ):
                for kw in call.keywords:
                    if kw.arg == "fallback":
                        got_default = kw.value.value
        assert got_default is False, "make_maps must default to False in run()"

    def test_outlook_map_renderer_early_returns_when_disabled(self):
        fn = _func(_TREE, "_generate_outlook_map")
        # first executable statement after the docstring must be the gate
        stmts = [s for s in fn.body if not (
            isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant)
        )]
        first = stmts[0]
        assert isinstance(first, ast.If), "gate must be the first statement"
        assert isinstance(first.test, ast.UnaryOp) and isinstance(first.test.op, ast.Not)
        assert getattr(first.test.operand, "id", "") == "_MAKE_MAPS"
        assert any(isinstance(s, ast.Return) for s in first.body)

    def test_diagnostics_call_is_gated(self):
        run = _func(_TREE, "run")
        # the _generate_diagnostics call must sit under an `if` whose test
        # references make_maps
        for node in ast.walk(run):
            if isinstance(node, ast.If):
                names = {
                    n.id for n in ast.walk(node.test) if isinstance(n, ast.Name)
                }
                if "make_maps" in names:
                    calls = {
                        getattr(c.func, "id", "")
                        for c in ast.walk(node)
                        if isinstance(c, ast.Call)
                    }
                    if "_generate_diagnostics" in calls:
                        return
        pytest.fail("_generate_diagnostics call must be gated by make_maps")


class TestMakeMapsBehavior:
    """Behavioral gate — only where yield_outlook's geo deps are importable."""

    def test_renderer_noop_when_disabled(self):
        yo = pytest.importorskip("geocif.yield_outlook")
        saved = yo._MAKE_MAPS
        try:
            yo._MAKE_MAPS = False
            # Passing df_outlook=None would raise if the body ran; the gate
            # must short-circuit to a bare return first.
            assert yo._generate_outlook_map(
                None, None, ["x"], "maize", "null", 2020, 10, "mean", "/tmp"
            ) is None
        finally:
            yo._MAKE_MAPS = saved
