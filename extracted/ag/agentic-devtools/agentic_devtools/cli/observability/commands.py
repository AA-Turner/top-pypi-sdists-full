"""CLI command for reading and summarizing observability log files.

Provides ``agdt-observability-summary`` which reads a ``.jsonl`` log
file and prints a human-readable summary to the console.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

from agentic_devtools.orchestration.observability_redactor import Redactor
from agentic_devtools.orchestration.observability_summary import (
    SummaryStats,
    format_summary_stats,
)

_DEFAULT_REDACTOR = Redactor()


def _as_int(value: Any) -> int | None:
    """Return int for numeric types only (bool/strings rejected), else None."""
    # bool is a subclass of int; reject it explicitly.
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _as_float(value: Any) -> float | None:
    """Return float for numeric types only (bool/strings rejected), else None."""
    # bool is a subclass of int; reject it explicitly.
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _as_bool(value: Any) -> bool | None:
    """Return bool only for actual bool values (int/string values rejected), else None."""
    if isinstance(value, bool):
        return value
    return None


def _as_model_label(value: Any) -> str:
    """Return a safe model label string from JSON-like values."""
    if value is None:
        return "unknown"
    if isinstance(value, str):
        normalized = value.strip()
        return normalized if normalized else "unknown"
    try:
        normalized = str(value).strip()
    except Exception:  # pragma: no cover
        return "unknown"
    return normalized if normalized else "unknown"


def _parse_events(log_path: Path) -> Iterator[dict[str, Any]]:
    """Stream events from a JSONL log file, applying redaction to each event."""
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    parsed = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(parsed, dict):
                    redacted = _DEFAULT_REDACTOR.redact(parsed)
                    # redact() returns None only if deep-copy fails; skip those entries.
                    if isinstance(redacted, dict):
                        yield redacted


def _format_summary_from_events(events: Iterable[dict[str, Any]]) -> str:
    """Format a summary from parsed events."""
    # Aggregate stats
    node_success = 0
    node_failure = 0
    node_skipped = 0
    llm_calls = 0
    llm_without_tokens = 0
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost: float | None = None
    per_model: dict[str, dict[str, Any]] = {}
    tool_calls = 0
    tool_failures = 0
    total_tool_duration_ms: float = 0.0
    errors: list[dict[str, Any]] = []

    for event in events:
        event_type = event.get("type")

        if event_type == "node":
            status = event.get("status")
            if status == "success":
                node_success += 1
            elif status == "failure":
                node_failure += 1
                errors.append(
                    {
                        "node_name": event.get("node_name", "unknown"),
                        "error_class": event.get("error_class", "unknown"),
                        "message": event.get("error_message", ""),
                    }
                )
            elif status == "skipped":
                node_skipped += 1

        elif event_type == "llm_call":
            llm_calls += 1
            input_t = _as_int(event.get("input_tokens"))
            output_t = _as_int(event.get("output_tokens"))
            if input_t is None or output_t is None:
                llm_without_tokens += 1
            else:
                total_input_tokens += input_t
                total_output_tokens += output_t

            cost = _as_float(event.get("estimated_cost_usd"))
            if cost is not None:
                if total_cost is None:
                    total_cost = 0.0
                total_cost += cost

            model = _as_model_label(event.get("model"))
            if model not in per_model:
                per_model[model] = {
                    "calls": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost": None,
                }
            per_model[model]["calls"] += 1
            if input_t is not None and output_t is not None:
                per_model[model]["input_tokens"] += input_t
                per_model[model]["output_tokens"] += output_t
            if cost is not None:
                if per_model[model]["cost"] is None:
                    per_model[model]["cost"] = 0.0
                per_model[model]["cost"] += cost

        elif event_type == "tool_call":
            tool_calls += 1
            if _as_bool(event.get("success")) is False:
                tool_failures += 1
            duration_ms = _as_float(event.get("duration_ms"))
            if duration_ms is not None:
                total_tool_duration_ms += duration_ms

    return format_summary_stats(
        SummaryStats(
            title="Workflow Run Summary (from log file)",
            node_success=node_success,
            node_failure=node_failure,
            node_skipped=node_skipped,
            tool_call_count=tool_calls,
            tool_failures=tool_failures,
            total_tool_duration_ms=total_tool_duration_ms,
            llm_call_count=llm_calls,
            llm_calls_without_tokens=llm_without_tokens,
            total_input_tokens=total_input_tokens,
            total_output_tokens=total_output_tokens,
            total_estimated_cost=total_cost,
            per_model_stats=per_model,
            errors=errors,
        )
    )


def observability_summary_command() -> None:
    """CLI entry point for ``agdt-observability-summary``.

    Reads a ``.jsonl`` observability log file and prints a summary.
    """
    parser = argparse.ArgumentParser(
        prog="agdt-observability-summary",
        description="Print a human-readable summary of an observability log file.",
    )
    parser.add_argument(
        "log_file",
        type=str,
        help="Path to the .jsonl observability log file.",
    )
    args = parser.parse_args()

    log_path = Path(args.log_file)
    if not log_path.is_file():
        print(f"Error: File not found: {log_path}", file=sys.stderr)
        sys.exit(1)

    try:
        event_gen = _parse_events(log_path)
        # Peek at the first event to detect an empty (or all-invalid) file before
        # consuming the generator in full.  The peeked event is chained back so
        # _format_summary_from_events receives the complete stream.
        first = next(event_gen, None)
        if first is None:
            print("No events found in log file.", file=sys.stderr)
            sys.exit(1)
        summary = _format_summary_from_events(itertools.chain([first], event_gen))
    except (OSError, UnicodeDecodeError) as exc:
        print(f"Error: Failed to read log file {log_path}: {exc}", file=sys.stderr)
        sys.exit(1)
    print(summary)
