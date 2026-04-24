"""
Extended tests for OpenSearch DB-API exception mapping — covers branches
missed by the base test_exceptions.py.
"""

import sys
import types
from unittest.mock import patch

import pytest

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import (
    AuthenticationError,
    DataError,
    IntegrityError,
    InvalidParameterError,
    OpenSearchConnectionError,
    OperationalError,
    ProgrammingError,
    QueryExecutionError,
    TransientError,
    handle_opensearch_error,
    map_opensearch_exception,
)


# ---------------------------------------------------------------------------
# Create a fake opensearchpy module with exception classes so we can test
# map_opensearch_exception without requiring opensearchpy to be importable.
# ---------------------------------------------------------------------------
def _make_fake_opensearchpy():
    """Build a fake opensearchpy module with the exception hierarchy."""
    mod = types.ModuleType("opensearchpy")

    class TransportError(Exception):
        def __init__(self, status_code, message, info=None):
            super().__init__(message)
            self.status_code = status_code
            self.info = info

    class ConnectionError(TransportError):
        def __init__(self, message, error=None, exception=None):
            super().__init__("N/A", message)
            self.error = error
            self.exception = exception

    class SSLError(ConnectionError):
        pass

    class AuthenticationException(TransportError):
        pass

    class AuthorizationException(TransportError):
        pass

    class RequestError(TransportError):
        pass

    class NotFoundError(TransportError):
        pass

    class ConflictError(TransportError):
        pass

    mod.TransportError = TransportError
    mod.ConnectionError = ConnectionError
    mod.SSLError = SSLError
    mod.AuthenticationException = AuthenticationException
    mod.AuthorizationException = AuthorizationException
    mod.RequestError = RequestError
    mod.NotFoundError = NotFoundError
    mod.ConflictError = ConflictError
    return mod


@pytest.fixture
def fake_opensearchpy():
    """Fixture that injects a fake opensearchpy module into sys.modules."""
    mod = _make_fake_opensearchpy()
    # Remove any cached opensearchpy modules
    to_remove = [k for k in sys.modules if k == "opensearchpy" or k.startswith("opensearchpy.")]
    saved = {k: sys.modules.pop(k) for k in to_remove if k in sys.modules}
    sys.modules["opensearchpy"] = mod
    yield mod
    # Restore
    del sys.modules["opensearchpy"]
    sys.modules.update(saved)


