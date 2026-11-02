from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import (
    CritiqueAdjudication,
    build_adjudication_comment,
    build_critique_task_comment,
)
from agentic_devtools.cli.ci.evaluator.critique_snapshot import (
    CritiquePostAgentFields,
    build_critique_post_agent_fields,
)
from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskLifecycle,
    AgentTaskSessionLifecycle,
    IssueCommentInfo,
    PRMetadata,
    ReviewInfo,
)


def _build_fields_for_linked_task(
    provider: MagicMock,
    *,
    head_branch: str = "feature",
    pr_id: int | None = None,
) -> CritiquePostAgentFields:
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    headline = "A concrete parser regression remains."
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    review = ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head")
    task_body = build_critique_task_comment(42, "head", 100, 1)
    task_body += "\n<!-- ai-pr-loop:critique-task-id task=task-123 -->"
    comments = [IssueCommentInfo(1, "github-actions[bot]", task_body, "2026-10-19T12:00:00Z")]
    pr_metadata = PRMetadata(
        number=42, title="PR", head_branch=head_branch, head_sha="head", base_branch="main", pr_id=pr_id
    )
    return build_critique_post_agent_fields(provider, pr_metadata, [review], comments, 100, "head", False)


def test_build_critique_post_agent_fields_ignores_missing_stale_and_changed_reviews() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    body = "<!-- ccr-overview-v2 -->\n### Needs a closer look\n\nA defect remains.\n\n0 open findings"
    review = ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "old")

    assert build_critique_post_agent_fields(provider, 42, [], [], 100, "head", False)["critique_headline"] == ""
    assert build_critique_post_agent_fields(provider, 42, [review], [], 100, "head", False)["critique_headline"] == ""
    assert build_critique_post_agent_fields(provider, 42, [review], [], 100, "head", True)["critique_headline"] == ""
    provider.get_trusted_loop_comment_logins.assert_not_called()


def test_build_critique_post_agent_fields_does_not_classify_headline_without_matching_task() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    headline = "A concrete parser regression remains."
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    review = ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head")

    with patch(
        "agentic_devtools.cli.ci.evaluator.critique_snapshot.classify_critique_headline",
        create=True,
    ) as classify:
        fields = build_critique_post_agent_fields(provider, 42, [review], [], 100, "head", False)

    classify.assert_not_called()
    assert fields["critique_headline"] == ""
    assert fields["critique_review_body"] == ""
    assert fields["critique_task"] is None
    assert fields["critique_tasks"] == ()
    assert fields["critique_adjudications"] == ()


def test_build_critique_post_agent_fields_omits_approval_worthy_headline() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    headline = "Broad modernization requires final human review."
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    review = ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head")

    fields = build_critique_post_agent_fields(provider, 42, [review], [], 100, "head", False)

    assert fields["critique_headline"] == ""
    assert fields["critique_review_body"] == ""


def test_build_critique_post_agent_fields_uses_latest_matching_task_and_adjudication() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    headline = "A concrete parser regression remains."
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    review = ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head")
    comments = [
        IssueCommentInfo(
            1, "github-actions[bot]", build_critique_task_comment(42, "head", 100, 1), "2026-10-19T12:00:00Z"
        ),
        IssueCommentInfo(
            2, "github-actions[bot]", build_critique_task_comment(42, "head", 100, 2), "2026-10-19T12:01:00Z"
        ),
        IssueCommentInfo(
            3,
            "github-actions[bot]",
            build_adjudication_comment(
                pr_number=42,
                head_sha="head",
                review_id=100,
                attempt=1,
                adjudication=CritiqueAdjudication(
                    verdict="needs_repair", rationale="Still broken.", concrete_instruction="Add a test."
                ),
            ),
        ),
    ]

    fields = build_critique_post_agent_fields(provider, 42, [review], comments, 100, "head", False)

    assert fields["critique_headline"] == headline
    task = fields["critique_task"]
    assert task is not None
    assert task.attempt == 2
    assert len(fields["critique_tasks"]) == 2
    assert len(fields["critique_adjudications"]) == 1


