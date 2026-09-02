"""Tests for persist_cooldown()."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.cooldown import (
    CooldownRecord,
    parse_cooldowns,
    persist_cooldown,
    serialize_cooldowns,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestPersistCooldown:
    """persist_cooldown() reads with the writer token and reports the effective record."""

    def test_retries_when_a_concurrent_write_erases_an_unrelated_record(self) -> None:
        provider = MagicMock()
        unrelated = serialize_cooldowns(
            {
                "github:OTHER_TOKEN": CooldownRecord(
                    150,
                    source="fallback",
                    updated_at=90,
                )
            }
        )
        raced = serialize_cooldowns(
            {
                "github:GH_TOKEN": CooldownRecord(
                    200,
                    source="retry-after",
                    updated_at=100,
                )
            }
        )
        stored = unrelated
        write_count = 0

        def get_variable(_name: str, *, use_writer_token: bool = False) -> str:
            assert use_writer_token is True
            return stored

        def set_variable(_name: str, value: str) -> None:
            nonlocal stored, write_count
            write_count += 1
            stored = raced if write_count == 1 else value

        provider.get_variable.side_effect = get_variable
        provider.set_variable.side_effect = set_variable
        error = ProviderRateLimitError(
            retry_after_seconds=90,
            provider="github",
            credential_identity="GH_TOKEN",
            source="retry-after",
        )

        result = persist_cooldown(provider, error, now=100, retries=2)

        assert result is not None
        assert write_count == 2
        assert parse_cooldowns(stored, now=100) == {
            "github:GH_TOKEN": CooldownRecord(200, source="retry-after", updated_at=100),
            "github:OTHER_TOKEN": CooldownRecord(150, source="fallback", updated_at=90),
        }

    def test_uses_writer_token_and_returns_effective_record(self) -> None:
        provider = MagicMock()
        stored = serialize_cooldowns(
            {
                "github:COPILOT_GITHUB_TOKEN": CooldownRecord(
                    200,
                    source="fallback",
                    updated_at=50,
                )
            }
        )

        def get_variable(_name: str, *, use_writer_token: bool = False) -> str:
            assert use_writer_token is True
            return stored

        provider.get_variable.side_effect = get_variable
        provider.set_variable.side_effect = lambda _name, _value: None
        error = ProviderRateLimitError(
            retry_after_seconds=30,
            provider="github",
            credential_identity="COPILOT_GITHUB_TOKEN",
            source="retry-after",
        )

        with patch("agentic_devtools.cli.ci.cooldown.time.time", return_value=100):
            result = persist_cooldown(provider, error, now=100)

        assert result is not None
        assert result[0] == "github:COPILOT_GITHUB_TOKEN"
        assert result[1].resume_at == 200
        assert result[1].source == "fallback"
        provider.set_variable.assert_called_once()

    def test_fails_open_after_write_errors(self) -> None:
        provider = MagicMock()
        provider.get_variable.side_effect = RuntimeError("unavailable")
        error = ProviderRateLimitError(provider="github", credential_identity="GH_TOKEN")

        assert persist_cooldown(provider, error, now=100, retries=1) is None

    def test_waits_between_retries(self) -> None:
        provider = MagicMock()
        provider.get_variable.side_effect = RuntimeError("unavailable")
        error = ProviderRateLimitError(provider="github", credential_identity="GH_TOKEN")

        with patch("agentic_devtools.cli.ci.cooldown.time.sleep") as sleep:
            assert persist_cooldown(provider, error, now=100, retries=2) is None

        sleep.assert_called_once_with(1.0)

    def test_fails_open_on_rate_limit_from_provider_read(self) -> None:
        provider = MagicMock()
        provider.get_variable.side_effect = ProviderRateLimitError(is_rate_limit=True)
        error = ProviderRateLimitError(provider="github", credential_identity="GH_TOKEN")

        assert persist_cooldown(provider, error, now=100, retries=1) is None

    def test_retries_when_known_record_is_seen_again_without_changes(self) -> None:
        provider = MagicMock()
        existing = serialize_cooldowns({"github:GH_TOKEN": CooldownRecord(300, source="fallback", updated_at=90)})
        provider.get_variable.side_effect = [existing, "{}", existing, existing]
        provider.set_variable.side_effect = lambda _name, _value: None
        error = ProviderRateLimitError(
            retry_after_seconds=90,
            provider="github",
            credential_identity="GH_TOKEN",
            source="retry-after",
        )

        result = persist_cooldown(provider, error, now=100, retries=2)

        assert result is not None
        assert result[1].resume_at == 300
        assert provider.set_variable.call_count == 2

    def test_reconciles_stale_read_after_write(self) -> None:
        provider = MagicMock()
        stale = serialize_cooldowns(
            {
                "github:GH_TOKEN": CooldownRecord(
                    150,
                    source="fallback",
                    updated_at=90,
                )
            }
        )
        effective = serialize_cooldowns(
            {
                "github:GH_TOKEN": CooldownRecord(
                    200,
                    source="retry-after",
                    updated_at=100,
                )
            }
        )
        provider.get_variable.side_effect = [None, stale, stale, effective]
        error = ProviderRateLimitError(
            retry_after_seconds=90,
            provider="github",
            credential_identity="GH_TOKEN",
            source="retry-after",
        )

        result = persist_cooldown(provider, error, now=100, retries=2)

        assert result is not None
        assert result[1].resume_at == 200
        assert provider.set_variable.call_count == 2

    def test_retries_until_longer_competing_same_key_cooldown_is_preserved(self) -> None:
        provider = MagicMock()
        shorter = serialize_cooldowns(
            {
                "github:GH_TOKEN": CooldownRecord(
                    150,
                    source="fallback",
                    updated_at=90,
                )
            }
        )
        longer = serialize_cooldowns(
            {
                "github:GH_TOKEN": CooldownRecord(
                    260,
                    source="x-ratelimit-reset",
                    updated_at=110,
                )
            }
        )
        provider.get_variable.side_effect = [None, shorter, longer, longer]
        error = ProviderRateLimitError(
            retry_after_seconds=90,
            provider="github",
            credential_identity="GH_TOKEN",
            source="retry-after",
        )

        result = persist_cooldown(provider, error, now=100, retries=2)

        assert result is not None
        assert result[1] == CooldownRecord(260, source="x-ratelimit-reset", updated_at=110)
        assert provider.set_variable.call_count == 2
