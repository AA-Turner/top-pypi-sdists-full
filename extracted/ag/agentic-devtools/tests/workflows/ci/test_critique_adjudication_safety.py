"""Integration regressions for critique adjudication safety."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.critique_adjudicator import CritiqueTask, build_critique_task_comment
from agentic_devtools.cli.ci.evaluator.classifier import classify_post_agent_state
from agentic_devtools.cli.ci.evaluator.lock import LockStatus
from agentic_devtools.cli.ci.evaluator.models import CommentInfo, PostAgentClassification, PostAgentSnapshot
from agentic_devtools.cli.ci.evaluator.snapshot_builder import build_snapshot
from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskLifecycle,
    IssueCommentInfo,
    PRMetadata,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.actions.critique_adjudication import CritiqueAdjudicationAction
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.runner import run_pipeline
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


class _LaterMutationAction:
    name = "publish"

    def __init__(self) -> None:
        self.executed = False

    def evaluate(self, snapshot, derived):
        return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

    def execute(self, provider, snapshot, derived):
        self.executed = True
        return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)


def test_evaluator_lock_loss_blocks_later_pipeline_mutations() -> None:
    provider = MagicMock()
    provider.list_issue_comments.return_value = []
    snapshot = PRStateSnapshot(pr_number=42, base_repo_full_name="owner/repo", head_sha="head")
    completed_snapshot = PostAgentSnapshot(
        pr_number=42,
        current_head_sha="head",
        review_id=100,
        critique_task=CritiqueTask(42, "head", 100, 1, "2026-10-20T08:00:00Z", "task-123"),
        critique_task_completed=True,
        latest_agent_comment=CommentInfo(
            id=11,
            author="copilot-swe-agent[bot]",
            body="No changes were made.",
            created_at="2026-10-20T08:01:00Z",
        ),
    )

    later_mutation = _LaterMutationAction()
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.lock.check_lock_status",
            side_effect=[LockStatus(is_locked=True, holder="token"), LockStatus()],
        ),
        patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.build_snapshot", return_value=completed_snapshot),
        patch("agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles"),
    ):
        summary = run_pipeline(
            provider,
            snapshot,
            [CritiqueAdjudicationAction("token"), later_mutation],
        )

    assert summary.results[0].decision is ActionDecision.BLOCKED
    assert summary.results[1].decision is ActionDecision.BLOCKED_BY_GUARD
    assert later_mutation.executed is False


def test_completed_synthetic_review_critique_task_is_adjudicable() -> None:
    provider = MagicMock()
    provider.get_pr_metadata.return_value = PRMetadata(
        number=42,
        title="PR",
        head_branch="feature",
        head_sha="head",
        base_branch="main",
    )
    body = (
        "<!-- synthetic-copilot-review -->\n"
        "<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n"
        "A concrete parser regression remains.\n\n0 open findings"
    )
    provider.list_reviews.return_value = [ReviewInfo(100, "AMARSNIK_swica", "COMMENTED", body, "head")]
    task_body = build_critique_task_comment(42, "head", 100, 1)
    task_body += "\n<!-- ai-pr-loop:critique-task-id task=task-123 -->"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(1, "github-actions[bot]", task_body, "2026-10-20T08:00:00Z"),
        IssueCommentInfo(2, "copilot-swe-agent[bot]", "No changes were made.", "2026-10-20T08:01:00Z"),
    ]
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id="task-123",
                repository="owner/repo",
                pr_number=42,
                head_branch="feature",
                state="completed",
                created_at="2026-10-20T08:00:00Z",
                head_sha="head",
            ),
        )
    )
    provider.get_pr_diff.return_value = ""

    with (
        patch("agentic_devtools.cli.ci.evaluator.snapshot_comments._get_review_thread_statuses", return_value={}),
        patch(
            "agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status",
            return_value=LockStatus(),
        ),
    ):
        snapshot = build_snapshot(provider, 42, "owner/repo")

    assert snapshot.review_id == 100
    assert snapshot.review_commit_sha == "head"
    assert snapshot.head_changed_since_review is False
    assert snapshot.critique_task is not None
    assert snapshot.critique_task_completed is True
    assert classify_post_agent_state(snapshot) is PostAgentClassification.critique_adjudication
