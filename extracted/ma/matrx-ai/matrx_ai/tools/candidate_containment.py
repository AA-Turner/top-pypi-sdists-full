"""Mandate-candidate containment for tool calls — decided BEFORE a call can act.

When ``AppContext.metadata["mandate_candidate"]`` is present, every tool call
the executor sees gets exactly one disposition before anything happens
(PLAN.md P3, P11, P12):

* ``borrowed`` — the live run made this same call (same tool, canonically-equal
  arguments) and the host can hand back the exact model-facing result it got.
  Any class. Nothing happens twice, nothing is invented. Checked FIRST, so a
  repeated read sees the live run's data, not fresher data.
* ``real`` — the invocation's effective side-effect class is ``read_only`` or
  ``paid_read`` (external MCP only when ``read_only``), and it is not
  client-delegated. Agent-as-tool calls (``ToolType.AGENT``) are also real: the
  child inherits the marker and every one of ITS calls comes back through here.
* ``stopped`` — everything else: every write class, an UNCLASSIFIED (NULL) tool
  (read as the most dangerous class), every client-delegated tool (no client
  exists in the background — the tool stays OFFERED, containment stops at the
  call), every external MCP tool not classified ``read_only``. A stop is
  TERMINAL: the run ends with ``status="candidate_stopped"``; the model is never
  fed an invented success or error, and the delegation suspend/resume machinery
  is never used.

The host supplies borrowed results through ONE injected seam,
:func:`set_candidate_borrow_lookup`; the default finds nothing (so nothing is
ever borrowed until a host installs it).
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from matrx_graph.candidate import (
    CANDIDATE_LEDGER_KEY,
    CANDIDATE_STOPPED_STATUS,
    MANDATE_CANDIDATE_KEY,
    CandidateStop,
    ToolDisposition,
    args_digest,
    candidate_context_metadata,
    candidate_ledger,
    candidate_marker,
    candidate_outcome,
    candidate_stop,
    canonical_args,
    next_occurrence,
    next_seq,
    record_disposition,
    record_stop,
    tool_dispositions,
)
from pydantic import BaseModel

from matrx_ai.tools.side_effect_class import (
    PAID_READ,
    READ_ONLY,
    effective_invocation_side_effect_class,
)

logger = logging.getLogger(__name__)

#: Classes that may run for real inside a candidate.
REAL_CLASSES: frozenset[str] = frozenset({READ_ONLY, PAID_READ})
#: What an external MCP tool must be classified to run for real.
REAL_MCP_CLASSES: frozenset[str] = frozenset({READ_ONLY})
#: LOCAL tools that start a nested agent run. They run CONTAINED (disposition
#: ``real``): the child inherits the marker and the shared ledger in-process
#: (agent_call copies ``AppContext.metadata`` into the child; mandate_call and
#: staff_escalate never hand off inside a candidate — aidream
#: ``mandates/tools.py::run_resolved_holder``), so every call the child makes is
#: decided here, and a child's stop stops the parent. Reclassified from STOPPED
#: by Mandate Candidates C2/C3 once the guard proved containment follows the
#: child (``aidream/scripts/prove_candidate_sub_agent_containment_on_clone.py``).
SUB_AGENT_TOOLS: frozenset[str] = frozenset({"agent_call", "mandate_call", "staff_escalate"})
#: The one sub-agent write that is NOT the child's own tool call: agent_call's
#: ``remember`` enqueues a durable note INTO ANOTHER CONVERSATION. Stopped.
SUB_AGENT_WRITE_BACK_ARGS: tuple[str, ...] = ("remember", "remember_visible_to_user")
SUB_AGENT_STOP_REASON = (
    "sub-agent call with remember=true — it writes a durable note into another conversation"
)
#: The side_effect_class recorded for an agent-as-tool call (its children are contained).
AGENT_TOOL_CLASS = "agent"


class BorrowRequest(BaseModel):
    """What the borrow seam is asked: "did the live run make this exact call?"."""

    marker: dict[str, Any]
    tool_name: str
    canonical_args: str
    args_digest: str
    occurrence: int
    """1-based: this is the Nth time the candidate made this exact call. Match it
    to the live run's Nth identical call (so a repeated read borrows in order)."""
    call_id: str


class BorrowedToolResult(BaseModel):
    """The live run's model-facing result for one call, exactly as the model saw it."""

    content: Any
    """The ``content`` the live model received: a string, or the provider
    content-block list. Handed to the candidate model unchanged."""
    is_error: bool = False
    live_call_id: str | None = None


BorrowLookup = Callable[[BorrowRequest], Awaitable[BorrowedToolResult | None]]

_BORROW_LOOKUP: BorrowLookup | None = None


def set_candidate_borrow_lookup(lookup: BorrowLookup | None) -> None:
    """Install (or clear, with ``None``) the host's borrow lookup."""
    global _BORROW_LOOKUP
    _BORROW_LOOKUP = lookup


def get_candidate_borrow_lookup() -> BorrowLookup | None:
    return _BORROW_LOOKUP


@dataclass(frozen=True)
class ContainmentDecision:
    disposition: str
    side_effect_class: str
    seq: int
    args_digest: str
    borrowed: BorrowedToolResult | None = None
    stopped_reason: str | None = None

    def as_record(self) -> dict[str, Any]:
        return {
            "disposition": self.disposition,
            "side_effect_class": self.side_effect_class,
            "seq": self.seq,
            "args_digest": self.args_digest,
            "borrowed_from_call_id": self.borrowed.live_call_id if self.borrowed else None,
            "stopped_reason": self.stopped_reason,
        }


