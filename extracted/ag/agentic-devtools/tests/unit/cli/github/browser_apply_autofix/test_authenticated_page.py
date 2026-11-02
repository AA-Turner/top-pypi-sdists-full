"""Tests for _authenticated_page."""

from __future__ import annotations

import contextlib
from unittest.mock import MagicMock, call, patch

import pytest

from agentic_devtools.cli.github import browser_apply_autofix
from agentic_devtools.cli.github.browser_apply_autofix import BrowserCredentialError, BrowserCredentials


@contextlib.contextmanager
def _noop_lock(*_args, **_kwargs):
    yield


@pytest.fixture(autouse=True)
def _expected_identity():
    with patch.dict(
        "os.environ",
        {
            browser_apply_autofix.ENV_BROWSER_EXPECTED_GITHUB_USER: "expected-user",
            browser_apply_autofix.ENV_BROWSER_EXPECTED_GITHUB_ORG: "owner",
        },
    ):
        yield


class TestAuthenticatedPage:
    """Tests for the _authenticated_page context manager."""

    def test_reuses_authenticated_profile_and_cleans_up(self) -> None:
        page = MagicMock()
        page.url = "https://github.com/"
        page.goto.side_effect = lambda url, **_kwargs: setattr(page, "url", url)
        page.locator.return_value.count.return_value = 0
        page.locator.return_value.get_attribute.return_value = "expected-user"
        context = MagicMock()
        context.pages = [page]
        playwright = MagicMock()
        playwright.chromium.launch_persistent_context.return_value = context
        factory = MagicMock()
        factory.return_value.start.return_value = playwright
        creds = BrowserCredentials(username="u", password="p", totp_secret="s")

        with (
            patch.object(browser_apply_autofix, "_require_sync_playwright", return_value=factory),
            patch.object(browser_apply_autofix, "_profile_lock", _noop_lock),
            patch.object(browser_apply_autofix, "perform_idp_login") as mock_login,
        ):
            with browser_apply_autofix._authenticated_page(
                creds,
                target_url="https://github.com/owner/repo/pull/7",
                headless=False,
            ) as yielded:
                assert yielded is page

        playwright.chromium.launch_persistent_context.assert_called_once_with(
            user_data_dir=str(browser_apply_autofix._default_browser_profile_dir()),
            headless=False,
        )
        page.goto.assert_called_once_with("https://github.com/owner/repo/pull/7", wait_until="domcontentloaded")
        assert [call.args[0] for call in page.locator.call_args_list] == [
            "a[href^='/login']",
            'meta[name="user-login"]',
        ]
        context.close.assert_called_once_with()
        mock_login.assert_not_called()
        playwright.stop.assert_called_once_with()

    def test_logs_in_when_profile_is_not_authenticated(self, tmp_path) -> None:
        page = MagicMock()
        page.url = "https://github.com/login"
        page.locator.return_value.get_attribute.return_value = "expected-user"
        context = MagicMock()
        context.pages = []
        context.new_page.return_value = page
        playwright = MagicMock()
        playwright.chromium.launch_persistent_context.return_value = context
        factory = MagicMock()
        factory.return_value.start.return_value = playwright
        creds = BrowserCredentials(username="u", password="p", totp_secret="s")

        credentials_path = tmp_path / "credentials.json"
        calls = MagicMock()
        with (
            patch.object(browser_apply_autofix, "_require_sync_playwright", return_value=factory),
            patch.object(browser_apply_autofix, "_profile_lock", _noop_lock),
            patch.object(browser_apply_autofix, "load_credentials", return_value=creds) as mock_load_credentials,
            patch.object(browser_apply_autofix, "perform_idp_login") as mock_login,
        ):
            calls.attach_mock(mock_load_credentials, "load_credentials")
            calls.attach_mock(mock_login, "perform_idp_login")
            mock_login.side_effect = lambda logged_in_page, _creds: setattr(
                logged_in_page, "url", "https://github.com/owner/repo/pull/7"
            )
            with browser_apply_autofix._authenticated_page(
                target_url="https://github.com/owner/repo/pull/7",
                profile_dir=tmp_path,
                credentials_path=credentials_path,
            ) as yielded:
                assert yielded is page

        playwright.chromium.launch_persistent_context.assert_called_once_with(
            user_data_dir=str(tmp_path),
            headless=True,
        )
        context.new_page.assert_called_once_with()
        mock_login.assert_called_once_with(page, creds)
        assert calls.mock_calls == [
            call.load_credentials(credentials_path),
            call.perform_idp_login(page, creds),
        ]
        # After a fresh login the target URL is re-navigated to, in case the
        # login flow lands back on a generic page rather than the target.
        assert page.goto.call_args_list == [
            (("https://github.com/owner/repo/pull/7",), {"wait_until": "domcontentloaded"}),
            (("https://github.com/owner/repo/pull/7",), {"wait_until": "domcontentloaded"}),
        ]
        context.close.assert_called_once_with()

    def test_checks_authentication_on_the_target_url(self, tmp_path) -> None:
        page = MagicMock()
        page.url = "https://github.com/owner/repo/pull/7"
        page.locator.return_value.count.return_value = 0
        page.locator.return_value.get_attribute.return_value = "expected-user"
        context = MagicMock()
        context.pages = [page]
        playwright = MagicMock()
        playwright.chromium.launch_persistent_context.return_value = context
        factory = MagicMock()
        factory.return_value.start.return_value = playwright

        with (
            patch.object(browser_apply_autofix, "_require_sync_playwright", return_value=factory),
            patch.object(browser_apply_autofix, "_profile_lock", _noop_lock),
            patch.object(browser_apply_autofix, "perform_idp_login") as mock_login,
        ):
            with browser_apply_autofix._authenticated_page(
                target_url="https://github.com/owner/repo/pull/7",
                profile_dir=tmp_path,
            ) as yielded:
                assert yielded is page

        page.goto.assert_called_once_with("https://github.com/owner/repo/pull/7", wait_until="domcontentloaded")
        mock_login.assert_not_called()
        page.locator.return_value.get_attribute.assert_called_once_with("content")

    def test_serializes_access_with_the_profile_lock(self, tmp_path) -> None:
        page = MagicMock()
        page.url = "https://github.com/"
        page.goto.side_effect = lambda url, **_kwargs: setattr(page, "url", url)
        page.locator.return_value.count.return_value = 0
        page.locator.return_value.get_attribute.return_value = "expected-user"
        context = MagicMock()
        context.pages = [page]
        playwright = MagicMock()
        playwright.chromium.launch_persistent_context.return_value = context
        factory = MagicMock()
        factory.return_value.start.return_value = playwright

        mock_lock = MagicMock(wraps=_noop_lock)
        with (
            patch.object(browser_apply_autofix, "_require_sync_playwright", return_value=factory),
            patch.object(browser_apply_autofix, "_profile_lock", mock_lock),
        ):
            with browser_apply_autofix._authenticated_page(
                target_url="https://github.com/owner/repo/pull/7",
                profile_dir=tmp_path,
            ):
                pass

        mock_lock.assert_called_once_with(tmp_path)

    @pytest.mark.parametrize("actual_user", [None, "other-user"])
    def test_rejects_a_different_authenticated_account(self, tmp_path, actual_user) -> None:
        page = MagicMock()
        page.url = "https://github.com/owner/repo/pull/7"
        page.locator.return_value.count.return_value = 0
        page.locator.return_value.get_attribute.return_value = actual_user
        context = MagicMock()
        context.pages = [page]
        playwright = MagicMock()
        playwright.chromium.launch_persistent_context.return_value = context
        factory = MagicMock()
        factory.return_value.start.return_value = playwright

        with (
            patch.object(browser_apply_autofix, "_require_sync_playwright", return_value=factory),
            patch.object(browser_apply_autofix, "_profile_lock", _noop_lock),
        ):
            with pytest.raises(BrowserCredentialError, match="account does not match"):
                with browser_apply_autofix._authenticated_page(
                    target_url="https://github.com/owner/repo/pull/7",
                    profile_dir=tmp_path,
                ):
                    pytest.fail("identity mismatch must not yield the page")

        context.close.assert_called_once_with()
        playwright.stop.assert_called_once_with()

    @pytest.mark.parametrize("target_url", ["https://github.com/other/repo/pull/7", "https://github.com/"])
    def test_rejects_a_different_target_organization(self, tmp_path, target_url) -> None:
        page = MagicMock()
        page.url = target_url
        page.locator.return_value.count.return_value = 0
        page.locator.return_value.get_attribute.return_value = "expected-user"
        context = MagicMock()
        context.pages = [page]
        playwright = MagicMock()
        playwright.chromium.launch_persistent_context.return_value = context
        factory = MagicMock()
        factory.return_value.start.return_value = playwright

        with (
            patch.object(browser_apply_autofix, "_require_sync_playwright", return_value=factory),
            patch.object(browser_apply_autofix, "_profile_lock", _noop_lock),
        ):
            with pytest.raises(BrowserCredentialError, match="organization does not match"):
                with browser_apply_autofix._authenticated_page(
                    target_url=target_url,
                    profile_dir=tmp_path,
                ):
                    pytest.fail("organization mismatch must not yield the page")

        context.close.assert_called_once_with()

    @pytest.mark.parametrize(
        ("expected_user", "expected_org"),
        [("", "owner"), ("expected-user", "")],
    )
    def test_requires_explicit_expected_identity(self, tmp_path, expected_user, expected_org) -> None:
        with (
            patch.dict(
                "os.environ",
                {
                    browser_apply_autofix.ENV_BROWSER_EXPECTED_GITHUB_USER: expected_user,
                    browser_apply_autofix.ENV_BROWSER_EXPECTED_GITHUB_ORG: expected_org,
                },
            ),
            patch.object(browser_apply_autofix, "_require_sync_playwright") as mock_require_playwright,
            patch.object(browser_apply_autofix, "_profile_lock") as mock_profile_lock,
        ):
            with pytest.raises(BrowserCredentialError, match="must be set"):
                with browser_apply_autofix._authenticated_page(
                    target_url="https://github.com/owner/repo/pull/7",
                    profile_dir=tmp_path,
                ):
                    pytest.fail("missing identity configuration must not yield the page")

        mock_require_playwright.assert_not_called()
        mock_profile_lock.assert_not_called()
