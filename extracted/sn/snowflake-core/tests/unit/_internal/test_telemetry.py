import platform

from types import SimpleNamespace
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest

from snowflake.connector.telemetry import TelemetryData
from snowflake.connector.telemetry import TelemetryField as ConnectorTelemetryField
from snowflake.core._common import ObjectReferenceMixin
from snowflake.core._internal.telemetry import ApiTelemetryClient, _TelemetryEventBuilder, api_telemetry
from snowflake.core._internal.utils import TelemetryField
from snowflake.core.exceptions import APIError
from snowflake.core.version import __version__ as VERSION


class TestApiTelemetryClient:
    """Test suite for ApiTelemetryClient class."""

    @pytest.fixture
    def mock_connection(self):
        """Create a mock SnowflakeConnection for testing."""
        conn = MagicMock()
        conn._telemetry = MagicMock()
        return conn

    @pytest.fixture
    def telemetry_client(self, mock_connection):
        """Create an ApiTelemetryClient instance with mocked dependencies."""
        return ApiTelemetryClient(mock_connection)

    @pytest.fixture
    def mock_connection_no_telemetry(self):
        """Create a mock SnowflakeConnection without telemetry for testing."""
        conn = MagicMock()
        conn._telemetry = None
        return conn

    def test_init_with_telemetry_enabled(self, mock_connection):
        """Test initialization when telemetry is enabled."""
        with patch("snowflake.core._internal.telemetry.is_running_inside_stored_procedure", return_value=False):
            client = ApiTelemetryClient(mock_connection)
            assert client.telemetry == mock_connection._telemetry

    def test_init_with_telemetry_disabled_in_stored_procedure(self, mock_connection):
        """Test initialization when running inside a stored procedure (telemetry disabled)."""
        with patch("snowflake.core._internal.telemetry.is_running_inside_stored_procedure", return_value=True):
            client = ApiTelemetryClient(mock_connection)
            assert client.telemetry is None

    def test_init_with_no_telemetry_client(self, mock_connection_no_telemetry):
        """Test initialization when connection has no telemetry client."""
        with patch("snowflake.core._internal.telemetry.is_running_inside_stored_procedure", return_value=False):
            client = ApiTelemetryClient(mock_connection_no_telemetry)

            assert client.telemetry is None

    def test_send_with_telemetry_enabled(self, telemetry_client):
        """Test _send method when telemetry is enabled."""
        test_message = {"test": "data"}
        timestamp = 12345

        telemetry_client._send(test_message, timestamp)

        telemetry_client.telemetry.try_add_log_to_batch.assert_called_once()
        call_args = telemetry_client.telemetry.try_add_log_to_batch.call_args[0][0]
        assert isinstance(call_args, TelemetryData)
        assert call_args.message == test_message
        assert call_args.timestamp == timestamp

    def test_send_with_no_telemetry(self, mock_connection_no_telemetry):
        """Test send method when telemetry is disabled."""
        with patch("snowflake.core._internal.telemetry.is_running_inside_stored_procedure", return_value=False):
            client = ApiTelemetryClient(mock_connection_no_telemetry)

            # Should not raise an exception and should do nothing
            client.safe_send({"test": "data"})
            # No assertions needed as method should return early

    def test_event_builder_usage_build(self, telemetry_client):
        """Test building a usage telemetry event."""
        builder = _TelemetryEventBuilder(class_name="TestClass", func_name="test_function")
        # Current implementation expects _data to be a mapping when building
        builder._data = {}
        result = builder.usage_event()

        assert result[ConnectorTelemetryField.KEY_SOURCE.value] == "snowflake.core"
        assert result[TelemetryField.KEY_VERSION.value] == VERSION
        assert result[TelemetryField.KEY_PYTHON_VERSION.value] == platform.python_version()
        assert result[TelemetryField.KEY_OS.value] == platform.system()
        assert result[ConnectorTelemetryField.KEY_TYPE.value] == "python_api"
        assert result[TelemetryField.KEY_DATA.value]["class_name"] == "TestClass"
        assert result[TelemetryField.KEY_DATA.value][TelemetryField.KEY_FUNC_NAME.value] == "test_function"

    def test_event_builder_exception_generic(self):
        """Test exception event building for generic exception."""
        builder = _TelemetryEventBuilder(class_name="TestClass", func_name="test_function")
        result = builder.exception_event(ValueError("Test error"))

        assert result[ConnectorTelemetryField.KEY_TYPE.value] == "python_api_exception"
        data_section = result[TelemetryField.KEY_DATA.value]
        assert data_section["exception_type"] == "ValueError"

    def test_event_builder_exception_api_error(self):
        """Test exception event building for APIError subclass."""

        class MockAPIError(APIError):
            def __init__(self):
                self.status = 400
                self.reason = "Bad Request"

            def get_request_info(self):
                # Include 'message' to satisfy APIError.__str__ path
                return {"message": "", "request_id": "test_request_id", "error_code": "test_error_code"}

        api_error = MockAPIError()
        builder = _TelemetryEventBuilder(class_name="TestClass", func_name="test_function")
        result = builder.exception_event(api_error)

        assert result[ConnectorTelemetryField.KEY_SOURCE.value] == "snowflake.core"
        assert result[TelemetryField.KEY_VERSION.value] == VERSION
        assert result[TelemetryField.KEY_PYTHON_VERSION.value] == platform.python_version()
        assert result[TelemetryField.KEY_OS.value] == platform.system()
        assert result[ConnectorTelemetryField.KEY_TYPE.value] == "python_api_exception"
        assert result[TelemetryField.KEY_DATA.value]["class_name"] == "TestClass"
        assert result[TelemetryField.KEY_DATA.value][TelemetryField.KEY_FUNC_NAME.value] == "test_function"
        assert TelemetryField.KEY_CI_ENVIRONMENT_TYPE.value in result

        data = result[TelemetryField.KEY_DATA.value]
        assert data["exception_type"] == "MockAPIError"
        assert data["http_code"] == 400
        assert data["request_id"] == "test_request_id"
        assert data["error_code"] == "test_error_code"
        # pragma: allowlist nextline secret
        assert data["exception_sha256"] == "65da287bf807d02bbd7dcef6bf879d31f2fb167dfb8bbc4ceff45176dc52d61a"
        assert data["is_python_api_error"] is True

    def test_event_builder_exception_none(self):
        """Test exception event building when exception is None."""
        builder = _TelemetryEventBuilder(class_name="TestClass", func_name="test_function")
        result = builder.exception_event(None)  # type: ignore[arg-type]
        data = result[TelemetryField.KEY_DATA.value]
        assert data["exception_type"] == "NoneType"
        assert data["is_python_api_error"] is False


