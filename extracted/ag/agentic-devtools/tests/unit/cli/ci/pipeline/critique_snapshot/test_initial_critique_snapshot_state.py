from types import SimpleNamespace
from unittest.mock import patch

from agentic_devtools.cli.ci.models import COPILOT_REVIEWER_LOGIN, ReviewInfo
from agentic_devtools.cli.ci.pipeline.critique_snapshot import initial_critique_snapshot_state
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_NEW_CCR_NOT_APPROVED, CopilotGateVerdict


def test_initial_state_carries_classifier_result() -> None:
    verdict = CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, body_comment_count=0)
    review = ReviewInfo(100, COPILOT_REVIEWER_LOGIN, "COMMENTED", "overview", "head")
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.critique_snapshot.parse_ccr_overview_summary",
            return_value=(True, "A defect remains."),
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.critique_snapshot.classify_critique_headline",
            return_value=SimpleNamespace(verdict="critique"),
        ),
    ):
        marker, headline, fields = initial_critique_snapshot_state(verdict, [review], "head", False, 0, 100, False)

    assert marker is None
    assert headline == "A defect remains."
    assert fields.critique_headline_classification == "critique"
