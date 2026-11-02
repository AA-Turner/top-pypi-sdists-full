"""Tests for deciding when persisted critique state must be loaded."""

import pytest

from agentic_devtools.cli.ci.pipeline.critique_snapshot import should_load_issue_comment_critique_state
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_CLEAN,
    REASON_NEW_CCR_NOT_APPROVED,
    CopilotGateVerdict,
)


@pytest.mark.parametrize(
    ("passed", "reason", "headline", "expected"),
    [
        (True, REASON_CLEAN, "", False),
        (True, REASON_CLEAN, "Ready for human approval.", True),
        (False, REASON_NEW_CCR_NOT_APPROVED, "", True),
    ],
)
def test_loads_for_blocked_reviews_or_any_current_overview(
    passed: bool,
    reason: str,
    headline: str,
    expected: bool,
) -> None:
    verdict = CopilotGateVerdict(passed=passed, reason=reason, review_id=42)

    assert should_load_issue_comment_critique_state(verdict, headline) is expected
