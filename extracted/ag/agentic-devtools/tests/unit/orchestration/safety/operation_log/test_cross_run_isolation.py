"""Tests for cross-run isolation — different run_id does not trigger skip."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


class TestCrossRunIsolation:
    """Tests that operation log is properly scoped by run_id."""

    def test_different_run_id_does_not_trigger_skip(self, tmp_path: Path) -> None:
        """A completed record from run_id='A' should not affect lookups in run_id='B'."""
        # Write a completed record for run A
        record_a = OperationLogRecord(
            operation_id="op1",
            run_id="run_A",
            tool_name="tool",
            status="completed",
            result_payload={"data": "from_A"},
        )
        log_file = tmp_path / "operation-log.ndjson"
        log_file.write_text(json.dumps(record_a.to_dict()) + "\n", encoding="utf-8")

        # Open log as run B
        log_b = OperationLog(tmp_path, "run_B")
        assert log_b.lookup("op1") is None

    def test_same_run_id_triggers_lookup(self, tmp_path: Path) -> None:
        """A completed record from the same run should be found."""
        record = OperationLogRecord(
            operation_id="op1",
            run_id="run_X",
            tool_name="tool",
            status="completed",
            result_payload={"data": "val"},
        )
        log_file = tmp_path / "operation-log.ndjson"
        log_file.write_text(json.dumps(record.to_dict()) + "\n", encoding="utf-8")

        log = OperationLog(tmp_path, "run_X")
        result = log.lookup("op1")
        assert result is not None
        assert result.result_payload == {"data": "val"}
