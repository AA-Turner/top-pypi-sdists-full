"""Tests for producer and replay deadline selection."""

from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import dispatcher_wakeup as subject
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


@pytest.fixture(autouse=True)
def isolated_deadlines(monkeypatch):
    monkeypatch.setattr(subject, "active_cooldown", Mock(return_value=None))
    monkeypatch.setattr(subject, "_get_read_token_pool", Mock(return_value=None))
    monkeypatch.setattr(subject.time, "time", lambda: 1000)


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        (ProviderRateLimitError(72000), 73000),
        (ProviderRateLimitError(172800), 173800),
        (ProviderRateLimitError(reset_timestamp=173800), 173800),
        (RetryableError("limited", retry_after=7200, is_rate_limit=True), 8200),
        (ProviderRateLimitError(reset_timestamp=8200, remaining=0), 8200),
        (ProviderRateLimitError(reset_timestamp=8200), 8200),
        (ProviderRateLimitError(60, reset_timestamp=8200), 8200),
        (ProviderRateLimitError(60, reset_timestamp=8200, remaining=0), 8200),
        (RetryableError("limited", reset_timestamp=8200, is_rate_limit=True), 8200),
        (RetryableError("limited", reset_timestamp=8200, remaining=0, is_rate_limit=True), 8200),
        (ProviderRateLimitError(reset_timestamp=8200, remaining=42), 1060),
        (ProviderRateLimitError(), 1060),
    ],
)
def test_preserves_typed_timing_without_the_in_job_retry_budget(error, expected):
    assert subject.wake_resume_at(Mock(), error, now=1000) == expected


def test_uses_current_time_when_not_provided():
    assert subject.wake_resume_at(Mock(), ProviderRateLimitError(60)) == 1060


def test_reset_only_metadata_without_remaining_honors_absolute_deadline():
    error = ProviderRateLimitError(reset_timestamp=900)
    assert subject.wake_resume_at(Mock(), error, now=100) == 900


@pytest.mark.parametrize(("remaining", "expected"), [(None, 900), (0, 900), (42, 600)])
def test_secondary_retry_after_ignores_reset_only_when_quota_explicitly_remains(remaining, expected):
    error = ProviderRateLimitError(500, reset_timestamp=900, remaining=remaining)
    assert subject.wake_resume_at(Mock(), error, now=100) == expected


@pytest.mark.parametrize(
    ("metadata_delay", "local_deadline", "persisted_deadline", "expected"),
    [(7200, 10000, 9000, 10000), (7200, 4000, 10000, 10000), (None, None, 10000, 10000)],
)
def test_uses_longest_provider_pool_or_independent_default_deadline(
    monkeypatch, metadata_delay, local_deadline, persisted_deadline, expected
):
    provider = Mock()
    pool = Mock()
    pool.active_cooldown_for.return_value = (
        None if local_deadline is None else ("github:TEAM_PAT", Mock(resume_at=local_deadline))
    )
    monkeypatch.setattr(subject, "_get_read_token_pool", Mock(return_value=pool))
    subject.active_cooldown.return_value = (
        None
        if persisted_deadline is None
        else ("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", Mock(resume_at=persisted_deadline))
    )
    error = ProviderRateLimitError(metadata_delay, credential_identity="TEAM_PAT")
    assert subject.wake_resume_at(provider, error, now=1000) == expected
    identities = ("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "TEAM_PAT")
    pool.active_cooldown_for.assert_called_once_with(identities, now=1000)
    subject.active_cooldown.assert_called_once_with(
        provider, credential_identity=identities, now=1000, use_writer_token=True
    )


def test_rejects_non_rate_limit_failure():
    with pytest.raises(ValueError, match="rate limit"):
        subject.wake_resume_at(Mock(), RetryableError("server error"), now=1000)


@pytest.mark.parametrize("field", ["retry_after_seconds", "reset_timestamp"])
@pytest.mark.parametrize("value", [True, "120", -1, float("inf"), float("nan"), 10**1000])
def test_rejects_invalid_supplied_timing(field, value):
    error = ProviderRateLimitError()
    setattr(error, field, value)
    with pytest.raises(ValueError, match="timing"):
        subject.wake_resume_at(Mock(), error, now=1000)
