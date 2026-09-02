"""Tests for _get_task_run_id."""

from agentic_devtools.cli.vscode_tasks import _get_task_run_id


class TestGetTaskRunId:
    """Tests for the _get_task_run_id helper."""

    def test_returns_none_when_args_missing(self):
        """Returns None when the task has no 'args' key."""
        assert _get_task_run_id({}) is None

    def test_returns_none_when_args_not_a_list(self):
        """Returns None when 'args' is not a list."""
        assert _get_task_run_id({"args": "not-a-list"}) is None

    def test_returns_none_when_run_id_arg_absent(self):
        """Returns None when --run-id is not in args."""
        assert _get_task_run_id({"args": ["--foo", "bar"]}) is None

    def test_returns_none_when_run_id_is_last_arg(self):
        """Returns None when --run-id is the last token (no following value)."""
        assert _get_task_run_id({"args": ["--run-id"]}) is None

    def test_returns_none_when_run_id_value_not_string(self):
        """Returns None when --run-id is followed by a non-string value."""
        assert _get_task_run_id({"args": ["--run-id", 123]}) is None

    def test_returns_none_when_run_id_value_blank(self):
        """Returns None when --run-id is followed by a blank/whitespace string."""
        assert _get_task_run_id({"args": ["--run-id", "   "]}) is None

    def test_returns_stripped_run_id(self):
        """Returns the stripped --run-id value."""
        assert _get_task_run_id({"args": ["--run-id", "abc-123"]}) == "abc-123"

    def test_strips_whitespace_from_run_id(self):
        """Strips leading/trailing whitespace from the --run-id value."""
        assert _get_task_run_id({"args": ["--run-id", "  abc-123  "]}) == "abc-123"

    def test_returns_first_run_id_when_multiple_present(self):
        """Returns the value after the first --run-id token found."""
        assert _get_task_run_id({"args": ["--run-id", "first", "--run-id", "second"]}) == "first"

    def test_handles_other_args_before_run_id(self):
        """Correctly extracts --run-id when other args precede it."""
        assert _get_task_run_id({"args": ["--worktree-path", "/tmp/wt", "--run-id", "xyz"]}) == "xyz"
