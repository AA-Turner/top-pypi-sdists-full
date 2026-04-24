"""
Unit tests for OpenSearch client management and authentication.
"""

from unittest.mock import MagicMock, patch

import pytest

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client import (
    OpenSearchClient,
    create_client,
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


@pytest.fixture
def api_key_params():
    return ConnectionParams(
        host="es.example.com",
        port=443,
        index="logs",
        api_key="mykey",
        api_key_id="myid",
        use_ssl=True,
    )


class TestOpenSearchClientInit:
    """Test OpenSearchClient initialization."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_stores_connection_params(self, mock_init_client, mock_validate, default_params):
        client = OpenSearchClient(default_params)
        assert client.connection_params is default_params

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_calls_initialize_and_validate(self, mock_init_client, mock_validate, default_params):
        OpenSearchClient(default_params)
        mock_init_client.assert_called_once()
        mock_validate.assert_called_once()


class TestBuildClientConfig:
    """Test _build_client_config."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_basic_config(self, mock_init, mock_validate, default_params):
        client = OpenSearchClient(default_params)
        config = client._build_client_config()
        assert config["hosts"] == [{"host": "localhost", "port": 443}]
        assert config["timeout"] == 30
        assert config["max_retries"] == 3
        assert config["use_ssl"] is True
        assert config["verify_certs"] is True
        assert "http_auth" not in config
        assert "api_key" not in config

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_basic_auth_config(self, mock_init, mock_validate, auth_params):
        client = OpenSearchClient(auth_params)
        config = client._build_client_config()
        assert config["http_auth"] == ("admin", "secret")
        assert config["use_ssl"] is True

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_api_key_config(self, mock_init, mock_validate, api_key_params):
        client = OpenSearchClient(api_key_params)
        config = client._build_client_config()
        assert config["api_key"] == ("myid", "mykey")
        assert "http_auth" not in config

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_ssl_cert_config(self, mock_init, mock_validate):
        params = ConnectionParams(
            host="es.example.com",
            port=443,
            use_ssl=True,
            ca_certs="/path/ca.pem",
            client_cert="/path/cert.pem",
            client_key="/path/key.pem",
        )
        client = OpenSearchClient(params)
        config = client._build_client_config()
        assert config["ca_certs"] == "/path/ca.pem"
        assert config["client_cert"] == "/path/cert.pem"
        assert config["client_key"] == "/path/key.pem"


class TestGetAuthMethodDescription:
    """Test _get_auth_method_description."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_basic_auth_description(self, mock_init, mock_validate, auth_params):
        client = OpenSearchClient(auth_params)
        desc = client._get_auth_method_description()
        assert "basic auth" in desc
        assert "admin" in desc

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_api_key_description(self, mock_init, mock_validate, api_key_params):
        client = OpenSearchClient(api_key_params)
        desc = client._get_auth_method_description()
        assert "API key" in desc
        assert "myid" in desc

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_no_auth_description(self, mock_init, mock_validate, default_params):
        client = OpenSearchClient(default_params)
        desc = client._get_auth_method_description()
        assert "no authentication" in desc


class TestClientProperty:
    """Test the client property."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_client_raises_when_none(self, mock_init, mock_validate, default_params):
        os_client = OpenSearchClient(default_params)
        os_client._client = None
        with pytest.raises(InterfaceError, match="Client not initialized"):
            _ = os_client.client

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_client_returns_client(self, mock_init, mock_validate, default_params):
        os_client = OpenSearchClient(default_params)
        mock_client = MagicMock()
        os_client._client = mock_client
        assert os_client.client is mock_client


class TestClientClose:
    """Test close method."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_close_sets_client_to_none(self, mock_init, mock_validate, default_params):
        os_client = OpenSearchClient(default_params)
        os_client._client = MagicMock()
        os_client.close()
        assert os_client._client is None


class TestGetConnectionInfo:
    """Test get_connection_info."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_returns_info(self, mock_init, mock_validate, default_params):
        os_client = OpenSearchClient(default_params)
        mock_os = MagicMock()
        mock_os.info.return_value = {
            "cluster_name": "my-cluster",
            "version": {"number": "2.11.0"},
        }
        os_client._client = mock_os
        info = os_client.get_connection_info()
        assert info["cluster_name"] == "my-cluster"
        assert info["version"] == "2.11.0"
        assert info["host"] == "localhost"

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_returns_error_on_failure(self, mock_init, mock_validate, default_params):
        os_client = OpenSearchClient(default_params)
        mock_os = MagicMock()
        mock_os.info.side_effect = RuntimeError("connection lost")
        os_client._client = mock_os
        info = os_client.get_connection_info()
        assert "error" in info


class TestTestPermissions:
    """Test test_permissions."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_all_permissions_pass(self, mock_init, mock_validate, default_params):
        os_client = OpenSearchClient(default_params)
        mock_os = MagicMock()
        mock_os.info.return_value = {}
        mock_os.cat.indices.return_value = []
        mock_os.transport.perform_request.return_value = {}
        os_client._client = mock_os

        perms = os_client.test_permissions()
        assert perms["cluster_info"] is True
        assert perms["list_indices"] is True
        assert perms["sql_query"] is True

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_permissions_fail_gracefully(self, mock_init, mock_validate, default_params):
        os_client = OpenSearchClient(default_params)
        mock_os = MagicMock()
        mock_os.info.side_effect = RuntimeError("denied")
        mock_os.cat.indices.side_effect = RuntimeError("denied")
        mock_os.transport.perform_request.side_effect = RuntimeError("denied")
        os_client._client = mock_os

        perms = os_client.test_permissions()
        assert perms["cluster_info"] is False
        assert perms["list_indices"] is False
        assert perms["sql_query"] is False


class TestExecuteSQL:
    """Test execute_sql."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_execute_sql_success(self, mock_init, mock_validate, default_params):
        os_client = OpenSearchClient(default_params)
        mock_os = MagicMock()
        mock_os.transport.perform_request.return_value = {"schema": [], "datarows": []}
        os_client._client = mock_os

        result = os_client.execute_sql("SELECT 1")
        assert result == {"schema": [], "datarows": []}
        mock_os.transport.perform_request.assert_called_once_with(
            "POST", "/_plugins/_sql", body={"query": "SELECT 1"}
        )

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_execute_sql_with_params(self, mock_init, mock_validate, default_params):
        os_client = OpenSearchClient(default_params)
        mock_os = MagicMock()
        mock_os.transport.perform_request.return_value = {}
        os_client._client = mock_os

        os_client.execute_sql("SELECT :v", {"v": 1})
        call_body = mock_os.transport.perform_request.call_args[1]["body"]
        assert call_body["query"] == "SELECT :v"
        assert call_body["parameters"] == {"v": 1}

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_execute_sql_maps_exception(self, mock_init, mock_validate, default_params):
        os_client = OpenSearchClient(default_params)
        mock_os = MagicMock()
        mock_os.transport.perform_request.side_effect = RuntimeError("query failed")
        os_client._client = mock_os

        with pytest.raises(OperationalError):
            os_client.execute_sql("BAD SQL")


class TestCreateClient:
    """Test create_client factory function."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._validate_connection"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.client.OpenSearchClient._initialize_client"
    )
    def test_returns_client_instance(self, mock_init, mock_validate, default_params):
        client = create_client(default_params)
        assert isinstance(client, OpenSearchClient)
