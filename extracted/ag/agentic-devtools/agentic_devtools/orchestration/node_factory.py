"""Node factory — wraps node functions with cross-cutting concerns.

Provides ``make_node()`` which injects ``ExecutionContext`` and handles
trace emission, exception handling, and outcome recording.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from agentic_devtools.orchestration.execution.context import ExecutionContext
from agentic_devtools.orchestration.execution.exceptions import RetryExhaustedError
from agentic_devtools.orchestration.execution.tracing import make_trace_event


def make_node(
    fn: Callable[..., dict[str, Any]],
    context: ExecutionContext,
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """Wrap a node function with context injection and cross-cutting concerns.

    The wrapped function:
    1. Emits a trace event at start
    2. Calls ``fn(state, context=context)``
    3. Emits a trace event at end with duration and outcome
    4. On ``RetryExhaustedError``: returns ``{"status": "failed", "error": ...}``
    5. On unexpected exceptions: returns ``{"status": "failed", "error": ...}``

    Args:
        fn: Node implementation with signature ``fn(state, *, context) -> dict``.
        context: The ``ExecutionContext`` to inject.

    Returns:
        A LangGraph-compatible node function ``(state: dict) -> dict``.
    """
    node_name = getattr(fn, "__name__", "unknown_node")

    def wrapped(state: dict[str, Any]) -> dict[str, Any]:
        start_time = time.monotonic()

        # Emit start trace
        start_event = make_trace_event(
            node_name=node_name,
            operation_type="node_start",
            input_summary=f"state_keys={list(state.keys())[:10]}",
        )
        context.tracer.emit(start_event)

        try:
            result = fn(state, context=context)

            # Reflect actual outcome — treat status="failed" as a failure trace
            result_success = result.get("status") != "failed"

            # Emit end trace
            duration_ms = (time.monotonic() - start_time) * 1000
            end_event = make_trace_event(
                node_name=node_name,
                operation_type="node_end",
                duration_ms=duration_ms,
                success=result_success,
                output_summary=f"status={result.get('status', 'ok')}",
            )
            context.tracer.emit(end_event)

            return result

        except RetryExhaustedError as exc:
            duration_ms = (time.monotonic() - start_time) * 1000
            error_info = {
                "type": "retry_exhausted",
                "message": str(exc),
                "attempts": exc.attempts,
                "last_error": exc.last_error,
            }

            # Emit failure trace
            end_event = make_trace_event(
                node_name=node_name,
                operation_type="node_end",
                duration_ms=duration_ms,
                success=False,
                output_summary=f"retry_exhausted: {str(exc.last_error or '')[:100]}",
            )
            context.tracer.emit(end_event)

            return {"status": "failed", "error": error_info}

        except Exception as exc:  # noqa: BLE001
            duration_ms = (time.monotonic() - start_time) * 1000
            error_info = {
                "type": type(exc).__name__,
                "message": str(exc),
            }

            # Emit failure trace
            end_event = make_trace_event(
                node_name=node_name,
                operation_type="node_end",
                duration_ms=duration_ms,
                success=False,
                output_summary=f"{type(exc).__name__}: {str(exc)[:100]}",
            )
            context.tracer.emit(end_event)

            return {"status": "failed", "error": error_info}

    wrapped.__name__ = node_name
    wrapped.__qualname__ = f"make_node.<wrapped>.{node_name}"
    return wrapped
