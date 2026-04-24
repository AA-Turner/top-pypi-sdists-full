"""
Unit tests for OpenSearch SQLAlchemy types.

Tests the type system and conversion utilities for OpenSearch-specific
types and standard type mappings.
"""

from datetime import date, datetime

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.types import (
    GEO_POINT,
    NESTED,
    OBJECT,
    OpenSearchTypeConverter,
)


class TestOpenSearchTypes:
    """Test cases for OpenSearch-specific SQLAlchemy types."""

    def test_object_type_bind_param(self):
        """Test OBJECT type bind parameter processing."""
        obj_type = OBJECT()

        # Test dict input
        result = obj_type.process_bind_param({"key": "value"}, None)
        assert result == {"key": "value"}

        # Test JSON string input
        result = obj_type.process_bind_param('{"key": "value"}', None)
        assert result == {"key": "value"}

        # Test None input
        result = obj_type.process_bind_param(None, None)
        assert result is None

        # Test string input (non-JSON)
        result = obj_type.process_bind_param("simple string", None)
        assert result == {"value": "simple string"}

    def test_object_type_result_value(self):
        """Test OBJECT type result value processing."""
        obj_type = OBJECT()

        # Test dict input
        result = obj_type.process_result_value({"key": "value"}, None)
        assert result == {"key": "value"}

        # Test None input
        result = obj_type.process_result_value(None, None)
        assert result is None

        # Test JSON string input
        result = obj_type.process_result_value('{"key": "value"}', None)
        assert result == {"key": "value"}

    def test_nested_type_bind_param(self):
        """Test NESTED type bind parameter processing."""
        nested_type = NESTED()

        # Test list input
        result = nested_type.process_bind_param([{"key": "value"}], None)
        assert result == [{"key": "value"}]

        # Test JSON array string input
        result = nested_type.process_bind_param('[{"key": "value"}]', None)
        assert result == [{"key": "value"}]

        # Test None input
        result = nested_type.process_bind_param(None, None)
        assert result is None

        # Test string input (non-JSON)
        result = nested_type.process_bind_param("simple string", None)
        assert result == [{"value": "simple string"}]

    def test_nested_type_result_value(self):
        """Test NESTED type result value processing."""
        nested_type = NESTED()

        # Test list input
        result = nested_type.process_result_value([{"key": "value"}], None)
        assert result == [{"key": "value"}]

        # Test None input
        result = nested_type.process_result_value(None, None)
        assert result == []

        # Test JSON array string input
        result = nested_type.process_result_value('[{"key": "value"}]', None)
        assert result == [{"key": "value"}]

    def test_geo_point_type_bind_param(self):
        """Test GEO_POINT type bind parameter processing."""
        geo_type = GEO_POINT()

        # Test dict input with lat/lon
        result = geo_type.process_bind_param({"lat": 40.7128, "lon": -74.0060}, None)
        assert result == "40.7128,-74.006"

        # Test string input
        result = geo_type.process_bind_param("40.7128,-74.0060", None)
        assert result == "40.7128,-74.0060"

        # Test None input
        result = geo_type.process_bind_param(None, None)
        assert result is None

    def test_geo_point_type_result_value(self):
        """Test GEO_POINT type result value processing."""
        geo_type = GEO_POINT()

        # Test string input with coordinates
        result = geo_type.process_result_value("40.7128,-74.0060", None)
        assert result == {"lat": 40.7128, "lon": -74.0060}

        # Test None input
        result = geo_type.process_result_value(None, None)
        assert result is None

        # Test invalid string input
        result = geo_type.process_result_value("invalid", None)
        assert result == "invalid"


