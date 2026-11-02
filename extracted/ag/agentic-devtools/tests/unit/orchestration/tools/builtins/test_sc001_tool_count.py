"""Tests for SC-001: at least 20 tools across all 7 categories."""

from agentic_devtools.orchestration.tools.builtins import register_all_builtins
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestSC001ToolCount:
    """SC-001: Registry has ≥20 tools across 7 categories."""

    def test_minimum_20_tools(self):
        """At least 20 tools registered (excluding aliases)."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        all_tools = registry.list_all()
        # get_issue_context is an alias, don't count it
        non_alias_count = len([t for t in all_tools.values() if t.name != "get_issue_context"])
        assert non_alias_count >= 20, f"Only {non_alias_count} tools registered, need ≥20"

    def test_all_seven_categories(self):
        """All 7 required categories present."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        categories = set(registry.get_categories())
        required = {"git", "jira", "azure_devops", "github", "filesystem", "testing", "state"}
        missing = required - categories
        assert not missing, f"Missing categories: {missing}"
