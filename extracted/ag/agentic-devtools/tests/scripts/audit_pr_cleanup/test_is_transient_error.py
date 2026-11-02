"""Unit tests for is_transient_error in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

import pytest

from scripts.audit_pr_cleanup import is_transient_error


@pytest.mark.parametrize(
    "msg",
    [
        "HTTP 429 Too Many Requests",
        "error 502 Bad Gateway occurred",
        "503 Service Unavailable",
        "Gateway Timeout (504)",
        "Connection reset by peer",
        "ECONNRESET socket disconnected",
        "ETIMEDOUT connection failed",
        "socket hang up during request",
        "Temporary failure in name resolution",
        "Internal server error occurred",
        "Network timed out after 30s",
    ],
)
def test_is_transient_error_detects_transient_messages(msg: str) -> None:
    """is_transient_error should return True for known transient network/server error patterns."""
    assert is_transient_error(msg) is True


@pytest.mark.parametrize(
    "msg",
    [
        "Resource not found 404",
        "Invalid authentication token 401",
        "Validation error: comment cannot be empty",
        "Branch already deleted",
        "Syntax error in graphql query",
        "PR #503 not found",
    ],
)
def test_is_transient_error_returns_false_for_non_transient(msg: str) -> None:
    """is_transient_error should return False for deterministic/permanent error messages."""
    assert is_transient_error(msg) is False
