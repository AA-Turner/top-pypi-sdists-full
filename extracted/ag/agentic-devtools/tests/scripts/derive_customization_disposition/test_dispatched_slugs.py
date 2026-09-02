"""Tests for dispatched_slugs in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive, unit


def test_handoff_target_is_dispatched() -> None:
    """A `handoffs:` entry naming another unit dispatches it."""
    parent = unit(
        slug="agdt.pull-request-review.initiate",
        frontmatter='\nhandoffs:\n  - agent: "agdt.pull-request-review.orchestrator"\n',
        body="Hand off.\n",
    )
    child = unit(slug="agdt.pull-request-review.orchestrator", body="Coordinate.\n")
    assert derive.dispatched_slugs([parent, child]) == frozenset({"agdt.pull-request-review.orchestrator"})


def test_body_declaration_is_dispatched() -> None:
    """A unit that says a parent spawned it is dispatched."""
    child = unit(slug="agdt.pr-merge-execute", body="You are a narrowly-scoped agent.\n")
    assert derive.dispatched_slugs([child]) == frozenset({"agdt.pr-merge-execute"})


def test_unknown_handoff_target_is_ignored() -> None:
    """A handoff naming a unit that does not exist dispatches nothing."""
    parent = unit(slug="agdt.a", frontmatter='\nhandoffs:\n  - agent: "agdt.gone"\n', body="x\n")
    assert derive.dispatched_slugs([parent]) == frozenset()


def test_self_reference_is_not_dispatch() -> None:
    """A unit naming itself in its own frontmatter dispatches nothing."""
    lone = unit(slug="agdt.a", frontmatter='\nhandoffs:\n  - agent: "agdt.a"\n', body="x\n")
    assert derive.dispatched_slugs([lone]) == frozenset()
