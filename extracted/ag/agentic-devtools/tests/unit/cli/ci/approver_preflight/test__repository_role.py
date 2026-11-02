"""Repository permissions never imply effective token review eligibility."""

import pytest

from agentic_devtools.cli.ci.approver_preflight import EvidenceStatus, _repository_role


@pytest.mark.parametrize(
    ("permissions", "role", "status"),
    [
        ({"admin": True}, "admin", EvidenceStatus.VERIFIED),
        ({"maintain": True}, "maintain", EvidenceStatus.VERIFIED),
        ({"push": True}, "write", EvidenceStatus.VERIFIED),
        ({"triage": True}, "triage", EvidenceStatus.DENIED),
        ({"pull": True}, "read", EvidenceStatus.DENIED),
        (dict.fromkeys(("admin", "maintain", "push", "triage", "pull"), False), None, EvidenceStatus.DENIED),
        ({}, None, EvidenceStatus.UNKNOWN),
        ({"push": "true"}, None, EvidenceStatus.UNKNOWN),
        (None, None, EvidenceStatus.UNKNOWN),
        ([], None, EvidenceStatus.UNKNOWN),
    ],
)
def test_role_evidence_is_separate_from_pat_grants(permissions, role, status) -> None:
    evidence = _repository_role({"permissions": permissions})
    assert evidence.value == role
    assert evidence.status is status
