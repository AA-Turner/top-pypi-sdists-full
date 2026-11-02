"""Tests for inline-code path-header detection."""

from agentic_devtools.cli.github.ccr_review_format import _ENTRY_HEADER_INLINE_RE, _is_inline_code_header


def test_detects_backticked_path_header() -> None:
    text = "`src/foo.py`: Finding body"
    match = _ENTRY_HEADER_INLINE_RE.match(text)

    assert match is not None
    assert _is_inline_code_header(text, match) is True


def test_does_not_mark_bold_path_header_as_inline_code() -> None:
    text = "**src/foo.py**: Finding body"
    match = _ENTRY_HEADER_INLINE_RE.match(text)

    assert match is not None
    assert _is_inline_code_header(text, match) is False
