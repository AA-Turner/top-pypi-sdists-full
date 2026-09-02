"""Progress counts for the v2 PR review flow (manifest total + answer ledger).

Sources the authoritative in-scope file *total* from the P1 ``manifest.json``
(falling back to the count of scaffolded ``answers/<fileKey>.answer.json`` files)
and the *reviewed* count from the P3 answer ledger. This replaces the retired
``queue.json`` / ``get_queue_status`` progress source for the v2 flow.

``manifest.json`` and the blank answer files are both written during review
*setup* (``generate_v2_review_artifacts``), before the ``delegate`` step accepts
any answers, so the total is correct from the start (equal to the number of
in-scope files, not 0).
"""

from __future__ import annotations

import json
from pathlib import Path

from .pr_review_ledger import (
    latest_accepted_by_file_key,
    read_ledger_entries,
    resolve_answers_dir,
    summarize_accepted,
)

#: Manifest filename written by ``generate_v2_review_artifacts`` (P1).
MANIFEST_FILENAME = "manifest.json"

#: Suffix of the per-file blank answer files scaffolded during setup (P3).
ANSWER_FILE_SUFFIX = ".answer.json"


def resolve_manifest_path(pull_request_id: int) -> Path:
    """Resolve the ``manifest.json`` path for a PR's review artifacts.

    The manifest lives one level above the ``answers/`` directory under
    ``<state_dir>/pull-request-review/<dir>/manifest.json``.

    Args:
        pull_request_id: The pull request ID whose artifacts to resolve.

    Returns:
        The manifest path (not guaranteed to exist yet).
    """
    return resolve_answers_dir(pull_request_id).parent / MANIFEST_FILENAME


def count_in_scope_files(pull_request_id: int) -> int:
    """Return the authoritative count of in-scope files for the review.

    Prefers ``manifest.json`` (``len(files)``); falls back to the number of
    scaffolded ``answers/<fileKey>.answer.json`` files when the manifest is
    missing or unreadable; returns 0 when neither artifact is present.

    Args:
        pull_request_id: The pull request ID whose in-scope files to count.

    Returns:
        The number of in-scope files (0 when no artifact is available).
    """
    manifest_path = resolve_manifest_path(pull_request_id)
    if manifest_path.exists():
        try:
            with open(manifest_path, encoding="utf-8") as handle:
                manifest = json.load(handle)
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            manifest = None
        if isinstance(manifest, dict):
            files = manifest.get("files")
            if isinstance(files, list):
                return len(files)
    # Fallback: count the blank per-file answer skeletons written at setup.
    answers_dir = resolve_answers_dir(pull_request_id)
    if answers_dir.is_dir():
        return sum(1 for _ in answers_dir.glob(f"*{ANSWER_FILE_SUFFIX}"))
    return 0


def ledger_reviewed_count(pull_request_id: int) -> int:
    """Return the count of accepted, complete answers from the answer ledger.

    Collapses the append-only ledger to the latest accepted attempt per
    ``fileKey`` and counts the ``complete`` answers (approve / request-changes).

    Args:
        pull_request_id: The pull request ID whose ledger to summarize.

    Returns:
        The number of reviewed (accepted, complete) files.
    """
    answers_dir = resolve_answers_dir(pull_request_id)
    entries = read_ledger_entries(answers_dir)
    latest = latest_accepted_by_file_key(entries)
    return int(summarize_accepted(latest)["reviewed"])


def compute_review_progress(pull_request_id: int) -> dict[str, object]:
    """Compute v2 PR-review progress counts from manifest total + answer ledger.

    Replaces the retired ``get_queue_status`` for the v2 flow.

    The returned ``all_complete`` preserves the exact ``delegate ->
    consolidate-and-submit`` gate: it is True only when there is at least one
    in-scope file and every in-scope file has an accepted, complete answer. A
    ledger that reports more reviewed files than the manifest contains (e.g.
    stale accepted entries for files no longer in scope after a new push) falls
    back to the baseline so the workflow never advances prematurely. Requiring
    ``total > 0`` also guards against a missing manifest spuriously reading a
    total of 0 and auto-advancing with no review performed.

    Args:
        pull_request_id: The pull request ID whose progress to compute.

    Returns:
        A dict with ``total_count`` / ``completed_count`` / ``pending_count`` /
        ``all_complete``.
    """
    total = count_in_scope_files(pull_request_id)
    reviewed = ledger_reviewed_count(pull_request_id)
    if 0 <= reviewed <= total:
        completed = reviewed
        pending = total - reviewed
    else:
        completed = 0
        pending = total
    all_complete = total > 0 and pending == 0
    return {
        "total_count": total,
        "completed_count": completed,
        "pending_count": pending,
        "all_complete": all_complete,
    }
