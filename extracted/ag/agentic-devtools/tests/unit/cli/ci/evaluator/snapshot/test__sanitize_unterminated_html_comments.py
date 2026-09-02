"""Tests for _sanitize_unterminated_html_comments()."""

from agentic_devtools.cli.ci.evaluator.snapshot import _sanitize_unterminated_html_comments


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

    def test_backslash_escaped_opener_is_not_modified(self):
        r"""A ``\<!--`` (odd backslash run) is a CommonMark escape and is not rewritten.

        CommonMark's backslash-escape rule makes ``\<`` a literal ``<``, so
        ``\<!--`` renders as the text ``&lt;!--`` — not an HTML comment opener.
        The sanitizer must leave it untouched so a valid code example or
        documentation comment is not corrupted when the body is persisted.
        """
        text = r"\<!-- this is literal text"
        assert _sanitize_unterminated_html_comments(text) == text

    def test_double_backslash_before_opener_is_not_an_escape(self):
        r"""A ``\\<!--`` (even backslash run) renders ``\\`` + real comment opener.

        Two backslashes cancel each other out; the ``<`` is not escaped, so
        ``<!--`` after them is a genuine HTML comment opener and must be closed.
        """
        text = r"\\<!-- unterminated"
        result = _sanitize_unterminated_html_comments(text)
        assert result == r"\\<!-- unterminated -->"

    def test_triple_backslash_before_opener_is_an_escape(self):
        r"""A ``\\\<!--`` (three = odd backslashes) escapes the ``<``.

        The first two backslashes cancel each other out; the third escapes the
        ``<``, so ``<!--`` is literal text that must not be balanced.
        """
        text = r"\\\<!-- literal"
        assert _sanitize_unterminated_html_comments(text) == text

    def test_escaped_opener_followed_by_real_opener_closes_real_one(self):
        r"""An escaped ``\<!--`` is skipped; a later real ``<!--`` is still closed."""
        text = r"\<!-- ok" + "\n<!-- real"
        result = _sanitize_unterminated_html_comments(text)
        # The escaped one is unchanged; the real one gets a closer.
        assert r"\<!-- ok" in result
        assert "<!-- real -->" in result
        # The escaped one is NOT followed by ' -->'
        assert r"\<!-- ok -->" not in result

    def test_blockquote_context_change_does_not_mask_opener(self):
        """A ``<!--`` after a backtick span that crosses a blockquote depth change is closed.

        The depth change flushes the paragraph so the backticks never form a
        span; the ``<!--`` inside the blockquote is genuine and must be balanced.
        """
        text = "text `\n> <!-- cut\n> `"
        result = _sanitize_unterminated_html_comments(text)
        assert "<!-- cut -->" in result

    def test_heading_context_change_does_not_mask_opener(self):
        """A heading starts a new block so a cross-block backtick span cannot hide ``<!--``."""
        text = "text `\n# <!-- cut\n# `"
        result = _sanitize_unterminated_html_comments(text)
        assert "<!-- cut -->" in result

    def test_escaped_backtick_opener_does_not_mask_html_comment(self):
        r"""A ``\`` followed by ``<!--`` leaves the opener unmasked and closeable.

        CommonMark renders ``\`` as a literal backtick (backslash-escape rule),
        so the character sequence ``\` <!-- cut `` does NOT form a code span: the
        backtick after ``\`` is literal text, and the ``<!--`` that follows is a
        genuine HTML comment opener.  The mask must NOT treat ``\`` as a
        code-span delimiter, so the sanitizer correctly closes the ``<!--``.
        """
        # ``\` <!-- cut `` — first backtick is escaped (literal); the trailing
        # backtick has no closer, so the ``<!--`` is genuine and gets balanced.
        text = "\\` <!-- cut `\nFixed."
        result = _sanitize_unterminated_html_comments(text)
        # A closer must have been inserted — the ``<!--`` must not remain open.
        assert " -->" in result
        # The line containing the opener must end with the closer before the \n.
        first_line = result.split("\n")[0]
        assert first_line.endswith(" -->")

    def test_backslash_before_closer_masks_html_comment(self):
        r"""A span closed by a backslash-preceded backtick masks its ``<!--``.

        CommonMark backslash escapes do not apply inside a code span, so the next
        run of equal-length backticks closes the span even when preceded by
        ``\``.  The ``<!--`` between opener and closer is inside code and renders
        as literal text, so the sanitizer must leave it untouched (no ``-->``
        inserted).
        """
        # `` ` <!-- cut \` tail`` — opener at 0 is unescaped; the backtick at
        # position 12 (preceded by ``\``) closes the span, so ``<!--`` is inside
        # code and must not be balanced.
        text = "` <!-- cut \\` tail"
        result = _sanitize_unterminated_html_comments(text)
        # The comment is inside a code span — nothing is inserted.
        assert result == text

    def test_heading_backtick_does_not_mask_html_comment_in_following_paragraph(self):
        """A backtick inside an ATX heading cannot mask an ``<!--`` in following text.

        An ATX heading is a self-contained block (CommonMark §4.2); its content
        cannot continue into the next paragraph.  A backtick in the heading must
        not pair with a backtick in a later paragraph, which would falsely mask
        an ``<!--`` and leave it unsanitized.
        """
        # ``# heading `\\n<!-- cut\\ntail ``` — the heading contains a bare backtick;
        # ``<!-- cut`` follows in a normal paragraph, then a potential closer.
        # With the heading isolated the ``<!--`` must not be masked and must be closed.
        text = "# heading `\n<!-- cut\ntail `"
        result = _sanitize_unterminated_html_comments(text)
        assert "<!-- cut -->" in result

    def test_wellformed_comment_with_closer_inside_code_span_is_not_corrupted(self):
        r"""A ``-->`` inside a backtick code span still closes the HTML comment.

        CommonMark's inline HTML comment rule takes precedence over code-span
        rules: once ``<!--`` has opened an HTML comment the first raw ``-->``
        closes it, even if that ``-->`` is inside what would otherwise be a
        backtick code span.  The sanitizer must not treat such a body as
        unterminated and must leave it unchanged.
        """
        # <!-- text `-->` tail  — the --> at position 12 is inside a backtick
        # span per the code mask but is the real HTML-comment closer.
        text = "<!-- text `-->` tail"
        result = _sanitize_unterminated_html_comments(text)
        # Body is well-formed: no extra closer should be inserted.
        assert result == text

    def test_setext_underline_context_change_does_not_mask_opener(self):
        """A setext ``===`` underline starts a new block so ``<!--`` stays closeable.

        The underline turns the preceding line into a heading, breaking the
        cross-line backtick span; the intervening ``<!--`` is genuine and must
        be balanced rather than left to swallow the following reply.
        """
        text = "Heading `\n===\n<!-- cut\nTail `"
        result = _sanitize_unterminated_html_comments(text)
        assert "<!-- cut -->" in result

    def test_indented_opener_inside_list_item_is_closed(self):
        """A four-space ``<!--`` inside a list item is balanced, not treated as code.

        Under ``- item`` (content column two) the four-space line is an ordinary
        block, so its ``<!--`` is a real comment that must be closed so the
        trailing agent reply keeps rendering.
        """
        text = "- item\n\n    <!-- cut\n\nFixed in the latest commit."
        result = _sanitize_unterminated_html_comments(text)
        assert "<!-- cut -->" in result
        assert "Fixed in the latest commit." in result

    def test_non_one_ordered_marker_inside_paragraph_is_not_rewritten(self):
        """A ``2.`` line inside a paragraph stays inside the code span.

        Ordered lists only interrupt a paragraph when they start at ``1``.
        Here the ``<!--`` is literal inline-code content and must not gain a
        synthetic closer.
        """
        text = "text `abc\n2. <!-- literal\n`"
        assert _sanitize_unterminated_html_comments(text) == text

    def test_nested_list_exit_restores_parent_indent_for_sanitizer(self):
        """A continuation after a nested item uses the parent's content column.

        The four-space ``<!--`` remains ordinary text inside ``- outer`` after
        leaving ``- nested``, so the sanitizer must close it and keep the tail
        visible.
        """
        text = "- outer\n\n  - nested\n\n  outer text\n\n    <!-- cut\n\nTail"
        result = _sanitize_unterminated_html_comments(text)
        assert "    <!-- cut -->" in result
        assert result.endswith("\n\nTail")

    def test_list_scoped_fence_closes_when_line_exits_list_item(self):
        """A fence opened inside a list item closes when a line de-indents out of it.

        The fence opens at the item's content column (two). A later unindented
        line (``outside``) leaves the list container and implicitly closes the
        fence, so the following ``<!-- cut`` is a real unterminated opener that
        must be balanced rather than masked as code.
        """
        text = "- item\n\n  ```\n  code\noutside\n<!-- cut\n\nFixed in the latest commit."
        result = _sanitize_unterminated_html_comments(text)
        assert "<!-- cut -->" in result
        assert "Fixed in the latest commit." in result

    def test_list_item_line_fence_keeps_inline_code_sample_untouched(self):
        """A fence opened on the list-item line itself protects its literal ``<!--``."""
        text = "- ```\n  <!-- sample\n  ```\nafter"
        assert _sanitize_unterminated_html_comments(text) == text

    def test_blockquote_inside_list_preserves_parent_item_indent(self):
        """A nested blockquote does not close the enclosing list item.

        After the quoted line, the four-space ``<!--`` is still only two columns
        into ``- item`` and must be balanced rather than treated as top-level
        indented code.
        """
        text = "- item\n\n  > quote\n\n    <!-- cut\n\nTail"
        result = _sanitize_unterminated_html_comments(text)
        assert "    <!-- cut -->" in result
        assert result.endswith("\n\nTail")

    def test_blockquote_nested_list_does_not_leak_into_top_level_indented_code(self):
        """A list inside a blockquote does not stop later top-level code from staying literal."""
        text = "> - item\n>\n\n    <!-- literal"
        assert _sanitize_unterminated_html_comments(text) == text

    def test_tab_after_list_marker_uses_commonmark_column_width(self):
        """Tab padding after a list marker expands to the next four-column stop.

        In ``-\\titem`` the tab moves the content column to four, so a later
        six-space ``<!--`` line is only two columns into the item and must stay
        active HTML instead of being masked as indented code.
        """
        text = "-\titem\n\n      <!-- cut\n\nTail"
        result = _sanitize_unterminated_html_comments(text)
        assert "      <!-- cut -->" in result
        assert result.endswith("\n\nTail")

    def test_lazy_continuation_preserves_list_context_for_indented_opener(self):
        """A lazy continuation line does not close the enclosing list item.

        CommonMark allows an unindented paragraph line to continue inside a list
        item (lazy continuation); the four-space ``<!--`` on the following line is
        therefore only two columns past ``- item``'s content column and must be
        balanced rather than treated as top-level indented code.
        """
        text = "- item\nlazy continuation\n\n    <!-- cut\n\nTail"
        result = _sanitize_unterminated_html_comments(text)
        assert "    <!-- cut -->" in result
        assert result.endswith("\n\nTail")

    def test_indented_list_marker_is_not_pushed_as_list_context(self):
        """A four-space indented list marker at the top level is indented code.

        ``    - example <!-- literal`` is a top-level indented code block (four
        columns, no enclosing list item), not a list item opener.  It must NOT
        update the list-indent stack; if it did, a later ``    <!-- cut`` would
        be measured relative to the false item's content column and be left
        unmasked instead of being treated as indented code too.
        """
        # The opener itself is inside indented code and must not be rewritten;
        # the second indented line is also code and must not be rewritten.
        text = "    - example <!-- literal\n\n    <!-- cut\n\nTail"
        result = _sanitize_unterminated_html_comments(text)
        # Both indented lines are code and must be left untouched.
        assert "    - example <!-- literal" in result
        assert "    <!-- cut" in result
        # Neither indented line should gain a synthetic closer.
        assert "    - example <!-- literal -->" not in result
        assert "    <!-- cut -->" not in result
        assert result.endswith("\n\nTail")

    def test_thematic_break_is_not_pushed_as_list_context(self):
        """A thematic break (``- - -``) must not update the list-indent stack.

        CommonMark gives thematic breaks higher precedence than list items, so
        ``- - -`` must not be recognised as a list item.  If it were pushed, a
        later four-space code sample would be measured relative to the false
        item's content column and left unmasked instead of being treated as
        indented code.
        """
        # The opener is inside indented code and must not be rewritten.
        text = "- - -\n\n    <!-- cut\n\nTail"
        result = _sanitize_unterminated_html_comments(text)
        assert "    <!-- cut" in result
        # The indented line is top-level indented code and must not gain a closer.
        assert "    <!-- cut -->" not in result
        assert result.endswith("\n\nTail")
