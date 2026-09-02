"""WorkflowRun context manager and event recording functions.

Provides the core lifecycle management for observability: run start/end,
atomic event sequence numbering, and convenience functions for recording
node executions, LLM calls, and tool calls.
"""

from __future__ import annotations

import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agentic_devtools.orchestration.observability_errors import ErrorClassifier
from agentic_devtools.orchestration.observability_events import (
    LLMCallEvent,
    NodeExecutionEvent,
    ToolCallEvent,
)
from agentic_devtools.orchestration.observability_pricing import (
    PricingTable,
    build_pricing_table,
    coerce_token_count,
    lookup_call_cost,
)
from agentic_devtools.orchestration.observability_redactor import Redactor
from agentic_devtools.orchestration.observability_truncation import truncate_summary
from agentic_devtools.orchestration.observability_writer import EventWriter

_EVENT_VERSION = 1


def _coerce_strict_bool(value: Any, *, default: bool) -> bool:
    """Return ``value`` only when it is a real bool, else fall back to ``default``."""
    if isinstance(value, bool):
        return value
    return default


def _coerce_duration_ms(value: Any) -> float:
    """Return a numeric duration, treating bools and other unexpected types as zero."""
    # bool is a subclass of int, so this guard must stay first to avoid
    # misclassifying True/False as 1.0/0.0 durations.
    if isinstance(value, bool):
        return 0.0
    if isinstance(value, (int, float)):
        return max(0.0, float(value))
    return 0.0


class WorkflowRun:
    """Context manager for an observability-instrumented workflow run.

    Usage::

        with WorkflowRun(workflow_name="pr-review", state_dir="/path/to/state") as run:
            record_node_execution(run, node_name="fetch", ...)
            record_llm_call(run, node_name="analyze", ...)
            record_tool_call(run, node_name="commit", ...)
        # Summary is printed on exit.
    """

    def __init__(
        self,
        state_dir: str | Path,
        run_id: str | None = None,
        workflow_name: str | None = None,
    ) -> None:
        self._state_dir = Path(state_dir)
        self._run_id = run_id or uuid.uuid4().hex
        self._workflow_name = workflow_name
        self._seq_counter = 0
        self._seq_lock = threading.Lock()
        self._stats_lock = threading.Lock()
        self._record_lock = threading.Lock()
        self._writer: EventWriter | None = None
        self._redactor = Redactor()
        self._classifier = ErrorClassifier()
        self._pricing_table: PricingTable | None = None
        self._start_time: float = 0.0
        self._end_time: float | None = None
        self._closed = False
        self._entered_once = False

        # Summary accumulators
        self.node_success: int = 0
        self.node_failure: int = 0
        self.node_skipped: int = 0
        self.tool_call_count: int = 0
        self.tool_failures: int = 0
        self.total_tool_duration_ms: float = 0.0
        self.llm_call_count: int = 0
        self.llm_calls_without_tokens: int = 0
        self.total_input_tokens: int = 0
        self.total_output_tokens: int = 0
        self.total_estimated_cost: float | None = None
        self.per_model_stats: dict[str, dict[str, Any]] = {}
        self.errors: list[dict[str, Any]] = []

    @property
    def run_id(self) -> str:
        """Return the run identifier."""
        return self._run_id

    @property
    def workflow_name(self) -> str | None:
        """Return the workflow name, if provided at construction."""
        return self._workflow_name

    @property
    def total_duration_ms(self) -> int:
        """Return total elapsed time since run start in milliseconds.

        Once the context manager has exited, returns the frozen elapsed time
        captured in ``__exit__`` so the value stays stable after the run ends.
        """
        if self._start_time == 0.0:
            return 0
        end = self._end_time if self._end_time is not None else time.monotonic()
        return int((end - self._start_time) * 1000)

    @property
    def log_path(self) -> Path | None:
        """Return the log file path if writer is active."""
        if self._writer and not self._writer.degraded:
            return self._writer.log_path
        return None

    def _next_seq(self) -> int:
        """Atomically increment and return the next event sequence number."""
        with self._seq_lock:
            self._seq_counter += 1
            return self._seq_counter

    def _now_iso(self) -> str:
        """Return current UTC time as ISO-8601 string."""
        return datetime.now(timezone.utc).isoformat()

    def _write_event(self, event: NodeExecutionEvent | LLMCallEvent | ToolCallEvent) -> None:
        """Write an event to the log file."""
        if self._writer:
            self._writer.write(event.to_dict())

    def _start_recording(self) -> bool:
        """Reserve the run for recording unless the context has already exited."""
        self._record_lock.acquire()
        if self._closed:
            self._record_lock.release()
            return False
        return True

    def _finish_recording(self) -> None:
        """Release the recording reservation acquired by ``_start_recording``."""
        self._record_lock.release()

    def __enter__(self) -> WorkflowRun:
        if self._entered_once:
            raise RuntimeError("WorkflowRun instances cannot be re-entered")
        self._entered_once = True
        self._start_time = time.monotonic()
        self._closed = False
        self._writer = EventWriter(self._run_id, self._state_dir)
        self._pricing_table = build_pricing_table(self._state_dir)
        if self._writer.log_path and not self._writer.degraded:
            workflow_tag = f" workflow={self._workflow_name}" if self._workflow_name else ""
            print(f"[observability]{workflow_tag} Log: {self._writer.log_path}", file=sys.stdout)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # Freeze and close under the record lock so no late recorder can update
        # in-memory stats after the final summary has been emitted.
        with self._record_lock:
            self._end_time = time.monotonic()
            self._closed = True
            if self._writer:
                self._writer.close()
        # Import here to avoid circular imports
        from agentic_devtools.orchestration.observability_summary import (
            print_run_summary,
        )

        try:
            print_run_summary(self)
        except Exception:  # noqa: BLE001
            # Best-effort: never let summary printing mask the original exception
            # or crash the workflow (e.g. BrokenPipeError, closed stdout).
            pass


