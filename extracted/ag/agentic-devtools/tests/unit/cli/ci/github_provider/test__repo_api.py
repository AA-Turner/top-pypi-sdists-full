"""Tests for GitHubActionsProvider._repo_api()."""

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


class TestRepoApi:
    """Tests for GitHubActionsProvider._repo_api()."""

    def test_explicit_repo_is_prefixed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """An explicit constructor repo is used for the /repos prefix."""
        monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider._repo_api("/actions/variables/X") == "/repos/owner/repo/actions/variables/X"

    def test_explicit_repo_takes_precedence_over_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """The constructor repo wins over GITHUB_REPOSITORY when both are set."""
        monkeypatch.setenv("GITHUB_REPOSITORY", "env-owner/env-repo")
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider._repo_api("/pulls/1") == "/repos/owner/repo/pulls/1"

    def test_falls_back_to_github_repository_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When no explicit repo is given, GITHUB_REPOSITORY scopes the path.

        Regression test for the scheduler 404 bug: the provider is constructed
        without an explicit repo, so the env fallback must supply the
        /repos/{owner}/{repo} prefix.
        """
        monkeypatch.setenv("GITHUB_REPOSITORY", "swai-factory/agentic-devtools")
        provider = GitHubActionsProvider()
        assert (
            provider._repo_api("/actions/workflows/ai-pr-loop.yml/runs")
            == "/repos/swai-factory/agentic-devtools/actions/workflows/ai-pr-loop.yml/runs"
        )

    def test_no_repo_anywhere_returns_bare_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """With neither an explicit repo nor GITHUB_REPOSITORY, the path is returned as-is."""
        monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
        provider = GitHubActionsProvider(repo="")
        assert provider._repo_api("/pulls/1") == "/pulls/1"
