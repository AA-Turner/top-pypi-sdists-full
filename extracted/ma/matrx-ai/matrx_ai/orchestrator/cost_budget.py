"""Tree-wide dollar budget for one user action (its turn + every child agent run).

One user action = one request TREE: the person's turn plus every child agent run it
spawns, at any depth. Every child owns its OWN turn (``chat.user_request``) — the fork
mints its ``request_id`` and freezes the tree's root as ``root_request_id``
(``AppContext.tree_request_id``). A sub-agent tree can fan out fast — a runaway agent
spawning agents spawning agents — and rack up real money with no ceiling: the
per-count spawn caps bound the NUMBER of children, never the DOLLARS. This module is
that dollar ceiling, shared across the whole tree.

How it works:
- Every billed model call folds its cost into the accumulator of its tree ROOT at the
  executor's ``add_usage`` chokepoint. A child's own request id is LINKED to its root
  (:func:`join_tree` at the child's run start; :func:`record_tree_cost` also links on a
  child's first spend), so one accumulator sums the entire tree.
- Before a turn's tool calls run, the orchestrator reads ``remaining_budget`` and
  threads it into ``ToolContext.cost_budget_remaining``; the existing
  ``ToolGuardrails._check_cost_budget`` then BLOCKS new (expensive / spawning)
  tool calls LOUDLY once the tree is out of budget — never silently.
- Every run releases ITS OWN request at finalize (:func:`release_tree_budget`): a child
  drops only its link; the root's total stays while any linked child still runs (a
  detached helper outliving its root stays capped) and is dropped by the last one out.
  A workflow step runs on the run's own id and never releases it.

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
#: Every child agent run owns its own request id and spends against its ROOT tree's
#: cap (R38). ``_root_of`` maps such a request id to the root request whose
#: accumulator it shares; ``_members`` is the reverse map (the refcount), dropped with
#: the root. An explicit ``link_tree_request`` (a factory build spending against its
#: calling run, ``cost_parent_request_id``) joins the same way.
_root_of: dict[str, str] = {}
_members: dict[str, set[str]] = {}
#: Roots whose own run finished while linked members (detached children) still ran:
#: their total stays until the last member finishes (review 6 §2 route 3).
_closing: set[str] = set()
_lock = threading.Lock()


def owns_tree(ctx: Any) -> bool:
    """Whether the run on ``ctx`` releases its own request at finalize.

    Every run does — a child agent run owns its own turn, and releasing it drops only
    its link (:func:`release_tree_budget`) — EXCEPT a workflow step, which runs on the
    workflow run's own ``request_id`` (``fork_for_workflow_step``) and would release the
    whole run's accumulator mid-run (review 6 N6-4). No context = a bare run that owns
    what it opened."""
    if ctx is None:
        return True
    return str(getattr(ctx, "origin_class", "") or "") != "workflow" and str(
        getattr(ctx, "conversation_type", "") or ""
    ) != "workflow"


def _ambient_root(user_request_id: str) -> str | None:
    """The ambient context's tree root when the context IS ``user_request_id``'s run."""
    try:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # noqa: BLE001 — no context, no root
        return None
    if ctx is None or str(getattr(ctx, "request_id", "") or "") != str(user_request_id):
        return None
    return str(getattr(ctx, "root_request_id", "") or "") or None


def join_tree(ctx: Any) -> None:
    """Link ``ctx``'s own request to its tree root (idempotent). Called at every run's
    start, so a child that has not spent yet already holds the root open: a detached
    helper outliving its root never restarts at a fresh 0."""
    if ctx is None:
        return
    link_tree_request(
        str(getattr(ctx, "request_id", "") or "") or None,
        str(getattr(ctx, "root_request_id", "") or "") or None,
    )


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


def record_tree_cost(
    user_request_id: str | None, cost: float | None, *, root_request_id: str | None = None
) -> None:
    """Fold a billed call's cost into the tree accumulator for its request's ROOT.

    ``root_request_id`` (default: the ambient context's, when the context is this
    request's run) links a child's own request to its tree on its first spend.
    No-op on a missing id or a non-positive / unknown cost — a call whose cost
    can't yet be computed simply doesn't count (conservative toward allowing
    work, never toward a phantom block)."""
    if not user_request_id or not cost or cost <= 0:
        return
    root_request_id = root_request_id or _ambient_root(user_request_id)
    if root_request_id:
        link_tree_request(user_request_id, root_request_id)
    with _lock:
        root = _root(user_request_id)
        _accrued[root] = _accrued.get(root, 0.0) + float(cost)
        _accrued.move_to_end(root)
        _evict()


def remaining_budget(
    user_request_id: str | None, *, root_request_id: str | None = None
) -> float | None:
    """Dollars left for this request's whole tree, or ``None`` when no budget applies
    (disabled, or unknown request id). ``None`` means the guardrail treats the budget
    as absent — never as exhausted. A child that has not spent yet reads its ROOT's
    total (``root_request_id``, default: the ambient context's)."""
    if TREE_COST_CEILING_USD is None or not user_request_id:
        return None
    root_request_id = root_request_id or _ambient_root(user_request_id)
    with _lock:
        root = _root(root_request_id or user_request_id)
        return TREE_COST_CEILING_USD - _accrued.get(root, 0.0)


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
