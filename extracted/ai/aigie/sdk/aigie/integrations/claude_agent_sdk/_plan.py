"""The run summary both Claude Agent SDK roots stamp on their span.

``query()`` and ``ClaudeSDKClient`` finalize different roots in different
modules, but summarise the same run, so the payload is built in one place.
"""

from __future__ import annotations

from typing import Any

from aigie.tracing.execution_state import build_execution_plan


def root_execution_plan(handler: Any, success: bool, turn_count: int) -> dict[str, Any]:
    """Goal Adherence & Drift binds ``{{execution_plan}}`` to this payload.

    ``turn_count`` is passed in rather than read off the handler, so the plan can
    never disagree with the top-level ``turn_count`` on the same span, and so
    each root can correct for what its own path knows. ``agent`` resolves with
    the identical expression both roots use for the span's own ``name``, for the
    same reason.

    That correction matters for a bare ``query()``: turns are advanced by
    ``handle_turn_start``, which only the client-mode patches drive, so the
    query patch counts its own model rounds instead.

    ``turn_count`` is not floored. A query that fails before any model round —
    transport, auth, no CLI — reports 0, which is what happened; the plan's
    ``status`` is what tells the judge the run failed. Flooring it would invent
    a model call to hide a zero, and a fabricated counter misleads the judge
    more than an accurate one that happens to be empty.
    """
    return build_execution_plan(
        agent=getattr(handler, "_root_name", handler.trace_name),
        tool_calls=handler.total_tool_calls,
        turn_count=turn_count,
        status="success" if success else "error",
    )
