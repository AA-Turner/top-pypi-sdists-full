"""Tests for provider-neutral pull-request comments."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.pull_request_comments import _sanitize_error


def test_sanitizes_token_and_environment_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SPECKIT_PR_TOKEN", "primary-secret")
    monkeypatch.setenv("GH_TOKEN", "environment-secret")
    assert _sanitize_error("primary-secret and environment-secret and explicit-secret", "explicit-secret") == (
        "[REDACTED] and [REDACTED] and [REDACTED]"
    )
    assert _sanitize_error("ordinary message") == "ordinary message"


def test_sanitizes_authorization_headers() -> None:
    assert _sanitize_error("Authorization: Basic dXNlcjpwYXQ=") == "Authorization: Basic [REDACTED]"
    assert (
        _sanitize_error("{'Authorization': 'Basic dXNlcjpwYXQ=', 'Accept': 'application/json'}")
        == "{'Authorization': 'Basic [REDACTED]', 'Accept': 'application/json'}"
    )
    assert _sanitize_error("Authorization: ******") == "Authorization: ******"
    assert _sanitize_error("Authorization: basic dXNlcjpwYXQ=") == "Authorization: basic [REDACTED]"
