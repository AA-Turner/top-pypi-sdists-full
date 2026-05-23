"""Unit tests for the Workday Data Connect SQLAlchemy dialect."""

from unittest.mock import Mock, patch

import pytest
from sqlalchemy.engine import url as sa_url
from trino.sqlalchemy.dialect import TrinoDialect

from ..dbapi.auth import DataServiceConfig, SDEAuth
from ..dbapi.connection import Connection
from ..dbapi.cursor import Cursor
from ..dbapi.exceptions import (
    DatabaseError,
    Error,
    InterfaceError,
    OperationalError,
    ProgrammingError,
)
from ..dialect import WorkdayDataConnectDialect


class TestDialectRegistration:
    """Test dialect registration and basic properties."""

    def test_dialect_name_and_driver(self):
        dialect = WorkdayDataConnectDialect()
        assert dialect.name == "workday_data_connect"
        assert dialect.driver == "workday_data_connect"

    def test_dialect_inherits_from_trino_dialect(self):
        dialect = WorkdayDataConnectDialect()
        assert isinstance(dialect, TrinoDialect)

    def test_supports_statement_cache(self):
        dialect = WorkdayDataConnectDialect()
        assert dialect.supports_statement_cache is True

    def test_import_dbapi(self):
        dbapi = WorkdayDataConnectDialect.import_dbapi()
        assert hasattr(dbapi, "Connection")
        assert hasattr(dbapi, "Cursor")
        assert hasattr(dbapi, "Error")
        assert hasattr(dbapi, "connect")
        assert dbapi.apilevel == "2.0"
        assert dbapi.threadsafety == 2
        assert dbapi.paramstyle == "pyformat"

    def test_dialect_registers_with_sqlalchemy(self):
        from sqlalchemy.dialects import registry  # noqa: F401

        # The dialect should be registered via auto-import
        from .. import register_dialect

        register_dialect()
        # If no exception, registration succeeded


class TestCreateConnectArgs:
    """Test create_connect_args URL parsing."""

    def test_basic_url(self):
        dialect = WorkdayDataConnectDialect()
        url = sa_url.make_url(
            "workday_data_connect://example.workday.com:443"
            "?client_id=my-client&isu=my-isu"
            "&token_endpoint=https://token.example.com/oauth"
            "&private_key=FAKE_KEY"
        )

        args, kwargs = dialect.create_connect_args(url)

        assert args == []
        assert kwargs["host"] == "example.workday.com"
        assert kwargs["port"] == 443
        assert kwargs["client_id"] == "my-client"
        assert kwargs["isu"] == "my-isu"
        assert kwargs["token_endpoint"] == "https://token.example.com/oauth"
        assert kwargs["private_key"] == "FAKE_KEY"

    def test_default_host_and_port(self):
        dialect = WorkdayDataConnectDialect()
        url = sa_url.make_url(
            "workday_data_connect://" "?client_id=c&isu=i&token_endpoint=t&private_key=k"
        )

        args, kwargs = dialect.create_connect_args(url)

        assert kwargs["host"] == "localhost"
        assert kwargs["port"] == 443

    def test_include_path_prefix_param(self):
        dialect = WorkdayDataConnectDialect()
        url = sa_url.make_url(
            "workday_data_connect://host:443"
            "?client_id=c&isu=i&token_endpoint=t&private_key=k"
            "&include_path_prefix=false"
        )

        _, kwargs = dialect.create_connect_args(url)

        assert kwargs["include_path_prefix"] == "false"

    def test_session_properties_param(self):
        dialect = WorkdayDataConnectDialect()
        url = sa_url.make_url(
            "workday_data_connect://host:443"
            "?client_id=c&isu=i&token_endpoint=t&private_key=k"
            "&session_properties=key1:val1,key2:val2"
        )

        _, kwargs = dialect.create_connect_args(url)

        assert kwargs["session_properties"] == "key1:val1,key2:val2"

    def test_missing_auth_params_returns_empty_strings(self):
        dialect = WorkdayDataConnectDialect()
        url = sa_url.make_url("workday_data_connect://host:443")

        _, kwargs = dialect.create_connect_args(url)

        assert kwargs["client_id"] == ""
        assert kwargs["isu"] == ""
        assert kwargs["token_endpoint"] == ""
        assert kwargs["private_key"] == ""


