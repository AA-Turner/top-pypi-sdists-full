"""Tests for the parent repository name validation helper."""

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import _parent_name_with_owner


@pytest.mark.parametrize(
    ("parent", "expected"),
    [
        (None, ""),
        ("invalid", ""),
        ({"number": 0, "repository": {"nameWithOwner": "owner/repo"}}, ""),
        ({"number": "10", "repository": {"nameWithOwner": "owner/repo"}}, ""),
        ({"repository": {"nameWithOwner": "owner/repo"}}, ""),
        ({"number": 10}, ""),
        ({"number": 10, "repository": "invalid"}, ""),
        ({"number": 10, "repository": {"nameWithOwner": ""}}, ""),
        ({"number": 10, "repository": {"nameWithOwner": 7}}, ""),
        ({"number": 10, "repository": {"nameWithOwner": "owner/repo"}}, "owner/repo"),
    ],
)
def test_parent_name_with_owner_validates_full_shape(parent, expected) -> None:
    assert _parent_name_with_owner(parent) == expected
