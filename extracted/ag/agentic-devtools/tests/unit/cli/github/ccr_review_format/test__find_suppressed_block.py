"""Tests for _find_suppressed_block() in the CCR review-format parser."""

import pytest

from agentic_devtools.cli.github.ccr_review_format import _find_suppressed_block


class TestFindSuppressedBlock:
    """Tests for _find_suppressed_block()."""

    def test_no_block_returns_none(self) -> None:
        assert _find_suppressed_block("Just a plain review body.") is None

    def test_legacy_summary_block(self) -> None:
        body = (
            "<details>\n<summary>Comments suppressed due to low confidence (1)</summary>\n\n"
            "**a.py**: A finding\n\n</details>"
        )
        assert _find_suppressed_block(body) == "**a.py**: A finding"

    def test_empty_legacy_block_falls_through_to_heading(self) -> None:
        """An empty ``<details>`` block does not shadow a heading-anchored block."""
        body = (
            "<details>\n<summary>Suppressed comments (0)</summary>\n\n</details>\n\n"
            "### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n"
        )
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_nonzero_legacy_block_with_empty_body_falls_through_to_heading(self) -> None:
        """An empty ``(1)`` legacy block must not mask later anchored findings."""
        body = (
            "<details>\n<summary>Suppressed comments (1)</summary>\n\n</details>\n\n"
            "### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n"
        )
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_heading_nested_in_review_details_block(self) -> None:
        body = (
            "<details>\n<summary>Review details</summary>\n\n"
            "### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n\n</details>"
        )
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_h1_heading_is_found(self) -> None:
        body = "# Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n"
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_block_terminated_by_next_heading(self) -> None:
        body = "### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n\n### Other section\n\nnot part of it\n"
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_block_terminated_by_metrics_footer(self) -> None:
        body = (
            "### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n\n"
            "- **Files reviewed:** 1/1 changed files\n- **Comments generated:** 0 new\n"
        )
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_block_terminated_by_details_close(self) -> None:
        body = "### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n</details>\n\ntrailing prose"
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_block_runs_to_end_of_body_when_unterminated(self) -> None:
        body = "### Suppressed comments (1)\n\n**a.py:1**\n* A finding."
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_fenced_heading_does_not_terminate_the_block(self) -> None:
        body = "### Suppressed comments (1)\n\n**a.py:1**\n* Wrong heading:\n```\n### Not a real heading\n```\n"
        block = _find_suppressed_block(body)
        assert block is not None
        assert "### Not a real heading" in block

    def test_fenced_heading_is_not_a_block_anchor(self) -> None:
        """A suppressed heading inside a fenced excerpt never opens a block."""
        assert _find_suppressed_block("Prose.\n\n```\n### Suppressed comments (2)\n\n**a.py:1**\n```\n") is None

    def test_pseudo_backtick_fence_does_not_hide_later_heading(self) -> None:
        """A backtick run with backticks in its info string is not a real fence opener."""
        body = "`````example`````\n### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n"
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_empty_heading_block_returns_none(self) -> None:
        body = "### Suppressed comments (0)\n\n- **Files reviewed:** 3/3 changed files\n"
        assert _find_suppressed_block(body) is None

    def test_nonzero_anchor_with_empty_content_falls_through(self) -> None:
        """A nonzero ``(N)`` heading with no content before the terminator returns None."""
        body = "### Suppressed comments (1)\n\n### Other section\n\ncontent"
        assert _find_suppressed_block(body) is None

    def test_heading_with_trailing_qualifier_is_found(self) -> None:
        """The count regex constrains nothing after ``(N)``, so neither may this one.

        A heading the count reads but the block regex rejects is the same
        "declared > 0, entries = 0" stall swai-factory/agentic-devtools#3638 fixes.
        """
        body = "### Suppressed comments (1) — low confidence\n\n**a.py:1**\n* A finding."
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_heading_with_atx_closing_sequence_is_found(self) -> None:
        body = "### Suppressed comments (1) ###\n\n**a.py:1**\n* A finding."
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_crlf_heading_is_found(self) -> None:
        """A CRLF body must not hide the block behind the trailing ``\\r``."""
        body = "### Suppressed comments (1)\r\n\r\n**a.py:1**\r\n* A finding."
        assert _find_suppressed_block(body) == "**a.py:1**\r\n* A finding."

    def test_details_tag_with_attributes_is_found(self) -> None:
        """``<details open>`` is still a legacy block."""
        body = "<details open>\n<summary>Suppressed comments (1)</summary>\n\n**a.py**: A finding\n\n</details>"
        assert _find_suppressed_block(body) == "**a.py**: A finding"

    def test_bare_summary_without_details_is_found(self) -> None:
        """A ``<summary>`` the count reads must also open a block.

        The count regex anchors on ``<summary>`` regardless of its enclosing
        element, so the block anchor does too — otherwise a malformed or
        unrecognised wrapper is a "declared > 0, entries = 0" stall.
        """
        body = "<summary>Suppressed comments (1)</summary>\n\n**a.py:1**\n* A finding."
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_low_confidence_heading_without_the_word_suppressed_is_found(self) -> None:
        """The block anchor covers the low-confidence fallback the count uses."""
        body = "### Low confidence (1)\n\n**a.py:1**\n* A finding."
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_empty_first_declaration_falls_through_to_a_later_one(self) -> None:
        body = "### Suppressed comments (0)\n\n### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n"
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    def test_zero_declaration_with_nonempty_text_does_not_mask_later_nonzero(self) -> None:
        """A ``(0)`` heading followed by prose must not shadow a later ``(1)`` section."""
        body = (
            "### Suppressed comments (0)\n\nNo findings.\n\n"
            "### Suppressed comments (1)\n\n**a.py:1**\n* A real finding.\n"
        )
        assert _find_suppressed_block(body) == "**a.py:1**\n* A real finding."

    def test_zero_legacy_block_with_text_does_not_mask_later_nonzero(self) -> None:
        """A ``<summary>... (0)</summary>`` block with text must not shadow later findings."""
        body = (
            "<details>\n<summary>Suppressed comments (0)</summary>\n\nNo findings.\n\n</details>\n\n"
            "### Suppressed comments (1)\n\n**a.py:1**\n* A real finding.\n"
        )
        assert _find_suppressed_block(body) == "**a.py:1**\n* A real finding."

    def test_inline_code_containing_details_close_does_not_truncate_legacy_block(self) -> None:
        """A literal ``</details>`` inside inline code is content, not the block terminator."""
        body = (
            "<details>\n<summary>Suppressed comments (2)</summary>\n\n"
            "**a.py**: Mention the literal `` `</details>` `` in docs.\n"
            "**b.py**: Second finding.\n\n"
            "</details>"
        )
        assert (
            _find_suppressed_block(body)
            == "**a.py**: Mention the literal `` `</details>` `` in docs.\n**b.py**: Second finding."
        )

    def test_declaration_on_the_last_line_returns_none(self) -> None:
        """A declaration with no following line cannot have any content."""
        assert _find_suppressed_block("### Suppressed comments (1)") is None

    @pytest.mark.parametrize(
        "heading",
        [
            "### Unsuppressed comments (2)",
            "### Suppressed commentary (2)",
        ],
    )
    def test_counted_look_alike_heading_does_not_open_a_block(self, heading: str) -> None:
        """FR-006: counted look-alike headings are rejected by the anchor fallback.

        The legacy ``<details>`` path already rejects ``Unsuppressed`` and
        ``commentary`` via word-bounded regexes.  These cases exercise the
        ``_SUPPRESSED_ANCHOR_RE`` fallback path directly — the heading form
        has no ``<details>`` wrapper so only the anchor path applies.
        """
        body = f"{heading}\n\n**a.py:1**\n* A finding.\n"
        assert _find_suppressed_block(body) is None

    def test_mixed_case_and_extra_whitespace_summary_is_found(self) -> None:
        """``re.IGNORECASE`` plus a tolerant separator match a shouty, padded summary."""
        body = "<details>\n<summary>  SUPPRESSED   Comments (3)  </summary>\n\n**a.py:1**\n* A finding.\n\n</details>"
        assert _find_suppressed_block(body) == "**a.py:1**\n* A finding."

    @pytest.mark.parametrize(
        "summary",
        [
            "Resolved comments",
            "Outdated comments",
            "Unsuppressed comments",
            "Suppressed commentary",
            "Unsuppressed comments (2)",
            "Suppressed commentary (2)",
        ],
    )
    def test_unrelated_details_summary_does_not_open_a_block(self, summary: str) -> None:
        """FR-006: only a genuine suppressed-comment summary opens a legacy block.

        ``Unsuppressed`` and ``commentary`` are the boundary cases: without word
        boundaries the substrings ``suppressed`` and ``comment`` match inside
        them, so an unrelated ``<details>`` section would be handed to the repair
        agent as suppressed findings.  The counted variants (``(2)``) exercise
        the shared ``_SUPPRESSED_DECLARATION`` anchor that feeds both
        :func:`parse_suppressed_count` and the :data:`_SUPPRESSED_ANCHOR_RE`
        fallback path in :func:`_find_suppressed_block`: without word-boundaries
        on ``suppressed`` and ``comments?`` in that declaration, the fallback
        would still return the block content for ``Unsuppressed comments (2)``
        and ``Suppressed commentary (2)`` even though the legacy path correctly
        rejects them.
        """
        body = f"<details>\n<summary>{summary}</summary>\n\n**a.py:1**\n* A finding.\n\n</details>"
        assert _find_suppressed_block(body) is None
