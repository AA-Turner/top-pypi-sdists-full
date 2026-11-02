"""Tests for _sanitize_unterminated_html_comments()."""

from agentic_devtools.cli.ci.evaluator.snapshot_comment_sanitization import _sanitize_unterminated_html_comments


class TestSanitizeUnterminatedHtmlComments:
    """Balance unterminated ``<!--`` sequences so they cannot break rendering."""

    def test_empty_string_unchanged(self):
        """An empty body has no comments and is returned unchanged."""
        assert _sanitize_unterminated_html_comments("") == ""

    def test_body_without_comment_unchanged(self):
        """A body with no ``<!--`` at all is returned verbatim."""
        text = "> quoted line\n\nFixed it."
        assert _sanitize_unterminated_html_comments(text) == text

    def test_wellformed_comment_untouched(self):
        """A properly terminated comment (e.g. the sentinel) is preserved verbatim."""
        text = "text <!-- copilot-agent-result --> more\nabc123 next"
        assert _sanitize_unterminated_html_comments(text) == text

    def test_unterminated_in_quoted_block_is_closed_at_line_end(self):
        """A cut-off marker inside a ``>`` block is closed so later lines render."""
        text = "> @copilot left a review.\n>\n> <!-- copilo\n\nFixed in the latest commit."
        result = _sanitize_unterminated_html_comments(text)
        assert result == "> @copilot left a review.\n>\n> <!-- copilo -->\n\nFixed in the latest commit."

    def test_unterminated_on_final_line_is_appended(self):
        """A cut-off marker on the last line gets the closer appended at the end."""
        text = "foo bar <!-- copilot-trigger:123"
        assert _sanitize_unterminated_html_comments(text) == "foo bar <!-- copilot-trigger:123 -->"

    def test_multiple_unterminated_each_closed(self):
        """Every unterminated marker on its own line is independently closed."""
        text = "<!-- a\nsome text <!-- b\nfinal"
        assert _sanitize_unterminated_html_comments(text) == "<!-- a -->\nsome text <!-- b -->\nfinal"

    def test_wellformed_then_unterminated(self):
        """A well-formed comment is skipped; a later unterminated one is closed."""
        text = "<!-- x --> ok\n> <!-- cut off\ntail line"
        assert _sanitize_unterminated_html_comments(text) == "<!-- x --> ok\n> <!-- cut off -->\ntail line"

    def test_truncated_opener_not_closed_by_later_comments_closer(self):
        """A ``-->`` that belongs to a later ``<!--`` does not close an earlier opener.

        This is the exact failure mode from cloud-agent replies: a truncated
        ``<!-- copilo`` opener is followed by ``<!-- copilot-agent-result -->``
        (the sentinel).  Without the intervening-opener check the sanitizer
        treats the sentinel's ``-->`` as closing the truncated opener, hides
        the sentinel inside the comment, and returns the malformed body unchanged.
        With the fix the truncated opener is closed on its own line so the
        sentinel stays visible.
        """
        text = "> <!-- copilo\n<!-- copilot-agent-result -->"
        result = _sanitize_unterminated_html_comments(text)
        # Truncated opener is closed at end of its line; sentinel is unaffected.
        assert result == "> <!-- copilo -->\n<!-- copilot-agent-result -->"
        # Sentinel is still present and well-formed in the output.
        assert "<!-- copilot-agent-result -->" in result

    def test_multiple_openers_on_one_line_are_each_closed(self):
        """Two openers on a single line each get their own closer.

        ``<!-- a <!-- b`` must not share one closer (``<!-- a <!-- b -->``);
        the first opener is closed just before the second so both are balanced.
        """
        result = _sanitize_unterminated_html_comments("<!-- a <!-- b")
        assert result == "<!-- a  --><!-- b -->"

    def test_three_openers_on_one_line_are_each_closed(self):
        """Every opener on a line is closed, not just the first."""
        result = _sanitize_unterminated_html_comments("<!-- a <!-- b <!-- c\ntail")
        assert result == "<!-- a  --><!-- b  --><!-- c -->\ntail"

    def test_unterminated_inside_inline_code_span_is_untouched(self):
        """A literal ``<!--`` inside an inline code span is never rewritten.

        Markdown renders code-span content verbatim, so an unterminated ``<!--``
        there does not break rendering. Because the sanitized body may be
        persisted back to the provider, rewriting it would corrupt a valid code
        sample in the comment.
        """
        text = "Use `<!-- marker` in code."
        assert _sanitize_unterminated_html_comments(text) == text

    def test_unterminated_inside_fenced_code_block_is_untouched(self):
        """A literal ``<!--`` inside a fenced code block is never rewritten."""
        text = "before\n```\n<!-- sample\n```\nafter"
        assert _sanitize_unterminated_html_comments(text) == text

    def test_unterminated_inside_quoted_fenced_block_is_untouched(self):
        """A literal ``<!--`` inside a *quoted* fenced block is never rewritten.

        A cloud-agent reply that includes a code sample in a quoted fenced block
        (``> ``` ``) should not have its ``<!--`` example corrupted.
        """
        text = "> ```\n> <!-- sample\n> ```\nafter"
        assert _sanitize_unterminated_html_comments(text) == text

    def test_code_sample_untouched_while_real_marker_is_closed(self):
        """An in-code ``<!--`` is preserved while a real unterminated one is closed."""
        text = "`<!-- keep` <!-- fix\ntail"
        result = _sanitize_unterminated_html_comments(text)
        assert result == "`<!-- keep` <!-- fix -->\ntail"

    def test_unterminated_inside_multiline_inline_span_is_untouched(self):
        """A ``<!--`` inside a code span that crosses a newline is not rewritten.

        GitHub joins a paragraph's lines before matching backticks, so
        ``\u0060<!-- x\\ny\u0060`` is one code span; the ``<!--`` inside renders as
        literal text and must be preserved when the sanitized body is persisted.
        """
        text = "Use `<!-- x\ny` here."
        assert _sanitize_unterminated_html_comments(text) == text

    def test_real_marker_after_blank_line_separated_backticks_is_closed(self):
        """Stray backticks in separate paragraphs do not hide a later marker.

        A blank line ends the paragraph, so the two stray backticks never form a
        span; the genuine unterminated ``<!--`` after them is still closed.
        """
        text = "backtick `\n\nbacktick `\n<!-- real"
        result = _sanitize_unterminated_html_comments(text)
        assert result == "backtick `\n\nbacktick `\n<!-- real -->"

    def test_unterminated_inside_span_crossing_multiple_lines_is_untouched(self):
        """A ``<!--`` inside a span crossing several newlines is preserved.

        The opener and closer are two lines apart, so the whole paragraph range
        (including both interior newlines) must be scanned for the span to be
        recognised and the ``<!--`` left untouched.
        """
        text = "Use `<!-- x\nmid line\ny` here."
        assert _sanitize_unterminated_html_comments(text) == text

    def test_unterminated_inside_indented_code_block_is_untouched(self):
        """A ``<!--`` inside a 4-space-indented code block is preserved.

        An indented code block (following a blank line) renders literally, so its
        ``<!--`` cannot break rendering and must survive persistence unchanged.
        """
        text = "intro\n\n    <!-- indented sample\n\nafter"
        assert _sanitize_unterminated_html_comments(text) == text

    def test_lazy_continuation_indented_marker_is_closed(self):
        """An indented ``<!--`` continuing a paragraph is still closed.

        CommonMark forbids an indented code block from interrupting a paragraph,
        so the indented line renders as normal text and its unterminated ``<!--``
        must be balanced with a closing ``-->``.
        """
        text = "text line\n    <!-- x"
        result = _sanitize_unterminated_html_comments(text)
        assert result == "text line\n    <!-- x -->"

    def test_result_is_always_balanced(self):
        """After sanitizing, every ``<!--`` has a matching ``-->`` following it."""
        text = "<!-- a\n<!-- b\nplain\n<!-- c -->\n<!-- d"
        result = _sanitize_unterminated_html_comments(text)
        idx = 0
        while True:
            open_idx = result.find("<!--", idx)
            if open_idx == -1:
                break
            close_idx = result.find("-->", open_idx + 4)
            assert close_idx != -1
            idx = close_idx + 3

    def test_result_has_no_opener_before_its_closer(self):
        """No opener shares a closer with a later opener on the same line.

        Verifies the strong balance property: scanning each ``<!--`` in order,
        its ``-->`` must appear before the next ``<!--`` — the exact guarantee a
        single shared closer (``<!-- a <!-- b -->``) would violate.
        """
        text = "x <!-- 1 <!-- 2\ny <!-- 3 <!-- 4"
        result = _sanitize_unterminated_html_comments(text)
        idx = 0
        while True:
            open_idx = result.find("<!--", idx)
            if open_idx == -1:
                break
            close_idx = result.find("-->", open_idx + 4)
            next_open = result.find("<!--", open_idx + 4)
            assert close_idx != -1
            assert next_open == -1 or next_open > close_idx
            idx = close_idx + 3
