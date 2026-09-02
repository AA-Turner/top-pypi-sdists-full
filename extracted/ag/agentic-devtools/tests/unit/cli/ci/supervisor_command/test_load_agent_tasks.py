"""Tests for loading agent-task data."""

from unittest.mock import patch


def test_load_agent_tasks_returns_parsed_tasks() -> None:
    from agentic_devtools.cli.ci.supervisor_command import load_agent_tasks

    completed = type("Completed", (), {"returncode": 0, "stdout": '[{"id": "one"}]', "stderr": ""})()
    with patch("agentic_devtools.cli.ci.supervisor_command.run_safe", return_value=completed):
        tasks, error = load_agent_tasks("o/r")

    assert tasks == [{"id": "one"}]
    assert error == ""


def test_load_agent_tasks_returns_error_without_raising() -> None:
    from agentic_devtools.cli.ci.supervisor_command import load_agent_tasks

    completed = type("Completed", (), {"returncode": 1, "stdout": "", "stderr": "permission denied"})()
    with patch("agentic_devtools.cli.ci.supervisor_command.run_safe", return_value=completed):
        tasks, error = load_agent_tasks("o/r")

    assert tasks == []
    assert error == "agent_tasks: permission denied"


def test_load_agent_tasks_handles_empty_error_and_os_error() -> None:
    from agentic_devtools.cli.ci.supervisor_command import load_agent_tasks

    completed = type("Completed", (), {"returncode": 1, "stdout": "", "stderr": ""})()
    with patch("agentic_devtools.cli.ci.supervisor_command.run_safe", return_value=completed):
        tasks, error = load_agent_tasks("o/r")
    assert tasks == []
    assert error == "agent_tasks: command failed"

    with patch(
        "agentic_devtools.cli.ci.supervisor_command.run_safe",
        side_effect=OSError("gh unavailable"),
    ):
        tasks, error = load_agent_tasks("o/r")
    assert tasks == []
    assert error == "agent_tasks: gh unavailable"


def test_load_agent_tasks_handles_timeout() -> None:
    import subprocess

    from agentic_devtools.cli.ci.supervisor_command import load_agent_tasks

    with patch(
        "agentic_devtools.cli.ci.supervisor_command.run_safe",
        side_effect=subprocess.TimeoutExpired(cmd="gh", timeout=60),
    ):
        tasks, error = load_agent_tasks("o/r")

    assert tasks == []
    assert "timed out" in error
