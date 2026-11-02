from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.orchestration.safety.classification import (
    ActionClassification,
    ClassificationEntry,
    ClassificationRegistry,
)
from agentic_devtools.orchestration.safety.enforcer import SafetyEnforcer, SafetyPolicy
from agentic_devtools.orchestration.safety.mode import ExecutionMode
from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


def _make_registry() -> ClassificationRegistry:
    registry = ClassificationRegistry()
    registry.register(ClassificationEntry("ext_tool", ActionClassification.external_mutation))
    return registry


def _make_enforcer(operation_log: OperationLog | None = None) -> SafetyEnforcer:
    branch_guard = MagicMock()
    worktree_guard = MagicMock()
    return SafetyEnforcer(
        policy=SafetyPolicy(execution_mode=ExecutionMode.dry_run),
        classification_registry=_make_registry(),
        operation_log=operation_log,
        branch_guard=branch_guard,
        worktree_guard=worktree_guard,
    )


class TestRecording:
    """Tests for SafetyEnforcer accessors and record helpers."""

    def test_policy_property_returns_policy(self) -> None:
        policy = SafetyPolicy(execution_mode=ExecutionMode.restricted)
        enforcer = SafetyEnforcer(policy=policy, classification_registry=_make_registry())

        assert enforcer.policy is policy

    def test_record_methods_noop_without_operation_log(self) -> None:
        enforcer = _make_enforcer(operation_log=None)

        enforcer.record_pending("ext_tool", {"value": 1}, "ext_tool:abcd")
        enforcer.record_completed("ext_tool:abcd", "ext_tool", result_summary="done")
        enforcer.record_failed("ext_tool:abcd", "ext_tool", error_message="boom")

    def test_record_pending_appends_pending_record(self) -> None:
        operation_log = MagicMock()
        operation_log.run_id = "run-1"
        operation_log.get_timestamp.return_value = "2024-01-01T00:00:00+00:00"
        enforcer = _make_enforcer(operation_log=operation_log)

        enforcer.record_pending("ext_tool", {"value": 1}, "ext_tool:abcd1234")

        record = operation_log.append.call_args.args[0]
        assert isinstance(record, OperationLogRecord)
        assert record.operation_id == "ext_tool:abcd1234"
        assert record.run_id == "run-1"
        assert record.tool_name == "ext_tool"
        assert record.input_hash == "abcd1234"
        assert record.execution_mode == "dry_run"
        assert record.status == "pending"

    def test_record_completed_appends_completed_record(self) -> None:
        operation_log = MagicMock()
        operation_log.run_id = "run-2"
        operation_log.get_timestamp.return_value = "2024-01-01T00:00:01+00:00"
        enforcer = _make_enforcer(operation_log=operation_log)

        enforcer.record_completed(
            "ext_tool:done",
            "ext_tool",
            result_summary="finished",
            result_payload={"ok": True},
        )

        record = operation_log.append.call_args.args[0]
        assert isinstance(record, OperationLogRecord)
        assert record.operation_id == "ext_tool:done"
        assert record.run_id == "run-2"
        assert record.tool_name == "ext_tool"
        assert record.execution_mode == "dry_run"
        assert record.status == "completed"
        assert record.result_summary == "finished"
        assert record.result_payload == {"ok": True}

    def test_record_failed_appends_failed_record(self) -> None:
        operation_log = MagicMock()
        operation_log.run_id = "run-3"
        operation_log.get_timestamp.return_value = "2024-01-01T00:00:02+00:00"
        enforcer = _make_enforcer(operation_log=operation_log)

        enforcer.record_failed("ext_tool:failed", "ext_tool", error_message="boom")

        record = operation_log.append.call_args.args[0]
        assert isinstance(record, OperationLogRecord)
        assert record.operation_id == "ext_tool:failed"
        assert record.run_id == "run-3"
        assert record.tool_name == "ext_tool"
        assert record.execution_mode == "dry_run"
        assert record.status == "failed"
        assert record.result_summary == "boom"

    def test_check_idempotency_returns_none_without_prior_record(self) -> None:
        operation_log = MagicMock()
        operation_log.lookup.return_value = None
        enforcer = _make_enforcer(operation_log=operation_log)

        decision = enforcer._check_idempotency("ext_tool:abc", "ext_tool")

        assert decision is None
        operation_log.lookup.assert_called_once_with("ext_tool:abc")

    def test_check_idempotency_allows_skipped_prior_status(self) -> None:
        operation_log = MagicMock()
        operation_log.lookup.return_value = OperationLogRecord(
            operation_id="ext_tool:abc",
            run_id="run-1",
            tool_name="ext_tool",
            status="skipped",
        )
        enforcer = _make_enforcer(operation_log=operation_log)

        decision = enforcer._check_idempotency("ext_tool:abc", "ext_tool")

        assert decision is None

    def test_record_pending_propagates_node_name(self) -> None:
        """record_pending stores node_name on the log record (FR-006)."""
        operation_log = MagicMock()
        operation_log.run_id = "run-4"
        operation_log.get_timestamp.return_value = "2024-01-01T00:00:03+00:00"
        enforcer = _make_enforcer(operation_log=operation_log)

        enforcer.record_pending("ext_tool", {"v": 1}, "ext_tool:xyzxyz", node_name="planning")

        record = operation_log.append.call_args.args[0]
        assert record.node_name == "planning"

    def test_record_completed_propagates_node_name(self) -> None:
        """record_completed stores node_name on the log record (FR-006)."""
        operation_log = MagicMock()
        operation_log.run_id = "run-5"
        operation_log.get_timestamp.return_value = "2024-01-01T00:00:04+00:00"
        enforcer = _make_enforcer(operation_log=operation_log)

        enforcer.record_completed("ext_tool:done", "ext_tool", result_summary="ok", node_name="implementation")

        record = operation_log.append.call_args.args[0]
        assert record.node_name == "implementation"

    def test_record_failed_propagates_node_name(self) -> None:
        """record_failed stores node_name on the log record (FR-006)."""
        operation_log = MagicMock()
        operation_log.run_id = "run-6"
        operation_log.get_timestamp.return_value = "2024-01-01T00:00:05+00:00"
        enforcer = _make_enforcer(operation_log=operation_log)

        enforcer.record_failed("ext_tool:fail", "ext_tool", error_message="err", node_name="commit")

        record = operation_log.append.call_args.args[0]
        assert record.node_name == "commit"
