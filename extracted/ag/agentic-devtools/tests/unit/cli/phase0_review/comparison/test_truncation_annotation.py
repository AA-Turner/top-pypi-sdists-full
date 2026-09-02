"""Tests for truncation annotation fidelity."""

from agentic_devtools.cli.phase0_review.comparison import compare_content
from agentic_devtools.cli.phase0_review.helpers import StructuralResult


def test_truncated_body_requires_exact_annotation():
    source = {"body": "abc", "truncated": True, "original_size": 102401}
    exact = "abc\n[CONTENT_TRUNCATED: original_size=102401 bytes, included=3 bytes]"
    assert compare_content(source, {}, StructuralResult(captures={"description": [exact]}))[0].passed
    assert not compare_content(
        source,
        {},
        StructuralResult(captures={"description": ["abc"]}),
    )[0].passed


def test_truncated_body_without_original_size_does_not_crash():
    """A malformed truncated payload missing original_size must not raise KeyError.

    validate_schema already records the malformed-input finding; comparison must
    skip the annotation rather than crash so the run still returns a report.
    """
    source = {"body": "abc", "truncated": True}
    findings = compare_content(source, {}, StructuralResult(captures={"description": ["abc"]}))
    assert findings[0].passed
