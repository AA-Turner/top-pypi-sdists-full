"""Tests for OperationLog thread safety — concurrent append/lookup/all_records."""

from __future__ import annotations

import threading
from pathlib import Path

from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


class TestConcurrentAccess:
    """Tests for thread-safe concurrent access to the in-memory index."""

    def test_concurrent_appends_do_not_raise(self, tmp_path: Path) -> None:
        """Concurrent appends from multiple threads must not raise RuntimeError."""
        log = OperationLog(tmp_path, "run1")
        errors: list[Exception] = []
        thread_count = 20

        def writer(op_id: str) -> None:
            try:
                log.append(
                    OperationLogRecord(
                        operation_id=op_id,
                        run_id="run1",
                        tool_name="tool",
                        status="pending",
                    )
                )
                log.append(
                    OperationLogRecord(
                        operation_id=op_id,
                        run_id="run1",
                        tool_name="tool",
                        status="completed",
                        result_payload={"ok": True},
                    )
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=writer, args=(f"op-{i}",)) for i in range(thread_count)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Unexpected exceptions during concurrent appends: {errors}"

    def test_concurrent_lookup_during_append_does_not_raise(self, tmp_path: Path) -> None:
        """Concurrent lookup and append must not raise RuntimeError."""
        log = OperationLog(tmp_path, "run1")
        # Pre-populate some records
        for i in range(10):
            log.append(
                OperationLogRecord(
                    operation_id=f"op-{i}",
                    run_id="run1",
                    tool_name="tool",
                    status="pending",
                )
            )

        errors: list[Exception] = []
        stop_event = threading.Event()

        def reader() -> None:
            while not stop_event.is_set():
                try:
                    log.lookup("op-0")
                    log.all_records()
                except Exception as exc:  # noqa: BLE001
                    errors.append(exc)
                    stop_event.set()

        def writer() -> None:
            for i in range(100, 120):
                try:
                    log.append(
                        OperationLogRecord(
                            operation_id=f"op-{i}",
                            run_id="run1",
                            tool_name="tool",
                            status="completed",
                        )
                    )
                except Exception as exc:  # noqa: BLE001
                    errors.append(exc)
                    stop_event.set()
                    return

        reader_thread = threading.Thread(target=reader)
        writer_thread = threading.Thread(target=writer)
        reader_thread.start()
        writer_thread.start()
        writer_thread.join()
        stop_event.set()
        reader_thread.join()

        assert errors == [], f"Unexpected exceptions during concurrent access: {errors}"

    def test_all_records_snapshot_safe(self, tmp_path: Path) -> None:
        """all_records() returns a stable snapshot even when a writer mutates the index."""
        log = OperationLog(tmp_path, "run1")
        for i in range(5):
            log.append(
                OperationLogRecord(
                    operation_id=f"op-{i}",
                    run_id="run1",
                    tool_name="tool",
                    status="pending",
                )
            )

        snapshot = log.all_records()
        # Mutate the log concurrently
        log.append(
            OperationLogRecord(
                operation_id="op-new",
                run_id="run1",
                tool_name="tool",
                status="pending",
            )
        )
        # The previously captured snapshot must be unchanged
        assert len(snapshot) == 5
        assert all(r.operation_id != "op-new" for r in snapshot)
        # The live index reflects the new record
        assert log.lookup("op-new") is not None
