"""Unit tests for Workday Data Connect authentication.

Tests DataServiceConfig validation and SDEAuth token lifecycle.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

import pytest

from ...dbapi.auth import DataServiceConfig, SDEAuth


@pytest.fixture
def valid_properties():
    return {
        "client_id": "test-client-id",
        "isu": "test-isu",
        "token_endpoint": "https://example.workday.com/oauth/token",
        "private_key": "-----BEGIN RSA PRIVATE KEY-----\nfake\n-----END RSA PRIVATE KEY-----",
        "host": "example.workday.com",
        "port": "443",
    }


@pytest.fixture
def config(valid_properties):
    return DataServiceConfig(valid_properties)


@pytest.fixture
def auth(config):
    return SDEAuth(config)


class TestDataServiceConfigValidation:
    """Test config validation rules."""

    def test_valid_config(self, valid_properties):
        config = DataServiceConfig(valid_properties)
        assert config.client_id == "test-client-id"

    def test_missing_client_id(self, valid_properties):
        del valid_properties["client_id"]
        with pytest.raises(ValueError, match="Missing required properties.*client_id"):
            DataServiceConfig(valid_properties)

    def test_missing_isu(self, valid_properties):
        del valid_properties["isu"]
        with pytest.raises(ValueError, match="Missing required properties.*isu"):
            DataServiceConfig(valid_properties)

    def test_missing_token_endpoint(self, valid_properties):
        del valid_properties["token_endpoint"]
        with pytest.raises(ValueError, match="Missing required properties.*token_endpoint"):
            DataServiceConfig(valid_properties)

    def test_missing_private_key(self, valid_properties):
        del valid_properties["private_key"]
        with pytest.raises(ValueError, match="private_key"):
            DataServiceConfig(valid_properties)

    def test_empty_client_id(self, valid_properties):
        valid_properties["client_id"] = ""
        with pytest.raises(ValueError, match="Missing required properties"):
            DataServiceConfig(valid_properties)

    def test_multiple_missing_fields(self):
        with pytest.raises(ValueError, match="Missing required properties"):
            DataServiceConfig({"private_key": "k"})


class TestDataServiceConfigProperties:
    """Test config property accessors."""

    def test_host_default(self):
        config = DataServiceConfig(
            {"client_id": "c", "isu": "i", "token_endpoint": "t", "private_key": "k"}
        )
        assert config.host == "localhost"

    def test_host_custom(self, valid_properties):
        config = DataServiceConfig(valid_properties)
        assert config.host == "example.workday.com"

    def test_port_default(self):
        config = DataServiceConfig(
            {"client_id": "c", "isu": "i", "token_endpoint": "t", "private_key": "k"}
        )
        assert config.port == 443

    def test_port_custom(self, valid_properties):
        valid_properties["port"] = "8443"
        config = DataServiceConfig(valid_properties)
        assert config.port == 8443

    def test_catalog_default(self, config):
        assert config.catalog == "workday_core"

    def test_catalog_custom(self, valid_properties):
        valid_properties["catalog"] = "my_catalog"
        config = DataServiceConfig(valid_properties)
        assert config.catalog == "my_catalog"

    def test_schema_default(self, config):
        assert config.schema == "public"

    def test_schema_custom(self, valid_properties):
        valid_properties["schema"] = "my_schema"
        config = DataServiceConfig(valid_properties)
        assert config.schema == "my_schema"

    def test_include_path_prefix_default(self, config):
        assert config.include_dataservice_path_prefix is True

    def test_include_path_prefix_true(self, valid_properties):
        valid_properties["include_path_prefix"] = "true"
        config = DataServiceConfig(valid_properties)
        assert config.include_dataservice_path_prefix is True

    def test_include_path_prefix_false(self, valid_properties):
        valid_properties["include_path_prefix"] = "false"
        config = DataServiceConfig(valid_properties)
        assert config.include_dataservice_path_prefix is False

    def test_include_path_prefix_yes(self, valid_properties):
        valid_properties["include_path_prefix"] = "yes"
        config = DataServiceConfig(valid_properties)
        assert config.include_dataservice_path_prefix is True

    def test_include_path_prefix_no(self, valid_properties):
        valid_properties["include_path_prefix"] = "no"
        config = DataServiceConfig(valid_properties)
        assert config.include_dataservice_path_prefix is False


class TestDataServiceConfigSessionProperties:
    """Test session properties parsing."""

    def test_empty_session_properties(self, config):
        assert config.session_properties == {}

    def test_single_property(self, valid_properties):
        valid_properties["session_properties"] = "key1:val1"
        config = DataServiceConfig(valid_properties)
        assert config.session_properties == {"key1": "val1"}

    def test_multiple_properties(self, valid_properties):
        valid_properties["session_properties"] = "key1:val1,key2:val2,key3:val3"
        config = DataServiceConfig(valid_properties)
        assert config.session_properties == {
            "key1": "val1",
            "key2": "val2",
            "key3": "val3",
        }

    def test_property_with_colon_in_value(self, valid_properties):
        valid_properties["session_properties"] = "url:http://example.com"
        config = DataServiceConfig(valid_properties)
        assert config.session_properties == {"url": "http://example.com"}

    def test_whitespace_trimmed(self, valid_properties):
        valid_properties["session_properties"] = " key1 : val1 , key2 : val2 "
        config = DataServiceConfig(valid_properties)
        assert config.session_properties == {"key1": "val1", "key2": "val2"}


class TestSDEAuthTokenLifecycle:
    """Test token acquisition and caching."""

    def test_initial_state(self, auth):
        assert auth._cached_token is None
        assert auth._token_expires_at is None

    def test_is_token_valid_when_no_token(self, auth):
        assert auth._is_token_valid() is False

    def test_is_token_valid_when_expired(self, auth):
        auth._cached_token = "old_token"
        auth._token_expires_at = datetime.now(timezone.utc) - timedelta(seconds=120)
        assert auth._is_token_valid() is False

    def test_is_token_valid_when_about_to_expire(self, auth):
        auth._cached_token = "expiring_token"
        # Within 60-second buffer
        auth._token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=30)
        assert auth._is_token_valid() is False

    def test_is_token_valid_when_fresh(self, auth):
        auth._cached_token = "fresh_token"
        auth._token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=3600)
        assert auth._is_token_valid() is True

    @patch("sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.requests.post")
    def test_refresh_token_posts_to_endpoint(self, mock_post, auth):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "new_token", "expires_in": 3600},
        )

        with patch(
            "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.jwt"
        ) as mock_jwt:
            mock_jwt.encode.return_value = "jwt_assertion"
            auth._refresh_token()

        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert call_kwargs[0][0] == "https://example.workday.com/oauth/token"
        assert "assertion" in call_kwargs[1]["data"]
        assert call_kwargs[1]["data"]["assertion"] == "jwt_assertion"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.requests.post")
    def test_refresh_token_stores_token(self, mock_post, auth):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "stored_token", "expires_in": 7200},
        )

        with patch(
            "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.jwt"
        ) as mock_jwt:
            mock_jwt.encode.return_value = "assertion"
            token = auth._refresh_token()

        assert token == "stored_token"
        assert auth._cached_token == "stored_token"
        assert auth._token_expires_at is not None

    @patch("sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.requests.post")
    def test_get_token_uses_cache(self, mock_post, auth):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "cached", "expires_in": 3600},
        )

        with patch(
            "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.jwt"
        ) as mock_jwt:
            mock_jwt.encode.return_value = "assertion"
            t1 = auth.get_token()
            t2 = auth.get_token()

        assert t1 == t2 == "cached"
        assert mock_post.call_count == 1

    @patch("sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.requests.post")
    def test_get_token_refreshes_when_expired(self, mock_post, auth):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "refreshed", "expires_in": 3600},
        )

        # Set expired token
        auth._cached_token = "old"
        auth._token_expires_at = datetime.now(timezone.utc) - timedelta(seconds=10)

        with patch(
            "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.jwt"
        ) as mock_jwt:
            mock_jwt.encode.return_value = "assertion"
            token = auth.get_token()

        assert token == "refreshed"
        mock_post.assert_called_once()


class TestSDEAuthSetHttpSession:
    """Test HTTP session configuration."""

    @patch("sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.requests.post")
    def test_set_http_session_sets_headers(self, mock_post, auth):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "token123", "expires_in": 3600},
        )

        http_session = Mock()
        http_session.headers = {}
        http_session.request = Mock()

        with patch(
            "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.jwt"
        ) as mock_jwt:
            mock_jwt.encode.return_value = "assertion"
            mock_jwt.decode.return_value = {"tenant": "test-tenant"}
            auth.set_http_session(http_session)

        assert http_session.headers["Authorization"] == "Bearer token123"
        assert http_session.headers["X-Tenant"] == "test-tenant"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.requests.post")
    def test_set_http_session_missing_tenant_raises(self, mock_post, auth):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "token123", "expires_in": 3600},
        )

        http_session = Mock()
        http_session.headers = {}

        with patch(
            "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.jwt"
        ) as mock_jwt:
            mock_jwt.encode.return_value = "assertion"
            mock_jwt.decode.return_value = {"tenant": ""}
            with pytest.raises(Exception, match="Tenant claim is missing"):
                auth.set_http_session(http_session)
