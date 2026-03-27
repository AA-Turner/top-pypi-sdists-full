"""Tests for live transcript rendering in workflow CLI (#1117).

Tests the _print_transcript_line helper and --no-transcript suppression.
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from anteroom.cli.workflow_cli import _print_transcript_line


class TestPrintTranscriptLine:
    """Tests for the _print_transcript_line helper function."""

    def test_stdout_rendered(self) -> None:
        """transcript_stdout renders with [stdout] prefix."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line("transcript_stdout", {"content": "hello world"})
        assert "stdout" in output.getvalue()
        assert "hello world" in output.getvalue()

    def test_stderr_rendered(self) -> None:
        """transcript_stderr renders with [stderr] prefix."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line("transcript_stderr", {"content": "error msg"})
        assert "stderr" in output.getvalue()
        assert "error msg" in output.getvalue()

    def test_assistant_rendered(self) -> None:
        """transcript_assistant renders with [assistant] prefix."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line("transcript_assistant", {"content": "I will help"})
        assert "assistant" in output.getvalue()
        assert "I will help" in output.getvalue()

    def test_prompt_rendered(self) -> None:
        """transcript_prompt renders a compact prompt preview."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line(
                "transcript_prompt",
                {"content": "Investigate issue 1092 and update the plan body.", "chars": 48},
            )
        text = output.getvalue()
        assert "prompt" in text
        assert "Investigate issue 1092" in text

    def test_tool_call_rendered(self) -> None:
        """transcript_tool_call renders with [tool_call] prefix."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line(
                "transcript_tool_call",
                {"tool_name": "bash", "arguments": "{'command': 'echo hi'}"},
            )
        assert "tool_call" in output.getvalue()
        assert "bash" in output.getvalue()
        assert "echo hi" in output.getvalue()

    def test_tool_result_rendered(self) -> None:
        """transcript_tool_result renders with [tool_result] prefix."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line(
                "transcript_tool_result",
                {"tool_name": "bash", "output": "{'stdout': 'hi', 'exit_code': 0}"},
            )
        assert "tool_result" in output.getvalue()
        assert "bash" in output.getvalue()
        assert "hi" in output.getvalue()

    def test_rich_markup_escaped(self) -> None:
        """Content with Rich markup characters is escaped, not interpreted."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line("transcript_stdout", {"content": "[bold]not bold[/bold]"})
        text = output.getvalue()
        # The brackets should be escaped so Rich doesn't interpret them
        assert "\\[bold]" in text or "\\[/bold]" in text

    def test_empty_content_skipped(self) -> None:
        """Empty content doesn't print anything."""
        printed = False

        with patch("anteroom.cli.workflow_cli.console") as mock_console:

            def _track_print(*a: Any, **k: Any) -> None:
                nonlocal printed
                printed = True

            mock_console.print = _track_print
            _print_transcript_line("transcript_stdout", {"content": ""})

        assert not printed

    def test_long_content_truncated(self) -> None:
        """Lines longer than 200 chars are truncated."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line("transcript_stdout", {"content": "x" * 300})
        text = output.getvalue()
        assert "..." in text

    def test_assistant_multiline_shows_first_line(self) -> None:
        """Multiline assistant content shows only the first line."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line(
                "transcript_assistant",
                {"content": "First line\nSecond line\nThird line"},
            )
        text = output.getvalue()
        assert "First line" in text
        assert "Second line" not in text

    def test_bash_cd_prefix_suppressed_in_tool_call(self) -> None:
        """Large worktree prefixes are removed from bash transcript summaries."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line(
                "transcript_tool_call",
                {
                    "tool_name": "bash",
                    "arguments": (
                        "{'command': 'cd /Users/troy/dev/github/troylar/anteroom-1092-worktree && "
                        "gh issue view 1092 --json body'}"
                    ),
                },
            )
        text = output.getvalue()
        assert "gh issue view 1092" in text
        assert "cd /Users/troy" not in text

    def test_read_file_tool_result_collapsed_to_stats(self) -> None:
        """read_file tool results summarize file path and size instead of dumping content."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line(
                "transcript_tool_result",
                {
                    "tool_name": "read_file",
                    "output": (
                        "{'path': '/Users/troy/dev/github/troylar/anteroom/CLAUDE.md', "
                        "'content': 'line 1\\nline 2\\nline 3'}"
                    ),
                },
            )
        text = output.getvalue()
        assert "CLAUDE.md" in text
        assert "line 1" not in text
        assert "lines" in text or "chars" in text

    def test_glob_files_tool_result_shows_count(self) -> None:
        """glob_files tool results summarize counts and a few names."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line(
                "transcript_tool_result",
                {
                    "tool_name": "glob_files",
                    "output": ("{'files': ['/tmp/a.py', '/tmp/b.py', '/tmp/c.py', '/tmp/d.py']}"),
                },
            )
        text = output.getvalue()
        assert "4 files" in text
        assert "a.py" in text
        assert "(+1)" in text

    def test_bash_tool_result_json_output_collapsed(self) -> None:
        """bash tool results that return JSON are summarized as JSON output stats."""
        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_transcript_line(
                "transcript_tool_result",
                {
                    "tool_name": "bash",
                    "output": (
                        "{'stdout': '{\"body\":\"example\",\"title\":\"Issue\"}', 'stderr': '', 'exit_code': 0}"
                    ),
                },
            )
        text = output.getvalue()
        assert "JSON output" in text
        assert "body" not in text


class TestTranscriptEdgeCases:
    """Edge case tests for _print_transcript_line."""

    def test_unknown_event_type_silent(self) -> None:
        """Unknown transcript event types (e.g. transcript_usage) are silently dropped."""
        printed = False

        with patch("anteroom.cli.workflow_cli.console") as mock_console:

            def _track_print(*a: Any, **k: Any) -> None:
                nonlocal printed
                printed = True

            mock_console.print = _track_print
            _print_transcript_line("transcript_usage", {"prompt_tokens": 100})

        assert not printed

    def test_empty_tool_call_skipped(self) -> None:
        """Empty tool_call payload doesn't print."""
        printed = False

        with patch("anteroom.cli.workflow_cli.console") as mock_console:

            def _track_print(*a: Any, **k: Any) -> None:
                nonlocal printed
                printed = True

            mock_console.print = _track_print
            _print_transcript_line("transcript_tool_call", {"tool_name": "", "arguments": ""})

        assert not printed

    def test_empty_tool_result_skipped(self) -> None:
        """Empty tool_result payload doesn't print."""
        printed = False

        with patch("anteroom.cli.workflow_cli.console") as mock_console:

            def _track_print(*a: Any, **k: Any) -> None:
                nonlocal printed
                printed = True

            mock_console.print = _track_print
            _print_transcript_line("transcript_tool_result", {"tool_name": "", "output": ""})

        assert not printed


