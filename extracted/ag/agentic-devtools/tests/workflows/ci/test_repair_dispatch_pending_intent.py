"""Regression tests for uncertain repair creation intent across pipeline stages."""

from typing import cast
from unittest.mock import patch

from agentic_devtools.cli.ci.evaluator.actions import agentic_fallback
from agentic_devtools.cli.ci.evaluator.models import PostAgentSnapshot, ThreadInfo
from agentic_devtools.cli.ci.models import IssueCommentInfo, ReviewCommentInfo
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import DispatchRepairAction
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider


class _Provider:
    def __init__(self, comment: ReviewCommentInfo) -> None:
        self.comments: list[IssueCommentInfo] = []
        self.review_comment = comment
        self.dispatch_calls = 0

    def get_pr_token_login(self) -> str:
        return "github-actions[bot]"

    def list_issue_comments(self, pr_number: int) -> list[IssueCommentInfo]:
        return self.comments.copy()

    def find_comment(self, pr_number: int, marker: str) -> tuple[int, str] | None:
        matches = [comment for comment in self.comments if marker in comment.body]
        if not matches:
            return None
        comment = max(matches, key=lambda item: item.id)
        return comment.id, comment.body

    def post_comment_as_pr_token(self, pr_number: int, body: str) -> int:
        return self.post_comment(pr_number, body)

    def post_comment(self, pr_number: int, body: str) -> int:
        comment_id = max((comment.id for comment in self.comments), default=0) + 1
        self.comments.append(IssueCommentInfo(comment_id, "github-actions[bot]", body))
        return comment_id

    def update_comment(self, comment_id: int, body: str) -> None:
        self.comments = [
            IssueCommentInfo(comment.id, comment.author, body if comment.id == comment_id else comment.body)
            for comment in self.comments
        ]

    def list_all_review_comments(self, pr_number: int) -> list[ReviewCommentInfo]:
        return [self.review_comment]

    def list_review_comments(self, pr_number: int, review_id: int) -> list[ReviewCommentInfo]:
        return [self.review_comment]

    def list_review_thread_states(self, pr_number: int) -> dict[int, tuple[bool, bool]]:
        return {}

    def dispatch_repair(self, **kwargs: object) -> str:
        self.dispatch_calls += 1
        if self.dispatch_calls == 1:
            raise RuntimeError("dispatch response was lost")
        return "task:confirmed"


def test_uncertain_evaluator_dispatch_remains_pending_during_pipeline_reconciliation() -> None:
    comment = ReviewCommentInfo(
        id=11,
        path="src/app.py",
        body="Fix this finding",
        html_url="https://example.test/comments/11",
        source_review_id=100,
    )
    provider = _Provider(comment)
    ci_provider = cast(CIPlatformProvider, provider)
    evaluator_result = agentic_fallback(
        ci_provider,
        PostAgentSnapshot(
            pr_number=42,
            current_head_sha="head",
            review_id=100,
            threads=(ThreadInfo(comment_id=11),),
        ),
    )
    pipeline_snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        ci_status="passing",
        review_state="CHANGES_REQUESTED",
        copilot_review_id=100,
    )

    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
        return_value=False,
    ):
        pipeline_result = DispatchRepairAction().execute(
            ci_provider, pipeline_snapshot, DerivedState(pipeline_snapshot)
        )

    assert evaluator_result.success is False
    assert evaluator_result.error_details is not None
    assert "dispatch response was lost" in evaluator_result.error_details
    assert pipeline_result.decision is ActionDecision.FAILED
    assert pipeline_result.error is not None
    assert "Unresolved repair creation" in pipeline_result.error
    assert provider.dispatch_calls == 1
