"""Unit tests for close_issue in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError, close_issue


def test_close_issue_with_integer() -> None:
    """close_issue invokes gh issue close with integer."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        close_issue(
            issue_number=3881,
            dry_run=False,
            max_retries=3,
            retry_delay=0.5,
        )
        mock_run.assert_called_once_with(
            ["gh", "issue", "close", "3881", "--repo", "swai-factory/agentic-devtools"],
            dry_run=False,
            max_retries=3,
            retry_delay=0.5,
        )


def test_close_issue_with_string_hash() -> None:
    """close_issue parses '#500' and executes close."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        close_issue(
            issue_number="#500",
            dry_run=True,
        )
        mock_run.assert_called_once_with(
            ["gh", "issue", "close", "500", "--repo", "swai-factory/agentic-devtools"],
            dry_run=True,
            max_retries=3,
            retry_delay=0.0,
        )


def test_close_issue_ignores_already_closed_error() -> None:
    """close_issue treats an already-closed response as success."""
    with patch(
        "scripts.audit_pr_cleanup.run_command",
        side_effect=AuditCleanupError("Command failed: issue already closed"),
    ):
        close_issue(issue_number=3881)


def test_close_issue_reraises_unexpected_errors() -> None:
    """close_issue preserves errors unrelated to an already-closed issue."""
    error = AuditCleanupError("Command failed: permission denied")
    with patch("scripts.audit_pr_cleanup.run_command", side_effect=error):
        with pytest.raises(AuditCleanupError, match="permission denied"):
            close_issue(issue_number=3881)
