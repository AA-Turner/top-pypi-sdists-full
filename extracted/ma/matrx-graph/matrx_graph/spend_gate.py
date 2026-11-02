"""Caller refusals and the per-run spend check — what a fan-out may NOT launch.

THE DEFECT THIS CLOSES (live 2026-10-27, run 1aa73a14): a ``control.map`` dispatched 199 paid
``ai.mandate.start`` items at once. The host's run-approval gate decides once per request from
memory, so ~141 paid calls landed in one minute before the $1-per-run hold could fire; after the
hold, every refused item was re-dispatched again and again (615 node_failed) — a refusal that can
never succeed by retrying, retried.

Two engine rules, both payload-blind (matrx-graph never learns what money, an agent or an
approval IS):

* **A caller refusal is final.** A gate saying no before anything was spent — a spend approval
  waiting, a protected account, a permission refusal — is marked by its SOURCE: an exception sets
  ``is_caller_refusal = True`` (anywhere on its ``__cause__``/``__context__`` chain), a returned
  ``Failure`` carries ``details[CALLER_REFUSAL_KEY] = True``. The scheduler never retries, never
  walks a refused attempt forward on replay, and ends the item with a typed refusal outcome.
* **A cost-bearing step asks before it launches.** The host installs ONE async
  :data:`SpendGate` (``configure_spend_gate``); the scheduler asks it right before each fresh
  attempt of a cost-bearing node (``NodeCategory.AGENT`` / ``LLM``) — after the earlier items of the
  same fan-out settled, because launches queue on the fan-out bound. A refusal latches for the rest
  of that drive: no further cost-bearing item of the run is dispatched, and the run parks with the
  refusal's sentence and ``approval_url``.

With no gate installed nothing is asked (a standalone install has no ledger); the refusal rule
still applies to refusals the steps themselves report.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from matrx_graph.types.primitives import NodeCategory

#: The flag a failure's ``details`` carry when the failure is a caller refusal. The same word
#: matrx-ai stamps on its error events (``providers/caller_refusal.CALLER_REFUSAL_KEY``).
CALLER_REFUSAL_KEY = "caller_refusal"

#: Node categories whose steps spend money per invocation.
COST_BEARING_CATEGORIES: frozenset[NodeCategory] = frozenset({NodeCategory.AGENT, NodeCategory.LLM})


def is_cost_bearing(spec: Any) -> bool:
    """True when the node's spec declares a category that spends per invocation."""
    return getattr(spec, "category", None) in COST_BEARING_CATEGORIES


def _refused_exception(exc: BaseException | None, *, max_depth: int = 16) -> bool:
    seen: set[int] = set()
    stack: list[Any] = [exc]
    while stack and len(seen) < max_depth:
        node = stack.pop()
        if node is None or id(node) in seen:
            continue
        seen.add(id(node))
        if getattr(node, "is_caller_refusal", False) is True:
            return True
        node_error = getattr(node, "node_error", None)
        if node_error is not None and _refused_details(getattr(node_error, "details", None)):
            return True
        for attr in ("__cause__", "__context__", "terminal_exception", "exception"):
            carried = getattr(node, attr, None)
            if isinstance(carried, BaseException):
                stack.append(carried)
    return False


def _refused_details(details: Any) -> bool:
    return isinstance(details, Mapping) and details.get(CALLER_REFUSAL_KEY) is True


def is_caller_refusal(
    *,
    exc: BaseException | None = None,
    node_error: Any = None,
    error: Mapping[str, Any] | None = None,
) -> bool:
    """True when a failure is a caller refusal: never retried, re-dispatched or auto-resumed.

    ``exc`` answers by its type (``is_caller_refusal``) anywhere on its chain, ``node_error`` (a
    ``NodeError``) and ``error`` (a persisted error dict) by ``details.caller_refusal``.
    """
    if exc is not None and _refused_exception(exc):
        return True
    if node_error is not None and _refused_details(getattr(node_error, "details", None)):
        return True
    if isinstance(error, Mapping):
        if _refused_details(error.get("details")) or error.get(CALLER_REFUSAL_KEY) is True:
            return True
    return False


@dataclass(frozen=True)
class SpendQuery:
    """What the scheduler tells the host about the step it is about to launch."""

    run_id: str
    node_id: str
    spec_type: str
    #: The invocation's own AppContext (actor, organization, request, metadata).
    app: Any
    definition_id: str = ""


