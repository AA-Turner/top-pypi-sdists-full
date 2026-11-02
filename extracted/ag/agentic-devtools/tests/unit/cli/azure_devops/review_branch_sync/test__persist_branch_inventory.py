"""Tests for _persist_branch_inventory."""

import json
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.review_branch_sync import _persist_branch_inventory


def test_persists_file_inventory_and_resolved_diff_base(tmp_path) -> None:
    with (
        patch(
            "agentic_devtools.cli.azure_devops.review_branch_sync.resolve_review_artifact_dir_name",
            return_value="PR42",
        ),
        patch("agentic_devtools.cli.azure_devops.review_branch_sync.get_state_dir", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.azure_devops.review_branch_sync.run_safe",
            return_value=MagicMock(returncode=0, stdout="merge-base-sha\n"),
        ) as run_safe,
    ):
        _persist_branch_inventory(42, {"src/a.py"}, {"src/a.py": "edit"}, {}, "main...HEAD", "abc123")

    artifact = tmp_path / "pull-request-review" / "PR42" / "files-on-branch.json"
    assert json.loads(artifact.read_text(encoding="utf-8")) == {
        "files": ["src/a.py"],
        "change_types": {"src/a.py": "edit"},
        "rename_sources": {},
        "diff_base_ref": "merge-base-sha",
    }
    run_safe.assert_called_once()
