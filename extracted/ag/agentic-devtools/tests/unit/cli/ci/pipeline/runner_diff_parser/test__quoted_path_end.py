"""Tests for quoted path terminator scanning."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _quoted_path_end


def test_finds_unescaped_closing_quote() -> None:
    header = r'"path\"with-quote.py"'

    assert _quoted_path_end(header, 0) == len(header) - 1


def test_rejects_unterminated_quoted_path() -> None:
    assert _quoted_path_end('"unfinished', 0) is None
