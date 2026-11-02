"""Claimed files require exact coverage."""

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import _validate_files


def test_complete_inventory(attestation):
    assert _validate_files(attestation) is None
