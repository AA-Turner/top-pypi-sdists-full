"""Tests for _list_item_content_indent()."""

from agentic_devtools.cli.ci.evaluator.snapshot import _list_item_content_indent


class TestListItemContentIndent:
    """Measure list-item content columns for Markdown masking."""

    def test_returns_none_for_non_list_line(self):
        """A line without a list marker has no list-item content indent."""
        assert _list_item_content_indent("plain text", 0) is None
