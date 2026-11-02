from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions import critique_task_binding
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_NEW_CCR_NOT_APPROVED, CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


def _snapshot(classification: str = "critique") -> PRStateSnapshot:
    body = "<!-- ccr-overview-v2 -->\n### Needs a closer look\n\nA parser regression remains.\n\n0 open findings"
    return PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        base_repo_full_name="owner/repo",
        effective_review_comment_count=0,
        effective_review_comment_count_review_id=100,
        effective_review_comment_filter_applied=False,
        reviews=[ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head")],
        copilot_gate_verdict=CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, body_comment_count=0),
        critique_headline_classification=classification,
    )


def _comment(comment_id: int) -> ReviewCommentInfo:
    return ReviewCommentInfo(
        id=comment_id,
        path="",
        body="",
        html_url="",
        source_review_id=100,
        author_login="",
        in_reply_to_id=None,
    )


@pytest.mark.parametrize(
    ("comments", "shortfall", "expected_shortfalls"),
    [([], 0, {}), ([_comment(-1)], 0, {100: 1}), ([], 2, {100: 2})],
)
def test_reconciles_eligible_prior_critique_attempt(
    comments: list[ReviewCommentInfo],
    shortfall: int,
    expected_shortfalls: dict[int, int],
) -> None:
    provider = MagicMock()
    ledger = MagicMock()
    expected = MagicMock()
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.RepairDispatchLedger",
            return_value=ledger,
        ) as make_ledger,
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.repair_work_key",
            return_value="work-key",
        ) as work_key,
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.reconcile_ledger_task_binding",
            return_value=expected,
        ) as reconcile,
    ):
        result = critique_task_binding.reconcile_before_attempt_skip(
            provider,
            _snapshot(),
            {"critique:100:1"},
            100,
            comments,
            shortfall,
            True,
            "dispatch_repair",
        )

    assert result is expected
    work_key.assert_called_once_with(100, comments, [], expected_shortfalls)
    make_ledger.assert_called_once_with(provider, 42, "head", 100, "work-key")
    reconcile.assert_called_once_with(provider, _snapshot(), {"critique:100:1"}, ledger, "dispatch_repair")


@pytest.mark.parametrize(
    ("snapshot", "review_id", "attempted", "body_only_work"),
    [
        (_snapshot(), 100, {"critique:100:1"}, False),
        (_snapshot("approval_worthy"), 100, {"critique:100:1"}, True),
        (_snapshot(), 101, {"critique:101:1"}, True),
        (_snapshot(), 100, {"review:100"}, True),
    ],
)
def test_skips_reconciliation_without_matching_body_only_attempt(
    snapshot: PRStateSnapshot,
    review_id: int,
    attempted: set[str],
    body_only_work: bool,
) -> None:
    with patch("agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.RepairDispatchLedger") as make_ledger:
        result = critique_task_binding.reconcile_before_attempt_skip(
            MagicMock(),
            snapshot,
            attempted,
            review_id,
            [],
            0,
            body_only_work,
            "dispatch_repair",
        )

    assert result is None
    make_ledger.assert_not_called()
