"""Tests for retained and deferred read-token pool rate-limit persistence."""

import json
from collections import deque
from contextvars import ContextVar
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci.cooldown import CooldownRecord, parse_cooldowns, serialize_cooldowns
from agentic_devtools.cli.ci.read_token_pool_execution import ReadTokenPoolOperations, ReadTokenPoolRateLimits
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError


def test_retained_cooldowns_prune_expiry_and_preserve_longer_repository_records(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    retained = {
        ("owner/repo", "expired"): 100.0,
        ("owner/repo", "active"): 140.0,
        ("owner/other", "isolated"): 150.0,
    }
    monkeypatch.setattr("agentic_devtools.cli.ci.read_token_pool_execution._RETAINED_RATE_LIMITS", retained)
    with patch("agentic_devtools.cli.ci.read_token_pool_execution.time.time", return_value=100.0):
        active = ReadTokenPoolRateLimits.merge_cooldowns("owner/repo", {"active": 160.0})
    assert active == {"active": 160.0}
    assert retained == {
        ("owner/repo", "active"): 140.0,
        ("owner/other", "isolated"): 150.0,
    }


def test_unknown_cooldown_is_preserved_and_only_finite_deadlines_are_retained(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    retained = {("owner/repo", "DEFAULT"): 140.0}
    monkeypatch.setattr("agentic_devtools.cli.ci.read_token_pool_execution._RETAINED_RATE_LIMITS", retained)
    monkeypatch.setattr("agentic_devtools.cli.ci.read_token_pool_execution.time.time", lambda: 100.0)
    monkeypatch.setattr("agentic_devtools.cli.ci.read_token_pool_execution._DEFERRED_RATE_LIMIT_PERSISTENCE", deque())
    assert ReadTokenPoolRateLimits.merge_cooldowns("owner/repo", {"DEFAULT": None}) == {"DEFAULT": None}
    nonfinite = float("nan")
    assert ReadTokenPoolRateLimits.merge_cooldowns("owner/repo", {"DEFAULT": nonfinite})["DEFAULT"] is nonfinite
    assert ReadTokenPoolRateLimits.merge_cooldowns("owner/repo", {}) == {"DEFAULT": 140.0}

    provider = Mock()
    bypass = ContextVar("test_unknown_cooldown_bypass", default=False)
    error = RetryableError("rate limited", retry_after=30, is_rate_limit=True)
    with patch(
        "agentic_devtools.cli.ci.read_token_pool_execution.calculate_rate_limit_delay",
        return_value=Mock(resume_at=None),
    ):
        with ReadTokenPoolOperations.request_context(10.0, lambda: 0.0):
            assert ReadTokenPoolRateLimits.persist_rate_limit(provider, "DEFAULT", error, bypass=bypass) is None
    assert retained == {("owner/repo", "DEFAULT"): 140.0}

    with patch("agentic_devtools.cli.ci.cooldown.persist_cooldown", return_value=None):
        assert ReadTokenPoolRateLimits.persist_rate_limit(provider, "DEFAULT", error, bypass=bypass) is None
    assert retained == {("owner/repo", "DEFAULT"): 140.0}


def test_provider_rate_limit_persistence_waits_for_an_unbounded_request() -> None:
    bypass = ContextVar("test_read_pool_bypass", default=False)
    provider = Mock()
    error = ProviderRateLimitError(
        retry_after_seconds=30,
        provider="github",
        credential_identity="DEFAULT",
        source="retry-after",
        is_rate_limit=True,
    )

    with ReadTokenPoolOperations.request_context(10.0, lambda: 0.0):
        resume_at = ReadTokenPoolRateLimits.persist_rate_limit(
            provider,
            "DEFAULT",
            error,
            bypass=bypass,
        )
        assert isinstance(resume_at, float)
        ReadTokenPoolRateLimits.flush_deferred_rate_limits()

    with patch("agentic_devtools.cli.ci.cooldown.persist_cooldown", return_value=None) as persist:
        ReadTokenPoolRateLimits.flush_deferred_rate_limits()
        ReadTokenPoolRateLimits.flush_deferred_rate_limits()

    persist.assert_called_once()
    assert persist.call_args.args[1].retry_after_seconds == 30
    assert not bypass.get()


def test_deferred_cooldown_persistence_keeps_observation_time() -> None:
    now = [100.0]
    other_cooldown = CooldownRecord(86600, source="fallback", updated_at=100)
    stored = [
        serialize_cooldowns(
            {
                "github:OTHER_TOKEN": other_cooldown,
            }
        )
    ]
    provider = Mock()
    provider.get_variable.side_effect = lambda *_args, **_kwargs: stored[0]
    provider.set_variable.side_effect = lambda _name, value: stored.__setitem__(0, value)
    bypass = ContextVar("test_observed_cooldown_bypass", default=False)
    error = RetryableError(
        "rate limited",
        retry_after=30,
        provider="github",
        credential_identity="DEFAULT",
        source="retry-after",
        is_rate_limit=True,
    )

    with patch("agentic_devtools.cli.ci.read_token_pool_execution.time.time", side_effect=lambda: now[0]):
        with ReadTokenPoolOperations.request_context(10.0, lambda: 0.0):
            resume_at = ReadTokenPoolRateLimits.persist_rate_limit(provider, "DEFAULT", error, bypass=bypass)
        assert resume_at == 140.0

        now[0] = 200.0
        ReadTokenPoolRateLimits.flush_deferred_rate_limits()

    record = json.loads(stored[0])["provider_cooldowns"]["github:DEFAULT"]
    assert record["resume_at"] == 140.0
    assert parse_cooldowns(stored[0], now=200.0) == {"github:OTHER_TOKEN": other_cooldown}
    provider.set_variable.assert_called_once()


def test_deferred_persistence_remains_queued_after_failure() -> None:
    bypass = ContextVar("test_read_pool_bypass", default=False)
    error = RetryableError("rate limited", retry_after=15, is_rate_limit=True)
    with ReadTokenPoolOperations.request_context(10.0, lambda: 0.0):
        ReadTokenPoolRateLimits.persist_rate_limit(
            Mock(),
            "TEAM",
            error,
            bypass=bypass,
        )

    with (
        patch("agentic_devtools.cli.ci.cooldown.persist_cooldown", side_effect=RuntimeError("offline")) as persist,
        pytest.raises(RuntimeError, match="offline"),
    ):
        ReadTokenPoolRateLimits.flush_deferred_rate_limits()

    with patch("agentic_devtools.cli.ci.cooldown.persist_cooldown", return_value=None):
        ReadTokenPoolRateLimits.flush_deferred_rate_limits()

    assert persist.call_count == 1
    assert not bypass.get()
