"""Integration tests for the compact tool-call lifecycle in the REPL (#1364).

Drives ``render_tool_call_start`` → ``render_tool_call_end`` sequences
against a captured Rich console (footer mode disabled — the parallel
thinking ticker is not part of these scenarios) and asserts on the
printed lines.

These are integration tests in the sense that they exercise the full
tool-call event path end-to-end: history bookkeeping, dedup accumulator,
inline diff routing, VERBOSE args footline, and parallel-out-of-order
completion. They run without a PTY because the scenarios don't depend
on terminal-level semantics.
"""

from __future__ import annotations

import io
import time
from typing import Any

import pytest
from rich.console import Console

import anteroom.cli.renderer as renderer

# Resolve Verbosity lazily via the live module — sibling unit tests reload
# the renderer module, which would otherwise leave us with a stale enum
# class whose identity no longer matches the live module's references.
Verbosity = renderer.Verbosity


@pytest.fixture(autouse=True)
def _isolate_renderer_state(monkeypatch: pytest.MonkeyPatch) -> Any:
    """Isolate renderer module state between tests."""
    monkeypatch.delenv("NO_COLOR", raising=False)

    # Re-resolve Verbosity against the live module (sibling tests may have
    # reloaded the module and invalidated the top-level alias).
    global Verbosity
    Verbosity = renderer.Verbosity

    prev_console = renderer.console
    prev_stdout = renderer._stdout_console
    prev_verbosity = renderer.get_verbosity()
    prev_live_tools = renderer.get_live_tools_config()
    prev_dedup = renderer._tool_dedup_enabled

    # Reset transient per-turn state
    renderer._current_turn_tools.clear()
    renderer._dedup_key = ""
    renderer._dedup_count = 0
    renderer._dedup_first_summary = ""
    renderer._dedup_summary = ""
    renderer._tool_batch_active = False
    renderer._reset_tool_phase()
    renderer.set_verbosity(Verbosity.COMPACT)
    renderer.configure_live_tools(
        show_args_in_verbose=True,
        show_metric_suffix=True,
        metric_max_chars=40,
    )

    try:
        yield
    finally:
        renderer.console = prev_console
        renderer._stdout_console = prev_stdout
        renderer.set_verbosity(prev_verbosity)
        renderer.configure_live_tools(
            show_args_in_verbose=prev_live_tools.show_args_in_verbose,
            show_metric_suffix=prev_live_tools.show_metric_suffix,
            metric_max_chars=prev_live_tools.metric_max_chars,
        )
        renderer._tool_dedup_enabled = prev_dedup
        renderer._current_turn_tools.clear()
        renderer._dedup_key = ""
        renderer._dedup_count = 0
        renderer._dedup_first_summary = ""
        renderer._dedup_summary = ""
        renderer._tool_batch_active = False
        renderer._reset_tool_phase()


def _swap_console() -> io.StringIO:
    """Redirect renderer console to a fresh StringIO Console and return the buffer."""
    buf = io.StringIO()
    capture = Console(file=buf, force_terminal=False, width=120, highlight=False)
    renderer.console = capture
    renderer._stdout_console = capture
    return buf


def _bump_start_back(seconds: float = 0.5) -> None:
    """Shift the most recent start_time back so elapsed is non-zero."""
    if renderer._current_turn_tools:
        entry = renderer._current_turn_tools[-1]
        entry["start_time"] = time.monotonic() - seconds
    renderer._tool_start = time.monotonic() - seconds


class TestNoPreStartBreadcrumb:
    """#1364: render_tool_call_start no longer prints a ``> tool(args)`` line."""

    def test_compact_start_no_breadcrumb(self) -> None:
        buf = _swap_console()
        renderer.render_tool_call_start("bash", {"command": "ls"})
        # Only spacing lines allowed; no "> bash(" text
        out = buf.getvalue()
        assert "> bash" not in out
        # stop the ticker so asyncio doesn't leak
        renderer.stop_tool_ticker_sync()

    def test_verbose_start_no_breadcrumb(self) -> None:
        renderer.set_verbosity(Verbosity.VERBOSE)
        buf = _swap_console()
        renderer.render_tool_call_start("bash", {"command": "ls -la"})
        out = buf.getvalue()
        assert "> bash" not in out
        assert "ls -la" not in out  # pre-start args not printed
        renderer.stop_tool_ticker_sync()


