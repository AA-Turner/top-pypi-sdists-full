"""Tests for the Unit dataclass in record_discovery_baseline."""

from __future__ import annotations

from tests.scripts.record_discovery_baseline import baseline


def test_sort_key_orders_by_surface_then_invocation_then_file():
    """sort_key returns the surface, invocation and backing file in that order."""
    unit = baseline.Unit("prompt", "/agdt.set", ".github/prompts/agdt.set.prompt.md")
    assert unit.sort_key() == ("prompt", "/agdt.set", ".github/prompts/agdt.set.prompt.md")


def test_units_are_hashable_and_comparable():
    """Unit is a frozen dataclass, so equal units compare equal."""
    first = baseline.Unit("skill", "run-checks", ".agents/skills/run-checks/SKILL.md")
    second = baseline.Unit("skill", "run-checks", ".agents/skills/run-checks/SKILL.md")
    assert first == second
