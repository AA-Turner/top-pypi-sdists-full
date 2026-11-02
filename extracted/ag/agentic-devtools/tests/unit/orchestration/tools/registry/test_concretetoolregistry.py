"""Tests for ConcreteToolRegistry."""

import pytest

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestConcreteToolRegistry:
    """Tests for registration and lookup."""

    def _make_definition(self, name: str = "test_tool", category: str = "testing") -> ToolDefinition:
        return ToolDefinition(
            name=name,
            description=f"A {name} tool",
            category=category,
            input_schema={"type": "object", "properties": {}},
        )

    def test_register_and_get(self):
        """Register a tool and look it up by name."""
        registry = ConcreteToolRegistry()
        defn = self._make_definition()
        registry.register(defn, fn=lambda: None)
        assert registry.get("test_tool") is defn

    def test_get_nonexistent_returns_none(self):
        """Lookup of non-registered tool returns None."""
        registry = ConcreteToolRegistry()
        assert registry.get("nonexistent") is None

    def test_register_non_callable_raises_type_error(self):
        """Registering a non-callable implementation fails fast with TypeError."""
        registry = ConcreteToolRegistry()
        defn = self._make_definition()
        with pytest.raises(TypeError, match="must be callable"):
            registry.register(defn, fn=None)  # type: ignore[arg-type]

    def test_duplicate_name_raises(self):
        """Registering same name twice raises ValueError."""
        registry = ConcreteToolRegistry()
        defn = self._make_definition()
        registry.register(defn, fn=lambda: None)
        with pytest.raises(ValueError, match="already registered"):
            registry.register(defn, fn=lambda: None)

    def test_list_all(self):
        """list_all returns flat dict of all tools."""
        registry = ConcreteToolRegistry()
        registry.register(self._make_definition("t1", "git"), fn=lambda: None)
        registry.register(self._make_definition("t2", "jira"), fn=lambda: None)
        all_tools = registry.list_all()
        assert len(all_tools) == 2
        assert "t1" in all_tools
        assert "t2" in all_tools

    def test_get_categories(self):
        """get_categories returns sorted unique categories."""
        registry = ConcreteToolRegistry()
        registry.register(self._make_definition("t1", "git"), fn=lambda: None)
        registry.register(self._make_definition("t2", "jira"), fn=lambda: None)
        registry.register(self._make_definition("t3", "git"), fn=lambda: None)
        cats = registry.get_categories()
        assert cats == ["git", "jira"]

    def test_get_tools_by_category(self):
        """get_tools filters by category."""
        registry = ConcreteToolRegistry()
        registry.register(self._make_definition("t1", "git"), fn=lambda: None)
        registry.register(self._make_definition("t2", "jira"), fn=lambda: None)
        registry.register(self._make_definition("t3", "git"), fn=lambda: None)
        git_tools = registry.get_tools(category="git")
        assert len(git_tools) == 2
        assert all(t.category == "git" for t in git_tools)

    def test_list_by_category(self):
        """list_by_category groups tools."""
        registry = ConcreteToolRegistry()
        registry.register(self._make_definition("t1", "git"), fn=lambda: None)
        registry.register(self._make_definition("t2", "jira"), fn=lambda: None)
        grouped = registry.list_by_category()
        assert "git" in grouped
        assert "jira" in grouped
        assert len(grouped["git"]) == 1
