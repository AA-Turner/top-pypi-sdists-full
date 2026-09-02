"""Unit tests for is_issue_closed in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError, is_issue_closed


def test_is_issue_closed_returns_true_for_closed_state() -> None:
    """is_issue_closed returns True when gh reports CLOSED state."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "issue", "view", "3881"],
        returncode=0,
        stdout='{"state":"CLOSED"}',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res) as mock_run:
        assert is_issue_closed(3881, dry_run=False, max_retries=2, retry_delay=0.1) is True
        mock_run.assert_called_once_with(
            [
                "gh",
                "issue",
                "view",
                "3881",
                "--repo",
                "swai-factory/agentic-devtools",
                "--json",
                "state",
            ],
            dry_run=False,
            max_retries=2,
            retry_delay=0.1,
        )


def test_is_issue_closed_returns_false_for_open_state() -> None:
    """is_issue_closed returns False when gh reports OPEN state."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "issue", "view", "3881"],
        returncode=0,
        stdout='{"state":"OPEN"}',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        assert is_issue_closed("#3881", dry_run=False) is False


def test_is_issue_closed_invalid_json_raises() -> None:
    """is_issue_closed wraps malformed JSON in AuditCleanupError."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "issue", "view", "3881"],
        returncode=0,
        stdout="not-json",
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        with pytest.raises(
            AuditCleanupError,
            match=r"Could not parse issue state for issue #3881: not-json",
        ):
            is_issue_closed(3881, dry_run=False)


def test_is_issue_closed_dry_run_returns_true_without_remote_call() -> None:
    """is_issue_closed returns True immediately in dry-run mode without calling run_command."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        assert is_issue_closed(3881, dry_run=True) is True
        mock_run.assert_not_called()


def test_is_issue_closed_non_dict_json_raises() -> None:
    """is_issue_closed raises AuditCleanupError when the JSON payload is not a dict."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "issue", "view", "3881"],
        returncode=0,
        stdout='["not", "a", "dict"]',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        with pytest.raises(AuditCleanupError, match=r"Unexpected issue state payload for issue #3881"):
            is_issue_closed(3881, dry_run=False)
