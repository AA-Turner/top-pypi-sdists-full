from unittest.mock import MagicMock

from agentic_devtools.cli.ci.critique_adjudicator import (
    CritiqueAdjudication,
    build_adjudication_comment,
    build_critique_task_comment,
)
from agentic_devtools.cli.ci.models import IssueCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.critique_snapshot import load_critique_snapshot_fields
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_NEW_CCR_NOT_APPROVED, CopilotGateVerdict


def test_loads_current_task_followup_and_rebuttal_for_same_head() -> None:
    headline = "A concrete parser regression remains."
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    comments = [
        IssueCommentInfo(1, "github-actions[bot]", build_critique_task_comment(42, "head", 100, 1)),
        IssueCommentInfo(
            2,
            "github-actions[bot]",
            build_adjudication_comment(
                pr_number=42,
                head_sha="head",
                review_id=100,
                attempt=1,
                adjudication=CritiqueAdjudication(
                    verdict="needs_repair",
                    rationale="A code issue remains.",
                    concrete_instruction="Add a parser regression test.",
                ),
            ),
        ),
        IssueCommentInfo(
            3,
            "github-actions[bot]",
            build_adjudication_comment(
                pr_number=42,
                head_sha="head",
                review_id=99,
                attempt=1,
                adjudication=CritiqueAdjudication(verdict="rebutted", rationale="Covered by existing behavior."),
            ),
        ),
    ]
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    verdict = CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, body_comment_count=0)
    reviews = [
        ReviewInfo(99, "copilot[bot]", "COMMENTED", body, "head"),
        ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head"),
    ]

    fields = load_critique_snapshot_fields(
        provider, 42, comments, reviews, "head", verdict, headline, "approval_worthy"
    )

    assert fields.critique_headline_classification == "critique"
    assert fields.critique_followup_instruction == "Add a parser regression test."
    assert fields.critique_adjudicated_review_id == 99
    assert fields.critique_adjudicated_headline == headline


def test_attempt_two_prevents_reusing_the_first_followup_instruction() -> None:
    headline = "A concrete parser regression remains."
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    comments = [
        IssueCommentInfo(1, "github-actions[bot]", build_critique_task_comment(42, "head", 100, 2)),
        IssueCommentInfo(
            2,
            "github-actions[bot]",
            build_adjudication_comment(
                pr_number=42,
                head_sha="head",
                review_id=100,
                attempt=1,
                adjudication=CritiqueAdjudication(
                    verdict="needs_repair",
                    rationale="A code issue remains.",
                    concrete_instruction="Add a parser regression test.",
                ),
            ),
        ),
    ]
    fields = load_critique_snapshot_fields(
        provider,
        42,
        comments,
        [ReviewInfo(100, "copilot[bot]", "COMMENTED", "", "head")],
        "head",
        CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, body_comment_count=0),
        headline,
        "critique",
    )

    assert fields.critique_followup_instruction == ""
