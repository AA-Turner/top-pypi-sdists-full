"""Tests for LangChain adapter optional field handling."""

import pytest

langchain_core = pytest.importorskip("langchain_core")


class TestOptionalFields:
    """Tests for optional (non-required) field support in schema conversion."""

    def test_optional_field_accepts_none(self):
        """Optional fields in schema are mapped to Optional types."""
        from agentic_devtools.orchestration.tools.definition import ToolDefinition
        from agentic_devtools.orchestration.tools.executor import ToolExecutor
        from agentic_devtools.orchestration.tools.langchain_adapter import to_langchain_tool
        from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="mixed_tool",
                description="Tool with required and optional fields",
                category="testing",
                input_schema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                    "required": ["name"],
                },
            ),
            fn=lambda name, age=None: {"name": name, "age": age},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        definition = registry.get("mixed_tool")

        tool = to_langchain_tool(definition, executor)
        # The tool should accept calls with optional field omitted
        result = tool._run(name="Alice")
        import json

        parsed = json.loads(result)
        assert parsed["success"] is True
        assert parsed["output"]["name"] == "Alice"
        assert parsed["output"]["age"] is None

    def test_required_nullable_field_accepts_none(self):
        """Required keys that allow null should validate with None values."""
        from agentic_devtools.orchestration.tools.definition import ToolDefinition
        from agentic_devtools.orchestration.tools.executor import ToolExecutor
        from agentic_devtools.orchestration.tools.langchain_adapter import to_langchain_tool
        from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="nullable_required_tool",
                description="Tool with required but nullable field",
                category="testing",
                input_schema={
                    "type": "object",
                    "properties": {
                        "name": {"type": ["string", "null"]},
                    },
                    "required": ["name"],
                },
            ),
            fn=lambda name: {"name": name},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        definition = registry.get("nullable_required_tool")

        tool = to_langchain_tool(definition, executor)
        validated = tool.args_schema.model_validate({"name": None})
        assert validated.name is None
