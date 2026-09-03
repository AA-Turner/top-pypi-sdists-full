"""Tests for is_reconciliation_run_duplicate()."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.idempotency import (
    IdempotencyStateUnknownError,
    OperationLog,
    OperationLogRecord,
    is_reconciliation_run_duplicate,
)


class TestIsReconciliationRunDuplicate:
    """Tests for duplicate reconciliation detection."""

    def test_raises_when_log_file_missing(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-1")
        with pytest.raises(IdempotencyStateUnknownError):
            is_reconciliation_run_duplicate(log, "run-1", "op-1")

    def test_returns_true_for_completed_record(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-1")
        log.append(
            OperationLogRecord(
                operation_id="op-1",
                run_id="run-1",
                tool_name="tool",
                status="completed",
            )
        )
        assert is_reconciliation_run_duplicate(log, "run-1", "op-1") is True

    def test_returns_false_for_failed_record(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-1")
        log.append(
            OperationLogRecord(
                operation_id="op-1",
                run_id="run-1",
                tool_name="tool",
                status="failed",
            )
        )
        assert is_reconciliation_run_duplicate(log, "run-1", "op-1") is False

    def test_raises_for_unrecognized_status_in_file_scan(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-2")
        log.log_path.write_text(
            '{"operation_id":"op-1","run_id":"run-1","tool_name":"tool","status":"unknown"}\n',
            encoding="utf-8",
        )
        with pytest.raises(IdempotencyStateUnknownError, match="unrecognized status"):
            is_reconciliation_run_duplicate(log, "run-2", "op-1")

    def test_raises_for_pending_record_in_lookup_cache(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-1")
        log.append(
            OperationLogRecord(
                operation_id="op-1",
                run_id="run-1",
                tool_name="tool",
                status="pending",
            )
        )
        with pytest.raises(IdempotencyStateUnknownError, match="pending"):
            is_reconciliation_run_duplicate(log, "run-1", "op-1")

    def test_returns_true_when_prior_completed_record_exists_in_another_run(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-1")
        log.append(
            OperationLogRecord(
                operation_id="op-1",
                run_id="run-1",
                tool_name="tool",
                status="completed",
            )
        )
        second_run_log = OperationLog(state_dir=tmp_path, run_id="run-2")
        assert is_reconciliation_run_duplicate(second_run_log, "run-2", "op-1") is True

    def test_same_log_object_with_different_run_id_falls_back_to_file_scan(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-1")
        log.append(OperationLogRecord(operation_id="op-1", run_id="run-1", tool_name="tool", status="completed"))
        assert is_reconciliation_run_duplicate(log, "run-2", "op-1") is True

    def test_raises_when_log_file_cannot_be_read(self, tmp_path, monkeypatch) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-1")
        log.append(OperationLogRecord(operation_id="op-1", run_id="run-1", tool_name="tool", status="failed"))
        monkeypatch.setattr(
            type(log.log_path),
            "read_text",
            lambda self, encoding="utf-8": (_ for _ in ()).throw(OSError("boom")),
        )
        with pytest.raises(IdempotencyStateUnknownError):
            is_reconciliation_run_duplicate(log, "run-2", "op-1")

    def test_malformed_json_line_raises_unknown_state(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-2")
        log.log_path.write_text(
            "\n".join(
                [
                    '{"operation_id":"other","run_id":"run-1","tool_name":"tool","status":"completed"}',
                    '{"operation_id":"op-1","run_id":"run-1","tool_name":"tool","status":"completed"}',
                    "{not-json",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        with pytest.raises(IdempotencyStateUnknownError, match="malformed JSON"):
            is_reconciliation_run_duplicate(log, "run-2", "op-1")

    def test_malformed_operation_record_raises_unknown_state(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-2")
        log.log_path.write_text(
            "\n".join(
                [
                    '{"operation_id":"op-1","run_id":"run-1","tool_name":"tool","status":"completed"}',
                    '{"operation_id":"op-1"}',
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        with pytest.raises(IdempotencyStateUnknownError, match="malformed operation records"):
            is_reconciliation_run_duplicate(log, "run-2", "op-1")

    def test_non_object_json_line_raises_unknown_state(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-2")
        log.log_path.write_text(
            "\n".join(
                [
                    '{"operation_id":"op-1","run_id":"run-1","tool_name":"tool","status":"completed"}',
                    '["not-an-object"]',
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        with pytest.raises(IdempotencyStateUnknownError, match="non-object"):
            is_reconciliation_run_duplicate(log, "run-2", "op-2")

    def test_pending_record_in_file_scan_raises_unknown_state(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-2")
        log.log_path.write_text(
            "\n".join(
                [
                    '{"operation_id":"op-1","run_id":"run-1","tool_name":"tool","status":"pending"}',
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        with pytest.raises(IdempotencyStateUnknownError, match="pending"):
            is_reconciliation_run_duplicate(log, "run-2", "op-1")

    def test_prior_run_completion_takes_precedence_over_same_run_failure(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-1")
        log.log_path.write_text(
            "\n".join(
                [
                    '{"operation_id":"op-1","run_id":"run-0","tool_name":"tool","status":"completed"}',
                    '{"operation_id":"op-1","run_id":"run-1","tool_name":"tool","status":"failed"}',
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        assert is_reconciliation_run_duplicate(log, "run-1", "op-1") is True

    def test_returns_false_when_matching_record_never_appears(self, tmp_path) -> None:
        log = OperationLog(state_dir=tmp_path, run_id="run-2")
        log.log_path.write_text(
            "\n".join(
                [
                    "",
                    '{"operation_id":"other","run_id":"run-1","tool_name":"tool","status":"completed"}',
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        assert is_reconciliation_run_duplicate(log, "run-2", "op-1") is False
