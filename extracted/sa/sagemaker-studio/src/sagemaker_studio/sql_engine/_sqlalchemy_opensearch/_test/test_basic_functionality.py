"""
Basic functionality tests for OpenSearch SQLAlchemy dialect.

Tests that the dialect can be imported and basic functionality works
without requiring an actual OpenSearch connection.
"""

import pytest


class TestBasicFunctionality:
    """Test basic functionality without requiring OpenSearch connection."""

    def test_import_dialect(self):
        """Test that the dialect can be imported."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dialect import OpenSearchDialect

        dialect = OpenSearchDialect()
        assert dialect.name == "opensearch"
        assert dialect.driver == "opensearch"

    def test_import_types(self):
        """Test that OpenSearch types can be imported."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.types import (
            GEO_POINT,
            NESTED,
            OBJECT,
            OpenSearchTypeConverter,
        )

        # Test type instantiation
        obj_type = OBJECT()
        nested_type = NESTED()
        geo_type = GEO_POINT()

        assert obj_type is not None
        assert nested_type is not None
        assert geo_type is not None

        # Test converter
        converter = OpenSearchTypeConverter()
        assert converter is not None

    def test_import_dbapi(self):
        """Test that DBAPI components can be imported."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection import Connection
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection_params import (
            ConnectionParams,
        )
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.cursor import Cursor
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import (
            DatabaseError,
            Error,
            OperationalError,
        )

        # Test that classes can be imported
        assert Connection is not None
        assert Cursor is not None
        assert ConnectionParams is not None

        # Test exception hierarchy
        assert issubclass(DatabaseError, Error)
        assert issubclass(OperationalError, DatabaseError)

    def test_connection_params_creation(self):
        """Test that connection parameters can be created."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection_params import (
            ConnectionParams,
        )

        params = ConnectionParams()
        assert params.host == "localhost"
        assert params.port == 443
        assert params.index == "_all"

    def test_url_parsing(self):
        """Test that URLs can be parsed."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.connection_params import (
            parse_connection_url,
        )

        params = parse_connection_url("opensearch://localhost:9200/test_index")
        assert params.host == "localhost"
        assert params.port == 9200
        assert params.index == "test_index"

    def test_dialect_registration(self):
        """Test that the dialect can be registered with SQLAlchemy."""

        # Try to create an engine (this will fail without opensearch-py, but should not fail due to registration)
        try:
            from sqlalchemy import create_mock_engine

            engine = create_mock_engine(
                "opensearch://localhost:9200/test", executor=lambda sql, *_: None
            )
            assert engine.dialect.name == "opensearch"
        except ImportError as e:
            if "opensearch" in str(e).lower():
                pytest.skip("opensearch-py not available for testing")
            else:
                raise

    def test_type_conversion(self):
        """Test basic type conversion functionality."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.types import OpenSearchTypeConverter

        converter = OpenSearchTypeConverter()

        # Test basic conversions
        assert converter.python_to_opensearch_param(None) is None
        assert converter.python_to_opensearch_param(42) == 42
        assert converter.python_to_opensearch_param("hello") == "hello"
        assert converter.python_to_opensearch_param(True) is True

        # Test result conversion
        assert converter.opensearch_result_to_python(None) is None
        assert converter.opensearch_result_to_python(42) == 42
        assert converter.opensearch_result_to_python("hello") == "hello"

    def test_object_type_processing(self):
        """Test OBJECT type processing."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.types import OBJECT

        obj_type = OBJECT()

        # Test bind parameter processing
        result = obj_type.process_bind_param({"key": "value"}, None)
        assert result == {"key": "value"}

        result = obj_type.process_bind_param(None, None)
        assert result is None

        # Test result value processing
        result = obj_type.process_result_value({"key": "value"}, None)
        assert result == {"key": "value"}

        result = obj_type.process_result_value(None, None)
        assert result is None

    def test_nested_type_processing(self):
        """Test NESTED type processing."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.types import NESTED

        nested_type = NESTED()

        # Test bind parameter processing
        result = nested_type.process_bind_param([{"key": "value"}], None)
        assert result == [{"key": "value"}]

        result = nested_type.process_bind_param(None, None)
        assert result is None

        # Test result value processing
        result = nested_type.process_result_value([{"key": "value"}], None)
        assert result == [{"key": "value"}]

        result = nested_type.process_result_value(None, None)
        assert result == []

    def test_exception_hierarchy(self):
        """Test that exception hierarchy is properly defined."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import (
            AuthenticationError,
            DatabaseError,
            DataError,
            Error,
            IntegrityError,
            InterfaceError,
            InternalError,
            NotSupportedError,
            OpenSearchConnectionError,
            OperationalError,
            ProgrammingError,
        )

        # Test inheritance hierarchy
        assert issubclass(InterfaceError, Error)
        assert issubclass(DatabaseError, Error)
        assert issubclass(DataError, DatabaseError)
        assert issubclass(OperationalError, DatabaseError)
        assert issubclass(IntegrityError, DatabaseError)
        assert issubclass(InternalError, DatabaseError)
        assert issubclass(ProgrammingError, DatabaseError)
        assert issubclass(NotSupportedError, DatabaseError)

        # Test OpenSearch-specific exceptions
        assert issubclass(OpenSearchConnectionError, OperationalError)
        assert issubclass(AuthenticationError, OperationalError)