def record_node_execution(
    run: WorkflowRun,
    *,
    node_name: str,
    start_time: str | None = None,
    end_time: str | None = None,
    status: str,
    input_data: Any = None,
    output_data: Any = None,
    duration_ms: int | float | None = None,
    inputs_summary: Any = None,
    outputs_summary: Any = None,
    error: BaseException | None = None,
    error_source: str | None = None,
) -> None:
    """Record a node execution event.

    Applies redaction → truncation → event construction → write.

    Args:
        run: The active WorkflowRun.
        node_name: LangGraph node identifier.
        start_time: ISO-8601 UTC start timestamp.
        end_time: ISO-8601 UTC end timestamp.
        status: ``"success"``, ``"failure"``, or ``"skipped"``.
        input_data: Raw input data (will be redacted and truncated).
        output_data: Raw output data (will be redacted and truncated).
        duration_ms: Optional explicit duration override for compatibility.
            Negative and invalid values are coerced to ``0``.
        inputs_summary: Alias for ``input_data`` (compatibility).
        outputs_summary: Alias for ``output_data`` (compatibility).
        error: Exception instance if status is "failure".
        error_source: Optional source context for error classification.
            Use ``"llm"`` when the failure originated from an LLM call,
            ``"tool"`` for tool-call failures. Influences whether the
            classifier routes to the ``llm`` or ``tool`` category.

    Example::

        from datetime import datetime, timezone

        now = datetime.now(timezone.utc).isoformat()
        record_node_execution(
            run,
            node_name="fetch_diff",
            start_time=now,
            end_time=now,
            status="success",
            input_data={"pr_id": 123},
            output_data={"files": 7},
        )
    """
    if not run._start_recording():
        return
    try:
        # Redact then truncate
        raw_input = input_data if input_data is not None else inputs_summary
        raw_output = output_data if output_data is not None else outputs_summary
        redacted_input = run._redactor.redact(raw_input)
        redacted_output = run._redactor.redact(raw_output)
        input_summary = truncate_summary(redacted_input)
        output_summary = truncate_summary(redacted_output)

        # Resolve timestamps and duration.
        resolved_end_time = end_time or run._now_iso()
        resolved_start_time = start_time or resolved_end_time
        resolved_duration_ms = (
            # NodeExecutionEvent.duration_ms is defined as int milliseconds.
            int(_coerce_duration_ms(duration_ms))
            if duration_ms is not None
            else _compute_duration_ms(resolved_start_time, resolved_end_time)
        )

        # Classify error if failure
        error_class: str | None = None
        retryable: bool | None = None
        error_message: str | None = None
        if status == "failure" and error is not None:
            context: dict[str, Any] | None = {"source": error_source} if error_source else None
            classification = run._classifier.classify(error, context)
            error_class = classification.error_class
            retryable = classification.retryable
            sanitized_class_msg = _sanitize_error_message(run, classification.message)
            error_message = sanitized_class_msg or _sanitize_error_message(run, str(error))

        event = NodeExecutionEvent(
            version=_EVENT_VERSION,
            event_seq=run._next_seq(),
            type="node",
            run_id=run.run_id,
            timestamp=resolved_end_time,
            node_name=node_name,
            status=status,
            start_time=resolved_start_time,
            end_time=resolved_end_time,
            duration_ms=resolved_duration_ms,
            input_summary=input_summary,
            output_summary=output_summary,
            error_class=error_class,
            retryable=retryable,
            error_message=error_message,
        )

        run._write_event(event)

        # Update summary stats — guarded so concurrent node executions don't race.
        with run._stats_lock:
            if status == "success":
                run.node_success += 1
            elif status == "failure":
                run.node_failure += 1
                run.errors.append(
                    {
                        "node_name": node_name,
                        "error_class": error_class or "unknown",
                        "message": (
                            error_message or (_sanitize_error_message(run, str(error)) if error else "Unknown error")
                        ),
                    }
                )
            elif status == "skipped":
                run.node_skipped += 1
    finally:
        run._finish_recording()


