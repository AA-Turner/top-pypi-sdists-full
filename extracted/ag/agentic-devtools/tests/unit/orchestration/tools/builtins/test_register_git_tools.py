"""Tests for built-in tool registrations."""

from agentic_devtools.orchestration.tools.builtins import register_all_builtins
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestRegisterGitTools:
    """Tests for git tool registrations."""

    def test_git_tools_registered(self):
        """Git category tools are registered."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        git_tools = registry.get_tools(category="git")
        assert len(git_tools) >= 6
        names = {t.name for t in git_tools}
        assert "git_stage_all" in names
        assert "git_save_work" in names
        assert "git_push" in names
        assert "git_current_branch" in names
        assert "git_get_current_branch" in names
        assert "git_get_status" in names
