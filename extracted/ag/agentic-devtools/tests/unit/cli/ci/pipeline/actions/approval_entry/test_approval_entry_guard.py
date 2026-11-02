"""Capability checks precede identity and live metadata checks."""

from unittest.mock import Mock

from agentic_devtools.cli.ci.approver_preflight import ApproverPreflightResult
from agentic_devtools.cli.ci.pipeline.actions.approval_entry import approval_entry_guard
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot


def test_preflight_blocks_without_live_metadata_reads() -> None:
    snapshot = PRStateSnapshot(approver_preflight=ApproverPreflightResult())
    derived = DerivedState(snapshot)
    provider = Mock()
    derived.set("provider", provider)
    result = approval_entry_guard(snapshot, derived)
    assert result is not None
    assert result.decision is ActionDecision.BLOCKED
    provider.get_pr_metadata.assert_not_called()


def test_legacy_provider_checks_live_head() -> None:
    snapshot = PRStateSnapshot(head_sha="old")
    derived = DerivedState(snapshot)
    provider = Mock()
    provider.get_pr_metadata.return_value.head_sha = "new"
    derived.set("provider", provider)
    result = approval_entry_guard(snapshot, derived)
    assert result is not None
    assert result.decision is ActionDecision.SKIP
    assert result.preconditions == {"live_head_matches_snapshot": False}


def test_matching_live_head_allows_further_evaluation() -> None:
    snapshot = PRStateSnapshot(head_sha="head")
    derived = DerivedState(snapshot)
    provider = Mock()
    provider.get_pr_metadata.return_value.head_sha = "head"
    derived.set("provider", provider)
    assert approval_entry_guard(snapshot, derived) is None


def test_no_provider_retains_legacy_evaluation() -> None:
    snapshot = PRStateSnapshot()
    assert approval_entry_guard(snapshot, DerivedState(snapshot)) is None
