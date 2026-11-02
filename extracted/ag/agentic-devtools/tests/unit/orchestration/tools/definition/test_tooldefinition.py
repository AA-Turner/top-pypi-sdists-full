"""Tests for ToolDefinition dataclass."""

from agentic_devtools.orchestration.tools.definition import ToolDefinition


class TestToolDefinition:
    """Tests for ToolDefinition construction and serialization."""

    def test_create_minimal(self):
        """Minimal construction with required fields."""
        td = ToolDefinition(
            name="test_tool",
            description="A test tool",
            category="testing",
            input_schema={"type": "object", "properties": {}},
        )
        assert td.name == "test_tool"
        assert td.description == "A test tool"
        assert td.category == "testing"
        assert td.mutating is False
        assert td.timeout_seconds == 30.0
        assert td.thread_safe is True

    def test_create_full(self):
        """Full construction with all fields."""
        td = ToolDefinition(
            name="mutating_tool",
            description="A mutating tool",
            category="git",
            input_schema={"type": "object", "properties": {"msg": {"type": "string"}}},
            output_schema={"type": "object", "properties": {"ok": {"type": "boolean"}}},
            mutating=True,
            timeout_seconds=60.0,
            thread_safe=False,
        )
        assert td.mutating is True
        assert td.timeout_seconds == 60.0
        assert td.thread_safe is False

    def test_frozen_immutable(self):
        """ToolDefinition is immutable (frozen dataclass)."""
        td = ToolDefinition(
            name="test",
            description="test",
            category="test",
            input_schema={"type": "object"},
        )
        try:
            td.name = "changed"  # type: ignore[misc]
            assert False, "Should have raised"
        except AttributeError:
            pass

    def test_to_dict(self):
        """to_dict returns JSON-serializable dict."""
        td = ToolDefinition(
            name="my_tool",
            description="My tool",
            category="git",
            input_schema={"type": "object", "properties": {}},
        )
        d = td.to_dict()
        assert d["name"] == "my_tool"
        assert d["description"] == "My tool"
        assert d["category"] == "git"
        assert isinstance(d, dict)
