"""Tests for agentic_devtools.skill_injector.InjectionPlan."""

from __future__ import annotations

import pytest

from agentic_devtools.skill_injector import InjectionPlan


class TestInjectionPlan:
    """Tests for the InjectionPlan dataclass."""

    def test_stores_three_categories(self) -> None:
        """The three diff categories are stored separately."""
        plan = InjectionPlan(
            kind="agents",
            added=("agdt.a.agent.md",),
            overwritten=("agdt.b.agent.md",),
            deleted=("agdt.c.agent.md",),
        )
        assert plan.kind == "agents"
        assert plan.added == ("agdt.a.agent.md",)
        assert plan.overwritten == ("agdt.b.agent.md",)
        assert plan.deleted == ("agdt.c.agent.md",)

    def test_is_frozen(self) -> None:
        """Instances are immutable."""
        plan = InjectionPlan(kind="prompts", added=(), overwritten=(), deleted=())
        with pytest.raises(AttributeError):
            plan.kind = "agents"  # type: ignore[misc]

    def test_equality_by_value(self) -> None:
        """Two plans with identical fields compare equal."""
        first = InjectionPlan(kind="agents", added=("x",), overwritten=(), deleted=())
        second = InjectionPlan(kind="agents", added=("x",), overwritten=(), deleted=())
        assert first == second
        assert first != InjectionPlan(kind="agents", added=(), overwritten=(), deleted=("x",))

    def test_case_renames_defaults_to_empty_tuple(self) -> None:
        """case_renames defaults to an empty tuple when not supplied."""
        plan = InjectionPlan(kind="skills", added=(), overwritten=(), deleted=())
        assert plan.case_renames == ()

    def test_case_renames_stored_when_provided(self) -> None:
        """case_renames is stored when explicitly provided."""
        plan = InjectionPlan(
            kind="skills",
            added=(),
            overwritten=("my-skill/guide.md",),
            deleted=(),
            case_renames=(("my-skill/Guide.md", "my-skill/guide.md"),),
        )
        assert plan.case_renames == (("my-skill/Guide.md", "my-skill/guide.md"),)
