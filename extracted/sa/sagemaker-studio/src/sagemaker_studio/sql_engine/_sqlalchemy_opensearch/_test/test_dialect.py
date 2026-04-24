"""
Unit tests for OpenSearch SQLAlchemy dialect.

Tests the core dialect functionality including URL parsing,
connection creation, and dialect-specific features.
"""

import pytest

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dialect import OpenSearchDialect


class TestOpenSearchDialect:
    """Test cases for OpenSearchDialect class."""

    def test_dialect_name(self):
        """Test that dialect has correct name."""
        dialect = OpenSearchDialect()
        assert dialect.name == "opensearch"
        assert dialect.driver == "opensearch"

    def test_dialect_features(self):
        """Test dialect feature flags."""
        dialect = OpenSearchDialect()

        # OpenSearch-specific features
        assert dialect.supports_statement_cache is True
        assert dialect.supports_sane_rowcount is True

        # Features not supported by OpenSearch
        assert dialect.supports_sane_multi_rowcount is False
        assert dialect.supports_sequences is False
        assert dialect.supports_empty_insert is False
        assert dialect.supports_multivalues_insert is False
        assert dialect.supports_alter is False
        assert dialect.supports_foreign_keys is False
        assert dialect.supports_pk_autoincrement is False

    def test_create_connect_args_basic(self):
        """Test basic URL parsing."""
        from sqlalchemy.engine.url import make_url

        dialect = OpenSearchDialect()
        url = make_url("opensearch://localhost:9200/test_index")

        args, kwargs = dialect.create_connect_args(url)

        assert args == []
        assert kwargs["host"] == "localhost"
        assert kwargs["port"] == 9200
        assert kwargs["index"] == "test_index"

    def test_create_connect_args_with_auth(self):
        """Test URL parsing with authentication."""
        from sqlalchemy.engine.url import make_url

        dialect = OpenSearchDialect()
        url = make_url("opensearch://user:pass@localhost:9200/test_index")

        args, kwargs = dialect.create_connect_args(url)

        assert kwargs["username"] == "user"
        assert kwargs["password"] == "pass"
        assert kwargs["host"] == "localhost"
        assert kwargs["port"] == 9200

    def test_create_connect_args_with_ssl(self):
        """Test URL parsing with SSL parameters."""
        from sqlalchemy.engine.url import make_url

        dialect = OpenSearchDialect()
        url = make_url("opensearch://localhost:9200/test_index?use_ssl=true&verify_certs=false")

        args, kwargs = dialect.create_connect_args(url)

        assert kwargs["use_ssl"] is True
        assert kwargs["verify_certs"] is False

    def test_create_connect_args_defaults(self):
        """Test URL parsing with defaults."""
        from sqlalchemy.engine.url import make_url

        dialect = OpenSearchDialect()
        url = make_url("opensearch:///test_index")  # No host/port specified

        args, kwargs = dialect.create_connect_args(url)

        assert kwargs["host"] == "localhost"
        assert kwargs["port"] == 443
        assert kwargs["index"] == "test_index"

    def test_get_column_type_mapping(self):
        """Test OpenSearch type to SQLAlchemy type mapping."""
        dialect = OpenSearchDialect()

        # Test standard types
        text_type = dialect._get_column_type("text")
        assert text_type.__class__.__name__ == "Text"

        keyword_type = dialect._get_column_type("keyword")
        assert keyword_type.__class__.__name__ == "String"

        long_type = dialect._get_column_type("long")
        assert long_type.__class__.__name__ == "BigInteger"

        boolean_type = dialect._get_column_type("boolean")
        assert boolean_type.__class__.__name__ == "Boolean"

        date_type = dialect._get_column_type("date")
        assert date_type.__class__.__name__ == "DateTime"

    def test_get_column_type_opensearch_specific(self):
        """Test OpenSearch-specific type mapping."""
        dialect = OpenSearchDialect()

        # Test OpenSearch-specific types
        object_type = dialect._get_column_type("object")
        assert object_type.__class__.__name__ == "OBJECT"

        nested_type = dialect._get_column_type("nested")
        assert nested_type.__class__.__name__ == "NESTED"

    def test_dialect_registration(self):
        """Test that dialect can be registered and used with SQLAlchemy."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dialect import _register_dialect

        # Register the dialect explicitly for this test
        _register_dialect()

        # This should not raise an exception
        from sqlalchemy import create_mock_engine

        engine = create_mock_engine(
            "opensearch://localhost:9200/test_index", executor=lambda sql, *_: None
        )
        assert engine.dialect.name == "opensearch"


class TestDialectIntegration:
    """Integration tests for dialect functionality."""

    @pytest.fixture
    def mock_connection(self):
        """Create a mock connection for testing."""
        from unittest.mock import Mock

        mock_conn = Mock()
        mock_conn.connection_params = Mock()
        mock_conn.connection_params.index = "test_index"
        return mock_conn

    def test_initialize_dialect(self, mock_connection):
        """Test dialect initialization."""
        dialect = OpenSearchDialect()

        # This should not raise an exception
        dialect.initialize(mock_connection)

        assert dialect.server_version_info == (2, 0, 0)
        assert dialect.default_schema_name == "test_index"

    def test_transaction_methods(self, mock_connection):
        """Test transaction methods (should be no-ops for OpenSearch)."""
        dialect = OpenSearchDialect()

        # These should not raise exceptions
        dialect.do_commit(mock_connection)
        dialect.do_rollback(mock_connection)

    def test_get_schema_names_fallback(self, mock_connection):
        """Test get_schema_names with fallback behavior."""
        dialect = OpenSearchDialect()

        # Mock connection.execute to raise an exception
        mock_connection.execute.side_effect = Exception("SHOW TABLES failed")

        # Should return empty list on failure
        schemas = dialect.get_schema_names(mock_connection)
        assert schemas == []

    def test_get_columns_fallback(self, mock_connection):
        """Test get_columns with fallback behavior."""
        dialect = OpenSearchDialect()

        # Mock connection.execute to raise an exception
        mock_connection.execute.side_effect = Exception("DESCRIBE failed")

        # Should return empty list on failure
        columns = dialect.get_columns(mock_connection, "test_table")
        assert columns == []

    def test_get_pk_constraint(self, mock_connection):
        """Test get_pk_constraint returns _id field."""
        dialect = OpenSearchDialect()

        pk_constraint = dialect.get_pk_constraint(mock_connection, "test_table")

        assert pk_constraint["constrained_columns"] == ["_id"]
        assert pk_constraint["name"] is None

    def test_get_foreign_keys(self, mock_connection):
        """Test get_foreign_keys returns empty list."""
        dialect = OpenSearchDialect()

        foreign_keys = dialect.get_foreign_keys(mock_connection, "test_table")

        assert foreign_keys == []

    def test_get_indexes(self, mock_connection):
        """Test get_indexes returns empty list."""
        dialect = OpenSearchDialect()

        indexes = dialect.get_indexes(mock_connection, "test_table")

        assert indexes == []
