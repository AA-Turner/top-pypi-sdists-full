"""Post-agent state classifier.

Contains the pure classification function that determines the PR state
after a Copilot agent session. This function performs zero I/O and is
fully unit-testable.
"""

from __future__ import annotations

from datetime import UTC, datetime

from .models import PostAgentClassification, PostAgentSnapshot


def _parse_timestamp(value: str) -> datetime | None:
    """Parse provider timestamps for a fail-closed task/reply ordering check."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed


def _has_completed_critique_task_reply(snapshot: PostAgentSnapshot) -> bool:
    """Return whether the latest Copilot reply follows an unanswered task marker."""
    task = snapshot.critique_task
    latest = snapshot.latest_agent_comment
    if task is None or snapshot.critique_task_completed is not True or latest is None or not latest.body.strip():
        return False
    if (
        task.pr_number != snapshot.pr_number
        or task.head_sha != snapshot.current_head_sha
        or task.review_id != snapshot.review_id
        or snapshot.head_changed_since_review
    ):
        return False
    task_started = _parse_timestamp(task.created_at)
    reply_created = _parse_timestamp(latest.created_at)
    if task_started is None or reply_created is None or reply_created <= task_started:
        return False
    matching_records = [
        record
        for record in snapshot.critique_adjudications
        if record.pr_number == snapshot.pr_number
        and record.head_sha == task.head_sha
        and record.review_id == task.review_id
        and record.attempt == task.attempt
    ]
    if matching_records:
        return any(record.verdict == "needs_human" for record in matching_records)
    return True


def classify_post_agent_state(snapshot: PostAgentSnapshot) -> PostAgentClassification:
    """Classify the post-agent PR state into a remediation category.

    This is a pure function — no I/O, no side effects. All decision logic
    for the post-agent evaluator lives here.

    Classification priority:
    1. Concurrent evaluation check (lock held by another run)
    2. Complete (sentinel already present)
    3. Repair satisfied — no changes needed (agent posted marker)
    4. Threads resolved but no sentinel
    5. Agent claims fixed (comment present, no code change, unresolved threads)
    6. Changes made but threads still unresolved
    7. Agent silent (fallback)

    Args:
        snapshot: Immutable snapshot of PR state.

    Returns:
        The classification enum value.
    """
    # 1. If another evaluator holds the lock, skip
    if snapshot.lock_holder:
        return PostAgentClassification.concurrent_evaluation_skipped

    if snapshot.critique_task is not None and snapshot.critique_task_completed is not True:
        return PostAgentClassification.critique_task_pending

    critique_reply = _has_completed_critique_task_reply(snapshot)
    task = snapshot.critique_task
    task_identity = (snapshot.pr_number, task.head_sha, task.review_id, task.attempt) if task is not None else None
    task_adjudications = tuple(
        record
        for record in snapshot.critique_adjudications
        if task_identity is not None
        and (record.pr_number, record.head_sha, record.review_id, record.attempt) == task_identity
    )
    task_has_adjudication = bool(task_adjudications)
    task_needs_human = any(record.verdict == "needs_human" for record in task_adjudications)
    current_task_was_rebutted = (
        task is not None
        and task.pr_number == snapshot.pr_number
        and task.head_sha == snapshot.current_head_sha
        and task.review_id == snapshot.review_id
        and not snapshot.head_changed_since_review
        and any(record.verdict == "rebutted" for record in task_adjudications)
    )

    # A generic HEAD sentinel does not prove that a newer critique task was adjudicated.
    if snapshot.has_sentinel and (not critique_reply or (task_has_adjudication and not task_needs_human)):
        return PostAgentClassification.complete

    # Critique replies need evidence-based adjudication before generic no-change handling.
    if critique_reply:
        return PostAgentClassification.critique_adjudication

    # 3. Repair satisfied — agent posted marker indicating no changes needed
    review_id_matches = snapshot.review_id == 0 or snapshot.repair_satisfied_review_id == snapshot.review_id
    if snapshot.has_repair_satisfied_marker and not snapshot.head_changed_since_review and review_id_matches:
        return PostAgentClassification.repair_satisfied_no_changes

    # Determine thread states
    unresolved_threads = [t for t in snapshot.threads if not t.is_resolved]
    all_threads_resolved = len(unresolved_threads) == 0 and len(snapshot.threads) > 0

    # 4. All threads resolved but no sentinel posted
    if all_threads_resolved and not snapshot.has_sentinel:
        return PostAgentClassification.threads_resolved_no_sentinel

    # 5. Agent left a comment claiming fixed, but threads still unresolved
    if snapshot.latest_agent_comment is not None and not snapshot.head_changed_since_review and unresolved_threads:
        return PostAgentClassification.agent_claims_fixed_no_sentinel

    # 6. Code was changed but threads remain unresolved
    if snapshot.head_changed_since_review and unresolved_threads:
        return PostAgentClassification.changes_made_threads_unresolved

    if current_task_was_rebutted and not unresolved_threads:
        return PostAgentClassification.complete

    # 7. Fallback: agent didn't respond meaningfully
    return PostAgentClassification.agent_silent
