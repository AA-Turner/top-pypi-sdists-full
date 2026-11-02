"""Tests for stable serialized inventory status values."""

from agentic_devtools.cli.ci.reconciliation.inventory_diagnostics import InventoryStatus


def test_inventory_status_serializes_typed_unknown():
    assert InventoryStatus.UNKNOWN == "unknown"
    assert InventoryStatus.COMPLETE == "complete"
