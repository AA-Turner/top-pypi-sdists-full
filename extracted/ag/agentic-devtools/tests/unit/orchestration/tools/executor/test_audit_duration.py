"""Tests that audit log uses result.duration_ms, not a re-measured value."""

from unittest.mock import patch

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestAuditDuration:
    """Verify audit emission uses ToolResult.duration_ms (no re-measurement)."""

    def _make_executor(self, fn=None, *, mutating=False):
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="tool",
                description="Tool",
                category="testing",
                input_schema={"type": "object", "properties": {}},
                mutating=mutating,
            ),
            fn=fn or (lambda: {"ok": True}),
        )
        return ToolExecutor(registry, dry_run_fn=lambda: False)

    def test_audit_duration_matches_result_duration(self):
        """Audit log receives the same duration_ms as the returned ToolResult."""
        executor = self._make_executor()

        with patch("agentic_devtools.orchestration.tools.executor.emit_audit_log") as mock_audit:
            result = executor.execute("tool")

        assert result.success is True
        assert result.duration_ms > 0
        assert mock_audit.call_count == 1
        # The duration_ms forwarded to emit_audit_log must equal result.duration_ms
        # exactly (no re-measurement inside _emit_audit).
        kwargs = mock_audit.call_args.kwargs
        assert kwargs["duration_ms"] == result.duration_ms

    def test_audit_duration_matches_result_on_not_found(self):
        """not_found path also populates result.duration_ms and forwards it to audit."""
        registry = ConcreteToolRegistry()
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)

        with patch("agentic_devtools.orchestration.tools.executor.emit_audit_log") as mock_audit:
            result = executor.execute("missing_tool")

        assert result.success is False
        assert result.error_type == "not_found"
        assert result.duration_ms >= 0
        kwargs = mock_audit.call_args.kwargs
        assert kwargs["duration_ms"] == result.duration_ms

    def test_audit_duration_matches_result_on_validation_error(self):
        """validation_error path forwards result.duration_ms to audit."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="strict",
                description="Strict",
                category="testing",
                input_schema={
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"],
                },
            ),
            fn=lambda name: name,
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)

        with patch("agentic_devtools.orchestration.tools.executor.emit_audit_log") as mock_audit:
            result = executor.execute("strict", {})

        assert result.success is False
        assert result.error_type == "validation_error"
        kwargs = mock_audit.call_args.kwargs
        assert kwargs["duration_ms"] == result.duration_ms
