"""Tests for route-sensitive table-cell encoding."""

from agentic_devtools.cli.phase0_review.comparison import compare_content
from agentic_devtools.cli.phase0_review.helpers import StructuralResult


def test_table_encoding_applies_only_to_table_routed_fields():
    source = {"properties": {"value": "a\\b|c\nd"}, "truncated": False}
    table = StructuralResult(captures={"value": ["a\\\\b\\|c<br>d"]}, table_fields={"value"})
    plain = StructuralResult(captures={"value": ["a\\b|c\nd"]})
    assert compare_content(source, {}, table)[0].passed
    assert compare_content(source, {}, plain)[0].passed
