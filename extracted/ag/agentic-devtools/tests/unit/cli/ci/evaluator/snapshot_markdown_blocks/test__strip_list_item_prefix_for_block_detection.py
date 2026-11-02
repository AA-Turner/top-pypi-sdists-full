"""Tests for _strip_list_item_prefix_for_block_detection()."""

from agentic_devtools.cli.ci.evaluator.snapshot_markdown_blocks import _strip_list_item_prefix_for_block_detection


class TestStripListItemPrefixForBlockDetection:
    """Expose the block-start text that follows a list marker."""

    def test_returns_original_text_for_non_list_line(self):
        """A non-list line is returned unchanged."""
        text = "plain text"

        assert _strip_list_item_prefix_for_block_detection(text, 0) == text

    def test_removes_marker_and_effective_padding(self):
        """Removes the list marker and up to four columns of padding."""
        assert _strip_list_item_prefix_for_block_detection("-    # heading", 0) == "# heading"

    def test_preserves_surplus_padding_as_nested_code(self):
        """Surplus padding remains after removing only one effective space."""
        assert _strip_list_item_prefix_for_block_detection("-      # code", 0) == "     # code"

    def test_returns_empty_text_for_empty_item(self):
        """An empty list item has no block-start content."""
        assert _strip_list_item_prefix_for_block_detection("-", 0) == ""
