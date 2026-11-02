"""Tests for idempotency re-export shim."""

from __future__ import annotations


class TestReexports:
    """Verify re-exports from agentic_devtools.orchestration.idempotency."""

    def test_idempotency_registry_importable(self) -> None:
        from agentic_devtools.orchestration.execution.idempotency import (
            IdempotencyRegistry as Canonical,
        )
        from agentic_devtools.orchestration.idempotency import IdempotencyRegistry

        assert IdempotencyRegistry is Canonical

    def test_operation_log_importable(self) -> None:
        from agentic_devtools.orchestration.idempotency import OperationLog
        from agentic_devtools.orchestration.safety.operation_log import (
            OperationLog as Canonical,
        )

        assert OperationLog is Canonical

    def test_operation_log_record_importable(self) -> None:
        from agentic_devtools.orchestration.idempotency import OperationLogRecord
        from agentic_devtools.orchestration.safety.operation_log import (
            OperationLogRecord as Canonical,
        )

        assert OperationLogRecord is Canonical

    def test_compute_operation_id_importable(self) -> None:
        from agentic_devtools.orchestration.idempotency import compute_operation_id
        from agentic_devtools.orchestration.safety.operation_id import (
            compute_operation_id as Canonical,
        )

        assert compute_operation_id is Canonical

    def test_is_reconciliation_run_duplicate_importable(self) -> None:
        from agentic_devtools.orchestration import idempotency
        from agentic_devtools.orchestration.idempotency import (
            is_reconciliation_run_duplicate,
        )

        assert is_reconciliation_run_duplicate is idempotency.is_reconciliation_run_duplicate

    def test_all_exports_listed(self) -> None:
        from agentic_devtools.orchestration import idempotency

        assert set(idempotency.__all__) == {
            "IdempotencyRegistry",
            "OperationLog",
            "OperationLogRecord",
            "compute_operation_id",
            "is_reconciliation_run_duplicate",
        }
