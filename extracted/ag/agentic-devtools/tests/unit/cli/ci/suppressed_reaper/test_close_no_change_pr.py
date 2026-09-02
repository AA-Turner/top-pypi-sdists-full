"""Tests for suppressed_reaper.close_no_change_pr()."""

from __future__ import annotations

import logging

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo, IssueFacts, PRMetadata
from agentic_devtools.cli.ci.suppressed_reaper import (
    ReapDecision,
    build_deferral_issue_comment,
    close_no_change_pr,
    evaluate_pr,
)
from tests.unit.cli.ci.suppressed_reaper._fixtures import ISSUE, TABLE, brief, provider


def _eligible() -> ReapDecision:
    return evaluate_pr(provider(), brief())


class TestCloseNoChangePr:
    """The close side effects and their ordering."""

    def test_posts_the_verdict_table_then_closes_the_issue_and_the_pr(self) -> None:
        """The HEAD is rechecked before mutating, then the issue is closed before the PR."""
        mock = provider()
        decision = _eligible()
        close_no_change_pr(mock, brief(), decision)

        assert mock.get_pr_metadata.call_args.args == (99,)
        issue_number, body = mock.post_issue_comment.call_args.args
        assert issue_number == ISSUE
        assert decision.verdict_table is not None and decision.verdict_table in body
        mock.close_issue.assert_called_once_with(ISSUE, reason="completed")
        mock.close_pr.assert_called_once()
        assert mock.close_pr.call_args.args[0] == 99

    def test_branch_is_deleted_only_after_the_pr_is_closed(self) -> None:
        """A failed PR close never strands the branch."""
        mock = provider()
        mock.close_pr.side_effect = RuntimeError("boom")
        with pytest.raises(RuntimeError):
            close_no_change_pr(mock, brief(), _eligible())
        mock.delete_branch.assert_not_called()

    def test_branch_is_deleted_after_a_successful_close(self) -> None:
        """The head branch is removed once the PR is closed."""
        mock = provider()
        close_no_change_pr(mock, brief(), _eligible())
        mock.delete_branch.assert_called_once_with("copilot/triage")

    def test_resume_after_issue_close_skips_reposting_and_reclosing_the_issue(self) -> None:
        """A prior issue-close success resumes by closing only the PR and branch."""
        mock = provider()
        original_issue_body = mock.get_issue_facts.return_value.body
        mock.get_issue_facts.return_value = IssueFacts(number=ISSUE, state="closed", body=original_issue_body)
        mock.list_issue_comments.return_value = [
            IssueCommentInfo(id=1, author="github-actions[bot]", body=build_deferral_issue_comment(99, TABLE))
        ]
        decision = evaluate_pr(mock, brief())

        close_no_change_pr(mock, brief(), decision)

        mock.post_issue_comment.assert_not_called()
        mock.close_issue.assert_not_called()
        mock.close_pr.assert_called_once_with(
            99,
            comment="Closed automatically: empty diff, no changes warranted. Verdicts recorded on #1240.",
        )
        mock.delete_branch.assert_called_once_with("copilot/triage")

    def test_fork_branches_are_never_deleted(self) -> None:
        """A branch in a fork is not ours to delete."""
        mock = provider()
        close_no_change_pr(mock, brief(is_cross_repository=True), _eligible())
        mock.delete_branch.assert_not_called()

    def test_unknown_branch_is_not_deleted(self) -> None:
        """An empty branch name is never passed to the provider."""
        mock = provider()
        close_no_change_pr(mock, brief(head_branch=""), _eligible())
        mock.delete_branch.assert_not_called()

    def test_non_copilot_same_repo_branch_is_not_deleted(self) -> None:
        """Only the managed ``copilot/`` namespace is eligible for cleanup."""
        mock = provider()
        close_no_change_pr(mock, brief(head_branch="release/2026.08"), _eligible())
        mock.delete_branch.assert_not_called()

    def test_branch_deletion_failure_is_logged_and_swallowed(self, caplog: pytest.LogCaptureFixture) -> None:
        """The PR is already closed, so a failed branch delete is not fatal."""
        mock = provider()
        mock.delete_branch.side_effect = RuntimeError("boom")
        with caplog.at_level(logging.WARNING):
            close_no_change_pr(mock, brief(), _eligible())
        assert "Failed to delete branch" in caplog.text

    def test_branch_not_deleted_when_sha_changes_after_pr_close(self, caplog: pytest.LogCaptureFixture) -> None:
        """A new commit pushed after the PR is closed prevents branch deletion."""
        mock = provider()
        new_sha = "x" * 40
        # get_ref_sha returns a different tip after the PR mutations complete
        mock.get_ref_sha.return_value = new_sha
        with caplog.at_level(logging.WARNING):
            close_no_change_pr(mock, brief(), _eligible())
        mock.delete_branch.assert_not_called()
        assert "tip changed after PR close" in caplog.text

    def test_head_change_skips_before_any_mutation(self) -> None:
        """A PR whose HEAD changed after evaluation is left open for a fresh pass."""
        mock = provider()
        mock.get_pr_metadata.return_value = PRMetadata(
            number=99,
            title="No changes needed",
            head_branch="copilot/triage",
            head_sha="new-head",
            base_branch="main",
        )
        with pytest.raises(RuntimeError, match="head changed after evaluation"):
            close_no_change_pr(mock, brief(), _eligible())
        mock.post_issue_comment.assert_not_called()
        mock.close_pr.assert_not_called()
        mock.close_issue.assert_not_called()

    @pytest.mark.parametrize(
        "decision",
        [
            ReapDecision(99, False, "no-marker"),
            ReapDecision(99, True, "eligible", None, "| table |"),
            ReapDecision(99, True, "eligible", ISSUE, None),
            ReapDecision(99, True, "eligible", ISSUE, "| table |", None),
        ],
    )
    def test_non_eligible_decisions_are_refused(self, decision: ReapDecision) -> None:
        """Closing is only ever driven by a fully-validated decision."""
        mock = provider()
        with pytest.raises(ValueError, match="not eligible for closing"):
            close_no_change_pr(mock, brief(), decision)
        mock.close_pr.assert_not_called()

    def test_mismatched_pr_number_is_refused(self) -> None:
        """A decision for a different PR number than the brief is rejected before any mutation."""
        mock = provider()
        decision = _eligible()
        mismatched_brief = brief(number=decision.pr_number + 1)
        with pytest.raises(ValueError, match="Decision is for PR #"):
            close_no_change_pr(mock, mismatched_brief, decision)
        mock.close_pr.assert_not_called()
        mock.post_issue_comment.assert_not_called()
