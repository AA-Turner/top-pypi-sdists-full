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
