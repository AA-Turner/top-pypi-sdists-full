"""Tests for validating empty-file deletions."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _valid_empty_file_deletion


def test_accepts_empty_file_deletion() -> None:
    assert _valid_empty_file_deletion(["deleted file mode 100644", "index e69de29..0000000"])


def test_rejects_nonempty_or_malformed_deletion() -> None:
    assert not _valid_empty_file_deletion(["deleted file mode 100644", "index e69de29..1234567"])
    assert not _valid_empty_file_deletion(["deleted file mode 100644", "index malformed"])
