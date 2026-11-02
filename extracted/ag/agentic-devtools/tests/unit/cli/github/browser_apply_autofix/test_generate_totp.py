"""Tests for generate_totp."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.github import browser_apply_autofix
from agentic_devtools.cli.github.browser_apply_autofix import generate_totp


class TestGenerateTotp:
    """Tests for generate_totp."""

    def test_generates_code_from_secret(self) -> None:
        fake_pyotp = MagicMock()
        fake_pyotp.TOTP.return_value.now.return_value = "123456"
        with patch.object(browser_apply_autofix, "_require_pyotp", return_value=fake_pyotp):
            assert generate_totp("SEED") == "123456"
        fake_pyotp.TOTP.assert_called_once_with("SEED")
