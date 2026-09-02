"""Tests for perform_idp_login."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.github import browser_apply_autofix
from agentic_devtools.cli.github.browser_apply_autofix import (
    SELECTOR_PASSWORD_INPUT,
    SELECTOR_TOTP_INPUT,
    SELECTOR_USERNAME_INPUT,
    BrowserCredentials,
    perform_idp_login,
)


class TestPerformIdpLogin:
    """Tests for perform_idp_login."""

    def test_drives_full_login_flow(self) -> None:
        page = MagicMock()
        creds = BrowserCredentials(username="user@x", password="pw", totp_secret="SEED")
        with (
            patch.object(browser_apply_autofix, "generate_totp", return_value="654321") as mock_totp,
            patch.object(browser_apply_autofix, "_github_enterprise_slug", return_value="swica"),
            patch.object(browser_apply_autofix, "_click_if_present") as mock_click,
        ):
            perform_idp_login(page, creds, base_url="https://gh.test")
        page.goto.assert_called_once_with("https://gh.test/enterprises/swica/sso")
        page.wait_for_url.assert_called_once_with("**login.microsoftonline.com/**")
        page.fill.assert_any_call(SELECTOR_USERNAME_INPUT, "user@x")
        page.fill.assert_any_call(SELECTOR_PASSWORD_INPUT, "pw")
        page.fill.assert_any_call(SELECTOR_TOTP_INPUT, "654321")
        mock_totp.assert_called_once_with("SEED")
        # Continue + Next + Sign in + Verify + Stay signed in
        assert mock_click.call_count == 5
