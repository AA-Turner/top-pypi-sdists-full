"""Tests for the reviews provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderReviewsMixin:
    """Tests for the reviews provider capability."""

    def test_request_reviewer_returns_none(self) -> None:
        provider = _ConcreteProvider()
        provider.request_reviewer(1, "user")

    def test_native_review_thread_creation_is_unsupported_by_default(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="supported only by GitHub"):
            provider.create_review_thread(
                pr_number=1,
                commit_sha="head",
                path="file.py",
                line=1,
                side="RIGHT",
                body="finding",
            )

    def test_delete_review_comments_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement delete_review_comments"):
            provider.delete_review_comments(1)

    def test_list_review_thread_states_default_raises_not_implemented(self) -> None:
        """Providers must opt into review-thread state; the default fails closed."""
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_review_thread_states"):
            provider.list_review_thread_states(1)
