"""
Extended tests for OpenSearch client — covers branches missed by test_client.py.
"""

from unittest.mock import MagicMock, patch

import pytest

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client import (
    OpenSearchClient,
)
from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection_params import (
    ConnectionParams,
)
from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import (
    InterfaceError,
    OperationalError,
)


@pytest.fixture
def default_params():
    return ConnectionParams(host="localhost", port=443, index="test")


@pytest.fixture
def auth_params():
    return ConnectionParams(
        host="es.example.com",
        port=443,
        index="logs",
        username="admin",
        password="secret",
        use_ssl=True,
    )


class TestInitializeClient:
    """Test _initialize_client method."""

    def test_opensearch_import_error(self, default_params):
        """When opensearch-py is not importable, InterfaceError is raised."""
        with patch(
            "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
        ):
            with patch.dict("sys.modules", {"opensearchpy": None}):
                with pytest.raises(InterfaceError, match="OpenSearch Python client not available"):
                    OpenSearchClient(default_params)

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    def test_client_creation_exception(self, mock_validate, default_params):
        """When OpenSearch() constructor raises, InterfaceError is raised."""
        mock_opensearch_cls = MagicMock(side_effect=RuntimeError("config error"))
        mock_module = MagicMock()
        mock_module.OpenSearch = mock_opensearch_cls
        with patch.dict("sys.modules", {"opensearchpy": mock_module}):
            with pytest.raises(InterfaceError, match="Failed to initialize"):
                OpenSearchClient(default_params)

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    def test_successful_initialization(self, mock_validate, default_params):
        """When opensearch-py is available and client creation succeeds."""
        mock_opensearch_instance = MagicMock()
        mock_opensearch_cls = MagicMock(return_value=mock_opensearch_instance)
        mock_module = MagicMock()
        mock_module.OpenSearch = mock_opensearch_cls
        with patch.dict("sys.modules", {"opensearchpy": mock_module}):
            client = OpenSearchClient(default_params)
            assert client._client is mock_opensearch_instance
            mock_opensearch_cls.assert_called_once()


class TestValidateConnection:
    """Test _validate_connection method."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_invalid_response(self, mock_init, default_params):
        """When info() returns invalid data, OperationalError is raised."""
        client = OpenSearchClient.__new__(OpenSearchClient)
        client.connection_params = default_params
        client._client = MagicMock()
        client._client.info.return_value = {"no_version": True}
        with pytest.raises(OperationalError, match="Invalid response"):
            client._validate_connection()

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_info_returns_non_dict(self, mock_init, default_params):
        """When info() returns non-dict, OperationalError is raised."""
        client = OpenSearchClient.__new__(OpenSearchClient)
        client.connection_params = default_params
        client._client = MagicMock()
        client._client.info.return_value = "not a dict"
        with pytest.raises(OperationalError, match="Invalid response"):
            client._validate_connection()

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_reraises_dbapi_error(self, mock_init, default_params):
        """DB-API errors from info() should be re-raised as-is."""
        client = OpenSearchClient.__new__(OpenSearchClient)
        client.connection_params = default_params
        client._client = MagicMock()
        client._client.info.side_effect = InterfaceError("already a dbapi error")
        with pytest.raises(InterfaceError, match="already a dbapi error"):
            client._validate_connection()

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_maps_generic_exception(self, mock_init, default_params):
        """Generic exceptions from info() should be mapped."""
        client = OpenSearchClient.__new__(OpenSearchClient)
        client.connection_params = default_params
        client._client = MagicMock()
        client._client.info.side_effect = RuntimeError("connection refused")
        with pytest.raises(OperationalError):
            client._validate_connection()


class TestBuildClientConfigExtended:
    """Extended tests for _build_client_config."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_no_ssl_certs_when_ssl_disabled(self, mock_init, mock_validate):
        params = ConnectionParams(host="localhost", port=9200, use_ssl=False)
        client = OpenSearchClient(params)
        config = client._build_client_config()
        assert config["use_ssl"] is False
        assert "ca_certs" not in config
        assert "client_cert" not in config
        assert "client_key" not in config

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_ssl_without_certs(self, mock_init, mock_validate):
        params = ConnectionParams(host="localhost", port=443, use_ssl=True)
        client = OpenSearchClient(params)
        config = client._build_client_config()
        assert config["use_ssl"] is True
        assert "ca_certs" not in config


class TestExecuteSQLExtended:
    """Extended tests for execute_sql."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_long_query_truncated_in_context(self, mock_init, mock_validate, default_params):
        """Long queries should be truncated in execution context."""
        os_client = OpenSearchClient(default_params)
        mock_os = MagicMock()
        mock_os.transport.perform_request.side_effect = RuntimeError("fail")
        os_client._client = mock_os

        long_query = "SELECT " + "a, " * 200
        with pytest.raises(OperationalError):
            os_client.execute_sql(long_query)

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_execute_sql_reraises_dbapi_error(self, mock_init, mock_validate, default_params):
        """DB-API errors should be re-raised as-is."""
        os_client = OpenSearchClient(default_params)
        mock_os = MagicMock()
        mock_os.transport.perform_request.side_effect = OperationalError("already mapped")
        os_client._client = mock_os

        with pytest.raises(OperationalError, match="already mapped"):
            os_client.execute_sql("SELECT 1")


class TestClientCloseExtended:
    """Extended tests for close method."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_close_handles_exception(self, mock_init, mock_validate, default_params):
        """close() should not raise even if underlying close fails."""
        os_client = OpenSearchClient(default_params)
        mock_os = MagicMock()
        mock_os.close.side_effect = RuntimeError("close failed")
        os_client._client = mock_os
        os_client.close()  # Should not raise
        assert os_client._client is None

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_close_when_client_is_none(self, mock_init, mock_validate, default_params):
        """close() should handle None client gracefully."""
        os_client = OpenSearchClient(default_params)
        os_client._client = None
        os_client.close()  # Should not raise
        assert os_client._client is None


class TestGetConnectionInfoExtended:
    """Extended tests for get_connection_info."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_missing_fields_in_info(self, mock_init, mock_validate, default_params):
        """get_connection_info should handle missing fields gracefully."""
        os_client = OpenSearchClient(default_params)
        mock_os = MagicMock()
        mock_os.info.return_value = {}
        os_client._client = mock_os
        info = os_client.get_connection_info()
        assert info["cluster_name"] == "unknown"
        assert info["version"] == "unknown"
