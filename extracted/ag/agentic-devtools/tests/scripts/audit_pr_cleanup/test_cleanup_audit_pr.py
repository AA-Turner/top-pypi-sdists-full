"""Unit tests for cleanup_audit_pr in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError, cleanup_audit_pr


def test_cleanup_audit_pr_validation_errors() -> None:
    """cleanup_audit_pr raises ValueError for non-positive PR number or empty comment."""
    with pytest.raises(ValueError, match="PR number must be positive"):
        cleanup_audit_pr(pr_number=0, comment="Valid comment")

    with pytest.raises(ValueError, match="PR comment text cannot be empty"):
        cleanup_audit_pr(pr_number=123, comment="   ")


def test_cleanup_audit_pr_rejects_bool_pr_number() -> None:
    """cleanup_audit_pr raises ValueError when pr_number is a bool (bool is int subclass)."""
    with pytest.raises(ValueError, match="PR number must be an integer"):
        cleanup_audit_pr(pr_number=True, comment="Valid comment")  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="PR number must be an integer"):
        cleanup_audit_pr(pr_number=False, comment="Valid comment")  # type: ignore[arg-type]


def test_cleanup_audit_pr_rejects_non_integer_pr_number() -> None:
    """cleanup_audit_pr raises ValueError for non-integer types such as str or None."""
    with pytest.raises(ValueError, match="PR number must be an integer"):
        cleanup_audit_pr(pr_number="123", comment="Valid comment")  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="PR number must be an integer"):
        cleanup_audit_pr(pr_number=None, comment="Valid comment")  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [float("nan"), float("inf")])
def test_cleanup_audit_pr_rejects_non_finite_retry_delay(value: float) -> None:
    """cleanup_audit_pr rejects NaN and infinite retry delays before mutating anything."""
    with pytest.raises(ValueError, match="retry_delay must be finite and non-negative"):
        cleanup_audit_pr(pr_number=123, comment="Valid comment", retry_delay=value)


def test_cleanup_audit_pr_issue_comment_without_related_issue_raises_before_pr_mutation() -> None:
    """cleanup_audit_pr raises ValueError when issue_comment is provided without related_issue."""
    with patch("scripts.audit_pr_cleanup.post_pr_comment") as mock_pr_comment:
        with pytest.raises(ValueError, match="issue_comment requires related_issue"):
            cleanup_audit_pr(
                pr_number=123,
                comment="PR comment body",
                issue_comment="Some issue comment",
            )
    mock_pr_comment.assert_not_called()


def test_cleanup_audit_pr_full_workflow_success() -> None:
    """cleanup_audit_pr executes comments and closures across PR and related issue."""
    with (
        patch("scripts.audit_pr_cleanup.post_pr_comment", return_value=True) as mock_pr_comment,
        patch("scripts.audit_pr_cleanup.get_pr_head_branch", return_value="feature/branch-123") as mock_head,
        patch("scripts.audit_pr_cleanup.close_pr") as mock_pr_close,
        patch("scripts.audit_pr_cleanup.delete_remote_branch") as mock_del_branch,
        patch("scripts.audit_pr_cleanup.is_pr_closed", return_value=True) as mock_pr_state,
        patch("scripts.audit_pr_cleanup.branch_exists", return_value=False) as mock_branch_state,
        patch("scripts.audit_pr_cleanup.post_issue_comment", return_value=True) as mock_issue_comment,
        patch("scripts.audit_pr_cleanup.close_issue") as mock_issue_close,
        patch("scripts.audit_pr_cleanup.is_issue_closed", return_value=True) as mock_issue_state,
    ):
        result = cleanup_audit_pr(
            pr_number=123,
            comment="PR comment body",
            related_issue=456,
            issue_comment="Issue comment body",
            delete_branch=True,
            dry_run=False,
            max_retries=3,
            retry_delay=0.1,
        )

        assert result.pr_number == 123
        assert result.pr_commented is True
        assert result.pr_closed is True
        assert result.branch_deleted is True
        assert result.issue_commented is True
        assert result.issue_closed is True
        assert result.success is True
        assert result.error_message is None

        mock_pr_comment.assert_called_once_with(
            pr_number=123,
            comment="PR comment body",
            dry_run=False,
            max_retries=3,
            retry_delay=0.1,
        )
        mock_head.assert_called_once_with(
            123,
            dry_run=False,
            max_retries=3,
            retry_delay=0.1,
        )
        mock_pr_close.assert_called_once_with(
            pr_number=123,
            dry_run=False,
            max_retries=3,
            retry_delay=0.1,
        )
        mock_pr_state.assert_called_once_with(
            pr_number=123,
            dry_run=False,
            max_retries=3,
            retry_delay=0.1,
        )
        mock_del_branch.assert_called_once_with(
            branch_name="feature/branch-123",
            dry_run=False,
            max_retries=3,
            retry_delay=0.1,
        )
        mock_branch_state.assert_called_once_with(
            branch_name="feature/branch-123",
            dry_run=False,
            max_retries=3,
            retry_delay=0.1,
        )
        mock_issue_comment.assert_called_once_with(
            issue_number=456,
            comment="Issue comment body",
            dry_run=False,
            max_retries=3,
            retry_delay=0.1,
        )
        mock_issue_close.assert_called_once_with(
            issue_number=456,
            dry_run=False,
            max_retries=3,
            retry_delay=0.1,
        )
        mock_issue_state.assert_called_once_with(
            issue_number=456,
            dry_run=False,
            max_retries=3,
            retry_delay=0.1,
        )


def test_cleanup_audit_pr_without_related_issue_and_no_branch_delete() -> None:
    """cleanup_audit_pr preserves a no-op PR comment result while still closing the PR."""
    with (
        patch("scripts.audit_pr_cleanup.post_pr_comment", return_value=False) as mock_pr_comment,
        patch("scripts.audit_pr_cleanup.close_pr") as mock_pr_close,
        patch("scripts.audit_pr_cleanup.is_pr_closed", return_value=True) as mock_pr_state,
        patch("scripts.audit_pr_cleanup.branch_exists") as mock_branch_state,
        patch("scripts.audit_pr_cleanup.post_issue_comment") as mock_issue_comment,
        patch("scripts.audit_pr_cleanup.close_issue") as mock_issue_close,
        patch("scripts.audit_pr_cleanup.is_issue_closed") as mock_issue_state,
    ):
        result = cleanup_audit_pr(
            pr_number=789,
            comment="PR evaluation",
            delete_branch=False,
            dry_run=True,
        )

        assert result.pr_number == 789
        assert result.pr_commented is False
        assert result.pr_closed is True
        assert result.branch_deleted is False
        assert result.issue_commented is False
        assert result.issue_closed is False
        assert result.success is True

        mock_pr_comment.assert_called_once_with(
            pr_number=789,
            comment="PR evaluation",
            dry_run=True,
            max_retries=3,
            retry_delay=0.0,
        )
        mock_pr_close.assert_called_once()
        mock_pr_state.assert_called_once_with(
            pr_number=789,
            dry_run=True,
            max_retries=3,
            retry_delay=0.0,
        )
        mock_branch_state.assert_not_called()
        mock_issue_comment.assert_not_called()
        mock_issue_close.assert_not_called()
        mock_issue_state.assert_not_called()


def test_cleanup_audit_pr_issue_comment_fallback_to_pr_comment() -> None:
    """cleanup_audit_pr preserves a no-op issue comment result while still closing the issue."""
    with (
        patch("scripts.audit_pr_cleanup.post_pr_comment", return_value=True),
        patch("scripts.audit_pr_cleanup.close_pr"),
        patch("scripts.audit_pr_cleanup.is_pr_closed", return_value=True),
        patch("scripts.audit_pr_cleanup.post_issue_comment", return_value=False) as mock_issue_comment,
        patch("scripts.audit_pr_cleanup.close_issue"),
        patch("scripts.audit_pr_cleanup.is_issue_closed", return_value=True),
    ):
        result = cleanup_audit_pr(
            pr_number=101,
            comment="Universal comment text",
            related_issue=202,
            issue_comment=None,
        )
        assert result.success is True
        assert result.issue_commented is False
        mock_issue_comment.assert_called_once_with(
            issue_number=202,
            comment="Universal comment text",
            dry_run=False,
            max_retries=3,
            retry_delay=0.0,
        )


def test_cleanup_audit_pr_invalid_related_issue_fails_before_pr_mutation() -> None:
    """cleanup_audit_pr validates related_issue before posting the PR comment."""
    with patch("scripts.audit_pr_cleanup.post_pr_comment") as mock_pr_comment:
        with pytest.raises(ValueError, match="Unsupported issue URL repository"):
            cleanup_audit_pr(
                pr_number=123,
                comment="PR comment body",
                related_issue="https://github.com/other/repo/issues/456",
            )
    mock_pr_comment.assert_not_called()


def test_cleanup_audit_pr_empty_issue_comment_raises_before_pr_mutation() -> None:
    """cleanup_audit_pr rejects an empty issue comment before mutating the PR."""
    with patch("scripts.audit_pr_cleanup.post_pr_comment") as mock_pr_comment:
        with pytest.raises(ValueError, match="issue_comment text cannot be empty or whitespace"):
            cleanup_audit_pr(
                pr_number=123,
                comment="PR comment body",
                related_issue=456,
                issue_comment="   ",
            )
    mock_pr_comment.assert_not_called()


def test_cleanup_audit_pr_blank_issue_comment_raises_before_pr_mutation() -> None:
    """cleanup_audit_pr rejects a blank string issue comment before mutating the PR."""
    with patch("scripts.audit_pr_cleanup.post_pr_comment") as mock_pr_comment:
        with pytest.raises(ValueError, match="issue_comment text cannot be empty or whitespace"):
            cleanup_audit_pr(
                pr_number=123,
                comment="PR comment body",
                related_issue=456,
                issue_comment="",
            )
    mock_pr_comment.assert_not_called()


def test_cleanup_audit_pr_failure_handling() -> None:
    """cleanup_audit_pr re-raises when a sub-operation fails."""
    with (
        patch("scripts.audit_pr_cleanup.post_pr_comment", side_effect=AuditCleanupError("Network timeout")),
        patch("scripts.audit_pr_cleanup.close_pr"),
    ):
        with pytest.raises(AuditCleanupError, match="Network timeout"):
            cleanup_audit_pr(pr_number=333, comment="PR comment")


def test_cleanup_audit_pr_sets_success_false_when_pr_not_closed() -> None:
    """cleanup_audit_pr sets success=False when PR remains open after close attempt."""
    with (
        patch("scripts.audit_pr_cleanup.post_pr_comment", return_value=True),
        patch("scripts.audit_pr_cleanup.close_pr"),
        patch("scripts.audit_pr_cleanup.is_pr_closed", return_value=False),
    ):
        result = cleanup_audit_pr(pr_number=123, comment="PR comment")

    assert result.success is False
    assert result.pr_closed is False
    assert result.error_message is not None
    assert "still open" in result.error_message


def test_cleanup_audit_pr_sets_success_false_when_branch_not_deleted() -> None:
    """cleanup_audit_pr sets success=False when branch still exists after delete attempt."""
    with (
        patch("scripts.audit_pr_cleanup.post_pr_comment", return_value=True),
        patch("scripts.audit_pr_cleanup.get_pr_head_branch", return_value="feature/abc"),
        patch("scripts.audit_pr_cleanup.close_pr"),
        patch("scripts.audit_pr_cleanup.is_pr_closed", return_value=True),
        patch("scripts.audit_pr_cleanup.delete_remote_branch"),
        patch("scripts.audit_pr_cleanup.branch_exists", return_value=True),
    ):
        result = cleanup_audit_pr(pr_number=123, comment="PR comment", delete_branch=True)

    assert result.success is False
    assert result.branch_deleted is False
    assert result.error_message is not None
    assert "still exists" in result.error_message


def test_cleanup_audit_pr_sets_success_false_when_issue_not_closed() -> None:
    """cleanup_audit_pr sets success=False when issue remains open after close attempt."""
    with (
        patch("scripts.audit_pr_cleanup.post_pr_comment", return_value=True),
        patch("scripts.audit_pr_cleanup.close_pr"),
        patch("scripts.audit_pr_cleanup.is_pr_closed", return_value=True),
        patch("scripts.audit_pr_cleanup.post_issue_comment", return_value=True),
        patch("scripts.audit_pr_cleanup.close_issue"),
        patch("scripts.audit_pr_cleanup.is_issue_closed", return_value=False),
    ):
        result = cleanup_audit_pr(pr_number=123, comment="PR comment", related_issue=456)

    assert result.success is False
    assert result.issue_closed is False
    assert result.error_message is not None
    assert "still open" in result.error_message


def test_cleanup_audit_pr_skips_branch_and_issue_steps_when_pr_close_fails() -> None:
    """cleanup_audit_pr returns immediately without deleting branch or closing issue when PR close fails."""
    with (
        patch("scripts.audit_pr_cleanup.post_pr_comment"),
        patch("scripts.audit_pr_cleanup.get_pr_head_branch", return_value="feature/abc"),
        patch("scripts.audit_pr_cleanup.close_pr"),
        patch("scripts.audit_pr_cleanup.is_pr_closed", return_value=False),
        patch("scripts.audit_pr_cleanup.delete_remote_branch") as mock_del_branch,
        patch("scripts.audit_pr_cleanup.post_issue_comment") as mock_issue_comment,
        patch("scripts.audit_pr_cleanup.close_issue") as mock_close_issue,
    ):
        result = cleanup_audit_pr(pr_number=123, comment="PR comment", delete_branch=True, related_issue=456)

    assert result.success is False
    assert result.pr_closed is False
    mock_del_branch.assert_not_called()
    mock_issue_comment.assert_not_called()
    mock_close_issue.assert_not_called()


def test_cleanup_audit_pr_skips_issue_step_when_branch_deletion_fails() -> None:
    """cleanup_audit_pr returns immediately without closing issue when branch deletion fails."""
    with (
        patch("scripts.audit_pr_cleanup.post_pr_comment"),
        patch("scripts.audit_pr_cleanup.get_pr_head_branch", return_value="feature/abc"),
        patch("scripts.audit_pr_cleanup.close_pr"),
        patch("scripts.audit_pr_cleanup.is_pr_closed", return_value=True),
        patch("scripts.audit_pr_cleanup.delete_remote_branch"),
        patch("scripts.audit_pr_cleanup.branch_exists", return_value=True),
        patch("scripts.audit_pr_cleanup.post_issue_comment") as mock_issue_comment,
        patch("scripts.audit_pr_cleanup.close_issue") as mock_close_issue,
    ):
        result = cleanup_audit_pr(pr_number=123, comment="PR comment", delete_branch=True, related_issue=456)

    assert result.success is False
    assert result.branch_deleted is False
    mock_issue_comment.assert_not_called()
    mock_close_issue.assert_not_called()


def test_cleanup_audit_pr_fails_before_mutation_when_head_branch_unresolvable() -> None:
    """cleanup_audit_pr returns success=False immediately when branch resolution fails."""
    with (
        patch("scripts.audit_pr_cleanup.get_pr_head_branch", return_value=None),
        patch("scripts.audit_pr_cleanup.post_pr_comment") as mock_pr_comment,
    ):
        result = cleanup_audit_pr(pr_number=123, comment="PR comment", delete_branch=True)

    assert result.success is False
    assert result.error_message is not None
    assert "could not be resolved" in result.error_message
    mock_pr_comment.assert_not_called()
