"""Tests for Markdown path escape decoding."""

from agentic_devtools.cli.github.ccr_review_format import _unescape_markdown_path


def test_decodes_escaped_underscore() -> None:
    assert _unescape_markdown_path(r"src/foo\_bar.py") == "src/foo_bar.py"


def test_preserves_other_backslash_escapes() -> None:
    assert _unescape_markdown_path(r"src/foo\.py") == r"src/foo\.py"


def test_decodes_escaped_backslash_and_underscore_in_one_pass() -> None:
    assert _unescape_markdown_path(r"src/foo\\\_bar.py") == r"src/foo\_bar.py"
