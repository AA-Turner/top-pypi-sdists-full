"""Pydantic models for the durable Action Ledger.

The ledger is a per-task, append-only record of every tool invocation's
outcome (writes, verifies, reads, plan-management calls). It survives
context compaction unchanged so the resuming agent has authoritative
evidence of what already happened in the real world — not just what the
summarizer LLM remembered.

Design notes:

* ``LedgerEntryClass`` separates *kind of side effect* from tool name. The
  optimizer uses this split for two things: (a) re-injecting a compact
  ``<authoritative_ledger>`` block into the post-compaction continuation
  prefers WRITE/VERIFY entries over READ noise; (b) the completion-evidence
  detector pairs WRITEs with VERIFYs to decide if a task is already done
  even when ``deep_planning`` items aren't all toggled.
* ``target`` is the canonicalized identifier the WRITE/VERIFY operates on
  (table name, file path, URL, plan-item UUID). When two entries share a
  target with opposite classes and matching ``result_signature`` digits,
  the detector treats them as a write+verify pair.
* ``result_signature`` is a short, machine-readable summary like
  ``rows_written=N`` / ``exit=0`` / ``http=201``. It's what the detector
  cross-checks against verify entries — preview text alone is too noisy.
* ``survives_compaction`` is always True today; the field exists so a future
  per-tenant config can mark sensitive entries as ephemeral without
  changing the storage shape.
"""

from enum import Enum
from typing import List, Literal, Optional, Set, Tuple

from .shared import XPanderSharedModel


class LedgerEntryClass(str, Enum):
    """Coarse classification of a tool call's effect on the world.

    The detector cares about WRITE/VERIFY pairs; the rest are recorded
    for the authoritative-ledger block but ignored by evidence logic.
    """

    READ = "read"
    """Pure observation — GET, file_read, list, schema introspection."""

    WRITE = "write"
    """Mutation — INSERT, file_write, POST, PUT, DELETE, exec with side effects."""

    VERIFY = "verify"
    """Post-write check — SELECT count, HEAD, file-stat, GET-by-id after a write."""

    PLAN = "plan"
    """Deep-planning lifecycle tool (create/start/complete plan items)."""

    INTERNAL = "internal"
    """SDK-internal — xpcompact_context, xpfinalize_task, etc."""


class LedgerEntry(XPanderSharedModel):
    """One tool invocation's durable record."""

    seq: int
    """Monotonic per-task counter. Used to order entries deterministically
    even if timestamps collide."""

    ts: str
    """ISO-8601 UTC timestamp of when the entry was finalized."""

    tool_call_id: Optional[str] = None
    """The agno/LLM tool_call id when present — lets the detector dedupe
    repeated retries against the same call."""

    tool_name: str

    entry_class: LedgerEntryClass = LedgerEntryClass.READ
    """READ is the safe default; classifier escalates to WRITE/VERIFY when
    the tool name + args + result match a known pattern."""

    target: Optional[str] = None
    """Canonicalized identifier the call operates on (table, path, URL).
    Required for evidence pairing — entries with no target never count
    as evidence."""

    args_preview: str = ""
    """Head/tail-trimmed, secret-redacted view of the call args."""

    status: Literal["ok", "error"] = "ok"

    result_preview: str = ""
    """Head/tail-trimmed, secret-redacted view of the result."""

    result_signature: Optional[str] = None
    """Short machine-readable summary like ``rows_written=N`` or ``http=201``."""

    workspace_offload_path: Optional[str] = None
    """When the result was L1-offloaded, the workspace path the preview
    points at. Lets a finalize-mode call reread the full content."""

    survives_compaction: bool = True


class EvidenceReport(XPanderSharedModel):
    """Output of ``detect_completion_evidence``.

    The retry path consults this before firing pre_retry compaction. If
    ``has_evidence`` is True and the number of uncompleted plan items is
    small, we skip the retry and enter Finalize-Only mode.
    """

    has_evidence: bool = False

    write_verify_pairs: List[Tuple[int, int]] = []
    """(write_seq, verify_seq) pairs the detector matched."""

    matched_plan_items: List[str] = []
    """Plan-item UUIDs whose target appears in a write+verify pair —
    the agent has already done these even if not toggled."""

    uncompleted_count: int = 0
    """How many plan items are still ``completed=False`` at detection time."""

    rationale: str = ""
    """Human-readable summary surfaced in logs + activity events."""


class FinalizeOnlyState(XPanderSharedModel):
    """State carried on ``task._xp_context_optimizer._finalize_state``.

    Lives on the optimizer (not the task) so it resets when a new task
    starts, but its mutation is mirrored to the ledger via
    ``xpfinalize_task`` so cross-process recovery sees it.
    """

    active: bool = False

    reason: Optional[
        Literal[
            "evidence",
            "compact_loop",
            "pre_retry_exhausted",
            "token_floor",
            "stagnant_compactions",
            "repeated_tool_call",
            "error_streak",
            "tool_overuse",
            "plan_churn",
            "no_progress",
            "plan_complete",
            "wrapup_budget",
        ]
    ] = None

    entered_at_compaction_attempt: int = 0

    allowed_tools: Set[str] = {
        "xpfinalize_task",
        "xpget_agent_plan",
        "xpworkspace-context-retrieve",
        "xpworkspace-file-read",
    }
    """Tools the gate lets through while finalize is active. Read-only ops
    are kept so the agent can re-read offloaded context when composing
    the final answer."""

    evidence: Optional[EvidenceReport] = None
