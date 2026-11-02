"""Tests for _github_login_required."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.github import browser_apply_autofix


class TestGithubLoginRequired:
    """Tests for detecting whether the current page needs GitHub authentication."""

    def test_returns_false_for_authenticated_github_page(self) -> None:
        page = MagicMock()
        page.url = "https://github.com/swai-factory/agentic-devtools"
        page.locator.return_value.count.return_value = 0

        assert browser_apply_autofix._github_login_required(page) is False

    def test_returns_true_for_github_login_url(self) -> None:
        page = MagicMock()
        page.url = "https://github.com/login"

        assert browser_apply_autofix._github_login_required(page) is True

    @pytest.mark.parametrize(
        "url",
        [
            "https://github.com/login-service/repo/pull/7",
            "https://github.com/acme/login-service/pull/7",
            "https://github.com/sso-tools/repo/pull/7",
            "https://github.com/acme/sso-tools/pull/7",
        ],
    )
    def test_returns_false_for_repository_paths_starting_with_auth_route_names(self, url: str) -> None:
        page = MagicMock()
        page.url = url
        page.locator.return_value.count.return_value = 0

        assert browser_apply_autofix._github_login_required(page) is False

    @pytest.mark.parametrize(
        "url",
        [
            "https://github.com/enterprises/acme/sso",
            "https://github.com/orgs/acme/sso",
        ],
    )
    def test_returns_true_for_github_sso_routes(self, url: str) -> None:
        page = MagicMock()
        page.url = url

        assert browser_apply_autofix._github_login_required(page) is True

    def test_returns_true_for_non_github_identity_provider_url(self) -> None:
        page = MagicMock()
        page.url = "https://login.microsoftonline.com/example"

        assert browser_apply_autofix._github_login_required(page) is True

    def test_returns_true_when_anonymous_github_page_has_sign_in_link(self) -> None:
        page = MagicMock()
        page.url = "https://github.com/"
        page.locator.return_value.count.return_value = 1

        assert browser_apply_autofix._github_login_required(page) is True

    def test_returns_true_when_sign_in_link_has_return_target(self) -> None:
        page = MagicMock()
        page.url = "https://github.com/"
        page.locator.return_value.count.return_value = 1

        assert browser_apply_autofix._github_login_required(page) is True
        page.locator.assert_called_once_with("a[href^='/login']")
