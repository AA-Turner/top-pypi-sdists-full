"""Tests for _generate_file_queue_entries."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_prompt_generation import _generate_file_queue_entries


def test_creates_queue_entry_and_counts_file(tmp_path) -> None:
    prompt_path = tmp_path / "review-src-file.py.md"
    with (
        patch(
            "agentic_devtools.cli.azure_devops.review_prompt_generation._write_file_prompt", return_value=prompt_path
        ),
        patch(
            "agentic_devtools.cli.azure_devops.review_helpers.normalize_repo_path",
            side_effect=lambda path: path,
        ),
    ):
        generated, skipped, entries, skipped_files, filtered = _generate_file_queue_entries(
            tmp_path,
            [{"path": "src/file.py"}],
            [],
            None,
            set(),
            None,
            None,
        )

    assert generated == 1
    assert skipped == 0
    assert entries[0]["path"] == "src/file.py"
    assert entries[0]["promptPath"] == str(prompt_path)
    assert skipped_files == []
    assert filtered == [{"path": "src/file.py"}]