class TestConnectMethod:
    """Test the dialect connect method."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.connection.trino.dbapi.connect"
    )
    def test_connect_creates_connection(self, mock_trino_connect):
        mock_trino_connect.return_value = Mock()

        dialect = WorkdayDataConnectDialect()
        conn = dialect.connect(
            host="example.com",
            port=443,
            client_id="cid",
            isu="isu",
            token_endpoint="https://token.example.com",
            private_key="-----BEGIN RSA PRIVATE KEY-----\nfake\n-----END RSA PRIVATE KEY-----",
        )

        assert isinstance(conn, Connection)
        mock_trino_connect.assert_called_once()


class TestDataServiceConfig:
    """Test DataServiceConfig validation and properties."""

    def _make_config(self, **overrides):
        props = {
            "client_id": "cid",
            "isu": "isu",
            "token_endpoint": "https://token.example.com",
            "private_key": "key",
            "host": "example.com",
            "port": "443",
        }
        props.update(overrides)
        return DataServiceConfig(props)

    def test_valid_config(self):
        config = self._make_config()
        assert config.client_id == "cid"
        assert config.isu == "isu"
        assert config.token_endpoint == "https://token.example.com"
        assert config.private_key == "key"
        assert config.host == "example.com"
        assert config.port == 443

    def test_missing_client_id_raises(self):
        with pytest.raises(ValueError, match="Missing required properties"):
            DataServiceConfig({"isu": "i", "token_endpoint": "t", "private_key": "k"})

    def test_missing_private_key_raises(self):
        with pytest.raises(ValueError, match="private_key"):
            DataServiceConfig({"client_id": "c", "isu": "i", "token_endpoint": "t"})

    def test_default_host(self):
        config = self._make_config()
        del config._properties["host"]
        assert config.host == "localhost"

    def test_default_port(self):
        config = self._make_config()
        del config._properties["port"]
        assert config.port == 443

    def test_default_catalog(self):
        config = self._make_config()
        assert config.catalog == "workday_core"

    def test_custom_catalog(self):
        config = self._make_config(catalog="my_catalog")
        assert config.catalog == "my_catalog"

    def test_default_schema(self):
        config = self._make_config()
        assert config.schema == "public"

    def test_include_dataservice_path_prefix_default_true(self):
        config = self._make_config()
        assert config.include_dataservice_path_prefix is True

    def test_include_dataservice_path_prefix_false(self):
        config = self._make_config(include_path_prefix="false")
        assert config.include_dataservice_path_prefix is False

    def test_session_properties_empty(self):
        config = self._make_config()
        assert config.session_properties == {}

    def test_session_properties_parsed(self):
        config = self._make_config(session_properties="key1:val1,key2:val2")
        assert config.session_properties == {"key1": "val1", "key2": "val2"}


class TestSDEAuth:
    """Test SDEAuth token management."""

    def _make_auth(self):
        config = DataServiceConfig(
            {
                "client_id": "cid",
                "isu": "isu",
                "token_endpoint": "https://token.example.com/oauth",
                "private_key": "-----BEGIN RSA PRIVATE KEY-----\nfake\n-----END RSA PRIVATE KEY-----",
                "host": "example.com",
                "port": "443",
            }
        )
        return SDEAuth(config)

    def test_initial_token_is_none(self):
        auth = self._make_auth()
        assert auth._cached_token is None
        assert auth._token_expires_at is None

    @patch("sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.requests.post")
    def test_refresh_token_success(self, mock_post):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "new_token", "expires_in": 3600},
        )

        auth = self._make_auth()
        # Patch jwt.encode at the module level where it's used
        with patch(
            "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.jwt"
        ) as mock_jwt:
            mock_jwt.encode.return_value = "fake_assertion"
            token = auth._refresh_token()

        assert token == "new_token"
        assert auth._cached_token == "new_token"
        assert auth._token_expires_at is not None
        mock_post.assert_called_once()

    @patch("sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.requests.post")
    def test_refresh_token_failure_raises(self, mock_post):
        from requests.exceptions import HTTPError

        mock_response = Mock(status_code=401)
        mock_response.raise_for_status.side_effect = HTTPError("Unauthorized")
        mock_post.return_value = mock_response

        auth = self._make_auth()
        with patch(
            "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.jwt"
        ) as mock_jwt:
            mock_jwt.encode.return_value = "fake_assertion"
            with pytest.raises(HTTPError):
                auth._refresh_token()

    @patch("sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.requests.post")
    def test_get_token_caches(self, mock_post):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "cached_token", "expires_in": 3600},
        )

        auth = self._make_auth()
        with patch(
            "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.auth.jwt"
        ) as mock_jwt:
            mock_jwt.encode.return_value = "fake_assertion"
            token1 = auth.get_token()
            token2 = auth.get_token()

        assert token1 == token2 == "cached_token"
        assert mock_post.call_count == 1  # Only called once due to caching


class TestConnection:
    """Test DB-API Connection class."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.connection.trino.dbapi.connect"
    )
    def test_connection_creates_trino_connection(self, mock_trino_connect):
        mock_trino_conn = Mock()
        mock_trino_connect.return_value = mock_trino_conn

        conn = Connection(
            host="example.com",
            port=443,
            client_id="cid",
            isu="isu",
            token_endpoint="https://token.example.com",
            private_key="key",
        )

        assert conn is not None
        mock_trino_connect.assert_called_once()
        call_kwargs = mock_trino_connect.call_args[1]
        assert call_kwargs["host"] == "example.com"
        assert call_kwargs["port"] == 443
        assert call_kwargs["catalog"] == "workday_core"
        assert call_kwargs["schema"] == "public"
        assert call_kwargs["http_scheme"] == "https"

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.connection.trino.dbapi.connect"
    )
    def test_cursor_returns_cursor_wrapper(self, mock_trino_connect):
        mock_trino_conn = Mock()
        mock_trino_connect.return_value = mock_trino_conn

        conn = Connection(
            host="h",
            port=443,
            client_id="c",
            isu="i",
            token_endpoint="t",
            private_key="k",
        )
        cursor = conn.cursor()

        assert isinstance(cursor, Cursor)
        mock_trino_conn.cursor.assert_called_once()

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.connection.trino.dbapi.connect"
    )
    def test_cursor_after_close_raises(self, mock_trino_connect):
        mock_trino_connect.return_value = Mock()

        conn = Connection(
            host="h",
            port=443,
            client_id="c",
            isu="i",
            token_endpoint="t",
            private_key="k",
        )
        conn.close()

        with pytest.raises(InterfaceError, match="Connection is closed"):
            conn.cursor()

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.connection.trino.dbapi.connect"
    )
    def test_close_is_idempotent(self, mock_trino_connect):
        mock_trino_conn = Mock()
        mock_trino_connect.return_value = mock_trino_conn

        conn = Connection(
            host="h",
            port=443,
            client_id="c",
            isu="i",
            token_endpoint="t",
            private_key="k",
        )
        conn.close()
        conn.close()

        mock_trino_conn.close.assert_called_once()


