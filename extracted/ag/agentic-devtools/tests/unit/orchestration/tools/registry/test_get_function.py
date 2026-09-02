"""Tests for ConcreteToolRegistry.get_function()."""

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestGetFunction:
    """Tests for get_function lookup."""

    def test_returns_registered_function(self):
        """get_function returns the registered callable."""
        registry = ConcreteToolRegistry()

        def my_fn():
            return "hello"

        registry.register(
            ToolDefinition(
                name="test_tool",
                description="Test",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=my_fn,
        )
        assert registry.get_function("test_tool") is my_fn

    def test_returns_none_for_unregistered(self):
        """get_function returns None for non-registered name."""
        registry = ConcreteToolRegistry()
        assert registry.get_function("nonexistent") is None