def record_llm_call(
    run: WorkflowRun,
    *,
    node_name: str,
    node_type: str,
    model: str,
    input_tokens: int | float | str | None,
    output_tokens: int | float | str | None,
    latency_ms: int,
    validation_result: str,
) -> None:
    """Record an LLM call event.

    Computes estimated cost via the pricing layer and writes the event.

    Non-int token values (strings, floats) are coerced to int so that
    callers using parsed JSON or provider libraries that return floats
    never crash the observability pipeline or silently corrupt totals.
    Bools and unconvertible values are treated as ``None`` (unavailable).

    Args:
        run: The active WorkflowRun.
        node_name: Owning node identifier.
        node_type: Provider/config context.
        model: Provider model identifier.
        input_tokens: Input token count (None if unavailable).
        output_tokens: Output token count (None if unavailable).
        latency_ms: End-to-end call latency in milliseconds.
        validation_result: Structured output validation outcome.
    """
    if not run._start_recording():
        return
    try:
        # Coerce tokens to int — bools, strings, floats, and unconvertible values
        # are all normalised to None so they cannot silently corrupt totals or
        # trigger a TypeError deep inside TokenUsage arithmetic.
        safe_input = coerce_token_count(input_tokens)
        safe_output = coerce_token_count(output_tokens)

        estimated_cost = lookup_call_cost(model, safe_input, safe_output, pricing_table=run._pricing_table)

        event = LLMCallEvent(
            version=_EVENT_VERSION,
            event_seq=run._next_seq(),
            type="llm_call",
            run_id=run.run_id,
            timestamp=run._now_iso(),
            node_name=node_name,
            node_type=node_type,
            model=model,
            input_tokens=safe_input,
            output_tokens=safe_output,
            latency_ms=latency_ms,
            validation_result=validation_result,
            estimated_cost_usd=estimated_cost,
        )

        run._write_event(event)

        # Update summary stats — guarded so concurrent LLM calls don't race on
        # shared counters or the check-then-insert per_model_stats pattern.
        with run._stats_lock:
            run.llm_call_count += 1
            if safe_input is None or safe_output is None:
                run.llm_calls_without_tokens += 1
            else:
                run.total_input_tokens += safe_input
                run.total_output_tokens += safe_output

            if estimated_cost is not None:
                if run.total_estimated_cost is None:
                    run.total_estimated_cost = 0.0
                run.total_estimated_cost += estimated_cost

            # Per-model stats
            if model not in run.per_model_stats:
                run.per_model_stats[model] = {
                    "calls": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost": None,
                }
            stats = run.per_model_stats[model]
            stats["calls"] += 1
            if safe_input is not None and safe_output is not None:
                stats["input_tokens"] += safe_input
                stats["output_tokens"] += safe_output
            if estimated_cost is not None:
                if stats["cost"] is None:
                    stats["cost"] = 0.0
                stats["cost"] += estimated_cost
    finally:
        run._finish_recording()


