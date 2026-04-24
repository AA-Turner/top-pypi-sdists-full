"""
Extended tests for OpenSearch SQLAlchemy dialect — covers branches
missed by test_dialect.py.
"""

from unittest.mock import MagicMock, patch

from sqlalchemy.engine.url import make_url

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dialect import (
    OpenSearchDialect,
    _version_tuple,
)


class TestVersionTuple:
    """Test the _version_tuple helper."""

    def test_standard_version(self):
        assert _version_tuple("2.0.0") == (2, 0, 0)

    def test_version_with_extra(self):
        assert _version_tuple("2.0.1") == (2, 0, 1)

    def test_version_comparison(self):
        assert _version_tuple("2.0.0") >= _version_tuple("1.4.0")
        assert _version_tuple("1.4.0") < _version_tuple("2.0.0")


class TestDialectDBAPI:
    """Test dbapi property and setter."""

    def test_dbapi_property_returns_module(self):
        dialect = OpenSearchDialect()
        dbapi = dialect.dbapi
        assert dbapi is not None
        assert hasattr(dbapi, "Connection")
        assert hasattr(dbapi, "Cursor")
        assert hasattr(dbapi, "Error")
        assert dbapi.apilevel == "2.0"
        assert dbapi.threadsafety == 1
        assert dbapi.paramstyle == "named"

    def test_dbapi_setter_ignores_none(self):
        dialect = OpenSearchDialect()
        original = dialect.dbapi
        dialect.dbapi = None
        # Should still return the original dbapi
        assert dialect.dbapi is original

    def test_dbapi_setter_accepts_module(self):
        dialect = OpenSearchDialect()
        mock_module = MagicMock()
        dialect.dbapi = mock_module
        assert dialect.dbapi is mock_module

    def test_import_dbapi_classmethod(self):
        module = OpenSearchDialect.import_dbapi()
        assert hasattr(module, "Connection")
        assert hasattr(module, "Cursor")
        assert hasattr(module, "Error")
        assert hasattr(module, "Warning")
        assert hasattr(module, "InterfaceError")
        assert hasattr(module, "DatabaseError")
        assert hasattr(module, "OperationalError")
        assert hasattr(module, "ProgrammingError")
        assert hasattr(module, "NotSupportedError")
        assert hasattr(module, "AuthenticationError")
        assert hasattr(module, "ConnectionError")  # Maps to OpenSearchConnectionError
        assert hasattr(module, "QueryExecutionError")
        assert hasattr(module, "InvalidParameterError")
        assert hasattr(module, "TransientError")


class TestCreateConnectArgs:
    """Test create_connect_args edge cases."""

    def test_no_host(self):
        dialect = OpenSearchDialect()
        url = make_url("opensearch:///my_index")
        _, kwargs = dialect.create_connect_args(url)
        assert kwargs["host"] == "localhost"
        assert kwargs["port"] == 443

    def test_no_database(self):
        dialect = OpenSearchDialect()
        url = make_url("opensearch://localhost:9200")
        _, kwargs = dialect.create_connect_args(url)
        assert kwargs["index"] == "_all"

    def test_ssl_string_false(self):
        dialect = OpenSearchDialect()
        url = make_url("opensearch://localhost:9200/idx?use_ssl=false&verify_certs=false")
        _, kwargs = dialect.create_connect_args(url)
        assert kwargs["use_ssl"] is False
        assert kwargs["verify_certs"] is False

    def test_ssl_string_true(self):
        dialect = OpenSearchDialect()
        url = make_url("opensearch://localhost:9200/idx?use_ssl=true&verify_certs=true")
        _, kwargs = dialect.create_connect_args(url)
        assert kwargs["use_ssl"] is True
        assert kwargs["verify_certs"] is True

    def test_ssl_string_yes(self):
        dialect = OpenSearchDialect()
        url = make_url("opensearch://localhost:9200/idx?use_ssl=yes&verify_certs=1")
        _, kwargs = dialect.create_connect_args(url)
        assert kwargs["use_ssl"] is True
        assert kwargs["verify_certs"] is True

    def test_with_timeout_and_retries_in_query(self):
        dialect = OpenSearchDialect()
        url = make_url("opensearch://localhost:9200/idx?timeout=60&max_retries=5")
        _, kwargs = dialect.create_connect_args(url)
        assert kwargs["timeout"] == 60
        assert kwargs["max_retries"] == 5

    def test_duplicate_query_param_takes_last(self):
        """When a query param is specified multiple times, the last value wins."""
        from sqlalchemy.engine.url import make_url

        dialect = OpenSearchDialect()
        # SQLAlchemy 2.0 stores repeated params as tuples
        url = make_url("opensearch://localhost:9200/idx?use_ssl=false&use_ssl=true")
        _, kwargs = dialect.create_connect_args(url)
        # Last value should be used
        assert kwargs["use_ssl"] is True

    def test_default_timeout_and_retries(self):
        dialect = OpenSearchDialect()
        url = make_url("opensearch://localhost:9200/idx")
        _, kwargs = dialect.create_connect_args(url)
        assert kwargs["timeout"] == 30
        assert kwargs["max_retries"] == 3


