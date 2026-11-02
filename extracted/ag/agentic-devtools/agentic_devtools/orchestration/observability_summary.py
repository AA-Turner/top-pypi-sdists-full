"""Human-readable console summary for observability runs.

Formats a concise multi-line summary of a workflow run including
duration, node counts, LLM token usage, cost estimates, and errors.
Output fits within an 80-column terminal width.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from agentic_devtools.orchestration.observability_run import WorkflowRun

# Keep summary lines within an 80-column terminal by reserving three characters
# for the "..." suffix whenever a rendered line must be clamped.
_MAX_LINE_LENGTH = 80
_ELLIPSIS_CUTOFF = _MAX_LINE_LENGTH - 3


@dataclass(slots=True)
class SummaryStats:
    """Aggregated summary data shared by runtime and log-file formatters."""

    title: str = "Workflow Run Summary"
    total_duration_ms: int | float | None = None
    node_success: int = 0
    node_failure: int = 0
    node_skipped: int = 0
    tool_call_count: int = 0
    tool_failures: int = 0
    total_tool_duration_ms: float = 0.0
    llm_call_count: int = 0
    llm_calls_without_tokens: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_estimated_cost: float | None = None
    per_model_stats: dict[str, dict[str, Any]] = field(default_factory=dict)
    errors: list[dict[str, Any]] = field(default_factory=list)


def format_summary_stats(stats: SummaryStats) -> str:
    """Format aggregated summary statistics into a console-friendly report."""
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append(stats.title)
    lines.append("=" * 60)

    # Duration
    duration = stats.total_duration_ms
    if duration is not None:
        if duration >= 60_000:
            minutes = int(duration) // 60_000
            remaining_seconds = (int(duration) % 60_000) // 1000
            lines.append(f"Duration: {minutes}m {remaining_seconds}s")
        else:
            seconds = duration / 1000
            lines.append(f"Duration: {seconds:.1f}s")

    # Node counts
    total_nodes = stats.node_success + stats.node_failure + stats.node_skipped
    parts = []
    if stats.node_success:
        parts.append(f"{stats.node_success} success")
    if stats.node_failure:
        parts.append(f"{stats.node_failure} failed")
    if stats.node_skipped:
        parts.append(f"{stats.node_skipped} skipped")
    node_detail = ", ".join(parts) if parts else "none"
    node_line = f"Nodes: {total_nodes} executed ({node_detail})"
    if len(node_line) > _MAX_LINE_LENGTH:
        node_line = node_line[:_ELLIPSIS_CUTOFF] + "..."
    lines.append(node_line)

    # Tool calls
    if stats.tool_call_count > 0:
        tool_parts = [f"{stats.tool_call_count} calls"]
        if stats.tool_failures:
            tool_parts.append(f"{stats.tool_failures} failed")
        total_tool_s = stats.total_tool_duration_ms / 1000
        tool_parts.append(f"{total_tool_s:.1f}s total")
        tool_line = f"Tools: {', '.join(tool_parts)}"
        if len(tool_line) > _MAX_LINE_LENGTH:
            tool_line = tool_line[:_ELLIPSIS_CUTOFF] + "..."
        lines.append(tool_line)

    # LLM calls
    llm_count = stats.llm_call_count
    excluded = stats.llm_calls_without_tokens
    if llm_count > 0:
        note = ""
        if excluded > 0:
            note = f" ({excluded} without token data)"
        llm_line = f"LLM calls: {llm_count}{note}"
        if len(llm_line) > _MAX_LINE_LENGTH:
            llm_line = llm_line[:_ELLIPSIS_CUTOFF] + "..."
        lines.append(llm_line)

        # Token totals
        token_line = f"Tokens: {stats.total_input_tokens:,} input | {stats.total_output_tokens:,} output"
        if len(token_line) > _MAX_LINE_LENGTH:
            token_line = token_line[:_ELLIPSIS_CUTOFF] + "..."
        lines.append(token_line)

        # Cost estimate
        cost = stats.total_estimated_cost
        if cost is not None and cost > 0:
            cost_note = ""
            if excluded > 0:
                cost_note = (
                    f" (lower bound — {excluded} call{'s' if excluded > 1 else ''} excluded: missing token data)"
                )
            cost_line = f"Estimated cost: ${cost:.4f}{cost_note}"
            if len(cost_line) > _MAX_LINE_LENGTH:
                cost_line = cost_line[:_ELLIPSIS_CUTOFF] + "..."
            lines.append(cost_line)

        # Per-model breakdown (if multiple models)
        if len(stats.per_model_stats) > 1:
            lines.append("Per-model breakdown:")
            for model, model_metrics in sorted(
                stats.per_model_stats.items(),
                key=lambda item: str(item[0]),
            ):
                model_cost = model_metrics.get("cost")
                cost_str = f"${model_cost:.4f}" if model_cost is not None else "n/a"
                line = (
                    f"  {model}: {model_metrics.get('calls', 0)} calls,"
                    f" {model_metrics.get('input_tokens', 0):,} in /"
                    f" {model_metrics.get('output_tokens', 0):,} out,"
                    f" cost={cost_str}"
                )
                if len(line) > _MAX_LINE_LENGTH:
                    line = line[:_ELLIPSIS_CUTOFF] + "..."
                lines.append(line)

    # Errors
    if stats.errors:
        lines.append("")
        lines.append(f"Errors ({len(stats.errors)}):")
        for err in stats.errors:
            node = str(err.get("node_name") or "unknown")
            cls = str(err.get("error_class") or "unknown")
            msg = " ".join(str(err.get("message") or "").splitlines())
            # Truncate message to fit 80 cols; guard against long prefix
            prefix = f"  [{cls}] {node}: "
            available = 78 - len(prefix)
            if available <= 0:
                lines.append(prefix[:78])
            else:
                if len(msg) > available:
                    if available > 3:
                        msg = msg[: available - 3] + "..."
                    else:
                        msg = msg[:available]
                lines.append(f"{prefix}{msg}")

    lines.append("=" * 60)
    return "\n".join(lines)


def format_run_summary(run: WorkflowRun) -> str:
    """Format a human-readable summary of a completed workflow run.

    Args:
        run: The completed WorkflowRun instance with accumulated stats.

    Returns:
        A multi-line string suitable for console output (≤80 columns).
    """
    return format_summary_stats(
        SummaryStats(
            total_duration_ms=run.total_duration_ms,
            node_success=run.node_success,
            node_failure=run.node_failure,
            node_skipped=run.node_skipped,
            tool_call_count=run.tool_call_count,
            tool_failures=run.tool_failures,
            total_tool_duration_ms=run.total_tool_duration_ms,
            llm_call_count=run.llm_call_count,
            llm_calls_without_tokens=run.llm_calls_without_tokens,
            total_input_tokens=run.total_input_tokens,
            total_output_tokens=run.total_output_tokens,
            total_estimated_cost=run.total_estimated_cost,
            per_model_stats=run.per_model_stats,
            errors=run.errors,
        )
    )


def print_run_summary(run: WorkflowRun) -> None:
    """Print the formatted run summary to stdout.

    Args:
        run: The completed WorkflowRun instance.
    """
    summary = format_run_summary(run)
    print(summary, file=sys.stdout)
