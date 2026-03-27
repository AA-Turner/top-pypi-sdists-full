"""Advanced renderer tests: dedup, plan, subagent, and diff rendering (#1021)."""

from __future__ import annotations

import re
from io import StringIO
from unittest.mock import patch

from rich.console import Console

from anteroom.cli.renderer import (
    Verbosity,
    _dedup_flush_label,
    _flush_dedup,
    _has_diff_data,
    _render_inline_diff,
    clear_plan,
    clear_subagent_state,
    get_plan_steps,
    is_plan_visible,
    render_subagent_end,
    render_subagent_start,
    render_subagent_tool,
    render_tool_call_end,
    render_tool_call_start,
    set_tool_dedup,
    set_verbosity,
    start_plan,
    update_plan_step,
)


def _strip_ansi(text: str) -> str:
    """Strip ANSI escape sequences for plain text assertions."""
    return re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", text)


class TestToolDedupFlushing:
    """Tool dedup: same key increments count, different key flushes previous."""

    def setup_method(self) -> None:
        set_verbosity(Verbosity.COMPACT)
        set_tool_dedup(True)
        clear_plan()
        # Reset dedup state
        _flush_dedup()

    def test_same_key_increments_count(self) -> None:
        buf = StringIO()
        test_console = Console(file=buf, force_terminal=True)
        with patch("anteroom.cli.renderer.console", test_console):
            render_tool_call_start("read_file", {"path": "/a.py"})
            render_tool_call_end("read_file", "success", {"content": "hello"})
            render_tool_call_start("read_file", {"path": "/b.py"})
            render_tool_call_end("read_file", "success", {"content": "world"})

        output = buf.getvalue()
        # First call renders, second deduped (no second line printed)
        assert "Reading" in output
        # The count should increment silently; only flush reveals total

    def test_different_key_flushes_previous(self) -> None:
        buf = StringIO()
        test_console = Console(file=buf, force_terminal=True)
        with patch("anteroom.cli.renderer.console", test_console):
            render_tool_call_start("read_file", {"path": "/a.py"})
            render_tool_call_end("read_file", "success", {"content": "hello"})
            render_tool_call_start("read_file", {"path": "/b.py"})
            render_tool_call_end("read_file", "success", {"content": "world"})
            # Now a different tool type triggers flush
            render_tool_call_start("bash", {"command": "ls"})
            render_tool_call_end("bash", "success", {"stdout": "output"})

        plain = _strip_ansi(buf.getvalue())
        assert "read 2 files total" in plain
        assert "bash" in plain.lower()

    def test_dedup_flush_label_editing(self) -> None:
        label = _dedup_flush_label("Editing", 5)
        assert "edited" in label
        assert "5" in label
        assert "files" in label

    def test_dedup_flush_label_bash(self) -> None:
        label = _dedup_flush_label("bash", 3)
        assert "ran" in label
        assert "3" in label
        assert "times" in label


class TestPlanChecklist:
    """Plan start, step update, and visibility."""

    def setup_method(self) -> None:
        clear_plan()

    def test_start_plan_creates_steps(self) -> None:
        start_plan(["Step 1", "Step 2", "Step 3"])
        steps = get_plan_steps()
        assert len(steps) == 3
        assert steps[0]["text"] == "Step 1"
        assert steps[0]["status"] == "pending"
        assert is_plan_visible()

    def test_update_plan_step_complete(self) -> None:
        start_plan(["Build", "Test", "Deploy"])
        update_plan_step(0, "complete")
        steps = get_plan_steps()
        assert steps[0]["status"] == "complete"
        assert steps[1]["status"] == "pending"

    def test_update_plan_step_in_progress(self) -> None:
        start_plan(["Build", "Test"])
        update_plan_step(1, "in_progress")
        steps = get_plan_steps()
        assert steps[1]["status"] == "in_progress"

    def test_clear_plan_resets_state(self) -> None:
        start_plan(["Step 1"])
        assert is_plan_visible()
        clear_plan()
        assert not is_plan_visible()
        assert get_plan_steps() == []


