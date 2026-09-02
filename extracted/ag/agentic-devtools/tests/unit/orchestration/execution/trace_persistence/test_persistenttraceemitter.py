"""Tests for PersistentTraceEmitter (JSONL writer)."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.orchestration.execution.trace_persistence import (
    PersistentTraceEmitter,
)
from agentic_devtools.orchestration.execution.tracing import TraceEvent


class TestPersistentTraceEmitter:
    """Tests for PersistentTraceEmitter file writing."""

    def test_emit_writes_jsonl(self, tmp_path: Path) -> None:
        """emit() appends JSONL records."""
        emitter = PersistentTraceEmitter(tmp_path, "run1")
        event = TraceEvent(
            timestamp=1000.0,
            node_name="test_node",
            operation_type="node_end",
            model_id="gpt-4",
            duration_ms=50.0,
            success=True,
            usage={"input_tokens": 10, "output_tokens": 5},
        )
        emitter.emit(event)

        trace_file = tmp_path / "orchestration" / "run1" / "execution-trace.jsonl"
        assert trace_file.exists()
        lines = trace_file.read_text().strip().split("\n")
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["node_name"] == "test_node"
        assert data["success"] is True

    def test_multiple_emits_append(self, tmp_path: Path) -> None:
        """Multiple emits append to the same file."""
        emitter = PersistentTraceEmitter(tmp_path, "run1")
        for i in range(5):
            event = TraceEvent(
                timestamp=float(i),
                node_name=f"node_{i}",
                operation_type="node_end",
                duration_ms=1.0,
                success=True,
            )
            emitter.emit(event)

        trace_file = tmp_path / "orchestration" / "run1" / "execution-trace.jsonl"
        lines = trace_file.read_text().strip().split("\n")
        assert len(lines) == 5

    def test_error_event(self, tmp_path: Path) -> None:
        """Failed events serialize correctly."""
        emitter = PersistentTraceEmitter(tmp_path, "run1")
        event = TraceEvent(
            timestamp=2000.0,
            node_name="failing_node",
            operation_type="node_end",
            model_id="claude",
            duration_ms=100.0,
            success=False,
            output_summary="timeout after 30s",
        )
        emitter.emit(event)

        trace_file = tmp_path / "orchestration" / "run1" / "execution-trace.jsonl"
        data = json.loads(trace_file.read_text().strip())
        assert data["success"] is False
        assert data["output_summary"] == "timeout after 30s"

    def test_concurrent_emits_no_corruption(self, tmp_path: Path) -> None:
        """Concurrent emit calls do not corrupt the JSONL file."""
        import threading

        emitter = PersistentTraceEmitter(tmp_path, "run1")

        def do_emit(node_id: int) -> None:
            event = TraceEvent(
                timestamp=float(node_id),
                node_name=f"node_{node_id}",
                operation_type="node_end",
                duration_ms=1.0,
                success=True,
            )
            emitter.emit(event)

        threads = [threading.Thread(target=do_emit, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        trace_file = tmp_path / "orchestration" / "run1" / "execution-trace.jsonl"
        lines = [ln for ln in trace_file.read_text().splitlines() if ln.strip()]
        assert len(lines) == 20
        for line in lines:
            json.loads(line)
