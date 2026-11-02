"""Tests for patch path constraints."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _patch_path_constraints


def test_ignores_unrelated_metadata_while_collecting_path_constraints() -> None:
    diff_lines = [
        "diff --git a/file.py b/file.py",
        "index 0123456..abcdef0",
        "--- a/file.py",
        "+++ b/file.py",
        "@@ -1 +1 @@",
    ]

    constraints = _patch_path_constraints(diff_lines, 0)

    assert constraints is not None
    assert constraints.old == "file.py"
    assert constraints.new == "file.py"
    assert not constraints.file_mode
