"""Evidence defaults fail closed."""

from agentic_devtools.cli.ci.approver_preflight import CapabilityEvidence, EvidenceStatus


def test_default_evidence_is_unknown() -> None:
    assert CapabilityEvidence().status is EvidenceStatus.UNKNOWN