class TestMapOpensearchExceptionExtended:
    """Additional mapping tests for uncovered branches."""

    def test_dbapi_error_returned_as_is(self):
        """If the exception is already a DB-API Error, return it unchanged."""
        original = ProgrammingError("already mapped")
        result = map_opensearch_exception(original)
        assert result is original

    def test_operational_error_returned_as_is(self):
        original = OperationalError("already mapped")
        result = map_opensearch_exception(original)
        assert result is original

    def test_opensearch_connection_error(self, fake_opensearchpy):
        """ConnectionError should map to OpenSearchConnectionError."""
        err = fake_opensearchpy.ConnectionError("connect failed", Exception("timeout"))
        result = map_opensearch_exception(err, {"host": "h", "port": "9200"})
        assert isinstance(result, OpenSearchConnectionError)
        assert "Failed to connect" in str(result)
        assert result.host == "h"

    def test_opensearch_ssl_error(self, fake_opensearchpy):
        """SSLError should map to OpenSearchConnectionError."""
        err = fake_opensearchpy.SSLError("SSL handshake failed", Exception("cert error"))
        result = map_opensearch_exception(err, {"host": "h", "port": "443"})
        assert isinstance(result, OpenSearchConnectionError)
        assert "Failed to connect" in str(result)

    def test_opensearch_authentication_exception(self, fake_opensearchpy):
        """AuthenticationException should map to AuthenticationError."""
        err = fake_opensearchpy.AuthenticationException(401, "Unauthorized")
        result = map_opensearch_exception(err, {"auth_method": "basic", "host": "h"})
        assert isinstance(result, AuthenticationError)
        assert "Authentication failed" in str(result)

    def test_opensearch_authorization_exception(self, fake_opensearchpy):
        """AuthorizationException should map to AuthenticationError."""
        err = fake_opensearchpy.AuthorizationException(403, "Forbidden")
        result = map_opensearch_exception(err, {"auth_method": "api_key", "host": "h"})
        assert isinstance(result, AuthenticationError)
        assert "Authentication failed" in str(result)

    def test_request_error_parsing_exception(self, fake_opensearchpy):
        """parsing_exception should map to ProgrammingError."""
        err = fake_opensearchpy.RequestError(
            400, "bad request", {"error": {"type": "parsing_exception"}}
        )
        result = map_opensearch_exception(err)
        assert isinstance(result, ProgrammingError)

    def test_request_error_sql_parse_exception(self, fake_opensearchpy):
        """sql_parse_exception should map to ProgrammingError."""
        err = fake_opensearchpy.RequestError(
            400, "bad request", {"error": {"type": "sql_parse_exception"}}
        )
        result = map_opensearch_exception(err)
        assert isinstance(result, ProgrammingError)

    def test_request_error_verification_exception(self, fake_opensearchpy):
        """verification_exception should map to InvalidParameterError."""
        err = fake_opensearchpy.RequestError(
            400, "bad request", {"error": {"type": "verification_exception"}}
        )
        result = map_opensearch_exception(err)
        assert isinstance(result, InvalidParameterError)

    def test_request_error_unknown_type(self, fake_opensearchpy):
        """Unknown error type in RequestError should map to QueryExecutionError."""
        err = fake_opensearchpy.RequestError(
            400, "bad request", {"error": {"type": "some_other_error"}}
        )
        result = map_opensearch_exception(err, {"query": "SELECT bad"})
        assert isinstance(result, QueryExecutionError)
        assert result.error_type == "some_other_error"

    def test_request_error_no_info(self, fake_opensearchpy):
        """RequestError with no info dict should map to QueryExecutionError."""
        err = fake_opensearchpy.RequestError(400, "bad request", None)
        result = map_opensearch_exception(err)
        assert isinstance(result, QueryExecutionError)
        assert result.error_type == "unknown"

    def test_request_error_info_not_dict(self, fake_opensearchpy):
        """RequestError with non-dict info should map to QueryExecutionError."""
        err = fake_opensearchpy.RequestError(400, "bad request", "string info")
        result = map_opensearch_exception(err)
        assert isinstance(result, QueryExecutionError)

    def test_not_found_error(self, fake_opensearchpy):
        """NotFoundError should map to DataError."""
        err = fake_opensearchpy.NotFoundError(404, "not found")
        result = map_opensearch_exception(err)
        assert isinstance(result, DataError)

    def test_conflict_error(self, fake_opensearchpy):
        """ConflictError should map to IntegrityError."""
        err = fake_opensearchpy.ConflictError(409, "conflict")
        result = map_opensearch_exception(err)
        assert isinstance(result, IntegrityError)

    def test_transport_error_429(self, fake_opensearchpy):
        """429 status should map to TransientError."""
        err = fake_opensearchpy.TransportError(429, "too many requests")
        result = map_opensearch_exception(err)
        assert isinstance(result, TransientError)

    def test_transport_error_502(self, fake_opensearchpy):
        """502 status should map to TransientError."""
        err = fake_opensearchpy.TransportError(502, "bad gateway")
        result = map_opensearch_exception(err)
        assert isinstance(result, TransientError)

    def test_transport_error_503(self, fake_opensearchpy):
        """503 status should map to TransientError."""
        err = fake_opensearchpy.TransportError(503, "service unavailable")
        result = map_opensearch_exception(err)
        assert isinstance(result, TransientError)

    def test_transport_error_504(self, fake_opensearchpy):
        """504 status should map to TransientError."""
        err = fake_opensearchpy.TransportError(504, "gateway timeout")
        result = map_opensearch_exception(err)
        assert isinstance(result, TransientError)

    def test_transport_error_non_transient(self, fake_opensearchpy):
        """Non-transient transport error should map to OperationalError."""
        err = fake_opensearchpy.TransportError(400, "bad request")
        result = map_opensearch_exception(err)
        assert isinstance(result, OperationalError)
        assert "Transport error" in str(result)

    def test_unknown_exception_with_opensearchpy(self, fake_opensearchpy):
        """Unknown exception type should map to OperationalError."""
        result = map_opensearch_exception(RuntimeError("unknown"), {})
        assert isinstance(result, OperationalError)
        assert "OpenSearch error" in str(result)

    def test_default_execution_context_is_empty(self):
        """When no execution_context is passed, it defaults to empty dict."""
        result = map_opensearch_exception(RuntimeError("boom"))
        assert isinstance(result, OperationalError)


