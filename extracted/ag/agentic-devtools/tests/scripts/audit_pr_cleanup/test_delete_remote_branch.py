"""Unit tests for delete_remote_branch in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError, delete_remote_branch


def test_delete_remote_branch_success() -> None:
    """delete_remote_branch invokes repo-scoped gh API deletion."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        delete_remote_branch(
            branch_name="feature/cleanup-branch",
            remote="origin",
            dry_run=False,
            max_retries=3,
            retry_delay=0.2,
        )
        mock_run.assert_called_once_with(
            [
                "gh",
                "api",
                "--method",
                "DELETE",
                "repos/swai-factory/agentic-devtools/git/refs/heads/feature%2Fcleanup-branch",
            ],
            dry_run=False,
            max_retries=3,
            retry_delay=0.2,
        )


def test_delete_remote_branch_empty_name_raises_value_error() -> None:
    """delete_remote_branch raises ValueError if branch name is empty."""
    with pytest.raises(ValueError, match="Branch name cannot be empty"):
        delete_remote_branch(branch_name="   ")


@pytest.mark.parametrize(
    "error_text",
    ["remote ref does not exist", "couldn't find remote ref", "reference does not exist"],
)
def test_delete_remote_branch_ignores_missing_remote_errors(error_text: str) -> None:
    """delete_remote_branch treats known missing-ref responses as success."""
    with patch(
        "scripts.audit_pr_cleanup.run_command",
        side_effect=AuditCleanupError(f"Command failed: {error_text}"),
    ):
        delete_remote_branch(branch_name="feature/cleanup-branch")


def test_delete_remote_branch_reraises_generic_not_found() -> None:
    """delete_remote_branch re-raises errors containing only 'not found' without a ref-specific phrase."""
    error = AuditCleanupError("Command failed (404): gh api\nNot Found")
    with patch("scripts.audit_pr_cleanup.run_command", side_effect=error):
        with pytest.raises(AuditCleanupError, match="Not Found"):
            delete_remote_branch(branch_name="feature/cleanup-branch")


def test_delete_remote_branch_propagates_unable_to_delete_error() -> None:
    """delete_remote_branch re-raises 'unable to delete' without missing-ref context."""
    error = AuditCleanupError("Command failed: unable to delete 'feature/branch'")
    with patch("scripts.audit_pr_cleanup.run_command", side_effect=error):
        with pytest.raises(AuditCleanupError, match="unable to delete"):
            delete_remote_branch(branch_name="feature/branch")


def test_delete_remote_branch_reraises_unexpected_errors() -> None:
    """delete_remote_branch preserves errors unrelated to a missing remote ref."""
    error = AuditCleanupError("Command failed: permission denied")
    with patch("scripts.audit_pr_cleanup.run_command", side_effect=error):
        with pytest.raises(AuditCleanupError, match="permission denied"):
            delete_remote_branch(branch_name="feature/cleanup-branch")


def test_delete_remote_branch_does_not_swallow_404_in_branch_name() -> None:
    """delete_remote_branch re-raises when '404' appears only in the branch name."""
    error = AuditCleanupError(
        "Command failed (1): gh api --method DELETE repos/.../git/refs/heads/feature%2F404-fix\npermission denied"
    )
    with patch("scripts.audit_pr_cleanup.run_command", side_effect=error):
        with pytest.raises(AuditCleanupError, match="permission denied"):
            delete_remote_branch(branch_name="feature/404-fix")
