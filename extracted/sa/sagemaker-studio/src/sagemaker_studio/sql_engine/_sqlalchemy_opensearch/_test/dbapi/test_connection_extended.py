"""
Extended tests for OpenSearch DB-API Connection — covers branches
missed by test_connection.py.
"""

from unittest.mock import MagicMock, patch

import pytest

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection import Connection
from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import (
    OperationalError,
)


@pytest.fixture
def mock_connection():
    """Create a Connection with mocked OpenSearch client."""
    with patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient"
    ) as MockClient:
        mock_client_instance = MagicMock()
        mock_client_instance.client = MagicMock()
        MockClient.return_value = mock_client_instance
        conn = Connection(host="localhost", port=9200, index="test_index")
        yield conn


class TestConnectionExecuteSQLExtended:
    """Extended execute_sql tests."""

    def test_execute_sql_reraises_dbapi_error(self, mock_connection):
        """DB-API errors from client should be re-raised as-is."""
        mock_connection.client_manager.execute_sql.side_effect = OperationalError("db error")
        with pytest.raises(OperationalError, match="db error"):
            mock_connection.execute_sql("SELECT 1")

    def test_execute_sql_maps_non_dbapi_exception(self, mock_connection):
        """Non-DB-API exceptions should be mapped."""
        mock_connection.client_manager.execute_sql.side_effect = RuntimeError("unexpected")
        with pytest.raises(OperationalError):
            mock_connection.execute_sql("SELECT 1")


class TestConnectionWithAuth:
    """Test connection with authentication parameters."""

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient")
    def test_with_basic_auth(self, MockClient):
        MockClient.return_value = MagicMock()
        conn = Connection(
            host="es.example.com",
            port=443,
            index="logs",
            username="admin",
            password="secret",
        )
        assert conn.connection_params.username == "admin"
        assert conn.connection_params.password == "secret"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient")
    def test_with_api_key(self, MockClient):
        MockClient.return_value = MagicMock()
        conn = Connection(
            host="es.example.com",
            port=443,
            index="logs",
            api_key="mykey",
            api_key_id="myid",
        )
        assert conn.connection_params.api_key == "mykey"
        assert conn.connection_params.api_key_id == "myid"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient")
    def test_with_ssl_params(self, MockClient):
        MockClient.return_value = MagicMock()
        conn = Connection(
            host="es.example.com",
            port=443,
            index="logs",
            use_ssl=True,
            verify_certs=True,
            ca_certs="/path/ca.pem",
            client_cert="/path/cert.pem",
            client_key="/path/key.pem",
        )
        assert conn.connection_params.ca_certs == "/path/ca.pem"
        assert conn.connection_params.client_cert == "/path/cert.pem"
        assert conn.connection_params.client_key == "/path/key.pem"
