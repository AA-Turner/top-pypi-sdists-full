"""Tests for _report_crash_to_chronos in the world runner."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from plato.worlds.runner import _report_crash_to_chronos

CHRONOS_PATCH = "plato.chronos.sdk.Chronos"


@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    """Create a temporary config file with session info."""
    config = {
        "session": {
            "session_id": "test-session-123",
            "chronos_url": "https://chronos.example.com",
        }
    }
    p = tmp_path / "config.json"
    p.write_text(json.dumps(config))
    return p


@pytest.fixture
def config_file_no_session(tmp_path: Path) -> Path:
    """Config file without session block."""
    p = tmp_path / "config.json"
    p.write_text(json.dumps({"world": {}}))
    return p


class TestReportCrashToChronos:
    def test_reports_failure_via_chronos_sdk(self, config_file: Path):
        """Verify it calls Chronos.complete with correct args."""
        mock_client = MagicMock()

        with (
            patch(CHRONOS_PATCH, return_value=mock_client) as mock_cls,
            patch.dict("os.environ", {"PLATO_API_KEY": ""}),
        ):
            _report_crash_to_chronos(
                config_file,
                exit_code=1,
                error_message="ImportError: cannot import name 'Foo'",
            )

        mock_cls.assert_called_once_with(base_url="https://chronos.example.com", api_key="")
        mock_client.complete.assert_called_once_with(
            session_id="test-session-123",
            status="failed",
            error_message="ImportError: cannot import name 'Foo'",
        )

    def test_passes_api_key_from_env(self, config_file: Path):
        """Verify PLATO_API_KEY env var is passed to Chronos client."""
        mock_client = MagicMock()

        with (
            patch(CHRONOS_PATCH, return_value=mock_client) as mock_cls,
            patch.dict("os.environ", {"PLATO_API_KEY": "pk_test_key"}),
        ):
            _report_crash_to_chronos(config_file, exit_code=1, error_message="crash")

        mock_cls.assert_called_once_with(base_url="https://chronos.example.com", api_key="pk_test_key")

    def test_truncates_long_error_messages(self, config_file: Path):
        """Error messages over 8000 chars should be truncated."""
        mock_client = MagicMock()

        with patch(CHRONOS_PATCH, return_value=mock_client):
            _report_crash_to_chronos(config_file, exit_code=1, error_message="x" * 10000)

        call_kwargs = mock_client.complete.call_args[1]
        assert len(call_kwargs["error_message"]) <= 8000

    def test_no_op_when_config_missing(self, tmp_path: Path):
        """Should silently return if config file doesn't exist."""
        with patch(CHRONOS_PATCH) as mock_cls:
            _report_crash_to_chronos(tmp_path / "nonexistent.json", exit_code=1, error_message="crash")
        mock_cls.assert_not_called()

    def test_no_op_when_session_config_missing(self, config_file_no_session: Path):
        """Should silently return if session block is missing from config."""
        with patch(CHRONOS_PATCH) as mock_cls:
            _report_crash_to_chronos(config_file_no_session, exit_code=1, error_message="crash")
        mock_cls.assert_not_called()

    def test_no_op_when_chronos_url_missing(self, tmp_path: Path):
        """Should silently return if chronos_url is missing."""
        config = {"session": {"session_id": "abc"}}
        p = tmp_path / "config.json"
        p.write_text(json.dumps(config))

        with patch(CHRONOS_PATCH) as mock_cls:
            _report_crash_to_chronos(p, exit_code=1, error_message="crash")
        mock_cls.assert_not_called()

    def test_swallows_sdk_errors(self, config_file: Path):
        """Should not raise if the Chronos SDK call fails."""
        mock_client = MagicMock()
        mock_client.complete.side_effect = Exception("connection refused")

        with patch(CHRONOS_PATCH, return_value=mock_client):
            # Should not raise
            _report_crash_to_chronos(config_file, exit_code=1, error_message="crash")
