"""A RUN-END NOTICE BELONGS TO THE RUN THAT WROTE IT (P8-RUNS 2026-11-15).

The budget wrap-up, the iteration ceiling and the loop guard each end a run with a host-written
notice — "ALL TOOLS ARE NOW DISABLED", "only this one reply fits". The tools come back on the next
turn (``tools_off_this_turn_only``), but the NOTICE is a stored user-role row, so the next run's
history still carries it. Live: a Company Setup stranger typed "continue" after the budget stop and
the model read the stale notice as current ("Tools are off, and the latest message says only a final
status reply fits") — the person got a status line, never a resumed build.

Once the person has spoken after such a notice, it is spent: on the WIRE copy only it is replaced by
one line saying that run is over and this one has its tools and a fresh budget. The saved row never
changes; the same words go out on every send, so the cached prefix holds.
Guard: ``packages/matrx-ai/tests/test_a_spent_run_end_notice_never_reaches_the_next_run.py``.
"""

from __future__ import annotations

from copy import copy
from typing import Any

#: ``authored_reason`` of every host notice that speaks for the END of the run it was written in.
RUN_END_NOTICE_REASONS = frozenset(
    {
        "budget_wrap_up",
        "budget_finish_unit",
        "iteration_ceiling_wrap_up",
        "iteration_ceiling_approaching",
        "loop_guard_tools_disabled",
        "loop_guard_approaching",
    }
)

SPENT_RUN_NOTICE = (
    "SYSTEM NOTICE (not from the user): an earlier run stopped here at one of its limits. That run is "
    "over. The person has spoken since, and this is a NEW run: your tools are available again and its "
    "budget is fresh. Carry on from what was left to do."
)


def _reason(message: Any) -> str | None:
    metadata = getattr(message, "metadata", None)
    if not isinstance(metadata, dict) or metadata.get("authored_by") != "host":
        return None
    return str(metadata.get("authored_reason") or "") or None


def _is_person_turn(message: Any) -> bool:
    """A user-role turn the person wrote (never a host notice, never a tool result)."""
    from matrx_ai.config.tools_config import ToolResultContent
    from matrx_ai.config.typed_text_last import is_host_authored

    if getattr(message, "role", None) != "user" or is_host_authored(message):
        return False
    content = list(getattr(message, "content", None) or [])
    return not content or not all(isinstance(block, ToolResultContent) for block in content)


def retire_spent_run_notices(messages: list[Any]) -> list[Any] | None:
    """``messages`` with every spent run-end notice replaced (copies), or None when none is spent."""
    from matrx_ai.config.unified_content import TextContent

    last_person = max((i for i, m in enumerate(messages) if _is_person_turn(m)), default=-1)
    out: list[Any] = []
    changed = False
    for index, message in enumerate(messages):
        if index < last_person and _reason(message) in RUN_END_NOTICE_REASONS:
            twin = copy(message)
            twin.content = [TextContent(text=SPENT_RUN_NOTICE)]
            out.append(twin)
            changed = True
        else:
            out.append(message)
    return out if changed else None


__all__ = ["RUN_END_NOTICE_REASONS", "SPENT_RUN_NOTICE", "retire_spent_run_notices"]
