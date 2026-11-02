"""Tests for GitHubPRFilesMixin."""

from unittest.mock import Mock

from agentic_devtools.cli.ci.github_pr_files import GitHubPRFilesMixin


class TestGitHubPRFilesMixin:
    """Tests for the provider's strict inventory method."""

    def test_fetches_raw_paginated_inventory_and_checks_completeness(self) -> None:
        provider = GitHubPRFilesMixin()
        provider._gh_api = Mock(return_value='[{"filename":"a.py"}]')
        provider._repo_api = Mock(return_value="/pulls/42/files")

        assert provider.list_pr_files_complete(42, 1) == ["a.py"]
        provider._repo_api.assert_called_once_with("/pulls/42/files")
        provider._gh_api.assert_called_once_with("/pulls/42/files", paginate=True)

    def test_does_not_fetch_inventory_when_file_count_reaches_api_cap(self) -> None:
        provider = GitHubPRFilesMixin()
        provider._gh_api = Mock()
        provider._repo_api = Mock()

        assert provider.list_pr_files_complete(42, 3000) is None
        provider._gh_api.assert_not_called()
        provider._repo_api.assert_not_called()
