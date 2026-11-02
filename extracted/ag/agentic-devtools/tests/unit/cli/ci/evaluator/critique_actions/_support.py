"""Shared fixtures for critique adjudication action tests."""

from types import SimpleNamespace
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.critique_adjudicator import (
    CritiqueAdjudicationRecord,
    CritiqueTask,
    build_critique_task_comment,
)
from agentic_devtools.cli.ci.evaluator.models import CommentInfo, PostAgentSnapshot, ThreadInfo
from agentic_devtools.cli.ci.models import COPILOT_REVIEWER_LOGIN, IssueCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_NEW_CCR_NOT_APPROVED, CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


def _make_task(attempt: int = 1) -> CritiqueTask:
    return CritiqueTask(42, "head", 100, attempt, "2026-10-19T12:00:00Z")


def _make_snapshot(
    *,
    task: CritiqueTask | None = None,
    tasks: tuple[CritiqueTask, ...] = (),
    adjudications: tuple[CritiqueAdjudicationRecord, ...] = (),
    current_head_sha: str = "head",
) -> PostAgentSnapshot:
    return PostAgentSnapshot(
        pr_number=42,
        current_head_sha=current_head_sha,
        critique_task=task or _make_task(),
        critique_tasks=tasks,
        critique_headline="A concrete code defect remains.",
        critique_adjudications=adjudications,
        threads=(ThreadInfo(comment_id=8),),
    )


def _make_provider(*head_shas: str) -> MagicMock:
    provider = MagicMock()
    provider.get_pr_metadata.side_effect = [SimpleNamespace(head_sha=head) for head in head_shas]
    provider.post_comment_as_pr_token.return_value = 77
    return provider


def _make_needs_repair_dispatch_case() -> tuple[
    MagicMock,
    dict[int, IssueCommentInfo],
    PostAgentSnapshot,
    PRStateSnapshot,
]:
    headline = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
    review_body = f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"
    task = _make_task()
    comments = {
        1: IssueCommentInfo(
            id=1,
            author="github-actions[bot]",
            body=('<!-- repair-dispatch-findings:42:head:v1 -->\n{"attempted": ["critique:100:1"]}'),
        ),
        2: IssueCommentInfo(
            id=2,
            author="github-actions[bot]",
            body=build_critique_task_comment(42, "head", 100, 1),
        ),
    }
    provider = MagicMock()
    provider.get_pr_metadata.return_value = SimpleNamespace(head_sha="head")
    provider.get_pr_token_login.return_value = "github-actions[bot]"
    provider.list_issue_comments.side_effect = lambda _pr: list(comments.values())
    provider.list_review_comments.return_value = []
    provider.list_review_thread_states.return_value = {}

    def post_comment(pr_number: int, body: str) -> int:
        comment_id = max(comments, default=0) + 1
        comments[comment_id] = IssueCommentInfo(comment_id, "github-actions[bot]", body)
        return comment_id

    def update_comment(comment_id: int, body: str) -> None:
        comments[comment_id] = IssueCommentInfo(comment_id, "github-actions[bot]", body)

    def find_comment(_pr_number: int, marker: str) -> tuple[int, str] | None:
        return next(((comment.id, comment.body) for comment in comments.values() if marker in comment.body), None)

    def dispatch_repair(**_kwargs: object) -> str:
        assert not any("critique-adjudicated" in comment.body for comment in comments.values())
        return "task:owner/repo:77"

    provider.post_comment.side_effect = post_comment
    provider.post_comment_as_pr_token.side_effect = post_comment
    provider.update_comment.side_effect = update_comment
    provider.update_comment_as_pr_token.side_effect = update_comment
    provider.find_comment.side_effect = find_comment
    provider.dispatch_repair.side_effect = dispatch_repair

    post_agent_snapshot = PostAgentSnapshot(
        pr_number=42,
        repo="owner/repo",
        latest_agent_comment=CommentInfo(
            id=2,
            author="copilot-swe-agent[bot]",
            body="I reviewed the concern and need to make a targeted change.",
        ),
        review_id=100,
        review_commit_sha="head",
        current_head_sha="head",
        critique_task=task,
        critique_tasks=(task,),
        critique_headline=headline,
        critique_review_body=review_body,
    )
    live_snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        ci_status="passing",
        review_state="COMMENTED",
        copilot_review_id=100,
        copilot_review_inline_count=0,
        effective_review_comment_count=0,
        effective_review_comment_count_review_id=100,
        effective_review_comment_filter_applied=False,
        copilot_gate_verdict=CopilotGateVerdict(
            passed=False,
            reason=REASON_NEW_CCR_NOT_APPROVED,
            review_id=100,
            body_comment_count=0,
        ),
        reviews=[
            ReviewInfo(
                id=100,
                user=COPILOT_REVIEWER_LOGIN,
                state="COMMENTED",
                body=review_body,
                commit_sha="head",
                submitted_at="2026-10-19T12:00:00Z",
            )
        ],
        critique_headline_classification="critique",
    )
    return provider, comments, post_agent_snapshot, live_snapshot
