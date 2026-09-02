from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


class TestAccessorsAndTimestamp:
    """Tests for OperationLog metadata accessors."""

    def test_log_path_property_returns_log_path(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run-123")

        assert log.log_path == tmp_path / "operation-log.ndjson"

    def test_run_id_property_returns_run_id(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run-456")

        assert log.run_id == "run-456"

    def test_all_records_returns_index_values(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run-1")
        first = OperationLogRecord(operation_id="op-1", run_id="run-1", tool_name="tool", status="pending")
        second = OperationLogRecord(operation_id="op-2", run_id="run-1", tool_name="tool", status="completed")

        log.append(first)
        log.append(second)

        assert log.all_records() == [first, second]

    def test_get_timestamp_returns_utc_isoformat(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run-1")

        timestamp = log.get_timestamp()
        parsed = datetime.fromisoformat(timestamp)

        assert parsed.tzinfo == timezone.utc