class TestHandleOpensearchErrorDecoratorExtended:
    """Additional decorator tests."""

    def test_maps_opensearch_exception_with_chaining(self):
        """Verify the decorator chains the original exception."""

        @handle_opensearch_error
        def raises_runtime():
            raise RuntimeError("original cause")

        with pytest.raises(OperationalError) as exc_info:
            raises_runtime()
        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, RuntimeError)

    def test_preserves_function_metadata(self):
        """Verify functools.wraps preserves the decorated function's metadata."""

        @handle_opensearch_error
        def my_function():
            """My docstring."""
            pass

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."


class TestMapOpensearchExceptionNoOpensearchPy:
    """Test map_opensearch_exception when opensearch-py is not importable."""

    def test_fallback_to_operational_error(self):
        """When opensearch-py is not installed, map to OperationalError."""
        # Block all opensearchpy modules
        modules_to_block = {
            k: None
            for k in list(sys.modules.keys())
            if k == "opensearchpy" or k.startswith("opensearchpy.")
        }
        modules_to_block["opensearchpy"] = None

        with patch.dict(sys.modules, modules_to_block):
            result = map_opensearch_exception(RuntimeError("no opensearchpy"))
            assert isinstance(result, OperationalError)
            assert "OpenSearch error" in str(result)


class TestConnectionErrorStr:
    """Test OpenSearchConnectionError __str__ edge cases."""

    def test_host_only(self):
        err = OpenSearchConnectionError("fail", host="myhost")
        assert "Host: myhost" in str(err)
        assert "Port" not in str(err)

    def test_port_only(self):
        err = OpenSearchConnectionError("fail", port=9200)
        assert "Port: 9200" in str(err)

    def test_with_multiple_context_keys(self):
        ctx = {"key1": "val1", "key2": "val2"}
        err = OpenSearchConnectionError("fail", execution_context=ctx)
        s = str(err)
        assert "key1: val1" in s
        assert "key2: val2" in s


class TestAuthenticationErrorStr:
    """Test AuthenticationError __str__ edge cases."""

    def test_auth_method_only(self):
        err = AuthenticationError("denied", auth_method="api_key")
        assert "Auth method: api_key" in str(err)

    def test_host_only(self):
        err = AuthenticationError("denied", host="es.example.com")
        assert "Host: es.example.com" in str(err)


class TestTransientErrorStr:
    """Test TransientError __str__ edge cases."""

    def test_retry_after_only(self):
        err = TransientError("wait", retry_after=10)
        assert "Retry after: 10s" in str(err)

    def test_attempt_count_only_no_max(self):
        """When only attempt_count is set but not max_attempts, no attempt info shown."""
        err = TransientError("wait", attempt_count=2)
        assert "Attempt" not in str(err)

    def test_max_attempts_only_no_count(self):
        """When only max_attempts is set but not attempt_count, no attempt info shown."""
        err = TransientError("wait", max_attempts=5)
        assert "Attempt" not in str(err)


class TestQueryExecutionErrorStr:
    """Test QueryExecutionError __str__ edge cases."""

    def test_error_type_only(self):
        err = QueryExecutionError("failed", error_type="timeout")
        assert "Error type: timeout" in str(err)
        assert "Query" not in str(err)

    def test_query_only(self):
        err = QueryExecutionError("failed", query="SELECT 1")
        assert "Query: SELECT 1" in str(err)

    def test_short_query_not_truncated(self):
        err = QueryExecutionError("failed", query="SELECT 1")
        assert "..." not in str(err)


class TestInvalidParameterErrorStr:
    """Test InvalidParameterError __str__ edge cases."""

    def test_parameter_name_only(self):
        err = InvalidParameterError("bad", parameter_name="timeout")
        assert "Parameter: timeout" in str(err)

    def test_parameter_value_zero(self):
        """parameter_value=0 should still be shown (not falsy)."""
        err = InvalidParameterError("bad", parameter_name="port", parameter_value=0)
        assert "Value: 0" in str(err)
