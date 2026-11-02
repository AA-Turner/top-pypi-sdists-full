"""Tests for checkout_and_sync_branch_async function."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops import async_commands
from agentic_devtools.cli.azure_devops.async_commands import checkout_and_sync_branch_async


class TestCheckoutAndSyncBranchAsync:
    """Tests for checkout_and_sync_branch_async function."""

    def test_function_exists(self):
        """Verify checkout_and_sync_branch_async is importable and callable."""
        assert callable(checkout_and_sync_branch_async)

    def test_dispatches_to_branch_sync_module(self):
        with (
            patch.object(async_commands, "get_value", return_value="123"),
            patch.object(async_commands, "run_function_in_background", return_value="task") as run_background,
            patch.object(async_commands, "print_task_tracking_info"),
        ):
            checkout_and_sync_branch_async()

        run_background.assert_called_once_with(
            "agentic_devtools.cli.azure_devops.review_branch_sync",
            "checkout_and_sync_branch_from_state",
            command_display_name="checkout-and-sync-branch",
        )
