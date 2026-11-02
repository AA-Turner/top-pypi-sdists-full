"""Tests for the repository provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderRepositoryMixin:
    """Tests for the repository provider capability."""

    def test_graphql_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement graphql"):
            provider.graphql(query="{ viewer { login } }")

    def test_get_commit_author_login_default_returns_empty(self) -> None:
        provider = _ConcreteProvider()
        assert provider.get_commit_author_login("abc123") == ""

    def test_list_relevant_pull_requests_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_relevant_pull_requests"):
            provider.list_relevant_pull_requests()

    def test_get_pr_copilot_attribution_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_pr_copilot_attribution"):
            provider.get_pr_copilot_attribution(1)

    def test_reclaim_copilot_commit_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement reclaim_copilot_commit"):
            provider.reclaim_copilot_commit(pr_number=1, head_branch="feature", head_sha="abc123")
