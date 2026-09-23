"""Per-subtree execution budget — a wall clock attached to ONE child run.

The tree-wide controls (``spine_control_check`` → the host's
``ensure_can_proceed``) resolve at the TREE ROOT: a cancel, a dollar budget or a
deadline there bounds the WHOLE turn, everything the person asked for. That is
the right shape for "stop this request", and the wrong shape for "the senior
desk gets about six minutes of the twenty this turn may take". A deadline placed
on the root to bound a child would stop the parent too; a deadline placed on the
child's spine control row is never polled, because the poll resolves the root.

So this module adds the missing axis: a budget that narrows ONE SUBTREE.

How it works, and why it is shaped this way
-------------------------------------------
* **It lives on ``AppContext.metadata``.** A child agent run forks the context
  (``child_agent_context``), which copies the metadata dict — so the budget
  reaches the child, every tool it calls, and every grandchild it spawns, with
  no fan-out, no registry and no DB read. The parent's own binding is restored
  when the tool call returns, so the parent loop is never bounded by its child's
  clock. Budgets NEST: a grandchild carries its parent's and its own, and the
  first one to expire stops it.

* **It is polled at the iteration boundary, exactly like the root controls**
  (``executor.execute_until_complete``). The loop finishes the tool it is
  holding, writes its messages, and exits through the SAME graceful path a
  cancel takes — the best answer so far is persisted and returned.

* **🚨 It never cancels mid-tool, and never uses ``asyncio.wait_for``.**
  Cancelling at the budget throws away work already paid for — the precise
  defect ``services/tooling/deferred_work.py`` exists to end ("the Senior Staff
  desk really ran, really thought, and its answer was thrown away"). A budget
  that destroys the answer is worse than no budget. The stop is always AT a
  boundary, and what the subtree has produced is what comes back, marked
  bounded.

* **Wall clock, not ``time.monotonic``.** A budgeted run can outlive its
  request (``deferred_work`` continues it detached) and is compared against by
  code that did not open it; an absolute epoch second means the same thing
  everywhere. Second-grain budgets do not care about clock skew.

The ITERATION half of a subtree budget is not here: an iteration ceiling is a
property of one loop, so it is passed down as ``execute_ai_request``'s own
``max_iterations`` and exits through its existing ``max_iterations_exceeded``
graceful path. This module owns the clock.
"""

from __future__ import annotations

import time
from typing import Any

#: Private ``AppContext.metadata`` key holding the ACTIVE budgets, innermost
#: last. A tuple of plain dicts so the value stays JSON-safe for anything that
#: serializes request metadata.
SUBTREE_BUDGET_METADATA_KEY = "runtime_subtree_budgets"

#: Smallest budget worth honoring. Below this a run cannot complete even one
#: provider call, so a caller asking for it has made a mistake; the opener
#: raises rather than silently producing a run that stops before it starts.
MIN_SUBTREE_BUDGET_SECONDS = 1


def active_budgets(metadata: Any) -> tuple[dict[str, Any], ...]:
    """The budgets in force for the subtree this metadata belongs to."""
    if not isinstance(metadata, dict):
        return ()
    raw = metadata.get(SUBTREE_BUDGET_METADATA_KEY)
    if not isinstance(raw, list | tuple):
        return ()
    return tuple(b for b in raw if isinstance(b, dict) and b.get("expires_at"))


def with_subtree_budget(
    metadata: dict[str, Any] | None,
    *,
    seconds: int,
    label: str,
    execution_id: str | None = None,
) -> dict[str, Any]:
    """Return a NEW metadata dict carrying ``metadata``'s budgets plus this one.

    Never mutates the input: concurrent sibling tool calls in one batch share
    the parent's metadata dict (``asyncio.gather``), and an in-place append
    would bind a sibling — and the parent — to a budget that was never theirs.
    """
    if int(seconds) < MIN_SUBTREE_BUDGET_SECONDS:
        raise ValueError(
            f"A subtree time budget must be at least {MIN_SUBTREE_BUDGET_SECONDS}s; "
            f"got {seconds}s, which would stop the run before its first call."
        )
    base = dict(metadata or {})
    budget = {
        "label": label,
        "seconds": int(seconds),
        "opened_at": time.time(),
        "expires_at": time.time() + int(seconds),
        "execution_id": str(execution_id) if execution_id else None,
    }
    base[SUBTREE_BUDGET_METADATA_KEY] = [*active_budgets(metadata), budget]
    return base


def expired_budget(metadata: Any, *, now: float | None = None) -> dict[str, Any] | None:
    """The budget that has run out, or None. Earliest expiry wins, so an outer
    budget stops an inner run whose own clock still has time on it."""
    moment = time.time() if now is None else now
    expired = [b for b in active_budgets(metadata) if float(b["expires_at"]) <= moment]
    if not expired:
        return None
    return min(expired, key=lambda b: float(b["expires_at"]))


def subtree_stop_reason(metadata: Any, *, now: float | None = None) -> str | None:
    """None to proceed; a short human reason when THIS subtree's clock is out.

    The string is what the loop shows and what the caller's ``bounded`` marker
    quotes, so it names the budget rather than talking about deadlines: the
    person is going to read a version of this sentence.
    """
    budget = expired_budget(metadata, now=now)
    if budget is None:
        return None
    return (
        f"the {budget['label']} ran out of its {int(budget['seconds'])}s time budget "
        "and stopped at a clean boundary with what it had"
    )


#: Marker the executor puts in front of a stop reason so a caller can tell a
#: subtree budget apart from a tree cancel, both of which exit the same way.
SUBTREE_BUDGET_STOP_MARKER = "subtree_budget_exhausted"


def is_subtree_budget_stop(reason: Any) -> bool:
    """True when a recorded stop reason / error came from a subtree budget."""
    return isinstance(reason, str) and SUBTREE_BUDGET_STOP_MARKER in reason


__all__ = [
    "MIN_SUBTREE_BUDGET_SECONDS",
    "SUBTREE_BUDGET_METADATA_KEY",
    "SUBTREE_BUDGET_STOP_MARKER",
    "active_budgets",
    "expired_budget",
    "is_subtree_budget_stop",
    "subtree_stop_reason",
    "with_subtree_budget",
]
