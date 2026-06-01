"""Shared pydantic models for the Gap Agent (extracted v0.1.143).

Pre-v0.1.143 these lived in `gap.py`. They got extracted so
`gap_batching.py` can import them without a circular dependency on
`gap.py` (which imports `gap_batching` for the per-batch planner).
Public API is unchanged: `gap.py` re-exports each name so existing
`from efterlev.agents.gap import GapReport` callers keep working.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

GapStatus = Literal[
    "implemented",
    "partial",
    "not_implemented",
    "not_applicable",
    # SPEC-57.1 (2026-04-25, 3PAO review §3): distinguishes "the scanner has
    # no path to evidence this KSI by design" (procedural-only, e.g.,
    # KSI-AFR-FSI / FedRAMP Security Inbox) from "not_implemented" (the CSP
    # genuinely doesn't implement this KSI). Critical for review credibility:
    # without this distinction, an infrastructure-only scan against any
    # baseline shows ~80% red because most KSIs are procedural — a coverage
    # statement masquerading as a compliance finding.
    "evidence_layer_inapplicable",
]


class KsiClassification(BaseModel):
    """One KSI's classification as returned by the Gap Agent.

    Structural invariant: `status="implemented"` and `status="partial"` MUST
    cite at least one evidence id. The fence-citation validator
    (`_validate_cited_ids` in gap.py) catches IDs the model fabricated
    against the prompt's nonced fences — but it never fires on zero
    citations (there's nothing to validate against). A model that returns
    `status="implemented"` with `evidence_ids=[]` is making an unfounded
    positive claim; reject it at the model layer so the agent's persistence
    path never sees it.

    `not_implemented`, `not_applicable`, and `evidence_layer_inapplicable`
    are exempt — those are honest declarations that the evidence is
    *missing* / *out of scope* / *unreachable from this input modality*,
    and the rationale is the cited record. Requiring evidence citations on
    those would force the model to fabricate them.
    """

    model_config = ConfigDict(frozen=True)

    ksi_id: str
    status: GapStatus
    rationale: str
    evidence_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _positive_status_requires_evidence(self) -> KsiClassification:
        if self.status in ("implemented", "partial") and not self.evidence_ids:
            raise ValueError(
                f"KSI {self.ksi_id}: status={self.status!r} requires at least one "
                f"evidence_id citation. A positive classification with no cited "
                f"evidence is an unfounded claim and is rejected at the model layer."
            )
        return self


class UnmappedFinding(BaseModel):
    """An evidence record whose `ksis_evidenced=[]` — no KSI attribution in FRMR."""

    model_config = ConfigDict(frozen=True)

    evidence_id: str
    controls: list[str]
    note: str


class GapReport(BaseModel):
    """Structured output of the Gap Agent — both persisted and returned to CLI.

    `claim_record_ids` is a parallel list to `ksi_classifications` holding the
    `ProvenanceRecord.record_id` each classification was persisted under — the
    id the user passes to `efterlev provenance show` to walk the chain. These
    are distinct from internal Claim content-hashes (which are the
    `Claim.claim_id`s); only the record_id walks the provenance graph.
    """

    model_config = ConfigDict(frozen=True)

    ksi_classifications: list[KsiClassification]
    unmapped_findings: list[UnmappedFinding]
    claim_record_ids: list[str] = Field(default_factory=list)
