"""Tests for ensure_azure_account function."""

from unittest.mock import patch

from agentic_devtools.cli.azure.auth import ensure_azure_account
from agentic_devtools.cli.azure.config import AzureAccount


class TestEnsureAzureAccount:
    """Tests for ensure_azure_account function."""

    def test_returns_true_when_correct_account_already_active(self):
        """Should return True immediately when the correct account is already active."""
        with patch(
            "agentic_devtools.cli.azure.auth.get_current_azure_account",
            return_value=("user.aza@company.com", "My Sub"),
        ):
            result = ensure_azure_account(AzureAccount.AZA, auto_switch=False)

        assert result is True

    def test_returns_false_when_not_logged_in_and_no_auto_switch(self):
        """Should return False when not logged in and auto_switch is disabled."""
        with patch(
            "agentic_devtools.cli.azure.auth.get_current_azure_account",
            return_value=None,
        ):
            result = ensure_azure_account(AzureAccount.AZA, auto_switch=False)

        assert result is False

    def test_switches_when_not_logged_in_and_auto_switch_is_enabled(self):
        """Should switch accounts when no account is active and auto_switch is enabled."""
        with (
            patch("agentic_devtools.cli.azure.auth.get_current_azure_account", return_value=None),
            patch("agentic_devtools.cli.azure.auth.switch_azure_account", return_value=True) as switch_account,
        ):
            result = ensure_azure_account(AzureAccount.AZA, auto_switch=True)

        assert result is True
        switch_account.assert_called_once_with(AzureAccount.AZA)

    def test_returns_false_when_wrong_account_and_no_auto_switch(self):
        """Should return False when a wrong account type is active and auto_switch=False."""
        with patch(
            "agentic_devtools.cli.azure.auth.get_current_azure_account",
            return_value=("normal.user@company.com", "My Sub"),
        ):
            result = ensure_azure_account(AzureAccount.AZA, auto_switch=False)

        assert result is False

    def test_switches_when_wrong_account_and_auto_switch_is_enabled(self):
        """Should switch accounts when the active account type does not match."""
        with (
            patch(
                "agentic_devtools.cli.azure.auth.get_current_azure_account",
                return_value=("normal.user@company.com", "My Sub"),
            ),
            patch("agentic_devtools.cli.azure.auth.switch_azure_account", return_value=True) as switch_account,
        ):
            result = ensure_azure_account(AzureAccount.AZA, auto_switch=True)

        assert result is True
        switch_account.assert_called_once_with(AzureAccount.AZA)
