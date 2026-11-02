"""Tests for report.parse_serialized_finding."""

from agentic_devtools.cli.phase0_review.report import parse_serialized_finding


def test_parse_serialized_finding_accepts_checklist_lines() -> None:
    assert parse_serialized_finding("- [ ] mismatch") == (False, "mismatch")
    assert parse_serialized_finding("- [x]  aligned") == (True, "aligned")


def test_parse_serialized_finding_rejects_non_finding_lines() -> None:
    assert parse_serialized_finding("## Verdict") is None
