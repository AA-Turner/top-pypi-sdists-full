"""Single-writer consolidated-comment refresh from the answer ledger (P3, §15.3).

``agdt-pr-review-refresh-comment`` is the orchestrator's live progress refresh
during the *delegate* phase. In one serial pass under the refresh/submit pipeline
lock it: reads the answer ledger once, overlays the accepted outcomes onto a copy
of the terminal review state (driving the lightweight
``N approved · M need work · X/Y reviewed`` headline), and PATCHes the current
commit's consolidated comment once via
:func:`agentic_devtools.cli.azure_devops.consolidated_scaffold.upsert_consolidated_comment`
with ``force_in_progress=True``.

The refresh **never** mutates terminal review status — only submit does (§15.3).
It overlays onto a deep copy for rendering and persists only the operational
comment metadata produced by the upsert (thread/comment ids, continuation ids,
and the per-commit registry), leaving every ``FileEntry`` status untouched. It is
idempotent / order-independent (re-running renders the same content), throttled
(every N accepted answers / T seconds, bypassed by ``--force`` / ``--final``),
403-safe (delegated to the upsert), and mutually exclusive with submit (both
acquire the pipeline lock).

When called with ``final=True`` (submit's completion render) it skips the ledger
overlay and renders the **terminal** state at full fidelity
(``force_in_progress=False``) so submit's posted verdicts, suggestion threads, and
smart-cutoff continuations are all rendered.
"""

from __future__ import annotations

import argparse
import copy
import sys
import time
from collections.abc import Callable
from typing import Any

import requests

from ...file_locking import FileLockError
from ...state import get_pull_request_id, get_value, is_dry_run, set_value
from .auth import get_auth_headers, get_pat
from .config import AzureDevOpsConfig
from .consolidated_scaffold import upsert_consolidated_comment
from .pr_review_ledger import (
    latest_accepted_by_file_key,
    read_ledger_entries,
    resolve_answers_dir,
    summarize_accepted,
)
from .pr_review_pipeline_lock import pipeline_lock
from .review_state import (
    ReviewStatus,
    load_review_state,
    normalize_file_path,
    save_review_state,
)

#: State keys recording the last refresh's accepted count / timestamp for throttling.
REFRESH_LAST_COUNT_KEY = "review.refresh.last_accepted_count"
REFRESH_LAST_TIME_KEY = "review.refresh.last_utc"

#: Throttle defaults: refresh on every accepted answer, no minimum interval. The
#: orchestrator (or a pipeline) can tighten these via ``--every-n`` / ``--min-interval``.
DEFAULT_REFRESH_EVERY_N = 1
DEFAULT_REFRESH_MIN_INTERVAL_SECONDS = 0.0

_COMPLETE_STATUS = "complete"
_APPROVE_OUTCOME = "approve"
_REQUEST_CHANGES_OUTCOME = "request-changes"
_REQUEST_CHANGES_WITH_SUGGESTION_OUTCOME = "request-changes-with-suggestion"
_NEEDS_WORK_OUTCOMES = frozenset({_REQUEST_CHANGES_OUTCOME, _REQUEST_CHANGES_WITH_SUGGESTION_OUTCOME})


def should_refresh(
    accepted_count: int,
    last_count: int | None,
    now_ts: float,
    last_ts: float | None,
    *,
    every_n: int,
    min_interval_seconds: float,
    force: bool,
    final: bool,
) -> bool:
    """Decide whether a refresh PATCH should happen now (throttle predicate).

    Args:
        accepted_count: Current number of accepted answers (ledger).
        last_count: Accepted count at the last refresh (``None`` if never).
        now_ts: Current timestamp (seconds).
        last_ts: Timestamp of the last refresh (``None`` if never).
        every_n: Refresh once the accepted count grows by at least this many.
        min_interval_seconds: Refresh once this many seconds have elapsed.
        force: Bypass the throttle (always refresh).
        final: Completion render — always refresh.

    Returns:
        ``True`` when a refresh should be performed.
    """
    if force or final:
        return True
    if last_count is None or last_ts is None:
        return True
    if accepted_count - last_count >= every_n:
        return True
    if min_interval_seconds <= 0:
        return False
    return (now_ts - last_ts) >= min_interval_seconds


