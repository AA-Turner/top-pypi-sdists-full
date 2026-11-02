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

    def test_indented_html_comment_opener_within_list_item_interrupts(self):
        """An ``<!--`` opener within three columns of a list item's content interrupts.

        Indentation is measured relative to the item's content column, so a
        ``<!--`` two columns into ``- item`` is still a block opener that flushes
        the paragraph and leaves the opener unmasked.
        """
        body = "- text `\n  <!-- cut\n  Tail `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_blockquote_lazy_continuation_keeps_span_masked(self):
        """A lazy blockquote continuation line stays in the same paragraph.

        CommonMark permits a blockquote paragraph to continue on a line that
        omits the ``>`` markers (lazy continuation), so ``> Use \\`<!-- q\\nr\\```
        is one paragraph and its code span masks the ``<!--``. A depth *decrease*
        must therefore not be treated as a block boundary.
        """
        body = "> Use `<!-- q\nr` end"
        assert _masked_substring(body, "<!--")

    def test_backslash_escaped_backtick_does_not_open_code_span(self):
        r"""A ``\`` (backslash + backtick) is a CommonMark escape, not a code-span opener.

        CommonMark's backslash-escape rule: ``\X`` (odd backslashes before
        ASCII punctuation) renders ``X`` literally.  A ``\`` followed by a
        backtick is therefore a literal backtick, not a code-span delimiter,
        and the characters following it — including any ``<!--`` — must remain
        unmasked.
        """
        # ``\` <!-- cut `` — the backtick after the backslash is escaped;
        # ``<!--`` is NOT inside a code span and must stay unmasked.
        body = "\\` <!-- cut `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!--")
        # The ``<!--`` must be unmasked so the sanitizer can close it.
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_backslash_before_closer_still_closes_code_span(self):
        r"""A backtick preceded by ``\`` still closes a code span.

        CommonMark backslash escapes do not apply inside a code span, so the
        next run of equal-length backticks closes the span even when preceded by
        a backslash.  The ``<!--`` between the opener and that closer is therefore
        inside code and must be masked (Markdown renders it as literal text, so
        the sanitizer must not rewrite it).
        """
        # `` ` <!-- cut \` tail`` — the opener at position 0 is unescaped and the
        # backtick at position 12 (preceded by ``\``) closes the span; ``<!--``
        # lies inside the span and must be masked.
        body = "` <!-- cut \\` tail"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!--")
        assert all(mask[i] for i in range(start, start + len("<!--")))

    def test_heading_content_cannot_pair_backtick_into_following_text(self):
        """A backtick inside an ATX heading cannot pair with a backtick on a later line.

        An ATX heading is a self-contained block (CommonMark §4.2): it cannot start
        or continue a paragraph, so a code-span opener inside the heading can never
        be closed by a backtick in subsequent text.  If that were allowed, an
        ``<!--`` between the opener and the following closer would be falsely masked
        and left unsanitized.
        """
        # ``# heading `\\n<!-- cut\\ntail ``` — the heading contains a bare
        # backtick, ``<!-- cut`` follows, then a closing backtick in normal text.
        # With the heading treated as an isolated block the backticks must NOT pair.
        body = "# heading `\n<!-- cut\ntail `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_heading_inside_list_uses_list_relative_indent_for_block_boundary(self):
        """A heading nested in a list item still breaks cross-line code-span pairing.

        Under ``10.`` the content column is four. An indented ``# heading`` at
        that same column is a real block boundary, so a later inline ``<!--``
        inside the list item must stay unmasked rather than being hidden by
        backticks paired across the heading line.
        """
        body = "10. text `\n    # heading\n    tail <!-- cut\n    more `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_heading_inline_code_span_is_masked(self):
        """An inline code span inside an ATX heading masks its own ``<!--``.

        Heading lines are self-contained blocks and must have their own inline spans
        masked so that a literal HTML-comment example inside backticks on the
        heading line (e.g. ``# Example: `<!-- foo``) is not left unmasked and then
        incorrectly closed by the sanitizer.
        """
        body = "# Example: `<!-- foo` bar"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- foo")
        # The ``<!--`` is inside backticks on the heading line and must be masked.
        assert all(mask[i] for i in range(start, start + len("<!--")))

    def test_list_item_continuation_keeps_multiline_span_masked(self):
        """A list item paragraph can continue on indented lines and keep one code span.

        The continuation line is ordinary text (it does not itself start a new
        block), so it stays in the item's paragraph and the code span spanning
        both lines masks the ``<!--`` in its interior.
        """
        body = "- Use `foo\n  sample <!-- x`\nend"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- x")
        assert all(mask[i] for i in range(start, start + len("<!--")))

    def test_backticks_do_not_pair_across_list_items(self):
        """Separate list items are distinct blocks; a code span cannot cross them.

        Each bullet-list item is its own CommonMark container block, so an
        unmatched backtick in one item cannot pair with a backtick in a later
        item.  A ``<!--`` in an intermediate item must therefore stay unmasked
        (and thus closeable by the sanitizer).
        """
        body = "- open `\n- <!-- cut\n- close `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_plain_list_item_flushes_active_paragraph(self):
        """A plain list item still breaks a paragraph before later backticks.

        Without the list-item paragraph flush, the opening backtick on the first
        line could pair with the closing backtick on the last line and mask the
        intervening real ``<!--``.
        """
        body = "open `\n- plain item\n<!-- cut\n`"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_backticks_do_not_pair_across_ordered_list_items(self):
        """Ordered list items are also distinct blocks and reset backtick pairing."""
        body = "1. open `\n2. <!-- cut\n3. close `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_non_one_ordered_marker_does_not_interrupt_paragraph(self):
        """A non-``1`` ordered marker cannot interrupt an active paragraph.

        CommonMark only lets an ordered list interrupt a paragraph when the
        marker starts at ``1``. A ``2.`` line inside an existing paragraph
        therefore stays in that paragraph, so its ``<!--`` remains inside the
        cross-line code span and stays masked.
        """
        body = "text `abc\n2. <!-- literal\n`"
        assert _masked_substring(body, "<!-- literal")
