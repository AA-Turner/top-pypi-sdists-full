"""Tests for authoritative and metadata hierarchy precedence."""

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import combine_levels


@pytest.mark.parametrize(
    ("authoritative", "metadata", "expected"),
    [
        ("epic", "feature", "epic"),
        ("unknown", "task", "unknown"),
        ("task", "unknown", "unknown"),
        ("task", "feature", "unknown"),
        ("", "task", "task"),
        ("feature", None, "feature"),
        ("", None, "unknown"),
    ],
)
def test_combine_levels_preserves_existing_precedence(authoritative, metadata, expected) -> None:
    assert combine_levels(authoritative, metadata) == expected
