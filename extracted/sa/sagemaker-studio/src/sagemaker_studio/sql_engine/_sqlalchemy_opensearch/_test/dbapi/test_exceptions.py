"""
Unit tests for OpenSearch DB-API exception hierarchy and mapping utilities.
"""

import pytest

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import (
    AuthenticationError,
    DatabaseError,
    DataError,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    InvalidParameterError,
    NotSupportedError,
    OpenSearchConnectionError,
    OperationalError,
    ProgrammingError,
    QueryExecutionError,
    TransientError,
    Warning,
    handle_opensearch_error,
    map_opensearch_exception,
)


class TestExceptionHierarchy:
    """Test the DB-API 2.0 exception hierarchy."""

    def test_base_exceptions(self):
        assert issubclass(Error, Exception)
        assert issubclass(Warning, Exception)

    def test_interface_error_inherits_error(self):
        assert issubclass(InterfaceError, Error)

    def test_database_error_inherits_error(self):
        assert issubclass(DatabaseError, Error)

    def test_database_error_subclasses(self):
        assert issubclass(DataError, DatabaseError)
        assert issubclass(OperationalError, DatabaseError)
        assert issubclass(IntegrityError, DatabaseError)
        assert issubclass(InternalError, DatabaseError)
        assert issubclass(ProgrammingError, DatabaseError)
        assert issubclass(NotSupportedError, DatabaseError)

    def test_opensearch_specific_exceptions(self):
        assert issubclass(OpenSearchConnectionError, OperationalError)
        assert issubclass(AuthenticationError, OperationalError)
        assert issubclass(TransientError, OperationalError)
        assert issubclass(QueryExecutionError, OperationalError)
        assert issubclass(InvalidParameterError, ProgrammingError)


class TestConnectionError:
    """Test OpenSearchConnectionError with extra context."""

    def test_basic_message(self):
        err = OpenSearchConnectionError("connection refused")
        assert str(err) == "connection refused"

    def test_with_host_and_port(self):
        err = OpenSearchConnectionError("connection refused", host="myhost", port=9200)
        result = str(err)
        assert "Host: myhost" in result
        assert "Port: 9200" in result

    def test_with_execution_context(self):
        ctx = {"attempt": "3"}
        err = OpenSearchConnectionError("timeout", execution_context=ctx)
        assert "attempt: 3" in str(err)

    def test_defaults(self):
        err = OpenSearchConnectionError("msg")
        assert err.host is None
        assert err.port is None
        assert err.execution_context == {}


class TestAuthenticationError:
    """Test AuthenticationError with extra context."""

    def test_basic_message(self):
        err = AuthenticationError("bad creds")
        assert str(err) == "bad creds"

    def test_with_auth_method_and_host(self):
        err = AuthenticationError("denied", auth_method="basic", host="es.example.com")
        result = str(err)
        assert "Auth method: basic" in result
        assert "Host: es.example.com" in result

    def test_with_execution_context(self):
        ctx = {"user": "admin"}
        err = AuthenticationError("denied", execution_context=ctx)
        assert "user: admin" in str(err)


class TestInvalidParameterError:
    """Test InvalidParameterError with extra context."""

    def test_basic_message(self):
        err = InvalidParameterError("bad param")
        assert str(err) == "bad param"

    def test_with_parameter_details(self):
        err = InvalidParameterError("invalid", parameter_name="port", parameter_value=-1)
        result = str(err)
        assert "Parameter: port" in result
        assert "Value: -1" in result

    def test_with_execution_context(self):
        ctx = {"source": "url"}
        err = InvalidParameterError("invalid", execution_context=ctx)
        assert "source: url" in str(err)


class TestTransientError:
    """Test TransientError with retry metadata."""

    def test_basic_message(self):
        err = TransientError("service unavailable")
        assert str(err) == "service unavailable"

    def test_with_retry_after(self):
        err = TransientError("rate limited", retry_after=5)
        assert "Retry after: 5s" in str(err)

    def test_with_attempt_info(self):
        err = TransientError("retry", attempt_count=2, max_attempts=5)
        assert "Attempt: 2/5" in str(err)

    def test_with_execution_context(self):
        ctx = {"query": "SELECT 1"}
        err = TransientError("timeout", execution_context=ctx)
        assert "query: SELECT 1" in str(err)


