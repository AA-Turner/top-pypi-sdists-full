"""Tests for auto_approve_waiting_runs()."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.watchdog_command import auto_approve_waiting_runs

REPO = "swai-factory/agentic-devtools"


class TestAutoApproveWaitingRuns:
    """Tests for waiting workflow approval."""

    def test_approves_valid_same_repository_runs_and_skips_invalid_entries(self, caplog, capsys) -> None:
        response = {
            "workflow_runs": [
                "not-a-run",
                {},
                {"head_repository": "not-a-repository", "id": 1},
                {"head_repository": {"full_name": "attacker/agentic-devtools"}, "id": 2},
                {"head_repository": {"full_name": REPO}, "id": True},
                {"head_repository": {"full_name": REPO}, "id": 0},
                {"head_repository": {"full_name": REPO}, "id": "3"},
                {"head_repository": {"full_name": REPO}, "id": 101},
                {"head_repository": {"full_name": REPO}, "id": 102},
            ]
        }
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._gh_api",
            side_effect=[json.dumps(response), RuntimeError("approval failed"), ""],
        ) as gh_api:
            assert auto_approve_waiting_runs(REPO, "token") == 1

        gh_api.assert_any_call(
            f"/repos/{REPO}/actions/runs/102/approve",
            method="POST",
            token="token",
        )
        assert "::notice::Approved waiting workflow run 102" in capsys.readouterr().out
        assert "invalid id" in caplog.text
        assert "Could not approve waiting workflow run 101" in caplog.text

    @pytest.mark.parametrize(
        "response",
        [
            "not-json",
            json.dumps({"workflow_runs": {}}),
        ],
    )
    def test_returns_zero_for_malformed_waiting_run_responses(self, response, caplog) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value=response):
            assert auto_approve_waiting_runs(REPO, "token") == 0
        assert "Could not list waiting workflow runs" in caplog.text

    def test_returns_zero_when_listing_waiting_runs_fails(self, caplog) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._gh_api",
            side_effect=RuntimeError("API unavailable"),
        ):
            assert auto_approve_waiting_runs(REPO, "token") == 0
        assert "Could not list waiting workflow runs" in caplog.text
