"""Tests for tool utilities."""

from mistralai.workflows.plugins.mistralai.tool import (
    ToolArgumentErrorResult,
    check_is_custom_tool,
    get_tool_name,
)


class TestToolUtilities:
    def test_check_is_custom_tool_with_callable(self):
        """Test that callable objects are identified as custom tools."""

        async def my_tool():
            pass

        assert check_is_custom_tool(my_tool) is True

    def test_get_tool_name_from_callable(self):
        """Test getting tool name from a callable."""

        async def my_custom_tool():
            pass

        assert get_tool_name(my_custom_tool) == "my_custom_tool"


class TestToolArgumentErrorResult:
    def test_error_result_creation(self):
        """Test creating a tool argument error result."""
        result = ToolArgumentErrorResult(error="Invalid argument")
        assert result.error == "Invalid argument"
        assert result.success is False

    def test_error_result_json_serialization(self):
        """Test that error result can be serialized to JSON."""
        result = ToolArgumentErrorResult(error="Test error")
        json_str = result.model_dump_json()
        assert "Test error" in json_str
        assert "false" in json_str.lower()
