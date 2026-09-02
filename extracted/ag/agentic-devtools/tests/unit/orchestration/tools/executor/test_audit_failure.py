"""Tests for ToolExecutor audit log failure handling."""

from unittest.mock import patch

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestAuditFailure:
    """Tests for audit emit exception swallowing."""

    def test_audit_failure_does_not_propagate(self):
        """When emit_audit_log raises, execute still returns a result."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="echo",
                description="Echo",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=lambda: {"ok": True},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)

        with patch(
            "agentic_devtools.orchestration.tools.executor.emit_audit_log",
            side_effect=RuntimeError("audit broken"),
        ):
            result = executor.execute("echo")

        assert result.success is True
        assert result.output == {"ok": True}
