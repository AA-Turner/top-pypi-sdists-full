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

    def test_empty_body_returns_empty_mask(self):
        """An empty body has no characters and yields an empty mask."""
        assert _compute_markdown_code_mask("") == []

    def test_plain_text_is_never_masked(self):
        """Text with no code markers is entirely unmasked."""
        body = "hello world\nsecond line"
        assert _compute_markdown_code_mask(body) == [False] * len(body)

    def test_inline_code_span_is_masked(self):
        """Characters inside a backtick span are masked, surrounding text is not."""
        body = "a `code` b"
        mask = _compute_markdown_code_mask(body)
        assert _masked_substring(body, "`code`")
        assert not mask[0]  # 'a'
        assert not mask[len(body) - 1]  # 'b'

    def test_unmatched_backtick_run_is_not_masked(self):
        """An opening backtick run with no matching closer is literal, not code."""
        body = "a `code without close"
        assert _compute_markdown_code_mask(body) == [False] * len(body)

    def test_mismatched_then_matched_backtick_runs(self):
        """A shorter run inside a double-backtick span does not close it."""
        body = "``x`y``"
        # The single backtick after x is not a closer; the trailing `` closes it.
        assert _masked_substring(body, "``x`y``")

    def test_short_backtick_run_is_not_a_fence(self):
        """A leading run of fewer than three backticks is not a code fence."""
        body = "``notafence <!-- z"
        mask = _compute_markdown_code_mask(body)
        # Not a fence: the '<!--' remains unmasked so the sanitizer can close it.
        assert not any(mask[mask_i] for mask_i in range(body.find("<!--"), len(body)))

    def test_fenced_block_masks_its_content(self):
        """A ``` fenced block masks the fence lines and everything between them."""
        body = "before\n```\n<!-- x\n```\nafter"
        assert _masked_substring(body, "<!-- x")
        mask = _compute_markdown_code_mask(body)
        assert not mask[0]  # 'before'
        assert not mask[len(body) - 1]  # 'after'

    def test_tilde_fence_masks_its_content(self):
        """A ~~~ fenced block masks its content just like a backtick fence."""
        body = "~~~\n<!-- t\n~~~"
        assert _masked_substring(body, "<!-- t")

    def test_open_fence_with_info_string_still_masks_content(self):
        """A fence opener may carry an info string (``` ```python ```)."""
        body = "```python\n<!-- p\n```"
        assert _masked_substring(body, "<!-- p")

    def test_different_delimiter_line_does_not_close_fence(self):
        """A ~~~ line inside a ``` fence is content, not a closing fence."""
        body = "```\n<!-- y\n~~~\n<!-- z\n```\nend"
        # Both markers stay inside the still-open backtick fence.
        assert _masked_substring(body, "<!-- y")
        assert _masked_substring(body, "<!-- z")

    def test_fence_line_with_trailing_text_does_not_close_fence(self):
        """A ``` line with trailing text is content, not a bare closing fence."""
        body = "```\n<!-- p\n```stuff\n<!-- q\n```\nend"
        assert _masked_substring(body, "<!-- p")
        assert _masked_substring(body, "<!-- q")
        mask = _compute_markdown_code_mask(body)
        assert not mask[len(body) - 1]  # 'end' after the real closer

    def test_unclosed_fence_masks_to_end_of_body(self):
        """A fence that never closes masks the remainder of the body."""
        body = "```\n<!-- open forever"
        assert _masked_substring(body, "<!-- open forever")

    def test_quoted_fenced_block_masks_its_content(self):
        """A blockquote-prefixed fence (``> ``` ``) is recognised and masks content."""
        body = "> ```\n> <!-- sample\n> ```\nafter"
        assert _masked_substring(body, "<!-- sample")
        mask = _compute_markdown_code_mask(body)
        assert not mask[len(body) - 1]  # 'after' is outside the fence

    def test_doubly_quoted_fenced_block_masks_content(self):
        """Nested blockquote prefixes (``> > `` ) are stripped before fence detection."""
        body = "> > ```\n> > <!-- deep\n> > ```\nend"
        assert _masked_substring(body, "<!-- deep")

    def test_quoted_fence_does_not_mask_outside_content(self):
        """Text before and after a quoted fenced block is not masked."""
        body = "before\n> ```\n> <!-- x\n> ```\nafter"
        mask = _compute_markdown_code_mask(body)
        assert not mask[0]  # 'before'
        assert not mask[len(body) - 1]  # 'after'

    def test_multiline_inline_code_span_is_masked(self):
        """A code span that crosses a newline within a paragraph masks its content.

        GitHub-Flavored Markdown joins a paragraph's lines before matching
        backtick runs, so ``\u0060a\\nb\u0060`` is a single code span. A ``<!--``
        inside it must therefore be masked and left untouched by the sanitizer.
        """
        body = "Use `<!-- x\ny` here."
        assert _masked_substring(body, "<!--")

    def test_blank_line_separates_inline_spans(self):
        """A blank line ends a paragraph, so backticks on either side do not pair.

        Two stray backticks in different paragraphs must not be treated as one
        span; a ``<!--`` after them stays unmasked so the sanitizer can close it.
        """
        body = "backtick `\n\nbacktick `\n<!-- real"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- real")
        assert not any(mask[i] for i in range(start, len(body)))

    def test_blank_blockquote_line_separates_inline_spans(self):
        """A bare ``>`` line (blank within a blockquote) ends the quoted paragraph."""
        body = "> backtick `\n>\n> backtick `\n<!-- real"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- real")
        assert not any(mask[i] for i in range(start, len(body)))

    def test_multiline_inline_span_in_blockquote_is_masked(self):
        """A multi-line code span inside a blockquote masks its ``<!--``."""
        body = "> Use `<!-- q\n> r` end"
        assert _masked_substring(body, "<!--")

    def test_inline_span_crossing_multiple_newlines_masks_interior(self):
        """A code span may cross several newlines; every interior newline is masked.

        Because the paragraph range handed to the matcher ends at the *last*
        content line's exclusive end, all inter-line newlines fall inside it, so
        a ``<!--`` two lines below its opener is still recognised as code.
        """
        body = "Use `<!-- x\nmid line\ny` here."
        assert _masked_substring(body, "<!--")
        mask = _compute_markdown_code_mask(body)
        for i, ch in enumerate(body):
            if ch == "\n":
                assert mask[i]  # interior newlines are inside the span

    def test_indented_code_block_after_blank_line_is_masked(self):
        """A 4-space-indented block (after a blank line) masks its ``<!--``.

        An indented code block renders its content literally, so a ``<!--``
        inside it cannot break rendering and must not be rewritten.
        """
        body = "intro\n\n    <!-- indented sample\n\nafter"
        assert _masked_substring(body, "<!--")
        mask = _compute_markdown_code_mask(body)
        assert not mask[0]  # 'intro'
        assert not mask[len(body) - 1]  # 'after'

    def test_tab_indented_code_block_is_masked(self):
        """A tab-indented block (after a blank line) is code and masks ``<!--``."""
        body = "intro\n\n\t<!-- tabbed\n\nafter"
        mask = _compute_markdown_code_mask(body)
        assert _masked_substring(body, "<!--")
        assert not mask[0]  # 'intro'
        assert not mask[len(body) - 1]  # 'after'

    def test_indented_line_continuing_paragraph_is_not_masked(self):
        """An indented line right after paragraph text is a lazy continuation.

        CommonMark forbids an indented code block from interrupting a paragraph,
        so ``    <!-- x`` on the line after ``text`` is normal text — its
        ``<!--`` is active HTML that must stay unmasked so it can be closed.
        """
        body = "text line\n    <!-- x"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!--")
        assert not any(mask[i] for i in range(start, len(body)))

    def test_indented_code_block_in_blockquote_is_masked(self):
        """A quoted 4-space-indented block masks its ``<!--`` content."""
        body = "> intro\n>\n>     <!-- quoted indented\n\nafter"
        mask = _compute_markdown_code_mask(body)
        assert _masked_substring(body, "<!--")
        assert not mask[len(body) - 1]  # 'after'

    def test_consecutive_indented_code_lines_are_masked(self):
        """Every line of a multi-line indented code block is masked."""
        body = "intro\n\n    line one\n    <!-- second\n\nafter"
        mask = _compute_markdown_code_mask(body)
        assert _masked_substring(body, "<!--")
        assert _masked_substring(body, "line one")  # earlier code line also masked
        assert not mask[0]  # 'intro'
        assert not mask[len(body) - 1]  # 'after'

    def test_indent_less_than_four_is_not_code(self):
        """Fewer than four leading spaces is not an indented code block."""
        body = "intro\n\n   <!-- three spaces"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!--")
        assert not any(mask[i] for i in range(start, len(body)))

    def test_backtick_fence_with_backtick_in_info_string_is_not_a_fence(self):
        """A backtick in a ``` fence's info string makes the line text, not a fence.

        CommonMark forbids a backtick in a backtick fence's info string, so
        ``` ```lang` ``` opens no block. A ``<!--`` on the following line stays
        active text and must remain unmasked so the sanitizer can close it.
        """
        body = "```lang`\n<!-- after"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- after")
        assert not any(mask[i] for i in range(start, len(body)))

    def test_tilde_fence_with_backtick_in_info_string_still_opens(self):
        """A ~~~ fence's info string may contain a backtick (no CommonMark limit)."""
        body = "~~~lang`\n<!-- t\n~~~"
        assert _masked_substring(body, "<!-- t")

    def test_four_space_indented_fence_does_not_close_block(self):
        """A closing fence indented four or more columns is content, not a closer.

        CommonMark allows a closing fence at most three columns of indentation, so
        a four-space-indented ``` line stays inside the block and later ``<!--``
        content remains masked.
        """
        body = "```\n<!-- x\n    ```\n<!-- y\n```\nend"
        assert _masked_substring(body, "<!-- x")
        assert _masked_substring(body, "<!-- y")
        mask = _compute_markdown_code_mask(body)
        assert not mask[len(body) - 1]  # 'end' after the real closer

    def test_three_space_indented_fence_closes_block(self):
        """A closing fence indented up to three columns still closes the block."""
        body = "```\n<!-- x\n   ```\nend"
        assert _masked_substring(body, "<!-- x")
        mask = _compute_markdown_code_mask(body)
        assert not mask[len(body) - 1]  # 'end' is outside the closed fence

    def test_four_space_indented_fence_opener_is_not_a_fence(self):
        """A fence opener indented four or more columns is literal text, not a fence.

        CommonMark requires at most three columns of indentation for a fence
        opener; a line such as ``text\\n    ```\\n<!-- cut off`` therefore does
        not open a code block, leaving the ``<!--`` unmasked (and closeable).
        """
        body = "text\n    ```\n<!-- cut off"
        assert not _masked_substring(body, "<!-- cut off")

    def test_three_space_indented_fence_opener_is_a_fence(self):
        """A fence opener indented at most three columns still opens a fence."""
        body = "\n   ```\n<!-- inside\n   ```\nafter"
        assert _masked_substring(body, "<!-- inside")
        mask = _compute_markdown_code_mask(body)
        assert not mask[len(body) - 1]  # 'after' is outside the closed fence

    def test_list_nested_fence_opener_is_measured_relative_to_item(self):
        """A fence under a list item opens when within three columns of its content.

        ``10. item`` has a content column of four, so a four-space-indented
        fence opener is zero columns into the item — a valid opener — and its
        ``<!--`` content is masked even though the absolute indent is four.
        """
        body = "10. item\n\n    ```\n    <!-- sample\n    ```\nafter"
        assert _masked_substring(body, "<!-- sample")
        mask = _compute_markdown_code_mask(body)
        assert not mask[len(body) - 1]  # 'after' is outside the closed fence

    def test_list_nested_fence_closer_is_measured_relative_to_item(self):
        """A fence under a list item closes when within three columns of its content.

        The closing fence at four absolute columns is zero columns into the
        ``10. item`` content column, so it closes the block and a later real
        ``<!--`` on an unindented line stays unmasked (and thus closeable).
        """
        body = "10. item\n\n    ```\n    <!-- sample\n    ```\n<!-- live"
        assert not _masked_substring(body, "<!-- live")

    def test_list_item_line_can_open_fence_as_its_first_block(self):
        """A fence immediately after a list marker is recognised inside the item."""
        body = "- ```\n  <!-- sample\n  ```\nafter"
        assert _masked_substring(body, "<!-- sample")
        mask = _compute_markdown_code_mask(body)
        assert not mask[len(body) - 1]  # 'after' is outside the closed fence

    def test_blockquote_context_change_flushes_paragraph(self):
        """A backtick that spans from normal text into a blockquote does not form a span.

        ``text \\`\\\\n> <!-- cut\\\\n> \\``` crosses from a normal paragraph into a
        blockquote. CommonMark containers are block-level; a code span cannot
        cross that boundary, so the backticks do not pair and the ``<!--`` inside
        the blockquote remains unmasked (and thus closeable by the sanitizer).
        """
        body = "text `\n> <!-- cut\n> `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_same_blockquote_depth_spans_paragraph(self):
        """A multi-line span stays masked when both lines share the same blockquote depth.

        Two consecutive lines inside the same blockquote level form one paragraph;
        a backtick span across them is valid and its ``<!--`` must be masked.
        """
        body = "> Use `<!-- q\n> r` end"
        assert _masked_substring(body, "<!--")

    def test_depth_increase_mid_paragraph_flushes(self):
        """Going from depth-0 to depth-1 mid-paragraph flushes and unblocks the ``<!--``.

        The stray opener backtick before the depth change can never pair with the
        closer inside the deeper blockquote; the ``<!--`` therefore stays unmasked.
        """
        body = "open `\n> <!-- here\n> close `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- here")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_heading_interrupts_paragraph_for_inline_spans(self):
        """An ATX heading starts a new block and breaks cross-line backtick pairing."""
        body = "text `\n# <!-- cut\n# `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_html_comment_opener_interrupts_paragraph(self):
        """A line-leading ``<!--`` HTML block opener interrupts the paragraph.

        ``text \\`\\n<!-- cut\\nTail \\``` would otherwise accumulate as one
        paragraph, pairing the two backticks and masking the real ``<!--``. The
        opener is a CommonMark HTML block start, so it flushes the paragraph and
        stays unmasked (and thus closeable by the sanitizer).
        """
        body = "text `\n<!-- cut\nTail `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_non_comment_html_block_start_interrupts_paragraph(self):
        """A line-leading HTML block start like ``<div>`` also interrupts the paragraph.

        ``text \\`\\n<div><!-- cut\\nTail \\``` must not be treated as one paragraph.
        ``<div>`` starts a CommonMark HTML block, so the prior paragraph flushes and
        the ``<!--`` stays unmasked.
        """
        body = "text `\n<div><!-- cut\nTail `"
        mask = _compute_markdown_code_mask(body)
        start = body.find("<!-- cut")
        assert not any(mask[i] for i in range(start, start + len("<!--")))

    def test_type7_html_tag_does_not_interrupt_paragraph(self):
        """A line-leading type-7 tag (e.g. ``<span>``) cannot interrupt a paragraph.

        CommonMark §4.6 restricts paragraph interruption to type-1 (``<pre>`` etc.)
        and type-6 (``<div>`` etc.) HTML blocks; type-7 open/close tags such as
        ``<span>`` may not interrupt. ``text \\`\\n<span><!-- cut\\ntail \\```
        therefore forms one multiline code span (``<span>`` stays in the paragraph),
        masking the ``<!--`` as harmless literal text. The sanitizer must not
        rewrite it.
        """
        body = "text `\n<span><!-- cut\ntail `"
        assert _masked_substring(body, "<!--")

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
