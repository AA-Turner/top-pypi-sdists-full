"""Tests for parsing Git diff path pairs."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _git_header_pairs


def test_reads_quoted_and_ambiguous_unquoted_path_pairs() -> None:
    assert _git_header_pairs('"a/file.py" "b/file.py"') == [("a/file.py", "b/file.py")]
    pairs = _git_header_pairs("a/dir b/name.py b/dir b/name.py")

    assert pairs is not None
    assert ("a/dir b/name.py", "b/dir b/name.py") in pairs


def test_rejects_malformed_quoted_header() -> None:
    assert _git_header_pairs('"a/file.py"missing-space "b/file.py"') is None
