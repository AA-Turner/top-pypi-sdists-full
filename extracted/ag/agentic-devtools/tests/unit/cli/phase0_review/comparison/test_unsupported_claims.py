"""Tests for unsupported optional source claims."""

from agentic_devtools.cli.phase0_review.comparison import compare_content
from agentic_devtools.cli.phase0_review.helpers import StructuralResult


def test_absent_optional_field_claim_is_discrepancy():
    findings = compare_content(
        {"truncated": False},
        {},
        StructuralResult(captures={"priority": ["invented"]}),
    )
    assert 'expected "", found "invented"' in findings[0].text


def test_renderer_owned_metadata_is_excluded():
    findings = compare_content(
        {"truncated": False},
        {},
        StructuralResult(captures={"content_hash": ["generated"]}),
    )
    assert findings == []
