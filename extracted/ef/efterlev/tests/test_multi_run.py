"""Tests for `efterlev.agents.multi_run.aggregate_gap_reports` (ConMon Lite v1).

Per DECISIONS 2026-05-11 "Tier 4 #2 design", the aggregator must:
- Reduce per-KSI to majority verdict via 2-of-3 voting (or higher N).
- Mark KSIs whose top vote count is below ceil(N/2) as "flickering".
- Tie-break to the most-conservative verdict from the tied set.
- Source rationale + evidence_ids from the FIRST run that voted majority,
  for determinism.
- Source claim_record_ids + unmapped_findings from the LAST run (most
  recently persisted to the provenance store).
- Handle the single-run path (N=1) trivially.
"""

from __future__ import annotations

import pytest

from efterlev.agents.gap import GapReport, KsiClassification, UnmappedFinding
from efterlev.agents.multi_run import _conservatism_rank, aggregate_gap_reports


def _clf(
    ksi_id: str,
    status: str,
    rationale: str = "default rationale",
    evidence_ids: list[str] | None = None,
) -> KsiClassification:
    """Build a synthetic KsiClassification. `implemented`/`partial` need
    at least one evidence_id per the model validator."""
    return KsiClassification(
        ksi_id=ksi_id,
        status=status,
        rationale=rationale,
        evidence_ids=evidence_ids
        or (["sha256:default"] if status in ("implemented", "partial") else []),
    )


def _report(
    *clfs: KsiClassification,
    claim_record_ids: list[str] | None = None,
    unmapped: list[UnmappedFinding] | None = None,
) -> GapReport:
    return GapReport(
        ksi_classifications=list(clfs),
        unmapped_findings=unmapped or [],
        claim_record_ids=claim_record_ids or [],
    )


# --- single-run path ----------------------------------------------------------


def test_single_run_returns_input_unchanged() -> None:
    """N=1: synthesized report matches the input; per_run_verdicts has
    one entry per KSI; no flickering."""
    inp = _report(
        _clf("KSI-CNA-RVP", "implemented"),
        _clf("KSI-MLA-LET", "partial"),
        claim_record_ids=["sha256:run0-claim0"],
    )
    out, per_run, flickering = aggregate_gap_reports([inp])
    # Sorted by ksi_id (the aggregator imposes deterministic order).
    assert [c.ksi_id for c in out.ksi_classifications] == ["KSI-CNA-RVP", "KSI-MLA-LET"]
    assert out.claim_record_ids == ["sha256:run0-claim0"]
    assert per_run == {
        "KSI-CNA-RVP": ["implemented"],
        "KSI-MLA-LET": ["partial"],
    }
    assert flickering == []


# --- 3-run majority paths -----------------------------------------------------


def test_three_run_unanimous_no_flickering() -> None:
    """3 runs, all returning the same verdict per KSI: stable verdict,
    no flickering, runs_aggregated path produces one consistent KSI."""
    r1 = _report(_clf("KSI-X", "implemented"))
    r2 = _report(_clf("KSI-X", "implemented"))
    r3 = _report(_clf("KSI-X", "implemented"))
    out, per_run, flickering = aggregate_gap_reports([r1, r2, r3])
    assert len(out.ksi_classifications) == 1
    assert out.ksi_classifications[0].status == "implemented"
    assert per_run["KSI-X"] == ["implemented", "implemented", "implemented"]
    assert flickering == []


def test_three_run_two_of_three_majority() -> None:
    """3 runs, two implemented + one partial: majority is implemented."""
    r1 = _report(_clf("KSI-X", "implemented", rationale="from run 0"))
    r2 = _report(_clf("KSI-X", "implemented", rationale="from run 1"))
    r3 = _report(_clf("KSI-X", "partial", rationale="from run 2"))
    out, per_run, flickering = aggregate_gap_reports([r1, r2, r3])
    assert out.ksi_classifications[0].status == "implemented"
    # Rationale comes from the FIRST run that voted majority (run 0).
    assert out.ksi_classifications[0].rationale == "from run 0"
    assert per_run["KSI-X"] == ["implemented", "implemented", "partial"]
    assert flickering == []


def test_three_run_one_one_one_split_is_flickering() -> None:
    """3 runs, three different verdicts (1-1-1 split): no majority,
    KSI is flickering, tie-break picks the most-conservative verdict."""
    r1 = _report(_clf("KSI-X", "implemented"))
    r2 = _report(_clf("KSI-X", "partial"))
    r3 = _report(_clf("KSI-X", "not_implemented"))
    out, per_run, flickering = aggregate_gap_reports([r1, r2, r3])
    # Tie-break: not_implemented is the most conservative of the three.
    assert out.ksi_classifications[0].status == "not_implemented"
    assert flickering == ["KSI-X"]
    assert per_run["KSI-X"] == ["implemented", "partial", "not_implemented"]


