"""Tests for the CCR recovered-path comparison key."""

from agentic_devtools.cli.github.ccr_review_format import ccr_path_match_key


def test_removes_zero_width_space_immediately_after_path_separator() -> None:
    assert ccr_path_match_key("src/\u200bfoo.py") == "src/foo.py"


def test_preserves_zero_width_space_inside_filename() -> None:
    assert ccr_path_match_key("src/foo\u200b.py") == "src/foo\u200b.py"