class TestSingleCompletionLine:
    """#1364: end prints exactly one completion line in compact mode."""

    def test_success_single_line(self) -> None:
        buf = _swap_console()
        renderer.render_tool_call_start("read_file", {"path": "src/foo.py"})
        _bump_start_back(0.3)
        renderer.render_tool_call_end(
            "read_file",
            "success",
            {"content": "alpha\nbeta\ngamma"},
        )
        out = buf.getvalue()
        # One completion line
        lines = [ln for ln in out.splitlines() if ln.strip()]
        # The first line may be a blank spacing, completion line follows.
        completion_lines = [ln for ln in lines if "\u2713" in ln or "\u2717" in ln]
        assert len(completion_lines) == 1
        assert "\u2713" in completion_lines[0]
        assert "Read" in completion_lines[0]
        assert "3 lines" in completion_lines[0]
        # Gutter
        assert "\u2502" in completion_lines[0]

    def test_glob_files_counts_directories(self) -> None:
        buf = _swap_console()
        renderer.render_tool_call_start("glob_files", {"pattern": "*"})
        _bump_start_back(0.2)
        renderer.render_tool_call_end(
            "glob_files",
            "success",
            {"files": ["a.py", "sub/", "c.py"]},
        )
        out = buf.getvalue()
        completion_lines = [ln for ln in out.splitlines() if "\u2713" in ln or "\u2717" in ln]
        assert len(completion_lines) == 1
        assert "Globbed" in completion_lines[0]
        assert "3 paths" in completion_lines[0]

    def test_failure_has_error_icon_and_summary(self) -> None:
        buf = _swap_console()
        renderer.render_tool_call_start("bash", {"command": "ls /nope"})
        _bump_start_back(1.2)
        renderer.render_tool_call_end(
            "bash",
            "error",
            {"error": "No such file or directory", "exit_code": 2},
        )
        out = buf.getvalue()
        assert "\u2717" in out  # ✗
        assert "No such file" in out


class TestVerboseArgsFootline:
    def test_args_footline_enabled(self) -> None:
        renderer.set_verbosity(Verbosity.VERBOSE)
        renderer.configure_live_tools(
            show_args_in_verbose=True,
            show_metric_suffix=True,
            metric_max_chars=40,
        )
        buf = _swap_console()
        renderer.render_tool_call_start("bash", {"command": "echo hi"})
        _bump_start_back(0.2)
        renderer.render_tool_call_end(
            "bash",
            "success",
            {"stdout": "hi\n", "exit_code": 0},
        )
        out = buf.getvalue()
        assert "args:" in out
        assert '"command"' in out

    def test_args_footline_disabled(self) -> None:
        renderer.set_verbosity(Verbosity.VERBOSE)
        renderer.configure_live_tools(
            show_args_in_verbose=False,
            show_metric_suffix=True,
            metric_max_chars=40,
        )
        buf = _swap_console()
        renderer.render_tool_call_start("bash", {"command": "echo hi"})
        _bump_start_back(0.2)
        renderer.render_tool_call_end(
            "bash",
            "success",
            {"stdout": "hi\n", "exit_code": 0},
        )
        out = buf.getvalue()
        assert "args:" not in out
        # Completion line still rendered
        assert "\u2713" in out


class TestDedupCollapsesConsecutive:
    """Dedup accumulator still collapses consecutive similar tool calls."""

    def test_three_consecutive_edits_collapse(self) -> None:
        buf = _swap_console()
        for path in ("a.py", "b.py", "c.py"):
            renderer.render_tool_call_start("edit_file", {"path": path})
            _bump_start_back(0.1)
            renderer.render_tool_call_end(
                "edit_file",
                "success",
                {"content": "ok"},
            )
        out = buf.getvalue()
        # First call prints a completion line; second and third should be
        # absorbed and produce no additional per-line ✓ until a flush.
        completion_count = out.count("\u2713")
        assert completion_count == 1
        # Dedup state accumulated
        assert renderer._dedup_count == 3


class TestDiffPathWinsForEditSuccess:
    """File-modifying tool with ``_new_content`` goes through diff rendering, not completion."""

    def test_edit_file_with_diff_data_uses_diff_path(self) -> None:
        buf = _swap_console()
        renderer.render_tool_call_start("edit_file", {"path": "src/foo.py"})
        _bump_start_back(0.2)
        renderer.render_tool_call_end(
            "edit_file",
            "success",
            {
                "_old_content": "old\nlines\n",
                "_new_content": "new\nlines\n",
                "path": "src/foo.py",
            },
        )
        out = buf.getvalue()
        # Diff path emits "Update(...)" header and does NOT use the unified
        # completion line, so no "Edited" text should appear.
        assert "Edited" not in out
        # But diff path does use its own bullet marker
        assert "Update" in out


class TestParallelOutOfOrderCompletion:
    """Each parallel tool gets exactly one completion line regardless of finish order."""

    def test_three_tools_one_completion_line_each(self) -> None:
        buf = _swap_console()
        # Start three tools in order
        renderer.render_tool_call_start("read_file", {"path": "a.py"})
        _bump_start_back(0.3)
        renderer.render_tool_call_start("bash", {"command": "ls"})
        _bump_start_back(0.3)
        renderer.render_tool_call_start("grep", {"pattern": "foo"})
        _bump_start_back(0.3)

        # Complete in reverse order
        renderer.render_tool_call_end("grep", "success", {"matches": 4})
        renderer.render_tool_call_end("bash", "success", {"stdout": "a\nb", "exit_code": 0})
        renderer.render_tool_call_end("read_file", "success", {"content": "x\ny\nz"})

        out = buf.getvalue()
        completion_count = out.count("\u2713")
        # All three produce completion lines (none are dedup-collapsed since
        # they have different dedup keys)
        assert completion_count == 3
        # History captured all three
        assert len(renderer._current_turn_tools) == 3
        tool_names = [e["tool_name"] for e in renderer._current_turn_tools]
        assert set(tool_names) == {"read_file", "bash", "grep"}
