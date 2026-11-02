"""Was this park already answered? The ONE reading of a question's checkpoint.

A run parked on a question writes its checkpoint with ``interrupt_payload`` set.
When a person answers, ``Scheduler.resume`` records the answer as the asking
step's outcome (at the checkpoint's step) and runs on — but the next checkpoint is
only written when the following super-step ends. Until then the LATEST checkpoint
is still the question's, so "the latest checkpoint has an interrupt payload" does
NOT mean "the run is waiting on a person". A process that dies in that window
leaves a run that was answered and working, and a reader that trusts the payload
alone treats it as unanswered (live run eedbb741, 2026-10-27: cancelled as
``interrupt_park`` after the person had answered).

The answer itself is the evidence: an outcome at the asking invocation's key.
A park that RELAYS a called workflow's question (``forwards_answer``) records no
outcome of its own — the answer goes down to the run that asked — so that case is
decided by the host, which can read the child run.
"""

from __future__ import annotations

from typing import Any


def asking_invocation(checkpoint: Any) -> Any | None:
    """The frontier invocation the question belongs to (marked ``is_interrupted``;
    the first frontier entry for checkpoints written before the mark existed)."""
    frontier = list(getattr(checkpoint, "next_invocations", None) or [])
    if not frontier:
        return None
    return next((ni for ni in frontier if getattr(ni, "is_interrupted", False)), frontier[0])


async def park_was_answered(checkpointer: Any, checkpoint: Any) -> bool:
    """True when the answer to this checkpoint's question is already recorded as
    the asking step's outcome. False for a checkpoint that asks nothing, or whose
    question nobody has answered yet."""
    if not getattr(checkpoint, "interrupt_payload", None):
        return False
    asking = asking_invocation(checkpoint)
    if asking is None:
        return False
    outcome = await checkpointer.get_outcome(
        run_id=checkpoint.run_id,
        step=checkpoint.step,
        node_id=asking.node_id,
        attempt=asking.attempt,
        dispatch_id=asking.dispatch_id,
        item_index=asking.item_index,
    )
    return outcome is not None


__all__ = ["asking_invocation", "park_was_answered"]
