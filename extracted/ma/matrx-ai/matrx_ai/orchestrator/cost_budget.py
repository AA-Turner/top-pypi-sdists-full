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
from collections import OrderedDict
from typing import Any

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

#: Bound on the trees held in memory. A root that never finishes in this process (a
#: workflow run whose steps never own it, a worker that died) is evicted oldest-first,
#: so the maps never grow without bound (review 6 N6-4).
_MAX_TREES = 50_000

_accrued: OrderedDict[str, float] = OrderedDict()
#: R38 (Agent Factory review 5 N5-4): a run that keeps its OWN request record
#: (``run_agent(independent_request=True)``) still spends against its ROOT tree's
#: cap. ``_root_of`` maps such a request id to the root request whose accumulator it
#: shares; ``_members`` is the reverse map, dropped with the root.
_root_of: dict[str, str] = {}
_members: dict[str, set[str]] = {}
#: Roots whose own run finished while linked members (detached children) still ran:
#: their total stays until the last member finishes (review 6 §2 route 3).
_closing: set[str] = set()
_lock = threading.Lock()


def owns_tree(ctx: Any) -> bool:
    """Whether the run on ``ctx`` owns its request's tree — the only run that may release it.

    Not a sub-agent (``parent_request_id`` set) and not a workflow step: a step runs on
    the ROOT's ``request_id`` with ``parent_request_id=None`` (``fork_for_workflow_step``),
    so reading ownership from ``parent_request_id`` alone let a workflow-holder mandate's
    step agent release the whole tree's accumulator mid-tree (review 6 N6-4). No context
    = a bare run that owns what it opened."""
    if ctx is None:
        return True
    if getattr(ctx, "parent_request_id", None):
        return False
    return str(getattr(ctx, "origin_class", "") or "") != "workflow" and str(
        getattr(ctx, "conversation_type", "") or ""
    ) != "workflow"


def _evict() -> None:
    """Drop the oldest trees past ``_MAX_TREES``. Lock held."""
    while len(_accrued) > _MAX_TREES:
        root, _ = _accrued.popitem(last=False)
        _closing.discard(root)
        for member in _members.pop(root, set()):
            _root_of.pop(member, None)


def _root(user_request_id: str) -> str:
    """The tree root a request spends against (itself when it is a root). Lock held."""
    return _root_of.get(user_request_id, user_request_id)


def link_tree_request(child_request_id: str | None, parent_request_id: str | None) -> None:
    """Count ``child_request_id``'s spend toward ``parent_request_id``'s ROOT tree.

    Called when a run is given its own request record inside a tree: the record is
    its own, the cap is the tree's — record-keeping never escapes the cap (R38)."""
    if not child_request_id or not parent_request_id or child_request_id == parent_request_id:
        return
    with _lock:
        root = _root(parent_request_id)
        if root == child_request_id:
            return
        _root_of[child_request_id] = root
        _members.setdefault(root, set()).add(child_request_id)
        _accrued.setdefault(root, 0.0)
        _accrued.move_to_end(root)
        _evict()


def tree_root_request_id(user_request_id: str | None) -> str | None:
    """The root request whose cap ``user_request_id`` spends against."""
    if not user_request_id:
        return None
    with _lock:
        return _root(user_request_id)


def record_tree_cost(user_request_id: str | None, cost: float | None) -> None:
    """Fold a billed call's cost into the tree accumulator for its user request.

    No-op on a missing id or a non-positive / unknown cost — a call whose cost
    can't yet be computed simply doesn't count (conservative toward allowing
    work, never toward a phantom block)."""
    if not user_request_id or not cost or cost <= 0:
        return
    with _lock:
        root = _root(user_request_id)
        _accrued[root] = _accrued.get(root, 0.0) + float(cost)
        _accrued.move_to_end(root)
        _evict()


def remaining_budget(user_request_id: str | None) -> float | None:
    """Dollars left for this user request's whole tree, or ``None`` when no
    budget applies (disabled, or unknown request id). ``None`` means the
    guardrail treats the budget as absent — never as exhausted."""
    if TREE_COST_CEILING_USD is None or not user_request_id:
        return None
    with _lock:
        return TREE_COST_CEILING_USD - _accrued.get(_root(user_request_id), 0.0)


def accrued_cost(user_request_id: str | None) -> float:
    """The running tree total recorded so far for this user request's tree."""
    if not user_request_id:
        return 0.0
    with _lock:
        return _accrued.get(_root(user_request_id), 0.0)


def forget_tree(user_request_id: str | None) -> None:
    """Drop a tree outright — its total, its links and any pending close. For tests and
    for a host that knows the whole tree is over; a run's own finalize calls
    :func:`release_tree_budget`."""
    if not user_request_id:
        return
    with _lock:
        root = _root(user_request_id)
        _accrued.pop(root, None)
        _closing.discard(root)
        for member in _members.pop(root, set()):
            _root_of.pop(member, None)


def release_tree_budget(user_request_id: str | None) -> None:
    """Drop the accumulator for a finished request so the map can't grow without
    bound. Safe to call more than once. A linked (non-root) request drops only its
    link — the tree's total stays until the root itself finishes. A root finishing
    while linked members still run (a detached child) keeps its total until the last
    member finishes, so that child never accrues to a fresh 0."""
    if not user_request_id:
        return
    with _lock:
        root = _root_of.pop(user_request_id, None)
        if root is not None:
            members = _members.get(root, set())
            members.discard(user_request_id)
            if not members and root in _closing:
                _closing.discard(root)
                _members.pop(root, None)
                _accrued.pop(root, None)
            return
        if _members.get(user_request_id):
            _closing.add(user_request_id)
            return
        _closing.discard(user_request_id)
        _members.pop(user_request_id, None)
        _accrued.pop(user_request_id, None)
