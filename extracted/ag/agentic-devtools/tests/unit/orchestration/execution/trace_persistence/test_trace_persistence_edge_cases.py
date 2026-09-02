"""Tests for PersistentTraceEmitter — error handling and trace_path property."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.orchestration.execution.trace_persistence import (
    PersistentTraceEmitter,
    write_execution_summary,
)
from agentic_devtools.orchestration.execution.tracing import TraceEvent


class TestPersistentTraceEmitterErrors:
    """Tests for PersistentTraceEmitter error paths."""

    def test_invalid_run_id_raises_valueerror(self, tmp_path: Path) -> None:
        """Path-like run IDs are rejected before constructing trace paths."""
        with patch("agentic_devtools.orchestration.execution.trace_persistence.locked_file"):
            with pytest.raises(ValueError, match="run_id"):
                PersistentTraceEmitter(tmp_path, "../escape")

    def test_trace_path_property(self, tmp_path: Path) -> None:
        """trace_path returns the correct path."""
        emitter = PersistentTraceEmitter(tmp_path, "run_abc")
        expected = tmp_path / "orchestration" / "run_abc" / "execution-trace.jsonl"
        assert emitter.trace_path == expected

    def test_emit_failure_swallowed(self, tmp_path: Path) -> None:
        """Emit failures are swallowed (logged to stderr)."""
        emitter = PersistentTraceEmitter(tmp_path, "run1")
        event = TraceEvent(
            timestamp=1000.0,
            node_name="test_node",
            operation_type="node_end",
            duration_ms=50.0,
            success=True,
        )
        # Make the trace path unwritable
        emitter._trace_path.parent.mkdir(parents=True, exist_ok=True)
        emitter._trace_path.write_text("")
        emitter._trace_path.chmod(0o000)

        try:
            # Should NOT raise despite write failure
            emitter.emit(event)
        finally:
            emitter._trace_path.chmod(0o644)


class TestWriteExecutionSummaryEdgeCases:
    """Tests for write_execution_summary() edge cases."""

    def test_invalid_run_id_raises_valueerror(self, tmp_path: Path) -> None:
        """Path-like run IDs are rejected before writing the summary path."""
        with pytest.raises(ValueError, match="run_id"):
            write_execution_summary(tmp_path, "../escape")

    def test_corrupt_trace_file(self, tmp_path: Path) -> None:
        """Corrupt trace file produces a valid summary (graceful degradation)."""
        trace_dir = tmp_path / "orchestration" / "run1"
        trace_dir.mkdir(parents=True)
        (trace_dir / "execution-trace.jsonl").write_text("not valid json\n")

        write_execution_summary(tmp_path, "run1")

        summary_path = trace_dir / "execution-trace-summary.json"
        summary = json.loads(summary_path.read_text())
        assert summary["total_nodes"] == 0

    def test_missing_trace_dir_is_created(self, tmp_path: Path) -> None:
        """Summary file is written even when trace directory does not exist yet."""
        run_id = "new_run"
        write_execution_summary(tmp_path, run_id)
        summary_path = tmp_path / "orchestration" / run_id / "execution-trace-summary.json"
        assert summary_path.exists()

    def test_records_with_usage_variants(self, tmp_path: Path) -> None:
        """Summary handles both prompt_tokens and input_tokens usage keys."""
        emitter = PersistentTraceEmitter(tmp_path, "run1")

        # Event with prompt_tokens style
        e1 = TraceEvent(
            timestamp=1.0,
            node_name="node_a",
            operation_type="node_end",
            duration_ms=10.0,
            success=True,
            usage={"prompt_tokens": 5, "completion_tokens": 3},
        )
        # Event with input_tokens style
        e2 = TraceEvent(
            timestamp=2.0,
            node_name="node_b",
            operation_type="node_end",
            duration_ms=20.0,
            success=True,
            usage={"input_tokens": 10, "output_tokens": 7},
        )
        # Event with no timestamp (zero)
        e3 = TraceEvent(
            timestamp=0.0,
            node_name="node_c",
            operation_type="reasoning",
            duration_ms=5.0,
            success=True,
        )
        emitter.emit(e1)
        emitter.emit(e2)
        emitter.emit(e3)

        write_execution_summary(tmp_path, "run1")

        summary_path = tmp_path / "orchestration" / "run1" / "execution-trace-summary.json"
        summary = json.loads(summary_path.read_text())
        assert summary["total_prompt_tokens"] == 15
        assert summary["total_completion_tokens"] == 10
        assert summary["wall_clock_ms"] == 2000.0  # (2.0 - 0.0) * 1000

    def test_explicit_zero_usage_fields_do_not_fall_back(self, tmp_path: Path) -> None:
        """Explicit zero token fields should be counted as zero, not fallback aliases."""
        trace_dir = tmp_path / "orchestration" / "run1"
        trace_dir.mkdir(parents=True)
        record = {
            "timestamp": 1.0,
            "node_name": "node_x",
            "operation_type": "node_end",
            "duration_ms": 10.0,
            "success": True,
            "usage": {
                "input_tokens": 0,
                "prompt_tokens": 99,
                "output_tokens": 0,
                "completion_tokens": 42,
            },
        }
        (trace_dir / "execution-trace.jsonl").write_text(json.dumps(record) + "\n")

        write_execution_summary(tmp_path, "run1")

        summary_path = trace_dir / "execution-trace-summary.json"
        summary = json.loads(summary_path.read_text())
        assert summary["total_prompt_tokens"] == 0
        assert summary["total_completion_tokens"] == 0

    def test_non_dict_usage_is_skipped(self, tmp_path: Path) -> None:
        """Non-dict usage field is ignored gracefully."""
        trace_dir = tmp_path / "orchestration" / "run1"
        trace_dir.mkdir(parents=True)
        record = {
            "timestamp": 1.0,
            "node_name": "node_x",
            "operation_type": "node_end",
            "duration_ms": 10.0,
            "success": True,
            "usage": "invalid",
        }
        (trace_dir / "execution-trace.jsonl").write_text(json.dumps(record) + "\n")

        write_execution_summary(tmp_path, "run1")

        summary_path = trace_dir / "execution-trace-summary.json"
        summary = json.loads(summary_path.read_text())
        assert summary["total_prompt_tokens"] == 0

    def test_empty_lines_in_trace_are_skipped(self, tmp_path: Path) -> None:
        """Empty lines in the JSONL file are skipped."""
        trace_dir = tmp_path / "orchestration" / "run1"
        trace_dir.mkdir(parents=True)
        record = json.dumps(
            {
                "timestamp": 1.0,
                "node_name": "a",
                "operation_type": "node_end",
                "success": True,
                "duration_ms": 5.0,
            }
        )
        # Include blank lines between records
        content = f"{record}\n\n   \n{record}\n"
        (trace_dir / "execution-trace.jsonl").write_text(content)

        write_execution_summary(tmp_path, "run1")

        summary_path = trace_dir / "execution-trace-summary.json"
        summary = json.loads(summary_path.read_text())
        assert summary["total_nodes"] == 1  # same node name "a" counted once

    def test_record_with_empty_node_name(self, tmp_path: Path) -> None:
        """Records with empty node_name don't contribute to total_nodes."""
        trace_dir = tmp_path / "orchestration" / "run1"
        trace_dir.mkdir(parents=True)
        records = [
            json.dumps(
                {
                    "timestamp": 1.0,
                    "node_name": "",
                    "operation_type": "reasoning",
                    "duration_ms": 5.0,
                    "success": True,
                }
            ),
            json.dumps(
                {
                    "timestamp": 2.0,
                    "node_name": "real_node",
                    "operation_type": "node_end",
                    "duration_ms": 10.0,
                    "success": True,
                }
            ),
        ]
        (trace_dir / "execution-trace.jsonl").write_text("\n".join(records) + "\n")

        write_execution_summary(tmp_path, "run1")

        summary_path = trace_dir / "execution-trace-summary.json"
        summary = json.loads(summary_path.read_text())
        assert summary["total_nodes"] == 1  # only "real_node" counted

    def test_partial_corrupt_trace_keeps_valid_records(self, tmp_path: Path) -> None:
        """A malformed line is skipped; valid lines before and after are still counted."""
        trace_dir = tmp_path / "orchestration" / "run1"
        trace_dir.mkdir(parents=True)
        good_record = json.dumps(
            {
                "timestamp": 1.0,
                "node_name": "node_a",
                "operation_type": "node_end",
                "duration_ms": 5.0,
                "success": True,
            }
        )
        content = f"{good_record}\nnot valid json\n{good_record}\n"
        (trace_dir / "execution-trace.jsonl").write_text(content)

        write_execution_summary(tmp_path, "run1")

        summary_path = trace_dir / "execution-trace-summary.json"
        summary = json.loads(summary_path.read_text())
        # "node_a" appears in both valid lines — counted once as a unique node
        assert summary["total_nodes"] == 1
        # Both valid node_end records are counted in outcomes
        assert summary["outcomes"].get("success", 0) == 2

    def test_non_numeric_timestamp_and_duration_are_ignored(self, tmp_path: Path) -> None:
        """Non-numeric timestamp/duration values are ignored safely."""
        trace_dir = tmp_path / "orchestration" / "run1"
        trace_dir.mkdir(parents=True)
        record = {
            "timestamp": "not-a-number",
            "node_name": "node_x",
            "operation_type": "node_end",
            "duration_ms": "slow",
            "success": True,
        }
        (trace_dir / "execution-trace.jsonl").write_text(json.dumps(record) + "\n")

        write_execution_summary(tmp_path, "run1")

        summary_path = trace_dir / "execution-trace-summary.json"
        summary = json.loads(summary_path.read_text())
        assert summary["wall_clock_ms"] == 0.0
        assert summary["outcomes"]["success"] == 1

    def test_oserror_on_trace_read_produces_empty_summary(self, tmp_path: Path) -> None:
        """OSError when opening the trace file is handled gracefully (lines 137-138)."""
        trace_dir = tmp_path / "orchestration" / "run1"
        trace_dir.mkdir(parents=True)
        (trace_dir / "execution-trace.jsonl").write_text('{"node_name": "n"}\n')

        with patch(
            "agentic_devtools.orchestration.execution.trace_persistence.locked_file",
            side_effect=OSError("permission denied"),
        ):
            write_execution_summary(tmp_path, "run1")

        summary_path = trace_dir / "execution-trace-summary.json"
        summary = json.loads(summary_path.read_text())
        assert summary["total_nodes"] == 0
        assert summary["outcomes"] == {}
