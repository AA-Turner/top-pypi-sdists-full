"""Tests for trusted_loop_comment_logins."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.provider import trusted_loop_comment_logins


def test_normalizes_provider_trusted_logins() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"Workflow-Bot", " "}

    assert trusted_loop_comment_logins(provider) == {"workflow-bot"}


def test_falls_back_to_pr_token_login_for_older_providers() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = ["not", "a", "set"]
    provider.get_pr_token_login.return_value = "Pat-Owner"

    assert trusted_loop_comment_logins(provider) == {"pat-owner"}


def test_supports_legacy_provider_without_trusted_login_method() -> None:
    class LegacyProvider:
        def get_pr_token_login(self) -> str:
            return "Pat-Owner"

    assert trusted_loop_comment_logins(LegacyProvider()) == {"pat-owner"}  # type: ignore[arg-type]


def test_returns_empty_when_no_usable_login_is_available() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = None
    provider.get_pr_token_login.return_value = " "

    assert trusted_loop_comment_logins(provider) == set()
