"""Multi-run aggregator for the Gap Agent (ConMon Lite v1).

Per DECISIONS 2026-05-11 "Tier 4 #2 design: ConMon Lite v1
(Gap-Agent KSI-verdict diffs with 2-of-3 voting)", this module
implements the verdict-stability mechanism: run the Gap Agent N
times, take per-KSI majority vote, mark non-majority splits as
"flickering" KSIs.

The aggregator is a pure function over a list of `GapReport`s.
It returns a synthesized `GapReport` with:
- per-KSI classifications using the majority verdict (with the
  rationale + evidence_ids from the FIRST run that voted that way,
  for determinism)
- claim_record_ids from the LAST run (most-recently persisted to
  the provenance store)
- unmapped_findings from the LAST run

Plus two side outputs:
- `per_run_verdicts`: dict[ksi_id, list[verdict]] across runs
- `flickering_ksis`: KSIs whose top vote count is < ceil(N/2)

Tie-break: when no single verdict has the majority (1-1-1 on N=3),
the verdict picks the most-conservative status from the tied set,
following the precedence order in `_GAP_STATUS_PRECEDENCE`. This
matches the DECISIONS Decision #2 hint "ties tolerated as the
lower-confidence verdict."
"""

from __future__ import annotations

import math
from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from efterlev.agents.gap import GapReport

# Precedence: leftmost is most-positive, rightmost is most-conservative.
# Used as the tie-break direction: when verdict votes tie, the verdict
# that appears LATER in this tuple wins (the more cautious answer).
_GAP_STATUS_PRECEDENCE: tuple[str, ...] = (
    "implemented",
    "partial",
    "not_implemented",
    "not_applicable",
    "evidence_layer_inapplicable",
)


def _conservatism_rank(status: str) -> int:
    """Rank a GapStatus by conservatism. Higher == more cautious.
    Unknown statuses get max rank (treated as conservative for safety)."""
    if status in _GAP_STATUS_PRECEDENCE:
        return _GAP_STATUS_PRECEDENCE.index(status)
    return len(_GAP_STATUS_PRECEDENCE)


def _majority_verdict(verdicts: list[str]) -> tuple[str, bool]:
    """Return (verdict, is_majority) for a list of N verdict strings.

    The verdict is the most-common entry. `is_majority` is True iff
    that entry has count >= ceil(N/2) (i.e., a real majority on N
    runs). For N=3, ceil(3/2)=2, so 2-of-3 wins. For N=1, ceil(1/2)=1,
    so trivially majority.

    Tie-break (when multiple verdicts tie at the top vote count):
    pick the one with the highest conservatism rank from the tied
    set. This matches DECISIONS Decision #2's "ties tolerated as the
    lower-confidence verdict" guidance.
    """
    if not verdicts:
        # Defensive: shouldn't happen in practice; the caller filters
        # empty per-KSI lists out.
        raise ValueError("majority of empty list is undefined")
    counts = Counter(verdicts)
    top_count = counts.most_common(1)[0][1]
    tied_at_top = [v for v, c in counts.items() if c == top_count]
    # Tie-break: pick the most-conservative from the tied set.
    chosen = max(tied_at_top, key=_conservatism_rank)
    threshold = math.ceil(len(verdicts) / 2)
    is_majority = top_count >= threshold and len(tied_at_top) == 1
    return chosen, is_majority


def aggregate_gap_reports(
    reports: list[GapReport],
) -> tuple[GapReport, dict[str, list[str]], list[str]]:
    """Aggregate N Gap Agent runs into a single majority-voted report.

    Returns (synthesized_report, per_run_verdicts, flickering_ksis):
    - synthesized_report: GapReport whose classifications use the
      majority verdict per KSI, with rationale + evidence_ids taken
      from the FIRST run that voted for the majority verdict (for
      determinism). claim_record_ids and unmapped_findings come
      from the LAST run.
    - per_run_verdicts: {ksi_id: [run0_verdict, run1_verdict, ...]}.
    - flickering_ksis: KSIs whose top vote count is below the
      majority threshold (ceil(N/2)).

    Single-run path (N=1) is supported: the synthesized report
    matches the input; per_run_verdicts has one entry per KSI;
    no flickering.
    """
    from efterlev.agents.gap import GapReport, KsiClassification

    if not reports:
        raise ValueError("aggregate_gap_reports requires at least one report")

    # Collect per-KSI verdicts across runs in run order.
    per_run_verdicts: dict[str, list[str]] = {}
    # Track the first KsiClassification for each (ksi_id, status) pair
    # so we can preserve rationale + evidence_ids from the earliest
    # matching run.
    first_seen: dict[tuple[str, str], KsiClassification] = {}
    for report in reports:
        for clf in report.ksi_classifications:
            per_run_verdicts.setdefault(clf.ksi_id, []).append(clf.status)
            key = (clf.ksi_id, clf.status)
            first_seen.setdefault(key, clf)

    # Reduce per-KSI to majority verdict + flickering flag.
    synthesized_classifications: list[KsiClassification] = []
    flickering: list[str] = []
    for ksi_id, verdicts in per_run_verdicts.items():
        majority, is_majority = _majority_verdict(verdicts)
        if not is_majority:
            flickering.append(ksi_id)
        # Source the rationale + evidence_ids from the first run that
        # voted for the majority verdict.
        chosen = first_seen[(ksi_id, majority)]
        synthesized_classifications.append(chosen)

    # Stable order by ksi_id so the synthesized report is reproducible
    # across run orderings (the input list order otherwise affects iteration).
    synthesized_classifications.sort(key=lambda c: c.ksi_id)
    flickering.sort()

    # claim_record_ids + unmapped_findings come from the LAST run --
    # those are the most-recently-persisted records in the provenance
    # store, which is what downstream `efterlev provenance show` walks
    # would resolve.
    last = reports[-1]
    synthesized = GapReport(
        ksi_classifications=synthesized_classifications,
        unmapped_findings=last.unmapped_findings,
        claim_record_ids=last.claim_record_ids,
    )
    return synthesized, per_run_verdicts, flickering
