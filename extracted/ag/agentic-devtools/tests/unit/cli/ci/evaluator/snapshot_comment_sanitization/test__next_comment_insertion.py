"""Tests for _next_comment_insertion()."""

from agentic_devtools.cli.ci.evaluator.snapshot_comment_sanitization import _next_comment_insertion


def test_returns_none_when_no_comment_opener_exists() -> None:
    """Stops scanning when no comment opener remains."""
    body = "plain text"

    assert _next_comment_insertion(body, [False] * len(body), 0) is None


def test_skips_a_well_formed_comment() -> None:
    """Advances beyond a valid closer without requesting an insertion."""
    body = "<!-- complete -->"

    assert _next_comment_insertion(body, [False] * len(body), 0) == (None, len(body), False)


def test_reports_an_unterminated_final_line() -> None:
    """Requests a closing marker at the end of an unterminated final line."""
    body = "<!-- cut"

    assert _next_comment_insertion(body, [False] * len(body), 0) == (len(body), len(body), True)