@dataclass(frozen=True)
class SpendRefusal:
    """The host's no: one plain sentence, a stable code, and where a person approves it."""

    code: str
    message: str
    approval_url: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def node_error_details(self) -> dict[str, Any]:
        out: dict[str, Any] = {**self.details, CALLER_REFUSAL_KEY: True, "refusal_code": self.code}
        if self.approval_url:
            out["approval_url"] = self.approval_url
        return out


SpendGate = Callable[[SpendQuery], Awaitable[SpendRefusal | None]]

_gate: SpendGate | None = None


def configure_spend_gate(gate: SpendGate | None) -> None:
    """Host wiring: the ONE async per-run spend check (None removes it)."""
    global _gate
    _gate = gate


def spend_gate() -> SpendGate | None:
    return _gate


__all__ = [
    "CALLER_REFUSAL_KEY",
    "COST_BEARING_CATEGORIES",
    "SpendGate",
    "SpendQuery",
    "SpendRefusal",
    "configure_spend_gate",
    "is_caller_refusal",
    "is_cost_bearing",
    "spend_gate",
]


# ---------------------------------------------------------------------------
# THE INVOCATION SPEND TALLY — node_cost equals the ledger, whatever the step's ending.
# ---------------------------------------------------------------------------
#
# Live 2026-10-27, run 1aa73a14: the ledger (chat.request) held $2.2456 for the run, its node_cost
# events $0.46. A step's cost was settled only from the usage block of a step that RETURNED
# (Success, or a Failure carrying ``details.usage``); a paid step that RAISED after spending (a
# pool timeout while saving, a refused second call) or was CANCELLED settled nothing. The tally
# closes that: the scheduler opens one per invocation (a ContextVar, so every task the step starts
# inherits it), the host's request-ledger writer notes every paid request row it queues
# (:func:`note_request_spend` — matrx-ai's ``queue_request_create``), and when the invocation ends,
# however it ends, the scheduler settles whatever the tally holds beyond what its node_cost events
# already said. Payload-blind: a row id and numbers.

from contextvars import ContextVar, Token  # noqa: E402

_INVOCATION_SPEND: ContextVar[dict[str, dict[str, Any]] | None] = ContextVar(
    "matrx_graph_invocation_spend", default=None
)


def open_invocation_spend() -> tuple[dict[str, dict[str, Any]], Token]:
    """Open this task's tally (scheduler only). Returns ``(tally, token)`` for :func:`close_invocation_spend`."""
    tally: dict[str, dict[str, Any]] = {}
    return tally, _INVOCATION_SPEND.set(tally)


def close_invocation_spend(token: Token) -> None:
    _INVOCATION_SPEND.reset(token)


def note_request_spend(
    row_id: str,
    *,
    cost: Any = None,
    input_tokens: Any = None,
    output_tokens: Any = None,
) -> None:
    """The host's ledger writer: one paid request row was written for the running step. No-op
    outside a workflow step; a later note for the same row replaces the earlier one. Never raises."""
    tally = _INVOCATION_SPEND.get()
    if tally is None or not row_id:
        return
    try:
        tally[str(row_id)] = {
            "cost_usd": float(cost or 0.0),
            "input_tokens": int(input_tokens or 0),
            "output_tokens": int(output_tokens or 0),
        }
    except (TypeError, ValueError):
        return


def tally_totals(tally: dict[str, dict[str, Any]] | None) -> tuple[float, int, int]:
    """``(cost_usd, input_tokens, output_tokens)`` of a tally (zeros when empty)."""
    if not tally:
        return 0.0, 0, 0
    rows = list(tally.values())
    return (
        sum(float(r.get("cost_usd") or 0.0) for r in rows),
        sum(int(r.get("input_tokens") or 0) for r in rows),
        sum(int(r.get("output_tokens") or 0) for r in rows),
    )


@dataclass(frozen=True)
class InterruptedAttempt:
    """The ledger spend of one step attempt a server restart cut off.

    The process holding that attempt's tally died with it, so the host reads the spend back
    from its request ledger and hands it to ``Scheduler.resume``, which settles it as the
    step's ``interrupted`` node_cost — only on a step that is starting again; an attempt
    naming any other step (or none) is logged and left to the run's request ledger."""

    request_id: str
    node_id: str | None = None
    cost_usd: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    model: str | None = None


__all__ += [
    "InterruptedAttempt",
    "close_invocation_spend",
    "note_request_spend",
    "open_invocation_spend",
    "tally_totals",
]
