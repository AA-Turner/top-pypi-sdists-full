"""Typed evidence blocking order."""

from agentic_devtools.cli.ci.approver_preflight import (
    ApproverPreflightResult,
    CapabilityEvidence,
    EvidenceStatus,
)


class TestApproverPreflightResult:
    def test_verified_requirements_have_no_block(self) -> None:
        verified = CapabilityEvidence(EvidenceStatus.VERIFIED, "evidence")
        result = ApproverPreflightResult(verified, verified, verified, verified)
        assert result.blocking_capability is None
        assert result.authenticated_login == "evidence"

    def test_missing_identity_value_cannot_bypass_guard(self) -> None:
        verified = CapabilityEvidence(EvidenceStatus.VERIFIED)
        assert ApproverPreflightResult(identity=verified).blocking_capability == "identity"

    def test_denied_identity_with_value_still_blocks(self) -> None:
        evidence = CapabilityEvidence(EvidenceStatus.DENIED, "bot", 403)
        result = ApproverPreflightResult(identity=evidence)
        assert result.blocking_capability == "identity"
        assert result.authenticated_login is None
