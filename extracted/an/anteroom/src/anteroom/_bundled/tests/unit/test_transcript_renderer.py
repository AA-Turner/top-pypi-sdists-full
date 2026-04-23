"""Tests for workflow transcript renderer (#1112)."""

from __future__ import annotations

import io
import re
from unittest.mock import patch

from rich.console import Console

from anteroom.cli import renderer as _renderer
from anteroom.cli.transcript_renderer import (
    TRANSCRIPT_ROLES,
    render_step_transcript,
    render_transcript_entry,
)

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _capture(func, *args, **kwargs) -> str:
    """Capture Rich console output, stripped of ANSI codes.

    The transcript renderer now routes ``transcript_assistant``,
    ``transcript_stdout`` and ``transcript_stderr`` through the shared
    ``anteroom.cli.renderer`` module (#1370). For those events the text
    lands on ``renderer.console`` / ``renderer._stdout_console`` rather
    than the console passed into ``func``. Combine both output streams
    so callers continue to see a single string.
    """
    buf = io.StringIO()
    console = Console(file=buf, width=120, force_terminal=True, color_system="truecolor")
    rbuf = io.StringIO()
    rconsole = Console(file=rbuf, width=120, force_terminal=True, color_system="truecolor")
    original_console = _renderer.console
    original_stdout_console = _renderer._stdout_console
    _renderer.console = rconsole
    _renderer._stdout_console = rconsole
    try:
        func(console, *args, **kwargs)
    finally:
        _renderer.console = original_console
        _renderer._stdout_console = original_stdout_console
    combined = buf.getvalue() + rbuf.getvalue()
    return _ANSI_RE.sub("", combined)


class TestTranscriptRoles:
    def test_all_event_types_mapped(self) -> None:
        expected = {
            "transcript_assistant",
            "transcript_tool_call",
            "transcript_tool_result",
            "transcript_stdout",
            "transcript_stderr",
            "transcript_usage",
        }
        assert set(TRANSCRIPT_ROLES.keys()) == expected


