"""Unit tests for AuditCleanupError class in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

import pytest

from scripts.audit_pr_cleanup import AuditCleanupError


def test_audit_cleanup_error_is_exception() -> None:
    """AuditCleanupError should be a subclass of Exception and store message."""
    error = AuditCleanupError("Failed to close PR")
    assert isinstance(error, Exception)
    assert str(error) == "Failed to close PR"


def test_audit_cleanup_error_can_be_raised_and_caught() -> None:
    """AuditCleanupError can be raised and caught as expected."""
    with pytest.raises(AuditCleanupError, match="Network timeout"):
        raise AuditCleanupError("Network timeout")