class TestDialectConnect:
    """Test the connect method."""

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient")
    def test_connect_creates_connection(self, MockClient):
        MockClient.return_value = MagicMock()
        dialect = OpenSearchDialect()
        conn = dialect.connect(host="localhost", port=9200, index="test")
        assert conn is not None

    def test_connect_fallback_to_dbapi_connection(self):
        """When both relative and absolute imports fail, uses dbapi.Connection."""
        import builtins

        dialect = OpenSearchDialect()
        original_import = builtins.__import__

        mock_connection = MagicMock()
        dialect._our_dbapi = MagicMock()
        dialect._our_dbapi.Connection = MagicMock(return_value=mock_connection)

        def failing_import(name, globals=None, locals=None, fromlist=(), level=0):
            if level != 0 and fromlist and "Connection" in fromlist:
                raise ImportError("relative import failed")
            if "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection" in name:
                raise ImportError("absolute import failed")
            return original_import(name, globals, locals, fromlist, level)

        with patch("builtins.__import__", side_effect=failing_import):
            result = dialect.connect(host="localhost", port=9200, index="test")
            assert result is mock_connection

    def test_import_dbapi_connect_function(self):
        """Test the inner connect function defined in import_dbapi."""
        dialect = OpenSearchDialect()
        dbapi_module = dialect.dbapi
        # The connect function is a plain function (not a method)
        assert hasattr(dbapi_module, "connect")
        assert callable(dbapi_module.connect)

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection.OpenSearchClient")
    def test_import_dbapi_connect_function_call(self, MockClient):
        """Test calling the inner connect function from import_dbapi."""
        MockClient.return_value = MagicMock()
        dialect = OpenSearchDialect()
        dbapi_module = dialect.dbapi
        # The connect function is a plain function (not a method)
        conn = dbapi_module.connect(host="localhost", port=9200, index="test")
        assert conn is not None


class TestDialectInitVersion:
    """Test dialect __init__ version check."""

    def test_old_sqlalchemy_raises(self):
        """When SQLAlchemy version is too old, ImportError is raised."""
        import pytest

        with patch(
            "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dialect.sqlalchemy_version",
            "1.4.0",
        ):
            with patch(
                "sagemaker_studio.sql_engine._sqlalchemy_opensearch.dialect._version_tuple",
                side_effect=lambda v: tuple(map(int, v.split(".")[:3])),
            ):
                with pytest.raises(ImportError, match="SQLAlchemy version"):
                    OpenSearchDialect()


