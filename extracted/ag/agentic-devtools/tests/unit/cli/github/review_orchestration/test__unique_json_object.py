import pytest

from agentic_devtools.cli.github.review_orchestration import _unique_json_object


def test_preserves_distinct_fields():
    assert _unique_json_object([("cycles", 1), ("tasks", [])]) == {"cycles": 1, "tasks": []}


def test_duplicate_fields_fail_instead_of_overwriting():
    with pytest.raises(ValueError, match="duplicate JSON field"):
        _unique_json_object([("cycles", 12), ("cycles", 0)])
