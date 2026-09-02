"""Tests for merge_family in derive_customization_disposition."""

from __future__ import annotations

import pytest

from tests.scripts.derive_customization_disposition import derive


@pytest.mark.parametrize(
    ("slug", "expected"),
    [
        ("agdt.work-on-jira-issue.setup", "agdt.work-on-jira-issue"),
        ("agdt.pull-request-review.decision", "agdt.pull-request-review"),
    ],
)
def test_family_steps_are_recognised(slug: str, expected: str) -> None:
    """Every step of a merged family reports the family it merges into."""
    assert derive.merge_family(slug) == expected


@pytest.mark.parametrize("slug", ["agdt.run-setup", "agdt.work-on-jira-issue"])
def test_non_members_are_none(slug: str) -> None:
    """The family slug itself is not a step of the family."""
    assert derive.merge_family(slug) is None