class TestDialectMetadata:
    """Test dialect metadata methods."""

    def test_get_view_names_returns_empty(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        assert dialect.get_view_names(mock_conn) == []

    def test_get_indexes_returns_empty(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        assert dialect.get_indexes(mock_conn, "test_table") == []

    def test_get_foreign_keys_returns_empty(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        assert dialect.get_foreign_keys(mock_conn, "test_table") == []

    def test_get_pk_constraint(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        pk = dialect.get_pk_constraint(mock_conn, "test_table")
        assert pk["constrained_columns"] == ["_id"]
        assert pk["name"] is None

    def test_get_table_names_delegates_to_get_schema_names(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        mock_conn.execute.side_effect = Exception("fail")
        # Both should return empty on failure
        assert dialect.get_table_names(mock_conn) == []

    def test_get_schema_names_success(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        mock_conn.execute.return_value = [("index1",), ("index2",)]
        result = dialect.get_schema_names(mock_conn)
        assert result == ["index1", "index2"]

    def test_get_columns_success(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        mock_conn.execute.return_value = [
            ("id", "long"),
            ("name", "text"),
            ("active", "boolean"),
        ]
        columns = dialect.get_columns(mock_conn, "test_table")
        assert len(columns) == 3
        assert columns[0]["name"] == "id"
        assert columns[0]["nullable"] is True
        assert columns[0]["default"] is None
        assert columns[0]["autoincrement"] is False

    def test_get_columns_invalid_table_name(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        # Table name with special chars should return empty
        columns = dialect.get_columns(mock_conn, "table; DROP TABLE")
        assert columns == []

    def test_get_columns_hyphenated_table_name(self):
        """Hyphenated index names (e.g. logs-2024-01) should be quoted with backticks."""
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        mock_conn.execute.return_value = [("ts", "date")]
        columns = dialect.get_columns(mock_conn, "logs-2024-01")
        assert len(columns) == 1
        # Verify the query used backtick quoting
        executed_query = mock_conn.execute.call_args[0][0]
        assert "`logs-2024-01`" in str(executed_query.text)

    def test_get_column_type_all_types(self):
        dialect = OpenSearchDialect()
        # Test all mapped types
        assert dialect._get_column_type("text").__class__.__name__ == "Text"
        assert dialect._get_column_type("keyword").__class__.__name__ == "String"
        assert dialect._get_column_type("long").__class__.__name__ == "BigInteger"
        assert dialect._get_column_type("integer").__class__.__name__ == "Integer"
        assert dialect._get_column_type("short").__class__.__name__ == "SmallInteger"
        assert dialect._get_column_type("byte").__class__.__name__ == "SmallInteger"
        assert dialect._get_column_type("double").__class__.__name__ == "Float"
        assert dialect._get_column_type("float").__class__.__name__ == "Float"
        assert dialect._get_column_type("half_float").__class__.__name__ == "Float"
        assert dialect._get_column_type("scaled_float").__class__.__name__ == "Float"
        assert dialect._get_column_type("boolean").__class__.__name__ == "Boolean"
        assert dialect._get_column_type("date").__class__.__name__ == "DateTime"
        assert dialect._get_column_type("binary").__class__.__name__ == "LargeBinary"
        assert dialect._get_column_type("ip").__class__.__name__ == "String"
        assert dialect._get_column_type("geo_point").__class__.__name__ == "String"
        assert dialect._get_column_type("geo_shape").__class__.__name__ == "String"
        assert dialect._get_column_type("object").__class__.__name__ == "OBJECT"
        assert dialect._get_column_type("nested").__class__.__name__ == "NESTED"

    def test_get_column_type_unknown(self):
        dialect = OpenSearchDialect()
        assert dialect._get_column_type("unknown_type").__class__.__name__ == "Text"


class TestDialectServerVersion:
    """Test server version and default schema."""

    def test_get_server_version_info(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        assert dialect._get_server_version_info(mock_conn) == (2, 0, 0)

    def test_get_default_schema_name_from_connection(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        mock_conn.connection_params.index = "my_index"
        assert dialect._get_default_schema_name(mock_conn) == "my_index"

    def test_get_default_schema_name_no_connection_params(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock(spec=[])  # No attributes
        assert dialect._get_default_schema_name(mock_conn) == "_all"

    def test_get_default_schema_name_exception(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        mock_conn.connection_params = property(lambda self: (_ for _ in ()).throw(RuntimeError()))
        # Should fall back to _all
        assert dialect._get_default_schema_name(mock_conn) == "_all"


class TestDialectTransactions:
    """Test transaction no-ops."""

    def test_do_rollback(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        dialect.do_rollback(mock_conn)  # Should not raise

    def test_do_commit(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        dialect.do_commit(mock_conn)  # Should not raise

    def test_do_close(self):
        dialect = OpenSearchDialect()
        mock_conn = MagicMock()
        dialect.do_close(mock_conn)
        mock_conn.close.assert_called_once()


class TestRegisterDialect:
    """Test _register_dialect function."""

    def test_register_dialect_import_error(self):
        """When sqlalchemy.dialects is not importable, no error is raised."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dialect import _register_dialect

        with patch.dict("sys.modules", {"sqlalchemy.dialects": None}):
            # Should not raise
            _register_dialect()
