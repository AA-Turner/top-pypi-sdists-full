from types import SimpleNamespace
from unittest.mock import patch

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.critique_gate import _block_prior_critique_carryover
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_AWAITING_FRESH,
    REASON_CLEAN,
    CopilotGateVerdict,
)


def test_block_prior_critique_carryover_requires_fresh_review_only_for_clean_critique() -> None:
    review = ReviewInfo(
        1,
        "copilot-pull-request-reviewer[bot]",
        "COMMENTED",
        "<!-- ccr-overview-v2 -->\n### Needs a closer look\nA parser regression remains unresolved.\n\n0 open findings",
        "prior",
    )
    clean = CopilotGateVerdict(True, REASON_CLEAN, review_id=1)
    blocked = CopilotGateVerdict(False, REASON_CLEAN, review_id=1)

    assert _block_prior_critique_carryover(blocked, review) is blocked
    with patch(
        "agentic_devtools.cli.ci.pipeline.critique_gate.classify_critique_headline",
        return_value=SimpleNamespace(verdict="critique"),
    ):
        result = _block_prior_critique_carryover(clean, review)

    assert result.passed is False
    assert result.reason == REASON_AWAITING_FRESH


def test_block_prior_critique_carryover_keeps_approval_worthy_and_non_overview_reviews() -> None:
    clean = CopilotGateVerdict(True, REASON_CLEAN, review_id=1)
    no_overview = ReviewInfo(1, "copilot", "COMMENTED", "Copilot generated no comments.", "prior")
    approval_body = (
        "<!-- ccr-overview-v2 -->\n### Needs a closer look\nOnly needs final human review.\n\n0 open findings"
    )
    approval_review = ReviewInfo(1, "copilot", "COMMENTED", approval_body, "prior")

    assert _block_prior_critique_carryover(clean, no_overview) is clean
    assert _block_prior_critique_carryover(clean, approval_review) is clean
