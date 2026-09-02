"""Tests for _mask_fenced_blocks() in the CCR review-format parser."""

from agentic_devtools.cli.github.ccr_review_format import _mask_fenced_blocks


class TestMaskFencedBlocks:
    """Tests for _mask_fenced_blocks()."""

    def test_empty_text_returns_empty(self) -> None:
        assert _mask_fenced_blocks("") == ""

    def test_text_without_fences_is_unchanged(self) -> None:
        text = "### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n"
        assert _mask_fenced_blocks(text) == text

    def test_offsets_are_preserved(self) -> None:
        """Masking must be length-preserving so matches can slice the original."""
        text = "before\n```\ncode **bold**\n```\nafter\n"
        masked = _mask_fenced_blocks(text)
        assert len(masked) == len(text)
        assert [len(line) for line in masked.split("\n")] == [len(line) for line in text.split("\n")]
        assert masked.split("\n") == ["before", "   ", " " * 13, "   ", "after", ""]

    def test_fenced_content_is_blanked(self) -> None:
        text = "**a.py:1**\n```\n### Heading (9)\n```\n**b.py:2**"
        masked = _mask_fenced_blocks(text)
        assert "### Heading (9)" not in masked
        assert "**a.py:1**" in masked
        assert "**b.py:2**" in masked

    def test_tilde_fences_are_masked(self) -> None:
        text = "~~~\n**Deliverable:** x\n~~~\nkept"
        masked = _mask_fenced_blocks(text)
        assert "**Deliverable:**" not in masked
        assert "kept" in masked

    def test_indented_fence_delimiter_is_recognised(self) -> None:
        """Up to three leading spaces are allowed on a fence delimiter."""
        text = "   ```\n**inside:** x\n   ```\nkept"
        masked = _mask_fenced_blocks(text)
        assert "**inside:**" not in masked
        assert "kept" in masked

    def test_shorter_inner_fence_does_not_close_a_longer_one(self) -> None:
        text = "````\n```\n**still inside:** x\n````\nkept"
        masked = _mask_fenced_blocks(text)
        assert "**still inside:**" not in masked
        assert "kept" in masked

    def test_different_delimiter_char_does_not_close_the_fence(self) -> None:
        text = "```\n~~~\n**still inside:** x\n```\nkept"
        masked = _mask_fenced_blocks(text)
        assert "**still inside:**" not in masked
        assert "kept" in masked

    def test_longer_closing_fence_closes_the_block(self) -> None:
        text = "```\nmasked\n`````\nkept"
        masked = _mask_fenced_blocks(text)
        assert "masked" not in masked
        assert "kept" in masked

    def test_unterminated_fence_masks_to_end_of_text(self) -> None:
        text = "kept\n```\n**a.py:1**\nstill inside"
        masked = _mask_fenced_blocks(text)
        assert masked.startswith("kept")
        assert "**a.py:1**" not in masked
        assert "still inside" not in masked

    def test_backtick_info_string_with_backtick_is_not_a_fence_opener(self) -> None:
        """A backtick fence opener is invalid when its info string contains backticks."""
        text = "`````example`````\n### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n"
        assert _mask_fenced_blocks(text) == text

    def test_tab_indented_fence_is_not_a_fence_opener(self) -> None:
        """A tab-indented fence delimiter is not valid CommonMark; the suppressed section must remain visible."""
        text = "\t```\n**inside:** x\n\t```\n### Suppressed comments (1)\n\n**a.py:1**\n* A finding.\n"
        masked = _mask_fenced_blocks(text)
        assert "### Suppressed comments (1)" in masked
        assert masked == text
