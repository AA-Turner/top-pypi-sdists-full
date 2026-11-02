"""Tests for SetupResult."""

from agentic_devtools.models.git_results import BlockedState, SetupResult


class TestSetupResult:
    """Tests for SetupResult dataclass."""

    def test_defaults_represent_unpopulated_result(self):
        """SetupResult defaults all optional fields to None."""
        result = SetupResult()

        assert result.worktree_path is None
        assert result.branch_name is None
        assert result.mode is None
        assert result.error is None

    def test_stores_success_fields(self):
        """SetupResult stores created worktree details."""
        result = SetupResult(worktree_path="/repo/1900", branch_name="feature/1900/tests", mode="created")

        assert result.worktree_path == "/repo/1900"
        assert result.branch_name == "feature/1900/tests"
        assert result.mode == "created"
        assert result.error is None

    def test_stores_error_state(self):
        """SetupResult stores structured setup errors."""
        error = BlockedState(category="corruption", message="stale directory")
        result = SetupResult(error=error)

        assert result.error is error
