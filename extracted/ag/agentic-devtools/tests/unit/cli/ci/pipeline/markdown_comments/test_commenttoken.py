"""Tests for the immutable CommentToken record."""

from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.cli.ci.pipeline.markdown_comments import CommentToken


def test_comment_token_preserves_all_declared_fields() -> None:
    token = CommentToken(line_number=7, column=3, kind="open")

    assert token.line_number == 7
    assert token.column == 3
    assert token.kind == "open"


def test_comment_token_is_immutable() -> None:
    token = CommentToken(line_number=1, column=0, kind="close")

    with pytest.raises(FrozenInstanceError):
        setattr(token, "kind", "open")
