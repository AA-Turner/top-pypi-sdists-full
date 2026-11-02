"""Tests for _sanitize_unterminated_html_comments()."""

from agentic_devtools.cli.ci.evaluator.snapshot_comment_sanitization import _sanitize_unterminated_html_comments


class TestSanitizeUnterminatedHtmlComments:
    """Balance unterminated ``<!--`` sequences so they cannot break rendering."""

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
