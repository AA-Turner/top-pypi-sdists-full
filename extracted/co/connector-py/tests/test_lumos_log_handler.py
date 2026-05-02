import logging
from unittest.mock import MagicMock, patch

import pytest
from connector.handlers.lumos_log_handler import LumosLogHandler


@pytest.fixture
def mock_config():
    with patch("connector.handlers.lumos_log_handler.config") as mock:
        mock.agent_identifier = "test-agent"
        mock.on_prem_agent_api_key = "test-key"
        mock.base_url = "https://test-base-url"
        yield mock


@pytest.fixture
def lumos_handler(mock_config):
    return LumosLogHandler()


def test_lumos_handler_initialization(mock_config):
    handler = LumosLogHandler()
    assert handler.agent_identifier == "test-agent"


def test_lumos_handler_ignores_non_error_logs(lumos_handler):
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    lumos_handler.emit(record)
    # No exception should be raised, and the log should be ignored


def test_lumos_handler_sends_error_logs(lumos_handler, mock_config):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_client.post.return_value = mock_response

    with patch("connector.handlers.lumos_log_handler.AsyncClient") as mock_async_client:
        mock_async_client.return_value.__aenter__.return_value = mock_client

        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            msg="Test error message",
            args=(),
            exc_info=None,
        )

        # Set a formatter to ensure the log message is properly formatted
        lumos_handler.setFormatter(logging.Formatter("%(message)s"))

        # Emit the log record
        lumos_handler.emit(record)

        # Verify the HTTP client was called with correct data
        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert call_args[0][0] == "/logs"
        assert call_args[1]["json"] == {
            "agent_identifier": "test-agent",
            "log": "Test error message",
        }


def test_lumos_handler_handles_http_errors(lumos_handler, mock_config):
    mock_client = MagicMock()
    mock_client.post.side_effect = Exception("HTTP Error")

    with patch("connector.handlers.lumos_log_handler.AsyncClient") as mock_async_client:
        mock_async_client.return_value.__aenter__.return_value = mock_client

        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            msg="Test error message",
            args=(),
            exc_info=None,
        )

        # The handler should not raise an exception
        lumos_handler.emit(record)

        # Verify the HTTP client was called
        mock_client.post.assert_called_once()


def test_lumos_handler_formatting(mock_config):
    handler = LumosLogHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    record = logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname="test.py",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    formatted = handler.format(record)
    assert formatted == "Test message"
