"""Commit-scoped review state helpers."""

from datetime import UTC, datetime

from .marker import build_marker
from .review_state import CommitComment, ReviewState, ReviewStatus, compute_aggregate_status


def _resolve_commit_thread_id(existing_state: ReviewState, commit_hash: str | None) -> int:
    """Return the review thread id for *commit_hash*.

    Prefers the per-commit registry entry (``commitComments``) so re-review
    replies land in the dedicated thread for that commit; falls back to the
    overall-summary thread for states that predate the per-commit registry.

    Args:
        existing_state: Current review state.
        commit_hash: Commit hash whose thread is wanted.

    Returns:
        The thread id, or ``0`` when none can be resolved.
    """
    if commit_hash:
        entry = existing_state.commitComments.get(commit_hash)
        if entry is not None and entry.threadId > 0:
            return entry.threadId
    return existing_state.overallSummary.threadId


def _build_rereview_skip_message(short_hash: str, model_id: str, pull_request_id: int) -> str:
    """Build the reply posted when a duplicate review is skipped.

    The message explains that the commit was already reviewed by this model and
    provides the ``--force-rereview`` command that overrides the skip and
    re-runs the review, updating the existing comment in place.

    Args:
        short_hash: Short commit hash (first 7 characters).
        model_id: Reviewing model identifier.
        pull_request_id: PR ID (used to build the rerun command).

    Returns:
        Markdown reply content.
    """
    return (
        f"{build_marker('rereview-skipped')}\n"
        f"### 🔁 Re-review requested — skipped\n"
        f"\n"
        f"Another review of commit `{short_hash}` by **{model_id}** was requested, "
        f"but it was **skipped** because this commit has already been reviewed by this model.\n"
        f"\n"
        f"To force a fresh review that overrides this skip and updates the review "
        f"comment in place, run:\n"
        f"\n"
        f"```bash\n"
        f"agdt-initiate-pull-request-review-workflow --pull-request-id {pull_request_id} --force-rereview\n"
        f"```\n"
    )


def _archive_commit_thread(
    state: ReviewState,
    old_commit_hash: str,
    now: datetime | None = None,
) -> None:
    """Archive the just-reviewed commit's thread, then reset the comment pointer.

    Implements the *new top-level thread per reviewed commit* model: before a
    new commit is rendered, the prior commit's consolidated thread is recorded
    in :attr:`ReviewState.commitComments` (so it appears in the "Previous
    reviews" index with a jump link), and ``overallSummary`` is reset to
    ``threadId == 0`` so the next :func:`upsert_consolidated_comment` call POSTs
    a brand-new thread for the incoming commit instead of patching the old one.

    Args:
        state: The review state being re-scaffolded for a new commit.
        old_commit_hash: The commit hash whose thread is being archived.
        now: Current time used to stamp the archived entry's timestamp fields.
            Defaults to ``datetime.now(UTC)`` when omitted.
    """
    if now is None:
        now = datetime.now(UTC)

    entry = state.commitComments.get(old_commit_hash)
    if entry is None:
        entry = CommitComment(commitHash=old_commit_hash)
        state.commitComments[old_commit_hash] = entry

    if state.overallSummary.threadId:
        entry.threadId = state.overallSummary.threadId
        entry.status = state.overallSummary.status
        entry.timestamp = now.isoformat()
        model_id = state.modelId or "unknown"
        ref = entry.upsert_model(model_id)
        # The archived commit's first model owns the thread root comment.
        if not entry.models or entry.models[0] is ref:
            ref.commentId = state.overallSummary.commentId
        ref.status = compute_aggregate_status([fe.status for fe in state.files.values()])
        ref.timestamp = now.isoformat()

    # Reset the consolidated-comment pointer so a fresh thread is created for
    # the incoming commit.
    state.overallSummary.threadId = 0
    state.overallSummary.commentId = 0
    state.overallSummary.status = ReviewStatus.IN_PROGRESS.value
