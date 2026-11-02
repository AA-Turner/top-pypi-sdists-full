"""Fail-closed, safe capability diagnostics."""

import pytest

from agentic_devtools.cli.ci.approver_preflight import (
    ApproverPreflightResult,
    CapabilityEvidence,
    EvidenceStatus,
)
from agentic_devtools.cli.ci.pipeline.actions.approval_entry import preflight_block
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, PipelineRunSummary
from agentic_devtools.cli.ci.pipeline.summary import render_summary_comment


@pytest.mark.parametrize(
    ("capability", "status", "http_status"),
    [
        ("identity", EvidenceStatus.MISSING, None),
        ("identity", EvidenceStatus.DENIED, 401),
        ("repository_visibility", EvidenceStatus.UNAVAILABLE, 404),
        ("repository_role", EvidenceStatus.DENIED, 200),
        ("repository_role", EvidenceStatus.UNKNOWN, None),
        ("review_eligibility", EvidenceStatus.UNKNOWN, None),
    ],
)
def test_first_unproven_required_capability_blocks_safely(capability, status, http_status) -> None:
    verified = CapabilityEvidence(EvidenceStatus.VERIFIED, "bot", 200)
    evidence = dict.fromkeys(("identity", "repository_visibility", "repository_role", "review_eligibility"), verified)
    evidence[capability] = CapabilityEvidence(status, http_status=http_status)
    result = preflight_block(ApproverPreflightResult(**evidence))
    assert result is not None
    assert result.decision is ActionDecision.BLOCKED
    assert result.capability == capability
    assert result.http_status == http_status
    assert capability in result.details
    assert status.value in result.details
    assert (
        "HTTP status unavailable" in result.details if http_status is None else f"HTTP {http_status}" in result.details
    )
    assert "bot" not in result.details


def test_optional_unsupported_provider_has_no_preflight_block() -> None:
    assert preflight_block(None) is None


def test_all_proven_capabilities_have_no_block() -> None:
    verified = CapabilityEvidence(EvidenceStatus.VERIFIED, "bot")
    assert preflight_block(ApproverPreflightResult(verified, verified, verified, verified)) is None


def test_existing_summary_renders_safe_capability_and_status_without_token() -> None:
    verified = CapabilityEvidence(EvidenceStatus.VERIFIED, "bot", 200)
    preflight = ApproverPreflightResult(
        identity=verified,
        repository_visibility=CapabilityEvidence(EvidenceStatus.UNAVAILABLE, http_status=404),
    )
    result = preflight_block(preflight)
    assert result is not None
    rendered = render_summary_comment(PipelineRunSummary(results=[result]))
    assert "repository_visibility" in rendered
    assert "HTTP 404" in rendered
    assert "unavailable" in rendered
    assert "blocked" in rendered
    assert "🚫" in rendered
    assert "credential" not in rendered
    assert "token" not in rendered