def test_build_critique_post_agent_fields_requires_completed_matching_agent_task() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id="task-123",
                repository="owner/repo",
                pr_number=42,
                head_branch="feature",
                state="completed",
                created_at="2026-10-19T12:01:00Z",
                head_sha="head",
            ),
        )
    )
    headline = "A concrete parser regression remains."
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    review = ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head")
    task_body = build_critique_task_comment(42, "head", 100, 1)
    task_body += "\n<!-- ai-pr-loop:critique-task-id task=task-123 -->"
    comments = [IssueCommentInfo(1, "github-actions[bot]", task_body, "2026-10-19T12:00:00Z")]

    fields = build_critique_post_agent_fields(provider, 42, [review], comments, 100, "head", False)

    assert fields["critique_task_completed"] is True


@pytest.mark.parametrize(("head_branch", "pr_id"), [("feature", None), ("", 1234)])
def test_build_critique_post_agent_fields_correlates_by_branch_or_database_id(
    head_branch: str,
    pr_id: int | None,
) -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id="task-123",
                repository="owner/repo",
                pr_number=42,
                head_branch=head_branch,
                state="completed",
                created_at="2026-10-19T12:01:00Z",
                head_sha="head",
            ),
        )
    )

    assert (
        _build_fields_for_linked_task(provider, head_branch=head_branch, pr_id=pr_id)["critique_task_completed"] is True
    )
    provider.list_pr_agent_task_lifecycles.assert_called_once_with(
        42, pr_id=pr_id, head_branch=head_branch, head_sha="head"
    )


@pytest.mark.parametrize("session_state", ["failed", "canceled", "cancelled", "stopped", "timed_out", "completed"])
def test_build_critique_post_agent_fields_accepts_terminal_session_after_completed_retry(
    session_state: str,
) -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id="task-123",
                repository="owner/repo",
                pr_number=42,
                head_branch="feature",
                state="completed",
                created_at="2026-10-19T12:01:00Z",
                sessions=(AgentTaskSessionLifecycle("terminal-session", session_state),),
                head_sha="head",
            ),
        )
    )

    assert _build_fields_for_linked_task(provider)["critique_task_completed"] is True


def test_build_critique_post_agent_fields_defers_for_active_or_unknown_task_inventory() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id="task-123",
                repository="owner/repo",
                pr_number=42,
                head_branch="feature",
                state="in_progress",
                created_at="2026-10-19T12:01:00Z",
                head_sha="head",
            ),
        )
    )
    headline = "A concrete parser regression remains."
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    review = ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head")
    task_body = build_critique_task_comment(42, "head", 100, 1)
    task_body += "\n<!-- ai-pr-loop:critique-task-id task=task-123 -->"
    comments = [IssueCommentInfo(1, "github-actions[bot]", task_body, "2026-10-19T12:00:00Z")]

    fields = build_critique_post_agent_fields(provider, 42, [review], comments, 100, "head", False)

    assert fields["critique_task_completed"] is False


def test_build_critique_post_agent_fields_defers_for_incomplete_inventory() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory((), complete=False)
    headline = "A concrete parser regression remains."
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    review = ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head")
    task_body = build_critique_task_comment(42, "head", 100, 1)
    task_body += "\n<!-- ai-pr-loop:critique-task-id task=task-123 -->"
    comments = [IssueCommentInfo(1, "github-actions[bot]", task_body, "2026-10-19T12:00:00Z")]

    fields = build_critique_post_agent_fields(provider, 42, [review], comments, 100, "head", False)

    assert fields["critique_task_completed"] is None


def test_build_critique_post_agent_fields_defers_when_lifecycle_capability_is_missing() -> None:
    provider = MagicMock()
    provider.list_pr_agent_task_lifecycles = None

    assert _build_fields_for_linked_task(provider)["critique_task_completed"] is None