def test_three_run_two_way_tie_picks_more_conservative() -> None:
    """3 runs, one each of implemented + partial + not_applicable:
    1-1-1 again but the tie-break order is different. not_applicable
    is more conservative than implemented + partial in the precedence
    order, so wins."""
    r1 = _report(_clf("KSI-X", "implemented"))
    r2 = _report(_clf("KSI-X", "partial"))
    r3 = _report(_clf("KSI-X", "not_applicable"))
    out, _, flickering = aggregate_gap_reports([r1, r2, r3])
    # Per the precedence: implemented, partial, not_implemented,
    # not_applicable, evidence_layer_inapplicable. In a tie, the
    # rightmost wins -> not_applicable.
    assert out.ksi_classifications[0].status == "not_applicable"
    assert flickering == ["KSI-X"]


# --- multi-KSI mix ------------------------------------------------------------


def test_multi_ksi_mixed_outcomes() -> None:
    """Three runs across multiple KSIs with a mix of stable + flickering
    + tied. Every KSI gets the right majority + the right flickering
    classification."""
    r1 = _report(
        _clf("KSI-STABLE", "implemented"),
        _clf("KSI-FLICKER", "implemented"),
        _clf("KSI-MAJORITY", "partial"),
    )
    r2 = _report(
        _clf("KSI-STABLE", "implemented"),
        _clf("KSI-FLICKER", "partial"),
        _clf("KSI-MAJORITY", "partial"),
    )
    r3 = _report(
        _clf("KSI-STABLE", "implemented"),
        _clf("KSI-FLICKER", "not_implemented"),
        _clf("KSI-MAJORITY", "implemented"),
    )
    out, per_run, flickering = aggregate_gap_reports([r1, r2, r3])
    by_id = {c.ksi_id: c for c in out.ksi_classifications}
    assert by_id["KSI-STABLE"].status == "implemented"
    assert by_id["KSI-FLICKER"].status == "not_implemented"  # 1-1-1 -> conservative
    assert by_id["KSI-MAJORITY"].status == "partial"  # 2/3 wins
    assert flickering == ["KSI-FLICKER"]
    assert per_run["KSI-MAJORITY"] == ["partial", "partial", "implemented"]


# --- claim_record_ids + unmapped_findings come from the LAST run --------------


def test_claim_record_ids_come_from_last_run() -> None:
    r1 = _report(_clf("KSI-X", "implemented"), claim_record_ids=["sha256:run0"])
    r2 = _report(_clf("KSI-X", "implemented"), claim_record_ids=["sha256:run1"])
    r3 = _report(_clf("KSI-X", "implemented"), claim_record_ids=["sha256:run2"])
    out, _, _ = aggregate_gap_reports([r1, r2, r3])
    assert out.claim_record_ids == ["sha256:run2"]


def test_unmapped_findings_come_from_last_run() -> None:
    last_unmapped = UnmappedFinding(
        evidence_id="sha256:unmapped-from-run2", controls=["SC-99"], note="late"
    )
    r1 = _report(
        _clf("KSI-X", "implemented"),
        unmapped=[UnmappedFinding(evidence_id="sha256:run0", controls=["SC-1"], note="early")],
    )
    r2 = _report(_clf("KSI-X", "implemented"))
    r3 = _report(_clf("KSI-X", "implemented"), unmapped=[last_unmapped])
    out, _, _ = aggregate_gap_reports([r1, r2, r3])
    assert out.unmapped_findings == [last_unmapped]


# --- conservatism rank --------------------------------------------------------


def test_conservatism_rank_orders_correctly() -> None:
    assert _conservatism_rank("implemented") < _conservatism_rank("partial")
    assert _conservatism_rank("partial") < _conservatism_rank("not_implemented")
    assert _conservatism_rank("not_implemented") < _conservatism_rank("not_applicable")
    assert _conservatism_rank("not_applicable") < _conservatism_rank("evidence_layer_inapplicable")
    # Unknown statuses sort to max rank (defensive).
    assert _conservatism_rank("totally-unknown") == 5


# --- empty input is rejected --------------------------------------------------


def test_empty_reports_list_raises() -> None:
    with pytest.raises(ValueError, match="at least one report"):
        aggregate_gap_reports([])
