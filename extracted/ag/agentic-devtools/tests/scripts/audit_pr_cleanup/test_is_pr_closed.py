"""Unit tests for is_pr_closed in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError, is_pr_closed


def test_is_pr_closed_returns_true_for_closed_state() -> None:
    """is_pr_closed returns True when gh reports CLOSED state."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout='{"state":"CLOSED"}',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res) as mock_run:
        assert is_pr_closed(123, dry_run=False, max_retries=2, retry_delay=0.1) is True
        mock_run.assert_called_once_with(
            [
                "gh",
                "pr",
                "view",
                "123",
                "--repo",
                "swai-factory/agentic-devtools",
                "--json",
                "state",
            ],
            dry_run=False,
            max_retries=2,
            retry_delay=0.1,
        )


def test_is_pr_closed_returns_false_for_open_state() -> None:
    """is_pr_closed returns False when gh reports OPEN state."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout='{"state":"OPEN"}',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        assert is_pr_closed(123, dry_run=False) is False


def test_is_pr_closed_invalid_json_raises() -> None:
    """is_pr_closed wraps malformed JSON in AuditCleanupError."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout="not-json",
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        with pytest.raises(AuditCleanupError, match=r"Could not parse PR state for PR #123: not-json"):
            is_pr_closed(123, dry_run=False)


def test_is_pr_closed_dry_run_returns_true_without_remote_call() -> None:
    """is_pr_closed returns True immediately in dry-run mode without calling run_command."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        assert is_pr_closed(123, dry_run=True) is True
        mock_run.assert_not_called()


def test_is_pr_closed_returns_true_for_merged_state() -> None:
    """is_pr_closed returns True when gh reports MERGED state."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout='{"state":"MERGED"}',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        assert is_pr_closed(123, dry_run=False) is True


def test_is_pr_closed_non_dict_json_raises() -> None:
    """is_pr_closed raises AuditCleanupError when the JSON payload is not a dict."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout='["not", "a", "dict"]',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        with pytest.raises(AuditCleanupError, match=r"Unexpected PR state payload for PR #123"):
            is_pr_closed(123, dry_run=False)
