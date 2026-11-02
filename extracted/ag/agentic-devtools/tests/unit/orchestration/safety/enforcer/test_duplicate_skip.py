"""Tests for duplicate-skip flow in SafetyEnforcer."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.safety.classification import (
    ActionClassification,
    ClassificationEntry,
    ClassificationRegistry,
)
from agentic_devtools.orchestration.safety.enforcer import SafetyEnforcer, SafetyPolicy
from agentic_devtools.orchestration.safety.mode import ExecutionMode
from agentic_devtools.orchestration.safety.operation_id import compute_operation_id
from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


def _make_enforcer_with_log(tmp_path: Path) -> SafetyEnforcer:
    """Create an enforcer with operation log for idempotency tests."""
    registry = ClassificationRegistry()
    registry.register(ClassificationEntry("ext_tool", ActionClassification.external_mutation))

    operation_log = OperationLog(tmp_path, "run1")
    policy = SafetyPolicy(execution_mode=ExecutionMode.live)

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


class TestDuplicateSkip:
    """Tests that completed records trigger skip with replay."""

    def test_completed_record_triggers_skip(self, tmp_path: Path) -> None:
        enforcer = _make_enforcer_with_log(tmp_path)
        inputs = {"key": "value"}

        op_id = compute_operation_id("test_node", "ext_tool", inputs, ())
        enforcer.operation_log.append(  # type: ignore[union-attr]
            OperationLogRecord(
                operation_id=op_id,
                run_id="run1",
                tool_name="ext_tool",
                status="completed",
                result_payload={"output": "data"},
            )
        )

        decision = enforcer.evaluate("ext_tool", inputs, node_name="test_node")
        assert decision.action == "skip_duplicate"
        assert decision.replay_record is not None
        assert decision.replay_record.result_payload == {"output": "data"}

    def test_skip_appends_skipped_record(self, tmp_path: Path) -> None:
        enforcer = _make_enforcer_with_log(tmp_path)
        inputs = {"key": "value"}

        op_id = compute_operation_id("test_node", "ext_tool", inputs, ())
        enforcer.operation_log.append(  # type: ignore[union-attr]
            OperationLogRecord(
                operation_id=op_id,
                run_id="run1",
                tool_name="ext_tool",
                status="completed",
                result_payload={"output": "data"},
            )
        )

        enforcer.evaluate("ext_tool", inputs, node_name="test_node")

        # The last record should be "skipped"
        last = enforcer.operation_log.lookup(op_id)  # type: ignore[union-attr]
        assert last is not None
        assert last.status == "skipped"
        assert last.skip_reason is not None

    def test_skip_record_carries_node_name_for_audit(self, tmp_path: Path) -> None:
        """Skipped-duplicate record carries node_name for cross-node audit traceability."""
        enforcer = _make_enforcer_with_log(tmp_path)
        inputs = {"key": "value"}

        op_id = compute_operation_id("planning_node", "ext_tool", inputs, ())
        enforcer.operation_log.append(  # type: ignore[union-attr]
            OperationLogRecord(
                operation_id=op_id,
                run_id="run1",
                tool_name="ext_tool",
                status="completed",
                result_payload={"output": "done"},
            )
        )

        enforcer.evaluate("ext_tool", inputs, node_name="planning_node")

        last = enforcer.operation_log.lookup(op_id)  # type: ignore[union-attr]
        assert last is not None
        assert last.node_name == "planning_node"

    def test_third_duplicate_evaluation_replays_from_skipped_record(self, tmp_path: Path) -> None:
        enforcer = _make_enforcer_with_log(tmp_path)
        inputs = {"key": "value"}

        op_id = compute_operation_id("test_node", "ext_tool", inputs, ())
        enforcer.operation_log.append(  # type: ignore[union-attr]
            OperationLogRecord(
                operation_id=op_id,
                run_id="run1",
                tool_name="ext_tool",
                status="completed",
                result_payload={"output": "data"},
            )
        )

        first_duplicate = enforcer.evaluate("ext_tool", inputs, node_name="test_node")
        second_duplicate = enforcer.evaluate("ext_tool", inputs, node_name="test_node")

        assert first_duplicate.action == "skip_duplicate"
        assert first_duplicate.replay_record is not None
        assert first_duplicate.replay_record.result_payload == {"output": "data"}
        assert second_duplicate.action == "skip_duplicate"
        assert second_duplicate.replay_record is not None
        assert second_duplicate.replay_record.result_payload == {"output": "data"}

    def test_prior_completion_timestamp_chains_to_original(self, tmp_path: Path) -> None:
        """prior_completion_timestamp always reflects the original completed record's timestamp.

        On the second duplicate evaluation the prior record is itself a skipped-duplicate.
        The new skipped record must carry the *original* completion timestamp, not the skip
        timestamp — so the audit field does not drift across chains.
        """
        enforcer = _make_enforcer_with_log(tmp_path)
        inputs = {"key": "chain-test"}

        original_ts = "2024-01-01T00:00:00+00:00"
        op_id = compute_operation_id("test_node", "ext_tool", inputs, ())
        enforcer.operation_log.append(  # type: ignore[union-attr]
            OperationLogRecord(
                operation_id=op_id,
                run_id="run1",
                tool_name="ext_tool",
                status="completed",
                execution_timestamp=original_ts,
                result_payload={"output": "data"},
            )
        )

        # First duplicate skip — prior_completion_timestamp should be original_ts
        enforcer.evaluate("ext_tool", inputs, node_name="test_node")
        first_skip = enforcer.operation_log.lookup(op_id)  # type: ignore[union-attr]
        assert first_skip is not None
        assert first_skip.status == "skipped"
        assert first_skip.prior_completion_timestamp == original_ts

        # Second duplicate skip — prior is now a skipped record; must still carry original_ts
        enforcer.evaluate("ext_tool", inputs, node_name="test_node")
        second_skip = enforcer.operation_log.lookup(op_id)  # type: ignore[union-attr]
        assert second_skip is not None
        assert second_skip.status == "skipped"
        assert second_skip.prior_completion_timestamp == original_ts, (
            "prior_completion_timestamp must chain to the original completion, not the skip timestamp"
        )
