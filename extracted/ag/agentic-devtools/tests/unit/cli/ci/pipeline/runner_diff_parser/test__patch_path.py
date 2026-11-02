"""Tests for parsing unified-diff path headers."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _patch_path


def test_parses_tab_separated_and_null_paths() -> None:
    assert _patch_path("--- a/file.py\tdate", "--- ", "a/") == "file.py"
    assert _patch_path("--- /dev/null", "--- ", "a/") == "/dev/null"


def test_rejects_wrong_prefix_and_quoted_suffix() -> None:
    assert _patch_path("--- x/file.py", "--- ", "a/") is None
    assert _patch_path('--- "a/file.py" suffix', "--- ", "a/") is None