class TestCursor:
    """Test DB-API Cursor wrapper."""

    def test_delegates_execute(self):
        mock_cursor = Mock()
        cursor = Cursor(mock_cursor)
        cursor.execute("SELECT 1", {"p": 1})
        mock_cursor.execute.assert_called_once_with("SELECT 1", {"p": 1})

    def test_delegates_fetchall(self):
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [(1,), (2,)]
        cursor = Cursor(mock_cursor)
        assert cursor.fetchall() == [(1,), (2,)]

    def test_delegates_fetchone(self):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1,)
        cursor = Cursor(mock_cursor)
        assert cursor.fetchone() == (1,)

    def test_description_property(self):
        mock_cursor = Mock()
        mock_cursor.description = [("col1", "VARCHAR")]
        cursor = Cursor(mock_cursor)
        assert cursor.description == [("col1", "VARCHAR")]

    def test_rowcount_property(self):
        mock_cursor = Mock()
        mock_cursor.rowcount = 5
        cursor = Cursor(mock_cursor)
        assert cursor.rowcount == 5

    def test_close(self):
        mock_cursor = Mock()
        cursor = Cursor(mock_cursor)
        cursor.close()
        mock_cursor.close.assert_called_once()


class TestExceptions:
    """Test exception hierarchy."""

    def test_hierarchy(self):
        assert issubclass(InterfaceError, Error)
        assert issubclass(DatabaseError, Error)
        assert issubclass(OperationalError, DatabaseError)
        assert issubclass(ProgrammingError, DatabaseError)

    def test_error_is_exception(self):
        assert issubclass(Error, Exception)


class TestWorkdayTransformer:
    """Test the updated WorkdayTransformer integration."""

    def test_to_sqlalchemy_config_produces_correct_url(self):
        from ...workday_transformer import WorkdayTransformer

        config = WorkdayTransformer.to_sqlalchemy_config(
            {
                "host": "example.workday.com",
                "port": "443",
                "client_id": "my-client",
                "isu": "my-isu",
                "access_token_endpoint": "https://example.com/oauth/token",
                "private_key_file": "FAKE_KEY",
            }
        )

        assert "workday_data_connect://" in config["connection_string"]
        assert "example.workday.com:443" in config["connection_string"]
        assert "client_id=my-client" in config["connection_string"]
        assert "isu=my-isu" in config["connection_string"]
        assert config["connect_args"] == {}

    def test_required_fields_validation(self):
        from ...workday_transformer import WorkdayTransformer

        with pytest.raises(ValueError, match="host is required"):
            WorkdayTransformer.to_sqlalchemy_config(
                {
                    "port": "443",
                    "client_id": "c",
                    "isu": "i",
                    "access_token_endpoint": "t",
                    "private_key_file": "k",
                }
            )

    def test_get_dialect_returns_trino(self):
        from ...workday_transformer import WorkdayTransformer

        assert WorkdayTransformer.get_dialect() == "trino"
