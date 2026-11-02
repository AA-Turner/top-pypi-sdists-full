"""Tests for OperationLog.lookup() — run_id scoping and last-wins."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


class TestLookup:
    """Tests for operation log lookup."""

    def test_returns_none_for_missing_operation(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        assert log.lookup("nonexistent") is None

    def test_returns_record_for_current_run(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        record = OperationLogRecord(operation_id="op1", run_id="run1", tool_name="tool", status="completed")
        log.append(record)
        result = log.lookup("op1")
        assert result is not None
        assert result.status == "completed"

    def test_last_wins_after_append(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        log.append(OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="pending"))
        log.append(OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="completed"))
        result = log.lookup("op1")
        assert result is not None
        assert result.status == "completed"
