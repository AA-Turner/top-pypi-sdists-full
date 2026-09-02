"""Tests for ordered and unordered multi-value comparison."""

from agentic_devtools.cli.phase0_review.comparison import compare_content
from agentic_devtools.cli.phase0_review.helpers import StructuralResult


def test_multisets_ignore_order_but_ordered_constraints_do_not():
    source = {
        "labels": ["a", "b"],
        "dependencies": ["one", "two"],
        "constraints": ["first", "second"],
        "truncated": False,
    }
    frontmatter = {"labels": ["b", "a"]}
    structure = StructuralResult(
        captures={
            "dependencies": ["two, one"],
            "constraints": ["second, first"],
        }
    )
    findings = compare_content(source, frontmatter, structure)
    assert findings[0].passed
    assert findings[1].passed
    assert not findings[2].passed


def test_multiset_multiplicity_is_preserved():
    source = {"labels": ["a", "a"], "truncated": False}
    findings = compare_content(source, {"labels": ["a"]}, StructuralResult())
    assert not findings[0].passed


def test_constraint_normalization_preserves_internal_whitespace():
    source = {"constraints": [" first \nline  \nlast "], "truncated": False}
    matching = StructuralResult(captures={"constraints": ["first \nline  \nlast"]})
    changed = StructuralResult(captures={"constraints": ["first \nline\nlast"]})
    assert compare_content(source, {}, matching)[0].passed
    assert not compare_content(source, {}, changed)[0].passed
