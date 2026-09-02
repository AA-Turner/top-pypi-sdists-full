"""Tests for OperationLog._build_index() — NDJSON parsing and recovery."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


class TestBuildIndex:
    """Tests for operation log index building."""

    def test_empty_file_returns_empty_index(self, tmp_path: Path) -> None:
        log_file = tmp_path / "operation-log.ndjson"
        log_file.write_text("", encoding="utf-8")
        log = OperationLog(tmp_path, "run1")
        assert log.lookup("op1") is None

    def test_missing_file_returns_empty_index(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        assert log.lookup("op1") is None

    def test_parses_valid_records(self, tmp_path: Path) -> None:
        record = OperationLogRecord(operation_id="op1", run_id="run1", tool_name="tool_a", status="completed")
        log_file = tmp_path / "operation-log.ndjson"
        log_file.write_text(json.dumps(record.to_dict()) + "\n", encoding="utf-8")
        log = OperationLog(tmp_path, "run1")
        result = log.lookup("op1")
        assert result is not None
        assert result.status == "completed"

    def test_skips_corrupted_lines(self, tmp_path: Path) -> None:
        good = json.dumps(
            OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="completed").to_dict()
        )
        log_file = tmp_path / "operation-log.ndjson"
        log_file.write_text(f"{good}\n{{invalid json\n{good}\n", encoding="utf-8")
        log = OperationLog(tmp_path, "run1")
        assert log.lookup("op1") is not None

    def test_insertion_order_reflects_last_occurrence(self, tmp_path: Path) -> None:
        """Index insertion order reflects last occurrence of each operation_id in the file."""
        r1 = OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="pending")
        r2 = OperationLogRecord(operation_id="op2", run_id="run1", tool_name="t", status="pending")
        r3 = OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="completed")
        log_file = tmp_path / "operation-log.ndjson"
        log_file.write_text(
            "\n".join(json.dumps(r.to_dict()) for r in [r1, r2, r3]) + "\n",
            encoding="utf-8",
        )
        log = OperationLog(tmp_path, "run1")
        records = log.all_records()
        # op1's last occurrence is after op2, so it must appear last in all_records().
        assert records[-1].operation_id == "op1"
        assert records[-1].status == "completed"

    def test_last_wins_semantics(self, tmp_path: Path) -> None:
        r1 = OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="pending")
        r2 = OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="completed")
        log_file = tmp_path / "operation-log.ndjson"
        lines = json.dumps(r1.to_dict()) + "\n" + json.dumps(r2.to_dict()) + "\n"
        log_file.write_text(lines, encoding="utf-8")
        log = OperationLog(tmp_path, "run1")
        result = log.lookup("op1")
        assert result is not None
        assert result.status == "completed"

    def test_only_indexes_matching_run_id(self, tmp_path: Path) -> None:
        r1 = OperationLogRecord(operation_id="op1", run_id="other_run", tool_name="t", status="completed")
        log_file = tmp_path / "operation-log.ndjson"
        log_file.write_text(json.dumps(r1.to_dict()) + "\n", encoding="utf-8")
        log = OperationLog(tmp_path, "run1")
        assert log.lookup("op1") is None
