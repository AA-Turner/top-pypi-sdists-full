"""Per-batch planning for the Gap Agent (v0.1.143).

Pre-v0.1.143 the Gap Agent issued a single LLM call carrying ALL N
indicators plus ALL M evidence records. On workspaces with hundreds
of evidence records this overflowed Bedrock's 200k-token context
window (customer report 2026-05-16: 660 evidence records ->
207k-token prompt, hard failure).

v0.1.143 splits the work into K batches of `batch_size_ksis`
indicators each. Each batch carries ONLY the evidence whose
`ksis_evidenced` overlaps with the batch's KSI ids. Evidence with
`ksis_evidenced=[]` (unmapped) is handled deterministically by
`compute_unmapped_findings` after all batches complete -- no LLM
call needed, no token cost, no hallucinated notes.

Correctness invariants:

- Every evidence record's `ksis_evidenced` is computed by the scanner
  from FRMR's KSI->control mapping. If KSI-X is in batch 3, every
  evidence record attributed to KSI-X is in batch 3's prompt. The
  filter is a strict superset of what the scanner attributed.

- An evidence record attributed to multiple KSIs (multi-KSI evidence)
  appears in every batch containing any of those KSIs. Duplication is
  bounded because typical evidence maps to 1-3 KSIs; token cost
  increase is negligible.

- Per-batch retry / graceful-repair semantics (v0.1.125 / v0.1.139 /
  v0.1.140) work batch-locally: a failed batch retries up to 3 times
  with feedback, then auto-repairs; other batches are untouched.

- `fill_missing_classifications` is a safety net for the case where
  the LLM omits one of the batch's KSIs entirely. Pre-batching this
  was invisible (60-KSI report missing 1 KSI got lost in the noise);
  per-batch the discrepancy is obvious. Missing KSIs get a
  `not_implemented` placeholder with an auto-repair marker.
"""

from __future__ import annotations

from dataclasses import dataclass

from efterlev.agents.gap_types import GapReport, KsiClassification, UnmappedFinding
from efterlev.models import Evidence, Indicator

# Default chosen to keep typical per-batch prompts well under 50k tokens
# (each KSI's evidence is typically 5-30 records of ~500 chars each, so
# a batch of 5 KSIs * 30 records * 500 chars = 75k chars ~= 19k tokens).
# Configurable per call site if needed.
DEFAULT_BATCH_SIZE_KSIS = 5


@dataclass(frozen=True)
class Batch:
    """One LLM call's worth of work: K indicators + their relevant evidence.

    `index` is 1-based for the progress reporter's "Batch 3/12" display.
    `total` is the total batch count (same value across every batch in
    the same plan so the reporter doesn't need a separate setter).
    """

    indicators: list[Indicator]
    evidence: list[Evidence]
    index: int
    total: int


def plan_batches(
    indicators: list[Indicator],
    evidence: list[Evidence],
    *,
    batch_size_ksis: int = DEFAULT_BATCH_SIZE_KSIS,
) -> list[Batch]:
    """Group indicators into batches and filter evidence per batch.

    Each batch carries only evidence whose `ksis_evidenced` overlaps
    with the batch's KSI ids. Unmapped evidence (`ksis_evidenced=[]`)
    is NOT included -- handled deterministically by
    `compute_unmapped_findings` after all batches complete.

    Empty `indicators` returns an empty plan. Negative or zero
    `batch_size_ksis` is treated as the default; we never want to
    silently produce zero-size batches.
    """
    if not indicators:
        return []
    if batch_size_ksis <= 0:
        batch_size_ksis = DEFAULT_BATCH_SIZE_KSIS

    chunks: list[list[Indicator]] = [
        indicators[i : i + batch_size_ksis] for i in range(0, len(indicators), batch_size_ksis)
    ]
    total = len(chunks)
    batches: list[Batch] = []
    for idx, chunk in enumerate(chunks, start=1):
        chunk_ksi_ids = {ind.id for ind in chunk}
        chunk_evidence = [
            ev for ev in evidence if ev.ksis_evidenced and (set(ev.ksis_evidenced) & chunk_ksi_ids)
        ]
        batches.append(Batch(indicators=chunk, evidence=chunk_evidence, index=idx, total=total))
    return batches


