"""Exercise zero-findings critique routing through snapshot, gate, and dispatch."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import CheckRunStatus, IssueCommentInfo, PRMetadata, ReviewInfo
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_NEW_CCR_NOT_APPROVED,
    CopilotGateVerdict,
    copilot_review_gate_passed,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot

HEADLINE = "Previously reported parser regressions remain unresolved and can lose findings or block promotion."
HUMAN_REVIEW_HEADLINE = "Broad modernization and limited baseline verification require final human review."


def _provider(body: str, review_state: str) -> MagicMock:
    provider = MagicMock()
    provider.get_pr_metadata.return_value = PRMetadata(
        number=42,
        title="Test PR",
        head_branch="feature",
        head_sha="head-sha",
        base_branch="main",
        requested_reviewers=[],
        base_repo_full_name="owner/repo",
    )
    provider.get_commit_author_login.return_value = ""
    provider.list_pr_files.return_value = ["src/parser.py"]
    provider.list_check_runs.return_value = [
        CheckRunStatus(id=1, name="Build", status="completed", conclusion="success")
    ]
    provider.is_codeql_configured.return_value = False
    provider.list_reviews.return_value = [
        ReviewInfo(
            id=100,
            user="Copilot",
            state=review_state,
            body=body,
            commit_sha="head-sha",
        )
    ]
    provider.list_review_comments.return_value = []
    provider.list_review_threads_by_thread_id.return_value = {}
    provider.list_review_thread_states.return_value = {}
    provider.list_pr_issue_events.return_value = []
    provider.count_commits_above_merge_base.return_value = 1
    provider.count_commits_behind.return_value = 0
    provider.get_approver_login.return_value = ""
    provider.compute_diff_files = None
    provider.list_issue_comments.return_value = []
    provider.get_pr_token_login.return_value = "github-actions[bot]"

    comments: list[IssueCommentInfo] = []

    def find_comment(pr_number: int, marker: str) -> tuple[int, str] | None:
        return next(((comment.id, comment.body) for comment in reversed(comments) if marker in comment.body), None)

    def post_comment(pr_number: int, comment_body: str) -> int:
        comment_id = len(comments) + 1
        comments.append(IssueCommentInfo(comment_id, "github-actions[bot]", comment_body))
        return comment_id

    def update_comment(comment_id: int, comment_body: str) -> None:
        for index, comment in enumerate(comments):
            if comment.id == comment_id:
                comments[index] = IssueCommentInfo(comment_id, comment.author, comment_body)
                return
        raise AssertionError(f"Unknown comment ID {comment_id}")

    provider.list_issue_comments.side_effect = lambda _pr_number: list(comments)
    provider.find_comment.side_effect = find_comment
    provider.post_comment.side_effect = post_comment
    provider.post_comment_as_pr_token.side_effect = post_comment
    provider.update_comment.side_effect = update_comment
    provider.update_comment_as_pr_token.side_effect = update_comment
    provider.dispatch_repair.return_value = "task:owner/repo:confirmed"
    return provider


@pytest.mark.parametrize("heading", ["### 🔴 Not ready to approve", "### 🔵 Needs a closer look"])
def test_human_review_headline_passes_not_approved_gate_under_either_heading(heading: str) -> None:
    body = (
        f"<!-- ccr-overview-v2 -->\n\n{heading}\n\n{HUMAN_REVIEW_HEADLINE}\n\n"
        "**Comments generated:** 0\n**No open issues** 🎉"
    )
    provider = _provider(body, "CHANGES_REQUESTED")

    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict",
            return_value=CopilotGateVerdict(
                False,
                REASON_NEW_CCR_NOT_APPROVED,
                100,
                body_comment_count=0,
            ),
        ),
        patch(
            "agentic_devtools.cli.ci.critique_adjudicator._run_single_adjudication",
            return_value='{"verdict":"approval_worthy"}',
        ) as run_adjudication,
    ):
        snapshot = build_pr_state_snapshot(
            provider,
            42,
            actionable_check_names=frozenset({"Build"}),
            promote_findings=False,
        )

    assert snapshot.critique_headline_classification == "approval_worthy"
    assert snapshot.effective_review_comment_count == 0
    assert snapshot.head_changed_since_review is False
    assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is True
    run_adjudication.assert_called_once()
    assert f'"headline":"{HUMAN_REVIEW_HEADLINE}"' in run_adjudication.call_args.args[0]
