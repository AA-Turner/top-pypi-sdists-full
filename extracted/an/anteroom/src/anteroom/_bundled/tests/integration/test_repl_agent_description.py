"""Integration tests for run_agent description field in the REPL (#1461).

Tests that:
(a) a run_agent completion with description= shows the description label in
    REPL notifications, not a generic prompt snippet or run-id alone.
(b) a run_agent completion without description= falls back to the title/prompt.

These tests drive the real ``poll_detached_agents`` rendering path via a
subprocess (same pattern as test_repl_subagent_live.py).
"""

from __future__ import annotations

import io
import sys
import textwrap

import pytest

pexpect = pytest.importorskip("pexpect", reason="pexpect required for PTY tests")

_PYTHON = sys.executable


def _script_with_description() -> str:
    """Render one completed run that has an explicit description in metadata."""
    return textwrap.dedent("""\
        from pathlib import Path
        import sys
        import types
        from rich.console import Console

        sys.path.insert(0, str((Path.cwd() / "src").resolve()))
        sys.modules.setdefault("filetype", types.SimpleNamespace(guess=lambda *_a, **_k: None))
        from anteroom.cli import renderer
        from anteroom.cli.repl import poll_detached_agents

        class FakeDetachManager:
            def poll_completed(self):
                return [
                    {
                        "id": "aabbccdd11223344",
                        "status": "completed",
                        "title": "Prompt snippet that should NOT appear",
                        "metadata": {
                            "description": "Deploy health check",
                            "task_result": {
                                "summary": "All services are healthy.",
                                "tool_calls": ["bash", "read_file"],
                                "duration_seconds": 3.7,
                            },
                        },
                    },
                ]

        plain = Console(file=sys.stdout, force_terminal=False, color_system=None, width=140)
        renderer.console = plain
        renderer._stdout_console = plain
        poll_detached_agents(FakeDetachManager(), plain)
        print("PTY_DONE")
    """)


def _script_without_description() -> str:
    """Render one completed run that has no description — falls back to title."""
    return textwrap.dedent("""\
        from pathlib import Path
        import sys
        import types
        from rich.console import Console

        sys.path.insert(0, str((Path.cwd() / "src").resolve()))
        sys.modules.setdefault("filetype", types.SimpleNamespace(guess=lambda *_a, **_k: None))
        from anteroom.cli import renderer
        from anteroom.cli.repl import poll_detached_agents

        class FakeDetachManager:
            def poll_completed(self):
                return [
                    {
                        "id": "ffeeddcc99887766",
                        "status": "completed",
                        "title": "Summarise the quarterly report",
                        "metadata": {
                            "task_result": {
                                "summary": "Summary done.",
                                "tool_calls": ["read_file"],
                                "duration_seconds": 1.2,
                            },
                        },
                    },
                ]

        plain = Console(file=sys.stdout, force_terminal=False, color_system=None, width=140)
        renderer.console = plain
        renderer._stdout_console = plain
        poll_detached_agents(FakeDetachManager(), plain)
        print("PTY_DONE")
    """)


def _script_failed_with_description() -> str:
    """Render a failed run that has an explicit description."""
    return textwrap.dedent("""\
        from pathlib import Path
        import sys
        import types
        from rich.console import Console

        sys.path.insert(0, str((Path.cwd() / "src").resolve()))
        sys.modules.setdefault("filetype", types.SimpleNamespace(guess=lambda *_a, **_k: None))
        from anteroom.cli import renderer
        from anteroom.cli.repl import poll_detached_agents

        class FakeDetachManager:
            def poll_completed(self):
                return [
                    {
                        "id": "deadbeef12345678",
                        "status": "failed",
                        "title": "Generic title fallback",
                        "metadata": {
                            "description": "Nightly lint sweep",
                            "task_result": {
                                "error": "ruff: command not found",
                                "tool_calls": [],
                                "duration_seconds": 0.3,
                            },
                        },
                    },
                ]

        plain = Console(file=sys.stdout, force_terminal=False, color_system=None, width=140)
        renderer.console = plain
        renderer._stdout_console = plain
        poll_detached_agents(FakeDetachManager(), plain)
        print("PTY_DONE")
    """)


@pytest.mark.integration
class TestReplAgentDescriptionLabel:
    def test_completion_notification_shows_description_not_title(self) -> None:
        """When description is in metadata, the notification uses it as the label."""
        buf = io.StringIO()
        child = pexpect.spawn(_PYTHON, ["-c", _script_with_description()], timeout=15, encoding="utf-8")
        child.logfile_read = buf

        child.expect("PTY_DONE", timeout=10)
        child.expect(pexpect.EOF, timeout=5)
        output = buf.getvalue()

        assert "Deploy health check" in output, f"Expected label in output:\n{output}"
        assert "Prompt snippet that should NOT appear" not in output, (
            f"Title should NOT appear when description is set:\n{output}"
        )
        assert "[agent aabbccdd]" in output, f"Expected run-id prefix in output:\n{output}"

    def test_completion_notification_falls_back_to_title_when_no_description(self) -> None:
        """When no description is present, the notification falls back to the run title."""
        buf = io.StringIO()
        child = pexpect.spawn(_PYTHON, ["-c", _script_without_description()], timeout=15, encoding="utf-8")
        child.logfile_read = buf

        child.expect("PTY_DONE", timeout=10)
        child.expect(pexpect.EOF, timeout=5)
        output = buf.getvalue()

        assert "Summarise the quarterly report" in output, f"Expected title as fallback label:\n{output}"
        assert "[agent ffeeddcc]" in output, f"Expected run-id prefix in output:\n{output}"

    def test_failed_run_with_description_shows_description_label(self) -> None:
        """A failed run with description shows the description label, not the generic title."""
        buf = io.StringIO()
        child = pexpect.spawn(_PYTHON, ["-c", _script_failed_with_description()], timeout=15, encoding="utf-8")
        child.logfile_read = buf

        child.expect("PTY_DONE", timeout=10)
        child.expect(pexpect.EOF, timeout=5)
        output = buf.getvalue()

        assert "Nightly lint sweep" in output, f"Expected description label in failed run output:\n{output}"
        assert "Generic title fallback" not in output, f"Title should NOT appear when description is set:\n{output}"
        assert "[agent deadbeef]" in output, f"Expected run-id prefix in output:\n{output}"
        assert "ruff: command not found" in output, f"Expected error preview in output:\n{output}"