def compute_unmapped_findings(evidence: list[Evidence]) -> list[UnmappedFinding]:
    """Build UnmappedFindings deterministically from evidence with no KSI attribution.

    Replaces the LLM-generated `unmapped_findings` output for two reasons:

    1. Cost: the LLM was emitting these in the same call as classifications,
       inflating output tokens. With batching, including unmapped evidence
       in every batch's prompt would duplicate token cost for no value.

    2. Accuracy: the LLM's `note` for unmapped findings was rarely insightful
       -- usually a paraphrase of "evidence with no KSI in baseline." A
       deterministic template is more accurate AND cheaper.

    The note explains the structural reason: the scanner emitted this
    evidence for controls X/Y, but FRMR has no KSI attributing those
    controls in the loaded baseline. Useful for manual review of
    detector->KSI mapping gaps.
    """
    unmapped: list[UnmappedFinding] = []
    for ev in evidence:
        if ev.ksis_evidenced:
            continue
        ctrl_list = list(ev.controls_evidenced)
        ctrl_str = ", ".join(ctrl_list) if ctrl_list else "(none)"
        note = (
            f"Detector {ev.detector_id} produced evidence for controls "
            f"[{ctrl_str}], but those controls are not mapped to any KSI "
            "in the loaded baseline. The evidence is preserved for "
            "transparency; manual review can determine if a KSI mapping "
            "should be added."
        )
        unmapped.append(
            UnmappedFinding(
                evidence_id=ev.evidence_id,
                controls=ctrl_list,
                note=note,
            )
        )
    return unmapped


def fill_missing_classifications(
    report: GapReport, batch_indicators: list[Indicator]
) -> tuple[GapReport, list[str]]:
    """Safety net: drop unknown-KSI classifications + add placeholders for omissions.

    Two corrective behaviors:

    1. **Drop unknown KSI IDs** (v0.1.146 / #351). The LLM sometimes
       emits a malformed KSI id (e.g. `KSI-SUS` instead of `KSI-IAM-SUS`)
       and ALSO omits the real one. Pre-v0.1.146 both leaked downstream
       and the wrong id surfaced in the gap report + got skipped by
       OSCAL emitters with confusing `skipped (unknown KSI in indicator
       dict)` warnings. Now we drop anything not in `batch_indicators`
       at the source.

    2. **Add placeholders for omitted batch indicators** (v0.1.143
       original behavior). Pre-batching, an omission of 1 of 60 KSIs
       went unnoticed; per-batch it's obvious (1 of 5). Missing KSIs
       get a `not_implemented` placeholder with an auto-repair marker.

    Returns the patched report plus a list of human-readable notes
    (one per dropped + one per placeholder) suitable for the stderr
    summary.
    """
    expected_ids = {ind.id for ind in batch_indicators}
    notes: list[str] = []

    # Drop classifications with unknown KSI ids — keep only those whose
    # ksi_id matches a batch indicator. Preserves original order for
    # downstream stability.
    kept: list[KsiClassification] = []
    for clf in report.ksi_classifications:
        if clf.ksi_id in expected_ids:
            kept.append(clf)
        else:
            notes.append(
                f"{clf.ksi_id}: dropped (not a valid KSI in this batch; "
                "model likely emitted a malformed or out-of-baseline id)"
            )

    seen_ids = {clf.ksi_id for clf in kept}
    missing = [ksi_id for ksi_id in (ind.id for ind in batch_indicators) if ksi_id not in seen_ids]

    placeholders: list[KsiClassification] = []
    for ksi_id in missing:
        placeholders.append(
            KsiClassification(
                ksi_id=ksi_id,
                status="not_implemented",
                rationale=(
                    "[auto-repair: model omitted this KSI from the batch response; "
                    "defaulting to not_implemented]"
                ),
                evidence_ids=[],
            )
        )
        notes.append(f"{ksi_id}: model omitted; filled with 'not_implemented' placeholder")

    if not notes:
        return report, []

    patched = GapReport(
        ksi_classifications=kept + placeholders,
        unmapped_findings=list(report.unmapped_findings),
        claim_record_ids=list(report.claim_record_ids),
    )
    return patched, notes
