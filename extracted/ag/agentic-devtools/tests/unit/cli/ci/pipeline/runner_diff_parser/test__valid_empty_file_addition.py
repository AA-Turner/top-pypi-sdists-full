"""Tests for validating empty-file additions."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _valid_empty_file_addition


def test_accepts_valid_empty_file_metadata() -> None:
    assert _valid_empty_file_addition("new.py", ["new file mode 100644", "index 0000000..e69de29"])


def test_rejects_wrong_destination_or_invalid_hashes() -> None:
    assert not _valid_empty_file_addition(
        "new.py",
        ["new file mode 100644", "index 0000000..e69de29", "--- /dev/null", "+++ b/other.py"],
    )
    assert not _valid_empty_file_addition("new.py", ["new file mode 100644", "index malformed"])
