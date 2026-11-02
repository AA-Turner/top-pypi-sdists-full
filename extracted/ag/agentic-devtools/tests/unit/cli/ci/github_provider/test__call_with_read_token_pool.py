"""Tests for pooled GitHub read failover."""

from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.github_provider import _call_with_read_token_pool
from agentic_devtools.cli.ci.read_token_pool import ReadCredential
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError


def test_default_fallback_rate_limit_is_persisted_and_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = Mock()
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    pool.default_is_active = False
    pool.select.return_value = None
    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._get_read_token_pool", lambda: pool)

    def operation(token: str | None, identity: str) -> tuple[str, int | None]:
        assert token == "default-token"
        assert identity == pool.default_identity
        raise RetryableError(
            "GitHub API rate limited",
            provider="github",
            credential_identity=identity,
            source="rest",
            is_rate_limit=True,
        )

    with pytest.raises(ProviderRateLimitError) as raised:
        _call_with_read_token_pool("rest", operation)

    assert raised.value.credential_identity == pool.default_identity
    pool.mark_rate_limited.assert_called_once()


def test_non_rate_retryable_error_from_default_fallback_is_preserved(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = Mock()
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    pool.default_is_active = False
    pool.select.return_value = None
    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._get_read_token_pool", lambda: pool)
    expected = RetryableError("temporary network failure", is_rate_limit=False)

    def operation(_token: str | None, _identity: str) -> tuple[str, int | None]:
        raise expected

    with pytest.raises(RetryableError) as raised:
        _call_with_read_token_pool("rest", operation)

    assert raised.value is expected
    pool.mark_rate_limited.assert_not_called()


def test_runs_operation_directly_when_pool_is_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._get_read_token_pool", lambda: None)

    result = _call_with_read_token_pool("rest", lambda token, _identity: (token or "fallback", None))

    assert result == "fallback"


def test_non_rate_retryable_error_from_alternate_is_preserved(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = Mock()
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    pool.select.return_value = ReadCredential("TEAM_PAT", "alternate-token", "team-user")
    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._get_read_token_pool", lambda: pool)
    expected = RetryableError("temporary network failure", is_rate_limit=False)

    def operation(_token: str | None, _identity: str) -> tuple[str, int | None]:
        raise expected

    with pytest.raises(RetryableError) as raised:
        _call_with_read_token_pool("rest", operation)

    assert raised.value is expected
    pool.mark_rate_limited.assert_not_called()


def test_reports_rate_limit_after_all_alternates_are_exhausted(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = Mock()
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    pool.default_is_active = False
    credential = ReadCredential("TEAM_PAT", "alternate-token", "team-user")
    pool.select.side_effect = [credential, None]
    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._get_read_token_pool", lambda: pool)
    attempted_identities: list[str] = []
    rate_limit_errors: list[RetryableError] = []

    def operation(_token: str | None, identity: str) -> tuple[str, int | None]:
        attempted_identities.append(identity)
        limited = RetryableError(
            "rate limited",
            provider="github",
            credential_identity=identity,
            is_rate_limit=True,
        )
        rate_limit_errors.append(limited)
        raise limited

    with pytest.raises(ProviderRateLimitError) as raised:
        _call_with_read_token_pool("rest", operation)

    assert attempted_identities == [credential.secret_name, pool.default_identity]
    assert raised.value.credential_identity == pool.default_identity
    assert pool.mark_rate_limited.call_args_list == [
        ((credential.secret_name, rate_limit_errors[0]),),
        ((pool.default_identity, rate_limit_errors[1]),),
    ]


def test_reports_alternate_rate_limit_when_default_token_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = Mock()
    pool.default_token = ""
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    credential = ReadCredential("TEAM_PAT", "alternate-token", "team-user")
    pool.select.side_effect = [credential, None]
    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._get_read_token_pool", lambda: pool)

    def operation(_token: str | None, identity: str) -> tuple[str, int | None]:
        raise RetryableError(
            "rate limited",
            provider="github",
            credential_identity=identity,
            is_rate_limit=True,
        )

    with pytest.raises(ProviderRateLimitError) as raised:
        _call_with_read_token_pool("rest", operation)

    assert raised.value.credential_identity == credential.secret_name
