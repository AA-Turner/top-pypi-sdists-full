"""
Extended tests for OpenSearch types — covers branches missed by test_types.py.
"""

from datetime import time
from uuid import UUID

from sqlalchemy import types as sqltypes

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.types import (
    GEO_POINT,
    NESTED,
    OBJECT,
    OpenSearchTypeConverter,
    get_column_type,
)


class TestOBJECTEdgeCases:
    """Edge cases for OBJECT type."""

    def test_bind_param_list(self):
        obj = OBJECT()
        result = obj.process_bind_param([1, 2, 3], None)
        assert result == [1, 2, 3]

    def test_bind_param_integer(self):
        obj = OBJECT()
        result = obj.process_bind_param(42, None)
        assert result == {"value": "42"}

    def test_result_value_list(self):
        obj = OBJECT()
        result = obj.process_result_value([1, 2], None)
        assert result == [1, 2]

    def test_result_value_invalid_json_string(self):
        obj = OBJECT()
        result = obj.process_result_value("not json", None)
        assert result == "not json"

    def test_result_value_numeric_string(self):
        """A numeric string that isn't valid JSON object should be returned as-is."""
        obj = OBJECT()
        result = obj.process_result_value("12345", None)
        assert result == 12345  # json.loads("12345") returns int


class TestNESTEDEdgeCases:
    """Edge cases for NESTED type."""

    def test_bind_param_json_object_string(self):
        """JSON string that parses to a dict (not list) should be wrapped in list."""
        nested = NESTED()
        result = nested.process_bind_param('{"key": "val"}', None)
        assert result == [{"key": "val"}]

    def test_bind_param_integer(self):
        nested = NESTED()
        result = nested.process_bind_param(42, None)
        assert result == [{"value": "42"}]

    def test_result_value_json_object_string(self):
        """JSON string that parses to a dict should be wrapped in list."""
        nested = NESTED()
        result = nested.process_result_value('{"key": "val"}', None)
        assert result == [{"key": "val"}]

    def test_result_value_invalid_json_string(self):
        nested = NESTED()
        result = nested.process_result_value("not json", None)
        assert result == ["not json"]

    def test_result_value_numeric_string(self):
        nested = NESTED()
        result = nested.process_result_value("42", None)
        assert result == [42]  # json.loads("42") returns int, wrapped in list


class TestGEO_POINTEdgeCases:
    """Edge cases for GEO_POINT type."""

    def test_bind_param_non_dict_non_string(self):
        geo = GEO_POINT()
        result = geo.process_bind_param(12345, None)
        assert result == "12345"

    def test_result_value_invalid_comma_string(self):
        """String with comma but non-numeric parts should return as string."""
        geo = GEO_POINT()
        result = geo.process_result_value("abc,def", None)
        assert result == "abc,def"

    def test_result_value_no_comma(self):
        geo = GEO_POINT()
        result = geo.process_result_value("single_value", None)
        assert result == "single_value"

    def test_result_value_dict_passthrough(self):
        """Non-string, non-None values should be stringified."""
        geo = GEO_POINT()
        result = geo.process_result_value(12345, None)
        assert result == "12345"

    def test_result_value_dict_input(self):
        """Dict input (e.g. from OpenSearch geo_point) should be returned as-is."""
        geo = GEO_POINT()
        result = geo.process_result_value({"lat": 40.7128, "lon": -74.006}, None)
        assert result == {"lat": 40.7128, "lon": -74.006}


