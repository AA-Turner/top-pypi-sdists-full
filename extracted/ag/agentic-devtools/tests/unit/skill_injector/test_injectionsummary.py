"""Tests for the InjectionSummary dataclass."""

from __future__ import annotations

import dataclasses

import pytest

from agentic_devtools.skill_injector import InjectionPlan, InjectionSummary


class TestInjectionSummary:
    """Tests for the InjectionSummary frozen dataclass."""

    def test_stores_injected_and_pruned_counts(self) -> None:
        summary = InjectionSummary(injected=5, pruned=2)
        assert summary.injected == 5
        assert summary.pruned == 2

    def test_is_frozen(self) -> None:
        summary = InjectionSummary(injected=1, pruned=0)
        with pytest.raises(dataclasses.FrozenInstanceError):
            summary.injected = 9  # type: ignore[misc]

    def test_equality_by_value(self) -> None:
        assert InjectionSummary(injected=3, pruned=1) == InjectionSummary(injected=3, pruned=1)
        assert InjectionSummary(injected=3, pruned=1) != InjectionSummary(injected=3, pruned=2)

    def test_equality_ignores_plan_details_and_blocked_flag(self) -> None:
        plan = InjectionPlan(kind="agents", added=(), overwritten=(), deleted=("agdt.stale.agent.md",))
        assert InjectionSummary(injected=3, pruned=1, plans=(plan,), deletions_blocked=True) == InjectionSummary(
            injected=3,
            pruned=1,
        )

    def test_zero_counts(self) -> None:
        summary = InjectionSummary(injected=0, pruned=0)
        assert summary.injected == 0
        assert summary.pruned == 0
