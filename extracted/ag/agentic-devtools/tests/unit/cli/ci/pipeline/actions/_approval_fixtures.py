"""Shared approval gate fixtures, kept outside the class-symbol test budget."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_HAS_COMMENTS,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


def _clean_verdict(review_id: int = 1) -> CopilotGateVerdict:
    """Build a passing gate verdict for use in tests."""
    return CopilotGateVerdict(passed=True, reason="clean", review_id=review_id)


def _failing_verdict(reason: str = REASON_HAS_COMMENTS, details: str = "test block") -> CopilotGateVerdict:
    """Build a failing gate verdict for use in tests."""
    return CopilotGateVerdict(passed=False, reason=reason, details=details)


def _provider_for_snapshot(snapshot: PRStateSnapshot) -> MagicMock:
    """Return a provider mock whose live HEAD matches the snapshot."""
    provider = MagicMock()
    provider.get_pr_metadata.return_value.head_sha = snapshot.head_sha
    return provider


def _suppressed_only_verdict(
    review_id: int = 5,
    *,
    reason: str = REASON_SUPPRESSED_COMMENTS,
) -> CopilotGateVerdict:
    """Build a suppressed-only blocking verdict (0 posted, suppressed > 0)."""
    return CopilotGateVerdict(
        passed=False,
        reason=reason,
        review_id=review_id,
        body_comment_count=0,
        suppressed_count=2,
        details="suppressed/low-confidence comment(s)",
    )


def _suppressed_snapshot(
    *,
    verdict: CopilotGateVerdict,
    repair_satisfied_review_id: int | None,
    head_changed_since_review: bool = False,
    unresolved_threads: int = 0,
    repairable_threads: int = 0,
) -> PRStateSnapshot:
    return PRStateSnapshot(
        pr_number=1,
        has_approval_on_head=False,
        ci_status="passing",
        review_state="APPROVED",
        copilot_review_id=5,
        copilot_review_inline_count=0,
        unresolved_threads=unresolved_threads,
        repairable_threads=repairable_threads,
        copilot_gate_verdict=verdict,
        repair_satisfied_review_id=repair_satisfied_review_id,
        head_changed_since_review=head_changed_since_review,
    )
