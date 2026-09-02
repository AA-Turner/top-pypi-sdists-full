"""Aggregate validate + submit of accepted answers (v2 PR review, P3, §15.5/D3).

``agdt-pr-review-submit`` is the orchestrator's one-shot fan-in submit. It reads
the accepted answers from the append-only ledger
(:mod:`agentic_devtools.cli.azure_devops.pr_review_ledger`), re-validates each
one against its scaffold baseline (reusing P2's
:func:`agentic_devtools.cli.azure_devops.pr_review_write.validate_answer_write`,
which rejects stale ``promptHash`` / ``commitHash`` / ``attemptId``), maps each
to a submission item via the explicit
:func:`agentic_devtools.cli.azure_devops.pr_review_submit_mapper.map_answer_to_submission_item`,
and submits them through the **durable serial engine** — ``SubmissionManager`` +
:func:`agentic_devtools.submission_processor.process_submission` (decision D3).
For large batches, per-file comments and state remain durable item operations,
while reviewer/viewed-status updates are deferred and sent as one batch after
the item queue drains; finalization then cascades and renders the shared
summary.

It holds the refresh/submit pipeline lock for the duration so it is mutually
exclusive with ``agdt-pr-review-refresh-comment``. It writes a structured result
file (``answers/submit-result.json``) recording accepted / posted / marked-viewed
/ failed / skipped / stale / retriable, which the orchestrator reads before
advancing to ``decision``.

After a real submit it triggers the completion render via
:func:`agentic_devtools.cli.azure_devops.pr_review_refresh.refresh_core`
(``final=True``) so the now-populated terminal state is rendered at full fidelity
(with smart-cutoff continuations); ``dry_run`` performs no remote mutation (no
enqueue / POST / PATCH / mark-viewed) yet still writes the intended result file
(plan §15.9).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ...background_tasks import run_function_in_background
from ...file_locking import FileLockError
from ...state import get_pull_request_id, get_value, is_dry_run, is_safe_dir_segment, set_value
from ...submission_manager import SubmissionItem, SubmissionManager, SubmissionStatus
from ...submission_processor import create_review_processor
from ...task_state import print_task_tracking_info
from .auth import get_auth_headers, get_pat
from .config import AzureDevOpsConfig
from .consolidated_review import is_review_complete
from .helpers import require_requests
from .pr_review_ledger import (
    latest_accepted_by_file_key,
    read_ledger_entries,
    resolve_answers_dir,
)
from .pr_review_pipeline_lock import pipeline_lock
from .pr_review_submit_mapper import MapperError, map_answer_to_submission_item
from .pr_review_write import ANSWER_FILENAME_SUFFIX, validate_answer_write
from .review_state import complete_active_session, load_review_state, read_modify_write_review_state
from .status_cascade import cascade_overall_summary_update, execute_cascade

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_submit"

SUBMIT_RESULT_FILENAME = "submit-result.json"
SUBMIT_RESULT_SCHEMA_VERSION = 1

_COMPLETE_STATUS = "complete"
_SUBMIT_MAX_RETRIES = 2


def _load_scaffold(answers_dir: Path, file_key: str) -> dict[str, Any] | None:
    """Read the scaffold answer baseline for *file_key*, or ``None`` if unusable."""
    if not is_safe_dir_segment(file_key):
        return None
    path = answers_dir / f"{file_key}{ANSWER_FILENAME_SUFFIX}"
    if not path.exists():
        return None
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return parsed if isinstance(parsed, dict) else None


def classify_accepted_answers(
    latest_by_key: dict[str, dict[str, Any]],
    load_scaffold: Callable[[str], dict[str, Any] | None],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Partition accepted answers into submittable, skipped, and stale buckets.

    Args:
        latest_by_key: Latest accepted ledger entry per ``fileKey``.
        load_scaffold: Callable returning the scaffold baseline for a ``fileKey``
            (``None`` when missing/unreadable).

    Returns:
        ``(submittable, skipped, stale)`` where:

        * *submittable* is a list of ``{"fileKey", "filePath", "item"}`` (the
          mapped submission item ready for the engine);
        * *skipped* is ``{"fileKey", "reason"}`` for non-complete or unmappable
          answers; and
        * *stale* is ``{"fileKey", "errors"}`` for answers that failed validation
          (stale hashes / scope / schema) or have no scaffold baseline.
    """
    submittable: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    stale: list[dict[str, Any]] = []

    for file_key, answer in latest_by_key.items():
        if answer.get("status") != _COMPLETE_STATUS:
            skipped.append({"fileKey": file_key, "reason": f"status:{answer.get('status')}"})
            continue
        scaffold = load_scaffold(file_key)
        if scaffold is None:
            stale.append({"fileKey": file_key, "errors": ["no scaffold baseline found"]})
            continue
        errors = validate_answer_write(answer, file_key, scaffold)
        if errors:
            stale.append({"fileKey": file_key, "errors": errors})
            continue
        try:
            item = map_answer_to_submission_item(answer)
        except MapperError as exc:
            skipped.append({"fileKey": file_key, "reason": f"unmappable: {exc}"})
            continue
        submittable.append({"fileKey": file_key, "filePath": answer.get("filePath"), "item": item})

    return submittable, skipped, stale


