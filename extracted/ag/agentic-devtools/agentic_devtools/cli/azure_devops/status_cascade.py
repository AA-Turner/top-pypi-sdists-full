"""Status derivation and cascade update logic for PR review state.

Provides functions to:
- Derive overall PR status directly from file statuses
- Compute PATCH operations needed after a file status change
- Execute those PATCH operations against the Azure DevOps API
"""

import sys
from dataclasses import dataclass, field

from .config import AzureDevOpsConfig
from .consolidated_review import render_consolidated_review_comment
from .helpers import CrossIdentityForbiddenError, patch_comment, patch_thread_status, post_cross_identity_reply
from .review_state import ReviewState, ReviewStatus, compute_aggregate_status, normalize_file_path

# Thread status mapping: review status → Azure DevOps thread status
_THREAD_STATUS_MAP: dict[str, str] = {
    ReviewStatus.UNREVIEWED.value: "active",
    ReviewStatus.IN_PROGRESS.value: "active",
    ReviewStatus.APPROVED.value: "closed",
    ReviewStatus.NEEDS_WORK.value: "active",
}


@dataclass
class PatchOperation:
    """A pair of PATCH operations for a review comment: content + thread status."""

    thread_id: int
    comment_id: int
    new_content: str
    thread_status: str


@dataclass
class CascadeResult:
    """Result of executing a batch of PATCH operations."""

    succeeded: list[int] = field(default_factory=list)
    fallen_back: list[int] = field(default_factory=list)
    blocked: list[int] = field(default_factory=list)
    #: Maps a thread id to the new comment id created when a cross-identity 403
    #: forced a reply fallback. Lets callers (and the ``state`` argument below)
    #: re-target that reply on the next cascade instead of re-replying to the
    #: forbidden comment and spamming the thread with duplicates.
    reply_comment_ids: dict[int, int] = field(default_factory=dict)


def derive_overall_status(state: ReviewState) -> str:
    """Compute the derived overall PR status based on file statuses.

    With the elimination of folder-level threads, the overall status is now
    derived directly from file statuses rather than folder statuses.

    Status Derivation Rules:
    - No files or all files unreviewed → unreviewed
    - At least 1 file started, not all complete → in-progress
    - All files complete, all Approved → approved
    - All files complete, any Needs Work → needs-work

    Args:
        state: Full ReviewState containing files.

    Returns:
        Derived status string (a ReviewStatus value).
    """
    # Normalize unknown statuses to 'unreviewed' so the derived status matches
    # the rendering normalization in render_overall_summary().
    known = {s.value for s in ReviewStatus}
    file_statuses = [f.status if f.status in known else ReviewStatus.UNREVIEWED.value for f in state.files.values()]

    return compute_aggregate_status(file_statuses)


def cascade_status_update(
    state: ReviewState,
    file_path: str,
    base_url: str,
    model_name: str | None = None,
    commit_hash: str | None = None,
    commit_url: str | None = None,
) -> list[PatchOperation]:
    """Compute PATCH operations needed after a file's status has changed.

    Updates the overall summary status in the state object, then returns
    the PATCH operation needed to sync the Azure DevOps overall summary
    comment and thread status.  Folder-level threads have been eliminated
    so only the overall summary is updated.

    Args:
        state: Full ReviewState (mutated in-place with new overall status).
        file_path: Path of the file whose status has changed.
        base_url: PR root URL for generating markdown content.
        model_name: Legacy compatibility parameter (ignored).
        commit_hash: Legacy compatibility parameter (ignored).
        commit_url: Legacy compatibility parameter (ignored).

    Returns:
        List of PatchOperation objects to execute via execute_cascade.

    Raises:
        KeyError: If file_path is not found in review state.
    """
    normalized = normalize_file_path(file_path)
    if normalized not in state.files:
        raise KeyError(f"File not found in review state: {normalized}")

    # Derive and update overall summary status directly from files
    new_overall_status = derive_overall_status(state)
    state.overallSummary.status = new_overall_status

    # Build PATCH operations — only the single consolidated review comment,
    # tracked by state.overallSummary. The consolidated renderer embeds its own
    # v2 marker and derives model/commit attribution directly from the state, so
    # the model_name/commit_hash/commit_url parameters are accepted for call-site
    # compatibility but are no longer used here, and no marker prefix is added.
    ops: list[PatchOperation] = []
    overall_content = render_consolidated_review_comment(state, base_url)
    ops.append(
        PatchOperation(
            thread_id=state.overallSummary.threadId,
            comment_id=state.overallSummary.commentId,
            new_content=overall_content,
            thread_status=_THREAD_STATUS_MAP.get(new_overall_status, "active"),
        )
    )

    return ops


