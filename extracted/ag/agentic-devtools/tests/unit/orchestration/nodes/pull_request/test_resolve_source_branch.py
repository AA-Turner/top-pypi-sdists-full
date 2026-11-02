"""Tests for _resolve_source_branch."""

from agentic_devtools.models.git_results import SetupResult
from agentic_devtools.orchestration.nodes.pull_request import _resolve_source_branch


class TestResolveSourceBranch:
    def test_prefers_explicit_source_branch(self):
        setup = SetupResult(worktree_path="/wt", branch_name="from-setup", mode="created")
        assert _resolve_source_branch({"source_branch": " explicit ", "setup_result": setup}) == "explicit"

    def test_falls_back_to_setup_result_branch(self):
        setup = SetupResult(worktree_path="/wt", branch_name=" from-setup ", mode="resumed")
        assert _resolve_source_branch({"setup_result": setup}) == "from-setup"

    def test_ignores_blank_source_branch(self):
        setup = SetupResult(worktree_path="/wt", branch_name="from-setup", mode="created")
        assert _resolve_source_branch({"source_branch": "   ", "setup_result": setup}) == "from-setup"

    def test_returns_empty_when_nothing_available(self):
        assert _resolve_source_branch({}) == ""

    def test_returns_empty_when_setup_result_branch_blank(self):
        setup = SetupResult(worktree_path="/wt", branch_name="   ", mode="created")
        assert _resolve_source_branch({"setup_result": setup}) == ""

    def test_returns_empty_when_source_branch_non_string(self):
        assert _resolve_source_branch({"source_branch": 42}) == ""
