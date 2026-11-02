"""Tests for the issue mutations provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderIssueMutationsMixin:
    """Tests for the issue mutations provider capability."""

    def test_post_issue_comment_as_bookkeeping_token_is_unsupported_by_default(self) -> None:
        with pytest.raises(NotImplementedError, match="does not implement post_issue_comment_as_bookkeeping_token"):
            _ConcreteProvider().post_issue_comment_as_bookkeeping_token(42, "body")

    def test_post_issue_comment_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement post_issue_comment"):
            provider.post_issue_comment(1, "body")

    def test_close_issue_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement close_issue"):
            provider.close_issue(1)

    def test_close_pr_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement close_pr"):
            provider.close_pr(1)
