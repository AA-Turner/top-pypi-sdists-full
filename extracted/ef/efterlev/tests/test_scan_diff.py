"""Tests for `efterlev.reports.scan_diff` (ConMon Lite v0).

Per DECISIONS 2026-05-11 "Tier 4 #1 design", this module locks the
per-detector gap-emission diff abstraction. The tests cover the four
diff outcomes the prompt called out: new_gap, resolved_gap,
modified_gap, unchanged (excluded), plus the multi-detector mix.
"""

from __future__ import annotations

from datetime import UTC, datetime

from efterlev.reports.scan_diff import (
    ScanDiff,
    compute_scan_diff,
    render_scan_diff_html,
    render_scan_diff_markdown,
)


def _ev(
    *,
    detector_id: str,
    resource_name: str,
    gap: str | None = None,
    detail: str | None = None,
    extra: dict | None = None,
    file: str = "infra/main.tf",
    line_start: int = 10,
    line_end: int = 20,
) -> dict:
    """Build a synthetic evidence record matching the scan-sidecar shape."""
    content: dict = {"resource_name": resource_name, "rule_state": "rules_present"}
    if gap is not None:
        content["gap"] = gap
        content["rule_state"] = "rules_absent"
    if detail is not None:
        content["detail"] = detail
    if extra:
        content.update(extra)
    return {
        "evidence_id": f"sha256:{detector_id}-{resource_name}",
        "detector_id": detector_id,
        "ksis_evidenced": ["KSI-CNA-RVP"],
        "controls_evidenced": ["SI-3"],
        "source_ref": {"file": file, "line_start": line_start, "line_end": line_end},
        "content": content,
    }


def _sidecar(*evidence: dict) -> dict:
    """Build a minimal scan-sidecar dict from the given evidence records."""
    return {
        "schema_version": 1,
        "generated_at": "2026-05-11T01:30:00+00:00",
        "scan_root": "/path/to/repo",
        "scan_mode": "hcl",
        "summary": {"detectors_run": 1, "evidence_count": len(evidence), "manifests_loaded": 0},
        "evidence": list(evidence),
    }


# --- gap-state classification + diff outcomes --------------------------------


def test_new_gap_when_resource_becomes_a_gap_in_current() -> None:
    """A (detector, resource) pair that was non-gap in prior and is
    a gap in current: surfaces as new_gap."""
    prior = _sidecar(_ev(detector_id="aws.waf_rule_count", resource_name="api_protection"))
    current = _sidecar(
        _ev(
            detector_id="aws.waf_rule_count",
            resource_name="api_protection",
            gap="zero rule blocks",
        )
    )
    diff = compute_scan_diff(prior, current)
    assert len(diff.new_gaps) == 1
    assert len(diff.modified_gaps) == 0
    assert len(diff.resolved_gaps) == 0
    e = diff.new_gaps[0]
    assert e.detector_id == "aws.waf_rule_count"
    assert e.resource_name == "api_protection"
    assert e.outcome == "new_gap"
    assert e.gap_text == "zero rule blocks"
    assert e.source_ref == "infra/main.tf:10-20"


def test_resolved_gap_when_resource_becomes_non_gap_in_current() -> None:
    """A (detector, resource) pair that was a gap in prior and is
    non-gap in current: surfaces as resolved_gap."""
    prior = _sidecar(
        _ev(
            detector_id="aws.waf_rule_count",
            resource_name="api_protection",
            gap="zero rule blocks",
        )
    )
    current = _sidecar(_ev(detector_id="aws.waf_rule_count", resource_name="api_protection"))
    diff = compute_scan_diff(prior, current)
    assert len(diff.new_gaps) == 0
    assert len(diff.modified_gaps) == 0
    assert len(diff.resolved_gaps) == 1
    assert diff.resolved_gaps[0].outcome == "resolved_gap"
    assert diff.resolved_gaps[0].gap_text == "zero rule blocks"


def test_modified_gap_when_content_differs_but_still_a_gap() -> None:
    """A (detector, resource) pair that's a gap in both, with
    different content: surfaces as modified_gap with a summary."""
    prior = _sidecar(
        _ev(
            detector_id="aws.waf_rule_count",
            resource_name="api_protection",
            gap="zero rule blocks",
            extra={"rule_count": 0},
        )
    )
    current = _sidecar(
        _ev(
            detector_id="aws.waf_rule_count",
            resource_name="api_protection",
            gap="rule blocks reduced",
            extra={"rule_count": 1},
        )
    )
    diff = compute_scan_diff(prior, current)
    assert len(diff.modified_gaps) == 1
    e = diff.modified_gaps[0]
    assert e.outcome == "modified_gap"
    assert "rule_count" in (e.modification_summary or "")


def test_unchanged_gap_excluded_from_output() -> None:
    """A (detector, resource) pair that's the same gap in both: not
    in any output list per Decision #3 (regression focus)."""
    same = _ev(
        detector_id="aws.waf_rule_count",
        resource_name="api_protection",
        gap="zero rule blocks",
    )
    prior = _sidecar(same)
    current = _sidecar(same)
    diff = compute_scan_diff(prior, current)
    assert diff.new_gaps == []
    assert diff.modified_gaps == []
    assert diff.resolved_gaps == []


def test_unchanged_non_gap_excluded_from_output() -> None:
    """A (detector, resource) pair that's non-gap in both: also
    excluded (no signal for the regression view)."""
    same = _ev(detector_id="aws.waf_rule_count", resource_name="api_protection")
    prior = _sidecar(same)
    current = _sidecar(same)
    diff = compute_scan_diff(prior, current)
    assert diff.new_gaps == []
    assert diff.modified_gaps == []
    assert diff.resolved_gaps == []


