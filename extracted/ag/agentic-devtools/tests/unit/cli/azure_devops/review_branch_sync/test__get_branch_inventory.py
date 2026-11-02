"""Tests for _get_branch_inventory."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_branch_sync import _get_branch_inventory


def test_falls_back_to_name_only_inventory_when_metadata_is_unavailable() -> None:
    with (
        patch(
            "agentic_devtools.cli.git.operations.get_branch_change_inventory",
            return_value=([], {}, {}, "main...HEAD", False),
        ),
        patch(
            "agentic_devtools.cli.git.operations.get_files_changed_on_branch",
            return_value=["src/file.py"],
        ) as get_files,
    ):
        result = _get_branch_inventory(save_files_on_branch=True)

    assert result == (["src/file.py"], {}, {}, "main...HEAD")
    get_files.assert_called_once_with()
