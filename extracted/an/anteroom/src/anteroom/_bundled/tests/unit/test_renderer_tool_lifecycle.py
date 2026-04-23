"""Unit tests for compact tool-call lifecycle helpers (#1364).

Covers:
- ``_humanize_tool_verb_past`` — past-tense verb mapping for completion copy
- ``_completion_metric`` — per-tool short metric extraction
- ``render_tool_call_completion`` — single-line completion surface
- ``configure_live_tools`` — renderer state wiring from config

Follows the same capture-console pattern as ``test_renderer_snapshot.py``:
swap ``renderer.console`` for a non-terminal ``rich.console.Console`` so we
can assert on the exact printed lines.
"""

from __future__ import annotations

import io

import pytest
from rich.console import Console

import anteroom.cli.renderer as renderer

# ``test_renderer.py::TestBugfix617Renderer`` reloads the renderer module via
# ``importlib.reload`` in its setup_method. When that class runs first, the
# ``Verbosity`` Enum class this file imported at top-level becomes a
# different Python object than the one referenced inside the (post-reload)
# helper functions, and identity-sensitive ``==`` comparisons silently fail.
# We re-resolve ``Verbosity`` in the autouse fixture below so the alias
# always matches the live module regardless of collection order.
Verbosity = renderer.Verbosity


@pytest.fixture(autouse=True)
def _clear_no_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)


@pytest.fixture(autouse=True)
def _reset_live_tools_cfg() -> None:  # type: ignore[return]
    """Restore default live_tools config between tests.

    Reset BEFORE the test so state leaked by prior modules (test_renderer.py
    in particular mutates _verbosity through set_verbosity) cannot
    contaminate our expectations. Also re-resolves Verbosity so the enum
    identity matches the live module (see top-of-file note about reloads).
    """
    global Verbosity
    Verbosity = renderer.Verbosity
    renderer.configure_live_tools(
        show_args_in_verbose=True,
        show_metric_suffix=True,
        metric_max_chars=40,
    )
    renderer.set_verbosity(Verbosity.COMPACT)
    yield
    Verbosity = renderer.Verbosity
    renderer.configure_live_tools(
        show_args_in_verbose=True,
        show_metric_suffix=True,
        metric_max_chars=40,
    )
    renderer.set_verbosity(Verbosity.COMPACT)


def _capture() -> tuple[io.StringIO, Console, Console]:
    """Redirect renderer.console to a capturing Console; return (buf, prev_console, prev_stdout)."""
    buf = io.StringIO()
    capture = Console(file=buf, force_terminal=False, width=100, highlight=False)
    prev_console = renderer.console
    prev_stdout = renderer._stdout_console
    renderer.console = capture
    renderer._stdout_console = capture
    return buf, prev_console, prev_stdout


def _restore(prev_console: Console, prev_stdout: Console) -> None:
    renderer.console = prev_console
    renderer._stdout_console = prev_stdout


# ---------------------------------------------------------------------------
# _humanize_tool_verb_past
# ---------------------------------------------------------------------------


class TestHumanizeToolVerbPast:
    def test_read_file(self) -> None:
        assert renderer._humanize_tool_verb_past("read_file") == "Read"

    def test_write_file(self) -> None:
        assert renderer._humanize_tool_verb_past("write_file") == "Wrote"

    def test_edit_file(self) -> None:
        assert renderer._humanize_tool_verb_past("edit_file") == "Edited"

    def test_bash(self) -> None:
        assert renderer._humanize_tool_verb_past("bash") == "Ran"

    def test_grep(self) -> None:
        assert renderer._humanize_tool_verb_past("grep") == "Searched"

    def test_glob_files(self) -> None:
        assert renderer._humanize_tool_verb_past("glob_files") == "Globbed"

    def test_run_agent(self) -> None:
        assert renderer._humanize_tool_verb_past("run_agent") == "Delegated"

    def test_alias_file_read(self) -> None:
        assert renderer._humanize_tool_verb_past("file_read") == "Read"

    def test_unknown_tool_falls_back_to_called(self) -> None:
        assert renderer._humanize_tool_verb_past("mcp.some_custom") == "Called"


# ---------------------------------------------------------------------------
# _completion_metric
# ---------------------------------------------------------------------------


