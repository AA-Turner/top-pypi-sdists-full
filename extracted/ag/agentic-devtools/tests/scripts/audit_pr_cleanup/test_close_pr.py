"""Unit tests for close_pr in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError, close_pr


def test_close_pr_without_delete_branch() -> None:
    """close_pr constructs basic gh pr close command."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        close_pr(
            pr_number=123,
            delete_branch=False,
            dry_run=False,
            max_retries=2,
            retry_delay=0.1,
        )
        mock_run.assert_called_once_with(
            ["gh", "pr", "close", "123", "--repo", "swai-factory/agentic-devtools"],
            dry_run=False,
            max_retries=2,
            retry_delay=0.1,
        )


def test_close_pr_with_delete_branch() -> None:
    """close_pr appends --delete-branch flag when delete_branch is True."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        close_pr(
            pr_number=123,
            delete_branch=True,
            dry_run=False,
        )
        mock_run.assert_called_once_with(
            [
                "gh",
                "pr",
                "close",
                "123",
                "--repo",
                "swai-factory/agentic-devtools",
                "--delete-branch",
            ],
            dry_run=False,
            max_retries=3,
            retry_delay=0.0,
        )


@pytest.mark.parametrize("error_text", ["already closed", "not open"])
def test_close_pr_ignores_already_closed_errors(error_text: str) -> None:
    """close_pr treats known already-closed responses as success."""
    with patch(
        "scripts.audit_pr_cleanup.run_command",
        side_effect=AuditCleanupError(f"Command failed: {error_text}"),
    ):
        close_pr(pr_number=123)


def test_close_pr_reraises_unexpected_errors() -> None:
    """close_pr preserves errors unrelated to an already-closed PR."""
    error = AuditCleanupError("Command failed: permission denied")
    with patch("scripts.audit_pr_cleanup.run_command", side_effect=error):
        with pytest.raises(AuditCleanupError, match="permission denied"):
            close_pr(pr_number=123)
