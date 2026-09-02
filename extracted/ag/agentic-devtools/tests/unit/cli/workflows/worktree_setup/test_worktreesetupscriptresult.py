"""Tests for WorktreeSetupScriptResult."""

from agentic_devtools.cli.workflows.worktree_setup import (
    WorktreeSetupScriptResult,
)


class TestWorktreeSetupScriptResult:
    """Tests for WorktreeSetupScriptResult dataclass."""

    def test_required_field_status(self):
        """Test that status is a required field."""
        result = WorktreeSetupScriptResult(status="missing")
        assert result.status == "missing"

    def test_optional_fields_default_to_none(self):
        """Test that optional fields default to None."""
        result = WorktreeSetupScriptResult(status="missing")
        assert result.exit_code is None
        assert result.error_message is None
        assert result.category is None

    def test_succeeded_with_exit_code(self):
        """Test a succeeded outcome with an exit code."""
        result = WorktreeSetupScriptResult(status="succeeded", exit_code=0)
        assert result.status == "succeeded"
        assert result.exit_code == 0
        assert result.error_message is None
        assert result.category is None

    def test_failed_with_all_fields(self):
        """Test a failed outcome populated with all optional fields."""
        result = WorktreeSetupScriptResult(
            status="failed",
            exit_code=1,
            error_message="exit: provider setup failed",
            category="execution",
        )
        assert result.status == "failed"
        assert result.exit_code == 1
        assert result.error_message == "exit: provider setup failed"
        assert result.category == "execution"

    def test_failed_validation_category(self):
        """Test a failed outcome with validation category."""
        result = WorktreeSetupScriptResult(
            status="failed",
            error_message="script is a symlink",
            category="validation",
        )
        assert result.status == "failed"
        assert result.exit_code is None
        assert result.category == "validation"

    def test_failed_timeout_category(self):
        """Test a failed outcome with timeout category."""
        result = WorktreeSetupScriptResult(
            status="failed",
            error_message="timed out after 60 seconds",
            category="timeout",
        )
        assert result.status == "failed"
        assert result.category == "timeout"
