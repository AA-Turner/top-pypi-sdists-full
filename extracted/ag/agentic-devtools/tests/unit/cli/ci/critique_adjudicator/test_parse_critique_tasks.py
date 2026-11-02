"""Tests for parsing trusted critique task markers."""

from agentic_devtools.cli.ci.critique_adjudicator import (
    CritiqueAdjudication,
    CritiqueTask,
    build_adjudication_comment,
    build_critique_task_cancellation_comment,
    build_critique_task_comment,
    parse_critique_tasks,
)
from agentic_devtools.cli.ci.evaluator.models import CommentInfo


def test_task_markers_are_trusted_and_head_scoped() -> None:
    body = build_critique_task_comment(42, "a" * 40, 100, 1)
    comments = [
        CommentInfo(1, "workflow[bot]", body, "2026-10-19T12:00:00Z"),
        CommentInfo(2, "attacker", body, "2026-10-19T12:01:00Z"),
        CommentInfo(3, "workflow[bot]", build_critique_task_comment(42, "b" * 40, 100, 2), "2026-10-19T12:02:00Z"),
    ]

    tasks = parse_critique_tasks(comments, trusted_logins={"workflow[bot]"}, pr_number=42, head_sha="a" * 40)

    assert tasks == (CritiqueTask(42, "a" * 40, 100, 1, "2026-10-19T12:00:00Z"),)


def test_task_marker_parses_the_bound_agent_task_id() -> None:
    body = build_critique_task_comment(42, "a" * 40, 100, 1)
    body += "\n<!-- ai-pr-loop:critique-task-id task=task_123 -->"

    tasks = parse_critique_tasks(
        [CommentInfo(1, "workflow[bot]", body, "2026-10-19T12:00:00Z")],
        trusted_logins={"workflow[bot]"},
        pr_number=42,
        head_sha="a" * 40,
    )

    assert len(tasks) == 1
    assert tasks[0].task_id == "task_123"


def test_embedded_task_markers_in_trusted_comment_text_are_ignored() -> None:
    task_marker = build_critique_task_comment(42, "a" * 40, 100, 2).splitlines()[0]
    adjudication = build_adjudication_comment(
        pr_number=42,
        head_sha="a" * 40,
        review_id=100,
        attempt=1,
        adjudication=CritiqueAdjudication(verdict="rebutted", rationale=f"Evidence quotes {task_marker}"),
    )
    comments = [
        CommentInfo(1, "workflow[bot]", adjudication),
        CommentInfo(2, "workflow[bot]", f"Quoted trusted commentary:\n> {task_marker}"),
    ]

    tasks = parse_critique_tasks(comments, trusted_logins={"workflow[bot]"}, pr_number=42, head_sha="a" * 40)

    assert tasks == ()


def test_cancelled_task_marker_is_not_parsed_as_a_dispatched_task() -> None:
    body = build_critique_task_cancellation_comment(42, "a" * 40, 100, 1)
    comments = [CommentInfo(1, "workflow[bot]", body, "2026-10-19T12:00:00Z")]

    assert "ai-pr-loop:critique-task-cancelled pr=42 head=" + ("a" * 40) in body
    tasks = parse_critique_tasks(comments, trusted_logins={"workflow[bot]"}, pr_number=42, head_sha="a" * 40)

    assert tasks == ()
