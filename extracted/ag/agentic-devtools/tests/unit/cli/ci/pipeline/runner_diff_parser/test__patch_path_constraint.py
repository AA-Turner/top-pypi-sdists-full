"""Tests for classifying patch path metadata."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _patch_path_constraint


def test_classifies_old_new_rename_and_file_mode_metadata() -> None:
    old_path = _patch_path_constraint("--- a/old.py")
    new_path = _patch_path_constraint("+++ b/new.py")
    rename_path = _patch_path_constraint("rename from old.py")
    file_mode = _patch_path_constraint("new file mode 100644")

    assert old_path is not None and old_path.kind == "old"
    assert new_path is not None and new_path.kind == "new"
    assert rename_path is not None and rename_path.path == "old.py"
    assert file_mode is not None and file_mode.kind == "file_mode"


def test_marks_invalid_paths_and_ignores_unrelated_metadata() -> None:
    invalid_path = _patch_path_constraint("--- x/file.py")

    assert invalid_path is not None and invalid_path.kind == "invalid"
    assert _patch_path_constraint("index 0123456..abcdef0") is None
