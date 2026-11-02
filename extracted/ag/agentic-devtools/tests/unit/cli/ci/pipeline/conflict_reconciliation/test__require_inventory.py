"""Inventory validation keeps canonical order."""

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import _require_inventory


def test_sorted_inventory():
    assert _require_inventory(("a", "b"), "duplicate_file") is None
