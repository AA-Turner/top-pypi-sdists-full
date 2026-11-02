"""Tests for validating file patch metadata and expected change counts."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _valid_file_patch


def test_accepts_complete_hunk_with_matching_change_count() -> None:
    assert _valid_file_patch("file.py", "file.py", ["@@ -1 +1 @@", "-old", "+new"], 2)


def test_rejects_empty_metadata_and_mismatched_change_counts() -> None:
    assert not _valid_file_patch("file.py", "file.py", [], 0)
    assert not _valid_file_patch("file.py", "file.py", ["@@ -1 +1 @@", "-old", "+new"], 1)
