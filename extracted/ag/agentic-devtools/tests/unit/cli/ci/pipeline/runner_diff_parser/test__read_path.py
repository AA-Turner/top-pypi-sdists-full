"""Tests for reading quoted and unquoted paths."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _read_path


def test_reads_quoted_and_unquoted_paths() -> None:
    quoted = '"quoted.py" extra'
    unquoted = "plain path.py"

    assert _read_path(quoted, 0) == ("quoted.py", quoted.index('"', 1) + 1)
    assert _read_path(unquoted, 0) == ("plain path.py", len(unquoted))


def test_rejects_missing_or_malformed_path() -> None:
    assert _read_path("", 0) is None
    assert _read_path('"unfinished', 0) is None
