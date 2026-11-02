"""Unit tests for _validate_retry_settings in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

import pytest

from scripts.audit_pr_cleanup import _validate_retry_settings


def test__validate_retry_settings_accepts_valid_values() -> None:
    """_validate_retry_settings accepts finite non-negative retry settings."""
    _validate_retry_settings(max_retries=0, retry_delay=0.0)
    _validate_retry_settings(max_retries=3, retry_delay=1.5)


def test__validate_retry_settings_negative_max_retries_raises() -> None:
    """_validate_retry_settings rejects a negative retry budget."""
    with pytest.raises(ValueError, match="max_retries cannot be negative"):
        _validate_retry_settings(max_retries=-1, retry_delay=0.0)


def test__validate_retry_settings_negative_retry_delay_raises() -> None:
    """_validate_retry_settings rejects a negative retry delay."""
    with pytest.raises(ValueError, match="retry_delay must be finite and non-negative"):
        _validate_retry_settings(max_retries=0, retry_delay=-0.1)


@pytest.mark.parametrize("value", [float("nan"), float("inf")])
def test__validate_retry_settings_non_finite_retry_delay_raises(value: float) -> None:
    """_validate_retry_settings rejects NaN and infinite retry delays."""
    with pytest.raises(ValueError, match="retry_delay must be finite and non-negative"):
        _validate_retry_settings(max_retries=0, retry_delay=value)
