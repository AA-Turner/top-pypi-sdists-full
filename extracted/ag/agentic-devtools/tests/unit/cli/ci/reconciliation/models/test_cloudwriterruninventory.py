"""Tests for cloud writer inventory completeness and cancellation boundaries."""

from agentic_devtools.cli.ci.reconciliation.models import CloudWriterRunInventory


def test_empty_inventory_is_explicitly_complete() -> None:
    result = CloudWriterRunInventory()
    assert result.runs == ()
    assert result.uncorrelated_runs == ()
    assert result.complete
    assert result.incomplete_reasons == ()
