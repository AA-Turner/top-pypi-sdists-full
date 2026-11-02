"""Review session lifecycle helpers."""

import sys
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from .review_scaffold_activity import (
    _format_activity_log_entry,
    _post_activity_log_entry,
    _update_activity_log_comment_status,
)
from .review_state import ReviewSession, ReviewState, ReviewStatus, save_review_state

STALE_SESSION_THRESHOLD = timedelta(hours=2)


def _check_session_status(
    existing_state: ReviewState,
    commit_hash: str | None,
    model_id: str,
    now: datetime | None = None,
) -> str:
    """Determine the review session status for a given commit + model.

    Args:
        existing_state: Current review state.
        commit_hash: Current commit hash (may be None).
        model_id: Current model identifier.
        now: Current time (injectable for testing).

    Returns:
        One of: "first_review", "already_reviewed", "in_progress",
        "resume_stale", "different_model", "different_commit".
    """
    if now is None:
        now = datetime.now(UTC)

    # Normalise None → "" for comparison so that two unknown hashes match.
    effective_old = existing_state.commitHash or ""
    effective_new = commit_hash or ""

    if effective_old == effective_new:
        # Filter by both model and commit hash — sessions accumulate across
        # commits, so we must scope to the current commit to avoid false
        # "already_reviewed" from sessions recorded for prior commits.
        current_hash = commit_hash or ""
        matching_sessions = [
            s for s in existing_state.sessions if s.modelId == model_id and (s.commitHash or "") == current_hash
        ]

        # First, prefer any completed session regardless of insertion order.
        for session in matching_sessions:
            if session.status == "completed":
                return "already_reviewed"

        # No completed session; next, look for in-progress sessions.
        has_stale_in_progress = False
        for session in matching_sessions:
            if session.status == "in_progress":
                started = datetime.fromisoformat(session.startedUtc)
                if now - started < STALE_SESSION_THRESHOLD:
                    return "in_progress"
                has_stale_in_progress = True

        if has_stale_in_progress:
            return "resume_stale"

        # No active/completed sessions for this model — check if a different
        # model has sessions *for the current commit*.  Sessions accumulate across
        # commits (audit trail), so we must scope this check to avoid false
        # positives from sessions created for prior commits.
        if any(s.modelId != model_id and (s.commitHash or "") == current_hash for s in existing_state.sessions):
            return "different_model"
        return "first_review"

    # Different commit hash — handled by caller (incremental re-scaffolding)
    return "different_commit"


def _mark_stale_sessions_failed(
    existing_state: ReviewState,
    commit_hash: str,
    model_id: str,
    now: datetime | None = None,
) -> list[ReviewSession]:
    """Mark all stale in-progress sessions as failed for a commit + model.

    Args:
        existing_state: Review state (mutated in-place).
        commit_hash: Current commit hash.
        model_id: Current model identifier.
        now: Current time (injectable for testing).

    Returns:
        Sessions that were transitioned from in_progress to failed.
    """
    if now is None:
        now = datetime.now(UTC)
    transitioned: list[ReviewSession] = []
    for session in existing_state.sessions:
        if (
            session.modelId == model_id
            and session.status == "in_progress"
            and (session.commitHash or "") == (commit_hash or "")
        ):
            started = datetime.fromisoformat(session.startedUtc)
            if now - started >= STALE_SESSION_THRESHOLD:
                session.status = "failed"
                session.completedUtc = now.isoformat()
                transitioned.append(session)
    return transitioned


def _update_stale_activity_log_comments(
    state: ReviewState,
    sessions: list[ReviewSession],
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    commit_hash: str | None,
) -> None:
    """Mark transitioned sessions' activity-log comments as failed."""
    if not state.activityLogThreadId:
        return
    for session in sessions:
        if session.activityLogCommentId is None:
            continue
        try:
            fallback_id = _update_activity_log_comment_status(
                requests_module,
                headers,
                threads_url,
                state.activityLogThreadId,
                session.activityLogCommentId,
                "❌",
                "Failed",
                session,
                commit_hash,
                state.sessions.index(session) + 1,
                "Session timed out (stale).",
            )
            if fallback_id is not None:
                session.activityLogCommentId = fallback_id
        except Exception as exc:
            print(f"Warning: Could not update activity log for failed session: {exc}", file=sys.stderr)


