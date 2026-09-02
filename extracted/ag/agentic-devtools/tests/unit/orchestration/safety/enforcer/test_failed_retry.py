"""Tests for failed retry — failed prior permits re-execution."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.safety.classification import (
    ActionClassification,
    ClassificationEntry,
    ClassificationRegistry,
)
from agentic_devtools.orchestration.safety.enforcer import SafetyEnforcer, SafetyPolicy
from agentic_devtools.orchestration.safety.mode import ExecutionMode
from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


class TestFailedRetry:
    """Tests that a failed prior attempt permits re-execution."""

    def test_failed_record_allows_retry(self, tmp_path: Path) -> None:
        registry = ClassificationRegistry()
        registry.register(ClassificationEntry("ext_tool", ActionClassification.external_mutation))

        operation_log = OperationLog(tmp_path, "run1")
        policy = SafetyPolicy(execution_mode=ExecutionMode.live)

        from unittest.mock import MagicMock

        branch_guard = MagicMock()
        branch_guard.check = MagicMock()
        worktree_guard = MagicMock()
        worktree_guard.check = MagicMock()

        enforcer = SafetyEnforcer(
            policy=policy,
            classification_registry=registry,
            operation_log=operation_log,
            branch_guard=branch_guard,
            worktree_guard=worktree_guard,
        )

        inputs = {"key": "value"}
        from agentic_devtools.orchestration.safety.operation_id import compute_operation_id

        op_id = compute_operation_id("test_node", "ext_tool", inputs, ())
        operation_log.append(
            OperationLogRecord(
                operation_id=op_id,
                run_id="run1",
                tool_name="ext_tool",
                status="failed",
                result_summary="connection error",
            )
        )

        decision = enforcer.evaluate("ext_tool", inputs, node_name="test_node")
        assert decision.action == "execute"
