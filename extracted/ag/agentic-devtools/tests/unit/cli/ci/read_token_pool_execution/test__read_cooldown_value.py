"""Tests for deadline-aware cooldown lookup."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.read_token_pool_execution import ReadTokenPoolOperations, _read_cooldown_value
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError, retry_with_backoff


def test_bypasses_decorated_getter_retries_only_with_deadline() -> None:
    class DecoratedProvider:
        @retry_with_backoff(max_retries=0)
        def get_variable(self, _name: str, *, use_writer_token: bool = False) -> str:
            assert use_writer_token is False
            return "cooldowns"

    class PlainProvider:
        def get_variable(self, _name: str, *, use_writer_token: bool = False) -> str:
            assert use_writer_token is False
            return "plain"

    decorated = DecoratedProvider()
    plain = PlainProvider()
    assert _read_cooldown_value(decorated, use_writer_token=False) == "cooldowns"
    with ReadTokenPoolOperations.request_context(10.0, lambda: 0.0):
        assert _read_cooldown_value(decorated, use_writer_token=False) == "cooldowns"
        assert _read_cooldown_value(plain, use_writer_token=False) == "plain"


def test_maps_deadline_scoped_rate_limit_and_preserves_deadline_free_error() -> None:
    class Provider:
        error: Exception

        def get_variable(self, _name: str, *, use_writer_token: bool = False) -> str:
            assert use_writer_token is False
            raise self.error

    provider = Provider()
    limited = RetryableError("rate limited", retry_after=45, is_rate_limit=True)
    provider.error = limited

    with ReadTokenPoolOperations.request_context(10.0, lambda: 0.0):
        with pytest.raises(ProviderRateLimitError) as raised:
            _read_cooldown_value(provider, use_writer_token=False)
    assert raised.value.retry_after_seconds == 45

    with pytest.raises(RetryableError) as raised_without_deadline:
        _read_cooldown_value(provider, use_writer_token=False)
    assert raised_without_deadline.value is limited


@pytest.mark.parametrize("deadline", [None, 10.0])
def test_preserves_non_rate_limit_and_generic_lookup_errors(deadline: float | None) -> None:
    class Provider:
        error: Exception

        def get_variable(self, _name: str, *, use_writer_token: bool = False) -> str:
            assert use_writer_token is False
            raise self.error

    provider = Provider()
    retryable = RetryableError("temporary failure", is_rate_limit=False)
    provider.error = retryable
    with ReadTokenPoolOperations.request_context(deadline, lambda: 0.0):
        with pytest.raises(RetryableError) as raised:
            _read_cooldown_value(provider, use_writer_token=False)
    assert raised.value is retryable

    provider.error = RuntimeError("offline")
    with ReadTokenPoolOperations.request_context(deadline, lambda: 0.0):
        with pytest.raises(RuntimeError, match="offline"):
            _read_cooldown_value(provider, use_writer_token=False)


def test_expired_deadline_propagates_from_lookup_error() -> None:
    class Provider:
        def get_variable(self, _name: str, *, use_writer_token: bool = False) -> str:
            assert use_writer_token is False
            raise RuntimeError("offline")

    with ReadTokenPoolOperations.request_context(10.0, lambda: 10.0):
        with pytest.raises(ReadTokenPoolOperations.DeadlineExpired):
            _read_cooldown_value(Provider(), use_writer_token=False)
