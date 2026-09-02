"""Tests for ToolRegistry protocol conformance."""

from agentic_devtools.orchestration.execution.protocols import ToolRegistry
from agentic_devtools.orchestration.tools.definition import ToolDefinition


class _MockToolRegistry:
    """A concrete class satisfying the ToolRegistry protocol."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def invoke(self, tool_name: str, **kwargs):  # noqa: ANN003, ANN201
        self.calls.append((tool_name, kwargs))
        return {"result": f"called {tool_name}"}

    def list_all(self) -> dict[str, ToolDefinition]:  # noqa: ANN201
        return {}

    def get_categories(self) -> list[str]:
        return []


class TestToolRegistry:
    def test_mock_satisfies_protocol(self) -> None:
        registry = _MockToolRegistry()
        assert isinstance(registry, ToolRegistry)

    def test_invoke_returns_json_value(self) -> None:
        registry = _MockToolRegistry()
        result = registry.invoke("get_diff", file="test.py")
        assert isinstance(result, dict)
        assert "called get_diff" in result["result"]

    def test_invoke_records_calls(self) -> None:
        registry = _MockToolRegistry()
        registry.invoke("tool_a", x=1)
        registry.invoke("tool_b", y="hello")
        assert len(registry.calls) == 2
        assert registry.calls[0] == ("tool_a", {"x": 1})
        assert registry.calls[1] == ("tool_b", {"y": "hello"})
