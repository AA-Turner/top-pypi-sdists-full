"""Tests for write_execution_summary()."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.orchestration.execution.trace_persistence import (
    PersistentTraceEmitter,
    write_execution_summary,
)
from agentic_devtools.orchestration.execution.tracing import TraceEvent


class TestWriteExecutionSummary:
    """Tests for write_execution_summary() generation."""

    def test_generates_summary_from_records(self, tmp_path: Path) -> None:
        """Summary file contains aggregated stats."""
        emitter = PersistentTraceEmitter(tmp_path, "run1")
        events = [
            TraceEvent(
                timestamp=1.0,
                node_name="node_a",
                operation_type="node_end",
                model_id="gpt-4",
                duration_ms=100.0,
                success=True,
                usage={"input_tokens": 10, "output_tokens": 5},
            ),
            TraceEvent(
                timestamp=2.0,
                node_name="node_b",
                operation_type="node_end",
                model_id="gpt-4",
                duration_ms=200.0,
                success=True,
                usage={"input_tokens": 20, "output_tokens": 10},
            ),
            TraceEvent(
                timestamp=3.0,
                node_name="node_c",
                operation_type="node_end",
                duration_ms=50.0,
                success=False,
            ),
        ]
        for e in events:
            emitter.emit(e)

        write_execution_summary(tmp_path, "run1")

        summary_path = tmp_path / "orchestration" / "run1" / "execution-trace-summary.json"
        assert summary_path.exists()
        summary = json.loads(summary_path.read_text())
        assert summary["total_nodes"] == 3
        assert summary["outcomes"]["success"] == 2
        assert summary["outcomes"]["failed"] == 1

    def test_empty_trace_produces_summary(self, tmp_path: Path) -> None:
        """Empty trace file produces a valid summary with zeros."""
        trace_dir = tmp_path / "orchestration" / "run1"
        trace_dir.mkdir(parents=True)
        (trace_dir / "execution-trace.jsonl").write_text("")

        write_execution_summary(tmp_path, "run1")

        summary_path = trace_dir / "execution-trace-summary.json"
        summary = json.loads(summary_path.read_text())
        assert summary["total_nodes"] == 0

    def test_missing_trace_file_produces_empty_summary(self, tmp_path: Path) -> None:
        """Missing trace file still writes a zero summary if dir exists."""
        # Create the directory but NOT the trace file
        trace_dir = tmp_path / "orchestration" / "run_empty"
        trace_dir.mkdir(parents=True)

        write_execution_summary(tmp_path, "run_empty")

        summary_path = trace_dir / "execution-trace-summary.json"
        assert summary_path.exists()
        summary = json.loads(summary_path.read_text())
        assert summary["total_nodes"] == 0
