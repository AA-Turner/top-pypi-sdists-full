"""Tests for _checkout_and_prepare_source_branch."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_branch_sync import _checkout_and_prepare_source_branch
from agentic_devtools.cli.git.operations import CheckoutResult


def test_checks_out_fetches_and_resets_source_branch() -> None:
    with (
        patch(
            "agentic_devtools.cli.git.operations.checkout_branch", return_value=CheckoutResult(CheckoutResult.SUCCESS)
        ),
        patch("agentic_devtools.cli.git.operations.fetch_branch", return_value=True) as fetch,
        patch("agentic_devtools.cli.git.operations.reset_branch_to_origin", return_value=True) as reset,
    ):
        assert _checkout_and_prepare_source_branch("feature/review", dry_run=False) == (True, None)

    fetch.assert_called_once_with("feature/review", dry_run=False)
    reset.assert_called_once_with("feature/review", dry_run=False)