def _build_submission_manager(
    pull_request_id: int,
    requests_module: Any,
    defer_shared_updates: bool = False,
) -> SubmissionManager:
    """Build a ``SubmissionManager`` wired to the durable review processor (D3)."""
    review_state = load_review_state(pull_request_id, fallback_to_branch=False)
    repo_id = review_state.repoId
    config = AzureDevOpsConfig.from_state()
    headers = get_auth_headers(get_pat())
    if defer_shared_updates:
        processor = create_review_processor(
            config,
            headers,
            repo_id,
            requests_module=requests_module,
            defer_shared_updates=True,
        )
    else:
        processor = create_review_processor(config, headers, repo_id, requests_module=requests_module)
    return SubmissionManager(processor=processor, max_retries=_SUBMIT_MAX_RETRIES)


def _run_submissions(
    manager: SubmissionManager,
    pull_request_id: int,
    submittable: list[dict[str, Any]],
    finalize_shared_updates: bool = False,
    requests_module: Any = None,
) -> dict[str, dict[str, Any]]:
    """Enqueue every submittable item, drain the queue, and collect outcomes.

    Returns a mapping of ``fileKey`` to ``{"status", "error", "attempts"}`` where
    ``status`` is ``"posted"`` (engine succeeded) or ``"failed"`` (exhausted).
    When ``finalize_shared_updates`` is true, successful files are marked as
    reviewed through one batch operation after the item queue drains, followed
    by an overall-summary status cascade.
    """
    id_to_key: dict[str, str] = {}
    for entry in submittable:
        item = entry["item"]
        submission: SubmissionItem = manager.enqueue(
            pull_request_id,
            item["file_path"],
            item["outcome"],
            item["summary"],
            item["suggestions"],
        )
        id_to_key[submission.id] = entry["fileKey"]

    manager.shutdown(wait=True)

    outcomes: dict[str, dict[str, Any]] = {}
    for submission_id, file_key in id_to_key.items():
        final = manager.get_item(submission_id)
        if final is not None and final.status == SubmissionStatus.SUCCEEDED:
            outcomes[file_key] = {"status": "posted", "error": None, "attempts": final.attempts}
        elif final is not None:
            outcomes[file_key] = {"status": "failed", "error": final.error_message, "attempts": final.attempts}
        else:
            outcomes[file_key] = {"status": "failed", "error": "submission item lost", "attempts": 0}
    if not finalize_shared_updates:
        return outcomes

    successful_entries = [
        entry for entry in submittable if outcomes.get(entry["fileKey"], {}).get("status") == "posted"
    ]
    if not successful_entries:
        return outcomes

    def _normalize_or_raw(path: str) -> str:
        return path  # pragma: no cover

    try:
        from .mark_reviewed import MarkFilesReviewedResult, mark_files_reviewed, normalize_repo_path

        def _normalize_or_raw(path: str) -> str:
            return normalize_repo_path(path) or path

        review_state = load_review_state(pull_request_id, fallback_to_branch=False)
        config = AzureDevOpsConfig.from_state()
        mark_result = mark_files_reviewed(
            [entry["item"]["file_path"] for entry in successful_entries],
            pull_request_id,
            config,
            review_state.repoId,
            return_details=True,
        )
        if not isinstance(mark_result, MarkFilesReviewedResult):  # pragma: no cover
            raise TypeError("mark_files_reviewed(return_details=True) returned a non-detailed result")
        failed_paths = set(mark_result.failed_paths)
        marked = not failed_paths
        error = mark_result.error or "Failed to mark reviewed files for the pull request"
    except Exception as exc:
        marked = False
        failed_paths = {_normalize_or_raw(entry["item"]["file_path"]) for entry in successful_entries}
        error = str(exc)

    if not marked:
        for entry in successful_entries:
            normalized_path = _normalize_or_raw(entry["item"]["file_path"])
            if normalized_path not in failed_paths:
                continue
            file_key = entry["fileKey"]
            previous = outcomes[file_key]
            outcomes[file_key] = {
                "status": "failed",
                "error": error,
                "attempts": previous.get("attempts", 0),
            }
        return outcomes

    try:
        with read_modify_write_review_state(pull_request_id) as review_state:
            cascade_result = execute_cascade(
                patch_operations=cascade_overall_summary_update(
                    review_state,
                    f"{review_state.organization.rstrip('/')}/{review_state.project}/_git/"
                    f"{review_state.repoName}/pullrequest/{pull_request_id}",
                ),
                requests_module=requests_module or require_requests(),
                headers=get_auth_headers(get_pat()),
                config=AzureDevOpsConfig.from_state(),
                repo_id=review_state.repoId,
                pull_request_id=pull_request_id,
                state=review_state,
            )
            if cascade_result.blocked:
                raise RuntimeError(f"Failed to finalize overall summary: {cascade_result.blocked}")
    except Exception as exc:
        for entry in successful_entries:
            file_key = entry["fileKey"]
            previous = outcomes[file_key]
            outcomes[file_key] = {
                "status": "failed",
                "error": str(exc),
                "attempts": previous.get("attempts", 0),
            }
    return outcomes