def _find_stale_session_id(
    state: ReviewState,
    transitioned_sessions: list[ReviewSession],
    effective_model: str,
    commit_hash: str | None,
) -> str:
    """Find the session ID to cite in a stale-session resume log."""
    if transitioned_sessions:
        return transitioned_sessions[-1].sessionId
    for session in reversed(state.sessions):
        if (
            session.modelId == effective_model
            and session.status == "failed"
            and (session.commitHash or "") == (commit_hash or "")
        ):
            return session.sessionId
    return "unknown"


def _handle_resume_stale(
    state: ReviewState,
    effective_model: str,
    commit_hash: str | None,
    pull_request_id: int,
    dry_run: bool,
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    now: datetime,
) -> ReviewState:
    """Resume stale review state and record its transition in the activity log."""
    reviewed = sum(1 for entry in state.files.values() if entry.status != ReviewStatus.UNREVIEWED.value)
    total = len(state.files)
    print(f"Resuming stale review session for PR {pull_request_id} ({reviewed}/{total} files reviewed).")
    if dry_run:
        return state
    transitioned_sessions = _mark_stale_sessions_failed(state, commit_hash or "", effective_model, now=now)
    _update_stale_activity_log_comments(
        state, transitioned_sessions, requests_module, headers, threads_url, commit_hash
    )
    stale_id = _find_stale_session_id(state, transitioned_sessions, effective_model, commit_hash)
    new_session = _create_session(effective_model, commit_hash=commit_hash, now=now)
    state.sessions.append(new_session)
    save_review_state(state)
    if state.activityLogThreadId:
        entry = _format_activity_log_entry(
            "🔄",
            "Resuming",
            now.isoformat(),
            effective_model,
            (commit_hash or "unknown")[:7],
            new_session.sessionId,
            f"Resuming incomplete review session `{stale_id}` ({reviewed}/{total} files reviewed).",
            len(state.sessions),
        )
        try:
            new_session.activityLogCommentId = _post_activity_log_entry(
                requests_module, headers, threads_url, state.activityLogThreadId, entry
            )
            save_review_state(state)
        except Exception as exc:
            print(f"Warning: Could not post activity log entry: {exc}", file=sys.stderr)
    return state


def _reset_files_for_rereview(existing_state: ReviewState, model_id: str) -> None:
    """Reset every file to ``unreviewed`` for a forced re-review.

    Rotates each file's current suggestions into the ``previousSuggestions``
    audit trail (once per re-review cycle), clears summaries, and resets the
    **forcing model's** verdict so the agent reviews the commit afresh. Other
    models' verdicts are preserved as an audit trail so the "different-model
    reply" semantics remain intact. Mutates *existing_state* in place.

    Args:
        existing_state: Review state to reset (mutated in place).
        model_id: Current model identifier (only this model's verdict is reset).
    """
    for fe in existing_state.files.values():
        if fe.previousSuggestions is None:
            fe.previousSuggestions = list(fe.suggestions)
        elif fe.suggestions:
            fe.previousSuggestions.extend(fe.suggestions)
        fe.suggestions = []
        fe.status = ReviewStatus.UNREVIEWED.value
        fe.summary = None
        fe.modelId = None
        fe.providerType = None
        fe.latencyMs = None
        fe.finishReason = None
        fe.tokensUsed = None
    # All files are now unreviewed — reset the overall status to in-progress so
    # the persisted state is consistent with the rendered headline and so any
    # subsequent archive of this commit records the correct (non-terminal) status.
    existing_state.overallSummary.status = ReviewStatus.IN_PROGRESS.value


def _create_session(
    model_id: str,
    commit_hash: str | None = None,
    now: datetime | None = None,
) -> ReviewSession:
    """Create a new ReviewSession with in_progress status.

    Args:
        model_id: AI model identifier.
        commit_hash: Commit hash this session is reviewing.
        now: Current time (injectable for testing).

    Returns:
        A new ReviewSession.
    """
    if now is None:
        now = datetime.now(UTC)
    return ReviewSession(
        sessionId=uuid.uuid4().hex,
        modelId=model_id,
        startedUtc=now.isoformat(),
        status="in_progress",
        commitHash=commit_hash,
    )
