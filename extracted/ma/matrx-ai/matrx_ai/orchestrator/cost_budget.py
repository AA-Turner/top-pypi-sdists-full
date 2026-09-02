"""Tree-wide dollar budget for one user request (parent + all sub-agents).

One user click = one ``cx_user_request`` = the total cost of everything it
triggered, INCLUDING every sub-agent it spawns (sub-agents inherit the parent's
``request_id`` / ``user_request_id``). A sub-agent tree can fan out fast — a
runaway agent spawning agents spawning agents — and rack up real money with no
ceiling: the per-count spawn caps bound the NUMBER of children, never the
DOLLARS. This module is that dollar ceiling, shared across the whole tree under
one user request.

How it works:
- Every billed model call folds its cost into a per-``user_request_id``
  accumulator at the executor's ``add_usage`` chokepoint. Because parent turns
  and every sub-agent share the same ``request_id``, one accumulator naturally
  sums the entire tree.
- Before a turn's tool calls run, the orchestrator reads ``remaining_budget`` and
  threads it into ``ToolContext.cost_budget_remaining``; the existing
  ``ToolGuardrails._check_cost_budget`` then BLOCKS new (expensive / spawning)
  tool calls LOUDLY once the tree is out of budget — never silently.
- The accumulator is released when the request owner finalizes (or on cancel)
  so the process-local map can't grow without bound.

This is a guardrail, not an accounting record: the authoritative per-call cost
still lives on the ``cx_request`` rows. The accumulator is an in-memory,
conservative running total (a call whose cost can't be computed yet contributes
0 — erring toward letting work proceed, never toward a phantom block).
"""

from __future__ import annotations

import threading

# ── THE TUNING KNOB ─────────────────────────────────────────────────────────
# Dollar ceiling for the WHOLE sub-agent tree under one user request. Start
# CONSERVATIVE and ease off as we learn how trees behave — change THIS constant
# (a code push) to widen or narrow the ceiling. It is deliberately a CAPS
# constant, NOT an env var: a silent prod/dev mismatch on a money guardrail is
# exactly the failure mode we refuse (CLAUDE.md "a new env var fails SILENTLY").
# Set to ``None`` to disable the budget entirely (no ceiling).
#
# Chosen so normal single-agent chat (well under a dollar per user request,
# even across many turns) is never affected, while a runaway fan-out — which can
# reach hundreds of dollars — is caught long before it does real damage.
TREE_COST_CEILING_USD: float | None = 25.0

_accrued: dict[str, float] = {}
_lock = threading.Lock()


def record_tree_cost(user_request_id: str | None, cost: float | None) -> None:
    """Fold a billed call's cost into the tree accumulator for its user request.

    No-op on a missing id or a non-positive / unknown cost — a call whose cost
    can't yet be computed simply doesn't count (conservative toward allowing
    work, never toward a phantom block)."""
    if not user_request_id or not cost or cost <= 0:
        return
    with _lock:
        _accrued[user_request_id] = _accrued.get(user_request_id, 0.0) + float(cost)


def remaining_budget(user_request_id: str | None) -> float | None:
    """Dollars left for this user request's whole tree, or ``None`` when no
    budget applies (disabled, or unknown request id). ``None`` means the
    guardrail treats the budget as absent — never as exhausted."""
    if TREE_COST_CEILING_USD is None or not user_request_id:
        return None
    with _lock:
        return TREE_COST_CEILING_USD - _accrued.get(user_request_id, 0.0)


def accrued_cost(user_request_id: str | None) -> float:
    """The running tree total recorded so far for this user request."""
    if not user_request_id:
        return 0.0
    with _lock:
        return _accrued.get(user_request_id, 0.0)


def release_tree_budget(user_request_id: str | None) -> None:
    """Drop the accumulator for a finished request so the map can't grow without
    bound. Safe to call more than once."""
    if not user_request_id:
        return
    with _lock:
        _accrued.pop(user_request_id, None)
