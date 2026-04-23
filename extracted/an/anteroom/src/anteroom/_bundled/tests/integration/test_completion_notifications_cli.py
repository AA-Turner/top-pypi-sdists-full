"""Integration tests for CLI completion notification poller (#1315).

Tests the real ``poll_bg_tasks`` and ``poll_detached_agents`` functions
extracted from ``repl.py``, exercising the actual rendering path instead
of reimplementing the loop body.
"""

from __future__ import annotations

from io import StringIO
from unittest.mock import MagicMock

import pytest
from rich.console import Console

from anteroom.cli.repl import poll_bg_tasks, poll_detached_agents


class TestPollBgTasks:
    """Verify poll_bg_tasks() renders [bg] notifications for completed tasks."""

    def test_completed_task_renders_notification(self) -> None:
        buf = StringIO()
        console = Console(file=buf, force_terminal=False, width=120)

        mgr = MagicMock()
        mgr.poll_completed.return_value = [
            {
                "id": "aaaa1111-2222-3333-4444-555566667777",
                "status": "completed",
                "exit_code": 0,
                "duration_seconds": 2.5,
            }
        ]
        mgr.count_running.return_value = 0

        poll_bg_tasks(mgr, console)

        output = buf.getvalue()
        assert "[bg]" in output
        assert "aaaa1111" in output
        assert "completed" in output
        assert "exit 0" in output
        assert "2.5s" in output

    def test_failed_task_shows_nonzero_exit_code(self) -> None:
        buf = StringIO()
        console = Console(file=buf, force_terminal=False, width=120)

        mgr = MagicMock()
        mgr.poll_completed.return_value = [
            {
                "id": "bbbb2222-3333-4444-5555-666677778888",
                "status": "failed",
                "exit_code": 1,
                "duration_seconds": 0.3,
            }
        ]
        mgr.count_running.return_value = 0

        poll_bg_tasks(mgr, console)

        output = buf.getvalue()
        assert "[bg]" in output
        assert "failed" in output
        assert "exit 1" in output

    def test_no_tasks_no_output(self) -> None:
        buf = StringIO()
        console = Console(file=buf, force_terminal=False, width=120)

        mgr = MagicMock()
        mgr.poll_completed.return_value = []
        mgr.count_running.return_value = 0

        poll_bg_tasks(mgr, console)

        output = buf.getvalue()
        assert "[bg]" not in output

    def test_multiple_tasks_all_render(self) -> None:
        buf = StringIO()
        console = Console(file=buf, force_terminal=False, width=120)

        mgr = MagicMock()
        mgr.poll_completed.return_value = [
            {"id": "task-aaa-1", "status": "completed", "exit_code": 0, "duration_seconds": 1.0},
            {"id": "task-bbb-2", "status": "failed", "exit_code": 2, "duration_seconds": 3.0},
        ]
        mgr.count_running.return_value = 0

        poll_bg_tasks(mgr, console)

        output = buf.getvalue()
        assert "task-aaa" in output
        assert "task-bbb" in output

    def test_updates_bg_task_count(self) -> None:
        buf = StringIO()
        console = Console(file=buf, force_terminal=False, width=120)

        mgr = MagicMock()
        mgr.poll_completed.return_value = []
        mgr.count_running.return_value = 3

        poll_bg_tasks(mgr, console)

        mgr.count_running.assert_called_once()


class TestPollDetachedAgents:
    """Verify poll_detached_agents() renders [agent] notifications."""

    def test_completed_agent_renders_notification(self) -> None:
        buf = StringIO()
        console = Console(file=buf, force_terminal=False, width=120)

        mgr = MagicMock()
        mgr.poll_completed.return_value = [
            {
                "id": "cccc3333-4444-5555-6666-777788889999",
                "status": "completed",
                "metadata": {
                    "task_result": {
                        "tool_calls": ["bash", "read_file"],
                        "duration_seconds": 5.2,
                    }
                },
            }
        ]

        poll_detached_agents(mgr, console)

        output = buf.getvalue()
        assert "[agent cccc3333]" in output
        assert "cccc3333" in output
        assert "done" in output
        assert "2 tools" in output
        assert "5.2s" in output

    def test_null_metadata_renders_safely(self) -> None:
        buf = StringIO()
        console = Console(file=buf, force_terminal=False, width=120)

        mgr = MagicMock()
        mgr.poll_completed.return_value = [
            {
                "id": "dddd4444-5555-6666-7777-888899990000",
                "status": "failed",
                "metadata": None,
            }
        ]

        poll_detached_agents(mgr, console)

        output = buf.getvalue()
        assert "[agent dddd4444]" in output
        assert "dddd4444" in output
        assert "failed" in output
        assert "unknown error" in output

    def test_no_completions_no_output(self) -> None:
        buf = StringIO()
        console = Console(file=buf, force_terminal=False, width=120)

        mgr = MagicMock()
        mgr.poll_completed.return_value = []

        poll_detached_agents(mgr, console)

        output = buf.getvalue()
        assert "[agent]" not in output


class TestPollerExceptionPropagation:
    """Verify that exceptions from the real functions propagate (the poller catches them)."""

    def test_bg_poll_exception_propagates(self) -> None:
        """poll_bg_tasks raises when poll_completed() raises — the poller's try/except handles it."""
        mgr = MagicMock()
        mgr.poll_completed.side_effect = RuntimeError("DB locked")

        buf = StringIO()
        console = Console(file=buf, force_terminal=False, width=120)

        with pytest.raises(RuntimeError, match="DB locked"):
            poll_bg_tasks(mgr, console)

    def test_detach_poll_exception_propagates(self) -> None:
        """poll_detached_agents raises when poll_completed() raises."""
        mgr = MagicMock()
        mgr.poll_completed.side_effect = ConnectionError("Socket error")

        buf = StringIO()
        console = Console(file=buf, force_terminal=False, width=120)

        with pytest.raises(ConnectionError, match="Socket error"):
            poll_detached_agents(mgr, console)
