"""Tests for normative verdict templates."""

from agentic_devtools.cli.phase0_review.report import Finding, render_report


def test_approved_and_changes_requested_templates_are_exact():
    approved = render_report(
        [
            Finding("template", "Structure matches", True),
            Finding("content", "Content matches", True),
        ]
    )
    assert (
        approved
        == """## Template Compliance
- [x] Structure matches

## Content Fidelity
- [x] Content matches

## Verdict
APPROVED
confidence: 100%"""
    )
    changed = render_report([Finding("template", "failure")])
    assert changed.endswith("## Verdict\nCHANGES REQUESTED")
    assert "confidence:" not in changed


def test_timeout_and_empty_content_use_literal_items():
    report = render_report([], timed_out=True)
    assert "- [ ] Operational timeout: review exceeded the 120-second ceiling" in report
    assert "- [x] No content-fidelity checks performed" in report

    content_only = render_report([Finding("content", "Content matches", passed=True)])
    assert "- [x] No structural findings" in content_only