class TestQueryExecutionError:
    """Test QueryExecutionError with query context."""

    def test_basic_message(self):
        err = QueryExecutionError("syntax error")
        assert str(err) == "syntax error"

    def test_with_query_and_error_type(self):
        err = QueryExecutionError("failed", query="SELECT *", error_type="parsing_exception")
        result = str(err)
        assert "Query: SELECT *" in result
        assert "Error type: parsing_exception" in result

    def test_long_query_truncated(self):
        long_query = "SELECT " + "a, " * 100
        err = QueryExecutionError("failed", query=long_query)
        result = str(err)
        assert "..." in result


class TestMapOpensearchException:
    """Test map_opensearch_exception utility."""

    def test_unknown_exception_maps_to_operational_error(self):
        result = map_opensearch_exception(ValueError("something"))
        assert isinstance(result, OperationalError)
        assert "OpenSearch error" in str(result)

    def test_execution_context_preserved(self):
        ctx = {"host": "myhost"}
        result = map_opensearch_exception(ValueError("err"), ctx)
        assert isinstance(result, OperationalError)

    def test_opensearch_connection_error(self):
        """Test mapping when opensearch-py ConnectionError is available."""
        try:
            from opensearchpy import ConnectionError as OSConnectionError

            os_err = OSConnectionError("N/A", "connect failed", Exception("timeout"))
            result = map_opensearch_exception(os_err, {"host": "h", "port": "9200"})
            assert isinstance(result, OpenSearchConnectionError)
        except ImportError:
            pytest.skip("opensearch-py not installed")

    def test_opensearch_auth_exception(self):
        try:
            from opensearchpy import AuthenticationException

            os_err = AuthenticationException(401, "Unauthorized", {})
            result = map_opensearch_exception(os_err, {"auth_method": "basic", "host": "h"})
            assert isinstance(result, AuthenticationError)
        except ImportError:
            pytest.skip("opensearch-py not installed")

    def test_opensearch_request_error_parsing(self):
        try:
            from opensearchpy import RequestError

            os_err = RequestError(400, "bad request", {"error": {"type": "parsing_exception"}})
            result = map_opensearch_exception(os_err)
            assert isinstance(result, ProgrammingError)
        except ImportError:
            pytest.skip("opensearch-py not installed")

    def test_opensearch_not_found_error(self):
        try:
            from opensearchpy import NotFoundError

            os_err = NotFoundError(404, "not found", {})
            result = map_opensearch_exception(os_err)
            assert isinstance(result, DataError)
        except ImportError:
            pytest.skip("opensearch-py not installed")

    def test_opensearch_conflict_error(self):
        try:
            from opensearchpy import ConflictError

            os_err = ConflictError(409, "conflict", {})
            result = map_opensearch_exception(os_err)
            assert isinstance(result, IntegrityError)
        except ImportError:
            pytest.skip("opensearch-py not installed")

    def test_opensearch_transport_error_transient(self):
        try:
            from opensearchpy import TransportError

            os_err = TransportError(429, "too many requests", {})
            result = map_opensearch_exception(os_err)
            assert isinstance(result, TransientError)
        except ImportError:
            pytest.skip("opensearch-py not installed")

    def test_opensearch_transport_error_non_transient(self):
        try:
            from opensearchpy import TransportError

            os_err = TransportError(400, "bad request", {})
            result = map_opensearch_exception(os_err)
            assert isinstance(result, OperationalError)
        except ImportError:
            pytest.skip("opensearch-py not installed")


class TestHandleOpensearchErrorDecorator:
    """Test the handle_opensearch_error decorator."""

    def test_passes_through_on_success(self):
        @handle_opensearch_error
        def good_func():
            return "ok"

        assert good_func() == "ok"

    def test_reraises_dbapi_exceptions(self):
        @handle_opensearch_error
        def raises_dbapi():
            raise ProgrammingError("bad sql")

        with pytest.raises(ProgrammingError, match="bad sql"):
            raises_dbapi()

    def test_maps_generic_exception(self):
        @handle_opensearch_error
        def raises_generic():
            raise RuntimeError("boom")

        with pytest.raises(OperationalError):
            raises_generic()
