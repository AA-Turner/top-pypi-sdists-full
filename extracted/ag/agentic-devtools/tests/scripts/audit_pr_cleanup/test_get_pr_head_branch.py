"""Unit tests for get_pr_head_branch in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError, get_pr_head_branch


def test_get_pr_head_branch_dry_run() -> None:
    """get_pr_head_branch returns synthetic branch in dry_run mode."""
    branch = get_pr_head_branch(123, dry_run=True)
    assert branch == "synthetic-branch-dry-run"


def test_get_pr_head_branch_real_call() -> None:
    """get_pr_head_branch returns branch name from gh pr view output."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout='{"headRefName": "feature/audit-branch-123", "isCrossRepository": false}',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res) as mock_run:
        branch = get_pr_head_branch(123, dry_run=False, max_retries=4, retry_delay=0.25)
        assert branch == "feature/audit-branch-123"
        mock_run.assert_called_once_with(
            [
                "gh",
                "pr",
                "view",
                "123",
                "--repo",
                "swai-factory/agentic-devtools",
                "--json",
                "headRefName,isCrossRepository",
            ],
            dry_run=False,
            max_retries=4,
            retry_delay=0.25,
        )


def test_get_pr_head_branch_empty_output_returns_none() -> None:
    """get_pr_head_branch returns None if output is whitespace."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout='{"headRefName": "   ", "isCrossRepository": false}',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        branch = get_pr_head_branch(123, dry_run=False)
        assert branch is None


def test_get_pr_head_branch_rejects_cross_repository_pr() -> None:
    """get_pr_head_branch rejects deleting a fork PR's head branch via origin."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout='{"headRefName": "feature/audit-branch-123", "isCrossRepository": true}',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        with pytest.raises(
            AuditCleanupError,
            match="Refusing to delete the head branch for cross-repository PR #123",
        ):
            get_pr_head_branch(123, dry_run=False)


def test_get_pr_head_branch_invalid_json_raises_audit_cleanup_error() -> None:
    """get_pr_head_branch wraps malformed gh JSON output in AuditCleanupError."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout="not-json",
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        with pytest.raises(
            AuditCleanupError,
            match=r"Could not parse PR metadata for PR #123: not-json",
        ):
            get_pr_head_branch(123, dry_run=False)


def test_get_pr_head_branch_rejects_missing_is_cross_repository() -> None:
    """get_pr_head_branch refuses deletion when isCrossRepository is absent (fail-safe)."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout='{"headRefName": "feature/audit-branch-123"}',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        with pytest.raises(
            AuditCleanupError,
            match="Refusing to delete the head branch for cross-repository PR #123",
        ):
            get_pr_head_branch(123, dry_run=False)


def test_get_pr_head_branch_rejects_null_is_cross_repository() -> None:
    """get_pr_head_branch refuses deletion when isCrossRepository is null (fail-safe)."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout='{"headRefName": "feature/audit-branch-123", "isCrossRepository": null}',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        with pytest.raises(
            AuditCleanupError,
            match="Refusing to delete the head branch for cross-repository PR #123",
        ):
            get_pr_head_branch(123, dry_run=False)


def test_get_pr_head_branch_rejects_non_object_json() -> None:
    """get_pr_head_branch raises AuditCleanupError when gh returns valid JSON that is not an object."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout="[]",
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        with pytest.raises(
            AuditCleanupError,
            match=r"Unexpected PR metadata payload for PR #123",
        ):
            get_pr_head_branch(123, dry_run=False)


def test_get_pr_head_branch_returns_none_for_non_string_head_ref_name() -> None:
    """get_pr_head_branch returns None when headRefName is not a string."""
    mock_res = subprocess.CompletedProcess(
        args=["gh", "pr", "view", "123"],
        returncode=0,
        stdout='{"headRefName": 42, "isCrossRepository": false}',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=mock_res):
        branch = get_pr_head_branch(123, dry_run=False)
        assert branch is None
