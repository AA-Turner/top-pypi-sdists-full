"""Tests for workflow replay (#1113)."""

from __future__ import annotations

import io
import re
from typing import Any
from unittest.mock import MagicMock, patch

from rich.console import Console

from anteroom.cli import renderer as _renderer
from anteroom.cli.transcript_renderer import render_run_replay

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _capture(func: Any, *args: Any, **kwargs: Any) -> str:
    """Capture Rich console output, stripped of ANSI codes.

    ``transcript_renderer`` now routes ``transcript_assistant``,
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


class TestRenderRunReplay:
    def test_empty_events(self) -> None:
        output = _capture(render_run_replay, [])
        assert "No replay data" in output

    def test_step_boundary_header(self) -> None:
        events = [
            {"event_type": "step_started", "step_id": "validate", "payload": {"step_type": "runner"}},
            {"event_type": "transcript_assistant", "step_id": "validate", "payload": {"content": "Running validation"}},
        ]
        output = _capture(render_run_replay, events)
        assert "validate" in output
        assert "Running validation" in output

    def test_step_finished_success(self) -> None:
        events = [
            {"event_type": "step_started", "step_id": "build", "payload": {}},
            {
                "event_type": "step_finished",
                "step_id": "build",
                "payload": {"result_status": "success", "duration_ms": 1500},
            },
        ]
        output = _capture(render_run_replay, events)
        assert "success" in output
        assert "1.5s" in output

    def test_step_finished_short_duration(self) -> None:
        events = [
            {"event_type": "step_started", "step_id": "quick", "payload": {}},
            {
                "event_type": "step_finished",
                "step_id": "quick",
                "payload": {"result_status": "success", "duration_ms": 200},
            },
        ]
        output = _capture(render_run_replay, events)
        assert "200ms" in output

    def test_step_failed(self) -> None:
        events = [
            {"event_type": "step_started", "step_id": "test", "payload": {}},
            {"event_type": "step_failed", "step_id": "test", "payload": {"error": "assertion failed"}},
        ]
        output = _capture(render_run_replay, events)
        assert "failed" in output
        assert "assertion failed" in output

    def test_multi_step_replay(self) -> None:
        events = [
            {"event_type": "step_started", "step_id": "step1", "payload": {}},
            {"event_type": "transcript_assistant", "step_id": "step1", "payload": {"content": "First step"}},
            {
                "event_type": "step_finished",
                "step_id": "step1",
                "payload": {"result_status": "success", "duration_ms": 500},
            },
            {"event_type": "step_started", "step_id": "step2", "payload": {}},
            {"event_type": "transcript_stdout", "step_id": "step2", "payload": {"content": "5 passed"}},
            {
                "event_type": "step_finished",
                "step_id": "step2",
                "payload": {"result_status": "success", "duration_ms": 800},
            },
        ]
        output = _capture(render_run_replay, events)
        assert "step1" in output
        assert "step2" in output
        assert "First step" in output
        assert "5 passed" in output

    def test_replay_summary_footer(self) -> None:
        events = [
            {"event_type": "step_started", "step_id": "s1", "payload": {}},
            {"event_type": "transcript_usage", "step_id": "s1", "payload": {"total_tokens": 1000}},
            {
                "event_type": "step_finished",
                "step_id": "s1",
                "payload": {"result_status": "success", "duration_ms": 100},
            },
        ]
        output = _capture(render_run_replay, events)
        assert "1,000" in output
        assert "Replay complete" in output

    def test_step_info_from_steps_list(self) -> None:
        events = [
            {"event_type": "step_started", "step_id": "gen", "payload": {}},
            {"event_type": "transcript_assistant", "step_id": "gen", "payload": {"content": "hi"}},
        ]
        steps = [{"step_id": "gen", "step_type": "runner", "runner_type": "cli_claude"}]
        output = _capture(render_run_replay, events, steps=steps)
        assert "runner" in output
        assert "cli_claude" in output

    def test_step_info_without_runner(self) -> None:
        events = [
            {"event_type": "step_started", "step_id": "check", "payload": {}},
            {"event_type": "transcript_assistant", "step_id": "check", "payload": {"content": "ok"}},
        ]
        steps = [{"step_id": "check", "step_type": "gate", "runner_type": ""}]
        output = _capture(render_run_replay, events, steps=steps)
        assert "gate" in output

    def test_step_finished_blocked(self) -> None:
        events = [
            {"event_type": "step_started", "step_id": "gate1", "payload": {}},
            {
                "event_type": "step_finished",
                "step_id": "gate1",
                "payload": {"result_status": "blocked", "duration_ms": 50},
            },
        ]
        output = _capture(render_run_replay, events)
        assert "blocked" in output

    def test_multiple_token_usage_accumulated(self) -> None:
        events = [
            {"event_type": "step_started", "step_id": "s1", "payload": {}},
            {"event_type": "transcript_usage", "step_id": "s1", "payload": {"total_tokens": 500}},
            {
                "event_type": "step_finished",
                "step_id": "s1",
                "payload": {"result_status": "success", "duration_ms": 100},
            },
            {"event_type": "step_started", "step_id": "s2", "payload": {}},
            {"event_type": "transcript_usage", "step_id": "s2", "payload": {"total_tokens": 700}},
            {
                "event_type": "step_finished",
                "step_id": "s2",
                "payload": {"result_status": "success", "duration_ms": 100},
            },
        ]
        output = _capture(render_run_replay, events)
        assert "1,200" in output
        assert "2 steps" in output


class TestGetRunReplayEvents:
    def test_returns_merged_events(self) -> None:
        db = MagicMock()
        db.execute_fetchall.return_value = [
            {
                "id": 1,
                "run_id": "r1",
                "step_id": "s1",
                "event_type": "step_started",
                "payload_json": '{"step_type": "runner"}',
                "created_at": "2025-01-01T00:00:00",
            },
            {
                "id": 2,
                "run_id": "r1",
                "step_id": "s1",
                "event_type": "transcript_assistant",
                "payload_json": '{"content": "hello"}',
                "created_at": "2025-01-01T00:00:01",
            },
            {
                "id": 3,
                "run_id": "r1",
                "step_id": "s1",
                "event_type": "step_finished",
                "payload_json": '{"result_status": "success", "duration_ms": 100}',
                "created_at": "2025-01-01T00:00:02",
            },
        ]

        from anteroom.services.workflow_storage import get_run_replay_events

        events = get_run_replay_events(db, "r1")
        assert len(events) == 3
        assert events[0]["event_type"] == "step_started"
        assert events[1]["event_type"] == "transcript_assistant"
        assert events[1]["payload"]["content"] == "hello"
        assert events[2]["event_type"] == "step_finished"

    def test_empty_run(self) -> None:
        db = MagicMock()
        db.execute_fetchall.return_value = []

        from anteroom.services.workflow_storage import get_run_replay_events

        events = get_run_replay_events(db, "nonexistent")
        assert events == []

    def test_null_payload(self) -> None:
        db = MagicMock()
        db.execute_fetchall.return_value = [
            {
                "id": 1,
                "run_id": "r1",
                "step_id": "s1",
                "event_type": "step_started",
                "payload_json": None,
                "created_at": "2025-01-01T00:00:00",
            },
        ]

        from anteroom.services.workflow_storage import get_run_replay_events

        events = get_run_replay_events(db, "r1")
        assert len(events) == 1
        assert events[0]["payload"] is None


class TestHandleReplay:
    def test_missing_run_id(self) -> None:
        from anteroom.cli.workflow_cli import _handle_replay

        args = MagicMock()
        args.run_id = None
        mock_console = MagicMock()
        mock_db = MagicMock()

        with patch("anteroom.cli.workflow_cli.console", mock_console):
            _handle_replay(mock_db, args)

        mock_console.print.assert_called_once()
        assert "Usage" in mock_console.print.call_args[0][0]

    def test_run_not_found(self) -> None:
        from anteroom.cli.workflow_cli import _handle_replay

        args = MagicMock()
        args.run_id = "bad-id"
        mock_console = MagicMock()
        mock_db = MagicMock()

        with (
            patch("anteroom.cli.workflow_cli.console", mock_console),
            patch(
                "anteroom.services.workflow_storage.resolve_workflow_run_id",
                side_effect=ValueError("Run not found: bad-id"),
            ),
        ):
            _handle_replay(mock_db, args)

        assert "not found" in mock_console.print.call_args[0][0].lower()

    def test_delegates_to_render(self) -> None:
        from anteroom.cli.workflow_cli import _handle_replay

        args = MagicMock()
        args.run_id = "run-123"
        mock_console = MagicMock()
        mock_db = MagicMock()

        fake_run = {"id": "run-123", "status": "completed"}
        fake_events: list[dict[str, Any]] = []
        fake_steps: list[dict[str, Any]] = []

        with (
            patch("anteroom.cli.workflow_cli.console", mock_console),
            patch("anteroom.services.workflow_storage.resolve_workflow_run_id", return_value="run-123"),
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=fake_run),
            patch("anteroom.services.workflow_storage.get_run_replay_events", return_value=fake_events) as mock_events,
            patch("anteroom.services.workflow_storage.list_workflow_steps", return_value=fake_steps),
            patch("anteroom.cli.transcript_renderer.render_run_replay") as mock_render,
        ):
            _handle_replay(mock_db, args)
            mock_events.assert_called_once_with(mock_db, "run-123")
            mock_render.assert_called_once_with(mock_console, fake_events, steps=fake_steps)
