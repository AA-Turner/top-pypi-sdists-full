"""Payload identity checks do not consult the provider."""

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import _validate_identities


def test_consistent_claim(attestation):
    assert _validate_identities(attestation) is None
