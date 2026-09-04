"""Tests for the Cloud Agent guard CLI entry point."""

from __future__ import annotations

import json
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.cloud_agent_guard import (
    CloudAgentGuardResult,
    cloud_agent_guard_command,
)


def test_outputs_secret_free_result(capsys: pytest.CaptureFixture[str]) -> None:
    with (
        patch.object(sys, "argv", ["agdt-speckit-cloud-agent-guard", "--issue-number", "7", "--repo", "owner/repo"]),
        patch(
            "agentic_devtools.cli.speckit.cloud_agent_guard.check_cloud_agent_in_flight",
            return_value=CloudAgentGuardResult(False, "none", 7),
        ),
    ):
        with pytest.raises(SystemExit) as exc_info:
            cloud_agent_guard_command()

    assert exc_info.value.code == 0
    output = json.loads(capsys.readouterr().out)
    assert output == {
        "in_flight": False,
        "reason": "none",
        "issue_number": 7,
        "phase": None,
        "matched_pr_number": None,
        "matched_label": None,
    }


@pytest.mark.parametrize(
    "argv",
    [
        ["--issue-number", "0", "--repo", "owner/repo"],
        ["--issue-number", "7", "--phase", "4", "--repo", "owner/repo"],
        ["--issue-number", "7", "--repo", "invalid"],
        ["--repo", "owner/repo"],
        ["--issue-number", "7", "--unknown", "value"],
    ],
)
def test_invalid_arguments_exit_one(argv: list[str], capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(sys, "argv", ["agdt-speckit-cloud-agent-guard", *argv]):
        with pytest.raises(SystemExit) as exc_info:
            cloud_agent_guard_command()

    assert exc_info.value.code == 1
    assert json.loads(capsys.readouterr().out)["reason"] == "invalid-arguments"


@pytest.mark.parametrize(
    "error",
    [
        RuntimeError("token-secret"),
        json.JSONDecodeError("token-secret", "payload", 0),
    ],
)
def test_api_error_is_secret_free(capsys: pytest.CaptureFixture[str], error: Exception) -> None:
    with (
        patch.object(sys, "argv", ["agdt-speckit-cloud-agent-guard", "--issue-number", "7", "--repo", "owner/repo"]),
        patch(
            "agentic_devtools.cli.speckit.cloud_agent_guard.check_cloud_agent_in_flight",
            side_effect=error,
        ),
    ):
        with pytest.raises(SystemExit) as exc_info:
            cloud_agent_guard_command()

    assert exc_info.value.code == 1
    output = capsys.readouterr().out
    assert "token-secret" not in output
    assert json.loads(output)["reason"] == "error"