def classify_call(
    tool_def: Any,
    arguments: dict[str, Any],
    *,
    is_delegated: bool,
) -> tuple[str, str | None]:
    """``(effective_class, stop_reason)`` — ``stop_reason`` is None when it may run for real.

    Pure: no seam, no ledger. Delegation is checked FIRST because the effect
    happens on a client that does not exist in the background, whatever the class.
    """
    from matrx_ai.tools.models import ToolType

    tool_type = getattr(tool_def, "tool_type", None)
    if tool_type == ToolType.AGENT:
        if is_delegated:
            return AGENT_TOOL_CLASS, "client-delegated tool: no client exists in a candidate run"
        return AGENT_TOOL_CLASS, None

    cls = effective_invocation_side_effect_class(tool_def, arguments)
    if getattr(tool_def, "name", None) in SUB_AGENT_TOOLS:
        if any((arguments or {}).get(key) for key in SUB_AGENT_WRITE_BACK_ARGS):
            return cls, SUB_AGENT_STOP_REASON
        if is_delegated:
            return cls, "client-delegated tool: no client exists in a candidate run"
        return AGENT_TOOL_CLASS, None
    if is_delegated:
        return cls, "client-delegated tool: no client exists in a candidate run"
    if tool_type == ToolType.EXTERNAL_MCP:
        if cls in REAL_MCP_CLASSES:
            return cls, None
        return cls, f"external MCP tool classified {cls!r} (only read_only runs for real)"
    if cls in REAL_CLASSES:
        return cls, None
    raw = getattr(tool_def, "side_effect_class", None)
    if raw is None:
        return cls, "unclassified tool (NULL side_effect_class counts as the most dangerous class)"
    return cls, f"side_effect_class {cls!r} changes things; only read_only / paid_read run for real"


async def decide(
    tool_def: Any,
    arguments: dict[str, Any],
    *,
    call_id: str,
    is_delegated: bool,
) -> ContainmentDecision | None:
    """Decide one call under the ambient marker, record it, and return it.

    ``None`` when no candidate marker is in scope (containment off). Never raises:
    a failing borrow seam is treated as "nothing to borrow" and announced.
    """
    marker = candidate_marker()
    if marker is None:
        return None
    ledger = candidate_ledger()
    assert ledger is not None  # marker present ⇒ ledger exists (created loudly if absent)

    tool_name = getattr(tool_def, "name", "") or ""
    digest = args_digest(arguments)
    seq = next_seq(ledger)
    occurrence = next_occurrence(ledger, tool_name, digest)
    cls, stop_reason = classify_call(tool_def, arguments, is_delegated=is_delegated)

    from matrx_ai.tools.models import ToolType

    borrowed: BorrowedToolResult | None = None
    lookup = _BORROW_LOOKUP
    # An agent-as-tool call is never borrowed: its child runs contained, and
    # each of the CHILD's calls is borrowed or not on its own.
    if lookup is not None and getattr(tool_def, "tool_type", None) != ToolType.AGENT:
        try:
            borrowed = await lookup(
                BorrowRequest(
                    marker=dict(marker),
                    tool_name=tool_name,
                    canonical_args=canonical_args(arguments),
                    args_digest=digest,
                    occurrence=occurrence,
                    call_id=call_id,
                )
            )
        except Exception:  # noqa: BLE001 — a broken seam must never unlock a write
            logger.exception(
                "[candidate containment] borrow lookup raised for %s — treating as not borrowable",
                tool_name,
            )
            borrowed = None

    if borrowed is not None:
        decision = ContainmentDecision("borrowed", cls, seq, digest, borrowed=borrowed)
    elif stop_reason is None:
        decision = ContainmentDecision("real", cls, seq, digest)
    else:
        decision = ContainmentDecision("stopped", cls, seq, digest, stopped_reason=stop_reason)

    record_disposition(
        ledger,
        ToolDisposition(
            seq=seq,
            tool=tool_name,
            side_effect_class=cls,
            disposition=decision.disposition,  # type: ignore[arg-type]
            args_digest=digest,
            borrowed_from_call_id=borrowed.live_call_id if borrowed else None,
            stopped_reason=decision.stopped_reason,
        ),
    )
    if decision.disposition == "stopped":
        record_stop(
            ledger,
            CandidateStop(
                step=seq,
                tool=tool_name,
                args=arguments,
                class_=cls,
                reason=decision.stopped_reason,
            ),
        )
    return decision


__all__ = [
    "AGENT_TOOL_CLASS",
    "BorrowLookup",
    "BorrowRequest",
    "BorrowedToolResult",
    "CANDIDATE_LEDGER_KEY",
    "CANDIDATE_STOPPED_STATUS",
    "ContainmentDecision",
    "MANDATE_CANDIDATE_KEY",
    "REAL_CLASSES",
    "REAL_MCP_CLASSES",
    "SUB_AGENT_STOP_REASON",
    "SUB_AGENT_TOOLS",
    "SUB_AGENT_WRITE_BACK_ARGS",
    "args_digest",
    "candidate_context_metadata",
    "candidate_ledger",
    "candidate_marker",
    "candidate_outcome",
    "candidate_stop",
    "canonical_args",
    "classify_call",
    "decide",
    "get_candidate_borrow_lookup",
    "set_candidate_borrow_lookup",
    "tool_dispositions",
]
