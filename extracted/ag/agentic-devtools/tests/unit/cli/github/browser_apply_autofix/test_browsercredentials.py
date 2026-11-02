"""Tests for the BrowserCredentials dataclass."""

from __future__ import annotations

from agentic_devtools.cli.github.browser_apply_autofix import BrowserCredentials


class TestBrowserCredentials:
    """Tests for BrowserCredentials."""

    def test_stores_fields(self) -> None:
        creds = BrowserCredentials(username="user@x", password="pw", totp_secret="SEED")
        assert creds.username == "user@x"
        assert creds.password == "pw"
        assert creds.totp_secret == "SEED"

    def test_equality(self) -> None:
        a = BrowserCredentials(username="u", password="p", totp_secret="s")
        b = BrowserCredentials(username="u", password="p", totp_secret="s")
        assert a == b
