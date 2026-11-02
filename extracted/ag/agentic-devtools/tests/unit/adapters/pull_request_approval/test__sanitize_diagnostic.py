from __future__ import annotations

from agentic_devtools.adapters.pull_request_approval import _sanitize_diagnostic


def test_redacts_authorization_header_value() -> None:
    assert _sanitize_diagnostic("Authorization: Basic dXNlcjpwYXQ=") == "Authorization: Basic [REDACTED]"


def test_redacts_quoted_authorization_header_value() -> None:
    assert _sanitize_diagnostic("{'Authorization': 'Basic dXNlcjpwYXQ='}") == "{'Authorization': 'Basic [REDACTED]'}"


def test_truncates_diagnostic() -> None:
    assert _sanitize_diagnostic("x" * 1001) == "x" * 1000
