"""Tests for safe permanent GitHub API errors."""

import re
import subprocess

import pytest

from agentic_devtools.cli.ci.agent_task_diagnostics import AgentTaskDiagnostics
from agentic_devtools.cli.ci.github_api_error import GitHubApiError, raise_github_api_error


@pytest.mark.parametrize("status", [401, 403, 404, 422, None])
def test_permanent_api_failure_retains_only_safe_parsed_status(status: int | None) -> None:
    diagnostics = AgentTaskDiagnostics("/repos/o/r", None, str)

    with pytest.raises(GitHubApiError) as caught:
        raise_github_api_error(
            diagnostics,
            status,
            "private raw response with offline-credential",
            1,
        )

    assert caught.value.http_status == status
    assert "private raw response" not in str(caught.value)
    assert "offline-credential" not in str(caught.value)


def test_agent_tasks_error_keeps_sanitized_diagnostics_and_exit_fallback() -> None:
    diagnostics = AgentTaskDiagnostics(
        "/agents/repos/o/r/tasks",
        None,
        lambda text: text.replace("offline-credential", "[REDACTED]"),
        is_agent_tasks=True,
    )
    diagnostics.record_result(
        subprocess.CompletedProcess(["gh"], 1, stdout="", stderr=""),
        404,
        "",
        re.compile(r"([45]\d{2})\b"),
    )

    with pytest.raises(GitHubApiError) as caught:
        raise_github_api_error(diagnostics, 404, "", 1)

    assert caught.value.http_status == 404
    assert "GitHub API error: exit code 1" in str(caught.value)
    assert "http_status=404" in str(caught.value)
    assert "offline-credential" not in str(caught.value)
