"""Tests for LangChain adapter - to_langchain_tool."""

import pytest

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry

langchain_core = pytest.importorskip("langchain_core")


class TestToLangchainTool:
    """Tests for to_langchain_tool conversion."""

    def test_converts_to_base_tool(self):
        """Converts a ToolDefinition to a LangChain BaseTool."""
        from langchain_core.tools import BaseTool

        from agentic_devtools.orchestration.tools.langchain_adapter import to_langchain_tool

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="jira_add_comment",
                description="Add a comment to a Jira issue",
                category="jira",
                input_schema={
                    "type": "object",
                    "properties": {
                        "issue_key": {"type": "string", "description": "Issue key"},
                        "comment": {"type": "string", "description": "Comment text"},
                    },
                    "required": ["issue_key", "comment"],
                },
            ),
            fn=lambda issue_key, comment: {"comment_id": "123"},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        definition = registry.get("jira_add_comment")

        tool = to_langchain_tool(definition, executor)
        assert isinstance(tool, BaseTool)
        assert tool.name == "jira_add_comment"
        assert tool.description == "Add a comment to a Jira issue"

    def test_run_delegates_to_executor(self):
        """BaseTool._run delegates to ToolExecutor."""
        from agentic_devtools.orchestration.tools.langchain_adapter import to_langchain_tool

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="echo",
                description="Echo",
                category="testing",
                input_schema={
                    "type": "object",
                    "properties": {"msg": {"type": "string"}},
                    "required": ["msg"],
                },
            ),
            fn=lambda msg: {"echoed": msg},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        definition = registry.get("echo")

        tool = to_langchain_tool(definition, executor)
        result = tool._run(msg="hello")
        import json

        parsed = json.loads(result)
        assert parsed["success"] is True
        assert parsed["output"]["echoed"] == "hello"

    def test_optional_field_without_null_is_non_nullable_in_pydantic_schema(self):
        """Optional field without null in JSON Schema is non-nullable in Pydantic args_schema."""
        from agentic_devtools.orchestration.tools.langchain_adapter import to_langchain_tool

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="tool_with_optional",
                description="Has an optional non-nullable field",
                category="testing",
                input_schema={
                    "type": "object",
                    "properties": {
                        "required_key": {"type": "string"},
                        "optional_non_null": {"type": "string"},
                    },
                    "required": ["required_key"],
                },
            ),
            fn=lambda required_key, optional_non_null=None: {"result": "ok"},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        definition = registry.get("tool_with_optional")

        tool = to_langchain_tool(definition, executor)
        schema = tool.args_schema.model_json_schema()

        # optional_non_null field should not include "null" in its type
        optional_field = schema.get("properties", {}).get("optional_non_null", {})
        field_type = optional_field.get("type")
        # When not nullable: type is a single string, not a list containing "null"
        assert field_type == "string", f"Expected 'string', got {field_type!r}"

    def test_optional_field_with_null_allows_null_in_pydantic_schema(self):
        """Optional field that explicitly allows null in JSON Schema is nullable in Pydantic."""
        from agentic_devtools.orchestration.tools.langchain_adapter import to_langchain_tool

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="tool_with_nullable",
                description="Has an optional nullable field",
                category="testing",
                input_schema={
                    "type": "object",
                    "properties": {
                        "required_key": {"type": "string"},
                        "optional_nullable": {"type": ["string", "null"]},
                    },
                    "required": ["required_key"],
                },
            ),
            fn=lambda required_key, optional_nullable=None: {"result": "ok"},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        definition = registry.get("tool_with_nullable")

        tool = to_langchain_tool(definition, executor)
        schema = tool.args_schema.model_json_schema()

        # optional_nullable field should allow null in the generated schema
        optional_field = schema.get("properties", {}).get("optional_nullable", {})
        field_type = optional_field.get("type")
        any_of = optional_field.get("anyOf")
        # Pydantic may render Optional[str] as {"anyOf": [{"type": "string"}, {"type": "null"}]}
        # or as {"type": ["string", "null"]} — either way null must appear
        allows_null = (isinstance(field_type, list) and "null" in field_type) or (
            any_of is not None and any(e.get("type") == "null" for e in any_of)
        )
        assert allows_null, f"Expected null to be allowed, got schema: {optional_field!r}"

    def test_node_name_is_forwarded_to_executor(self):
        """node_name passed to to_langchain_tool() is forwarded to execute()."""
        from unittest.mock import patch

        from agentic_devtools.orchestration.tools.langchain_adapter import to_langchain_tool
        from agentic_devtools.orchestration.tools.result import ToolResult

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="send_message",
                description="Send a message",
                category="messaging",
                input_schema={
                    "type": "object",
                    "properties": {"text": {"type": "string"}},
                    "required": ["text"],
                },
            ),
            fn=lambda text: {"sent": True},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        definition = registry.get("send_message")

        tool = to_langchain_tool(definition, executor, node_name="planning_node")

        mock_result = ToolResult(success=True, output={"sent": True})
        with patch.object(executor, "execute", return_value=mock_result) as mock_execute:
            tool._run(text="hello")

        mock_execute.assert_called_once_with("send_message", {"text": "hello"}, node_name="planning_node")
        executor.shutdown(wait=False)

    def test_default_node_name_is_empty_string(self):
        """When node_name is omitted, execute() receives node_name='' (read-only / local-mutation tools)."""
        from unittest.mock import patch

        from agentic_devtools.orchestration.tools.langchain_adapter import to_langchain_tool
        from agentic_devtools.orchestration.tools.result import ToolResult

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="read_data",
                description="Read data",
                category="query",
                input_schema={
                    "type": "object",
                    "properties": {"key": {"type": "string"}},
                    "required": ["key"],
                },
            ),
            fn=lambda key: {"value": "data"},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        definition = registry.get("read_data")

        tool = to_langchain_tool(definition, executor)

        mock_result = ToolResult(success=True, output={"value": "data"})
        with patch.object(executor, "execute", return_value=mock_result) as mock_execute:
            tool._run(key="x")

        mock_execute.assert_called_once_with("read_data", {"key": "x"}, node_name="")
        executor.shutdown(wait=False)
