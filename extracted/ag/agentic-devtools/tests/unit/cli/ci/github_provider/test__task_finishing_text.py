"""Tests for _task_finishing_text."""

import subprocess
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.github_provider import _task_finishing_text


def test_reads_supported_text_fields() -> None:
    """Returns the first supported finishing-text field."""
    assert _task_finishing_text({"output": "finished"}) == "finished"


def test_returns_empty_for_non_text_or_missing_values() -> None:
    """Returns an empty string when no supported field contains text."""
    assert _task_finishing_text({"result": 42}) == ""
    assert _task_finishing_text({}) == ""
    assert _task_finishing_text({"task": {"summary": 42, "output": 42}}, "task-1") == ""


def test_reads_task_level_summary_and_falls_back_to_agent_task_log() -> None:
    """Reads task-level text and uses the agent-task log when metadata has no text."""
    assert _task_finishing_text({"task": {"summary": 42, "output": "task output"}}) == "task output"
    result = MagicMock(returncode=0, stdout='{"output": "log output"}')
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result) as run_safe:
        assert _task_finishing_text({}, "task-42") == "log output"
    assert run_safe.call_args.args[0] == ["gh", "agent-task", "view", "task-42", "--log"]
    assert run_safe.call_args.kwargs["capture_output"] is True
    assert run_safe.call_args.kwargs["text"] is True
    assert run_safe.call_args.kwargs["shell"] is False
    assert run_safe.call_args.kwargs["timeout"] == 60
    assert all(
        key not in run_safe.call_args.kwargs["env"]
        for key in ("COPILOT_GITHUB_TOKEN", "SPECKIT_PR_TOKEN", "GH_TOKEN", "GITHUB_TOKEN")
    )


def test_uses_session_id_and_repository_for_agent_task_log_fallback() -> None:
    """Uses the session identifier and repository when fetching the session log."""
    result = MagicMock(returncode=0, stdout='{"output": "log output"}')
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result) as run_safe:
        assert _task_finishing_text({}, "task-42", "session-42", "owner/repo") == "log output"
    assert run_safe.call_args.args[0] == [
        "gh",
        "agent-task",
        "view",
        "session-42",
        "--log",
        "--repo",
        "owner/repo",
    ]
    assert all(
        key not in run_safe.call_args.kwargs["env"]
        for key in ("COPILOT_GITHUB_TOKEN", "SPECKIT_PR_TOKEN", "GH_TOKEN", "GITHUB_TOKEN")
    )


def test_agent_task_log_fallback_handles_failures_and_unusable_payloads() -> None:
    """Returns empty text when the agent-task log cannot provide a usable result."""
    responses = [
        OSError("gh unavailable"),
        subprocess.TimeoutExpired("gh", 60),
        MagicMock(returncode=1, stdout="error", stderr="worker End subagent: final\nusable error text"),
        MagicMock(returncode=0, stdout=""),
        MagicMock(returncode=0, stdout="plain text"),
        MagicMock(returncode=0, stdout="[]"),
        MagicMock(returncode=0, stdout='{"result": 42}'),
    ]
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=responses):
        assert _task_finishing_text({}, "task-1") == ""
        assert _task_finishing_text({}, "task-2") == ""
        assert _task_finishing_text({}, "task-3") == "usable error text"
        assert _task_finishing_text({}, "task-4") == ""
        assert _task_finishing_text({}, "task-5") == ""
        assert _task_finishing_text({}, "task-6") == ""
        assert _task_finishing_text({}, "task-7") == ""


def test_extracts_final_response_from_non_json_agent_task_log() -> None:
    """Extracts only the text after the last End subagent marker."""
    result = MagicMock(
        returncode=0,
        stdout="prior transcript\nworker End subagent: first\nfirst response\n"
        "worker End subagent: final\nfinal response\n",
    )
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        assert _task_finishing_text({}, "task-1") == "final response"


def test_returns_empty_when_non_json_log_has_no_final_response() -> None:
    """Returns empty text when the final subagent marker has no following content."""
    result = MagicMock(returncode=0, stdout="worker End subagent: final\n")
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        assert _task_finishing_text({}, "task-1") == ""
