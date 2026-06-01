"""Typed Studio events — the vocabulary of the event spine.

Frozen Pydantic models, discriminated on `kind`. Phase 0 ships only the
scan-producer events; agent-theater and readiness events arrive with
their producers (Phase 1+) — we don't define event types nothing emits.

Every event carries `at` (wall-clock, tz-aware) so the JSONL recorder can
replay a real run with faithful timing later.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


def _now() -> datetime:
    return datetime.now().astimezone()


class _BaseEvent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    at: datetime = Field(default_factory=_now)


class ScanStarted(_BaseEvent):
    """A scan run is beginning."""

    kind: Literal["scan_started"] = "scan_started"
    mode: Literal["hcl", "plan"]
    target: str


class EvidenceFound(_BaseEvent):
    """One Evidence record was produced by a detector / manifest load.

    Carries just the projection a renderer needs to light the right star
    and (later) trace a citation — not the whole Evidence object.
    """

    kind: Literal["evidence_found"] = "evidence_found"
    detector_id: str
    ksis: list[str] = Field(default_factory=list)
    source_file: str
    line_start: int | None = None
    boundary_state: str = "boundary_undeclared"


class KsiEvidenced(_BaseEvent):
    """A KSI now has at least one piece of evidence (emitted once per KSI,
    after the scan, with the running count) — the 'star ignites' signal."""

    kind: Literal["ksi_evidenced"] = "ksi_evidenced"
    ksi: str
    evidence_count: int


class ScanFinished(_BaseEvent):
    """The scan run completed; carries the headline totals."""

    kind: Literal["scan_finished"] = "scan_finished"
    evidence_total: int
    by_source: dict[str, int] = Field(default_factory=dict)
    ksis_with_evidence: int = 0


# --- agent theater (Phase 1) -------------------------------------------

# The five gap-classification verdicts a star can take.
ClassificationStatus = Literal[
    "implemented",
    "partial",
    "not_implemented",
    "not_applicable",
    "evidence_layer_inapplicable",
]


class AgentStarted(_BaseEvent):
    """A reasoning agent run is beginning."""

    kind: Literal["agent_started"] = "agent_started"
    agent: str
    total_ksis: int


class BatchStarted(_BaseEvent):
    """The agent is about to classify a batch of KSIs (the 'now reasoning
    about these' beat)."""

    kind: Literal["batch_started"] = "batch_started"
    index: int
    total: int
    ksis: list[str] = Field(default_factory=list)


class KsiClassified(_BaseEvent):
    """A KSI got its verdict — the star turns to its classification color."""

    kind: Literal["ksi_classified"] = "ksi_classified"
    ksi: str
    status: ClassificationStatus
    evidence_count: int = 0
    rationale: str = ""


class AgentFinished(_BaseEvent):
    """The agent run completed; carries the verdict tally."""

    kind: Literal["agent_finished"] = "agent_finished"
    counts: dict[str, int] = Field(default_factory=dict)


StudioEvent = Annotated[
    ScanStarted
    | EvidenceFound
    | KsiEvidenced
    | ScanFinished
    | AgentStarted
    | BatchStarted
    | KsiClassified
    | AgentFinished,
    Field(discriminator="kind"),
]
"""The discriminated union of all Studio events. Renderers match on `kind`."""
