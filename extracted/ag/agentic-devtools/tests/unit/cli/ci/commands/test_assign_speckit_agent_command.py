"""Tests for the cloud-agent SpecKit dispatch command."""

from __future__ import annotations

import json
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.agent_assignment import AgentAssignmentResult
from agentic_devtools.cli.ci.commands import (
    assign_speckit_agent_command,
)
from agentic_devtools.cli.ci.retry import RetryableError


def _invoke(argv: list[str], capsys: pytest.CaptureFixture[str]) -> tuple[dict, int]:
    with (
        patch.object(sys, "argv", ["agdt-assign-speckit-agent", *argv]),
        pytest.raises(SystemExit) as exc_info,
    ):
        assign_speckit_agent_command()
    exit_code = exc_info.value.code
    return json.loads(capsys.readouterr().out), exit_code if isinstance(exit_code, int) else 1


class TestAssignSpeckitAgentCommand:
    """CLI tests for cloud-agent dispatch and tracking."""

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    def test_phase_one_includes_unattended_no_wait_instruction(
        self, mock_api, mock_assign, monkeypatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "secret")
        mock_api.side_effect = [
            json.dumps([]),
            json.dumps([]),
            json.dumps([{"name": "speckit:agent-assigned-phase-1"}, {"name": "speckit:processing"}]),
            "{}",
            "{}",
            "{}",
        ]
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="agent_assignment",
            task_id="event-1",
            token_identity="SPECKIT_PR_TOKEN",
            session_confirmed=True,
        )

        _invoke(
            [
                "--issue-number",
                "42",
                "--phase",
                "1",
                "--hierarchy-level",
                "feature",
                "--repo",
                "owner/repo",
            ],
            capsys,
        )

        instructions = mock_assign.call_args.kwargs["custom_instructions"]
        assert "This run is unattended. Do not wait for user answers" in instructions

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    def test_dispatches_phase_with_marker_and_audit_fields(
        self, mock_api, mock_assign, monkeypatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "secret")
        mock_api.side_effect = [
            json.dumps([]),
            json.dumps([]),
            json.dumps([{"name": "speckit:agent-assigned-phase-2"}, {"name": "speckit:processing"}]),
            "{}",
            "{}",
            "{}",
        ]
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="agent_assignment",
            task_id="event-1",
            token_identity="SPECKIT_PR_TOKEN",
            session_confirmed=True,
        )

        payload, code = _invoke(
            [
                "--issue-number",
                "42",
                "--phase",
                "2",
                "--hierarchy-level",
                "feature",
                "--repo",
                "owner/repo",
                "--model",
                "claude-sonnet-5",
                "--base-branch",
                "speckit/42/phase-1-specify",
                "--correlation-id",
                "11111111-1111-4111-8111-AAAAAAAAAAAA",
            ],
            capsys,
        )

        assert code == 0
        assert payload["engine"] == "cloud-agent"
        assert payload["phase"] == 2
        assert payload["issue_number"] == 42
        assert payload["task_id"] == "event-1"
        assert payload["token_identity"] == "SPECKIT_PR_TOKEN"
        assert payload["status"] == "dispatched"
        assert payload["correlation_id"] == "11111111-1111-4111-8111-aaaaaaaaaaaa"
        instructions = mock_assign.call_args.kwargs["custom_instructions"]
        assert "speckit:agent-assigned schema_version=1" in instructions
        assert "Copy the marker into the pull request description unchanged" in instructions
        assert "This run is unattended. Do not wait for user answers" in instructions
        assert mock_assign.call_args.kwargs["custom_agent"] == "speckit.clarify"
        assert mock_assign.call_args.kwargs["base_branch"] == "speckit/42/phase-1-specify"
        assert mock_assign.call_args.kwargs["allow_preexisting_assignment"] is False

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    def test_returns_already_in_flight_without_assignment(
        self, mock_api, mock_assign, monkeypatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "secret")
        mock_api.return_value = json.dumps([{"name": "speckit:agent-assigned-phase-1"}])

        payload, code = _invoke(["--issue-number", "7", "--phase", "1", "--repo", "owner/repo"], capsys)

        assert code == 0
        assert payload["status"] == "already-in-flight"
        assert payload["task_id"] == ""
        mock_assign.assert_not_called()

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    def test_uses_copilot_pr_as_in_flight_guard(
        self, mock_api, mock_assign, monkeypatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "secret")
        mock_api.side_effect = [
            json.dumps([]),
            (
                json.dumps(
                    [
                        {
                            "user": {"login": "copilot-swe-agent[bot]"},
                            "head": {"ref": "other"},
                            "body": "",
                        }
                    ]
                )
                + "\n"
                + json.dumps(
                    [
                        {
                            "user": {"login": "copilot-swe-agent[bot]"},
                            "head": {"ref": "speckit/7/phase-1-specify"},
                            "base": {"ref": "main"},
                            "body": (
                                "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
                                "issue=7 phase=1 hierarchy=feature correlation_id=abc -->"
                            ),
                        }
                    ]
                )
            ),
        ]

        payload, code = _invoke(["--issue-number", "7", "--phase", "1", "--repo", "owner/repo"], capsys)

        assert code == 0
        assert payload["status"] == "already-in-flight"
        mock_assign.assert_not_called()

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    def test_assignment_without_confirmed_session_is_rejected(
        self, mock_api, mock_assign, monkeypatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "secret")
        mock_api.side_effect = [json.dumps([]), json.dumps([])]
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="agent_assignment",
            task_id="",
            token_identity="COPILOT_GITHUB_TOKEN",
            session_confirmed=False,
        )

        payload, code = _invoke(["--issue-number", "9", "--phase", "3", "--repo", "owner/repo"], capsys)

        assert code == 1
        assert payload["status"] == "assignment-unconfirmed"
        assert payload["session_confirmed"] is False
        assert mock_api.call_count == 2

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    def test_reports_assignment_failure_without_mutations(
        self, mock_api, mock_assign, monkeypatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "secret")
        mock_api.side_effect = [json.dumps([]), json.dumps([])]
        mock_assign.return_value = AgentAssignmentResult(
            success=False,
            method="",
            token_identity="COPILOT_GITHUB_TOKEN",
            error="assignment failed",
        )

        payload, code = _invoke(["--issue-number", "9", "--phase", "3", "--repo", "owner/repo"], capsys)

        assert code == 1
        assert payload["status"] == "assignment-failed"
        assert payload["task_id"] == ""
        assert mock_api.call_count == 2

    def test_rejects_invalid_phase(self) -> None:
        with (
            patch.object(sys, "argv", ["agdt-assign-speckit-agent", "--issue-number", "1", "--phase", "4"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            assign_speckit_agent_command()
        assert exc_info.value.code == 2

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    def test_missing_token_returns_assignment_failure(self, mock_assign, monkeypatch, capsys) -> None:
        monkeypatch.delenv("SPECKIT_PR_TOKEN", raising=False)
        monkeypatch.delenv("COPILOT_GITHUB_TOKEN", raising=False)
        payload, code = _invoke(["--issue-number", "9", "--phase", "1", "--repo", "owner/repo"], capsys)
        assert code == 1
        assert payload["status"] == "assignment-failed"
        mock_assign.assert_not_called()

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    @pytest.mark.parametrize("error", [RuntimeError("API unavailable"), RetryableError("rate limit")])
    def test_in_flight_check_failure_is_reported(self, mock_api, mock_assign, monkeypatch, capsys, error) -> None:
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "secret")
        mock_api.side_effect = error
        payload, code = _invoke(["--issue-number", "9", "--phase", "1", "--repo", "owner/repo"], capsys)
        assert code == 1
        assert payload["status"] == "assignment-failed"
        mock_assign.assert_not_called()

    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    def test_partial_tracking_failure_keeps_labels_when_marker_write_fails(
        self, mock_assign, mock_api, monkeypatch, capsys
    ) -> None:
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "secret")
        mock_api.side_effect = [
            json.dumps([]),
            json.dumps([]),
            json.dumps([{"name": "speckit:agent-assigned-phase-1"}, {"name": "speckit:processing"}]),
            "{}",
            RuntimeError("marker failed"),
        ]
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="agent_assignment",
            task_id="event-1",
            token_identity="SPECKIT_PR_TOKEN",
            session_confirmed=True,
        )
        payload, code = _invoke(["--issue-number", "9", "--phase", "1", "--repo", "owner/repo"], capsys)
        assert code == 1
        assert payload["status"] == "partial-tracking-failure"
        assert mock_api.call_count == 5

    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    def test_notice_failure_is_reported_as_warning_without_failing_dispatch(
        self, mock_assign, mock_api, monkeypatch, capsys
    ) -> None:
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "secret")
        mock_api.side_effect = [
            json.dumps([]),
            json.dumps([]),
            json.dumps([{"name": "speckit:agent-assigned-phase-1"}, {"name": "speckit:processing"}]),
            "{}",
            "{}",
            RuntimeError("notice failed"),
        ]
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="agent_assignment",
            task_id="event-1",
            token_identity="SPECKIT_PR_TOKEN",
            session_confirmed=True,
        )
        payload, code = _invoke(["--issue-number", "9", "--phase", "1", "--repo", "owner/repo"], capsys)
        assert code == 0
        assert payload["status"] == "dispatched"
        assert "Non-authoritative notice failed" in payload["warning"]
        assert mock_api.call_count == 6

    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    def test_retryable_notice_failure_is_reported_as_warning_without_failing_dispatch(
        self, mock_assign, mock_api, monkeypatch, capsys
    ) -> None:
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "secret")
        mock_api.side_effect = [
            json.dumps([]),
            json.dumps([]),
            json.dumps([{"name": "speckit:agent-assigned-phase-1"}, {"name": "speckit:processing"}]),
            "{}",
            "{}",
            RetryableError("notice failed"),
        ]
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="agent_assignment",
            task_id="event-1",
            token_identity="SPECKIT_PR_TOKEN",
            session_confirmed=True,
        )
        payload, code = _invoke(["--issue-number", "9", "--phase", "1", "--repo", "owner/repo"], capsys)
        assert code == 0
        assert payload["status"] == "dispatched"
        assert "Non-authoritative notice failed" in payload["warning"]
        assert mock_api.call_count == 6

    @pytest.mark.parametrize(
        ("argv", "status"),
        [
            (["--issue-number", "1", "--phase", "1", "--repo", "invalid"], "invalid-repository"),
            (["--issue-number", "0", "--phase", "1", "--repo", "owner/repo"], "invalid-issue-number"),
            (
                ["--issue-number", "1", "--phase", "1", "--repo", "owner/repo", "--base-branch", "feature/not-main"],
                "invalid-base-branch",
            ),
            (
                ["--issue-number", "1", "--phase", "1", "--repo", "owner/repo", "--correlation-id", "job-42"],
                "invalid-correlation-id",
            ),
            (
                ["--issue-number", "1", "--phase", "1", "--repo", "owner/repo", "--correlation-id", "deadbeef"],
                "invalid-correlation-id",
            ),
            (
                ["--issue-number", "1", "--phase", "1", "--repo", "owner/repo", "--correlation-id", "-"],
                "invalid-correlation-id",
            ),
        ],
    )
    def test_rejects_invalid_dispatch_arguments(self, argv: list[str], status: str, capsys) -> None:
        payload, code = _invoke(argv, capsys)
        assert code == 1
        assert payload["status"] == status

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    @pytest.mark.parametrize(
        ("issue", "phase", "hierarchy", "expected_base", "spec_dir"),
        [
            (5, 1, "feature", "main", None),
            (5, 2, "feature", "speckit/5/phase-1-specify", None),
            (5, 3, "feature", "speckit/5/phase-2-clarify", None),
            (5, 3, "task", "main", "specs/100/101"),
        ],
    )
    def test_derives_default_base_branch_from_phase_when_omitted(
        self,
        mock_api,
        mock_assign,
        monkeypatch,
        capsys: pytest.CaptureFixture[str],
        issue: int,
        phase: int,
        hierarchy: str,
        expected_base: str,
        spec_dir: str | None,
    ) -> None:
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "secret")
        mock_api.side_effect = [
            json.dumps([]),
            json.dumps([]),
            json.dumps([{"name": f"speckit:agent-assigned-phase-{phase}"}, {"name": "speckit:processing"}]),
            "{}",
            "{}",
            "{}",
        ]
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="agent_assignment",
            task_id="event-x",
            token_identity="SPECKIT_PR_TOKEN",
            session_confirmed=True,
        )
        _invoke(
            [
                "--issue-number",
                str(issue),
                "--phase",
                str(phase),
                "--hierarchy-level",
                hierarchy,
                *(["--spec-dir", spec_dir] if spec_dir else []),
                "--repo",
                "owner/repo",
            ],
            capsys,
        )
        assert mock_assign.call_args.kwargs["base_branch"] == expected_base

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.commands._gh_api_call")
    def test_task_phase_three_includes_spec_dir_instructions(
        self, mock_api, mock_assign, monkeypatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "secret")
        mock_api.side_effect = [
            json.dumps([]),
            json.dumps([]),
            json.dumps([{"name": "speckit:agent-assigned-phase-3"}, {"name": "speckit:processing"}]),
            "{}",
            "{}",
            "{}",
        ]
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="agent_assignment",
            task_id="event-task",
            token_identity="SPECKIT_PR_TOKEN",
            session_confirmed=True,
        )

        _invoke(
            [
                "--issue-number",
                "101",
                "--phase",
                "3",
                "--hierarchy-level",
                "task",
                "--spec-dir",
                "specs/100/101",
                "--repo",
                "owner/repo",
            ],
            capsys,
        )

        instructions = mock_assign.call_args.kwargs["custom_instructions"]
        assert 'SPECIFY_FEATURE_DIRECTORY="specs/100/101"' in instructions
        assert "task spec and inherited parent context resolve correctly" in instructions

    def test_rejects_invalid_spec_dir(self, capsys: pytest.CaptureFixture[str]) -> None:
        payload, code = _invoke(
            [
                "--issue-number",
                "1",
                "--phase",
                "3",
                "--hierarchy-level",
                "task",
                "--spec-dir",
                "../outside",
                "--repo",
                "owner/repo",
            ],
            capsys,
        )
        assert code == 1
        assert payload["status"] == "invalid-spec-dir"

    def test_rejects_absolute_spec_dir(self, capsys: pytest.CaptureFixture[str]) -> None:
        payload, code = _invoke(
            [
                "--issue-number",
                "1",
                "--phase",
                "3",
                "--hierarchy-level",
                "task",
                "--spec-dir",
                "/specs/100/101",
                "--repo",
                "owner/repo",
            ],
            capsys,
        )
        assert code == 1
        assert payload["status"] == "invalid-spec-dir"

    def test_rejects_spec_dir_with_unsafe_characters(self, capsys: pytest.CaptureFixture[str]) -> None:
        payload, code = _invoke(
            [
                "--issue-number",
                "1",
                "--phase",
                "3",
                "--hierarchy-level",
                "task",
                "--spec-dir",
                'specs/x"; command #',
                "--repo",
                "owner/repo",
            ],
            capsys,
        )
        assert code == 1
        assert payload["status"] == "invalid-spec-dir"

    def test_rejects_task_phase_three_without_spec_dir(self, capsys: pytest.CaptureFixture[str]) -> None:
        payload, code = _invoke(
            [
                "--issue-number",
                "1",
                "--phase",
                "3",
                "--hierarchy-level",
                "task",
                "--repo",
                "owner/repo",
            ],
            capsys,
        )
        assert code == 1
        assert payload["status"] == "invalid-spec-dir"
