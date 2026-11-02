"""Tests for the comments provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderCommentsMixin:
    """Tests for the comments provider capability."""

    def test_post_comment_returns_int(self) -> None:
        provider = _ConcreteProvider()
        result = provider.post_comment(1, "hello")
        assert isinstance(result, int)

    def test_post_comment_as_pr_token_defaults_to_post_comment(self) -> None:
        """Base helper falls back to post_comment for providers without override."""
        provider = _ConcreteProvider()
        result = provider.post_comment_as_pr_token(1, "hello")
        assert result == 100

    def test_update_comment_as_pr_token_defaults_to_update_comment(self) -> None:
        """Base helper updates in place when the provider has a single identity."""
        provider = _ConcreteProvider()
        assert provider.update_comment_as_pr_token(1, "hello") is None

    def test_get_bookkeeping_token_login_is_empty_by_default(self) -> None:
        assert _ConcreteProvider().get_bookkeeping_token_login() == ""

    def test_get_trusted_loop_comment_logins_uses_default_token_identity(self, monkeypatch: pytest.MonkeyPatch) -> None:
        provider = _ConcreteProvider()
        monkeypatch.setattr(provider, "get_pr_token_login", lambda: "Workflow-Bot")

        assert provider.get_trusted_loop_comment_logins() == {"workflow-bot"}

    def test_get_trusted_loop_comment_logins_is_empty_without_default_identity(self) -> None:
        assert _ConcreteProvider().get_trusted_loop_comment_logins() == set()

    def test_update_comment_returns_none(self) -> None:
        provider = _ConcreteProvider()
        assert provider.update_comment(1, "updated") is None

    def test_find_comment_returns_none_or_tuple(self) -> None:
        provider = _ConcreteProvider()
        result = provider.find_comment(1, "marker")
        assert result is None

    def test_delete_comment_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement delete_comment"):
            provider.delete_comment(1)

    def test_get_approver_login_default_returns_empty(self) -> None:
        """Base class get_approver_login returns empty string (best-effort default)."""
        provider = _ConcreteProvider()
        assert provider.get_approver_login() == ""

    def test_get_pr_token_login_default_returns_empty(self) -> None:
        """Base class get_pr_token_login returns empty string (best-effort default)."""
        provider = _ConcreteProvider()
        assert provider.get_pr_token_login() == ""

    def test_get_dispatch_login_uses_pr_token_identity(self) -> None:
        provider = _ConcreteProvider()
        provider.get_pr_token_login = lambda: "workflow-bot"  # type: ignore[method-assign]
        assert provider.get_dispatch_login() == "workflow-bot"
