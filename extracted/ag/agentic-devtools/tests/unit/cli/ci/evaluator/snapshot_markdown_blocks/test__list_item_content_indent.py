"""Tests for _list_item_content_indent()."""

from agentic_devtools.cli.ci.evaluator.snapshot_markdown_blocks import _list_item_content_indent


class TestListItemContentIndent:
    """Measure list-item content columns for Markdown masking."""

    def test_returns_none_for_non_list_line(self):
        """A line without a list marker has no list-item content indent."""
        assert _list_item_content_indent("plain text", 0) is None

    def test_measures_bullet_and_ordered_item_content(self):
        """Content starts after the marker and its ordinary padding."""
        assert _list_item_content_indent("- item", 0) == 2
        assert _list_item_content_indent("12. item", 0) == 4

    def test_tab_padding_uses_visual_columns(self):
        """A tab after the marker advances to the next four-column stop."""
        assert _list_item_content_indent("-\titem", 0) == 4

    def test_excess_padding_and_empty_items_use_single_space(self):
        """Excess padding and empty items fall back to a one-column indent."""
        assert _list_item_content_indent("-      item", 0) == 2
        assert _list_item_content_indent("-", 0) == 2
