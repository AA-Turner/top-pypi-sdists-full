"""Unit tests for _comment_marker_exists in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from subprocess import CompletedProcess
from unittest.mock import patch

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError, _comment_marker_exists


def test__comment_marker_exists_returns_true_when_marker_found() -> None:
    """_comment_marker_exists returns True when any existing comment body contains the marker."""
    result = CompletedProcess(
        args=["gh", "api"],
        returncode=0,
        stdout='[{"body": "before\\n<!-- audit-pr-cleanup:pr:123:abc -->\\nafter"}]',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=result) as mock_run:
        assert _comment_marker_exists(123, "<!-- audit-pr-cleanup:pr:123:abc -->") is True
    mock_run.assert_called_once()


def test__comment_marker_exists_returns_false_when_marker_missing() -> None:
    """_comment_marker_exists ignores comments without the marker and non-string bodies."""
    result = CompletedProcess(
        args=["gh", "api"],
        returncode=0,
        stdout='[{"body": "different"}, {"body": null}]',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=result):
        assert _comment_marker_exists(123, "<!-- audit-pr-cleanup:pr:123:abc -->") is False


def test__comment_marker_exists_merges_paginated_json_arrays() -> None:
    """_comment_marker_exists scans concatenated paginated array payloads page by page."""
    result = CompletedProcess(
        args=["gh", "api"],
        returncode=0,
        stdout='[{"body": "first page"}]\n[{"body": "second page\\n<!-- audit-pr-cleanup:pr:123:abc -->"}]',
        stderr="",
    )
    with patch("scripts.audit_pr_cleanup.run_command", return_value=result):
        assert _comment_marker_exists(123, "<!-- audit-pr-cleanup:pr:123:abc -->") is True


def test__comment_marker_exists_dry_run_skips_remote_lookup() -> None:
    """_comment_marker_exists returns False in dry-run mode without calling gh."""
    with patch("scripts.audit_pr_cleanup.run_command") as mock_run:
        assert _comment_marker_exists(123, "<!-- marker -->", dry_run=True) is False
    mock_run.assert_not_called()


def test__comment_marker_exists_empty_response_raises() -> None:
    """_comment_marker_exists raises AuditCleanupError when gh api returns empty output."""
    result = CompletedProcess(args=["gh", "api"], returncode=0, stdout="", stderr="")
    with patch("scripts.audit_pr_cleanup.run_command", return_value=result):
        with pytest.raises(AuditCleanupError, match="Empty response for comments"):
            _comment_marker_exists(123, "<!-- marker -->")


def test__comment_marker_exists_invalid_json_raises() -> None:
    """_comment_marker_exists wraps invalid JSON as AuditCleanupError."""
    result = CompletedProcess(args=["gh", "api"], returncode=0, stdout="not-json", stderr="")
    with patch("scripts.audit_pr_cleanup.run_command", return_value=result):
        with pytest.raises(AuditCleanupError, match="Could not parse existing comments"):
            _comment_marker_exists(123, "<!-- marker -->")


def test__comment_marker_exists_non_list_payload_raises() -> None:
    """_comment_marker_exists rejects unexpected top-level JSON payloads."""
    result = CompletedProcess(args=["gh", "api"], returncode=0, stdout='{"body": "marker"}', stderr="")
    with patch("scripts.audit_pr_cleanup.run_command", return_value=result):
        with pytest.raises(AuditCleanupError, match="Unexpected comments payload"):
            _comment_marker_exists(123, "<!-- marker -->")


def test__comment_marker_exists_non_dict_entry_raises() -> None:
    """_comment_marker_exists rejects list payloads with non-dict entries."""
    result = CompletedProcess(args=["gh", "api"], returncode=0, stdout='["bad-entry"]', stderr="")
    with patch("scripts.audit_pr_cleanup.run_command", return_value=result):
        with pytest.raises(AuditCleanupError, match="Unexpected comment entry payload"):
            _comment_marker_exists(123, "<!-- marker -->")