class TestMakeProgressCallback:
    """Test the shared _make_progress_callback factory."""

    def test_transcript_suppressed_when_disabled(self) -> None:
        """With show_transcript=False, transcript events are not forwarded."""
        from anteroom.cli.workflow_cli import _make_progress_callback

        printed = False

        with patch("anteroom.cli.workflow_cli.console") as mock_console:

            def _track_print(*a: Any, **k: Any) -> None:
                nonlocal printed
                printed = True

            mock_console.print = _track_print
            cb = _make_progress_callback(show_transcript=False)
            cb("transcript_stdout", "step1", {"content": "should not print"})

        assert not printed

    def test_transcript_shown_when_enabled(self) -> None:
        """With show_transcript=True, transcript events are forwarded."""
        from anteroom.cli.workflow_cli import _make_progress_callback

        output = StringIO()

        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            cb = _make_progress_callback(show_transcript=True)
            cb("transcript_stdout", "step1", {"content": "visible output"})

        assert "visible output" in output.getvalue()

    def test_step_failed_shows_reason_summary(self) -> None:
        """Failed step progress prints a dedicated reason line."""
        from anteroom.cli.workflow_cli import _make_progress_callback

        output = StringIO()

        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            cb = _make_progress_callback(show_transcript=True)
            cb("step_failed", "implement_issue", {"summary": "Max iterations (15) reached"})

        text = output.getvalue()
        assert "implement_issue" in text
        assert "reason:" in text
        assert "Max iterations (15) reached" in text


class TestNoTranscriptFlag:
    """Test that --no-transcript suppresses transcript in progress callbacks."""

    def test_no_transcript_attr_parsed(self) -> None:
        """Verify argparse produces no_transcript attribute."""
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("--no-transcript", action="store_true", default=False)
        args = parser.parse_args(["--no-transcript"])
        assert args.no_transcript is True

    def test_default_transcript_enabled(self) -> None:
        """Without --no-transcript, transcript is enabled by default."""
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("--no-transcript", action="store_true", default=False)
        args = parser.parse_args([])
        assert args.no_transcript is False


