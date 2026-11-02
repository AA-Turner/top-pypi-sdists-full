"""Tests for parse_changed_file_count."""

import pytest

from agentic_devtools.cli.ci.github_pr_files import parse_changed_file_count


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ({"changed_files": 0}, 0),
        ({"changed_files": 3}, 3),
        ({"changed_files": True}, None),
        ({"changed_files": -1}, None),
        ({"changed_files": "3"}, None),
        ({}, None),
    ],
)
def test_accepts_only_nonnegative_integer_counts(data: dict[str, object], expected: int | None) -> None:
    assert parse_changed_file_count(data) == expected
