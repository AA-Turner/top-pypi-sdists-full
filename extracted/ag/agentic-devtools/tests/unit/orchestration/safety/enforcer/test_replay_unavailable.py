"""Tests for replay-unavailable handling in SafetyEnforcer."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.safety.classification import (
    ActionClassification,
    ClassificationEntry,
    ClassificationRegistry,
)
from agentic_devtools.orchestration.safety.enforcer import SafetyEnforcer, SafetyPolicy
from agentic_devtools.orchestration.safety.exceptions import ReplayUnavailableError
from agentic_devtools.orchestration.safety.mode import ExecutionMode
from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


def _make_enforcer(tmp_path: Path, allow_fallback: bool = False) -> SafetyEnforcer:
    registry = ClassificationRegistry()
    registry.register(ClassificationEntry("ext_tool", ActionClassification.external_mutation))

    operation_log = OperationLog(tmp_path, "run1")
    policy = SafetyPolicy(
        execution_mode=ExecutionMode.live,
        allow_replay_fallback_reexecute=allow_fallback,
    )

    from unittest.mock import MagicMock

    branch_guard = MagicMock()
    branch_guard.check = MagicMock()
    worktree_guard = MagicMock()
    worktree_guard.check = MagicMock()

    return SafetyEnforcer(
        policy=policy,
        classification_registry=registry,
        operation_log=operation_log,
        branch_guard=branch_guard,
        worktree_guard=worktree_guard,
    )


class TestReplayUnavailable:
    """Tests that missing replay payload raises ReplayUnavailableError."""

    def test_missing_payload_raises(self, tmp_path: Path) -> None:
        enforcer = _make_enforcer(tmp_path, allow_fallback=False)
        inputs = {"key": "value"}

        from agentic_devtools.orchestration.safety.operation_id import compute_operation_id

        op_id = compute_operation_id("test_node", "ext_tool", inputs, ())
        enforcer.operation_log.append(  # type: ignore[union-attr]
            OperationLogRecord(
                operation_id=op_id,
                run_id="run1",
                tool_name="ext_tool",
                status="completed",
                result_payload=None,
            )
        )

        with pytest.raises(ReplayUnavailableError, match=op_id):
            enforcer.evaluate("ext_tool", inputs, node_name="test_node")

    def test_missing_payload_with_fallback_allows_execution(self, tmp_path: Path) -> None:
        enforcer = _make_enforcer(tmp_path, allow_fallback=True)
        inputs = {"key": "value"}

        from agentic_devtools.orchestration.safety.operation_id import compute_operation_id

        op_id = compute_operation_id("test_node", "ext_tool", inputs, ())
        enforcer.operation_log.append(  # type: ignore[union-attr]
            OperationLogRecord(
                operation_id=op_id,
                run_id="run1",
                tool_name="ext_tool",
                status="completed",
                result_payload=None,
            )
        )

        decision = enforcer.evaluate("ext_tool", inputs, node_name="test_node")
        assert decision.action == "execute"
