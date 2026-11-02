"""Tests for parent spec path matching."""

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import find_parent_spec


@pytest.mark.parametrize(
    ("paths", "number", "expected"),
    [
        (["specs/1859-feature/spec.md"], 1859, ["specs/1859-feature/spec.md"]),
        (["specs/group/1859/spec.md"], 1859, ["specs/group/1859/spec.md"]),
        (["specs/group/1859-child/spec.md"], 1859, ["specs/group/1859-child/spec.md"]),
        (["specs/01859-feature/spec.md"], 1859, ["specs/01859-feature/spec.md"]),
        (["specs/01859-feature/spec.md"], "01859", ["specs/01859-feature/spec.md"]),
        (
            ["specs/001-task/tasks.md", "specs/0012-parent/spec.md"],
            12,
            ["specs/0012-parent/spec.md"],
        ),
        (["specs/11859-feature/spec.md", "specs/18590-feature/spec.md"], 1859, []),
        (
            ["specs/1859-a/spec.md", "specs/group/1859/spec.md"],
            1859,
            ["specs/1859-a/spec.md", "specs/group/1859/spec.md"],
        ),
        (["specs/01859-a/spec.md"], 0, []),
    ],
)
def test_find_parent_spec_matches_supported_layouts_and_padding(paths, number, expected) -> None:
    assert find_parent_spec(paths, number) == expected
