# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the Sentry integration module."""

from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp._sentry import (
    DISABLE_SENTRY_ENV_VAR,
    _get_package_version,
    capture_exception,
    capture_message,
    init_sentry_tracking,
)


@pytest.fixture(autouse=True)
def reset_sentry_state():
    """Reset the global sentry state before each test."""
    import airbyte_ops_mcp._sentry as sentry_module

    sentry_module._sentry_initialized = False
    yield
    sentry_module._sentry_initialized = False


@pytest.mark.parametrize(
    "version_result,expected",
    [
        pytest.param("1.2.3", "1.2.3", id="valid_version"),
        pytest.param(None, "unknown", id="version_not_found"),
    ],
)
def test_get_package_version(version_result: str | None, expected: str) -> None:
    """Test _get_package_version returns correct version or 'unknown'."""
    if version_result is None:
        with patch(
            "importlib.metadata.version",
            side_effect=Exception("Package not found"),
        ):
            assert _get_package_version() == expected
    else:
        with patch("importlib.metadata.version", return_value=version_result):
            assert _get_package_version() == expected


def test_init_sentry_disabled_via_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test init_sentry returns False when disabled via environment variable."""
    monkeypatch.setenv(DISABLE_SENTRY_ENV_VAR, "1")
    assert init_sentry_tracking() is False


def test_init_sentry_already_initialized(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test init_sentry returns True if already initialized."""
    import airbyte_ops_mcp._sentry as sentry_module

    sentry_module._sentry_initialized = True
    assert init_sentry_tracking() is True


def test_capture_exception_calls_sentry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test capture_exception calls sentry_sdk.capture_exception when initialized."""
    import airbyte_ops_mcp._sentry as sentry_module

    mock_capture = MagicMock()
    monkeypatch.setattr("sentry_sdk.capture_exception", mock_capture)
    monkeypatch.setattr(sentry_module, "_sentry_initialized", True)

    test_exception = ValueError("test error")
    capture_exception(test_exception)

    mock_capture.assert_called_once_with(test_exception)


def test_capture_message_calls_sentry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test capture_message calls sentry_sdk.capture_message when initialized."""
    import airbyte_ops_mcp._sentry as sentry_module

    mock_capture = MagicMock()
    monkeypatch.setattr("sentry_sdk.capture_message", mock_capture)
    monkeypatch.setattr(sentry_module, "_sentry_initialized", True)

    capture_message("test message", level="warning")

    mock_capture.assert_called_once_with("test message", level="warning")


def test_capture_exception_skips_when_not_initialized(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test capture_exception does nothing when Sentry is not initialized."""
    # Disable Sentry via env var so it won't initialize
    monkeypatch.setenv(DISABLE_SENTRY_ENV_VAR, "1")

    with patch("sentry_sdk.capture_exception") as mock_capture:
        capture_exception(ValueError("test"))
        mock_capture.assert_not_called()


def test_capture_message_skips_when_not_initialized(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test capture_message does nothing when Sentry is not initialized."""
    # Disable Sentry via env var so it won't initialize
    monkeypatch.setenv(DISABLE_SENTRY_ENV_VAR, "1")

    with patch("sentry_sdk.capture_message") as mock_capture:
        capture_message("test")
        mock_capture.assert_not_called()
