"""
Tests for the OpenSearch dbapi __init__.py module — covers the connect() function
and module-level attributes.
"""

from unittest.mock import MagicMock, patch

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi import (
    apilevel,
    connect,
    paramstyle,
    threadsafety,
)


class TestDBAPIModuleAttributes:
    """Test DB-API 2.0 module-level attributes."""

    def test_apilevel(self):
        assert apilevel == "2.0"

    def test_threadsafety(self):
        assert threadsafety == 1

    def test_paramstyle(self):
        assert paramstyle == "named"


class TestDBAPIConnect:
    """Test the module-level connect() function."""

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient")
    def test_connect_default_params(self, MockClient):
        MockClient.return_value = MagicMock()
        conn = connect()
        assert conn is not None
        assert conn.connection_params.host == "localhost"
        assert conn.connection_params.port == 443
        assert conn.connection_params.index == "_all"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient")
    def test_connect_custom_params(self, MockClient):
        MockClient.return_value = MagicMock()
        conn = connect(host="es.example.com", port=9200, index="logs")
        assert conn.connection_params.host == "es.example.com"
        assert conn.connection_params.port == 9200
        assert conn.connection_params.index == "logs"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient")
    def test_connect_with_auth(self, MockClient):
        MockClient.return_value = MagicMock()
        conn = connect(
            host="es.example.com",
            port=443,
            index="logs",
            username="admin",
            password="secret",
        )
        assert conn.connection_params.username == "admin"
        assert conn.connection_params.password == "secret"