class TestCompletionMetric:
    def test_read_file_lines(self) -> None:
        content = "line1\nline2\nline3"
        assert renderer._completion_metric("read_file", {"content": content}) == "3 lines"

    def test_read_file_single_line(self) -> None:
        assert renderer._completion_metric("read_file", {"content": "only"}) == "1 line"

    def test_read_file_no_content(self) -> None:
        assert renderer._completion_metric("read_file", {}) == ""

    def test_write_file_bytes(self) -> None:
        out = renderer._completion_metric("write_file", {"bytes_written": 2048})
        assert out == "2.0 KB"

    def test_write_file_bytes_small(self) -> None:
        assert renderer._completion_metric("write_file", {"bytes_written": 512}) == "512 B"

    def test_edit_file_lines(self) -> None:
        # Fallback when no structured counts: treat content as new file content
        content = "a\nb\nc\nd"
        assert renderer._completion_metric("edit_file", {"content": content}) == "4 lines"

    def test_bash_exit_code_zero(self) -> None:
        assert renderer._completion_metric("bash", {"exit_code": 0}) == "exit 0"

    def test_bash_exit_code_nonzero(self) -> None:
        assert renderer._completion_metric("bash", {"exit_code": 1}) == "exit 1"

    def test_bash_without_exit_code_stdout(self) -> None:
        assert renderer._completion_metric("bash", {"stdout": "one\ntwo\nthree"}) == "3 lines stdout"

    def test_grep_match_count(self) -> None:
        assert renderer._completion_metric("grep", {"matches": 17}) == "17 matches"

    def test_glob_files_count(self) -> None:
        assert renderer._completion_metric("glob_files", {"files": ["a.py", "sub/", "c.py"]}) == "3 paths"

    def test_clamp_to_metric_max(self) -> None:
        renderer.configure_live_tools(
            show_args_in_verbose=True,
            show_metric_suffix=True,
            metric_max_chars=5,
        )
        out = renderer._completion_metric("bash", {"stdout": "a\nb\nc\nd\ne\nf\ng\nh\ni\nj"})
        assert len(out) <= 5

    def test_disabled_returns_empty(self) -> None:
        renderer.configure_live_tools(
            show_args_in_verbose=True,
            show_metric_suffix=False,
            metric_max_chars=40,
        )
        assert renderer._completion_metric("read_file", {"content": "x"}) == ""

    def test_non_dict_output(self) -> None:
        assert renderer._completion_metric("bash", None) == ""
        assert renderer._completion_metric("bash", "string output") == ""

    def test_mcp_unknown_tool_no_keys(self) -> None:
        # Arbitrary dict without recognized keys produces empty (no crash)
        assert renderer._completion_metric("mcp.custom", {"foo": "bar"}) == ""


# ---------------------------------------------------------------------------
# render_tool_call_completion
# ---------------------------------------------------------------------------


