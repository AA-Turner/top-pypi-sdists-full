"""Unit tests for the Workday Data Connect Connection class.

Tests connection lifecycle, cursor creation, transaction methods, and error handling.
"""

from unittest.mock import Mock, patch

import pytest

from ...dbapi.connection import Connection
from ...dbapi.cursor import Cursor
from ...dbapi.exceptions import InterfaceError


@pytest.fixture
def mock_trino_connect():
    with patch(
        "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.connection.trino.dbapi.connect"
    ) as mock:
        mock.return_value = Mock()
        yield mock


@pytest.fixture
def connection_params():
    return {
        "host": "example.workday.com",
        "port": 443,
        "client_id": "test-client-id",
        "isu": "test-isu",
        "token_endpoint": "https://example.workday.com/oauth/token",
        "private_key": "test-private-key",
    }


class TestConnectionInitialization:
    """Test connection initialization and parameter handling."""

    def test_basic_initialization(self, mock_trino_connect, connection_params):
        conn = Connection(**connection_params)

        assert conn is not None
        assert conn._closed is False
        mock_trino_connect.assert_called_once()

    def test_trino_connect_called_with_correct_defaults(
        self, mock_trino_connect, connection_params
    ):
        Connection(**connection_params)

        call_kwargs = mock_trino_connect.call_args[1]
        assert call_kwargs["host"] == "example.workday.com"
        assert call_kwargs["port"] == 443
        assert call_kwargs["catalog"] == "workday_core"
        assert call_kwargs["schema"] == "public"
        assert call_kwargs["http_scheme"] == "https"
        assert call_kwargs["session_properties"] == {}

    def test_custom_catalog(self, mock_trino_connect, connection_params):
        connection_params["catalog"] = "custom_catalog"
        Connection(**connection_params)

        call_kwargs = mock_trino_connect.call_args[1]
        assert call_kwargs["catalog"] == "custom_catalog"

    def test_custom_schema(self, mock_trino_connect, connection_params):
        connection_params["schema"] = "custom_schema"
        Connection(**connection_params)

        call_kwargs = mock_trino_connect.call_args[1]
        assert call_kwargs["schema"] == "custom_schema"

    def test_session_properties_passed_through(self, mock_trino_connect, connection_params):
        connection_params["session_properties"] = "key1:val1,key2:val2"
        Connection(**connection_params)

        call_kwargs = mock_trino_connect.call_args[1]
        assert call_kwargs["session_properties"] == {"key1": "val1", "key2": "val2"}

    def test_auth_object_passed_to_trino(self, mock_trino_connect, connection_params):
        Connection(**connection_params)

        call_kwargs = mock_trino_connect.call_args[1]
        assert call_kwargs["auth"] is not None

    def test_missing_required_field_raises(self, mock_trino_connect):
        with pytest.raises(ValueError):
            Connection(
                host="h",
                port=443,
                client_id="",
                isu="i",
                token_endpoint="t",
                private_key="k",
            )

    def test_extra_kwargs_ignored(self, mock_trino_connect, connection_params):
        connection_params["unknown_param"] = "value"
        conn = Connection(**connection_params)
        assert conn is not None


class TestConnectionCursor:
    """Test cursor creation."""

    def test_cursor_returns_cursor_instance(self, mock_trino_connect, connection_params):
        conn = Connection(**connection_params)
        cursor = conn.cursor()

        assert isinstance(cursor, Cursor)

    def test_cursor_delegates_to_trino(self, mock_trino_connect, connection_params):
        mock_trino_conn = mock_trino_connect.return_value
        conn = Connection(**connection_params)
        conn.cursor()

        mock_trino_conn.cursor.assert_called_once()

    def test_multiple_cursors(self, mock_trino_connect, connection_params):
        conn = Connection(**connection_params)
        c1 = conn.cursor()
        c2 = conn.cursor()

        assert c1 is not c2

    def test_cursor_after_close_raises_interface_error(self, mock_trino_connect, connection_params):
        conn = Connection(**connection_params)
        conn.close()

        with pytest.raises(InterfaceError, match="Connection is closed"):
            conn.cursor()


class TestConnectionTransactions:
    """Test transaction methods."""

    def test_commit_delegates_to_trino(self, mock_trino_connect, connection_params):
        mock_trino_conn = mock_trino_connect.return_value
        conn = Connection(**connection_params)
        conn.commit()

        mock_trino_conn.commit.assert_called_once()

    def test_rollback_delegates_to_trino(self, mock_trino_connect, connection_params):
        mock_trino_conn = mock_trino_connect.return_value
        conn = Connection(**connection_params)
        conn.rollback()

        mock_trino_conn.rollback.assert_called_once()


class TestConnectionClose:
    """Test connection close behavior."""

    def test_close_delegates_to_trino(self, mock_trino_connect, connection_params):
        mock_trino_conn = mock_trino_connect.return_value
        conn = Connection(**connection_params)
        conn.close()

        mock_trino_conn.close.assert_called_once()

    def test_close_sets_closed_flag(self, mock_trino_connect, connection_params):
        conn = Connection(**connection_params)
        assert conn._closed is False
        conn.close()
        assert conn._closed is True

    def test_close_is_idempotent(self, mock_trino_connect, connection_params):
        mock_trino_conn = mock_trino_connect.return_value
        conn = Connection(**connection_params)
        conn.close()
        conn.close()
        conn.close()

        mock_trino_conn.close.assert_called_once()