class TestCreateEngineSafetyConfig:
    def test_create_engine_applies_safety_config_to_tool_registry(self) -> None:
        from anteroom.cli.workflow_cli import _create_engine

        config = MagicMock()
        config.ai = MagicMock()
        config.workflow = MagicMock()
        config.workflow.credentials = None
        config.safety = MagicMock()
        config.app.data_dir = Path("/tmp/anteroom-tests")
        db = MagicMock()

        mock_tool_reg = MagicMock()
        mock_engine = MagicMock()

        with (
            patch("anteroom.services.ai_service.create_ai_service", return_value=MagicMock()),
            patch("anteroom.tools.ToolRegistry", return_value=mock_tool_reg),
            patch("anteroom.tools.register_default_tools"),
            patch("anteroom.services.workflow_runners.create_default_registry", return_value=MagicMock()),
            patch("anteroom.services.workflow_engine.WorkflowEngine", return_value=mock_engine),
        ):
            engine, _event_bus = _create_engine(config, db)

        assert engine is mock_engine
        mock_tool_reg.set_safety_config.assert_called_once_with(config.safety, working_dir=str(Path.cwd()))


# ---------------------------------------------------------------------------
# Emit step rendering (#1150)
# ---------------------------------------------------------------------------


class TestEmitEventRendering:
    """Tests for step_emitted event rendering in progress callback and watch."""

    def test_progress_callback_renders_emit_info(self) -> None:
        from anteroom.cli.workflow_cli import _make_progress_callback

        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            cb = _make_progress_callback()
            cb("step_emitted", "notify", {"message": "Starting deploy", "level": "info"})
        assert "Starting deploy" in output.getvalue()
        assert "cyan" in output.getvalue()

    def test_progress_callback_renders_emit_error(self) -> None:
        from anteroom.cli.workflow_cli import _make_progress_callback

        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            cb = _make_progress_callback()
            cb("step_emitted", "alert", {"message": "Something broke", "level": "error"})
        assert "Something broke" in output.getvalue()
        assert "red" in output.getvalue()

    def test_progress_callback_renders_emit_warning(self) -> None:
        from anteroom.cli.workflow_cli import _make_progress_callback

        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            cb = _make_progress_callback()
            cb("step_emitted", "warn", {"message": "Heads up", "level": "warning"})
        assert "Heads up" in output.getvalue()
        assert "yellow" in output.getvalue()

    def test_progress_callback_renders_emit_success(self) -> None:
        from anteroom.cli.workflow_cli import _make_progress_callback

        output = StringIO()
        with patch("anteroom.cli.workflow_cli.console") as mock_console:
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            cb = _make_progress_callback()
            cb("step_emitted", "done", {"message": "All good", "level": "success"})
        assert "All good" in output.getvalue()
        assert "green" in output.getvalue()

    def test_result_summary_shown_in_print_run_progress(self) -> None:
        from anteroom.cli.workflow_cli import _print_run_progress

        run = {
            "id": "run-123",
            "workflow_id": "test",
            "status": "completed",
            "result_summary": "Deployed alpha successfully",
        }
        output = StringIO()
        with (
            patch("anteroom.cli.workflow_cli.console") as mock_console,
            patch("anteroom.services.workflow_storage.list_workflow_steps", return_value=[]),
            patch("anteroom.services.workflow_storage.list_workflow_events", return_value=[]),
        ):
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_run_progress(MagicMock(), run)
        assert "Deployed alpha successfully" in output.getvalue()

    def test_describe_transcript_event_emit(self) -> None:
        from anteroom.cli.workflow_cli import _describe_transcript_event

        result = _describe_transcript_event("step_emitted", {"message": "hello", "level": "warning"})
        assert result is not None
        label, text, color = result
        assert label == "emit"
        assert text == "hello"
        assert color == "yellow"

    def test_describe_transcript_event_emit_empty(self) -> None:
        from anteroom.cli.workflow_cli import _describe_transcript_event

        result = _describe_transcript_event("step_emitted", {"message": "", "level": "info"})
        assert result is None


class TestPrintRunProgressRecoveryActions:
    """Tests for recovery actions in _print_run_progress (#1153)."""

    def test_print_run_progress_shows_recovery_actions(self) -> None:
        from anteroom.cli.workflow_cli import _print_run_progress

        run = {
            "id": "abc12345-xxxx",
            "workflow_id": "test",
            "status": "waiting_for_approval",
        }
        output = StringIO()
        with (
            patch("anteroom.cli.workflow_cli.console") as mock_console,
            patch("anteroom.services.workflow_storage.list_workflow_steps", return_value=[]),
            patch("anteroom.services.workflow_storage.list_workflow_events", return_value=[]),
        ):
            mock_console.print = lambda *a, **k: output.write(str(a[0]) + "\n")
            _print_run_progress(MagicMock(), run)
        text = output.getvalue()
        assert "Recovery options" in text
        assert "approve" in text.lower()
        assert "deny" in text.lower()
