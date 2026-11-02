"""Tests for resolve_cursor."""

import json
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.scheduler import DispatchEvent, resolve_cursor
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestResolveCursor:
    """Tests for the resolve_cursor function."""

    def test_tier1_variable_valid(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = "2025"
        result = resolve_cursor(provider)
        assert result == 2025
        provider.get_variable.assert_called_once_with("AI_PR_LOOP_LAST_DISPATCHED_PR")

    def test_tier1_variable_valid_with_whitespace(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = " 2025 "
        result = resolve_cursor(provider)
        assert result == 2025

    def test_tier1_variable_invalid_falls_to_tier2(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = "not-a-number"
        provider.get_recent_dispatch_history.return_value = [
            DispatchEvent(pr_number=2030, created_at="2024-01-01T00:00:00Z"),
        ]
        result = resolve_cursor(provider)
        assert result == 2030

    def test_tier1_none_falls_to_tier2(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = None
        provider.get_recent_dispatch_history.return_value = [
            DispatchEvent(pr_number=2022, created_at="2024-01-01T00:00:00Z"),
        ]
        result = resolve_cursor(provider)
        assert result == 2022

    def test_tier1_zero_falls_to_tier2(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = "0"
        provider.get_recent_dispatch_history.return_value = []
        result = resolve_cursor(provider)
        assert result is None

    def test_both_tiers_unavailable_returns_none(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = None
        provider.get_recent_dispatch_history.return_value = []
        result = resolve_cursor(provider)
        assert result is None

    def test_tier2_runtime_error_returns_none(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = None
        provider.get_recent_dispatch_history.side_effect = RuntimeError("API error")
        result = resolve_cursor(provider)
        assert result is None

    def test_tier1_error_falls_to_tier2(self) -> None:
        provider = MagicMock()
        provider.get_variable.side_effect = RuntimeError("API error")
        provider.get_recent_dispatch_history.return_value = [
            DispatchEvent(pr_number=2024, created_at="2024-01-01T00:00:00Z"),
        ]
        result = resolve_cursor(provider)
        assert result == 2024

    def test_tier2_not_implemented_returns_none(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = None
        provider.get_recent_dispatch_history.side_effect = NotImplementedError()
        result = resolve_cursor(provider)
        assert result is None

    def test_tier2_json_decode_error_returns_none(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = None
        provider.get_recent_dispatch_history.side_effect = json.JSONDecodeError("bad json", "x", 0)
        result = resolve_cursor(provider)
        assert result is None

    def test_tier2_unexpected_exception_returns_none(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = None
        provider.get_recent_dispatch_history.side_effect = TypeError("unexpected shape")
        result = resolve_cursor(provider)
        assert result is None

    def test_tier2_event_with_zero_pr_number_returns_none(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = None
        provider.get_recent_dispatch_history.return_value = [
            DispatchEvent(pr_number=0, created_at="2024-01-01T00:00:00Z"),
        ]
        result = resolve_cursor(provider)
        assert result is None

    def test_tier1_non_rate_limit_provider_error_falls_to_tier2(self) -> None:
        provider = MagicMock()
        provider.get_variable.side_effect = ProviderRateLimitError(is_rate_limit=False)
        provider.get_recent_dispatch_history.return_value = [
            DispatchEvent(pr_number=2024, created_at="2024-01-01T00:00:00Z"),
        ]

        result = resolve_cursor(provider)

        assert result == 2024

    def test_tier1_rate_limit_provider_error_is_reraised(self) -> None:
        provider = MagicMock()
        provider.get_variable.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="REPO_VARIABLE_WRITER_PAT",
            source="retry-after",
        )

        with pytest.raises(ProviderRateLimitError):
            resolve_cursor(provider)

    def test_tier2_non_rate_limit_provider_error_returns_none(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = None
        provider.get_recent_dispatch_history.side_effect = ProviderRateLimitError(is_rate_limit=False)

        result = resolve_cursor(provider)

        assert result is None

    def test_tier2_rate_limit_provider_error_is_reraised(self) -> None:
        provider = MagicMock()
        provider.get_variable.return_value = None
        provider.get_recent_dispatch_history.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="REPO_VARIABLE_WRITER_PAT",
            source="retry-after",
        )

        with pytest.raises(ProviderRateLimitError):
            resolve_cursor(provider)