def test_build_critique_post_agent_fields_defers_when_task_is_missing_from_inventory() -> None:
    provider = MagicMock()
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(())

    assert _build_fields_for_linked_task(provider)["critique_task_completed"] is None


@pytest.mark.parametrize(
    ("pr_number", "head_sha"),
    [(43, "head"), (42, "other-head")],
)
def test_build_critique_post_agent_fields_defers_when_task_context_does_not_match(
    pr_number: int,
    head_sha: str,
) -> None:
    provider = MagicMock()
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id="task-123",
                repository="owner/repo",
                pr_number=pr_number,
                head_branch="feature",
                state="completed",
                created_at="2026-10-19T12:01:00Z",
                head_sha=head_sha,
            ),
        )
    )

    assert _build_fields_for_linked_task(provider)["critique_task_completed"] is None


def test_build_critique_post_agent_fields_defers_when_task_inventory_has_duplicate_ids() -> None:
    provider = MagicMock()
    lifecycle = AgentTaskLifecycle(
        task_id="task-123",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="completed",
        created_at="2026-10-19T12:01:00Z",
        head_sha="head",
    )
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory((lifecycle, lifecycle))

    assert _build_fields_for_linked_task(provider)["critique_task_completed"] is None


@pytest.mark.parametrize("session_state", ["in_progress", "unknown"])
def test_build_critique_post_agent_fields_rejects_active_or_unknown_linked_sessions(session_state: str) -> None:
    provider = MagicMock()
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id="task-123",
                repository="owner/repo",
                pr_number=42,
                head_branch="feature",
                state="completed",
                created_at="2026-10-19T12:01:00Z",
                sessions=(AgentTaskSessionLifecycle("session-1", session_state),),
                head_sha="head",
            ),
        )
    )

    assert _build_fields_for_linked_task(provider)["critique_task_completed"] is False


def test_build_critique_post_agent_fields_keeps_prior_same_head_review_history() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    headline = "A concrete parser regression remains."
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    review = ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head")
    prior_adjudication = CritiqueAdjudication(
        verdict="needs_repair",
        rationale="The earlier review's parser finding is still relevant.",
        concrete_instruction="Add a parser regression test.",
    )
    comments = [
        IssueCommentInfo(1, "github-actions[bot]", build_critique_task_comment(42, "head", 100, 1)),
        IssueCommentInfo(
            2,
            "github-actions[bot]",
            build_adjudication_comment(
                pr_number=42,
                head_sha="head",
                review_id=90,
                attempt=1,
                adjudication=prior_adjudication,
            ),
        ),
        IssueCommentInfo(
            3,
            "github-actions[bot]",
            build_adjudication_comment(
                pr_number=42,
                head_sha="older-head",
                review_id=95,
                attempt=1,
                adjudication=CritiqueAdjudication(verdict="rebutted", rationale="That older HEAD was resolved."),
            ),
        ),
        IssueCommentInfo(
            4,
            "github-actions[bot]",
            build_adjudication_comment(
                pr_number=42,
                head_sha="head",
                review_id=110,
                attempt=1,
                adjudication=CritiqueAdjudication(verdict="rebutted", rationale="This review is later."),
            ),
        ),
    ]

    fields = build_critique_post_agent_fields(provider, 42, [review], comments, 100, "head", False)

    assert [(record.review_id, record.rationale) for record in fields["critique_adjudications"]] == [
        (90, "The earlier review's parser finding is still relevant.")
    ]


def test_build_critique_post_agent_fields_rejects_overview_without_headline() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    review = ReviewInfo(100, "copilot[bot]", "COMMENTED", "<!-- ccr-overview-v2 -->\n0 open findings", "head")

    fields = build_critique_post_agent_fields(provider, 42, [review], [], 100, "head", False)

    assert fields["critique_headline"] == ""
    assert fields["critique_review_body"] == ""
    provider.get_trusted_loop_comment_logins.assert_not_called()
