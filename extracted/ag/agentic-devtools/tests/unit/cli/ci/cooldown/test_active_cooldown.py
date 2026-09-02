"""Tests for active_cooldown()."""

from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.cooldown import CooldownRecord, active_cooldown, serialize_cooldowns
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestActiveCooldown:
    """active_cooldown() uses the configured identity and fails open on read errors."""

    def test_uses_configured_identity(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = serialize_cooldowns({"github:safe.id": CooldownRecord(101, updated_at=1)})

        with patch.dict("os.environ", {"AI_PR_LOOP_CREDENTIAL_IDENTITY": "safe.id"}, clear=True):
            result = active_cooldown(provider, now=100)

        assert result is not None
        assert result[0] == "github:safe.id"

    def test_returns_none_when_record_missing_or_provider_errors(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            assert active_cooldown(MagicMock(), now=100) is None

        provider = MagicMock()
        provider.get_variable.side_effect = RuntimeError("unavailable")

        assert active_cooldown(provider, now=100) is None

    def test_fails_open_for_non_rate_limit_provider_error(self) -> None:
        provider = MagicMock()
        provider.get_variable.side_effect = ProviderRateLimitError(is_rate_limit=False)

        assert active_cooldown(provider, now=100) is None

    def test_reraises_rate_limit_provider_error(self) -> None:
        provider = MagicMock()
        provider.get_variable.side_effect = ProviderRateLimitError(is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            active_cooldown(provider, now=100)

    def test_returns_latest_active_record_across_multiple_identities(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = serialize_cooldowns(
            {
                "github:SPECKIT_PR_TOKEN": CooldownRecord(120, updated_at=1),
                "github:AGDT_PR_APPROVER_PAT": CooldownRecord(180, updated_at=1),
            }
        )

        result = active_cooldown(
            provider,
            credential_identity=("SPECKIT_PR_TOKEN", "AGDT_PR_APPROVER_PAT"),
            now=100,
        )

        assert result is not None
        assert result[0] == "github:AGDT_PR_APPROVER_PAT"

    def test_uses_explicit_string_identity(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = serialize_cooldowns({"github:safe.id": CooldownRecord(101, updated_at=1)})

        result = active_cooldown(provider, credential_identity="safe.id", now=100)

        assert result is not None
        assert result[0] == "github:safe.id"

    def test_ignores_invalid_iterable_entries_and_falls_back_when_none_are_valid(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = serialize_cooldowns({"github:GH_TOKEN": CooldownRecord(101, updated_at=1)})

        with patch.dict("os.environ", {}, clear=True):
            result = active_cooldown(
                provider,
                credential_identity=cast(tuple[str, ...], ("", "   ", object())),  # type: ignore[arg-type]
                now=100,
            )

        assert result is not None
        assert result[0] == "github:GH_TOKEN"

    def test_non_iterable_identity_falls_back_to_environment_identity(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = serialize_cooldowns({"github:GH_TOKEN": CooldownRecord(101, updated_at=1)})

        with patch.dict("os.environ", {}, clear=True):
            result = active_cooldown(
                provider,
                credential_identity=cast("str | tuple[str, ...]", 123),  # type: ignore[arg-type]
                now=100,
            )

        assert result is not None
        assert result[0] == "github:GH_TOKEN"
