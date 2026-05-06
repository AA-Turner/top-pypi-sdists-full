import shutil
import subprocess
import textwrap

import pytest

from abstra_internals.agents.tools.browser import _wrap_for_safe_eval


def _node_check(snippet: str) -> subprocess.CompletedProcess:
    """Ask Node to parse the snippet and return the result.

    We pipe through `--check` because that only validates syntax without
    running anything (so DOM globals don't need to exist).
    """
    return subprocess.run(
        ["node", "--check"],
        input=snippet,
        capture_output=True,
        text=True,
    )


_NODE_AVAILABLE = shutil.which("node") is not None
needs_node = pytest.mark.skipif(not _NODE_AVAILABLE, reason="node not installed")


class TestWrapForSafeEval:
    """The wrapper takes the user's script verbatim and injects it into an
    async IIFE inside the safe-eval helper. We don't try to be clever
    about expression-vs-statement — the agent is expected to use
    `return X;` to surface values."""

    def test_injects_script_verbatim(self):
        wrapped = _wrap_for_safe_eval("return 42;")
        assert "return 42;" in wrapped

    def test_wraps_in_async_iife(self):
        wrapped = _wrap_for_safe_eval("return 42;")
        assert wrapped.startswith("(") and wrapped.endswith(")()")
        assert "async () => { return 42; }" in wrapped

    def test_no_heuristic_for_pure_expression(self):
        # `42` is a valid expression but the wrapper does NOT insert an
        # implicit return — agents must write `return 42;` to get the value.
        wrapped = _wrap_for_safe_eval("42")
        assert "async () => { 42 }" in wrapped

    @needs_node
    def test_statements_with_trailing_semicolon_dont_syntax_error(self):
        # c09 regression: an earlier version produced `;);` at the boundary
        # and crashed every JS call with `SyntaxError: Unexpected token ';'`.
        wrapped = _wrap_for_safe_eval("setInterval(fn, 50);")
        result = _node_check(wrapped)
        assert result.returncode == 0, result.stderr

    @needs_node
    def test_multistatement_with_return_is_valid(self):
        wrapped = _wrap_for_safe_eval("const x = 1;\nreturn x;")
        result = _node_check(wrapped)
        assert result.returncode == 0, result.stderr

    @needs_node
    def test_pure_expression_is_valid_js(self):
        wrapped = _wrap_for_safe_eval("42")
        result = _node_check(wrapped)
        assert result.returncode == 0, result.stderr

    @needs_node
    def test_iife_input_does_not_double_wrap_unsafely(self):
        wrapped = _wrap_for_safe_eval("(async () => { return 42; })()")
        result = _node_check(wrapped)
        assert result.returncode == 0, result.stderr

    @needs_node
    def test_script_with_window_open_is_valid(self):
        # c17 / circular-reference regression: window.open returns an object
        # full of cycles; the wrapper must keep producing valid JS for it.
        wrapped = _wrap_for_safe_eval(
            textwrap.dedent(
                """
                window.open('http://example.com/x', '_blank');
                """
            ).strip()
        )
        result = _node_check(wrapped)
        assert result.returncode == 0, result.stderr
