"""Tests for _compute_markdown_code_mask()."""

from agentic_devtools.cli.ci.evaluator.snapshot import _compute_markdown_code_mask


def _masked_substring(body: str, sub: str) -> bool:
    """Return True when every character of the first ``sub`` occurrence is masked."""
    start = body.find(sub)
    assert start != -1, f"{sub!r} not found in {body!r}"
    mask = _compute_markdown_code_mask(body)
    return all(mask[i] for i in range(start, start + len(sub)))


class TestComputeMarkdownCodeMask:
    """Mark Markdown fenced-block and inline-code-span positions."""

    def test_blockquote_fence_does_not_mask_unquoted_lines(self):
        """A fence opened inside a blockquote closes when the blockquote ends.

        In CommonMark a fenced block is scoped to its container (§4.5).  Leaving
        the blockquote (a depth change from 1 to 0) implicitly closes the fence.
        Lines outside the blockquote must *not* be masked — their ``<!--`` must
        remain closeable by the sanitizer.
        """
        # > ```\n> code\n<!-- cut off
        # The fence opens at depth 1; the third line has depth 0.
        # CommonMark closes the fence at the depth change, so ``<!-- cut off``
        # is unmasked text and should remain closeable.
        body = "> ```\n> code\n<!-- cut off"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut off")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_blockquote_list_context_does_not_survive_after_container_exit(self):
        """A list nested in a blockquote does not affect later top-level indented code."""
        body = "> - item\n>\n\n    <!-- literal"
        assert _masked_substring(body, "<!-- literal")

    def test_setext_equals_underline_breaks_backtick_pairing(self):
        """A setext ``===`` underline ends the paragraph like an ATX heading.

        CommonMark treats a paragraph line followed by ``===`` as a setext
        heading, so a backtick in the heading line cannot pair with one on a
        later paragraph line. Without this boundary the intervening ``<!--`` is
        falsely masked and the sanitizer leaves the rendering-breaking opener
        untouched.
        """
        body = "Heading `\n===\n<!-- cut\nTail `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_setext_double_dash_underline_breaks_backtick_pairing(self):
        """A two-character ``--`` setext underline also ends the paragraph."""
        body = "Heading `\n--\n<!-- cut\nTail `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_lone_dash_is_not_a_setext_underline(self):
        """A single ``-`` is a list bullet, not a setext underline.

        It must still be handled by list-item logic (a separate container), so a
        backtick before it cannot pair across into a following item's ``<!--``.
        """
        body = "open `\n- <!-- cut\n- close `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_indented_line_inside_list_item_is_not_code(self):
        """A four-space line inside a list item is an ordinary block, not code.

        Under ``- item`` the content column is two, so a four-space line is only
        two columns into the item — a paragraph, not an indented code block. Its
        ``<!--`` must stay unmasked so the sanitizer can close it.
        """
        body = "- item\n\n    <!-- cut"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!--")
        assert not any(mask[i] for i in range(start, len(body)))

    def test_deeply_indented_line_inside_list_item_is_code(self):
        """Four columns past the list item's content column is a code block.

        Under ``- item`` (content column two) a six-space line is four columns
        into the item — a genuine indented code block whose ``<!--`` is masked.
        """
        body = "- item\n\n      <!-- code"
        assert _masked_substring(body, "<!--")

    def test_ordered_list_item_content_indent_shifts_code_threshold(self):
        """An ordered marker widens the content column before the code threshold.

        ``10. item`` has a content column of four, so an eight-space line is four
        columns into the item (code) while a four-space line is not.
        """
        code_body = "10. item\n\n        <!-- code"
        assert _masked_substring(code_body, "<!--")
        text_body = "10. item\n\n    <!-- cut"
        mask = _compute_markdown_code_mask(text_body)
        start = text_body.find("<!--")
        assert not any(mask[i] for i in range(start, len(text_body)))

    def test_empty_list_item_content_indent_is_measured(self):
        """An empty list item (marker at end of line) still sets a content column."""
        body = "-\n\n    <!-- cut"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!--")
        assert not any(mask[i] for i in range(start, len(body)))

    def test_extra_spaces_after_marker_fall_back_to_content_column(self):
        """More than four spaces after a marker cap the content column at one.

        CommonMark treats the surplus indentation as code *within* the item, so
        the item's content column is marker width plus one (two for ``-``). A
        four-space line is then only two columns into the item (not code), while
        a six-space line is four columns in (a genuine indented code block).
        """
        text_body = "-      item\n\n    <!-- cut"
        mask = _compute_markdown_code_mask(text_body)
        start = text_body.find("<!--")
        assert not any(mask[i] for i in range(start, len(text_body)))
        code_body = "-      item\n\n      <!-- code"
        assert _masked_substring(code_body, "<!--")

    def test_lazy_continuation_preserves_list_context_for_indented_block(self):
        """A lazy continuation before a blank line preserves the list-item context.

        In ``- item\\nback\\n\\n    <!-- code``, ``back`` is a CommonMark lazy
        continuation of the paragraph in ``- item`` and does not exit the list
        item.  After the blank line, the four-space ``<!--`` is only two columns
        past the item's content column (two), which is insufficient for an
        indented code block inside the list, so it is live HTML and must remain
        unmasked.
        """
        body = "- item\nback\n\n    <!-- code"
        assert not _masked_substring(body, "<!--")

    def test_nested_list_exit_restores_parent_content_indent(self):
        """Leaving a nested item restores the parent item's content column.

        After exiting ``- nested`` the continuation line ``outer text`` is still
        inside ``- outer``, so a later four-space ``<!--`` is only two columns
        into the outer item and must remain unmasked (and closeable).
        """
        body = "- outer\n\n  - nested\n\n  outer text\n\n    <!-- cut"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, len(body)))

    def test_list_scoped_fence_closes_when_line_exits_list_item(self):
        """A fence opened in a list item does not mask text outside the item."""
        body = "- ```\n  <!-- literal\noutside <!-- cut"
        mask = _compute_markdown_code_mask(body)
        start = body.find("outside")

        assert not any(mask[i] for i in range(start, len(body)))
