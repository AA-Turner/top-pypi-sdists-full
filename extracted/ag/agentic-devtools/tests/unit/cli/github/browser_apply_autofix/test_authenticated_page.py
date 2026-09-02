"""Tests for _authenticated_page."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.github import browser_apply_autofix
from agentic_devtools.cli.github.browser_apply_autofix import BrowserCredentials


class TestAuthenticatedPage:
    """Tests for the _authenticated_page context manager."""

    def test_launches_logs_in_yields_and_cleans_up(self) -> None:
        page = MagicMock()
        context = MagicMock()
        context.new_page.return_value = page
        browser = MagicMock()
        browser.new_context.return_value = context
        playwright = MagicMock()
        playwright.chromium.launch.return_value = browser
        factory = MagicMock()
        factory.return_value.start.return_value = playwright
        creds = BrowserCredentials(username="u", password="p", totp_secret="s")

        with (
            patch.object(browser_apply_autofix, "_require_sync_playwright", return_value=factory),
            patch.object(browser_apply_autofix, "perform_idp_login") as mock_login,
        ):
            with browser_apply_autofix._authenticated_page(creds, headless=False) as yielded:
                assert yielded is page

        playwright.chromium.launch.assert_called_once_with(headless=False)
        mock_login.assert_called_once_with(page, creds)
        browser.close.assert_called_once_with()
        playwright.stop.assert_called_once_with()
