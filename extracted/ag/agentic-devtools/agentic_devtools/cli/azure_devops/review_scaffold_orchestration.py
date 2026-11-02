"""Orchestrate initial, resumed, and incremental review scaffolding."""

import sys
from datetime import UTC, datetime
from typing import Any

from .config import AzureDevOpsConfig
from .consolidated_scaffold import upsert_consolidated_comment
from .helpers import build_pr_base_url
from .review_scaffold_activity import (
    _format_activity_log_entry,
    _post_activity_log_entry,
)
from .review_scaffold_commit_state import _build_rereview_skip_message, _resolve_commit_thread_id
from .review_scaffold_fresh import _fresh_scaffold
from .review_scaffold_incremental import _incremental_rescaffold
from .review_scaffold_model_reply import _post_or_update_model_reply
from .review_scaffold_recovery import _try_recover_state_from_pr_threads
from .review_scaffold_replies import _post_reply
from .review_scaffold_session_state import (
    _check_session_status,
    _create_session,
    _handle_resume_stale,
    _reset_files_for_rereview,
)
from .review_state import ReviewState, load_review_state, save_review_state


def _handle_already_reviewed(
    state: ReviewState,
    force_rereview: bool,
    dry_run: bool,
    rebase_conflicts_changed: bool,
    effective_model: str,
    short_hash: str,
    pull_request_id: int,
    commit_hash: str | None,
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    config: AzureDevOpsConfig,
    repo_id: str,
    now: datetime,
) -> ReviewState:
    if not force_rereview:
        print(
            f"Commit {short_hash} already reviewed by {effective_model} for PR {pull_request_id}. "
            "Skipping (pass --force-rereview to override)."
        )
        if not dry_run:
            commit_thread_id = _resolve_commit_thread_id(state, commit_hash)
            if commit_thread_id > 0:
                try:
                    _post_reply(
                        requests_module,
                        headers,
                        threads_url,
                        commit_thread_id,
                        _build_rereview_skip_message(short_hash, effective_model, pull_request_id),
                    )
                except Exception as exc:
                    print(f"Warning: Could not post re-review skip notice: {exc}", file=sys.stderr)
        if rebase_conflicts_changed and not dry_run:
            save_review_state(state)
        return state

    print(
        f"Force re-review requested for commit {short_hash} by {effective_model} "
        f"(PR {pull_request_id}); resetting review state and updating the comment in place."
    )
    if dry_run:
        return state
    _reset_files_for_rereview(state, effective_model)
    state.sessions.append(_create_session(effective_model, commit_hash=commit_hash, now=now))
    try:
        upsert_consolidated_comment(
            state=state,
            config=config,
            repo_id=repo_id,
            requests_module=requests_module,
            headers=headers,
        )
    except Exception as exc:
        print(f"Warning: Could not update consolidated review comment: {exc}", file=sys.stderr)
    save_review_state(state)
    return state


def _handle_in_progress(
    state: ReviewState,
    effective_model: str,
    short_hash: str,
    commit_hash: str | None,
    pull_request_id: int,
    dry_run: bool,
    rebase_conflicts_changed: bool,
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    now: datetime,
) -> None:
    active_session = next(
        (
            session
            for session in state.sessions
            if session.modelId == effective_model
            and session.status == "in_progress"
            and (session.commitHash or "") == (commit_hash or "")
        ),
        None,
    )
    active_id = active_session.sessionId if active_session else "unknown"
    active_start = active_session.startedUtc if active_session else "unknown"
    print(f"Review already in progress for commit {short_hash} by {effective_model} (session {active_id}). Aborting.")
    if not dry_run and state.activityLogThreadId:
        seq = len(state.sessions) + 1
        detail = (
            f"A review session is currently in progress (session `{active_id}` started at {active_start}). Aborting."
        )
        entry = _format_activity_log_entry(
            "⚠️", "In Progress", now.isoformat(), effective_model, short_hash, "n/a", detail, seq
        )
        try:
            _post_activity_log_entry(
                requests_module,
                headers,
                threads_url,
                state.activityLogThreadId,
                entry,
            )
        except Exception as exc:
            print(f"Warning: Could not post activity log entry: {exc}", file=sys.stderr)
    if rebase_conflicts_changed and not dry_run:
        save_review_state(state)


