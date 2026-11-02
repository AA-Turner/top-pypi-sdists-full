"""Tests for scanning raw HTML-comment delimiter tokens from one line."""

from typing import SupportsIndex

import pytest

from agentic_devtools.cli.ci.pipeline.markdown_comments import CommentToken, scan_comment_tokens


@pytest.mark.parametrize(
    ("line", "line_number", "expected"),
    [
        ("<!--", 1, (CommentToken(1, 0, "open"),)),
        ("-->", 2, (CommentToken(2, 0, "close"),)),
        ("", 3, ()),
        ("ordinary text", 4, ()),
        ("<!-- -->", 5, (CommentToken(5, 0, "open"), CommentToken(5, 5, "close"))),
        ("<!---->", 6, (CommentToken(6, 0, "open"), CommentToken(6, 4, "close"))),
        ("-->x<!--", 7, (CommentToken(7, 0, "close"), CommentToken(7, 4, "open"))),
        ("<!--<!--", 8, (CommentToken(8, 0, "open"), CommentToken(8, 4, "open"))),
        ("<!-->", 9, (CommentToken(9, 0, "open"),)),
        ("---->", 10, (CommentToken(10, 2, "close"),)),
        ("< !-- <!-> -- >", 11, ()),
        ("éx\t<!--", 12, (CommentToken(12, 3, "open"),)),
        ("``` <!-- --> ```", 13, (CommentToken(13, 4, "open"), CommentToken(13, 9, "close"))),
    ],
)
def test_scan_comment_tokens_reports_exact_nonoverlapping_delimiters(
    line: str,
    line_number: int,
    expected: tuple[CommentToken, ...],
) -> None:
    assert scan_comment_tokens(line, line_number) == expected


@pytest.mark.parametrize("line_number", [0, -1])
def test_scan_comment_tokens_rejects_nonpositive_line_number(line_number: int) -> None:
    with pytest.raises(ValueError, match="line_number must be a positive integer"):
        scan_comment_tokens("<!--", line_number)


def test_scan_comment_tokens_does_not_retain_context_between_calls() -> None:
    assert scan_comment_tokens("<!--", 20) == (CommentToken(20, 0, "open"),)
    assert scan_comment_tokens("-->", 21) == (CommentToken(21, 0, "close"),)


def test_scan_comment_tokens_bounds_absent_close_suffix_search_work() -> None:
    class TrackedLine(str):
        absent_close_work = 0

        def find(self, sub: str, start: SupportsIndex | None = 0, end: SupportsIndex | None = None, /) -> int:
            result = super().find(sub, start, end)
            if sub == "-->" and result == -1:
                self.absent_close_work += len(self[start:end])
            return result

    line = TrackedLine("<!--" * 64)

    assert scan_comment_tokens(line, 22) == tuple(CommentToken(22, column, "open") for column in range(0, len(line), 4))
    assert line.absent_close_work <= len(line)
