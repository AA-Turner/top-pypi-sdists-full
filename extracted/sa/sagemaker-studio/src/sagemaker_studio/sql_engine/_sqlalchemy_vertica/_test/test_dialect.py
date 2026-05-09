"""
Unit tests for VerticaDialect.

Tests the custom SQLAlchemy 2.0 dialect for Vertica databases.
"""

import sys
from unittest.mock import MagicMock, Mock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import SQLAlchemyError

# Mock vertica_python if not installed, using patch.dict for safe restoration
_need_mock = "vertica_python" not in sys.modules
_patcher = patch.dict(sys.modules, {"vertica_python": MagicMock()}) if _need_mock else None

if _patcher:
    _patcher.start()

from ..dialect import VerticaDialect  # noqa: E402


@pytest.fixture(autouse=True, scope="module")
def _cleanup_vertica_mock():
    yield
    if _patcher:
        _patcher.stop()


class TestVerticaDialect:
    """Test suite for VerticaDialect."""

    def test_dialect_name(self):
        """Test that dialect has correct name."""
        dialect = VerticaDialect()
        assert dialect.name == "vertica"

    def test_dialect_driver(self):
        """Test that dialect has correct driver."""
        dialect = VerticaDialect()
        assert dialect.driver == "vertica_python"

    def test_supports_statement_cache(self):
        """Test that statement caching is enabled."""
        dialect = VerticaDialect()
        assert dialect.supports_statement_cache is True

    def test_supports_sane_rowcount(self):
        """Test that rowcount is supported."""
        dialect = VerticaDialect()
        assert dialect.supports_sane_rowcount is True

    def test_supports_sequences_false(self):
        """Test that sequences are not supported (Vertica limitation)."""
        dialect = VerticaDialect()
        assert dialect.supports_sequences is False

    def test_import_dbapi(self):
        """Test that import_dbapi returns vertica_python module."""
        dbapi = VerticaDialect.import_dbapi()
        # Should return the vertica_python module (or mock in test environment)
        assert dbapi is not None
        assert hasattr(dbapi, "__name__") or isinstance(dbapi, MagicMock)

    def test_create_connect_args_basic(self):
        """Test basic connection argument creation."""
        dialect = VerticaDialect()
        url = make_url("vertica+vertica_python://user:pass@host:5433/db")

        args, kwargs = dialect.create_connect_args(url)

        assert args == []
        assert kwargs["host"] == "host"
        assert kwargs["port"] == 5433
        assert kwargs["user"] == "user"
        assert kwargs["password"] == "pass"
        assert kwargs["database"] == "db"

    def test_create_connect_args_missing_host(self):
        """Test that missing host raises ValueError."""
        dialect = VerticaDialect()
        url = make_url("vertica+vertica_python://user:pass@/db")

        with pytest.raises(ValueError, match="Host is required"):
            dialect.create_connect_args(url)

    def test_create_connect_args_with_default_port(self):
        """Test connection arguments with default port."""
        dialect = VerticaDialect()
        url = make_url("vertica+vertica_python://user:pass@host/db")

        args, kwargs = dialect.create_connect_args(url)

        assert kwargs["host"] == "host"
        assert kwargs["port"] == 5433

    def test_create_connect_args_with_query_params(self):
        """Test connection arguments with query parameters."""
        dialect = VerticaDialect()
        url = make_url("vertica+vertica_python://user:pass@host:5433/db?connection_timeout=30")

        args, kwargs = dialect.create_connect_args(url)

        assert kwargs["connection_timeout"] == "30"

    def test_get_server_version_info(self):
        """Test server version retrieval."""
        dialect = VerticaDialect()

        # Mock connection
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.scalar.return_value = "Vertica Analytic Database v11.0.1-0"
        mock_connection.execute.return_value = mock_result

        version = dialect._get_server_version_info(mock_connection)

        assert version == (11, 0, 1)

    def test_get_server_version_info_fallback(self):
        """Test server version raises on error."""
        dialect = VerticaDialect()

        # Mock connection that raises error
        mock_connection = Mock()
        mock_connection.execute.side_effect = SQLAlchemyError("Connection error")

        with pytest.raises(RuntimeError, match="Failed to retrieve Vertica server version"):
            dialect._get_server_version_info(mock_connection)

    def test_get_default_schema_name(self):
        """Test default schema name retrieval."""
        dialect = VerticaDialect()

        # Mock connection
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.scalar.return_value = "public"
        mock_connection.execute.return_value = mock_result

        schema = dialect._get_default_schema_name(mock_connection)

        assert schema == "public"

    def test_get_default_schema_name_fallback(self):
        """Test default schema name fallback."""
        dialect = VerticaDialect()

        # Mock connection that raises error
        mock_connection = Mock()
        mock_connection.execute.side_effect = SQLAlchemyError("Connection error")

        schema = dialect._get_default_schema_name(mock_connection)

        assert schema == "public"

    def test_do_rollback(self):
        """Test transaction rollback."""
        dialect = VerticaDialect()
        mock_connection = Mock()

        dialect.do_rollback(mock_connection)

        mock_connection.rollback.assert_called_once()

    def test_do_commit(self):
        """Test transaction commit."""
        dialect = VerticaDialect()
        mock_connection = Mock()

        dialect.do_commit(mock_connection)

        mock_connection.commit.assert_called_once()

    def test_do_close(self):
        """Test connection close."""
        dialect = VerticaDialect()
        mock_connection = Mock()

        dialect.do_close(mock_connection)

        mock_connection.close.assert_called_once()

    def test_get_schema_names(self):
        """Test schema name retrieval."""
        dialect = VerticaDialect()

        # Mock connection
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.__iter__ = Mock(
            return_value=iter([("public",), ("myschema",), ("testschema",)])
        )
        mock_connection.execute.return_value = mock_result

        schemas = dialect.get_schema_names(mock_connection)

        assert schemas == ["public", "myschema", "testschema"]

    def test_get_table_names(self):
        """Test table name retrieval."""
        dialect = VerticaDialect()

        # Mock connection
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.__iter__ = Mock(return_value=iter([("users",), ("orders",), ("products",)]))
        mock_connection.execute.return_value = mock_result

        tables = dialect.get_table_names(mock_connection, schema="public")

        assert tables == ["users", "orders", "products"]

    def test_get_view_names(self):
        """Test view name retrieval."""
        dialect = VerticaDialect()

        # Mock connection
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.__iter__ = Mock(return_value=iter([("user_view",), ("order_summary",)]))
        mock_connection.execute.return_value = mock_result

        views = dialect.get_view_names(mock_connection, schema="public")

        assert views == ["user_view", "order_summary"]

    def test_get_columns(self):
        """Test column metadata retrieval."""
        dialect = VerticaDialect()

        # Mock connection
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.__iter__ = Mock(
            return_value=iter(
                [
                    ("id", "integer", True, None, None, None, None, 1),
                    ("name", "varchar", False, None, 255, None, None, 2),
                    ("age", "integer", True, None, None, None, None, 3),
                ]
            )
        )
        mock_connection.execute.return_value = mock_result

        columns = dialect.get_columns(mock_connection, "users", schema="public")

        assert len(columns) == 3
        assert columns[0]["name"] == "id"
        assert columns[1]["name"] == "name"
        assert columns[2]["name"] == "age"

    def test_get_column_type_integer(self):
        """Test integer type mapping."""
        dialect = VerticaDialect()

        col_type = dialect._get_column_type("integer")

        assert col_type.__class__.__name__ == "Integer"

    def test_get_column_type_varchar(self):
        """Test varchar type mapping with length."""
        dialect = VerticaDialect()

        col_type = dialect._get_column_type("varchar", char_max_length=255)

        assert col_type.__class__.__name__ == "VARCHAR"
        assert col_type.length == 255

    def test_get_column_type_decimal(self):
        """Test decimal type mapping with precision and scale."""
        dialect = VerticaDialect()

        col_type = dialect._get_column_type("decimal", numeric_precision=10, numeric_scale=2)

        assert col_type.__class__.__name__ == "Numeric"

    def test_get_column_type_unknown(self):
        """Test unknown type defaults to Text."""
        dialect = VerticaDialect()

        col_type = dialect._get_column_type("unknown_type")

        assert col_type.__class__.__name__ == "Text"

    def test_get_indexes_returns_empty(self):
        """Test that get_indexes returns empty list (Vertica uses projections)."""
        dialect = VerticaDialect()
        mock_connection = Mock()

        indexes = dialect.get_indexes(mock_connection, "users", schema="public")

        assert indexes == []

    def test_get_pk_constraint(self):
        """Test primary key constraint retrieval."""
        dialect = VerticaDialect()

        # Mock connection
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.__iter__ = Mock(
            return_value=iter(
                [
                    ("id",),
                ]
            )
        )
        mock_connection.execute.return_value = mock_result

        pk = dialect.get_pk_constraint(mock_connection, "users", schema="public")

        assert pk["constrained_columns"] == ["id"]

    def test_get_pk_constraint_none(self):
        """Test primary key constraint when none exists."""
        dialect = VerticaDialect()

        # Mock connection with no results
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.__iter__ = Mock(return_value=iter([]))
        mock_connection.execute.return_value = mock_result

        pk = dialect.get_pk_constraint(mock_connection, "users", schema="public")

        assert pk["constrained_columns"] == []

    def test_get_foreign_keys(self):
        """Test foreign key retrieval."""
        dialect = VerticaDialect()

        # Mock connection
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.__iter__ = Mock(
            return_value=iter(
                [
                    ("user_id", "public", "users", "id", "fk_user"),
                ]
            )
        )
        mock_connection.execute.return_value = mock_result

        fks = dialect.get_foreign_keys(mock_connection, "orders", schema="public")

        assert len(fks) == 1
        assert fks[0]["constrained_columns"] == ["user_id"]
        assert fks[0]["referred_table"] == "users"
        assert fks[0]["referred_columns"] == ["id"]

    def test_has_table_true(self):
        """Test has_table returns True when table exists."""
        dialect = VerticaDialect()

        # Mock connection
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.scalar.return_value = 1
        mock_connection.execute.return_value = mock_result

        exists = dialect.has_table(mock_connection, "users", schema="public")

        assert exists is True

    def test_has_table_false(self):
        """Test has_table returns False when table doesn't exist."""
        dialect = VerticaDialect()

        # Mock connection
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.scalar.return_value = 0
        mock_connection.execute.return_value = mock_result

        exists = dialect.has_table(mock_connection, "nonexistent", schema="public")

        assert exists is False

    def test_has_sequence_always_false(self):
        """Test has_sequence always returns False (Vertica doesn't support sequences)."""
        dialect = VerticaDialect()
        mock_connection = Mock()

        exists = dialect.has_sequence(mock_connection, "seq_name", schema="public")

        assert exists is False

    def test_get_sequence_names_empty(self):
        """Test get_sequence_names returns empty list (Vertica doesn't support sequences)."""
        dialect = VerticaDialect()
        mock_connection = Mock()

        sequences = dialect.get_sequence_names(mock_connection, schema="public")

        assert sequences == []


