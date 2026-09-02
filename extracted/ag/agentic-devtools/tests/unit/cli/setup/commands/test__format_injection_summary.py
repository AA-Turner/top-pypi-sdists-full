"""Tests for _format_injection_summary."""

from __future__ import annotations

from agentic_devtools.cli.setup.commands import _format_injection_summary
from agentic_devtools.skill_injector import InjectionSummary


class TestFormatInjectionSummary:
    """Tests for _format_injection_summary."""

    def test_both_none_omits_prune_detail(self) -> None:
        """Legacy inject-all (both axes None) reports no platform filter."""
        line = _format_injection_summary(InjectionSummary(injected=257, pruned=0), None, None)
        assert line == "  ✓ Injected 257 agent/prompt/skill items (no platform filter applied)"

    def test_both_axes_resolved(self) -> None:
        """Both axes resolved → prune count + both axis labels."""
        line = _format_injection_summary(InjectionSummary(injected=145, pruned=112), "github", "github")
        assert line == (
            "  ✓ Injected 145 agent/prompt/skill items, pruned 112 (issue_adapter=github, code_hosting=github)"
        )

    def test_issue_adapter_only(self) -> None:
        """Only issue_adapter resolved → code_hosting renders as unrestricted."""
        line = _format_injection_summary(InjectionSummary(injected=248, pruned=9), "jira", None)
        assert line == (
            "  ✓ Injected 248 agent/prompt/skill items, pruned 9 (issue_adapter=jira, code_hosting=unrestricted)"
        )

    def test_code_hosting_only(self) -> None:
        """Only code_hosting resolved → issue_adapter renders as unrestricted."""
        line = _format_injection_summary(InjectionSummary(injected=250, pruned=7), None, "azure_devops")
        assert line == (
            "  ✓ Injected 250 agent/prompt/skill items, pruned 7 "
            "(issue_adapter=unrestricted, code_hosting=azure_devops)"
        )

    def test_includes_injected_agent_prompt_skills_substring(self) -> None:
        """All variants keep the 'Injected N agent/prompt/skill items' substring."""
        assert "Injected 3 agent/prompt/skill items" in _format_injection_summary(
            InjectionSummary(injected=3, pruned=0), None, None
        )
        assert "Injected 3 agent/prompt/skill items" in _format_injection_summary(
            InjectionSummary(injected=3, pruned=1), "github", "azure_devops"
        )