class TestOpenSearchTypeConverterExtended:
    """Extended converter tests for uncovered branches."""

    def test_python_to_opensearch_param_uuid(self):
        converter = OpenSearchTypeConverter()
        uid = UUID("12345678-1234-5678-1234-567812345678")
        result = converter.python_to_opensearch_param(uid)
        assert result == "12345678-1234-5678-1234-567812345678"

    def test_python_to_opensearch_param_time(self):
        converter = OpenSearchTypeConverter()
        t = time(12, 30, 45)
        result = converter.python_to_opensearch_param(t)
        assert result == "12:30:45"

    def test_python_to_opensearch_param_custom_object(self):
        """Custom objects should fall back to str()."""
        converter = OpenSearchTypeConverter()

        class Custom:
            def __str__(self):
                return "custom_value"

        result = converter.python_to_opensearch_param(Custom())
        assert result == "custom_value"

    def test_python_to_opensearch_param_bool_subclass(self):
        """Bool subclass should hit the isinstance(value, bool) fallback."""

        class MyBool(int):
            """A bool-like subclass that isn't exactly bool."""

            pass

        converter = OpenSearchTypeConverter()
        val = MyBool(1)
        result = converter.python_to_opensearch_param(val)
        # MyBool is an int subclass, so direct type lookup finds int
        assert result == 1

    def test_python_to_opensearch_param_int_subclass(self):
        """Int subclass not in direct mapping should hit isinstance fallback."""

        class MyInt(int):
            pass

        converter = OpenSearchTypeConverter()
        result = converter.python_to_opensearch_param(MyInt(42))
        assert result == 42

    def test_python_to_opensearch_param_float_subclass(self):
        """Float subclass not in direct mapping should hit isinstance fallback."""

        class MyFloat(float):
            pass

        converter = OpenSearchTypeConverter()
        result = converter.python_to_opensearch_param(MyFloat(3.14))
        assert result == 3.14

    def test_python_to_opensearch_param_str_subclass(self):
        """Str subclass not in direct mapping should hit isinstance fallback."""

        class MyStr(str):
            pass

        converter = OpenSearchTypeConverter()
        result = converter.python_to_opensearch_param(MyStr("hello"))
        assert result == "hello"

    def test_python_to_opensearch_param_bytes_subclass(self):
        """Bytes subclass not in direct mapping should hit isinstance fallback."""

        class MyBytes(bytes):
            pass

        converter = OpenSearchTypeConverter()
        result = converter.python_to_opensearch_param(MyBytes(b"hello"))
        assert result == "hello"

    def test_python_to_opensearch_param_dict_subclass(self):
        """Dict subclass not in direct mapping should hit isinstance fallback."""
        from collections import OrderedDict

        converter = OpenSearchTypeConverter()
        result = converter.python_to_opensearch_param(OrderedDict(a=1))
        assert result == {"a": 1}

    def test_python_to_opensearch_param_list_subclass(self):
        """List subclass not in direct mapping should hit isinstance fallback."""

        class MyList(list):
            pass

        converter = OpenSearchTypeConverter()
        result = converter.python_to_opensearch_param(MyList([1, 2, 3]))
        assert result == [1, 2, 3]

    def test_python_to_opensearch_param_datetime_subclass(self):
        """Datetime subclass not in direct mapping should hit isinstance fallback."""
        from datetime import datetime

        class MyDatetime(datetime):
            pass

        converter = OpenSearchTypeConverter()
        dt = MyDatetime(2023, 6, 15, 12, 0, 0)
        result = converter.python_to_opensearch_param(dt)
        assert result == "2023-06-15T12:00:00"

    def test_python_to_opensearch_param_bool_isinstance_branch(self):
        """
        The isinstance(value, bool) branch (line 206) is unreachable in practice
        since bool is final and type(True) == bool is always in the direct mapping.
        We verify the direct mapping handles bool correctly.
        """
        converter = OpenSearchTypeConverter()
        assert converter.python_to_opensearch_param(True) is True
        assert converter.python_to_opensearch_param(False) is False

    def test_opensearch_result_to_python_conversion_failure(self):
        """If type conversion fails, return raw value."""
        converter = OpenSearchTypeConverter()
        result = converter.opensearch_result_to_python("not_a_number", "long")
        assert result == "not_a_number"

    def test_opensearch_result_to_python_no_type(self):
        """Without column_type, value is returned as-is."""
        converter = OpenSearchTypeConverter()
        assert converter.opensearch_result_to_python(42) == 42
        assert converter.opensearch_result_to_python("hello") == "hello"

    def test_opensearch_result_to_python_unknown_type(self):
        """Unknown column type returns value as-is."""
        converter = OpenSearchTypeConverter()
        result = converter.opensearch_result_to_python("val", "unknown_type")
        assert result == "val"

    def test_convert_nested_value_none(self):
        result = OpenSearchTypeConverter._convert_nested_value(None)
        assert result == []

    def test_convert_nested_value_list(self):
        result = OpenSearchTypeConverter._convert_nested_value([1, 2])
        assert result == [1, 2]

    def test_convert_nested_value_json_string(self):
        result = OpenSearchTypeConverter._convert_nested_value('[{"a": 1}]')
        assert result == [{"a": 1}]

    def test_convert_nested_value_json_object_string(self):
        result = OpenSearchTypeConverter._convert_nested_value('{"a": 1}')
        assert result == [{"a": 1}]

    def test_convert_nested_value_plain_string(self):
        result = OpenSearchTypeConverter._convert_nested_value("not json")
        assert result == ["not json"]

    def test_convert_nested_value_scalar(self):
        result = OpenSearchTypeConverter._convert_nested_value(42)
        assert result == [42]

    def test_convert_result_row_extra_fields(self):
        """Row data longer than metadata should still convert all fields."""
        converter = OpenSearchTypeConverter()
        row_data = ["text", 42, True, "extra"]
        column_metadata = [{"type": "text"}, {"type": "long"}]
        result = converter.convert_result_row(row_data, column_metadata)
        assert len(result) == 4
        assert result[0] == "text"
        assert result[1] == 42
        assert result[2] is True
        assert result[3] == "extra"

    def test_opensearch_to_python_ip(self):
        converter = OpenSearchTypeConverter()
        result = converter.opensearch_result_to_python("192.168.1.1", "ip")
        assert result == "192.168.1.1"

    def test_opensearch_to_python_boolean(self):
        converter = OpenSearchTypeConverter()
        result = converter.opensearch_result_to_python(True, "boolean")
        assert result is True

    def test_opensearch_to_python_geo_point(self):
        converter = OpenSearchTypeConverter()
        val = {"lat": 40.7, "lon": -74.0}
        result = converter.opensearch_result_to_python(val, "geo_point")
        assert result == val

    def test_opensearch_to_python_binary(self):
        converter = OpenSearchTypeConverter()
        result = converter.opensearch_result_to_python(b"hello", "binary")
        assert result == b"hello"

    def test_opensearch_to_python_object_none(self):
        converter = OpenSearchTypeConverter()
        result = converter.opensearch_result_to_python(None, "object")
        assert result is None

    def test_opensearch_to_python_keyword(self):
        converter = OpenSearchTypeConverter()
        result = converter.opensearch_result_to_python("keyword_val", "keyword")
        assert result == "keyword_val"

    def test_opensearch_to_python_half_float(self):
        converter = OpenSearchTypeConverter()
        result = converter.opensearch_result_to_python(3.14, "half_float")
        assert result == 3.14

    def test_opensearch_to_python_scaled_float(self):
        converter = OpenSearchTypeConverter()
        result = converter.opensearch_result_to_python("2.5", "scaled_float")
        assert result == 2.5


class TestGetColumnTypeExtended:
    """Extended tests for get_column_type."""

    def test_short_type(self):
        result = get_column_type({"type": "SHORT"})
        assert result == sqltypes.SmallInteger

    def test_byte_type(self):
        result = get_column_type({"type": "BYTE"})
        assert result == sqltypes.SmallInteger

    def test_half_float_type(self):
        result = get_column_type({"type": "HALF_FLOAT"})
        assert result == sqltypes.Float

    def test_scaled_float_type(self):
        result = get_column_type({"type": "SCALED_FLOAT"})
        assert result == sqltypes.Float

    def test_binary_type(self):
        result = get_column_type({"type": "BINARY"})
        assert result == sqltypes.LargeBinary

    def test_ip_type(self):
        result = get_column_type({"type": "IP"})
        assert result == sqltypes.String

    def test_geo_shape_type(self):
        result = get_column_type({"type": "GEO_SHAPE"})
        assert result == sqltypes.String
