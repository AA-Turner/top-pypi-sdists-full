"""Tests for _recover_missing_branch_files."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_prompt_generation import _recover_missing_branch_files


def test_appends_synthetic_records_for_missing_branch_files() -> None:
    files = [{"path": "src/known.py"}]
    with patch(
        "agentic_devtools.cli.azure_devops.review_prompt_generation._load_recovered_file_diff",
        return_value=(False, [], [], None),
    ) as load_diff:
        _recover_missing_branch_files(
            files,
            {},
            {"src/known.py", "src/missing.py"},
            {"src/known.py", "src/missing.py"},
            {"src/missing.py": "add"},
            {},
            "origin/main",
        )

    assert files[1]["path"] == "src/missing.py"
    assert files[1]["changeType"] == "add"
    assert files[1]["addedLines"] == []
    load_diff.assert_called_once_with("src/missing.py", "origin/main", "src/missing.py")
