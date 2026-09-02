"""Tests for GitHubActionsProvider.list_prs_with_label()."""

import json
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


class TestListPrsWithLabel:
    """Search-API listing of PRs carrying a label."""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_pr_numbers(self, mock_gh) -> None:
        mock_gh.return_value = json.dumps({"items": [{"number": 1}, {"number": 2}]})
        provider = GitHubActionsProvider(repo="o/r")
        assert provider.list_prs_with_label("in-progress") == [1, 2]

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_includes_repo_in_query(self, mock_gh) -> None:
        mock_gh.return_value = json.dumps({"items": []})
        provider = GitHubActionsProvider(repo="o/r")
        provider.list_prs_with_label("lbl")
        endpoint = mock_gh.call_args[0][0]
        assert "repo%3Ao%2Fr" in endpoint  # url-encoded "repo:o/r"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.dict("os.environ", {"GITHUB_REPOSITORY": "env-owner/env-repo"}, clear=False)
    def test_uses_env_repo_when_constructor_repo_is_empty_string(self, mock_gh) -> None:
        mock_gh.return_value = json.dumps({"items": []})
        provider = GitHubActionsProvider(repo="")
        provider.list_prs_with_label("lbl")
        endpoint = mock_gh.call_args[0][0]
        assert "repo%3Aenv-owner%2Fenv-repo" in endpoint

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.dict("os.environ", {"GITHUB_REPOSITORY": "env-owner/env-repo"}, clear=False)
    def test_uses_env_repo_when_constructor_repo_is_none(self, mock_gh) -> None:
        mock_gh.return_value = json.dumps({"items": []})
        provider = GitHubActionsProvider()
        provider.list_prs_with_label("lbl")
        endpoint = mock_gh.call_args[0][0]
        assert "repo%3Aenv-owner%2Fenv-repo" in endpoint

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.dict("os.environ", {}, clear=True)
    def test_omits_repo_when_no_repo_resolved(self, mock_gh) -> None:
        mock_gh.return_value = json.dumps({"items": []})
        provider = GitHubActionsProvider(repo="")
        provider.list_prs_with_label("lbl")
        endpoint = mock_gh.call_args[0][0]
        assert "repo%3A" not in endpoint

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.dict("os.environ", {}, clear=True)
    def test_omits_repo_when_constructor_repo_is_none_and_no_env(self, mock_gh) -> None:
        mock_gh.return_value = json.dumps({"items": []})
        provider = GitHubActionsProvider()
        provider.list_prs_with_label("lbl")
        endpoint = mock_gh.call_args[0][0]
        assert "repo%3A" not in endpoint

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.dict("os.environ", {"GITHUB_REPOSITORY": ""}, clear=True)
    def test_omits_repo_when_env_repo_is_empty_string(self, mock_gh) -> None:
        mock_gh.return_value = json.dumps({"items": []})
        provider = GitHubActionsProvider(repo="")
        provider.list_prs_with_label("lbl")
        endpoint = mock_gh.call_args[0][0]
        assert "repo%3A" not in endpoint

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_skips_items_without_number(self, mock_gh) -> None:
        mock_gh.return_value = json.dumps({"items": [{"number": 5}, {"title": "no number"}, {"number": 0}]})
        provider = GitHubActionsProvider(repo="o/r")
        assert provider.list_prs_with_label("lbl") == [5]

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_handles_missing_items_key(self, mock_gh) -> None:
        mock_gh.return_value = json.dumps({})
        provider = GitHubActionsProvider(repo="o/r")
        assert provider.list_prs_with_label("lbl") == []

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_uses_deterministic_sort(self, mock_gh) -> None:
        mock_gh.return_value = json.dumps({"items": []})
        provider = GitHubActionsProvider(repo="o/r")
        provider.list_prs_with_label("lbl")
        mock_gh.assert_called_once()
        endpoint = mock_gh.call_args[0][0]
        assert "sort=updated" in endpoint
        assert "order=asc" in endpoint

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_uses_pagination(self, mock_gh) -> None:
        mock_gh.return_value = json.dumps({"items": []})
        provider = GitHubActionsProvider(repo="o/r")
        provider.list_prs_with_label("lbl")
        mock_gh.assert_called_once()
        kwargs = mock_gh.call_args[1]
        assert kwargs.get("paginate") is True