def record_tool_call(
    run: WorkflowRun,
    *,
    node_name: str,
    tool_name: str,
    input_params: Any,
    tool_result: Any,
    tool_def: Any,
) -> None:
    """Record a tool call event.

    Sources ``success``, ``dry_run``, and ``duration_ms`` from the
    ``ToolResult`` and ``mutating`` from the ``ToolDefinition``.

    Args:
        run: The active WorkflowRun.
        node_name: Owning node identifier.
        tool_name: Tool registry name.
        input_params: Raw input parameters (will be redacted/truncated).
        tool_result: A ToolResult instance (or duck-typed object with
            ``success``, ``dry_run``, ``duration_ms`` attributes).
        tool_def: A ToolDefinition instance (or duck-typed object with
            ``mutating`` attribute).
    """
    if not run._start_recording():
        return
    try:
        # Redact and truncate input
        redacted_input = run._redactor.redact(input_params)
        truncated_input = truncate_summary(redacted_input)

        # Source fields from tool_result and tool_def.
        # Coerce to safe types so that duck-typed objects with unexpected attribute
        # values (e.g. None, strings, bool-as-number) never crash the workflow or
        # silently misclassify the event.
        success = _coerce_strict_bool(getattr(tool_result, "success", True), default=True)
        dry_run = _coerce_strict_bool(getattr(tool_result, "dry_run", False), default=False)
        duration_ms = _coerce_duration_ms(getattr(tool_result, "duration_ms", 0.0))
        mutating = _coerce_strict_bool(getattr(tool_def, "mutating", False), default=False)

        # Redact and truncate result summary
        result_output = getattr(tool_result, "output", None)
        redacted_output = run._redactor.redact(result_output)
        tool_result_summary = truncate_summary(redacted_output)

        # Error classification for failed tools
        error_class: str | None = None
        if not success:
            error_class = "tool"

        event = ToolCallEvent(
            version=_EVENT_VERSION,
            event_seq=run._next_seq(),
            type="tool_call",
            run_id=run.run_id,
            timestamp=run._now_iso(),
            node_name=node_name,
            tool_name=tool_name,
            input_params=truncated_input,
            duration_ms=duration_ms,
            success=success,
            dry_run=dry_run,
            mutating=mutating,
            tool_result_summary=tool_result_summary,
            error_class=error_class,
        )

        run._write_event(event)

        # Update summary stats — guarded so concurrent tool calls don't race.
        with run._stats_lock:
            run.tool_call_count += 1
            if not success:
                run.tool_failures += 1
            run.total_tool_duration_ms += duration_ms
    finally:
        run._finish_recording()


def _compute_duration_ms(start_time: str, end_time: str) -> int:
    """Compute duration in milliseconds between two ISO-8601 timestamps."""
    try:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        delta = (end - start).total_seconds() * 1000
        return max(0, int(delta))
    except (ValueError, TypeError):
        return 0


def _sanitize_error_message(run: WorkflowRun, message: str) -> str:
    """Redact and truncate an error message for safe logging.

    Args:
        run: Active workflow run containing the redactor instance.
        message: Raw error message text.

    Returns:
        A sanitized string safe for event and summary output.
    """
    redacted = run._redactor.redact(message)
    sanitized = truncate_summary(redacted)
    return str(sanitized)
