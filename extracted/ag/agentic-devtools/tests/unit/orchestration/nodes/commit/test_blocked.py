"""Tests for agentic_devtools.orchestration.nodes.commit._blocked."""

import pytest

from agentic_devtools.models.git_results import BlockedState, CommitResult
from agentic_devtools.orchestration.nodes import commit as commit_mod


class TestBlocked:
    def test_raises_when_error_is_none(self):
        with pytest.raises(ValueError, match="non-None error"):
            commit_mod._blocked(CommitResult(no_op=False, error=None))

    def test_returns_result_when_error_is_set(self):
        blocked = BlockedState(category="transient", message="net error")
        result = CommitResult(no_op=False, error=blocked)
        assert commit_mod._blocked(result) is result
