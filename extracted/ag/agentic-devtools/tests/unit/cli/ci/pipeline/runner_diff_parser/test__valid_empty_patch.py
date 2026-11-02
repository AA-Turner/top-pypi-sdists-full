"""Tests for dispatching empty patch validation."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _valid_empty_patch


def test_dispatches_rename_addition_and_deletion_metadata() -> None:
    similarity = "similarity index 100%"
    assert _valid_empty_patch("new.py", [similarity, "rename from old.py", "rename to new.py"], "old.py", similarity)
    assert _valid_empty_patch("new.py", ["new file mode 100644", "index 0000000..e69de29"], "", "")
    assert _valid_empty_patch("old.py", ["deleted file mode 100644", "index e69de29..0000000"], "", "")


def test_rejects_unknown_empty_patch() -> None:
    assert not _valid_empty_patch("file.py", ["unsupported"], "", "")