def _handle_different_model(
    state: ReviewState,
    effective_model: str,
    commit_hash: str | None,
    pull_request_id: int,
    dry_run: bool,
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    base_url: str,
    now: datetime,
) -> ReviewState:
    print(f"Additional reviewer ({effective_model}) joining review for PR {pull_request_id}.")
    if dry_run:
        return state
    new_session = _create_session(effective_model, commit_hash=commit_hash, now=now)
    state.sessions.append(new_session)
    save_review_state(state)
    try:
        _post_or_update_model_reply(
            requests_module,
            headers,
            threads_url,
            state,
            commit_hash,
            effective_model,
            base_url,
            now,
        )
        save_review_state(state)
    except Exception as exc:
        print(f"Warning: Could not post additional-model review reply: {exc}", file=sys.stderr)
    if state.activityLogThreadId:
        entry = _format_activity_log_entry(
            "🤝",
            "Additional Reviewer",
            now.isoformat(),
            effective_model,
            (commit_hash or "unknown")[:7],
            new_session.sessionId,
            "Additional reviewer joining existing review for this commit.",
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


def _handle_complete_review_state(
    state: ReviewState,
    pull_request_id: int,
    files: list[str],
    config: AzureDevOpsConfig,
    repo_id: str,
    repo_name: str,
    latest_iteration_id: int,
    requests_module: Any,
    headers: dict[str, str],
    dry_run: bool,
    commit_hash: str | None,
    effective_model: str,
    rebase_conflicts: bool,
    force_rereview: bool,
    now: datetime,
) -> tuple[bool, ReviewState | None]:
    """Route a complete saved state through its commit/model idempotency path."""
    status = _check_session_status(state, commit_hash, effective_model, now=now)
    threads_url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "threads")
    base_url = build_pr_base_url(config, pull_request_id)
    short_hash = (commit_hash or "unknown")[:7]
    rebase_conflicts_changed = state.rebaseConflicts != rebase_conflicts
    state.rebaseConflicts = rebase_conflicts

    if status == "already_reviewed":
        return True, _handle_already_reviewed(
            state,
            force_rereview,
            dry_run,
            rebase_conflicts_changed,
            effective_model,
            short_hash,
            pull_request_id,
            commit_hash,
            requests_module,
            headers,
            threads_url,
            config,
            repo_id,
            now,
        )
    if status == "in_progress":
        _handle_in_progress(
            state,
            effective_model,
            short_hash,
            commit_hash,
            pull_request_id,
            dry_run,
            rebase_conflicts_changed,
            requests_module,
            headers,
            threads_url,
            now,
        )
        return True, None
    if status == "resume_stale":
        return True, _handle_resume_stale(
            state,
            effective_model,
            commit_hash,
            pull_request_id,
            dry_run,
            requests_module,
            headers,
            threads_url,
            now,
        )
    if status == "different_model":
        return True, _handle_different_model(
            state,
            effective_model,
            commit_hash,
            pull_request_id,
            dry_run,
            requests_module,
            headers,
            threads_url,
            base_url,
            now,
        )
    if status == "different_commit":
        return True, _incremental_rescaffold(
            existing_state=state,
            pull_request_id=pull_request_id,
            files=files,
            config=config,
            repo_id=repo_id,
            repo_name=repo_name,
            latest_iteration_id=latest_iteration_id,
            requests_module=requests_module,
            headers=headers,
            dry_run=dry_run,
            commit_hash=commit_hash,
            model_id=effective_model,
            now=now,
            rebase_conflicts=rebase_conflicts,
        )
    if status == "first_review":
        print(f"Scaffolding already exists for PR {pull_request_id}. Skipping.")
        if rebase_conflicts_changed and not dry_run:
            save_review_state(state)
        return True, state
    return False, None