def overlay_ledger_onto_state(state: Any, latest_by_key: dict[str, dict[str, Any]]) -> Any:
    """Overlay accepted-answer outcomes onto *state*'s file statuses (in place).

    Only ``complete`` answers are applied. Each maps its ``filePath`` to the
    matching ``FileEntry`` (by normalized path) and sets its status to
    ``approved`` (outcome ``approve``) or ``needs-work`` (otherwise), plus the
    answer summary when present. Answers for files not present in *state* are
    ignored. Callers must pass a **copy** — this never mutates terminal state.

    Args:
        state: A ``ReviewState`` (copy) whose ``files`` statuses to overlay.
        latest_by_key: Latest accepted ledger entry per ``fileKey``.

    Returns:
        The mutated *state* (for chaining).
    """
    for entry in latest_by_key.values():
        if entry.get("status") != _COMPLETE_STATUS:
            continue
        file_path = entry.get("filePath")
        if not isinstance(file_path, str) or not file_path:
            continue
        file_entry = state.files.get(normalize_file_path(file_path))
        if file_entry is None:
            continue
        outcome = entry.get("outcome")
        if outcome == _APPROVE_OUTCOME:
            file_entry.status = ReviewStatus.APPROVED.value
        elif outcome in _NEEDS_WORK_OUTCOMES:
            file_entry.status = ReviewStatus.NEEDS_WORK.value
        else:
            continue
        summary = entry.get("summary")
        if summary is not None:
            file_entry.summary = summary
    return state


def refresh_core(
    pull_request_id: int,
    *,
    dry_run: bool = False,
    force: bool = False,
    final: bool = False,
    every_n: int = DEFAULT_REFRESH_EVERY_N,
    min_interval_seconds: float = DEFAULT_REFRESH_MIN_INTERVAL_SECONDS,
    requests_module: Any = None,
    now_fn: Callable[[], float] | None = None,
) -> dict[str, Any]:
    """Render + PATCH the consolidated comment once (no pipeline lock held here).

    This is the lock-free core shared by ``agdt-pr-review-refresh-comment`` (which
    acquires the pipeline lock around it) and submit's completion render (which
    already holds the lock).

    Args:
        pull_request_id: The PR to refresh.
        dry_run: Render the intended comment but make no API calls / no save.
        force: Bypass the throttle.
        final: Completion render — render the terminal state at full fidelity
            (no ledger overlay, ``force_in_progress=False``) and bypass throttle.
        every_n: Throttle — refresh once the accepted count grows by this many.
        min_interval_seconds: Throttle — refresh once this many seconds elapse.
        requests_module: Optional ``requests`` module injected into the upsert.
        now_fn: Optional timestamp factory (defaults to ``time.time``).

    Returns:
        A result dict with ``refreshed`` (bool), ``reason``, ``accepted``,
        ``approved`` / ``needsWork`` / ``reviewed`` counts, and ``dryRun``.
    """
    now = now_fn if now_fn is not None else time.time
    answers_dir = resolve_answers_dir(pull_request_id, backfill=not dry_run)
    latest_by_key = latest_accepted_by_file_key(read_ledger_entries(answers_dir))
    summary = summarize_accepted(latest_by_key)
    accepted_count = summary["reviewed"]

    if not final and not should_refresh(
        accepted_count,
        get_value(REFRESH_LAST_COUNT_KEY),
        now(),
        get_value(REFRESH_LAST_TIME_KEY),
        every_n=every_n,
        min_interval_seconds=min_interval_seconds,
        force=force,
        final=final,
    ):
        return {"refreshed": False, "reason": "throttled", "accepted": accepted_count, "dryRun": dry_run, **summary}

    try:
        base_state = load_review_state(pull_request_id, fallback_to_branch=False)
    except FileNotFoundError:
        return {
            "refreshed": False,
            "reason": "no-review-state",
            "accepted": accepted_count,
            "dryRun": dry_run,
            **summary,
        }

    config = AzureDevOpsConfig.from_state()
    repo_id = base_state.repoId
    headers = {} if dry_run else get_auth_headers(get_pat())

    effective_requests_module = requests if requests_module is None else requests_module

    if final:
        upsert_consolidated_comment(
            base_state,
            config,
            repo_id,
            effective_requests_module,
            headers,
            dry_run=dry_run,
            force_in_progress=False,
        )
        if not dry_run:
            save_review_state(base_state)
        return {"refreshed": True, "reason": "final", "accepted": accepted_count, "dryRun": dry_run, **summary}

    render_state = copy.deepcopy(base_state)
    overlay_ledger_onto_state(render_state, latest_by_key)
    upsert_consolidated_comment(
        render_state,
        config,
        repo_id,
        effective_requests_module,
        headers,
        dry_run=dry_run,
        force_in_progress=True,
    )

    if not dry_run:
        # Persist only operational comment metadata from the render copy; the
        # base state's terminal FileEntry statuses are intentionally untouched.
        base_state.overallSummary = render_state.overallSummary
        base_state.commitComments = render_state.commitComments
        save_review_state(base_state)
        set_value(REFRESH_LAST_COUNT_KEY, accepted_count)
        set_value(REFRESH_LAST_TIME_KEY, now())

    return {"refreshed": True, "reason": "updated", "accepted": accepted_count, "dryRun": dry_run, **summary}


