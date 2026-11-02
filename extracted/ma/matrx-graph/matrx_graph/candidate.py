"""Mandate-candidate containment: the marker, the ledger, and the stop record.

A mandate *candidate* re-runs a real run's input through a different holder in
the background. It must never cause an effect: reads may run, writes never
happen for real, and when the candidate reaches something it may not do it
STOPS — terminally, honestly — instead of faking a result.

This module is the part of that containment every engine shares. It lives in
matrx-graph (not matrx-ai) because BOTH executors consult it: matrx-ai's tool
executor (every tool call) and this package's scheduler (every workflow node),
and matrx-ai depends on matrx-graph, never the reverse. The tool-level decision
(side-effect classes, borrowed results) lives in
``matrx_ai.tools.candidate_containment``.

The contract (common-docs/systems/intelligence/mandates/projects/mandate-candidates/REGISTER.md §2.1, §2.7):

* ``AppContext.metadata["mandate_candidate"] = {candidate_id, candidate_run_id,
  live_request_id}`` — the MARKER. Present ⇒ containment is on.
* ``AppContext.metadata["mandate_candidate_containment"]`` — the LEDGER, a plain
  JSON-safe dict shared BY REFERENCE with every child context (metadata forks
  are shallow copies), so a child agent's dispositions and its stop land in the
  one ledger the executor that set the marker reads back. Build both keys with
  :func:`candidate_context_metadata` — never set the marker alone.
* Every decision appends one ``tool_dispositions`` entry (disposition ``real`` /
  ``borrowed`` / ``stopped``, or ``contained`` for a call that starts a child run)
  ``{seq, tool, side_effect_class, disposition, args_digest,
  borrowed_from_call_id, stopped_reason}``; the FIRST stop is ``stopped_at``
  ``{step, tool, args, class, live_call_at_same_step}``.
"""

from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)

MANDATE_CANDIDATE_KEY = "mandate_candidate"
CANDIDATE_LEDGER_KEY = "mandate_candidate_containment"
CANDIDATE_STOPPED_STATUS = "candidate_stopped"

#: ``contained`` — a call that starts a CHILD agent run (``agent_call``,
#: ``mandate_call``, ``staff_escalate``, a saved agent offered as a tool). The call
#: itself runs, but the child inherits the marker and this ledger, so every call
#: the CHILD makes is decided here too and a stop in the child ends the parent.
Disposition = Literal["real", "borrowed", "stopped", "contained"]


class ToolDisposition(BaseModel):
    """One contained call — the §2.1 ``tool_dispositions`` element."""

    seq: int
    tool: str
    side_effect_class: str
    disposition: Disposition
    args_digest: str
    borrowed_from_call_id: str | None = None
    stopped_reason: str | None = None


class CandidateStop(BaseModel):
    """Where a candidate halted — the §2.1 ``stopped_at`` shape.

    ``live_call_at_same_step`` is left ``None`` here: only the host holds the
    live run's calls, and it fills this in when it records the pair.
    """

    model_config = ConfigDict(populate_by_name=True)

    step: int
    tool: str
    args: Any = None
    class_: str = Field(alias="class")
    reason: str | None = None
    live_call_at_same_step: Any = None

    def as_record(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, mode="json")


#: Workflow node types a candidate run may execute although they are neither
#: ``ActionTier.PURE`` nor an agent/LLM step. An EXPLICIT, NAMED list (chair
#: ruling 2026-09-30) — never widened by tier. Each entry was verified against
#: the node's code; the reason says what makes it safe. Everything else stops.
CANDIDATE_ALLOWED_NODE_TYPES: dict[str, str] = {
    "control.send": ("routes only: ctx.send() to a node inside this run, per list item; no I/O"),
    "control.map": (
        "fans out only: ctx.send() of each templated item to a node inside this run; no I/O"
    ),
    "output.to_frontend": (
        "emits only through the run's own emitter (silent in a candidate) and reads the "
        "kind catalog; writes nothing else"
    ),
    "data.read_record": (
        "a read as the run's own actor through the record gateway, whose protocol has "
        "read methods only (describe / may_read / read_row)"
    ),
    "http.get": (
        "an outbound GET with a hard-wired method (no method input exists), the same "
        "standing as a read_only web-fetch tool"
    ),
}


def canonical_args(args: Any) -> str:
    """The canonical JSON text of a call's arguments.

    Two calls are "the same call" when their tool names match and these strings
    are equal: keys sorted at every depth, no insignificant whitespace, non-JSON
    values rendered by ``str``. The host MUST record live calls through this
    same function, or no candidate call ever borrows.
    """
    return json.dumps(
        args if args is not None else {},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    )


def args_digest(args: Any) -> str:
    """sha256 hex of :func:`canonical_args`."""
    return hashlib.sha256(canonical_args(args).encode("utf-8")).hexdigest()


def new_candidate_ledger() -> dict[str, Any]:
    return {"seq": 0, "tool_dispositions": [], "stopped_at": None, "occurrences": {}}