def build_submit_result(
    *,
    pr_id: int,
    commit_hash: str,
    dry_run: bool,
    submittable: list[dict[str, Any]],
    skipped: list[dict[str, Any]],
    stale: list[dict[str, Any]],
    item_outcomes: dict[str, dict[str, Any]],
    generated_utc: str,
) -> dict[str, Any]:
    """Build the structured submit result the orchestrator reads before advancing.

    Args:
        pr_id: Pull request ID.
        commit_hash: Reviewed commit hash (informational).
        dry_run: Whether this was a dry run (no remote mutation).
        submittable: The mapped submittable entries (``fileKey`` / ``filePath``).
        skipped: Skipped entries (non-complete / unmappable).
        stale: Stale/invalid entries (failed validation / no scaffold).
        item_outcomes: Per-``fileKey`` engine outcome (empty for dry runs / when
            nothing was submitted).
        generated_utc: ISO-8601 UTC timestamp for the result.

    Returns:
        The structured result dict.
    """
    accepted = [entry["fileKey"] for entry in submittable]
    key_to_path = {entry["fileKey"]: entry["filePath"] for entry in submittable}

    posted: list[str] = []
    failed: list[dict[str, Any]] = []
    retriable: list[str] = []
    for file_key in accepted:
        outcome = item_outcomes.get(file_key)
        if outcome is None:
            continue
        if outcome["status"] == "posted":
            posted.append(file_key)
        else:
            failed.append(
                {
                    "fileKey": file_key,
                    "filePath": key_to_path.get(file_key),
                    "error": outcome.get("error"),
                    "attempts": outcome.get("attempts", 0),
                }
            )
            retriable.append(file_key)

    counts = {
        "accepted": len(accepted),
        "posted": len(posted),
        "markedViewed": len(posted),
        "failed": len(failed),
        "skipped": len(skipped),
        "stale": len(stale),
    }
    return {
        "schemaVersion": SUBMIT_RESULT_SCHEMA_VERSION,
        "prId": pr_id,
        "commitHash": commit_hash,
        "dryRun": dry_run,
        "generatedUtc": generated_utc,
        "counts": counts,
        "accepted": accepted,
        "posted": posted,
        "markedViewed": posted,
        "failed": failed,
        "skipped": skipped,
        "stale": stale,
        "retriable": retriable,
    }


def write_submit_result(answers_dir: Path, result: dict[str, Any]) -> Path:
    """Atomically write *result* to ``answers/submit-result.json`` and return its path."""
    answers_dir.mkdir(parents=True, exist_ok=True)
    target = answers_dir / SUBMIT_RESULT_FILENAME
    tmp_path = target.parent / f"{SUBMIT_RESULT_FILENAME}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
    try:
        tmp_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp_path, target)
    except OSError:
        tmp_path.unlink(missing_ok=True)
        raise
    return target


def read_submit_result(answers_dir: Path) -> dict[str, Any] | None:
    """Read ``answers/submit-result.json`` and return its parsed contents, or ``None`` if absent or unreadable."""
    target = answers_dir / SUBMIT_RESULT_FILENAME
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    return data


def _finalize_consolidated_comment(pull_request_id: int, requests_module: Any) -> None:
    """Render the completion (full-fidelity) consolidated comment after submit.

    Delegates to :func:`agentic_devtools.cli.azure_devops.pr_review_refresh.refresh_core`
    with ``final=True`` so the now-populated terminal review state (posted
    verdicts + suggestion threads) is rendered at full fidelity with smart-cutoff
    continuations. Imported lazily to avoid a module-load import cycle.
    """
    from .pr_review_refresh import refresh_core

    refresh_core(
        pull_request_id,
        dry_run=False,
        force=True,
        final=True,
        requests_module=requests_module,
    )