def test_resource_added_with_gap_surfaces_as_new_gap() -> None:
    """A (detector, resource) pair that doesn't exist in prior and
    appears as a gap in current: surfaces as new_gap (the absent-
    in-prior case is treated as non-gap-in-prior)."""
    prior = _sidecar()  # empty
    current = _sidecar(
        _ev(detector_id="aws.security_group_open_ingress", resource_name="web", gap="0.0.0.0/0")
    )
    diff = compute_scan_diff(prior, current)
    assert len(diff.new_gaps) == 1
    assert diff.new_gaps[0].resource_name == "web"


def test_resource_removed_with_gap_surfaces_as_resolved_gap() -> None:
    """A (detector, resource) pair that was a gap in prior and is
    absent from current: surfaces as resolved_gap."""
    prior = _sidecar(
        _ev(detector_id="aws.security_group_open_ingress", resource_name="web", gap="0.0.0.0/0")
    )
    current = _sidecar()  # the resource was removed
    diff = compute_scan_diff(prior, current)
    assert len(diff.resolved_gaps) == 1


def test_multi_detector_mix() -> None:
    """End-to-end: multiple detectors, multiple resources, mix of
    new + modified + resolved + unchanged."""
    prior = _sidecar(
        _ev(detector_id="aws.waf_rule_count", resource_name="acl_a"),  # non-gap, stays
        _ev(
            detector_id="aws.waf_rule_count", resource_name="acl_b", gap="zero rules"
        ),  # gap, gets resolved
        _ev(detector_id="aws.waf_rate_limiting", resource_name="acl_a"),  # non-gap, becomes gap
        _ev(
            detector_id="aws.waf_geo_blocking",
            resource_name="acl_a",
            gap="no geo block",
            extra={"country_code_count": 0},
        ),  # gap, gets modified
    )
    current = _sidecar(
        _ev(detector_id="aws.waf_rule_count", resource_name="acl_a"),  # unchanged non-gap
        _ev(detector_id="aws.waf_rule_count", resource_name="acl_b"),  # resolved
        _ev(
            detector_id="aws.waf_rate_limiting", resource_name="acl_a", gap="no rate limit"
        ),  # new gap
        _ev(
            detector_id="aws.waf_geo_blocking",
            resource_name="acl_a",
            gap="no geo block",
            extra={"country_code_count": 0, "additional_field": "x"},
        ),  # modified gap (extra field added)
    )
    diff = compute_scan_diff(prior, current)
    assert len(diff.new_gaps) == 1
    assert diff.new_gaps[0].detector_id == "aws.waf_rate_limiting"
    assert len(diff.resolved_gaps) == 1
    assert diff.resolved_gaps[0].detector_id == "aws.waf_rule_count"
    assert len(diff.modified_gaps) == 1
    assert diff.modified_gaps[0].detector_id == "aws.waf_geo_blocking"


# --- markdown rendering -------------------------------------------------------


def test_markdown_empty_diff_says_no_changes() -> None:
    """An empty diff renders the 'No detector-level gap changes' message."""
    md = render_scan_diff_markdown(ScanDiff())
    assert "No detector-level gap changes" in md
    assert "<!-- efterlev-conmon-lite -->" in md  # marker for sticky-comment edit-in-place


def test_markdown_with_new_gap_renders_table_and_marker() -> None:
    """A new-gap diff renders the markdown table + the sticky-comment marker."""
    prior = _sidecar()
    current = _sidecar(
        _ev(
            detector_id="aws.waf_rule_count",
            resource_name="api_protection",
            gap="zero rule blocks",
        )
    )
    diff = compute_scan_diff(prior, current)
    md = render_scan_diff_markdown(diff, base_branch="main")
    assert "**1 new gaps**" in md
    assert "vs `main`" in md
    assert "aws.waf_rule_count" in md
    assert "api_protection" in md
    assert "infra/main.tf:10-20" in md
    assert "<!-- efterlev-conmon-lite -->" in md


def test_markdown_resolved_only_does_not_render_table() -> None:
    """A diff with only resolved gaps renders the 'no regressions' note."""
    prior = _sidecar(
        _ev(
            detector_id="aws.waf_rule_count",
            resource_name="api_protection",
            gap="zero rules",
        )
    )
    current = _sidecar(_ev(detector_id="aws.waf_rule_count", resource_name="api_protection"))
    diff = compute_scan_diff(prior, current)
    md = render_scan_diff_markdown(diff)
    assert "no regressions to flag" in md
    assert "0 new gaps" in md
    assert "1 resolved" in md


def test_markdown_truncates_at_max_rows() -> None:
    """A diff with more new+modified gaps than max_rows renders a
    'showing X of Y' truncation note."""
    prior = _sidecar()
    evs = [_ev(detector_id=f"d{i}", resource_name=f"r{i}", gap=f"gap-{i}") for i in range(25)]
    current = _sidecar(*evs)
    diff = compute_scan_diff(prior, current)
    md = render_scan_diff_markdown(diff, max_rows=5)
    assert "showing 5 of 25" in md


# --- HTML rendering -----------------------------------------------------------


def test_html_includes_three_section_headers() -> None:
    """HTML report has dedicated sections for new / modified / resolved."""
    prior = _sidecar(
        _ev(detector_id="aws.x", resource_name="r1", gap="prior gap"),
    )
    current = _sidecar(
        _ev(detector_id="aws.y", resource_name="r2", gap="new gap"),
    )
    diff = compute_scan_diff(prior, current)
    html = render_scan_diff_html(diff, generated_at=datetime(2026, 5, 11, 1, 30, 0, tzinfo=UTC))
    assert "New gaps (1)" in html
    assert "Modified gaps (0)" in html
    assert "Resolved gaps (1)" in html
    # Includes both detector names.
    assert "aws.x" in html
    assert "aws.y" in html
