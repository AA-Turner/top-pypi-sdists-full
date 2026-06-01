"""Trace-update finalization. Single function builds and emits the
trace_update payload at run completion.

The atexit-safe synchronous fallback for terminal updates (when the
buffer's bg_loop is unusable) is owned by the Buffer/Emitter layer, NOT
here — callbacks just emit normally and the Buffer transparently falls
back when needed.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from aigie.buffer import EventType
from aigie.tracing.retention import is_retention_suppressed

if TYPE_CHECKING:
    from aigie.tracing.execution_state import ExecutionState


def finalize_trace(
    *,
    emitter: Any,
    trace_id: str,
    agent_name: str,
    execution_state: ExecutionState,
    trace_metadata: dict[str, Any] | None,
    error: BaseException | None,
) -> None:
    """Emit a single trace_update event marking the trace complete."""
    if is_retention_suppressed():
        return
    status = "error" if error else "success"
    payload: dict[str, Any] = {
        "id": trace_id,
        "status": status,
        "end_time": datetime.now(timezone.utc).isoformat(),
    }
    if error is not None:
        err_str = str(error)
        payload["error"] = err_str
        payload["error_message"] = err_str
        payload["error_type"] = type(error).__name__

    execution_data = execution_state.to_execution_data()
    if execution_data["execution_path"]:
        payload["execution_data"] = execution_data

    metadata = dict(trace_metadata or {})
    metadata["execution_plan"] = execution_state.to_execution_plan(
        agent_name=agent_name, status=status
    )
    metadata["turn_count"] = execution_state.turn_count
    payload["metadata"] = metadata

    emitter.emit_raw_sync(EventType.TRACE_UPDATE, payload)
