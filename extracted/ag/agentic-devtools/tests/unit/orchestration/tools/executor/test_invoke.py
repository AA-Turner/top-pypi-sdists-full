"""Tests for ToolExecutor.invoke()."""

from unittest.mock import patch

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry
from agentic_devtools.orchestration.tools.result import ToolResult


class TestInvoke:
    """Tests for ToolExecutor.invoke() facade."""

    def test_invoke_returns_json_dict(self):
        """invoke returns a JSON-serializable dict envelope."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="echo",
                description="Echo",
                category="testing",
                input_schema={"type": "object", "properties": {"msg": {"type": "string"}}},
            ),
            fn=lambda msg="": {"echoed": msg},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.invoke("echo", msg="hi")
        assert isinstance(result, dict)
        assert result["success"] is True
        assert result["output"]["echoed"] == "hi"

    def test_invoke_failure_returns_error_envelope(self):
        """invoke returns error dict for failing tools."""
        registry = ConcreteToolRegistry()
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.invoke("nonexistent")
        assert isinstance(result, dict)
        assert result["success"] is False
        assert result["error_type"] == "not_found"

    def test_invoke_with_node_name_executes_registered_tool(self):
        """invoke keeps node_name out of tool kwargs for normal registered tools."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="echo",
                description="Echo",
                category="testing",
                input_schema={"type": "object", "properties": {"msg": {"type": "string"}}},
            ),
            fn=lambda msg="": {"echoed": msg},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.invoke("echo", node_name="planning", msg="hi")
        assert result["success"] is True
        assert result["output"]["echoed"] == "hi"

    def test_invoke_passes_reserved_node_name_to_execute(self):
        """invoke routes reserved node_name to execute context instead of tool inputs."""
        registry = ConcreteToolRegistry()
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        with patch.object(executor, "execute") as mock_execute:
            mock_execute.return_value = ToolResult(success=True, output={"ok": True})
            _ = executor.invoke("echo", node_name="planning", msg="hi")

        mock_execute.assert_called_once_with("echo", {"msg": "hi"}, node_name="planning")

    def test_invoke_uses_empty_node_name_when_not_provided(self):
        """invoke defaults node_name context to empty string when omitted."""
        registry = ConcreteToolRegistry()
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        with patch.object(executor, "execute") as mock_execute:
            mock_execute.return_value = ToolResult(success=True, output={"ok": True})
            _ = executor.invoke("echo", msg="hi")

        mock_execute.assert_called_once_with("echo", {"msg": "hi"}, node_name="")

    def test_invoke_rejects_ambiguous_node_name_input_conflict(self):
        """invoke returns validation error when tool input also defines node_name."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="tool_with_node_name",
                description="Tool with node_name input",
                category="testing",
                input_schema={"type": "object", "properties": {"node_name": {"type": "string"}}},
            ),
            fn=lambda node_name="": {"echoed": node_name},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        with patch.object(executor, "execute") as mock_execute:
            result = executor.invoke("tool_with_node_name", node_name="planning")

        assert result["success"] is False
        assert result["error_type"] == "validation_error"
        assert "Ambiguous invoke argument 'node_name'" in result["error_message"]
        mock_execute.assert_not_called()
