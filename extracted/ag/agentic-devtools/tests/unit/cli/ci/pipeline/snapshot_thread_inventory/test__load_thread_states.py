"""Tests for loading provider review-thread state."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.pipeline.snapshot_thread_inventory import _load_thread_states
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def test_returns_none_when_provider_does_not_expose_thread_lookup() -> None:
    provider = MagicMock()
    provider.list_review_threads_by_thread_id = None

    assert _load_thread_states(provider, 1) is None


def test_returns_none_when_thread_lookup_is_not_implemented() -> None:
    provider = MagicMock()
    provider.list_review_threads_by_thread_id.side_effect = NotImplementedError

    assert _load_thread_states(provider, 1) is None


def test_returns_none_when_thread_lookup_fails() -> None:
    provider = MagicMock()
    provider.list_review_threads_by_thread_id.side_effect = RuntimeError("unavailable")

    assert _load_thread_states(provider, 1) is None


def test_reraises_rate_limit_from_thread_lookup() -> None:
    provider = MagicMock()
    provider.list_review_threads_by_thread_id.side_effect = ProviderRateLimitError(
        retry_after_seconds=1,
        provider="test",
    )

    with pytest.raises(ProviderRateLimitError):
        _load_thread_states(provider, 1)


def test_returns_none_when_provider_state_is_not_a_mapping() -> None:
    provider = MagicMock()
    provider.list_review_threads_by_thread_id.return_value = []

    assert _load_thread_states(provider, 1) is None


def test_returns_provider_thread_state_mapping() -> None:
    provider = MagicMock()
    provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}

    assert _load_thread_states(provider, 1) == {"thread-1": (False, (101,))}
