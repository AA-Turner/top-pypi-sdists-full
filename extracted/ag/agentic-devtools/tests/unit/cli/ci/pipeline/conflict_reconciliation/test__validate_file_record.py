"""Accepted file claims have a behavior and a syntactic content digest."""

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import _validate_file_record


def test_accepted_record(attestation):
    assert _validate_file_record(attestation.file_verdicts[0]) is None
