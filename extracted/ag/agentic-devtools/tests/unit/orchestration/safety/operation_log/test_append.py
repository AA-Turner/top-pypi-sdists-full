"""Tests for OperationLog.append() — atomic append with file locking."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


class TestAppend:
    """Tests for operation log append."""

    def test_appends_to_new_file(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        record = OperationLogRecord(operation_id="op1", run_id="run1", tool_name="tool", status="pending")
        log.append(record)
        log_file = tmp_path / "operation-log.ndjson"
        assert log_file.exists()
        lines = log_file.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["operation_id"] == "op1"
        assert data["status"] == "pending"

    def test_appends_multiple_records(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        log.append(OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="pending"))
        log.append(OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="completed"))
        log_file = tmp_path / "operation-log.ndjson"
        lines = log_file.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2

    def test_does_not_index_other_run_id(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        record = OperationLogRecord(operation_id="op1", run_id="other_run", tool_name="t", status="completed")
        log.append(record)
        assert log.lookup("op1") is None

    def test_insertion_order_updated_on_lifecycle_transition(self, tmp_path: Path) -> None:
        """Appending a later record for the same op_id updates insertion order."""
        log = OperationLog(tmp_path, "run1")
        log.append(OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="pending"))
        log.append(OperationLogRecord(operation_id="op2", run_id="run1", tool_name="t", status="pending"))
        log.append(OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="completed"))
        records = log.all_records()
        # op1's transition to "completed" happened after op2 was appended;
        # all_records() ordering must reflect last-seen position.
        assert records[-1].operation_id == "op1"
        assert records[-1].status == "completed"
        log = OperationLog(tmp_path, "run1")
        log.append(OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="pending"))
        assert log.lookup("op1").status == "pending"  # type: ignore[union-attr]
        log.append(
            OperationLogRecord(
                operation_id="op1",
                run_id="run1",
                tool_name="t",
                status="completed",
                result_payload={"result": "ok"},
            )
        )
        result = log.lookup("op1")
        assert result is not None
        assert result.status == "completed"
        assert result.result_payload == {"result": "ok"}
