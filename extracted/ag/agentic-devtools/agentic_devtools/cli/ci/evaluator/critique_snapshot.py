"""Critique-specific fields for post-agent evaluator snapshots."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from ...github.ccr_headline import parse_ccr_overview_summary
from ..critique_adjudicator import (
    CritiqueAdjudicationRecord,
    CritiqueTask,
    parse_critique_adjudications,
    parse_critique_tasks,
)
from ..models import AgentTaskInventory, PRMetadata
from ..provider import CIPlatformProvider, trusted_loop_comment_logins

if TYPE_CHECKING:
    from ..models import IssueCommentInfo, ReviewInfo


class CritiquePostAgentFields(TypedDict):
    critique_task: CritiqueTask | None
    critique_task_completed: bool | None
    critique_tasks: tuple[CritiqueTask, ...]
    critique_headline: str
    critique_review_body: str
    critique_adjudications: tuple[CritiqueAdjudicationRecord, ...]


def build_critique_post_agent_fields(
    provider: CIPlatformProvider,
    pr_number: int | PRMetadata,
    copilot_reviews: list[ReviewInfo],
    issue_comments: list[IssueCommentInfo],
    review_id: int,
    current_head_sha: str,
    head_changed: bool,
    *,
    head_branch: str = "",
    pr_id: int | None = None,
) -> CritiquePostAgentFields:
    """Build trusted critique task and adjudication data for the selected review."""
    if isinstance(pr_number, PRMetadata):
        head_branch = pr_number.head_branch
        pr_id = pr_number.pr_id
        pr_number = pr_number.number
    latest_review = next((review for review in copilot_reviews if review.id == review_id), None)
    headline = ""
    task = None
    task_completed = None
    tasks: tuple[CritiqueTask, ...] = ()
    adjudications: tuple[CritiqueAdjudicationRecord, ...] = ()
    if latest_review is not None and latest_review.commit_sha == current_head_sha and not head_changed:
        overview = parse_ccr_overview_summary(latest_review.body)
        if overview is not None and overview[0] and overview[1]:
            trusted_logins = trusted_loop_comment_logins(provider)
            parsed_tasks = parse_critique_tasks(
                issue_comments,
                trusted_logins=trusted_logins,
                pr_number=pr_number,
                head_sha=current_head_sha,
            )
            tasks = tuple(parsed_tasks)
            matching_tasks = [candidate for candidate in parsed_tasks if candidate.review_id == review_id]
            if matching_tasks:
                headline = overview[1]
                task = max(matching_tasks, key=lambda candidate: (candidate.attempt, candidate.created_at))
                task_completed = _completed_agent_task(
                    provider,
                    pr_number,
                    task,
                    head_branch=head_branch,
                    pr_id=pr_id,
                )
            adjudications = tuple(
                record
                for record in parse_critique_adjudications(
                    issue_comments,
                    trusted_logins=trusted_logins,
                    pr_number=pr_number,
                )
                if record.head_sha == current_head_sha and record.review_id <= review_id
            )
    return {
        "critique_task": task,
        "critique_task_completed": task_completed,
        "critique_tasks": tasks,
        "critique_headline": headline,
        "critique_review_body": latest_review.body if headline and latest_review is not None else "",
        "critique_adjudications": adjudications,
    }


def _completed_agent_task(
    provider: CIPlatformProvider,
    pr_number: int,
    task: CritiqueTask,
    *,
    head_branch: str,
    pr_id: int | None,
) -> bool | None:
    """Return true only when the linked Agent Task has a verified completed lifecycle."""
    if not task.task_id:
        return None
    list_lifecycles = getattr(provider, "list_pr_agent_task_lifecycles", None)
    if not callable(list_lifecycles):
        return None
    inventory = list_lifecycles(pr_number, pr_id=pr_id, head_branch=head_branch, head_sha=task.head_sha)
    if not isinstance(inventory, AgentTaskInventory) or not inventory.complete:
        return None
    matches = [candidate for candidate in inventory.tasks if candidate.task_id == task.task_id]
    if len(matches) != 1:
        return None
    lifecycle = matches[0]
    if lifecycle.pr_number != pr_number or (lifecycle.head_sha and lifecycle.head_sha != task.head_sha):
        return None
    if lifecycle.state.casefold() != "completed":
        return False
    terminal_session_states = {"completed", "failed", "canceled", "cancelled", "stopped", "timed_out"}
    if any(session.state.casefold() not in terminal_session_states for session in lifecycle.sessions):
        return False
    return True
