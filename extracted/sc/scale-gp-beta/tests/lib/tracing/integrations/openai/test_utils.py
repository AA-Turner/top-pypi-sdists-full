import json
from unittest.mock import Mock, patch

from scale_gp_beta.lib.tracing.integrations.openai.utils import (
    sgp_span_name,  # pyright: ignore[reportUnknownVariableType]
    parse_metadata,  # pyright: ignore[reportUnknownVariableType]
    parse_input_output,  # pyright: ignore[reportUnknownVariableType]
)


class TestParseInputOutput:
    """Tests for parse_input_output function"""

    def test_parse_dict_json_string(self):
        """Test parsing a JSON string that represents a dict"""
        mock_span = Mock()
        mock_span_data = Mock()
        dict_value = {"key": "value", "nested": {"data": 123}}
        mock_span_data.export.return_value = {"input": json.dumps(dict_value)}
        mock_span.span_data = mock_span_data

        result = parse_input_output(mock_span, "input")

        assert result == dict_value
        assert isinstance(result, dict)

    def test_parse_list_json_string(self):
        """Test parsing a JSON string that represents a list - should wrap in dict"""
        mock_span = Mock()
        mock_span_data = Mock()
        list_value = [1, 2, 3, "test"]
        mock_span_data.export.return_value = {"output": json.dumps(list_value)}
        mock_span.span_data = mock_span_data

        result = parse_input_output(mock_span, "output")

        assert result == {"output": list_value}
        assert isinstance(result, dict)

    def test_parse_integer_json_string(self):
        """Test parsing a JSON string that represents an integer - should wrap in dict"""
        mock_span = Mock()
        mock_span_data = Mock()
        int_value = 42
        mock_span_data.export.return_value = {"input": json.dumps(int_value)}
        mock_span.span_data = mock_span_data

        result = parse_input_output(mock_span, "input")

        assert result == {"input": int_value}
        assert isinstance(result, dict)

    def test_parse_string_json_string(self):
        """Test parsing a JSON string that represents a string - should wrap in dict"""
        mock_span = Mock()
        mock_span_data = Mock()
        string_value = "hello world"
        mock_span_data.export.return_value = {"output": json.dumps(string_value)}
        mock_span.span_data = mock_span_data

        result = parse_input_output(mock_span, "output")

        assert result == {"output": string_value}
        assert isinstance(result, dict)

    def test_parse_boolean_json_string(self):
        """Test parsing a JSON string that represents a boolean - should wrap in dict"""
        mock_span = Mock()
        mock_span_data = Mock()
        bool_value = True
        mock_span_data.export.return_value = {"input": json.dumps(bool_value)}
        mock_span.span_data = mock_span_data

        result = parse_input_output(mock_span, "input")

        assert result == {"input": bool_value}
        assert isinstance(result, dict)

    def test_parse_null_json_string(self):
        """Test parsing a JSON string that represents null - should wrap in dict"""
        mock_span = Mock()
        mock_span_data = Mock()
        mock_span_data.export.return_value = {"output": json.dumps(None)}
        mock_span.span_data = mock_span_data

        result = parse_input_output(mock_span, "output")

        assert result == {"output": None}
        assert isinstance(result, dict)

    def test_parse_invalid_json_string(self):
        """Test parsing an invalid JSON string - should wrap in dict"""
        mock_span = Mock()
        mock_span_data = Mock()
        invalid_json = "not valid json {"
        mock_span_data.export.return_value = {"input": invalid_json}
        mock_span.span_data = mock_span_data

        result = parse_input_output(mock_span, "input")

        assert result == {"input": invalid_json}
        assert isinstance(result, dict)

    def test_parse_non_string_dict_value(self):
        """Test when value is already a dict (not a string)"""
        mock_span = Mock()
        mock_span_data = Mock()
        dict_value = {"existing": "dict"}
        mock_span_data.export.return_value = {"output": dict_value}
        mock_span.span_data = mock_span_data

        result = parse_input_output(mock_span, "output")

        assert result == {"output": dict_value}
        assert isinstance(result, dict)

    def test_parse_non_string_list_value(self):
        """Test when value is already a list (not a string)"""
        mock_span = Mock()
        mock_span_data = Mock()
        list_value = [1, 2, 3]
        mock_span_data.export.return_value = {"input": list_value}
        mock_span.span_data = mock_span_data

        result = parse_input_output(mock_span, "input")

        assert result == {"input": list_value}
        assert isinstance(result, dict)

    def test_parse_none_value(self):
        """Test when the key doesn't exist in exported data"""
        mock_span = Mock()
        mock_span_data = Mock()
        mock_span_data.export.return_value = {}
        mock_span.span_data = mock_span_data

        result = parse_input_output(mock_span, "nonexistent_key")

        assert result == {}
        assert isinstance(result, dict)

    def test_parse_none_span_data(self):
        """Test when span_data is None"""
        mock_span = Mock()
        mock_span.span_data = None

        result = parse_input_output(mock_span, "input")

        assert result == {}
        assert isinstance(result, dict)

    def test_parse_complex_nested_structure(self):
        """Test parsing a complex nested JSON structure"""
        mock_span = Mock()
        mock_span_data = Mock()
        complex_value = {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ],
            "metadata": {
                "tokens": 150,
                "model": "gpt-4"
            }
        }
        mock_span_data.export.return_value = {"input": json.dumps(complex_value)}
        mock_span.span_data = mock_span_data

        result = parse_input_output(mock_span, "input")

        assert result == complex_value
        assert isinstance(result, dict)
        assert len(result["messages"]) == 2
        assert result["metadata"]["tokens"] == 150


