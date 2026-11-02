"""All original criterion IDs are required."""

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import _validate_criteria


def test_complete_criteria(attestation):
    assert _validate_criteria(attestation.criterion_verdicts) is None
