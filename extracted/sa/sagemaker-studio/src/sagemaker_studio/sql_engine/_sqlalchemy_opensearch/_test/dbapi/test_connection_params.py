"""
Unit tests for OpenSearch connection parameter parsing and validation.

Tests the ConnectionParams class and URL parsing functionality.
"""

import pytest

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection_params import (
    ConnectionParams,
    create_connection_params,
    parse_connection_url,
)
from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import InterfaceError


class TestConnectionParams:
    """Test cases for ConnectionParams class."""

    def test_connection_params_defaults(self):
        """Test ConnectionParams with default values."""
        params = ConnectionParams()

        assert params.host == "localhost"
        assert params.port == 443
        assert params.index == "_all"
        assert params.username is None
        assert params.password is None
        assert params.use_ssl is True
        assert params.max_retries == 3

    def test_connection_params_custom_values(self):
        """Test ConnectionParams with custom values."""
        params = ConnectionParams(
            host="example.com",
            port=9201,
            index="test_index",
            username="user",
            password="pass",
            use_ssl=True,
            verify_certs=False,
            timeout=60,
            max_retries=5,
        )

        assert params.host == "example.com"
        assert params.port == 9201
        assert params.index == "test_index"
        assert params.username == "user"
        assert params.password == "pass"
        assert params.use_ssl is True
        assert params.verify_certs is False
        assert params.timeout == 60
        assert params.max_retries == 5

    def test_connection_params_validation_invalid_port(self):
        """Test validation of invalid port numbers."""
        with pytest.raises(InterfaceError, match="port must be between 1 and 65535"):
            ConnectionParams(port=0)

        with pytest.raises(InterfaceError, match="port must be between 1 and 65535"):
            ConnectionParams(port=65536)

    def test_connection_params_validation_invalid_timeout(self):
        """Test validation of invalid timeout values."""
        with pytest.raises(InterfaceError, match="timeout must be positive"):
            ConnectionParams(timeout=0)

        with pytest.raises(InterfaceError, match="timeout must be positive"):
            ConnectionParams(timeout=-1)

    def test_connection_params_validation_invalid_max_retries(self):
        """Test validation of invalid max_retries values."""
        with pytest.raises(InterfaceError, match="max_retries must be non-negative"):
            ConnectionParams(max_retries=-1)

    def test_connection_params_validation_empty_host(self):
        """Test validation of empty host."""
        with pytest.raises(InterfaceError, match="host cannot be empty"):
            ConnectionParams(host="")

    def test_connection_params_validation_auth_combinations(self):
        """Test validation of authentication parameter combinations."""
        # Username without password should fail
        with pytest.raises(InterfaceError, match="password is required when username is provided"):
            ConnectionParams(username="user")

        # Password without username should fail
        with pytest.raises(InterfaceError, match="username is required when password is provided"):
            ConnectionParams(password="pass")

        # API key without API key ID should fail
        with pytest.raises(InterfaceError, match="api_key_id is required when api_key is provided"):
            ConnectionParams(api_key="key123")

        # API key ID without API key should fail
        with pytest.raises(InterfaceError, match="api_key is required when api_key_id is provided"):
            ConnectionParams(api_key_id="id123")

        # Both basic auth and API key auth should fail
        with pytest.raises(
            InterfaceError, match="Cannot specify both basic auth and API key authentication"
        ):
            ConnectionParams(username="user", password="pass", api_key="key", api_key_id="id")

    def test_connection_params_validation_ssl_combinations(self):
        """Test validation of SSL parameter combinations."""
        # Client cert without client key should fail
        with pytest.raises(
            InterfaceError, match="client_key is required when client_cert is provided"
        ):
            ConnectionParams(client_cert="/path/to/cert.pem")

        # Client key without client cert should fail
        with pytest.raises(
            InterfaceError, match="client_cert is required when client_key is provided"
        ):
            ConnectionParams(client_key="/path/to/key.pem")

        # SSL params without use_ssl should fail
        with pytest.raises(
            InterfaceError, match="SSL certificate parameters.*can only be used when use_ssl=True"
        ):
            ConnectionParams(ca_certs="/path/to/ca.pem", use_ssl=False)

    def test_connection_params_to_dict(self):
        """Test conversion to dictionary."""
        params = ConnectionParams(
            host="example.com",
            port=9201,
            index="test_index",
            username="user",
            password="pass",
            use_ssl=True,
        )

        result = params.to_dict()

        assert result["host"] == "example.com"
        assert result["port"] == 9201
        assert result["index"] == "test_index"
        assert result["username"] == "user"
        assert result["password"] == "pass"
        assert result["use_ssl"] is True
        assert result["verify_certs"] is True  # Default value


