"""Tests for assign_implementation_agent_command()."""

from __future__ import annotations

import json
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.agent_assignment import AgentAssignmentResult
from agentic_devtools.cli.ci.commands import assign_implementation_agent_command


class TestAssignImplementationAgentCommand:
    """CLI tests for assigning implementation coding agent."""

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    def test_exits_zero_on_success(self, mock_assign, capsys: pytest.CaptureFixture[str]) -> None:
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="coding_agent_task",
            task_id="task-1",
            task_url="https://example/task-1",
            attempts=1,
            token_identity="SPECKIT_PR_TOKEN",
        )

        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-assign-implementation-agent",
                    "--issue-number",
                    "42",
                    "--spec-dir",
                    "specs/123-feature",
                    "--repo",
                    "owner/repo",
                    "--model",
                    "claude-opus-4.6",
                ],
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            assign_implementation_agent_command()

        assert exc_info.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert output["success"] is True
        kwargs = mock_assign.call_args.kwargs
        assert kwargs["repo"] == "owner/repo"
        assert kwargs["issue_number"] == 42
        assert kwargs["custom_agent"] == "speckit.implement"
        assert kwargs["model"] == "claude-opus-4.6"
        assert "specs/123-feature/tasks.md" in kwargs["problem_statement"]

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    def test_exits_nonzero_on_assignment_failure(self, mock_assign) -> None:
        mock_assign.return_value = AgentAssignmentResult(
            success=False,
            method="",
            token_identity="SPECKIT_PR_TOKEN",
            error="failed",
        )

        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-assign-implementation-agent",
                    "--issue-number",
                    "42",
                    "--spec-dir",
                    "specs/123-feature",
                    "--repo",
                    "owner/repo",
                ],
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            assign_implementation_agent_command()

        assert exc_info.value.code == 1

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    def test_uses_parent_context_when_spec_context_is_provided(self, mock_assign) -> None:
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="coding_agent_task",
            task_id="task-2",
            task_url="https://example/task-2",
            attempts=1,
            token_identity="SPECKIT_PR_TOKEN",
        )

        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-assign-implementation-agent",
                    "--issue-number",
                    "42",
                    "--spec-dir",
                    "specs/100/200/300-task",
                    "--spec-context",
                    "specs/100/200/spec.md",
                    "--repo",
                    "owner/repo",
                ],
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            assign_implementation_agent_command()

        assert exc_info.value.code == 0
        kwargs = mock_assign.call_args.kwargs
        assert "specs/100/200/300-task/tasks.md" in kwargs["problem_statement"]
        assert "specs/100/200/spec.md" in kwargs["problem_statement"]
        assert "specs/100/200/plan.md" in kwargs["problem_statement"]

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    def test_uses_repo_root_plan_path_when_spec_context_has_no_parent(self, mock_assign) -> None:
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="coding_agent_task",
            task_id="task-3",
            task_url="https://example/task-3",
            attempts=1,
            token_identity="SPECKIT_PR_TOKEN",
        )

        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-assign-implementation-agent",
                    "--issue-number",
                    "42",
                    "--spec-dir",
                    "specs/300-task",
                    "--spec-context",
                    "spec.md",
                    "--repo",
                    "owner/repo",
                ],
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            assign_implementation_agent_command()

        assert exc_info.value.code == 0
        kwargs = mock_assign.call_args.kwargs
        assert "plan.md" in kwargs["problem_statement"]
        assert "./plan.md" not in kwargs["problem_statement"]

    @patch("agentic_devtools.cli.ci.commands.assign_issue_to_agent")
    def test_uses_parent_context_when_spec_context_uses_windows_separator(self, mock_assign) -> None:
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="coding_agent_task",
            task_id="task-4",
            task_url="https://example/task-4",
            attempts=1,
            token_identity="SPECKIT_PR_TOKEN",
        )

        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-assign-implementation-agent",
                    "--issue-number",
                    "42",
                    "--spec-dir",
                    "specs/100/200/300-task",
                    "--spec-context",
                    "specs\\100\\200\\spec.md",
                    "--repo",
                    "owner/repo",
                ],
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            assign_implementation_agent_command()

        assert exc_info.value.code == 0
        kwargs = mock_assign.call_args.kwargs
        assert "specs/100/200/spec.md" in kwargs["problem_statement"]
        assert "specs/100/200/plan.md" in kwargs["problem_statement"]

    def test_exits_nonzero_when_repo_missing(self) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-assign-implementation-agent",
                    "--issue-number",
                    "42",
                    "--spec-dir",
                    "specs/123-feature",
                ],
            ),
            patch.dict("os.environ", {}, clear=True),
            pytest.raises(SystemExit) as exc_info,
        ):
            assign_implementation_agent_command()

        assert exc_info.value.code == 1

    def test_exits_nonzero_when_spec_dir_empty_after_normalization(self) -> None:
        for empty_spec_dir in ["/", "////", "  /  "]:
            with (
                patch.object(
                    sys,
                    "argv",
                    [
                        "agdt-assign-implementation-agent",
                        "--issue-number",
                        "42",
                        "--spec-dir",
                        empty_spec_dir,
                        "--repo",
                        "owner/repo",
                    ],
                ),
                pytest.raises(SystemExit) as exc_info,
            ):
                assign_implementation_agent_command()

            assert exc_info.value.code == 1

    @pytest.mark.parametrize(
        "bad_repo",
        [
            "invalid-repo-format",
            "owner/repo/extra",
            "owner/",
            "/repo",
        ],
    )
    def test_exits_nonzero_when_repo_format_invalid(self, bad_repo: str) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-assign-implementation-agent",
                    "--issue-number",
                    "42",
                    "--spec-dir",
                    "specs/123-feature",
                    "--repo",
                    bad_repo,
                ],
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            assign_implementation_agent_command()

        assert exc_info.value.code == 1

    @pytest.mark.parametrize("bad_number", ["0", "-1", "-100"])
    def test_exits_nonzero_when_issue_number_not_positive(self, bad_number: str) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-assign-implementation-agent",
                    "--issue-number",
                    bad_number,
                    "--spec-dir",
                    "specs/123-feature",
                    "--repo",
                    "owner/repo",
                ],
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            assign_implementation_agent_command()

        assert exc_info.value.code == 1
