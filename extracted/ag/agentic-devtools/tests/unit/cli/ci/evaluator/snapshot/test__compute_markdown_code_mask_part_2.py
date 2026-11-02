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
