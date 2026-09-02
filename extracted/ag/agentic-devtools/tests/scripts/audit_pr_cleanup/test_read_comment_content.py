"""Unit tests for read_comment_content in scripts/audit_pr_cleanup.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.audit_pr_cleanup import read_comment_content


def test_read_comment_content_from_direct_string() -> None:
    """read_comment_content returns stripped direct comment text."""
    result = read_comment_content(comment="  This is an evaluation comment.  ")
    assert result == "This is an evaluation comment."


def test_read_comment_content_from_file(tmp_path: Path) -> None:
    """read_comment_content reads and strips content from an existing file."""
    comment_file = tmp_path / "comment.md"
    comment_file.write_text("## Evaluation Summary\nPR is valid.\n", encoding="utf-8")
    result = read_comment_content(comment_file=str(comment_file))
    assert result == "## Evaluation Summary\nPR is valid."


def test_read_comment_content_file_not_found(tmp_path: Path) -> None:
    """read_comment_content raises FileNotFoundError if file does not exist."""
    missing = tmp_path / "non_existent.md"
    with pytest.raises(FileNotFoundError, match="Comment file not found"):
        read_comment_content(comment_file=str(missing))


def test_read_comment_content_empty_file_raises_value_error(tmp_path: Path) -> None:
    """read_comment_content raises ValueError if file content is empty or whitespace only."""
    empty_file = tmp_path / "empty.md"
    empty_file.write_text("   \n\n  ", encoding="utf-8")
    with pytest.raises(ValueError, match="Comment file is empty"):
        read_comment_content(comment_file=str(empty_file))


def test_read_comment_content_empty_string_raises_value_error() -> None:
    """read_comment_content raises ValueError if direct comment string is empty or whitespace."""
    with pytest.raises(ValueError, match="Comment string cannot be empty"):
        read_comment_content(comment="   ")


def test_read_comment_content_no_arguments_raises_value_error() -> None:
    """read_comment_content raises ValueError if neither argument is provided."""
    with pytest.raises(ValueError, match="Either comment_file or comment must be provided"):
        read_comment_content(comment_file=None, comment=None)
