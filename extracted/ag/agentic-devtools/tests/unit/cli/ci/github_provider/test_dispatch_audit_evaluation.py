"""Tests for GitHubActionsProvider.dispatch_audit_evaluation()."""

import logging
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.agent_assignment import AgentAssignmentResult
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


class TestDispatchAuditEvaluation:
    """Tests for coding-agent based audit evaluation dispatch."""

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    def test_dispatches_via_shared_assignment_helper(
        self,
        mock_read_repo_file,
        mock_assign,
    ) -> None:
        mock_read_repo_file.return_value = "# prompt"
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="coding_agent_task",
            task_id="task-77",
            task_url="https://example/task-77",
            attempts=1,
            token_identity="SPECKIT_PR_TOKEN",
            session_confirmed=True,
        )
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            result = provider.dispatch_audit_evaluation(
                tracking_issue=2042,
                batch_id="batch-123",
                batch_branch="audit/batch-batch123",
                batch_dir="audit-batches/batch-123",
                pr_numbers=[10, 11],
            )

        assert result.success is True
        assert result.session_confirmed is True
        assert result.task_id == "task-77"
        kwargs = mock_assign.call_args.kwargs
        assert kwargs["repo"] == "swai-factory/agentic-devtools"
        assert kwargs["issue_number"] == 2042
        assert kwargs["custom_agent"] == "agdt.review-feedback-audit.evaluate"
        assert kwargs["token_env_vars"] == ("SPECKIT_PR_TOKEN",)
        assert "audit-batches/batch-123/batch-summary.md" in kwargs["problem_statement"]
        assert "`AGENTS.md` for directory-scoped guidance" in kwargs["problem_statement"]
        assert "`.github/copilot-instructions.md` for repository-wide guidance" in kwargs["problem_statement"]
        assert kwargs["problem_statement"] == kwargs["custom_instructions"]

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    def test_raises_when_speckit_token_missing(self, mock_assign) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(RuntimeError, match="SPECKIT_PR_TOKEN"):
                provider.dispatch_audit_evaluation(
                    tracking_issue=2042,
                    batch_id="batch-123",
                    batch_branch="audit/batch-batch123",
                    batch_dir="audit-batches/batch-123",
                    pr_numbers=[10],
                )
        mock_assign.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    def test_raises_when_assignment_fails(
        self,
        mock_read_repo_file,
        mock_assign,
    ) -> None:
        mock_read_repo_file.return_value = "# prompt"
        mock_assign.return_value = AgentAssignmentResult(
            success=False,
            method="",
            token_identity="SPECKIT_PR_TOKEN",
            error="all methods failed",
        )
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            with pytest.raises(RuntimeError, match="all methods failed"):
                provider.dispatch_audit_evaluation(
                    tracking_issue=2042,
                    batch_id="batch-123",
                    batch_branch="audit/batch-batch123",
                    batch_dir="audit-batches/batch-123",
                    pr_numbers=[10, 11],
                )

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    def test_succeeds_when_session_is_not_confirmed(
        self,
        mock_read_repo_file,
        mock_assign,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        mock_read_repo_file.return_value = "# prompt"
        mock_assign.return_value = AgentAssignmentResult(
            success=True,
            method="agent_assignment",
            task_id="",
            task_url="",
            attempts=1,
            token_identity="SPECKIT_PR_TOKEN",
            session_confirmed=False,
        )
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with (
            caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.github_provider"),
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True),
        ):
            result = provider.dispatch_audit_evaluation(
                tracking_issue=2042,
                batch_id="batch-123",
                batch_branch="audit/batch-batch123",
                batch_dir="audit-batches/batch-123",
                pr_numbers=[10, 11],
            )

        assert result.success is True
        assert result.session_confirmed is False
        assert "session_confirmed=False" in caplog.text

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    def test_raises_when_prompt_file_cannot_be_read(
        self,
        mock_read_repo_file,
        mock_assign,
    ) -> None:
        """dispatch_audit_evaluation must fail fast when the agent prompt file is missing."""
        mock_read_repo_file.return_value = ""
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            with pytest.raises(RuntimeError, match="Could not read required agent prompt file"):
                provider.dispatch_audit_evaluation(
                    tracking_issue=2042,
                    batch_id="batch-123",
                    batch_branch="audit/batch-batch123",
                    batch_dir="audit-batches/batch-123",
                    pr_numbers=[10, 11],
                )

        mock_assign.assert_not_called()
