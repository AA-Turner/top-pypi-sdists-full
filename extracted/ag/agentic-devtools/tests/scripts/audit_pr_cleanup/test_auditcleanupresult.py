"""Unit tests for AuditCleanupResult dataclass in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from scripts.audit_pr_cleanup import AuditCleanupResult


def test_audit_cleanup_result_defaults() -> None:
    """AuditCleanupResult initializes with default flags."""
    result = AuditCleanupResult(pr_number=100)
    assert result.pr_number == 100
    assert result.pr_commented is False
    assert result.pr_closed is False
    assert result.branch_deleted is False
    assert result.issue_commented is False
    assert result.issue_closed is False
    assert result.success is True
    assert result.error_message is None


def test_audit_cleanup_result_custom_values() -> None:
    """AuditCleanupResult preserves modified attributes."""
    result = AuditCleanupResult(
        pr_number=200,
        pr_commented=True,
        pr_closed=True,
        branch_deleted=True,
        issue_commented=True,
        issue_closed=True,
        success=False,
        error_message="Simulated error",
    )
    assert result.pr_number == 200
    assert result.pr_commented is True
    assert result.pr_closed is True
    assert result.branch_deleted is True
    assert result.issue_commented is True
    assert result.issue_closed is True
    assert result.success is False
    assert result.error_message == "Simulated error"
