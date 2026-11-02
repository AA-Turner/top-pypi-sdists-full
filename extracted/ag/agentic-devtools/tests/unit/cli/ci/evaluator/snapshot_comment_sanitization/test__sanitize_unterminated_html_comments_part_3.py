"""Tests for _sanitize_unterminated_html_comments()."""

from agentic_devtools.cli.ci.evaluator.snapshot_comment_sanitization import _sanitize_unterminated_html_comments


class TestSanitizeUnterminatedHtmlComments:
    """Balance unterminated ``<!--`` sequences so they cannot break rendering."""

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
