"""Tests for the public cooldown persistence entry point."""

from unittest.mock import Mock, patch

from agentic_devtools.cli.ci.cooldown import CooldownRecord, persist_cooldown
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


def test_persist_cooldown_forwards_options_to_persistence_implementation() -> None:
    provider = Mock()
    error = ProviderRateLimitError(provider="github")
    result = ("github:DEFAULT", CooldownRecord(140))

    with patch(
        "agentic_devtools.cli.ci.cooldown_persistence.persist_cooldown",
        return_value=result,
    ) as persist:
        assert persist_cooldown(provider, error, now=200, retries=2, observed_at=100) == result

    persist.assert_called_once_with(provider, error, now=200, retries=2, observed_at=100)
