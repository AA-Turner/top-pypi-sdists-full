"""Tests for lossless typed rate-limit diagnostics."""

import pytest

from agentic_devtools.cli.ci.dispatcher_policy import _rate_limit_error


@pytest.mark.parametrize(
    "headers",
    [
        {"retry-after": "not-a-date"},
        {"retry-after": "9" * 400},
        {"retry-after": "-1"},
        {"x-ratelimit-reset": "invalid"},
        {"x-ratelimit-reset": "-1"},
    ],
)
def test_invalid_provider_timing_fails_explicitly(headers):
    with pytest.raises(ValueError, match="timing"):
        _rate_limit_error(headers, 60)


@pytest.mark.parametrize("retry_after", ["172800", "Wed, 14 Oct 2026 23:13:20 GMT"])
def test_preserves_numeric_and_http_date_delays(monkeypatch, retry_after):
    monkeypatch.setenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", "TEAM_PAT")
    error = _rate_limit_error({"retry-after": retry_after}, 172800)
    assert error.retry_after_seconds == 172800
    assert error.credential_identity == "TEAM_PAT"


def test_keeps_primary_reset_and_remaining_metadata(monkeypatch):
    monkeypatch.delenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", raising=False)
    error = _rate_limit_error({"x-ratelimit-reset": "173800", "x-ratelimit-remaining": "0"}, 172801)
    assert error.reset_timestamp == 173800
    assert error.remaining == 0
    assert error.credential_identity == "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
