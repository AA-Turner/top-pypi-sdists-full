"""Unit tests for branch_exists in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError, branch_exists


def test_branch_exists_returns_true_when_ref_resolves() -> None:
    """branch_exists returns True when gh API can read the branch ref."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        assert branch_exists("feature/cleanup", dry_run=False, max_retries=2, retry_delay=0.1) is True
        mock_run.assert_called_once_with(
            [
                "gh",
                "api",
                "repos/swai-factory/agentic-devtools/git/ref/heads/feature%2Fcleanup",
            ],
            dry_run=False,
            max_retries=2,
            retry_delay=0.1,
        )


@pytest.mark.parametrize("error_text", ["reference does not exist", "no ref found for"])
def test_branch_exists_returns_false_for_explicit_missing_ref(error_text: str) -> None:
    """branch_exists returns False for missing-ref responses."""
    with patch(
        "scripts.audit_pr_cleanup.run_command",
        side_effect=AuditCleanupError(f"Command failed: {error_text}"),
    ):
        assert branch_exists("feature/missing", dry_run=False) is False


def test_branch_exists_verifies_repo_access_for_generic_not_found() -> None:
    """branch_exists confirms repo access before treating generic 404 text as missing ref."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        mock_run.side_effect = [
            AuditCleanupError("Command failed: not found"),
            None,
        ]
        assert branch_exists("feature/missing", dry_run=False) is False
        assert mock_run.call_count == 2
        assert mock_run.call_args_list[1].args[0] == ["gh", "api", "repos/swai-factory/agentic-devtools"]


def test_branch_exists_reraises_when_repo_check_fails_for_generic_not_found() -> None:
    """branch_exists fails closed when generic not-found text cannot be disambiguated."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        mock_run.side_effect = [
            AuditCleanupError("Command failed: not found"),
            AuditCleanupError("Command failed: Resource not accessible by integration"),
        ]
        with pytest.raises(AuditCleanupError, match="Resource not accessible"):
            branch_exists("feature/missing", dry_run=False)


def test_branch_exists_does_not_swallow_404_in_branch_name() -> None:
    """branch_exists re-raises when '404' appears only in the branch name, not in the response."""
    error = AuditCleanupError("Command failed (1): gh api repos/.../git/ref/heads/feature%2F404-fix\npermission denied")
    with patch("scripts.audit_pr_cleanup.run_command", side_effect=error):
        with pytest.raises(AuditCleanupError, match="permission denied"):
            branch_exists("feature/404-fix", dry_run=False)


def test_branch_exists_reraises_unexpected_error() -> None:
    """branch_exists re-raises non-missing-ref errors."""
    with patch(
        "scripts.audit_pr_cleanup.run_command",
        side_effect=AuditCleanupError("Command failed: permission denied"),
    ):
        with pytest.raises(AuditCleanupError, match="permission denied"):
            branch_exists("feature/cleanup", dry_run=False)


def test_branch_exists_dry_run_returns_false_without_remote_call() -> None:
    """branch_exists returns False immediately in dry-run mode without calling run_command."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        assert branch_exists("feature/cleanup", dry_run=True) is False
        mock_run.assert_not_called()


def test_branch_exists_raises_for_empty_branch_name() -> None:
    """branch_exists raises ValueError when the branch name is empty or blank."""
    with pytest.raises(ValueError, match="Branch name cannot be empty"):
        branch_exists("", dry_run=False)
