"""Tests for agentic_devtools.skill_injector._format_plans."""

from __future__ import annotations

from agentic_devtools.skill_injector import InjectionPlan, _format_plans


class TestFormatPlans:
    """Tests for the _format_plans renderer."""

    def test_empty_plans_render_as_empty_string(self) -> None:
        """No plans → no output at all."""
        assert _format_plans(()) == ""

    def test_all_three_lists_are_labelled(self) -> None:
        """Adds, overwrites and deletes are printed as three labelled lists."""
        plan = InjectionPlan(
            kind="agents",
            added=("agdt.a.agent.md",),
            overwritten=("agdt.b.agent.md",),
            deleted=("agdt.c.agent.md",),
        )
        text = _format_plans((plan,))
        assert "Manifest diff — agents: 1 add(s), 1 overwrite(s), 1 delete(s)" in text
        assert "adds (1):" in text
        assert "+ agdt.a.agent.md" in text
        assert "overwrites (1):" in text
        assert "~ agdt.b.agent.md" in text
        assert "deletes (1):" in text
        assert "- agdt.c.agent.md" in text

    def test_empty_category_renders_none_marker(self) -> None:
        """An empty category is rendered explicitly rather than omitted."""
        plan = InjectionPlan(kind="prompts", added=(), overwritten=(), deleted=())
        text = _format_plans((plan,))
        assert text.count("(none)") == 3

    def test_each_kind_gets_its_own_block(self) -> None:
        """Both kinds are rendered, in the order given."""
        plans = (
            InjectionPlan(kind="agents", added=(), overwritten=(), deleted=()),
            InjectionPlan(kind="prompts", added=(), overwritten=(), deleted=()),
        )
        text = _format_plans(plans)
        assert text.index("agents") < text.index("prompts")
