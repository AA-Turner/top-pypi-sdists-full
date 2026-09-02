"""Tests for _interrupts_paragraph_with_list_item()."""

from agentic_devtools.cli.ci.evaluator.snapshot import _interrupts_paragraph_with_list_item


class TestInterruptsParagraphWithListItem:
    """Only paragraph-interrupting list items flush an active paragraph."""

    def test_non_list_line_does_not_interrupt(self):
        """A line without a list marker never interrupts a paragraph."""
        assert _interrupts_paragraph_with_list_item("plain text", in_list_context=False) is False

    def test_bullet_marker_interrupts(self):
        """A bullet-list item may interrupt a paragraph."""
        assert _interrupts_paragraph_with_list_item("- item", in_list_context=False) is True

    def test_ordered_one_interrupts(self):
        """An ordered list starting at ``1`` may interrupt a paragraph."""
        assert _interrupts_paragraph_with_list_item("1. item", in_list_context=False) is True

    def test_ordered_one_paren_interrupts(self):
        """An ordered ``1)`` item may interrupt a paragraph."""
        assert _interrupts_paragraph_with_list_item("1) item", in_list_context=False) is True

    def test_ordered_non_one_does_not_interrupt(self):
        """A non-``1`` ordered marker does not flush a top-level paragraph."""
        assert _interrupts_paragraph_with_list_item("2. item", in_list_context=False) is False

    def test_ordered_multidigit_starting_with_one_does_not_interrupt(self):
        """``14.`` starts with ``1`` but its start number is 14, so it must not interrupt."""
        assert _interrupts_paragraph_with_list_item("14. item", in_list_context=False) is False

    def test_ordered_ten_paren_does_not_interrupt(self):
        """``10)`` (start number 10) does not interrupt a paragraph."""
        assert _interrupts_paragraph_with_list_item("10) item", in_list_context=False) is False

    def test_non_one_ordered_in_list_context_interrupts(self):
        """Within an existing list, a later ``2.`` sibling still breaks accumulation."""
        assert _interrupts_paragraph_with_list_item("2. item", in_list_context=True) is True

    def test_ordered_leading_zero_one_interrupts(self):
        """``01.`` has numeric start value 1 and must interrupt a paragraph."""
        assert _interrupts_paragraph_with_list_item("01. item", in_list_context=False) is True

    def test_ordered_leading_zeros_one_paren_interrupts(self):
        """``001)`` has numeric start value 1 and must interrupt a paragraph."""
        assert _interrupts_paragraph_with_list_item("001) item", in_list_context=False) is True

    def test_ordered_leading_zero_non_one_does_not_interrupt(self):
        """``02.`` has numeric start value 2 and must not interrupt a paragraph."""
        assert _interrupts_paragraph_with_list_item("02. item", in_list_context=False) is False
