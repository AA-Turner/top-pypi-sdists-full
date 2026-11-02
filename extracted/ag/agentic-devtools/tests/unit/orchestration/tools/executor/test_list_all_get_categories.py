"""Tests for ToolExecutor.list_all() and ToolExecutor.get_categories()."""

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


def _noop() -> None:
    """No-op tool function — these tests don't invoke tools."""
    return None


def _make_executor(*tools: tuple[str, str]) -> ToolExecutor:
    """Create a ToolExecutor with tools registered under given (name, category) pairs."""
    registry = ConcreteToolRegistry()
    for name, category in tools:
        registry.register(
            ToolDefinition(
                name=name,
                description=f"Tool {name}",
                category=category,
                input_schema={"type": "object", "properties": {}},
            ),
            fn=_noop,
        )
    return ToolExecutor(registry, dry_run_fn=lambda: False)


class TestListAll:
    """ToolExecutor.list_all() delegates to the underlying registry."""

    def test_empty_registry(self):
        """list_all returns empty dict when no tools are registered."""
        executor = _make_executor()
        assert executor.list_all() == {}

    def test_returns_registered_tools(self):
        """list_all returns all registered tools as a name→ToolDefinition mapping."""
        executor = _make_executor(("git_branch", "git"), ("jira_comment", "jira"))
        result = executor.list_all()
        assert set(result) == {"git_branch", "jira_comment"}
        assert all(isinstance(d, ToolDefinition) for d in result.values())

    def test_satisfies_tool_registry_protocol(self):
        """ToolExecutor.list_all satisfies the ToolRegistry Protocol contract."""
        from agentic_devtools.orchestration.execution.protocols import ToolRegistry

        executor = _make_executor(("echo", "testing"))
        assert isinstance(executor, ToolRegistry)


class TestGetCategories:
    """ToolExecutor.get_categories() delegates to the underlying registry."""

    def test_empty_registry(self):
        """get_categories returns empty list when no tools are registered."""
        executor = _make_executor()
        assert executor.get_categories() == []

    def test_returns_sorted_categories(self):
        """get_categories returns sorted unique category names."""
        executor = _make_executor(
            ("tool_a", "zzz"),
            ("tool_b", "aaa"),
            ("tool_c", "aaa"),
        )
        assert executor.get_categories() == ["aaa", "zzz"]

    def test_deduplicates_categories(self):
        """get_categories deduplicates categories across tools."""
        executor = _make_executor(("t1", "git"), ("t2", "git"), ("t3", "jira"))
        cats = executor.get_categories()
        assert cats.count("git") == 1
        assert "jira" in cats
