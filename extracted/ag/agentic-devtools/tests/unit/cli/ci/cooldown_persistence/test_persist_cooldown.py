"""Tests for persist_cooldown()."""

import json
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.cooldown import (
    CooldownRecord,
    parse_cooldowns,
    serialize_cooldowns,
)
from agentic_devtools.cli.ci.cooldown_persistence import persist_cooldown
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestPersistCooldown:
    """persist_cooldown() reads with the writer token and reports the effective record."""

    @pytest.mark.parametrize("stored_deadline,expected", [(1e300, 200), (10**400, 200), (300, 300)])
    @pytest.mark.parametrize("stale_readback", [False, True])
    @pytest.mark.parametrize("explicit_now", [False, True])
    def test_repairs_invalid_deadline_and_retries_with_one_validation_time(
        self, stored_deadline, expected, stale_readback, explicit_now
    ):
        initial = json.dumps(
            {
                "legacy": True,
                "provider_cooldowns": {
                    "github:GH_TOKEN": {"resume_at": stored_deadline, "custom": "keep"},
                    "github:OTHER": {"resume_at": 1e300},
                },
            }
        )
        stored = initial
        reads = 0
        provider = MagicMock()

        def get_variable(_name, *, use_writer_token=False):
            nonlocal reads
            assert use_writer_token is True
            reads += 1
            return initial if stale_readback and reads == 2 else stored

        def set_variable(_name, value):
            nonlocal stored
            stored = value

        provider.get_variable.side_effect = get_variable
        provider.set_variable.side_effect = set_variable
        error = ProviderRateLimitError(
            retry_after_seconds=90,
            provider="github",
            credential_identity="GH_TOKEN",
            source="retry-after",
        )
        with (
            patch(
                "agentic_devtools.cli.ci.cooldown_persistence.time.time", side_effect=[] if explicit_now else [100]
            ) as clock,
            patch("agentic_devtools.cli.ci.cooldown_persistence.logger.warning") as warning,
            patch("agentic_devtools.cli.ci.cooldown_persistence.time.sleep") as sleep,
        ):
            result = persist_cooldown(provider, error, retries=2, **({"now": 100} if explicit_now else {}))
        assert result is not None
        assert result[0] == "github:GH_TOKEN"
        assert result[1].resume_at == expected
        assert clock.call_count == (0 if explicit_now else 1)
        attempts = 2 if stale_readback else 1
        assert provider.set_variable.call_count == attempts
        assert reads == 2 * attempts
        sleep.assert_not_called()
        assert not any(
            call.args[0].startswith("Could not persist provider cooldown") for call in warning.call_args_list
        )
        payload = json.loads(stored)
        assert payload["legacy"] is True
        assert payload["provider_cooldowns"]["github:GH_TOKEN"]["custom"] == "keep"
        assert payload["provider_cooldowns"]["github:OTHER"] == {"resume_at": 1e300}
        assert parse_cooldowns(stored, now=100)["github:GH_TOKEN"].resume_at == expected

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

    def test_observation_time_does_not_discard_current_other_credential_cooldowns(self) -> None:
        other = CooldownRecord(86600, source="fallback", updated_at=100)
        stored = [serialize_cooldowns({"github:OTHER_TOKEN": other})]
        provider = MagicMock()
        provider.get_variable.side_effect = lambda *_args, **_kwargs: stored[0]
        provider.set_variable.side_effect = lambda _name, value: stored.__setitem__(0, value)
        error = ProviderRateLimitError(
            retry_after_seconds=30,
            provider="github",
            credential_identity="DEFAULT",
            source="retry-after",
        )

        with patch("agentic_devtools.cli.ci.cooldown_persistence.time.time", return_value=200):
            assert persist_cooldown(provider, error, observed_at=100) is None

        records = parse_cooldowns(stored[0], now=200)
        assert records == {"github:OTHER_TOKEN": other}
        assert provider.set_variable.call_count == 1
        assert json.loads(stored[0])["provider_cooldowns"]["github:DEFAULT"]["resume_at"] == 140
