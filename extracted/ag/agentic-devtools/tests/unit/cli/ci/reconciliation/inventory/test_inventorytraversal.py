"""Tests for InventoryTraversal."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.inventory import InventoryTraversal


def test_advance_updates_cursor_and_page_count() -> None:
    traversal = InventoryTraversal(cursor="c1", page_count=0, full_scan_complete=False)
    advanced = traversal.advance(next_cursor="c2")
    assert advanced.cursor == "c2"
    assert advanced.page_count == 1
    assert not advanced.full_scan_complete


def test_advance_marks_full_scan_complete_when_cursor_absent() -> None:
    traversal = InventoryTraversal(cursor="c1", page_count=0, full_scan_complete=False)
    advanced = traversal.advance(next_cursor=None)
    assert advanced.full_scan_complete
