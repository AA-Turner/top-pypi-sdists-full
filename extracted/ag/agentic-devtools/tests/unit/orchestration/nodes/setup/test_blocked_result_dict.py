"""Tests for agentic_devtools.orchestration.nodes.setup._blocked_result_dict."""

import pytest

from agentic_devtools.models.git_results import BlockedState, SetupResult
from agentic_devtools.orchestration.nodes import setup as setup_mod


class TestBlockedResultDict:
    def test_raises_when_error_is_none(self):
        with pytest.raises(ValueError, match="non-None error"):
            setup_mod._blocked_result_dict(SetupResult(worktree_path="/wt", branch_name="b", mode="created"))

    def test_returns_blocked_state_dict_when_error_is_present(self):
        result = setup_mod._blocked_result_dict(
            SetupResult(error=BlockedState(category="context_mismatch", message="wrong worktree"))
        )

        assert result["status"] == "blocked"
        assert result["error"] == "wrong worktree"
        assert result["setup_complete"] is False
