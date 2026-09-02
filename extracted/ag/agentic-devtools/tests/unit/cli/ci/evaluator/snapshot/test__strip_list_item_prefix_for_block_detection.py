"""Tests for _strip_list_item_prefix_for_block_detection()."""

from agentic_devtools.cli.ci.evaluator.snapshot import _strip_list_item_prefix_for_block_detection


class TestStripListItemPrefixForBlockDetection:
    """Expose the block-start text that follows a list marker."""

    def test_returns_original_text_for_non_list_line(self):
        """A non-list line is returned unchanged."""
        text = "plain text"

        assert _strip_list_item_prefix_for_block_detection(text, 0) == text
