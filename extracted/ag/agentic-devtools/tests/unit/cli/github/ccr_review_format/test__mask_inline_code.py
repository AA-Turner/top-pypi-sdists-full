"""Tests for _mask_inline_code() in the CCR review-format parser."""

from agentic_devtools.cli.github.ccr_review_format import _mask_inline_code


class TestMaskInlineCode:
    """Tests for _mask_inline_code()."""

    def test_empty_text_returns_empty(self) -> None:
        assert _mask_inline_code("") == ""

    def test_text_without_code_spans_is_unchanged(self) -> None:
        text = "A plain review body with **bold** and a (2) count."
        assert _mask_inline_code(text) == text

    def test_offsets_are_preserved(self) -> None:
        text = "before `code span` after"
        assert len(_mask_inline_code(text)) == len(text)

    def test_span_content_is_blanked(self) -> None:
        assert _mask_inline_code("a `x` b") == "a     b"

    def test_multiple_spans_on_one_line_are_blanked(self) -> None:
        assert _mask_inline_code("`a` and `b`") == "    and    "

    def test_unterminated_backtick_does_not_swallow_the_rest(self) -> None:
        """A lone backtick must not blank the remainder of the body."""
        text = "a ` b\nSuppressed comments (2)"
        assert _mask_inline_code(text) == text

    def test_span_does_not_cross_a_newline(self) -> None:
        text = "`open\nclose`"
        assert _mask_inline_code(text) == text

    def test_double_backtick_span_is_blanked(self) -> None:
        assert _mask_inline_code("``a b``") == "       "

    def test_span_containing_a_shorter_backtick_run_is_fully_masked(self) -> None:
        """A shorter inner run does not close a longer inline-code span."""
        assert _mask_inline_code("``a`b``") == "       "