def pr_review_submit(
    *,
    pull_request_id: int | None = None,
    dry_run: bool | None = None,
    requests_module: Any = None,
    now_fn: Callable[[], str] | None = None,
) -> int:
    """Worker: validate + submit all accepted answers; write the result file.

    Args:
        pull_request_id: PR ID (defaults to ``pull_request_id`` state).
        dry_run: Force dry-run mode (defaults to the ``dry_run`` state).
        requests_module: Optional ``requests`` module injected into the processor.
        now_fn: Optional timestamp factory (for deterministic tests).

    Returns:
        Process exit code: ``0`` success, ``1`` one or more failures / locked,
        ``2`` missing PR id.
    """
    now = now_fn if now_fn is not None else (lambda: datetime.now(UTC).isoformat())

    pr_id = pull_request_id if pull_request_id is not None else get_pull_request_id()
    if pr_id is None:
        print("Error: PR ID required (pull_request_id state).", file=sys.stderr)
        return 2
    effective_dry_run = is_dry_run() if dry_run is None else dry_run

    try:
        with pipeline_lock(pr_id):
            answers_dir = resolve_answers_dir(pr_id, backfill=not effective_dry_run)
            ledger_entries = read_ledger_entries(answers_dir)
            latest_by_key = latest_accepted_by_file_key(ledger_entries)
            commit_hash = (
                next(
                    (e["commitHash"] for e in latest_by_key.values() if e.get("commitHash")),
                    None,
                )
                or get_value("review.commit_hash_short")
                or ""
            )
            submittable, skipped, stale = classify_accepted_answers(
                latest_by_key,
                lambda file_key: _load_scaffold(answers_dir, file_key),
            )
            item_outcomes: dict[str, dict[str, Any]] = {}
            if not effective_dry_run and submittable:
                manager = _build_submission_manager(pr_id, requests_module, defer_shared_updates=True)
                item_outcomes = _run_submissions(
                    manager,
                    pr_id,
                    submittable,
                    finalize_shared_updates=True,
                    requests_module=requests_module,
                )
            result = build_submit_result(
                pr_id=pr_id,
                commit_hash=commit_hash,
                dry_run=effective_dry_run,
                submittable=submittable,
                skipped=skipped,
                stale=stale,
                item_outcomes=item_outcomes,
                generated_utc=now(),
            )
            result_path = write_submit_result(answers_dir, result)
            if not effective_dry_run and submittable:
                try:
                    if (
                        not skipped
                        and not stale
                        and all(
                            item_outcomes.get(entry["fileKey"], {}).get("status") == "posted" for entry in submittable
                        )
                    ):
                        with read_modify_write_review_state(pr_id) as _rs:
                            if is_review_complete(_rs):
                                complete_active_session(_rs)
                except Exception as exc:
                    print(f"Warning: could not mark review session completed: {exc}", file=sys.stderr)
                try:
                    _finalize_consolidated_comment(pr_id, requests_module)
                except Exception as exc:  # best-effort; result already persisted
                    print(f"Warning: completion render failed (result already saved): {exc}", file=sys.stderr)
    except FileLockError:
        print("Error: another refresh or submit is already in progress for this PR.", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print("Error: review-state.json not found for this PR.", file=sys.stderr)
        return 2

    counts = result["counts"]
    prefix = "[dry-run] " if effective_dry_run else ""
    print(
        f"{prefix}submit: {counts['accepted']} accepted, {counts['posted']} posted, "
        f"{counts['failed']} failed, {counts['skipped']} skipped, {counts['stale']} stale. "
        f"Result: {result_path}"
    )
    return 1 if counts["failed"] else 0


def pr_review_submit_command() -> None:
    """CLI entry point for ``agdt-pr-review-submit`` (background by default)."""
    parser = argparse.ArgumentParser(
        description="Validate accepted answers and submit them via the durable engine (v2 PR review).",
    )
    parser.add_argument("--pr", type=int, default=None, help="Pull request ID (defaults to pull_request_id state).")
    parser.add_argument("--dry-run", action="store_true", help="Validate + render intended ops; no remote mutation.")
    parser.add_argument("--inline", action="store_true", help="Run synchronously instead of as a background task.")
    args = parser.parse_args()

    pr_id = args.pr if args.pr is not None else get_pull_request_id()
    if pr_id is None:
        print("Error: PR ID required (--pr or pull_request_id state).", file=sys.stderr)
        sys.exit(2)
    set_value("pull_request_id", pr_id)

    if args.dry_run or args.inline:
        sys.exit(pr_review_submit(pull_request_id=pr_id, dry_run=True if args.dry_run else None))

    task = run_function_in_background(_MODULE, "pr_review_submit", command_display_name="agdt-pr-review-submit")
    print_task_tracking_info(task, f"Submitting accepted answers for PR {pr_id}")
