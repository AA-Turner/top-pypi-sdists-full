"""Tests for get_pull_request_details_async function."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.async_commands import get_pull_request_details_async


class TestGetPullRequestDetailsAsync:
    def test_delegates_to_provider_neutral_async_command(self):
        with patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as neutral_async:
            get_pull_request_details_async()
        neutral_async.assert_called_once_with()