class TestSgpSpanName:
    """Tests for sgp_span_name function"""

    def test_with_valid_name(self):
        """Test when span_data has a name in export"""
        mock_span = Mock()
        mock_span_data = Mock()
        mock_span_data.export.return_value = {"name": "TestSpan"}
        mock_span_data.__class__.__name__ = "CustomSpanData"
        mock_span.span_data = mock_span_data

        result = sgp_span_name(mock_span)

        assert result == "TestSpan"

    def test_without_name(self):
        """Test when span_data doesn't have a name - should use class name"""
        mock_span = Mock()
        mock_span_data = Mock()
        mock_span_data.export.return_value = {}
        mock_span_data.__class__.__name__ = "ToolSpanData"
        mock_span.span_data = mock_span_data

        result = sgp_span_name(mock_span)

        assert result == "Tool"

    def test_with_none_span_data(self):
        """Test when span_data is None"""
        mock_span = Mock()
        mock_span.span_data = None

        result = sgp_span_name(mock_span)

        assert result == "Unnamed Span"

class TestParseMetadata:
    """Tests for parse_metadata function"""

    def test_with_valid_span_data(self):
        """Test parsing metadata from span with valid span_data"""
        mock_span = Mock()
        mock_span_data = Mock()
        mock_span_data.export.return_value = {
            "type": "tool",
            "name": "calculator",
            "extra": "value",
            "input": "should be excluded",
            "output": "should be excluded"
        }
        mock_span.span_id = "span-123"
        mock_span.span_data = mock_span_data

        with patch('scale_gp_beta.lib.tracing.integrations.openai.utils.extract_response', return_value=None):
            result = parse_metadata(mock_span)

        assert "openai_metadata" in result
        assert result["openai_metadata"]["openai_span_id"] == "span-123"
        assert result["openai_metadata"]["type"] == "tool"
        assert result["openai_metadata"]["name"] == "calculator"
        assert result["openai_metadata"]["extra"] == "value"
        assert "input" not in result["openai_metadata"]
        assert "output" not in result["openai_metadata"]

    def test_with_none_span_data(self):
        """Test when span_data is None"""
        mock_span = Mock()
        mock_span.span_data = None

        result = parse_metadata(mock_span)

        assert result == {}
