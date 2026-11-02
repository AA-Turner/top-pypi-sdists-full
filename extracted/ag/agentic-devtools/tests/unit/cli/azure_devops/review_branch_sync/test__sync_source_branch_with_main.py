"""Tests for _sync_source_branch_with_main."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_branch_sync import _sync_source_branch_with_main


def test_rebases_and_pushes_when_main_was_applied() -> None:
    rebase_result = type(
        "RebaseResultStub",
        (),
        {"is_success": True, "was_rebased": True, "needs_manual_resolution": False, "message": ""},
    )()
    with (
        patch("agentic_devtools.cli.git.operations.fetch_main", return_value=True),
        patch("agentic_devtools.cli.git.operations.rebase_onto_main", return_value=rebase_result),
        patch("agentic_devtools.cli.git.operations.force_push") as force_push,
    ):
        assert _sync_source_branch_with_main(dry_run=False) == (False, True)

    force_push.assert_called_once_with(dry_run=False)