class TestSubagentRendering:
    """Subagent start/tool/end events."""

    def setup_method(self) -> None:
        clear_subagent_state()

    def test_subagent_start_and_end(self) -> None:
        buf = StringIO()
        test_console = Console(file=buf, force_terminal=True)
        with patch("anteroom.cli.renderer.console", test_console):
            render_subagent_start("agent-1", "Analyze the code", "gpt-4o", depth=1)
            render_subagent_end("agent-1", elapsed=2.5, tool_calls=["read_file", "grep"])

        plain = _strip_ansi(buf.getvalue())
        assert "agent-1" in plain
        assert "Analyze the code" in plain
        assert "2.5s" in plain
        assert "2 tool calls" in plain

    def test_subagent_with_error(self) -> None:
        buf = StringIO()
        test_console = Console(file=buf, force_terminal=True)
        with patch("anteroom.cli.renderer.console", test_console):
            render_subagent_start("agent-2", "Try something", "gpt-4o", depth=1)
            render_subagent_end("agent-2", elapsed=1.0, tool_calls=[], error="Timeout exceeded")

        plain = _strip_ansi(buf.getvalue())
        assert "failed" in plain
        assert "Timeout exceeded" in plain

    def test_subagent_tool_breadcrumb(self) -> None:
        buf = StringIO()
        test_console = Console(file=buf, force_terminal=True)
        with patch("anteroom.cli.renderer.console", test_console):
            render_subagent_start("agent-3", "Read files", "gpt-4o", depth=2)
            render_subagent_tool("agent-3", "read_file", {"path": "/test.py"})

        plain = _strip_ansi(buf.getvalue())
        assert "Reading" in plain

    def test_subagent_depth_indentation(self) -> None:
        buf = StringIO()
        test_console = Console(file=buf, force_terminal=True)
        with patch("anteroom.cli.renderer.console", test_console):
            render_subagent_start("deep-agent", "Nested task", "gpt-4o", depth=3)
            render_subagent_end("deep-agent", elapsed=0.5, tool_calls=["bash"])

        plain = _strip_ansi(buf.getvalue())
        assert "deep-agent" in plain
        assert "1 tool call" in plain  # singular


class TestDiffRendering:
    """Inline diff detection and rendering."""

    def test_has_diff_data_with_new_content(self) -> None:
        assert _has_diff_data("write_file", {"_new_content": "hello"})

    def test_has_diff_data_with_old_content(self) -> None:
        assert _has_diff_data("edit_file", {"_old_content": "before"})

    def test_has_diff_data_wrong_tool(self) -> None:
        assert not _has_diff_data("bash", {"_new_content": "hello"})

    def test_has_diff_data_no_content(self) -> None:
        assert not _has_diff_data("write_file", {"path": "/test.py"})

    def test_render_inline_diff_shows_changes(self) -> None:
        buf = StringIO()
        test_console = Console(file=buf, force_terminal=True)
        output = {
            "_old_content": "line1\nline2\nline3\n",
            "_new_content": "line1\nmodified\nline3\n",
            "path": "/test.py",
        }
        with patch("anteroom.cli.renderer.console", test_console):
            _render_inline_diff("edit_file", output)

        rendered = buf.getvalue()
        assert "Update" in rendered
        assert "test.py" in rendered

    def test_render_inline_diff_created_file(self) -> None:
        buf = StringIO()
        test_console = Console(file=buf, force_terminal=True)
        output = {
            "action": "created",
            "lines": 10,
            "path": "/new_file.py",
        }
        with patch("anteroom.cli.renderer.console", test_console):
            _render_inline_diff("write_file", output)

        rendered = buf.getvalue()
        assert "Write" in rendered
        assert "Created" in rendered
        assert "10 lines" in rendered