def candidate_context_metadata(marker: dict[str, Any]) -> dict[str, Any]:
    """The two metadata keys a candidate context carries: marker + fresh ledger.

    Merge into the context the candidate runs under, e.g.
    ``ctx.with_overrides(metadata={**ctx.metadata, **candidate_context_metadata(m)})``.
    Keep a reference to the returned ledger (``[CANDIDATE_LEDGER_KEY]``): it is
    where every disposition and the stop are read back after the run.
    """
    missing = [
        k for k in ("candidate_id", "candidate_run_id", "live_request_id") if not marker.get(k)
    ]
    if missing:
        raise ValueError(f"mandate_candidate marker is missing {missing}")
    return {MANDATE_CANDIDATE_KEY: dict(marker), CANDIDATE_LEDGER_KEY: new_candidate_ledger()}


def _metadata_of(source: Any) -> dict[str, Any] | None:
    if source is None:
        from matrx_connect.context.app_context import try_get_app_context

        source = try_get_app_context()
        if source is None:
            return None
    if isinstance(source, dict):
        return source
    metadata = getattr(source, "metadata", None)
    return metadata if isinstance(metadata, dict) else None


def candidate_marker(source: Any = None) -> dict[str, Any] | None:
    """The marker on ``source`` (a metadata dict, an AppContext, or the ambient context)."""
    metadata = _metadata_of(source)
    if not metadata:
        return None
    marker = metadata.get(MANDATE_CANDIDATE_KEY)
    return marker if isinstance(marker, dict) and marker else None


def candidate_ledger(source: Any = None) -> dict[str, Any] | None:
    """The shared ledger, or ``None`` when containment is off.

    A marker without a ledger is a host defect (the executor that set it can
    never read what happened). The run is still contained — a ledger is created
    in place so decisions and the terminal stop still work — but it SCREAMS.
    """
    metadata = _metadata_of(source)
    if not metadata or candidate_marker(metadata) is None:
        return None
    ledger = metadata.get(CANDIDATE_LEDGER_KEY)
    if isinstance(ledger, dict):
        return ledger
    logger.error(
        "[candidate containment] %r is set without %r — the run is still contained, but "
        "the dispositions recorded here are invisible to whoever set the marker. Build the "
        "context with matrx_graph.candidate.candidate_context_metadata(marker).",
        MANDATE_CANDIDATE_KEY,
        CANDIDATE_LEDGER_KEY,
    )
    ledger = new_candidate_ledger()
    metadata[CANDIDATE_LEDGER_KEY] = ledger
    return ledger


def next_seq(ledger: dict[str, Any]) -> int:
    ledger["seq"] = int(ledger.get("seq") or 0) + 1
    return ledger["seq"]


def next_occurrence(ledger: dict[str, Any], tool: str, digest: str) -> int:
    """1-based count of how often this run has made this exact call.

    The key is ``<tool>:<digest>``: printable, because the ledger rides the candidate's
    request metadata into Postgres, which rejects NUL bytes (a ``\\x00`` separator made
    every contained call log a sanitizer ERROR). The digest is hex, so it stays unambiguous.
    """
    occurrences = ledger.setdefault("occurrences", {})
    key = f"{tool}:{digest}"
    occurrences[key] = int(occurrences.get(key) or 0) + 1
    return occurrences[key]


def record_disposition(ledger: dict[str, Any], entry: ToolDisposition) -> None:
    ledger.setdefault("tool_dispositions", []).append(entry.model_dump(mode="json"))


def record_stop(ledger: dict[str, Any], stop: CandidateStop) -> bool:
    """Record the run's stop. The FIRST stop wins; returns whether this one did."""
    if ledger.get("stopped_at") is not None:
        return False
    ledger["stopped_at"] = stop.as_record()
    return True


def candidate_stop(source: Any = None) -> dict[str, Any] | None:
    """The recorded ``stopped_at`` of the candidate run in scope, if it stopped."""
    ledger = candidate_ledger(source)
    if ledger is None:
        return None
    stop = ledger.get("stopped_at")
    return stop if isinstance(stop, dict) else None


def tool_dispositions(source: Any = None) -> list[dict[str, Any]]:
    ledger = candidate_ledger(source)
    if ledger is None:
        return []
    return list(ledger.get("tool_dispositions") or [])


def candidate_outcome(source: Any = None) -> dict[str, Any] | None:
    """``{"tool_dispositions": [...], "candidate_stopped": stopped_at|None}`` or None."""
    ledger = candidate_ledger(source)
    if ledger is None:
        return None
    return {
        "tool_dispositions": list(ledger.get("tool_dispositions") or []),
        CANDIDATE_STOPPED_STATUS: ledger.get("stopped_at"),
    }


__all__ = [
    "CANDIDATE_LEDGER_KEY",
    "CANDIDATE_STOPPED_STATUS",
    "MANDATE_CANDIDATE_KEY",
    "CandidateStop",
    "Disposition",
    "ToolDisposition",
    "args_digest",
    "candidate_context_metadata",
    "candidate_ledger",
    "candidate_marker",
    "candidate_outcome",
    "candidate_stop",
    "canonical_args",
    "new_candidate_ledger",
    "next_occurrence",
    "next_seq",
    "record_disposition",
    "record_stop",
    "tool_dispositions",
]