class TestRenderTranscriptEntry:
    def test_assistant_content(self) -> None:
        event = {"event_type": "transcript_assistant", "payload": {"content": "Hello world"}}
        output = _capture(render_transcript_entry, event)
        assert "Hello world" in output

    def test_tool_call(self) -> None:
        event = {
            "event_type": "transcript_tool_call",
            "payload": {"tool_name": "write_file", "arguments": '{"path": "test.py"}'},
        }
        # render_tool_call_start writes to the module-level renderer console, not the
        # test console — patch it to a no-op so the call succeeds without side effects.
        with patch("anteroom.cli.renderer.render_tool_call_start") as mock_start:
            _capture(render_transcript_entry, event)
            mock_start.assert_called_once()
            call_args = mock_start.call_args
            assert call_args[0][0] == "write_file"

    def test_tool_call_dict_arguments(self) -> None:
        event = {
            "event_type": "transcript_tool_call",
            "payload": {"tool_name": "bash", "arguments": {"command": "ls"}},
        }
        with patch("anteroom.cli.renderer.render_tool_call_start") as mock_start:
            _capture(render_transcript_entry, event)
            mock_start.assert_called_once_with("bash", {"command": "ls"})

    def test_tool_call_invalid_json_string(self) -> None:
        event = {
            "event_type": "transcript_tool_call",
            "payload": {"tool_name": "bash", "arguments": "not-valid-json"},
        }
        with patch("anteroom.cli.renderer.render_tool_call_start") as mock_start:
            _capture(render_transcript_entry, event)
            mock_start.assert_called_once_with("bash", {"_raw": "not-valid-json"})

    def test_tool_result(self) -> None:
        event = {
            "event_type": "transcript_tool_result",
            "payload": {"tool_name": "write_file", "status": "success", "output": "wrote 10 lines"},
        }
        with patch("anteroom.cli.renderer.render_tool_call_end") as mock_end:
            _capture(render_transcript_entry, event)
            mock_end.assert_called_once_with("write_file", "success", "wrote 10 lines")

    def test_stdout(self) -> None:
        event = {"event_type": "transcript_stdout", "payload": {"content": "5 passed"}}
        output = _capture(render_transcript_entry, event)
        assert "5 passed" in output

    def test_stderr(self) -> None:
        event = {"event_type": "transcript_stderr", "payload": {"content": "error: failed"}}
        output = _capture(render_transcript_entry, event)
        assert "error: failed" in output

    def test_usage(self) -> None:
        event = {"event_type": "transcript_usage", "payload": {"total_tokens": 1500, "elapsed_ms": 2300}}
        output = _capture(render_transcript_entry, event)
        assert "1,500" in output
        assert "2.3s" in output

    def test_usage_milliseconds(self) -> None:
        event = {"event_type": "transcript_usage", "payload": {"total_tokens": 0, "elapsed_ms": 800}}
        output = _capture(render_transcript_entry, event)
        assert "800ms" in output

    def test_usage_hidden_when_disabled(self) -> None:
        event = {"event_type": "transcript_usage", "payload": {"total_tokens": 1500}}
        output = _capture(render_transcript_entry, event, show_usage=False)
        assert "1,500" not in output

    def test_empty_content_no_output(self) -> None:
        event = {"event_type": "transcript_assistant", "payload": {"content": ""}}
        output = _capture(render_transcript_entry, event)
        assert output.strip() == ""

    def test_empty_stdout_no_output(self) -> None:
        event = {"event_type": "transcript_stdout", "payload": {"content": ""}}
        output = _capture(render_transcript_entry, event)
        assert output.strip() == ""

    def test_empty_stderr_no_output(self) -> None:
        event = {"event_type": "transcript_stderr", "payload": {"content": ""}}
        output = _capture(render_transcript_entry, event)
        assert output.strip() == ""

    def test_unknown_event_type_no_crash(self) -> None:
        event = {"event_type": "transcript_unknown", "payload": {}}
        output = _capture(render_transcript_entry, event)
        assert isinstance(output, str)

    def test_missing_payload_no_crash(self) -> None:
        event = {"event_type": "transcript_assistant"}
        output = _capture(render_transcript_entry, event)
        assert isinstance(output, str)

    def test_none_payload_no_crash(self) -> None:
        event = {"event_type": "transcript_assistant", "payload": None}
        output = _capture(render_transcript_entry, event)
        assert isinstance(output, str)

    def test_rich_markup_in_content_escaped(self) -> None:
        event = {"event_type": "transcript_assistant", "payload": {"content": "[bold]not markup[/bold]"}}
        output = _capture(render_transcript_entry, event)
        assert "not markup" in output


class TestRenderStepTranscript:
    def test_with_step_header(self) -> None:
        events = [{"event_type": "transcript_assistant", "payload": {"content": "Hi"}}]
        output = _capture(render_step_transcript, events, step_header="generate_code (cli_claude)")
        assert "generate_code" in output
        assert "Hi" in output

    def test_without_step_header(self) -> None:
        events = [{"event_type": "transcript_assistant", "payload": {"content": "Hi"}}]
        output = _capture(render_step_transcript, events)
        assert "Hi" in output
        assert "──" not in output

    def test_empty_events(self) -> None:
        output = _capture(render_step_transcript, [])
        assert output.strip() == ""

    def test_empty_events_with_header(self) -> None:
        output = _capture(render_step_transcript, [], step_header="step_name")
        assert "step_name" in output

    def test_multiple_events(self) -> None:
        events = [
            {"event_type": "transcript_assistant", "payload": {"content": "Planning..."}},
            {"event_type": "transcript_tool_call", "payload": {"tool_name": "bash", "arguments": "ls"}},
            {
                "event_type": "transcript_tool_result",
                "payload": {"tool_name": "bash", "status": "success", "output": "file.py"},
            },
            {"event_type": "transcript_usage", "payload": {"total_tokens": 500, "elapsed_ms": 800}},
        ]
        with (
            patch("anteroom.cli.renderer.render_tool_call_start"),
            patch("anteroom.cli.renderer.render_tool_call_end"),
        ):
            output = _capture(render_step_transcript, events)
        assert "Planning" in output
        assert "500" in output

    def test_show_usage_false_propagates(self) -> None:
        events = [
            {"event_type": "transcript_usage", "payload": {"total_tokens": 9999, "elapsed_ms": 100}},
        ]
        output = _capture(render_step_transcript, events, show_usage=False)
        assert "9,999" not in output