def refresh_comment_command() -> None:
    """CLI entry point for ``agdt-pr-review-refresh-comment`` (acquires the lock)."""
    parser = argparse.ArgumentParser(
        description="Refresh the consolidated review comment from the answer ledger (v2 PR review).",
    )
    parser.add_argument("--pr", type=int, default=None, help="Pull request ID (defaults to pull_request_id state).")
    parser.add_argument("--dry-run", action="store_true", help="Render the intended comment; make no API calls.")
    parser.add_argument("--force", action="store_true", help="Bypass the throttle and refresh now.")
    parser.add_argument("--final", action="store_true", help="Completion render of the terminal state (full fidelity).")
    parser.add_argument("--every-n", type=int, default=DEFAULT_REFRESH_EVERY_N, help="Throttle: refresh per N answers.")
    parser.add_argument(
        "--min-interval",
        type=float,
        default=DEFAULT_REFRESH_MIN_INTERVAL_SECONDS,
        help="Throttle: refresh once this many seconds elapse.",
    )
    args = parser.parse_args()

    if args.every_n < 1:
        print("Error: --every-n must be >= 1.", file=sys.stderr)
        sys.exit(2)
    if args.min_interval < 0:
        print("Error: --min-interval must be >= 0.", file=sys.stderr)
        sys.exit(2)

    pr_id = args.pr if args.pr is not None else get_pull_request_id()
    if pr_id is None:
        print("Error: PR ID required (--pr or pull_request_id state).", file=sys.stderr)
        sys.exit(2)

    dry_run = args.dry_run or is_dry_run()
    try:
        with pipeline_lock(pr_id):
            result = refresh_core(
                pr_id,
                dry_run=dry_run,
                force=args.force,
                final=args.final,
                every_n=args.every_n,
                min_interval_seconds=args.min_interval,
            )
    except FileLockError:
        print("Error: another refresh or submit is already in progress for this PR.", file=sys.stderr)
        sys.exit(1)

    state = "refreshed" if result["refreshed"] else f"skipped ({result['reason']})"
    prefix = "[dry-run] " if dry_run else ""
    print(
        f"{prefix}refresh-comment: {state} — "
        f"{result['approved']} approved \u00b7 {result['needsWork']} need work \u00b7 {result['reviewed']} reviewed."
    )