class TestRenderToolCallCompletion:
    def test_success_compact_line(self) -> None:
        buf, pc, ps = _capture()
        try:
            renderer.render_tool_call_completion(
                "read_file",
                "success",
                elapsed=0.3,
                arguments={"path": "src/foo.py"},
                output={"content": "a\nb\nc"},
            )
        finally:
            _restore(pc, ps)
        out = buf.getvalue()
        assert "Read" in out or "Reading" in out
        assert "\u2713" in out  # ✓
        # gutter glyph
        assert "\u2502" in out

    def test_failure_line_uses_error_icon(self) -> None:
        buf, pc, ps = _capture()
        try:
            renderer.render_tool_call_completion(
                "bash",
                "error",
                elapsed=1.2,
                arguments={"command": "ls /nope"},
                output={"error": "No such file", "exit_code": 2},
            )
        finally:
            _restore(pc, ps)
        out = buf.getvalue()
        assert "\u2717" in out  # ✗
        assert "\u2502" in out  # gutter

    def test_failure_line_includes_error_summary(self) -> None:
        buf, pc, ps = _capture()
        try:
            renderer.render_tool_call_completion(
                "bash",
                "error",
                elapsed=0.5,
                arguments={"command": "exit 1"},
                output={"error": "failed badly"},
            )
        finally:
            _restore(pc, ps)
        out = buf.getvalue()
        assert "failed badly" in out

    def test_short_elapsed_suppressed(self) -> None:
        """Elapsed < 0.1s should NOT include an elapsed suffix."""
        buf, pc, ps = _capture()
        try:
            renderer.render_tool_call_completion(
                "read_file",
                "success",
                elapsed=0.05,
                arguments={"path": "foo.py"},
                output={"content": "x"},
            )
        finally:
            _restore(pc, ps)
        out = buf.getvalue()
        # Some output, but no "0.0s" suffix
        assert out.strip() != ""
        assert "0.0s" not in out

    def test_verbose_emits_args_footline_when_enabled(self) -> None:
        renderer.set_verbosity(Verbosity.VERBOSE)
        renderer.configure_live_tools(
            show_args_in_verbose=True,
            show_metric_suffix=True,
            metric_max_chars=40,
        )
        # Sanity dump
        import sys as _sys

        _sys.stderr.write(
            f"\nDEBUG pre-call: _verbosity={renderer._verbosity} "
            f"cfg={renderer._live_tools_state} "
            f"theme.chrome={renderer._theme.chrome!r}\n"
        )
        buf, pc, ps = _capture()
        try:
            renderer.render_tool_call_completion(
                "bash",
                "success",
                elapsed=0.4,
                arguments={"command": "echo hi"},
                output={"stdout": "hi", "exit_code": 0},
            )
        finally:
            _restore(pc, ps)
        out = buf.getvalue()
        _sys.stderr.write(f"DEBUG out={out!r}\n")
        assert "args:" in out
        assert '"command"' in out

    def test_verbose_no_args_when_disabled(self) -> None:
        renderer.set_verbosity(Verbosity.VERBOSE)
        renderer.configure_live_tools(
            show_args_in_verbose=False,
            show_metric_suffix=True,
            metric_max_chars=40,
        )
        buf, pc, ps = _capture()
        try:
            renderer.render_tool_call_completion(
                "bash",
                "success",
                elapsed=0.4,
                arguments={"command": "echo hi"},
                output={"stdout": "hi", "exit_code": 0},
            )
        finally:
            _restore(pc, ps)
        out = buf.getvalue()
        # No args footline when disabled
        assert "args:" not in out
        # Completion line still rendered — just no args footline
        assert "\u2713" in out

    def test_compact_mode_no_args_footline_even_with_flag(self) -> None:
        """Args footline is VERBOSE-only regardless of flag."""
        renderer.set_verbosity(Verbosity.COMPACT)
        renderer.configure_live_tools(
            show_args_in_verbose=True,
            show_metric_suffix=True,
            metric_max_chars=40,
        )
        buf, pc, ps = _capture()
        try:
            renderer.render_tool_call_completion(
                "bash",
                "success",
                elapsed=0.4,
                arguments={"command": "echo hi"},
                output={"stdout": "hi", "exit_code": 0},
            )
        finally:
            _restore(pc, ps)
        out = buf.getvalue()
        # No args footline in compact mode regardless of flag
        assert "args:" not in out

    def test_metric_shown_when_enabled(self) -> None:
        renderer.set_verbosity(Verbosity.COMPACT)
        renderer.configure_live_tools(
            show_args_in_verbose=True,
            show_metric_suffix=True,
            metric_max_chars=40,
        )
        buf, pc, ps = _capture()
        try:
            renderer.render_tool_call_completion(
                "read_file",
                "success",
                elapsed=0.5,
                arguments={"path": "foo.py"},
                output={"content": "a\nb\nc\nd\ne"},
            )
        finally:
            _restore(pc, ps)
        out = buf.getvalue()
        assert "5 lines" in out

    def test_metric_hidden_when_disabled(self) -> None:
        renderer.set_verbosity(Verbosity.COMPACT)
        renderer.configure_live_tools(
            show_args_in_verbose=True,
            show_metric_suffix=False,
            metric_max_chars=40,
        )
        buf, pc, ps = _capture()
        try:
            renderer.render_tool_call_completion(
                "read_file",
                "success",
                elapsed=0.5,
                arguments={"path": "foo.py"},
                output={"content": "a\nb\nc\nd\ne"},
            )
        finally:
            _restore(pc, ps)
        out = buf.getvalue()
        assert "5 lines" not in out


# ---------------------------------------------------------------------------
# configure_live_tools
# ---------------------------------------------------------------------------


class TestConfigureLiveTools:
    def test_defaults(self) -> None:
        renderer.configure_live_tools(
            show_args_in_verbose=True,
            show_metric_suffix=True,
            metric_max_chars=40,
        )
        cfg = renderer.get_live_tools_config()
        assert cfg.show_args_in_verbose is True
        assert cfg.show_metric_suffix is True
        assert cfg.metric_max_chars == 40

    def test_overrides(self) -> None:
        renderer.configure_live_tools(
            show_args_in_verbose=False,
            show_metric_suffix=False,
            metric_max_chars=12,
        )
        cfg = renderer.get_live_tools_config()
        assert cfg.show_args_in_verbose is False
        assert cfg.show_metric_suffix is False
        assert cfg.metric_max_chars == 12