class TestVerticaDialectIntegration:
    """Integration tests for VerticaDialect with SQLAlchemy."""

    def test_dialect_registration(self):
        """Test that dialect is registered with SQLAlchemy."""
        from sqlalchemy.dialects import registry

        # Import to trigger registration
        from .. import register_dialect

        register_dialect()

        # Try to load the dialect
        dialect_cls = registry.load("vertica.vertica_python")

        assert dialect_cls == VerticaDialect

    def test_create_engine_with_dialect(self):
        """Test creating engine with Vertica dialect."""
        # Import to trigger registration
        from .. import register_dialect

        register_dialect()

        # Create engine (won't actually connect)
        engine = create_engine("vertica+vertica_python://user:pass@host:5433/db")

        assert engine.dialect.name == "vertica"
        assert engine.dialect.driver == "vertica_python"

    def test_engine_connect(self):
        """Test engine connection setup with Vertica dialect."""
        # Import to trigger registration
        from .. import register_dialect

        register_dialect()

        # Create engine (won't actually connect)
        engine = create_engine("vertica+vertica_python://user:pass@host:5433/db")

        # Verify engine is configured correctly
        assert engine.dialect.name == "vertica"
        assert engine.dialect.driver == "vertica_python"
        assert engine.url.username == "user"
        assert engine.url.password == "pass"
        assert engine.url.host == "host"
        assert engine.url.port == 5433
        assert engine.url.database == "db"

    def test_url_parsing(self):
        """Test URL parsing for various connection string formats."""
        from .. import register_dialect

        register_dialect()

        # Test basic URL
        engine = create_engine("vertica+vertica_python://user:pass@host:5433/db")
        assert engine.url.username == "user"
        assert engine.url.password == "pass"
        assert engine.url.host == "host"
        assert engine.url.port == 5433
        assert engine.url.database == "db"

        # Test URL with query parameters
        engine = create_engine(
            "vertica+vertica_python://user:pass@host:5433/db?connection_timeout=30"
        )
        assert engine.url.query.get("connection_timeout") == "30"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
