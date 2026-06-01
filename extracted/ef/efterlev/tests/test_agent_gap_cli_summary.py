"""Tests for `_format_gap_agent_summary` — `/agent gap` post-run output.

v0.1.152 / #357 collapsed the pre-v0.1.152 per-KSI dump (60 rows x 5+
lines each) into a status-count summary. Customer reported the verbose
form "no one will read in the terminal" 2026-05-17. `--verbose`
restores the full dump for debugging.
"""

from __future__ import annotations

from efterlev.agents.gap_types import GapReport, KsiClassification
from efterlev.cli.main import _format_gap_agent_summary


def _clf(ksi_id: str, status: str, evidence_ids: list[str] | None = None) -> KsiClassification:
    if status in ("implemented", "partial") and not evidence_ids:
        evidence_ids = ["sha256:" + "a" * 64]
    return KsiClassification(
        ksi_id=ksi_id,
        status=status,  # type: ignore[arg-type]
        rationale="rationale for " + ksi_id,
        evidence_ids=evidence_ids or [],
    )


def _report(classifications: list[KsiClassification]) -> GapReport:
    return GapReport(ksi_classifications=classifications, unmapped_findings=[])


def test_default_output_is_status_count_summary_not_per_ksi_dump() -> None:
    """Default (non-verbose) prints one line per status, NOT one per KSI."""
    report = _report(
        [
            _clf("KSI-CNA-01", "implemented"),
            _clf("KSI-CNA-02", "implemented"),
            _clf("KSI-CNA-03", "partial"),
            _clf("KSI-SVC-01", "not_implemented"),
            _clf("KSI-SVC-02", "not_applicable"),
        ]
    )
    lines = _format_gap_agent_summary(report, verbose=False)
    body = "\n".join(lines)

    # Header reports the total.
    assert "Gap Agent classified 5 KSI(s)" in body
    # Each status appears with its count.
    assert "implemented" in body and "  2" in body
    assert "partial" in body and "  1" in body
    assert "not_implemented" in body and "  1" in body
    # The per-KSI rationales are NOT printed by default.
    assert "rationale for KSI-CNA-01" not in body
    assert "KSI-CNA-01" not in body
    # And the user is told where to find them.
    assert "--verbose" in body and "HTML" in body


def test_verbose_restores_full_per_ksi_dump() -> None:
    report = _report(
        [
            _clf("KSI-CNA-01", "implemented"),
            _clf("KSI-SVC-02", "not_applicable"),
        ]
    )
    lines = _format_gap_agent_summary(report, verbose=True)
    body = "\n".join(lines)

    # Status counts still present.
    assert "Gap Agent classified 2 KSI(s)" in body
    # AND per-KSI ids + rationales.
    assert "KSI-CNA-01" in body
    assert "rationale for KSI-CNA-01" in body
    assert "KSI-SVC-02" in body
    assert "rationale for KSI-SVC-02" in body


def test_status_counts_ordered_actionable_first() -> None:
    """`partial` + `not_implemented` (the actionable ones) print before
    `not_applicable` so the human eye lands on them first."""
    report = _report(
        [
            _clf("KSI-1", "not_applicable"),
            _clf("KSI-2", "partial"),
            _clf("KSI-3", "implemented"),
            _clf("KSI-4", "not_implemented"),
        ]
    )
    lines = _format_gap_agent_summary(report, verbose=False)
    # Find the order in which each status label first appears.
    body = "\n".join(lines)
    order = {
        s: body.index(s) for s in ("implemented", "partial", "not_implemented", "not_applicable")
    }
    assert (
        order["implemented"] < order["partial"] < order["not_implemented"] < order["not_applicable"]
    )


def test_empty_report_does_not_crash() -> None:
    """No KSI classifications (e.g., empty baseline) → header + footer only,
    no exception from `max([])`."""
    lines = _format_gap_agent_summary(_report([]), verbose=False)
    body = "\n".join(lines)
    assert "Gap Agent classified 0 KSI(s)" in body
    assert "--verbose" in body
