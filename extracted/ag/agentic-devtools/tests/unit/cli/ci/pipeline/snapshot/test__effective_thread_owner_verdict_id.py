"""Tests for _effective_thread_owner_verdict_id."""

from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_CLEAN, CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.snapshot import _effective_thread_owner_verdict_id


def test_effective_thread_owner_uses_verdict_review_id_when_verdict_is_none() -> None:
    """It falls back to the integer argument when the verdict object is omitted."""
    assert _effective_thread_owner_verdict_id(42, None) == 42
    assert _effective_thread_owner_verdict_id(0, None) is None


def test_effective_thread_owner_uses_verdict_when_available() -> None:
    """It extracts the review_id from the provided CopilotGateVerdict."""
    verdict = CopilotGateVerdict(passed=True, reason=REASON_CLEAN, review_id=84)
    assert _effective_thread_owner_verdict_id(42, verdict) == 84


def test_effective_thread_owner_reports_unknown_provenance_as_none() -> None:
    """An unknown or failed-closed verdict does not pretend a review id owns the thread."""
    verdict = CopilotGateVerdict(passed=False, reason=REASON_CLEAN, review_id=0)
    assert _effective_thread_owner_verdict_id(0, verdict) is None


def test_effective_thread_owner_does_not_fallback_when_verdict_is_unknown() -> None:
    """When a verdict is present but unknown, the legacy id must not override it."""
    verdict = CopilotGateVerdict(passed=False, reason=REASON_CLEAN, review_id=0)
    assert _effective_thread_owner_verdict_id(42, verdict) is None
