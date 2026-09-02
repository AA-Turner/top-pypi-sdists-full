"""Tests for add_pull_request_comment_async function."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.async_commands import add_pull_request_comment_async
from tests.unit.cli.azure_devops.async_commands._helpers import assert_function_in_script, get_script_from_call


class TestAddPullRequestCommentAsync:
    def test_spawns_background_task(self, mock_background_and_state, capsys):
        """Test command delegates to the provider-neutral background task."""
        from agentic_devtools.state import set_value

        set_value("platform.code_hosting", "azure_devops")
        set_value("pull_request_id", "12345")
        set_value("content", "Test comment")
        with patch("sys.argv", ["agdt-add-pull-request-comment"]):
            add_pull_request_comment_async()
        captured = capsys.readouterr()
        assert "Background task started" in captured.out
        script = get_script_from_call(mock_background_and_state["mock_popen"])
        assert_function_in_script(script, "agentic_devtools.cli.pull_request_comments", "_run_request_snapshot")
