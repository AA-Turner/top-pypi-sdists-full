"""Tests for collisions in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive, row


def test_agent_and_prompt_of_one_slug_is_not_a_collision() -> None:
    """One slug mapping to one target from two files is the intended merge."""
    rows = [
        row(path="a", slug="agdt.squash-commits", target="agdt-squash-commits"),
        row(path="b", slug="agdt.squash-commits", target="agdt-squash-commits", disposition="collapse"),
    ]
    assert derive.collisions(rows) == {}


def test_family_members_sharing_a_target_is_not_a_collision() -> None:
    """A merged workflow-step family collapses onto its family name by design."""
    rows = [
        row(path="a", slug="agdt.work-on-jira-issue.setup", target="agdt-work-on-jira-issue", disposition="merge"),
        row(path="b", slug="agdt.work-on-jira-issue.commit", target="agdt-work-on-jira-issue", disposition="merge"),
    ]
    assert derive.collisions(rows) == {}


def test_unrelated_slugs_sharing_a_target_is_a_collision() -> None:
    """Two different legacy names claiming one skill name is an error."""
    rows = [
        row(path="a", slug="agdt.one", target="agdt-shared"),
        row(path="b", slug="agdt.two", target="agdt-shared"),
    ]
    assert derive.collisions(rows) == {"agdt-shared": ["agdt.one", "agdt.two"]}


def test_deleted_rows_claim_no_target() -> None:
    """Delete rows carry '-' and cannot collide."""
    rows = [row(path=str(n), slug=f"agdt.{n}", disposition="delete", group="-", target="-") for n in range(2)]
    assert derive.collisions(rows) == {}
