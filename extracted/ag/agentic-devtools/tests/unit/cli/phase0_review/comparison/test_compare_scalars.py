"""Tests for scalar content comparison."""

from agentic_devtools.cli.phase0_review.comparison import compare_content
from agentic_devtools.cli.phase0_review.helpers import StructuralResult


def test_compare_scalars_reports_matches_and_discrepancies():
    source = {
        "issue_id": "1",
        "title": "Expected",
        "type": "feature",
        "status": "open",
        "provider": "github",
        "labels": [],
        "body": "Body",
        "truncated": False,
    }
    frontmatter = {
        "id": "1",
        "title": "Wrong",
        "type": "feature",
        "status": "open",
        "provider": "github",
        "labels": [],
    }
    structure = StructuralResult(captures={"description": ["Body"]})
    findings = compare_content(source, frontmatter, structure)
    assert any('Field "title": expected "Expected", found "Wrong"' in item.text for item in findings)
    assert any(item.passed for item in findings)
