"""Tests for ToolExecutor integration with SafetyEnforcer."""

from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.orchestration.safety.enforcer import SafetyDecision
from agentic_devtools.orchestration.safety.exceptions import PolicyViolationError
from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


def _build_registry_with_tool() -> ConcreteToolRegistry:
    """Build a registry with a single test tool."""
    registry = ConcreteToolRegistry()
    registry.register(
        ToolDefinition(
            name="test_tool",
            description="A test tool",
            category="test",
            input_schema={},
            mutating=True,
            thread_safe=True,
            timeout_seconds=10.0,
        ),
        fn=lambda: {"result": "ok"},
    )
    return registry


class TestExecutorIntegration:
    """Tests for ToolExecutor with SafetyEnforcer injection."""

    def test_legacy_behavior_preserved_without_enforcer(self) -> None:
        """When no enforcer is injected, the legacy dry-run check works."""
        registry = _build_registry_with_tool()
        executor = ToolExecutor(registry, dry_run_fn=lambda: True)
        result = executor.execute("test_tool")
        assert result.success is True
        assert result.dry_run is True
        executor.shutdown(wait=False)

    def test_enforcer_simulate_returns_dry_run(self) -> None:
        """When enforcer returns 'simulate', executor returns dry_run result."""
        registry = _build_registry_with_tool()

        # Create a mock enforcer that returns simulate
        enforcer = MagicMock()
        enforcer.evaluate.return_value = SafetyDecision(action="simulate", reason="dry_run mode")

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        result = executor.execute("test_tool")
        assert result.success is True
        assert result.dry_run is True
        executor.shutdown(wait=False)

    def test_enforcer_execute_allows_through(self) -> None:
        """When enforcer returns 'execute', the tool runs normally."""
        registry = _build_registry_with_tool()

        enforcer = MagicMock()
        enforcer.evaluate.return_value = SafetyDecision(action="execute", reason="allowed")

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        result = executor.execute("test_tool")
        assert result.success is True
        assert result.output == {"result": "ok"}
        executor.shutdown(wait=False)

    def test_enforcer_exception_returns_error(self) -> None:
        """When enforcer raises, executor returns error result."""
        registry = _build_registry_with_tool()

        enforcer = MagicMock()
        enforcer.evaluate.side_effect = PolicyViolationError("test_tool", "restricted", "local_mutation")

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        result = executor.execute("test_tool")
        assert result.success is False
        assert result.error_type == "precondition_not_met"
        assert result.error_message is not None
        assert "Policy violation" in result.error_message
        executor.shutdown(wait=False)

    def test_enforcer_skip_duplicate_returns_replay(self) -> None:
        """When enforcer returns 'skip_duplicate', executor replays result."""
        registry = _build_registry_with_tool()

        from agentic_devtools.orchestration.safety.operation_log import OperationLogRecord

        replay_record = OperationLogRecord(
            operation_id="op1",
            run_id="run1",
            tool_name="test_tool",
            status="completed",
            result_payload={"replayed": True},
        )
        enforcer = MagicMock()
        enforcer.evaluate.return_value = SafetyDecision(
            action="skip_duplicate",
            reason="duplicate",
            replay_record=replay_record,
        )

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        result = executor.execute("test_tool")
        assert result.success is True
        assert result.output == {"replayed": True}
        executor.shutdown(wait=False)

    def test_enforcer_skip_duplicate_emits_skipped_duplicate_audit_status(self) -> None:
        """When enforcer returns 'skip_duplicate', audit status is 'skipped_duplicate'."""
        from unittest.mock import patch

        registry = _build_registry_with_tool()

        from agentic_devtools.orchestration.safety.operation_log import OperationLogRecord

        replay_record = OperationLogRecord(
            operation_id="op1",
            run_id="run1",
            tool_name="test_tool",
            status="completed",
            result_payload={"replayed": True},
        )
        enforcer = MagicMock()
        enforcer.evaluate.return_value = SafetyDecision(
            action="skip_duplicate",
            reason="duplicate",
            replay_record=replay_record,
        )

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        with patch("agentic_devtools.orchestration.tools.executor.emit_audit_log") as mock_emit:
            result = executor.execute("test_tool")
        assert result.success is True
        assert mock_emit.call_args.kwargs["status"] == "skipped_duplicate"
        executor.shutdown(wait=False)

    def test_enforcer_unknown_action_fails_closed(self) -> None:
        """Unknown SafetyDecision.action values must fail closed, not execute."""
        registry = _build_registry_with_tool()

        enforcer = MagicMock()
        enforcer.evaluate.return_value = SafetyDecision(action="mystery_action", reason="future value")

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        result = executor.execute("test_tool")
        assert result.success is False
        assert result.error_type == "precondition_not_met"
        assert result.error_message is not None
        assert "mystery_action" in result.error_message
        executor.shutdown(wait=False)

    def test_enforcer_execute_records_pending_and_completed(self) -> None:
        """When enforcer returns 'execute' with an operation_id, pending and
        completed lifecycle records are written to the operation log."""
        registry = _build_registry_with_tool()

        enforcer = MagicMock()
        enforcer.evaluate.return_value = SafetyDecision(action="execute", reason="allowed", operation_id="op-abc")

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        result = executor.execute("test_tool")
        assert result.success is True

        enforcer.record_pending.assert_called_once_with("test_tool", {}, "op-abc", node_name="")
        enforcer.record_completed.assert_called_once()
        completed_call = enforcer.record_completed.call_args
        assert completed_call.args[0] == "op-abc"
        assert completed_call.args[1] == "test_tool"
        executor.shutdown(wait=False)

    def test_enforcer_execute_records_failed_on_tool_error(self) -> None:
        """When enforcer returns 'execute' with an operation_id and the tool
        raises, record_failed is called instead of record_completed."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="failing_tool",
                description="A tool that fails",
                category="test",
                input_schema={},
                mutating=True,
                thread_safe=True,
                timeout_seconds=10.0,
            ),
            fn=lambda: (_ for _ in ()).throw(RuntimeError("boom")),  # always raises
        )

        enforcer = MagicMock()
        enforcer.evaluate.return_value = SafetyDecision(action="execute", reason="allowed", operation_id="op-fail")

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        result = executor.execute("failing_tool")
        assert result.success is False

        enforcer.record_pending.assert_called_once_with("failing_tool", {}, "op-fail", node_name="")
        enforcer.record_failed.assert_called_once()
        failed_call = enforcer.record_failed.call_args
        assert failed_call.args[0] == "op-fail"
        assert failed_call.args[1] == "failing_tool"
        executor.shutdown(wait=False)

    def test_enforcer_execute_tool_busy_records_failed(self) -> None:
        """When a non-thread-safe tool is busy, pending operation is marked failed."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="busy_tool",
                description="A tool that is not thread safe",
                category="test",
                input_schema={},
                mutating=True,
                thread_safe=False,
                timeout_seconds=10.0,
            ),
            fn=lambda: {"result": "ok"},
        )

        enforcer = MagicMock()
        enforcer.evaluate.return_value = SafetyDecision(action="execute", reason="allowed", operation_id="op-busy")

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        lock = executor._get_tool_lock("busy_tool")
        lock.acquire()
        try:
            result = executor.execute("busy_tool")
        finally:
            lock.release()

        assert result.success is False
        assert result.error_type == "precondition_not_met"
        assert result.error_message == "tool_busy"
        enforcer.record_pending.assert_called_once_with("busy_tool", {}, "op-busy", node_name="")
        enforcer.record_failed.assert_called_once_with("op-busy", "busy_tool", error_message="tool_busy", node_name="")
        enforcer.record_completed.assert_not_called()
        executor.shutdown(wait=False)

    def test_enforcer_execute_no_operation_id_skips_recording(self) -> None:
        """When enforcer returns 'execute' with no operation_id (read-only/local
        mutation tools), no operation log calls are made."""
        registry = _build_registry_with_tool()

        enforcer = MagicMock()
        enforcer.evaluate.return_value = SafetyDecision(action="execute", reason="allowed", operation_id=None)

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        result = executor.execute("test_tool")
        assert result.success is True

        enforcer.record_pending.assert_not_called()
        enforcer.record_completed.assert_not_called()
        enforcer.record_failed.assert_not_called()
        executor.shutdown(wait=False)

    def test_enforcer_block_returns_error(self) -> None:
        """When enforcer returns 'block', executor returns error result."""
        registry = _build_registry_with_tool()

        enforcer = MagicMock()
        enforcer.evaluate.return_value = SafetyDecision(
            action="block",
            reason="Branch protection: writes to 'main' are blocked",
        )

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        result = executor.execute("test_tool")
        assert result.success is False
        assert result.error_type == "precondition_not_met"
        assert result.error_message is not None
        assert "Branch protection" in result.error_message
        executor.shutdown(wait=False)

    def test_enforcer_timeout_leaves_pending_record(self) -> None:
        """On timeout, record_failed must NOT be called; the 'pending' record remains
        to block retries and prevent duplicate external-mutation side effects."""
        import time

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="slow_external",
                description="A slow external tool",
                category="test",
                input_schema={},
                mutating=True,
                thread_safe=True,
                timeout_seconds=0.1,
            ),
            fn=lambda: time.sleep(2) or {"result": "ok"},  # type: ignore[func-returns-value]
        )

        enforcer = MagicMock()
        enforcer.evaluate.return_value = SafetyDecision(action="execute", reason="allowed", operation_id="op-timeout")

        executor = ToolExecutor(registry, safety_enforcer=enforcer)
        result = executor.execute("slow_external")
        assert result.success is False
        assert result.error_type == "timeout"

        # The pending record must have been written before execution
        enforcer.record_pending.assert_called_once_with("slow_external", {}, "op-timeout", node_name="")
        # On timeout, neither completed nor failed must be called — pending stays
        enforcer.record_completed.assert_not_called()
        enforcer.record_failed.assert_not_called()
        executor.shutdown(wait=False)