class TestOpenSearchTypeConverter:
    """Test cases for OpenSearchTypeConverter utility class."""

    def test_python_to_opensearch_param_basic_types(self):
        """Test conversion of basic Python types to OpenSearch format."""
        converter = OpenSearchTypeConverter()

        # Test None
        assert converter.python_to_opensearch_param(None) is None

        # Test basic types
        assert converter.python_to_opensearch_param(True) is True
        assert converter.python_to_opensearch_param(42) == 42
        assert converter.python_to_opensearch_param(3.14) == 3.14
        assert converter.python_to_opensearch_param("hello") == "hello"

        # Test bytes
        assert converter.python_to_opensearch_param(b"hello") == "hello"

        # Test datetime
        dt = datetime(2023, 1, 1, 12, 0, 0)
        result = converter.python_to_opensearch_param(dt)
        assert result == "2023-01-01T12:00:00"

        # Test date
        d = date(2023, 1, 1)
        result = converter.python_to_opensearch_param(d)
        assert result == "2023-01-01"

    def test_python_to_opensearch_param_collections(self):
        """Test conversion of collections to OpenSearch format."""
        converter = OpenSearchTypeConverter()

        # Test dict
        data = {"key": "value"}
        assert converter.python_to_opensearch_param(data) == data

        # Test list
        data = [1, 2, 3]
        assert converter.python_to_opensearch_param(data) == data

    def test_opensearch_result_to_python_basic_types(self):
        """Test conversion of OpenSearch results to Python types."""
        converter = OpenSearchTypeConverter()

        # Test None
        assert converter.opensearch_result_to_python(None) is None

        # Test basic types (should pass through)
        assert converter.opensearch_result_to_python(42) == 42
        assert converter.opensearch_result_to_python("hello") == "hello"
        assert converter.opensearch_result_to_python(True) is True

    def test_opensearch_result_to_python_with_type_hints(self):
        """Test conversion with column type hints."""
        converter = OpenSearchTypeConverter()

        # Test date conversion
        result = converter.opensearch_result_to_python("2023-01-01T12:00:00Z", "date")
        assert isinstance(result, datetime)

        # Test object conversion
        result = converter.opensearch_result_to_python('{"key": "value"}', "object")
        assert result == {"key": "value"}

        # Test nested conversion
        result = converter.opensearch_result_to_python('[{"key": "value"}]', "nested")
        assert result == [{"key": "value"}]

    def test_convert_parameters(self):
        """Test parameter dictionary conversion."""
        converter = OpenSearchTypeConverter()

        params = {
            "string_param": "hello",
            "int_param": 42,
            "bool_param": True,
            "date_param": datetime(2023, 1, 1),
        }

        result = converter.convert_parameters(params)

        assert result["string_param"] == "hello"
        assert result["int_param"] == 42
        assert result["bool_param"] is True
        assert result["date_param"] == "2023-01-01T00:00:00"

    def test_convert_parameters_empty(self):
        """Test conversion of empty parameters."""
        converter = OpenSearchTypeConverter()

        assert converter.convert_parameters(None) == {}
        assert converter.convert_parameters({}) == {}

    def test_convert_result_row(self):
        """Test conversion of result row data."""
        converter = OpenSearchTypeConverter()

        row_data = ["text_value", 42, True, "2023-01-01T12:00:00Z"]
        column_metadata = [
            {"type": "text"},
            {"type": "long"},
            {"type": "boolean"},
            {"type": "date"},
        ]

        result = converter.convert_result_row(row_data, column_metadata)

        assert result[0] == "text_value"
        assert result[1] == 42
        assert result[2] is True
        assert isinstance(result[3], datetime)

    def test_convert_result_row_mismatched_lengths(self):
        """Test conversion when row data and metadata lengths don't match."""
        converter = OpenSearchTypeConverter()

        row_data = ["text_value", 42, True]
        column_metadata = [{"type": "text"}]  # Shorter than row_data

        result = converter.convert_result_row(row_data, column_metadata)

        # Should handle gracefully
        assert len(result) == 3
        assert result[0] == "text_value"
        assert result[1] == 42  # No type conversion applied
        assert result[2] is True  # No type conversion applied


class TestTypeMapping:
    """Test cases for type mapping utilities."""

    def test_get_column_type_standard_types(self):
        """Test get_column_type for standard OpenSearch types."""
        from sqlalchemy import types as sqltypes

        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.types import get_column_type

        # Test text type
        result = get_column_type({"type": "TEXT"})
        assert result == sqltypes.Text

        # Test keyword type
        result = get_column_type({"type": "KEYWORD"})
        assert result == sqltypes.String

        # Test numeric types
        result = get_column_type({"type": "LONG"})
        assert result == sqltypes.BigInteger

        result = get_column_type({"type": "INTEGER"})
        assert result == sqltypes.Integer

        result = get_column_type({"type": "DOUBLE"})
        assert result == sqltypes.Float

        # Test boolean type
        result = get_column_type({"type": "BOOLEAN"})
        assert result == sqltypes.Boolean

        # Test date type
        result = get_column_type({"type": "DATE"})
        assert result == sqltypes.DateTime

    def test_get_column_type_opensearch_specific(self):
        """Test get_column_type for OpenSearch-specific types."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.types import get_column_type

        # Test object type
        result = get_column_type({"type": "OBJECT"})
        assert result == OBJECT

        # Test nested type
        result = get_column_type({"type": "NESTED"})
        assert result == NESTED

        # Test geo_point type
        result = get_column_type({"type": "GEO_POINT"})
        assert result == GEO_POINT

    def test_get_column_type_unknown_type(self):
        """Test get_column_type for unknown types."""
        from sqlalchemy import types as sqltypes

        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.types import get_column_type

        # Test unknown type defaults to String
        result = get_column_type({"type": "UNKNOWN_TYPE"})
        assert result == sqltypes.String

    def test_get_column_type_missing_type(self):
        """Test get_column_type when type is missing."""
        from sqlalchemy import types as sqltypes

        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.types import get_column_type

        # Test missing type defaults to String
        result = get_column_type({})
        assert result == sqltypes.String