class _DummyCollection:
    def __init__(self, root):
        # minimal _api with api_client attribute to satisfy decorator
        self._api = SimpleNamespace(api_client=object())
        self._root = root

    @property
    def root(self):
        return self._root


class _DummyResource(ObjectReferenceMixin[object]):
    def __init__(self, telemetry_client):
        root = SimpleNamespace(_telemetry_client=telemetry_client)
        self.collection = _DummyCollection(root)

    @api_telemetry
    def success_method(self):
        return "ok"

    @api_telemetry
    def failing_method(self):
        raise ValueError("boom")


def test_api_telemetry_sends_usage_event():
    telemetry_client = SimpleNamespace(safe_send=mock.Mock())
    res = _DummyResource(telemetry_client)

    assert res.success_method() == "ok"

    telemetry_client.safe_send.assert_called_once()
    event = telemetry_client.safe_send.call_args[0][0]
    assert event["type"] == "python_api"
    assert event["source"] == "snowflake.core"
    assert event["data"]["class_name"] == "_DummyResource"
    assert event["data"]["func_name"] == "success_method"


def test_api_telemetry_sends_exception_event_on_error():
    telemetry_client = SimpleNamespace(safe_send=mock.Mock())
    res = _DummyResource(telemetry_client)

    with pytest.raises(ValueError):
        res.failing_method()

    # First usage event, then exception event
    assert telemetry_client.safe_send.call_count == 2
    _, exc_call = telemetry_client.safe_send.call_args_list
    exc_event = exc_call[0][0]
    assert exc_event["type"] == "python_api_exception"
    assert exc_event["data"]["class_name"] == "_DummyResource"
    assert exc_event["data"]["func_name"] == "failing_method"
    assert exc_event["data"]["exception_type"] == "ValueError"
