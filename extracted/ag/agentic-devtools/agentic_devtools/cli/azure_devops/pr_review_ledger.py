"""Append-only answer ledger for the v2 PR review fan-in (P3).

The ledger (``answers/ledger.jsonl``) records each *accepted* answer on its own
line via atomic, locked append. It is **distinct** from the terminal
``review-state.json``: the ledger is the record of "answers accepted" (it drives
the live ``N approved · M need work · X/Y reviewed`` line rendered by
``agdt-pr-review-refresh-comment``), while terminal review state is mutated
**only** by ``agdt-pr-review-submit`` (plan §15.3).

"Latest accepted attempt for a ``fileKey`` wins": a re-spawn appends a new line
carrying a fresh ``attemptId`` and supersedes earlier lines for the same key.
:func:`latest_accepted_by_file_key` collapses the append-only log to the latest
entry per key, so the ledger is order-independent and idempotent to read.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ...file_locking import locked_file
from ...state import get_state_dir, get_value
from .helpers import resolve_review_artifact_dir_name

LEDGER_FILENAME = "ledger.jsonl"

#: Lock timeout (seconds) for the append critical section.
_LEDGER_LOCK_TIMEOUT_SECONDS = 10.0

#: Suffix for the sidecar lock file guarding atomic appends.
_LEDGER_LOCK_SUFFIX = ".lock"

#: Answer status that marks an accepted answer as a finished review (counts
#: toward the ``X/Y reviewed`` progress line). Non-complete statuses
#: (``pending`` / ``needs-info`` / ``failed``) are recorded but not counted.
_COMPLETE_STATUS = "complete"

_APPROVE_OUTCOME = "approve"
_NEEDS_WORK_OUTCOMES = frozenset({"request-changes", "request-changes-with-suggestion"})


def resolve_answers_dir(pull_request_id: int, *, backfill: bool = True) -> Path:
    """Resolve the canonical ``answers/`` directory for a PR's review artifacts.

    Mirrors the resolution used by ``agdt-file-review-write`` so the ledger lives
    alongside the per-file answer JSONs under
    ``<state_dir>/pull-request-review/<dir>/answers``.

    When the ``review.commit_hash_short`` state key is absent (e.g. it was
    written to a different scope after a bootstrap re-scope), resolution
    falls back via :func:`resolve_review_artifact_dir_name` so discovery and
    self-healing stay centralized (#1182).

    Args:
        pull_request_id: The pull request ID whose artifacts to resolve.
        backfill: Whether artifact-directory discovery may backfill
            ``review.commit_hash_short`` into state while resolving.

    Returns:
        The ``answers`` directory path (not guaranteed to exist yet).
    """
    state_dir = get_state_dir()
    commit_hash_short = get_value("review.commit_hash_short")
    dir_name = resolve_review_artifact_dir_name(pull_request_id, commit_hash_short, backfill=backfill)
    return state_dir / "pull-request-review" / dir_name / "answers"


def ledger_path(answers_dir: Path) -> Path:
    """Return the ledger file path inside *answers_dir*."""
    return answers_dir / LEDGER_FILENAME


def build_ledger_entry(answer: dict[str, Any], accepted_utc: str) -> dict[str, Any]:
    """Build a ledger line from an accepted answer.

    The full accepted answer is preserved (so submit can re-validate it against
    the scaffold baseline) with an ``acceptedUtc`` timestamp added.

    Args:
        answer: The accepted answer dict (plan §9 schema).
        accepted_utc: ISO-8601 UTC timestamp of acceptance.

    Returns:
        A shallow copy of *answer* with ``acceptedUtc`` set.
    """
    entry = dict(answer)
    entry["acceptedUtc"] = accepted_utc
    return entry


def append_ledger_entry(answers_dir: Path, entry: dict[str, Any]) -> None:
    """Atomically append one *entry* as a JSON line to the ledger.

    The append is serialized by an exclusive lock on a sidecar ``.lock`` file so
    concurrent writers never interleave a partial line. The directory is created
    if missing.

    Args:
        answers_dir: The ``answers/`` directory holding the ledger.
        entry: The ledger entry to append (serialized as one JSON line).
    """
    answers_dir.mkdir(parents=True, exist_ok=True)
    lock_path = answers_dir / (LEDGER_FILENAME + _LEDGER_LOCK_SUFFIX)
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    with locked_file(lock_path, mode="r+", exclusive=True, timeout=_LEDGER_LOCK_TIMEOUT_SECONDS):
        with open(ledger_path(answers_dir), "a", encoding="utf-8") as handle:
            handle.write(line)


def read_ledger_entries(answers_dir: Path) -> list[dict[str, Any]]:
    """Read all ledger entries, tolerating blank or malformed lines.

    A missing ledger yields an empty list. Blank lines, lines that fail to parse
    as JSON, and lines that parse to a non-object are skipped so a partial final
    write (or hand-edit) never breaks the reader.

    Args:
        answers_dir: The ``answers/`` directory holding the ledger.

    Returns:
        The list of entry dicts in append order (oldest first).
    """
    path = ledger_path(answers_dir)
    if not path.exists():
        return []

    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError:
        return []

    entries: list[dict[str, Any]] = []
    for raw_line in raw_text.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            entries.append(parsed)
    return entries


def latest_accepted_by_file_key(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Collapse append-only entries to the latest entry per ``fileKey``.

    Because the ledger is append-ordered, iterating front-to-back and letting
    later entries overwrite earlier ones yields "latest accepted attempt wins".
    Entries without a non-empty string ``fileKey`` are ignored.

    Args:
        entries: Ledger entries in append order.

    Returns:
        A mapping of ``fileKey`` to its most recent ledger entry.
    """
    latest: dict[str, dict[str, Any]] = {}
    for entry in entries:
        key = entry.get("fileKey")
        if isinstance(key, str) and key:
            latest[key] = entry
    return latest


def summarize_accepted(latest_by_key: dict[str, dict[str, Any]]) -> dict[str, int]:
    """Summarize accepted outcomes for the live progress line.

    Only ``complete`` answers are counted. ``approve`` outcomes count as
    approved; ``request-changes`` / ``request-changes-with-suggestion`` count as
    needing work; any other (or missing) outcome on a complete answer is ignored.

    Args:
        latest_by_key: The latest accepted entry per ``fileKey``.

    Returns:
        ``{"approved": int, "needsWork": int, "reviewed": int}`` where
        ``reviewed == approved + needsWork``.
    """
    approved = 0
    needs_work = 0
    for entry in latest_by_key.values():
        if entry.get("status") != _COMPLETE_STATUS:
            continue
        outcome = entry.get("outcome")
        if outcome == _APPROVE_OUTCOME:
            approved += 1
        elif outcome in _NEEDS_WORK_OUTCOMES:
            needs_work += 1
    return {"approved": approved, "needsWork": needs_work, "reviewed": approved + needs_work}
