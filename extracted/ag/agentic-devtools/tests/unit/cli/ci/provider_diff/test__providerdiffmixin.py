"""Tests for the diff provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderDiffMixin:
    """Tests for the diff provider capability."""

    def test_get_pr_diff_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_pr_diff"):
            provider.get_pr_diff(1)

    def test_get_ref_sha_default_returns_empty(self) -> None:
        """Base class get_ref_sha degrades to an empty string."""
        provider = _ConcreteProvider()
        assert provider.get_ref_sha("main") == ""

    def test_compute_diff_hash_default_returns_none(self) -> None:
        """Base class diff fingerprint capability is optional."""
        provider = _ConcreteProvider()
        assert provider.compute_diff_hash(base_branch="main", sha="head") is None

    def test_compute_diff_files_default_returns_none(self) -> None:
        """Base class diff file inventory capability is optional."""
        provider = _ConcreteProvider()
        assert provider.compute_diff_files(base_branch="main", sha="head") is None

    def test_get_commit_range_diff_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_commit_range_diff"):
            provider.get_commit_range_diff("abc", "def")

    def test_get_commit_range_diff_bytes_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_commit_range_diff_bytes"):
            provider.get_commit_range_diff_bytes("abc", "def")

    def test_get_commit_range_diff_change_counts_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_commit_range_diff_change_counts"):
            provider.get_commit_range_diff_change_counts("abc", "def")

    def test_count_commits_behind_default_returns_zero(self) -> None:
        provider = _ConcreteProvider()
        result = provider.count_commits_behind(pr_number=1, base_branch="main", head_branch="feature")
        assert result == 0

    def test_rebase_onto_base_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement rebase_onto_base"):
            provider.rebase_onto_base(pr_number=1, base_branch="main", head_branch="feature", head_sha="abc123")


def test_list_pr_commits_requires_provider_support():
    with pytest.raises(NotImplementedError):
        _ConcreteProvider().list_pr_commits(1)
