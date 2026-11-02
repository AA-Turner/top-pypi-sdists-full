"""Tests for query_operation_log() — FR-010."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord
from agentic_devtools.orchestration.safety.query import query_operation_log


class TestQueryOperationLog:
    """Tests for operation log query surface."""

    def test_no_filters_returns_all(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        log.append(OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t1", status="completed"))
        log.append(OperationLogRecord(operation_id="op2", run_id="run1", tool_name="t2", status="failed"))
        results = query_operation_log(log)
        assert len(results) == 2

    def test_filter_by_tool_name(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        log.append(OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t1", status="completed"))
        log.append(OperationLogRecord(operation_id="op2", run_id="run1", tool_name="t2", status="completed"))
        results = query_operation_log(log, tool_name="t1")
        assert len(results) == 1
        assert results[0].tool_name == "t1"

    def test_filter_by_status(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        log.append(OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="completed"))
        log.append(OperationLogRecord(operation_id="op2", run_id="run1", tool_name="t", status="failed"))
        results = query_operation_log(log, status="failed")
        assert len(results) == 1
        assert results[0].status == "failed"

    def test_filter_by_run_id(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        log.append(OperationLogRecord(operation_id="op1", run_id="run1", tool_name="t", status="completed"))
        log.append(OperationLogRecord(operation_id="op2", run_id="run1", tool_name="t", status="completed"))
        # Filter to matching run_id returns all records in this log
        results = query_operation_log(log, run_id="run1")
        assert len(results) == 2
        # Filter to a non-matching run_id fails fast for this scoped log
        with pytest.raises(ValueError, match="does not match OperationLog run_id"):
            query_operation_log(log, run_id="run_other")

    def test_limit(self, tmp_path: Path) -> None:
        log = OperationLog(tmp_path, "run1")
        for i in range(5):
            log.append(OperationLogRecord(operation_id=f"op{i}", run_id="run1", tool_name="t", status="completed"))
        results = query_operation_log(log, limit=3)
        assert len(results) == 3
