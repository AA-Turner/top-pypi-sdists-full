"""Tests for _refresh_artifact_commit_hash."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_branch_sync import _refresh_artifact_commit_hash


def test_refreshes_saved_scope_from_current_head_after_sync() -> None:
    with (
        patch(
            "agentic_devtools.cli.azure_devops.review_branch_sync.get_value",
            return_value="old-commit",
        ),
        patch(
            "agentic_devtools.cli.azure_devops.review_branch_sync._get_current_commit_hash",
            return_value="abcdef0123456789",
        ),
        patch("agentic_devtools.cli.azure_devops.review_branch_sync.set_value") as set_value,
    ):
        result = _refresh_artifact_commit_hash(True, True, False, None)

    assert result == "abcdef012345"
    set_value.assert_called_once_with("review.commit_hash_short", "abcdef012345")
