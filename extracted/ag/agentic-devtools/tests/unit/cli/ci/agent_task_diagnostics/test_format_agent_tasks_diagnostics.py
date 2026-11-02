"""Tests for Agent Tasks diagnostics."""

import re
import subprocess
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import agent_task_diagnostics
from agentic_devtools.cli.ci.agent_task_diagnostics import AgentTaskDiagnostics
from agentic_devtools.cli.ci.retry import RetryableError


def test_formats_agent_task_transport_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(agent_task_diagnostics.importlib.metadata, "version", Mock(return_value="1.2.3"))
    which = Mock(return_value="C:\\tools\\gh.exe")
    monkeypatch.setattr(agent_task_diagnostics.shutil, "which", which)
    diagnostics = AgentTaskDiagnostics(
        "/agents/repos/owner/repo/tasks?per_page=10",
        {"PATH": "C:\\tools", "GH_HOST": "github.example.com"},
        lambda value: value,
        is_agent_tasks=True,
    )
    diagnostics.status = 404
    diagnostics.status_source = "response_headers"
    diagnostics.returncode = 1

    message = diagnostics.format_error("Not Found")

    assert "agentic_devtools_version=1.2.3; gh_executable=C:\\tools\\gh.exe" in message
    assert "endpoint=/agents/repos/owner/repo/tasks; host=github.example.com; query=per_page=10" in message
    assert "http_status=404; http_status_source=response_headers; returncode=1" in message
    assert "url=not captured" in message and "response_body=not captured" in message
    which.assert_called_once_with("gh", path="C:\\tools")


@pytest.mark.parametrize("env", [{}, {"PATH": ""}])
def test_does_not_search_when_subprocess_path_is_missing_or_empty(
    monkeypatch: pytest.MonkeyPatch, env: dict[str, str]
) -> None:
    monkeypatch.setattr(agent_task_diagnostics.importlib.metadata, "version", Mock(side_effect=RuntimeError))
    which = Mock(return_value="C:\\current\\gh.exe")
    monkeypatch.setattr(agent_task_diagnostics.shutil, "which", which)
    diagnostics = AgentTaskDiagnostics("/agents/repos/owner/repo/tasks", env, lambda value: value, is_agent_tasks=True)

    message = diagnostics.format_error("Not Found")

    assert "agentic_devtools_version=not captured" in message
    assert "gh_executable=not captured" in message
    assert "query=not captured; url=not captured" in message
    assert "http_status=not captured; http_status_source=not captured; returncode=not captured" in message
    which.assert_not_called()


def test_preserves_non_agent_prefix_and_truncation_order() -> None:
    diagnostics = AgentTaskDiagnostics("/repos/owner/repo", None, lambda value: value[:512])
    text = "x" * 600

    assert diagnostics.format_error(text, prefix="GitHub API error: ") == f"GitHub API error: {text[:512]}"
    assert diagnostics.format_error(text) == text
    agent_diagnostics = AgentTaskDiagnostics(
        "/agents/repos/owner/repo/tasks", {}, lambda value: value, is_agent_tasks=True
    )
    assert agent_diagnostics.format_error(text).startswith(f"{text[:512]}; Agent Tasks failure diagnostics:")


def test_uses_provider_supplied_agent_tasks_classification() -> None:
    endpoint = "/agents/repos/owner/repo/tasks"
    unclassified = AgentTaskDiagnostics(endpoint, {}, str)
    classified = AgentTaskDiagnostics(endpoint, {}, str, is_agent_tasks=True)

    assert unclassified.is_agent_tasks is False
    assert "Agent Tasks failure diagnostics" not in unclassified.format_error("Not Found")
    assert classified.is_agent_tasks is True
    assert "Agent Tasks failure diagnostics" in classified.format_error("Not Found")


def test_adds_launch_failure_note_only_for_agent_tasks() -> None:
    launch_error = FileNotFoundError("gh is missing")
    diagnostics = AgentTaskDiagnostics("/agents/repos/owner/repo/tasks", {}, lambda value: value, is_agent_tasks=True)

    diagnostics.add_launch_failure_note(launch_error)

    assert "http_status=not captured" in launch_error.__notes__[0]
    assert "returncode=not captured; response_body=not captured" in launch_error.__notes__[0]
    ordinary_error = FileNotFoundError("gh is missing")
    AgentTaskDiagnostics("/repos/owner/repo", {}, lambda value: value).add_launch_failure_note(ordinary_error)
    assert not hasattr(ordinary_error, "__notes__")


def test_marks_executable_uncaptured_when_lookup_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(agent_task_diagnostics.shutil, "which", Mock(side_effect=OSError("lookup failed")))
    diagnostics = AgentTaskDiagnostics(
        "/agents/repos/owner/repo/tasks", {"PATH": "C:\\tools"}, lambda value: value, is_agent_tasks=True
    )

    assert "gh_executable=not captured" in diagnostics.format_error("Not Found")


def test_runs_command_and_preserves_retryable_or_launch_failures() -> None:
    diagnostics = AgentTaskDiagnostics("/agents/repos/owner/repo/tasks", {}, lambda value: value, is_agent_tasks=True)
    result = subprocess.CompletedProcess(["gh"], 0, "", "")
    runner = Mock(return_value=result)

    assert diagnostics.run(runner, ["gh"], "timeout", text=True) is result
    runner.assert_called_once_with(["gh"], text=True)

    timeout = subprocess.TimeoutExpired(["gh"], 1)
    with pytest.raises(RetryableError, match="timeout") as timeout_error:
        diagnostics.run(Mock(side_effect=timeout), ["gh"], "timeout")
    assert timeout_error.value.__cause__ is timeout

    launch_error = FileNotFoundError("gh missing")
    with pytest.raises(FileNotFoundError) as launch:
        diagnostics.run(Mock(side_effect=launch_error), ["gh"], "timeout")
    assert launch.value is launch_error
    assert "http_status=not captured" in launch.value.__notes__[0]


@pytest.mark.parametrize(
    ("status", "stderr", "expected_status", "expected_source"),
    [(None, "HTTP 404: missing", 404, "stderr"), (403, "HTTP 404: missing", 403, None), (None, "other", None, None)],
)
def test_records_response_status_provenance(
    status: int | None, stderr: str, expected_status: int | None, expected_source: str | None
) -> None:
    diagnostics = AgentTaskDiagnostics("/agents/repos/owner/repo/tasks", {}, lambda value: value, is_agent_tasks=True)

    result_status = diagnostics.record_result(
        subprocess.CompletedProcess(["gh"], 1, "", stderr),
        status,
        stderr,
        re.compile(r"HTTP\s+(\d{3})"),
    )

    assert result_status == expected_status
    assert diagnostics.status_source == expected_source
    assert diagnostics.returncode == 1
