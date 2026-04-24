"""
Extended tests for OpenSearch connection params — covers branches
missed by test_connection_params.py.
"""

import pytest

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection_params import (
    ConnectionParams,
    parse_connection_url,
)
from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import InterfaceError


class TestConnectionParamsExtended:
    """Extended ConnectionParams tests."""

    def test_valid_index_with_wildcard(self):
        params = ConnectionParams(index="logs-*")
        assert params.index == "logs-*"

    def test_valid_index_with_dot(self):
        params = ConnectionParams(index=".kibana")
        assert params.index == ".kibana"

    def test_invalid_index_with_spaces(self):
        with pytest.raises(InterfaceError, match="index name must contain only"):
            ConnectionParams(index="invalid index")

    def test_invalid_index_with_special_chars(self):
        with pytest.raises(InterfaceError, match="index name must contain only"):
            ConnectionParams(index="index@name")

    def test_to_dict_with_api_key(self):
        params = ConnectionParams(
            host="localhost",
            port=443,
            api_key="mykey",
            api_key_id="myid",
        )
        d = params.to_dict()
        assert d["api_key"] == "mykey"
        assert d["api_key_id"] == "myid"

    def test_to_dict_with_ssl_certs(self):
        params = ConnectionParams(
            host="localhost",
            port=443,
            use_ssl=True,
            ca_certs="/path/ca.pem",
            client_cert="/path/cert.pem",
            client_key="/path/key.pem",
        )
        d = params.to_dict()
        assert d["ca_certs"] == "/path/ca.pem"
        assert d["client_cert"] == "/path/cert.pem"
        assert d["client_key"] == "/path/key.pem"

    def test_to_dict_minimal(self):
        params = ConnectionParams()
        d = params.to_dict()
        assert "username" not in d
        assert "password" not in d
        assert "ca_certs" not in d
        assert "client_cert" not in d
        assert "client_key" not in d
        assert "api_key" not in d
        assert "api_key_id" not in d

    def test_ssl_certs_without_ssl_ca_certs(self):
        with pytest.raises(InterfaceError, match="SSL certificate parameters"):
            ConnectionParams(use_ssl=False, ca_certs="/path/ca.pem")

    def test_ssl_certs_without_ssl_client_cert_key(self):
        with pytest.raises(InterfaceError, match="SSL certificate parameters"):
            ConnectionParams(
                use_ssl=False,
                client_cert="/path/cert.pem",
                client_key="/path/key.pem",
            )

    def test_max_retries_zero_is_valid(self):
        params = ConnectionParams(max_retries=0)
        assert params.max_retries == 0

    def test_port_boundary_values(self):
        params_min = ConnectionParams(port=1)
        assert params_min.port == 1
        params_max = ConnectionParams(port=65535)
        assert params_max.port == 65535


class TestParseConnectionUrlExtended:
    """Extended URL parsing tests."""

    def test_url_with_encoded_credentials(self):
        """URL-encoded special characters in credentials."""
        params = parse_connection_url("opensearch://user%40domain:p%40ss@localhost:9200/idx")
        assert params.username == "user@domain"
        assert params.password == "p@ss"

    def test_url_with_api_key_params(self):
        params = parse_connection_url(
            "opensearch://localhost:9200/idx?api_key=mykey&api_key_id=myid"
        )
        assert params.api_key == "mykey"
        assert params.api_key_id == "myid"

    def test_url_with_ssl_cert_params(self):
        params = parse_connection_url(
            "opensearch://localhost:9200/idx?ca_certs=/path/ca.pem"
            "&client_cert=/path/cert.pem&client_key=/path/key.pem"
        )
        assert params.ca_certs == "/path/ca.pem"
        assert params.client_cert == "/path/cert.pem"
        assert params.client_key == "/path/key.pem"

    def test_url_with_max_retries(self):
        params = parse_connection_url("opensearch://localhost:9200/idx?max_retries=5")
        assert params.max_retries == 5

    def test_url_invalid_integer_param(self):
        with pytest.raises(InterfaceError, match="Invalid integer value"):
            parse_connection_url("opensearch://localhost:9200/idx?timeout=abc")

    def test_url_invalid_max_retries(self):
        with pytest.raises(InterfaceError, match="Invalid integer value"):
            parse_connection_url("opensearch://localhost:9200/idx?max_retries=abc")

    def test_url_with_username_only_in_path(self):
        """URL with username but no password in path."""
        # This should parse username from path, but password will be None
        # which will fail validation
        with pytest.raises(InterfaceError, match="password is required"):
            parse_connection_url("opensearch://admin@localhost:9200/idx")

    def test_url_invalid_scheme_with_driver(self):
        with pytest.raises(InterfaceError, match="Invalid URL scheme"):
            parse_connection_url("mysql+driver://localhost:9200/idx")

    def test_url_no_path_no_host(self):
        """URL with just scheme and empty rest."""
        params = parse_connection_url("opensearch://")
        assert params.host == "localhost"
        assert params.index == "_all"

    def test_url_host_with_port_no_index(self):
        """URL with host:port but no index path defaults index to _all."""
        params = parse_connection_url("opensearch://myhost:9200")
        assert params.host == "myhost"
        assert params.port == 9200
        assert params.index == "_all"

    def test_url_empty_index_after_slash(self):
        """URL with trailing slash but no index defaults to _all."""
        params = parse_connection_url("opensearch://myhost:9200/")
        assert params.host == "myhost"
        assert params.port == 9200
        assert params.index == "_all"

    def test_url_empty_host_with_port(self):
        """URL with empty host but port specified defaults host to localhost."""
        params = parse_connection_url("opensearch://:9200/idx")
        assert params.host == "localhost"
        assert params.port == 9200
        assert params.index == "idx"
