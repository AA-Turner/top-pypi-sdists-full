"""Lexical scanning for Markdown HTML-comment delimiter tokens."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CommentToken:
    """An HTML-comment delimiter and its position on one physical line."""

    line_number: int
    column: int
    kind: str


def scan_comment_tokens(line: str, line_number: int) -> tuple[CommentToken, ...]:
    """Return exact HTML-comment delimiters in source order for one line."""
    if line_number <= 0:
        raise ValueError("line_number must be a positive integer")

    tokens = []
    offset = 0
    while offset < len(line):
        if line.startswith("<!--", offset):
            tokens.append(CommentToken(line_number, offset, "open"))
            offset += 4
        elif line.startswith("-->", offset):
            tokens.append(CommentToken(line_number, offset, "close"))
            offset += 3
        else:
            offset += 1
    return tuple(tokens)
