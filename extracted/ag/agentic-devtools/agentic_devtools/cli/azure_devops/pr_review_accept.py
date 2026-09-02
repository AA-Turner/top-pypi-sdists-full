"""Orchestrator ledger-accept command for the v2 PR review (P3).

``agdt-pr-review-accept-answer`` is the orchestrator's fan-in *accept* action: it
validates a finished per-file answer against its scaffold baseline (reusing the
P2 validation in :mod:`agentic_devtools.cli.azure_devops.pr_review_write`) and
appends it as one line to the append-only answer ledger
(:mod:`agentic_devtools.cli.azure_devops.pr_review_ledger`).

The ledger is the record of "answers accepted" that drives the live progress
line rendered by ``agdt-pr-review-refresh-comment``; it is distinct from terminal
review state, which is mutated only by ``agdt-pr-review-submit`` (plan §15.3).
Only ``complete`` answers may be accepted — ``pending`` / ``needs-info`` answers
are rejected so the live line never claims a review that has not finished.

Exit codes:
    0  answer accepted and appended (or dry-run validated)
    1  answer rejected — stale, malformed, or not complete
    2  IO / argument / artifact-resolution error
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from ...file_locking import FileLockError
from ...state import get_value, is_safe_dir_segment
from .pr_review_ledger import append_ledger_entry, build_ledger_entry, resolve_answers_dir
from .pr_review_write import ANSWER_FILENAME_SUFFIX, validate_answer_write

_COMPLETE_STATUS = "complete"


def _resolve_pull_request_id(arg_pr: int | None) -> int | None:
    """Resolve the PR id from ``--pr`` or the ``pull_request_id`` state key.

    Returns ``None`` (after printing an error) when no usable id is available.
    """
    pr_value = arg_pr if arg_pr is not None else get_value("pull_request_id")
    if pr_value is None:
        print("Error: PR ID required (--pr or pull_request_id state).", file=sys.stderr)
        return None
    if isinstance(pr_value, bool):
        print("Error: pull_request_id must be an integer, not a boolean.", file=sys.stderr)
        return None
    try:
        return int(pr_value)
    except (TypeError, ValueError):
        print("Error: pull_request_id must be an integer.", file=sys.stderr)
        return None


def accept_answer_command() -> None:
    """CLI entry point for ``agdt-pr-review-accept-answer``."""
    parser = argparse.ArgumentParser(
        description="Validate a complete per-file answer and append it to the answer ledger (v2 PR review).",
    )
    parser.add_argument("--file-key", required=True, help="The fileKey of the answer to accept.")
    parser.add_argument(
        "--answer-file",
        default=None,
        help="Optional path to an edited answer JSON to accept (defaults to the scaffolded answer).",
    )
    parser.add_argument("--pr", type=int, default=None, help="Pull request ID (defaults to pull_request_id state).")
    parser.add_argument("--dry-run", action="store_true", help="Validate only; do not append to the ledger.")
    args = parser.parse_args()

    file_key = args.file_key
    if not is_safe_dir_segment(file_key):
        print(f"Error: invalid --file-key {file_key!r} (unsafe path segment).", file=sys.stderr)
        sys.exit(2)

    pull_request_id = _resolve_pull_request_id(args.pr)
    if pull_request_id is None:
        sys.exit(2)

    answers_dir = resolve_answers_dir(pull_request_id)
    scaffold_path = answers_dir / f"{file_key}{ANSWER_FILENAME_SUFFIX}"
    if not scaffold_path.exists():
        print(f"Error: no scaffolded answer for fileKey {file_key!r} at {scaffold_path}.", file=sys.stderr)
        sys.exit(2)
    try:
        scaffold = json.loads(scaffold_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error: could not read scaffold answer {scaffold_path}: {exc}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(scaffold, dict):
        print(f"Error: scaffold answer {scaffold_path} is not a JSON object.", file=sys.stderr)
        sys.exit(2)

    if args.answer_file is not None:
        answer_path = Path(args.answer_file)
        try:
            answer_raw = answer_path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"Error: could not read answer file {answer_path}: {exc}", file=sys.stderr)
            sys.exit(2)
        try:
            answer = json.loads(answer_raw)
        except json.JSONDecodeError as exc:
            print(f"Error: answer file is not valid JSON: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        answer = scaffold

    errors = validate_answer_write(answer, file_key, scaffold)
    if errors:
        print("Error: answer validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    if answer.get("status") != _COMPLETE_STATUS:
        print(
            f"Error: only complete answers can be accepted (fileKey {file_key!r} status={answer.get('status')!r}).",
            file=sys.stderr,
        )
        sys.exit(1)

    accepted_utc = datetime.now(timezone.utc).isoformat()
    entry = build_ledger_entry(answer, accepted_utc)

    if args.dry_run:
        print(f"[dry-run] would accept {file_key} (outcome={answer.get('outcome')}); ledger not modified.")
        return

    try:
        append_ledger_entry(answers_dir, entry)
    except FileLockError as exc:
        print(f"Error: ledger is locked (another accept in progress): {exc}", file=sys.stderr)
        sys.exit(2)
    except OSError as exc:
        print(f"Error: could not append to ledger: {exc}", file=sys.stderr)
        sys.exit(2)
    print(f"Accepted {file_key} (outcome={answer.get('outcome')}): appended to ledger.")
