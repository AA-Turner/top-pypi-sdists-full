"""Tests for rate-limit timing selection."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.exceptions import ProviderRateLimitError
from agentic_devtools.cli.ci.reconciliation import command_errors


@pytest.mark.parametrize("conversion_error", [OverflowError, ValueError, OSError])
@pytest.mark.parametrize(
    ("retry_after_seconds", "expected_timing"),
    [(30, "retry after 30 seconds"), (None, "reset timing unknown")],
)
def test_unrepresentable_reset_timestamp_uses_fallback(
    conversion_error, retry_after_seconds, expected_timing, monkeypatch
) -> None:
    """Unrepresentable reset times fall back to retry delay or unknown timing."""
    fromtimestamp = Mock(side_effect=conversion_error("out of range"))
    monkeypatch.setattr(command_errors, "datetime", SimpleNamespace(fromtimestamp=fromtimestamp))
    error = ProviderRateLimitError(retry_after_seconds, reset_timestamp=1792684800000)

    assert command_errors._get_rate_limit_timing(error) == expected_timing
    fromtimestamp.assert_called_once_with(1792684800000, command_errors.UTC)