class TestParseConnectionUrl:
    """Test cases for parse_connection_url function."""

    def test_parse_basic_url(self):
        """Test parsing of basic URL."""
        params = parse_connection_url("opensearch://localhost:9200/test_index")

        assert params.host == "localhost"
        assert params.port == 9200
        assert params.index == "test_index"
        assert params.username is None
        assert params.password is None

    def test_parse_url_with_auth(self):
        """Test parsing of URL with authentication."""
        params = parse_connection_url("opensearch://user:pass@localhost:9200/test_index")

        assert params.host == "localhost"
        assert params.port == 9200
        assert params.index == "test_index"
        assert params.username == "user"
        assert params.password == "pass"

    def test_parse_url_with_query_params(self):
        """Test parsing of URL with query parameters."""
        params = parse_connection_url(
            "opensearch://localhost:9200/test_index?use_ssl=true&verify_certs=false&timeout=60"
        )

        assert params.host == "localhost"
        assert params.port == 9200
        assert params.index == "test_index"
        assert params.use_ssl is True
        assert params.verify_certs is False
        assert params.timeout == 60

    def test_parse_url_defaults(self):
        """Test parsing of URL with defaults."""
        params = parse_connection_url("opensearch:///test_index")

        assert params.host == "localhost"
        assert params.port == 443
        assert params.index == "test_index"

    def test_parse_url_no_index(self):
        """Test parsing of URL without index."""
        params = parse_connection_url("opensearch://localhost")

        assert params.host == "localhost"
        assert params.port == 443
        assert params.index == "_all"

    def test_parse_url_sqlalchemy_driver_format(self):
        """Test parsing of SQLAlchemy driver format URL."""
        params = parse_connection_url("opensearch+opensearch://localhost:9200/test_index")

        assert params.host == "localhost"
        assert params.port == 9200
        assert params.index == "test_index"

    def test_parse_url_invalid_scheme(self):
        """Test parsing of URL with invalid scheme."""
        with pytest.raises(InterfaceError, match="Invalid URL scheme"):
            parse_connection_url("mysql://localhost:3306/test")

    def test_parse_url_missing_scheme(self):
        """Test parsing of URL without scheme."""
        with pytest.raises(InterfaceError, match="Invalid URL format: missing"):
            parse_connection_url("localhost:9200/test_index")

    def test_parse_url_empty(self):
        """Test parsing of empty URL."""
        with pytest.raises(InterfaceError, match="Connection URL cannot be empty"):
            parse_connection_url("")

    def test_parse_url_invalid_port(self):
        """Test parsing of URL with invalid port."""
        with pytest.raises(InterfaceError, match="Invalid port number"):
            parse_connection_url("opensearch://localhost:abc/test_index")

    def test_parse_url_boolean_params(self):
        """Test parsing of boolean query parameters."""
        # Test various boolean representations
        params = parse_connection_url("opensearch://localhost:9200/test?use_ssl=1&verify_certs=yes")
        assert params.use_ssl is True
        assert params.verify_certs is True

        params = parse_connection_url("opensearch://localhost:9200/test?use_ssl=0&verify_certs=no")
        assert params.use_ssl is False
        assert params.verify_certs is False

        params = parse_connection_url(
            "opensearch://localhost:9200/test?use_ssl=on&verify_certs=off"
        )
        assert params.use_ssl is True
        assert params.verify_certs is False

    def test_parse_url_invalid_boolean(self):
        """Test parsing of URL with invalid boolean parameter."""
        with pytest.raises(InterfaceError, match="Invalid boolean value"):
            parse_connection_url("opensearch://localhost:9200/test?use_ssl=maybe")

    def test_parse_url_duplicate_params(self):
        """Test parsing of URL with duplicate parameters."""
        with pytest.raises(InterfaceError, match="Parameter.*specified multiple times"):
            parse_connection_url("opensearch://localhost:9200/test?use_ssl=true&use_ssl=false")

    def test_parse_url_auth_override(self):
        """Test that query parameters can override URL auth."""
        params = parse_connection_url(
            "opensearch://user1:pass1@localhost:9200/test?username=user2&password=pass2"
        )

        # Query parameters should take precedence
        assert params.username == "user2"
        assert params.password == "pass2"


class TestCreateConnectionParams:
    """Test cases for create_connection_params function."""

    def test_create_connection_params_basic(self):
        """Test creating connection params from kwargs."""
        params = create_connection_params(
            host="example.com",
            port=9201,
            index="test_index",
            username="user",
            password="pass",
        )

        assert params.host == "example.com"
        assert params.port == 9201
        assert params.index == "test_index"
        assert params.username == "user"
        assert params.password == "pass"

    def test_create_connection_params_validation(self):
        """Test that create_connection_params validates parameters."""
        with pytest.raises(InterfaceError):
            create_connection_params(port=0)  # Invalid port should raise error