def cascade_overall_summary_update(
    state: ReviewState,
    base_url: str,
    model_name: str | None = None,
    commit_hash: str | None = None,
    commit_url: str | None = None,
) -> list[PatchOperation]:
    """Compute PATCH operations for the overall PR summary without a file context.

    Used at workflow completion to ensure the overall summary reflects the
    final derived status. Unlike cascade_status_update(), this does not
    require a file_path argument.

    Args:
        state: Full ReviewState (mutated in-place with new overall status).
        base_url: PR root URL for generating markdown content.
        model_name: Legacy compatibility parameter (ignored).
        commit_hash: Legacy compatibility parameter (ignored).
        commit_url: Legacy compatibility parameter (ignored).

    Returns:
        List of PatchOperation objects to execute via execute_cascade.
    """
    new_overall_status = derive_overall_status(state)
    state.overallSummary.status = new_overall_status

    # The consolidated renderer derives model/commit attribution directly from
    # the ReviewState, so the model_name/commit_hash/commit_url parameters are
    # accepted for call-site compatibility but are no longer used here. The
    # renderer also embeds its own v2 marker, so no marker prefix is added.
    overall_content = render_consolidated_review_comment(state, base_url)
    return [
        PatchOperation(
            thread_id=state.overallSummary.threadId,
            comment_id=state.overallSummary.commentId,
            new_content=overall_content,
            # Default to "active" for non-final statuses (unreviewed, in-progress)
            thread_status=_THREAD_STATUS_MAP.get(new_overall_status, "active"),
        )
    ]


def _record_cross_identity_reply(
    op: PatchOperation,
    reply_result: dict,
    result: CascadeResult,
    state: ReviewState | None,
) -> None:
    """Feed a cross-identity reply's new comment id back into the result and state.

    When :func:`execute_cascade` cannot PATCH the consolidated comment because it is
    owned by another identity, it posts a *reply* instead. That reply is owned by the
    **current** identity, so recording its id lets the next cascade PATCH the reply in
    place rather than posting yet another duplicate reply to the forbidden comment.

    The ``state.overallSummary`` comment id is re-targeted only when *op* actually
    refers to it (matching thread **and** comment id), keeping this safe for future
    multi-operation cascades. The function performs no I/O and never raises.

    Args:
        op: The operation whose PATCH fell back to a reply.
        reply_result: JSON dict returned by ``post_cross_identity_reply`` (the new
            comment), or ``{}`` in dry-run mode.
        result: Cascade result to annotate with the new comment id.
        state: Review state to re-target, or ``None`` when unavailable.
    """
    raw_id = reply_result.get("id") if reply_result else None
    if raw_id is None:
        return
    try:
        new_id = int(raw_id)
    except (TypeError, ValueError):
        return
    result.reply_comment_ids[op.thread_id] = new_id
    if (
        state is not None
        and op.thread_id == state.overallSummary.threadId
        and op.comment_id == state.overallSummary.commentId
        and new_id != state.overallSummary.commentId
    ):
        state.overallSummary.commentId = new_id


def execute_cascade(
    patch_operations: list[PatchOperation],
    requests_module,
    headers: dict[str, str],
    config: AzureDevOpsConfig,
    repo_id: str,
    pull_request_id: int,
    dry_run: bool = False,
    state: ReviewState | None = None,
) -> CascadeResult:
    """Execute all PATCH operations against the Azure DevOps API.

    For each PatchOperation, updates both the comment content and the
    thread status via separate PATCH calls. Cross-identity 403 errors
    are isolated per-operation so one forbidden update does not abort the
    entire batch; those operations fall back to a reply update when possible.

    When a forbidden PATCH falls back to a reply and *state* is provided, the new
    reply's comment id is written back to ``state.overallSummary.commentId`` (when the
    operation targets it) so the **next** cascade edits that reply in place instead of
    posting another duplicate. Callers are responsible for persisting *state*.

    Args:
        patch_operations: List of PatchOperation objects to execute.
        requests_module: The requests module.
        headers: Auth headers for API calls.
        config: Azure DevOps configuration.
        repo_id: Repository ID.
        pull_request_id: Pull request ID.
        dry_run: If True, skip API calls and print dry-run messages.
        state: Optional review state whose ``overallSummary`` comment id is
            re-targeted after a cross-identity reply fallback.

    Returns:
        CascadeResult with succeeded, fallen_back, and blocked thread IDs, plus
        ``reply_comment_ids`` mapping each fallen-back thread to its new comment id.
    """
    result = CascadeResult()
    for op in patch_operations:
        try:
            patch_comment(
                requests_module=requests_module,
                headers=headers,
                config=config,
                repo_id=repo_id,
                pull_request_id=pull_request_id,
                thread_id=op.thread_id,
                comment_id=op.comment_id,
                new_content=op.new_content,
                dry_run=dry_run,
            )
            patch_thread_status(
                requests_module=requests_module,
                headers=headers,
                config=config,
                repo_id=repo_id,
                pull_request_id=pull_request_id,
                thread_id=op.thread_id,
                status=op.thread_status,
                dry_run=dry_run,
            )
            result.succeeded.append(op.thread_id)
        except CrossIdentityForbiddenError:
            try:
                reply_result = post_cross_identity_reply(
                    requests_module=requests_module,
                    headers=headers,
                    config=config,
                    repo_id=repo_id,
                    pull_request_id=pull_request_id,
                    thread_id=op.thread_id,
                    content=op.new_content,
                    dry_run=dry_run,
                )
                patch_thread_status(
                    requests_module=requests_module,
                    headers=headers,
                    config=config,
                    repo_id=repo_id,
                    pull_request_id=pull_request_id,
                    thread_id=op.thread_id,
                    status=op.thread_status,
                    dry_run=dry_run,
                )
                result.fallen_back.append(op.thread_id)
                _record_cross_identity_reply(op, reply_result, result, state)
            except Exception as exc:
                print(
                    f"Warning: 403 on thread {op.thread_id} (cross-identity) and reply fallback failed: {exc}",
                    file=sys.stderr,
                )
                result.blocked.append(op.thread_id)
    return result
