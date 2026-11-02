"""Tests for the get_pull_request_details_async_cli function."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.async_commands import get_pull_request_details_async_cli


class TestGetPullRequestDetailsAsyncCli:
    """Tests for the legacy wrapper around the provider-neutral PR-details CLI."""

    def test_delegates_to_provider_neutral_async_cli(self):
        with patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async_cli") as neutral_async_cli:
            get_pull_request_details_async_cli()
        neutral_async_cli.assert_called_once_with()
