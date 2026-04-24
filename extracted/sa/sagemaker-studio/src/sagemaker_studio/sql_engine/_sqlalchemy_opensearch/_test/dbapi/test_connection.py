"""
Unit tests for OpenSearch DB-API Connection class.
"""

from unittest.mock import MagicMock, patch

import pytest

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection import Connection
from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.cursor import Cursor
from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import (
    DatabaseError,
    InterfaceError,
)


@pytest.fixture
def mock_connection():
    """Create a Connection with mocked OpenSearch client."""
    with patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient"
    ) as MockClient:
        mock_client_instance = MagicMock()
        mock_client_instance.client = MagicMock()
        mock_client_instance.get_connection_info.return_value = {"cluster_name": "test"}
        mock_client_instance.test_permissions.return_value = {"sql_query": True}
        MockClient.return_value = mock_client_instance

        conn = Connection(host="localhost", port=9200, index="test_index")
        yield conn


class TestConnectionInit:
    """Test Connection initialization."""

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient")
    def test_default_params(self, MockClient):
        MockClient.return_value = MagicMock()
        conn = Connection()
        assert conn.connection_params.host == "localhost"
        assert conn.connection_params.port == 443
        assert conn.connection_params.index == "_all"
        assert conn._closed is False
        assert conn.autocommit is True

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient")
    def test_custom_params(self, MockClient):
        MockClient.return_value = MagicMock()
        conn = Connection(host="es.example.com", port=443, index="logs")
        assert conn.connection_params.host == "es.example.com"
        assert conn.connection_params.port == 443
        assert conn.connection_params.index == "logs"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient")
    def test_creates_client_manager(self, MockClient):
        mock_instance = MagicMock()
        MockClient.return_value = mock_instance
        conn = Connection(host="localhost")
        assert conn.client_manager is mock_instance
        MockClient.assert_called_once()


class TestConnectionClient:
    """Test the client property."""

    def test_client_returns_client(self, mock_connection):
        client = mock_connection.client
        assert client is not None

    def test_client_raises_when_closed(self, mock_connection):
        mock_connection.close()
        with pytest.raises(InterfaceError, match="Connection is closed"):
            _ = mock_connection.client


class TestConnectionCursor:
    """Test cursor creation."""

    def test_cursor_returns_cursor_instance(self, mock_connection):
        cursor = mock_connection.cursor()
        assert isinstance(cursor, Cursor)

    def test_cursor_raises_when_closed(self, mock_connection):
        mock_connection.close()
        with pytest.raises(InterfaceError, match="Connection is closed"):
            mock_connection.cursor()


class TestConnectionTransactions:
    """Test commit/rollback (no-ops for OpenSearch)."""

    def test_commit_succeeds(self, mock_connection):
        mock_connection.commit()  # Should not raise

    def test_rollback_succeeds(self, mock_connection):
        mock_connection.rollback()  # Should not raise

    def test_commit_raises_when_closed(self, mock_connection):
        mock_connection.close()
        with pytest.raises(InterfaceError, match="Connection is closed"):
            mock_connection.commit()

    def test_rollback_raises_when_closed(self, mock_connection):
        mock_connection.close()
        with pytest.raises(InterfaceError, match="Connection is closed"):
            mock_connection.rollback()


class TestConnectionClose:
    """Test connection close behavior."""

    def test_close_sets_closed_flag(self, mock_connection):
        assert mock_connection.is_closed() is False
        mock_connection.close()
        assert mock_connection.is_closed() is True

    def test_close_calls_client_close(self, mock_connection):
        mock_connection.close()
        mock_connection.client_manager.close.assert_called_once()

    def test_double_close_is_safe(self, mock_connection):
        mock_connection.close()
        mock_connection.close()  # Should not raise
        # close on client_manager called only once
        mock_connection.client_manager.close.assert_called_once()


class TestConnectionInfo:
    """Test get_client_info and test_permissions."""

    def test_get_client_info(self, mock_connection):
        info = mock_connection.get_client_info()
        assert info == {"cluster_name": "test"}

    def test_get_client_info_raises_when_closed(self, mock_connection):
        mock_connection.close()
        with pytest.raises(InterfaceError, match="Connection is closed"):
            mock_connection.get_client_info()

    def test_test_permissions(self, mock_connection):
        perms = mock_connection.test_permissions()
        assert perms == {"sql_query": True}

    def test_test_permissions_raises_when_closed(self, mock_connection):
        mock_connection.close()
        with pytest.raises(InterfaceError, match="Connection is closed"):
            mock_connection.test_permissions()


class TestConnectionExecuteSQL:
    """Test execute_sql method."""

    def test_execute_sql_delegates_to_client(self, mock_connection):
        mock_connection.client_manager.execute_sql.return_value = {"schema": [], "datarows": []}
        result = mock_connection.execute_sql("SELECT 1")
        assert result == {"schema": [], "datarows": []}
        mock_connection.client_manager.execute_sql.assert_called_once_with("SELECT 1", None)

    def test_execute_sql_with_parameters(self, mock_connection):
        mock_connection.client_manager.execute_sql.return_value = {"schema": [], "datarows": []}
        mock_connection.execute_sql("SELECT :val", {"val": 1})
        mock_connection.client_manager.execute_sql.assert_called_once_with(
            "SELECT :val", {"val": 1}
        )

    def test_execute_sql_raises_when_closed(self, mock_connection):
        mock_connection.close()
        with pytest.raises(InterfaceError, match="Connection is closed"):
            mock_connection.execute_sql("SELECT 1")

    def test_execute_sql_maps_exceptions(self, mock_connection):
        mock_connection.client_manager.execute_sql.side_effect = RuntimeError("boom")
        with pytest.raises(DatabaseError):
            mock_connection.execute_sql("SELECT 1")
