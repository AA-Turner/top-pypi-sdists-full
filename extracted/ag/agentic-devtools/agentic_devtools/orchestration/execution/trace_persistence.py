"""Trace persistence — JSONL writer and execution summary.

Provides ``TraceRecord``, ``PersistentTraceEmitter``, and
``write_execution_summary()`` for recording node execution traces
to persistent storage.
"""

from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

from agentic_devtools.file_locking import locked_file

from .run_id import validate_run_id
from .tracing import TraceEvent
from .types import JSONValue

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TraceRecord:
    """A single trace record persisted to JSONL.

    Attributes:
        node_name: Name of the node that produced this record.
        start_time: Unix epoch start timestamp.
        end_time: Unix epoch end timestamp.
        duration_ms: Wall-clock duration in milliseconds.
        model_id: LLM model identifier (empty for tool events).
        prompt_tokens: Number of prompt/input tokens used.
        completion_tokens: Number of completion/output tokens used.
        tool_id: Tool identifier (empty for reasoning events).
        tool_arguments: Summary of tool arguments.
        tool_result_summary: Truncated tool result.
        outcome: Outcome of the operation (success, error, timeout, etc.).
    """

    node_name: str
    start_time: float
    end_time: float
    duration_ms: float
    model_id: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    tool_id: str = ""
    tool_arguments: str = ""
    tool_result_summary: str = ""
    outcome: str = "success"


class PersistentTraceEmitter:
    """Appends trace events as JSONL to an execution trace file.

    Implements the ``TraceEmitter`` protocol. Failures are swallowed
    with a stderr warning — they never propagate into node execution.

    File: ``<state_dir>/orchestration/<run_id>/execution-trace.jsonl``
    """

    def __init__(self, state_dir: Path, run_id: str) -> None:
        safe_run_id = validate_run_id(run_id)
        self._trace_dir = state_dir / "orchestration" / safe_run_id
        self._trace_dir.mkdir(parents=True, exist_ok=True)
        self._trace_path = self._trace_dir / "execution-trace.jsonl"

    @property
    def trace_path(self) -> Path:
        """Path to the JSONL trace file."""
        return self._trace_path

    def emit(self, event: TraceEvent) -> None:
        """Append a trace event as a JSON line.

        Uses an exclusive file lock so that concurrent node executions cannot
        interleave partial writes and corrupt the JSONL file.
        Failures are caught and reported to stderr (never raised).
        """
        try:
            payload: dict[str, JSONValue] = {
                "timestamp": event.timestamp,
                "node_name": event.node_name,
                "operation_type": event.operation_type,
                "model_id": event.model_id,
                "tool_name": event.tool_name,
                "input_summary": event.input_summary,
                "output_summary": event.output_summary,
                "duration_ms": event.duration_ms,
                "success": event.success,
                "usage": event.usage,
            }
            line = json.dumps(payload, default=str) + "\n"
            with locked_file(self._trace_path, mode="a") as f:
                f.write(line)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[PersistentTraceEmitter] emit failed for node={event.node_name}: {type(exc).__name__}",
                file=sys.stderr,
            )


def write_execution_summary(state_dir: Path, run_id: str) -> None:
    """Read the JSONL trace and write an aggregated summary.

    Creates ``<state_dir>/orchestration/<run_id>/execution-trace-summary.json``
    with total nodes, total tokens, wall-clock time, and outcome breakdown.
    """
    safe_run_id = validate_run_id(run_id)
    trace_dir = state_dir / "orchestration" / safe_run_id
    trace_path = trace_dir / "execution-trace.jsonl"
    summary_path = trace_dir / "execution-trace-summary.json"
    trace_dir.mkdir(parents=True, exist_ok=True)

    if not trace_path.exists():
        summary = {
            "total_nodes": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_tokens": 0,
            "wall_clock_ms": 0.0,
            "outcomes": {},
        }
        summary_path.write_text(json.dumps(summary, indent=2))
        return

    records: list[dict] = []
    try:
        with locked_file(trace_path, mode="r", exclusive=False, encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    try:
                        records.append(json.loads(stripped))
                    except json.JSONDecodeError as exc:
                        logger.warning("Skipping malformed trace line: %s", exc)
    except OSError as exc:
        logger.warning("Failed to read trace file: %s", exc)

    # Aggregate metrics
    node_names: set[str] = set()
    total_prompt_tokens = 0.0
    total_completion_tokens = 0.0
    outcomes: dict[str, int] = {}
    min_time = float("inf")
    max_time = 0.0
    total_duration_ms = 0.0

    for record in records:
        node_name = record.get("node_name", "")
        if node_name:
            node_names.add(node_name)

        # Token usage from usage dict
        usage = record.get("usage", {})
        if isinstance(usage, dict):
            # Prefer canonical orchestration keys; only use aliases when the
            # canonical key is absent (not merely falsy).
            prompt_tokens = usage["input_tokens"] if "input_tokens" in usage else usage.get("prompt_tokens")
            completion_tokens = usage["output_tokens"] if "output_tokens" in usage else usage.get("completion_tokens")
            if isinstance(prompt_tokens, int | float):
                total_prompt_tokens += prompt_tokens
            if isinstance(completion_tokens, int | float):
                total_completion_tokens += completion_tokens

        # Track timing
        ts = record.get("timestamp")
        if isinstance(ts, int | float):
            ts_f = float(ts)
            min_time = min(min_time, ts_f)
            max_time = max(max_time, ts_f)

        duration = record.get("duration_ms")
        if isinstance(duration, int | float):
            total_duration_ms += float(duration)

        # Count outcomes (only for node_end events)
        op_type = record.get("operation_type", "")
        if op_type == "node_end":
            success = record.get("success", True)
            outcome = "success" if success else "failed"
            outcomes[outcome] = outcomes.get(outcome, 0) + 1

    wall_clock_ms = (max_time - min_time) * 1000 if max_time > min_time else total_duration_ms

    summary = {
        "total_nodes": len(node_names),
        "total_prompt_tokens": total_prompt_tokens,
        "total_completion_tokens": total_completion_tokens,
        "total_tokens": total_prompt_tokens + total_completion_tokens,
        "wall_clock_ms": round(wall_clock_ms, 2),
        "outcomes": outcomes,
    }

    summary_path.write_text(json.dumps(summary, indent=2))
