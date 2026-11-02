"""Tests for joined-placeholder ambiguity."""

from agentic_devtools.cli.phase0_review.comparison import compare_content
from agentic_devtools.cli.phase0_review.helpers import StructuralResult


def test_delimiter_collision_blocks_named_and_property_arrays():
    source = {
        "dependencies": ["one, two"],
        "properties": {"custom": ["a, b"]},
        "truncated": False,
    }
    findings = compare_content(
        source,
        {},
        StructuralResult(captures={"dependencies": ["one, two"], "custom": ["a, b"]}),
    )
    assert all("Ambiguous source field" in item.text for item in findings)


def test_non_array_named_field_is_not_ambiguous():
    findings = compare_content(
        {"dependencies": "one", "truncated": False},
        {},
        StructuralResult(captures={"dependencies": ["one"]}),
    )
    assert findings[0].passed
