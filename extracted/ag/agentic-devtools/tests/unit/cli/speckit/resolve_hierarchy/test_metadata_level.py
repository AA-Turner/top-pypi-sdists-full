"""Tests for parsing hierarchy.yml levels."""

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import metadata_level


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("level: feature\n", "feature"),
        ('level: "Task" # inherited\n', "task"),
        ("level: 'epic'\n", "epic"),
        ("", "unknown"),
        ("level: task\nlevel: feature\n", "unknown"),
        ("level: other\n", "unknown"),
        ("level: # missing value\n", "unknown"),
        ("  level: task\n", "unknown"),
    ],
)
def test_metadata_level_parses_one_canonical_top_level_level(content, expected) -> None:
    assert metadata_level(content) == expected