def scaffold_review_threads(
    pull_request_id: int,
    files: list[str],
    config: AzureDevOpsConfig,
    repo_id: str,
    repo_name: str,
    latest_iteration_id: int,
    requests_module: Any,
    headers: dict[str, str],
    dry_run: bool = False,
    commit_hash: str | None = None,
    model_id: str | None = None,
    rebase_conflicts: bool = False,
    force_rereview: bool = False,
) -> ReviewState | None:
    """Scaffold a per-commit consolidated review thread and initialise file state.

    Creates **one top-level Azure DevOps thread per reviewed commit** rather than
    per-file or per-PR threads.  File content is rendered inline within that
    single commit thread (lightweight headline while in progress; full content
    once all files are reviewed).  Code suggestions continue to be posted as
    separate line-anchored threads.

    Commit-hash-based idempotency:
      - Same commit, same model, review complete, no ``force_rereview``
        → skip; post a ``rereview-skipped`` reply on the commit thread.
      - Same commit, same model, review complete, ``force_rereview=True``
        → reset file state to ``unreviewed``, re-render the commit comment
        in place.
      - Same commit, same model, in progress (< 2h) → abort, post warning.
      - Same commit, same model, stale session (≥ 2h) → resume.
      - Same commit, different model → post (or update in place) a
        ``model-review`` reply within the existing commit thread; no
        ``force_rereview`` flag needed.
      - Different commit → archive the prior commit into ``commitComments``
        and POST a fresh thread for the new commit.

    An absent or incomplete state file (``overallSummary.threadId == 0``)
    triggers a full re-scaffold from scratch.

    Args:
        pull_request_id: PR ID.
        files: List of file paths to scaffold threads for.
        config: Azure DevOps configuration.
        repo_id: Repository ID (GUID).
        repo_name: Repository name.
        latest_iteration_id: Latest iteration ID for the PR.
        requests_module: Injected requests module (for testability).
        headers: Auth headers dict.
        dry_run: If True, print the plan without making API calls.
        commit_hash: Commit hash (``lastMergeSourceCommit.commitId``) from
            the Azure DevOps PR API.
        model_id: AI model identifier that initiated scaffolding.
        rebase_conflicts: True if rebase conflicts were detected during checkout.
        force_rereview: When ``True``, override the same-commit/same-model
            skip and re-review from scratch.

    Returns:
        ReviewState with the consolidated thread recorded.  Returns the
        existing state when scaffolding is skipped (already reviewed by the
        same model on the same commit) or when the different-model path
        completes without re-scaffolding.  Returns ``None`` when
        ``dry_run=True`` or when a recent same-model session is already in
        progress (aborted to avoid duplicate reviews).
    """
    effective_model = model_id or "unknown"
    now = datetime.now(UTC)

    # -------------------------------------------------------------------
    # Idempotency check: load existing state and decide on action
    # -------------------------------------------------------------------
    existing_state: ReviewState | None = None
    try:
        existing_state = load_review_state(pull_request_id)
    except FileNotFoundError:
        # A missing review-state file means this pull request has no prior state.
        existing_state = None

    if existing_state is not None and existing_state.overallSummary.threadId != 0:
        handled, result = _handle_complete_review_state(
            existing_state,
            pull_request_id,
            files,
            config,
            repo_id,
            repo_name,
            latest_iteration_id,
            requests_module,
            headers,
            dry_run,
            commit_hash,
            effective_model,
            rebase_conflicts,
            force_rereview,
            now,
        )
        if handled:
            return result

    elif existing_state is not None and existing_state.overallSummary.threadId == 0:
        print(f"Incomplete scaffolding detected for PR {pull_request_id}. Re-scaffolding from scratch.")

    # -------------------------------------------------------------------
    # First-time scaffolding (or incomplete state re-scaffold)
    # -------------------------------------------------------------------
    # Before creating new threads, check if the PR already has agdt-marker
    # threads (e.g., from a prior review session whose state.json was lost).
    # If found, recover state from them to avoid creating duplicate threads.
    if not dry_run:
        recovered = _try_recover_state_from_pr_threads(
            pull_request_id=pull_request_id,
            files=files,
            config=config,
            repo_id=repo_id,
            repo_name=repo_name,
            latest_iteration_id=latest_iteration_id,
            requests_module=requests_module,
            headers=headers,
            commit_hash=commit_hash,
            model_id=effective_model,
            now=now,
            rebase_conflicts=rebase_conflicts,
        )
        if recovered is not None:
            return recovered

    return _fresh_scaffold(
        pull_request_id=pull_request_id,
        files=files,
        config=config,
        repo_id=repo_id,
        repo_name=repo_name,
        latest_iteration_id=latest_iteration_id,
        requests_module=requests_module,
        headers=headers,
        dry_run=dry_run,
        commit_hash=commit_hash,
        model_id=effective_model,
        now=now,
        rebase_conflicts=rebase_conflicts,
    )
