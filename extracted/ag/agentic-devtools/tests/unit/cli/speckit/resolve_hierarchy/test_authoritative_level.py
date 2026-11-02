"""Tests for authoritative SpecKit issue classification."""

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import authoritative_level


@pytest.mark.parametrize(
    ("labels", "issue_type", "expected"),
    [
        (["feature", "epic"], "Task", "epic"),
        (["feature"], "Task", "unknown"),
        (["task"], "Feature", "unknown"),
        (["TASK"], None, "task"),
        ([], "Feature", "feature"),
        ([], None, ""),
        ([None, {"name": "task"}], {"name": "feature"}, "unknown"),
    ],
)
def test_authoritative_level_preserves_label_and_issue_type_precedence(labels, issue_type, expected) -> None:
    assert authoritative_level(labels, issue_type) == expected
