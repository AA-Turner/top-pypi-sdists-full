"""Tests for approve_pull_request_async function."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.async_commands import approve_pull_request_async


class TestApprovePullRequestAsync:
    def test_delegates_to_provider_neutral_approval(self, mock_background_and_state):
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        with patch("agentic_devtools.cli.pull_request_approval.approve_pull_request_async") as approve_neutral:
            approve_pull_request_async()

        approve_neutral.assert_called_once_with(provider="azure_devops", pull_request_id=None, content=None)
