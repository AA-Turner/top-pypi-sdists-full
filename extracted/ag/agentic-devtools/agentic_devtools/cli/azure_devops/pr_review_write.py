"""Atomic, scope-checked per-file answer writes (v2 PR review).

This module provides the single command a ``file-reviewer`` subagent may run:
``agdt-file-review-write --file-key K --answer-file <path>``. It validates a
COMPLETE answer JSON against the plan §9 schema, enforces ``fileKey`` scope and
freshness (``promptHash`` / ``commitHash`` / ``attemptId`` must echo the
scaffolded baseline), validates line-anchoring (§15.6), and writes the answer
atomically via :func:`os.replace` into ``answers/<fileKey>.answer.json``.

The command touches **no** shared workflow state and never PATCHes the PR
comment; it is the *only* ``agdt-*`` surface a subagent is permitted to use
(§5.2 collapsed to one atomic write per §15.2). ``needs-info`` is a *status
inside the answer JSON* (carrying ``partialSummary`` / ``partialFindings`` /
``blockedOn`` / ``attemptId``) so a re-spawned reviewer can continue from a
preserved draft.

Exit codes:
    0  answer validated and written (or dry-run validated)
    1  answer rejected — out-of-scope, stale, or malformed input
    2  IO / argument / artifact-resolution error
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any

from ...state import get_state_dir, get_value, is_safe_dir_segment
from .helpers import resolve_review_artifact_dir_name
from .pr_review_answers import ANSWER_SCHEMA_VERSION

ANSWER_FILENAME_SUFFIX = ".answer.json"

VALID_STATUSES = frozenset({"pending", "needs-info", "complete", "failed"})
VALID_OUTCOMES = frozenset({"approve", "request-changes", "request-changes-with-suggestion"})
VALID_REVIEW_MODES = frozenset({"diff", "metadata-only", "deleted", "renamed", "binary", "skipped"})
VALID_REVIEW_DEPTHS = frozenset({"deep", "light"})
VALID_CONFIDENCE_LEVELS = frozenset({"high", "medium", "low"})
VALID_SEVERITIES = frozenset({"high", "medium", "low"})
VALID_LINE_SIDES = frozenset({"left", "right"})
VALID_DUCK_VERDICTS = frozenset({"accept", "reject", "partial"})

# reviewModes for which a line-anchored suggestion is not meaningful (§15.6).
LINE_ANCHOR_FORBIDDEN_MODES = frozenset({"binary", "deleted", "metadata-only"})

# Immutable carried fields a fresh answer must echo from the scaffold baseline.
FRESHNESS_FIELDS = ("promptHash", "commitHash", "attemptId")

# Scaffold-carried context fields the answer must not spoof.
# ``reviewMode`` is the most critical because ``validate_line_anchoring``
# trusts the answer's own ``reviewMode`` — a subagent that changes it could
# bypass line-anchor enforcement (e.g. claim "diff" on a binary file).
SCAFFOLD_LOCKED_FIELDS = ("reviewMode", "filePath", "prId", "reviewDepth")

# Outcome requiring at least one suggestion to be present.
_OUTCOME_REQUIRING_SUGGESTION = "request-changes-with-suggestion"

# Common string fields required on every answer regardless of status.
_REQUIRED_STRING_FIELDS = ("commitHash", "fileKey", "filePath", "promptHash", "attemptId")


def _is_nonempty_str(value: Any) -> bool:
    """Return True when *value* is a non-blank string."""
    return isinstance(value, str) and bool(value.strip())


def _is_int(value: Any) -> bool:
    """Return True when *value* is an int and not a bool."""
    return isinstance(value, int) and not isinstance(value, bool)


def _validate_optional_enum(answer: dict[str, Any], field_name: str, allowed_values: frozenset[str]) -> str | None:
    """Validate an optional enum-like string field."""
    value = answer.get(field_name)
    if value is None:
        return None
    if not isinstance(value, str) or value not in allowed_values:
        return f"{field_name} must be one of {sorted(allowed_values)} when provided"
    return None


def validate_suggestion(suggestion: Any, index: int) -> list[str]:
    """Validate one suggestion's structural shape (mode-independent).

    Args:
        suggestion: The candidate suggestion (expected to be a dict).
        index: Position in the suggestions list (for error messages).

    Returns:
        A list of error strings; empty when the suggestion is well-formed.
    """
    prefix = f"suggestions[{index}]"
    if not isinstance(suggestion, dict):
        return [f"{prefix}: must be an object"]

    errors: list[str] = []
    if suggestion.get("severity") not in VALID_SEVERITIES:
        errors.append(f"{prefix}: severity must be one of {sorted(VALID_SEVERITIES)}")
    if not _is_nonempty_str(suggestion.get("content")):
        errors.append(f"{prefix}: content must be a non-empty string")

    out_of_scope = suggestion.get("out_of_scope")
    if out_of_scope is not None and not isinstance(out_of_scope, bool):
        errors.append(f"{prefix}: out_of_scope must be a boolean")
    is_out_of_scope = out_of_scope is True

    line = suggestion.get("line")
    if line is None:
        if not is_out_of_scope:
            errors.append(f"{prefix}: line is required unless out_of_scope is true")
    elif not _is_int(line):
        errors.append(f"{prefix}: line must be an integer")
    elif line < 1:
        errors.append(f"{prefix}: line must be >= 1 (diff line anchors are 1-based)")

    end_line = suggestion.get("endLine")
    if end_line is not None and line is None:
        errors.append(f"{prefix}: endLine is only valid when line is provided")
    elif end_line is not None:
        if not _is_int(end_line):
            errors.append(f"{prefix}: endLine must be an integer")
        elif end_line < 1:
            errors.append(f"{prefix}: endLine must be >= 1 (diff line anchors are 1-based)")
        elif _is_int(line) and end_line < line:
            errors.append(f"{prefix}: endLine must be >= line")

    line_side = suggestion.get("lineSide")
    if line_side is not None and line is None:
        errors.append(f"{prefix}: lineSide is only valid when line is provided")
    elif line_side is not None and line_side not in VALID_LINE_SIDES:
        errors.append(f"{prefix}: lineSide must be one of {sorted(VALID_LINE_SIDES)}")

    replacement = suggestion.get("replacement_code")
    if replacement is not None and not isinstance(replacement, str):
        errors.append(f"{prefix}: replacement_code must be a string")

    return errors


def validate_reviewer(reviewer: Any) -> list[str]:
    """Validate the ``reviewer`` block (model + optional rubberDucks).

    The subagent supplies ``reviewer.model``; ``rubberDucks`` are recorded by the
    orchestrator (§15.1), so they are optional here but validated when present.
    """
    if not isinstance(reviewer, dict):
        return ["reviewer: must be an object"]

    errors: list[str] = []
    if not _is_nonempty_str(reviewer.get("model")):
        errors.append("reviewer.model: must be a non-empty string")

    ducks = reviewer.get("rubberDucks")
    if ducks is None:
        return errors
    if not isinstance(ducks, list):
        errors.append("reviewer.rubberDucks: must be a list")
        return errors

    for index, duck in enumerate(ducks):
        prefix = f"reviewer.rubberDucks[{index}]"
        if not isinstance(duck, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        if not _is_nonempty_str(duck.get("model")):
            errors.append(f"{prefix}.model: must be a non-empty string")
        if duck.get("verdict") not in VALID_DUCK_VERDICTS:
            errors.append(f"{prefix}.verdict: must be one of {sorted(VALID_DUCK_VERDICTS)}")
        notes = duck.get("notes")
        if notes is not None and not isinstance(notes, str):
            errors.append(f"{prefix}.notes: must be a string")
    return errors


def _validate_complete_fields(answer: dict[str, Any], suggestions: list[Any]) -> list[str]:
    """Validate fields required only when ``status == "complete"``."""
    errors: list[str] = []
    outcome = answer.get("outcome")
    if outcome not in VALID_OUTCOMES:
        errors.append(f"complete answers require outcome in {sorted(VALID_OUTCOMES)}")
    if not _is_nonempty_str(answer.get("summary")):
        errors.append("complete answers require a non-empty summary")
    errors.extend(validate_reviewer(answer.get("reviewer")))
    if outcome == _OUTCOME_REQUIRING_SUGGESTION:
        if not suggestions:
            errors.append("request-changes-with-suggestion requires at least one suggestion")
        for index, suggestion in enumerate(suggestions):
            if isinstance(suggestion, dict) and not _is_nonempty_str(suggestion.get("replacement_code")):
                errors.append(
                    f"suggestions[{index}]: replacement_code is required (non-empty) "
                    "for outcome 'request-changes-with-suggestion'"
                )
    return errors


def validate_answer_schema(answer: Any) -> list[str]:
    """Validate an answer dict's structural shape against the §9 schema.

    Returns a list of human-readable errors; empty means structurally valid.
    Status-specific rules:
      * ``complete`` requires a valid ``outcome``, non-empty ``summary``, a valid
        ``reviewer``, and (for ``request-changes-with-suggestion``) at least one
        suggestion.
      * ``needs-info`` requires a non-empty ``blockedOn``.
    """
    if not isinstance(answer, dict):
        return ["answer must be a JSON object"]

    errors: list[str] = []
    if answer.get("schemaVersion") != ANSWER_SCHEMA_VERSION:
        errors.append(f"schemaVersion must equal {ANSWER_SCHEMA_VERSION}")
    if not _is_int(answer.get("prId")):
        errors.append("prId must be an integer")
    for field_name in _REQUIRED_STRING_FIELDS:
        if not _is_nonempty_str(answer.get(field_name)):
            errors.append(f"{field_name} must be a non-empty string")
    if answer.get("reviewMode") not in VALID_REVIEW_MODES:
        errors.append(f"reviewMode must be one of {sorted(VALID_REVIEW_MODES)}")
    review_depth_error = _validate_optional_enum(answer, "reviewDepth", VALID_REVIEW_DEPTHS)
    if review_depth_error:
        errors.append(review_depth_error)
    confidence_error = _validate_optional_enum(answer, "confidence", VALID_CONFIDENCE_LEVELS)
    if confidence_error:
        errors.append(confidence_error)

    status = answer.get("status")
    if status not in VALID_STATUSES:
        errors.append(f"status must be one of {sorted(VALID_STATUSES)}")

    suggestions = answer.get("suggestions", [])
    if not isinstance(suggestions, list):
        errors.append("suggestions must be a list")
        suggestions = []
    else:
        for index, suggestion in enumerate(suggestions):
            errors.extend(validate_suggestion(suggestion, index))

    if status == "complete":
        errors.extend(_validate_complete_fields(answer, suggestions))
    elif status == "needs-info":
        if not _is_nonempty_str(answer.get("blockedOn")):
            errors.append("needs-info answers require a non-empty blockedOn")
        partial_summary = answer.get("partialSummary")
        if partial_summary is not None and not _is_nonempty_str(partial_summary):
            errors.append("needs-info partialSummary must be a non-empty string when provided")
        partial_findings = answer.get("partialFindings")
        if partial_findings is not None and not isinstance(partial_findings, list):
            errors.append("needs-info partialFindings must be a list when provided")

    return errors


def validate_line_anchoring(answer: Any) -> list[str]:
    """Reject line-anchored suggestions for non-anchorable review modes (§15.6).

    Binary, deleted, and metadata-only files have no meaningful diff line to
    anchor a suggestion to. Out-of-scope suggestions are exempt.
    """
    if not isinstance(answer, dict):
        return []
    mode = answer.get("reviewMode")
    if mode not in LINE_ANCHOR_FORBIDDEN_MODES:
        return []
    suggestions = answer.get("suggestions")
    if not isinstance(suggestions, list):
        return []

    errors: list[str] = []
    for index, suggestion in enumerate(suggestions):
        if not isinstance(suggestion, dict):
            continue
        if suggestion.get("out_of_scope") is True:
            continue
        if suggestion.get("line") is not None:
            errors.append(f"suggestions[{index}]: line-anchored suggestion is not allowed for reviewMode '{mode}'")
    return errors


def check_answer_scope(answer: Any, file_key: str, scaffold: dict[str, Any]) -> list[str]:
    """Ensure the answer is scoped strictly to *file_key* (refuse out-of-scope).

    Both the submitted answer's ``fileKey`` and the scaffold baseline's
    ``fileKey`` must equal *file_key*. The write target is derived from
    *file_key* alone, so a subagent can never write outside its own file.
    """
    errors: list[str] = []
    answer_key = answer.get("fileKey") if isinstance(answer, dict) else None
    if answer_key != file_key:
        errors.append(f"answer fileKey {answer_key!r} does not match --file-key {file_key!r}")
    scaffold_key = scaffold.get("fileKey")
    if scaffold_key != file_key:
        errors.append(f"scaffold fileKey {scaffold_key!r} does not match --file-key {file_key!r}")
    return errors


def check_answer_freshness(answer: Any, scaffold: dict[str, Any]) -> list[str]:
    """Reject stale answers whose carried hashes diverge from the scaffold.

    Checks two groups against the scaffold baseline:

    * **Freshness fields** (``promptHash`` / ``commitHash`` / ``attemptId``):
      any mismatch means the answer was produced against a different prompt /
      commit / attempt and must be regenerated.
    * **Scaffold-locked context fields** (``reviewMode`` / ``filePath`` /
      ``prId`` / ``reviewDepth``): these must be echoed verbatim from the
      scaffold so that a subagent cannot spoof them to bypass validation
      (e.g. changing ``reviewMode`` from ``binary`` to ``diff`` to sneak
      line-anchored suggestions past :func:`validate_line_anchoring`).
    """
    answer_dict = answer if isinstance(answer, dict) else {}
    errors: list[str] = []
    for field_name in FRESHNESS_FIELDS:
        submitted = answer_dict.get(field_name)
        expected = scaffold.get(field_name)
        if submitted != expected:
            errors.append(f"stale answer: {field_name} {submitted!r} does not match scaffold {expected!r}")
    for field_name in SCAFFOLD_LOCKED_FIELDS:
        expected = scaffold.get(field_name)
        submitted = answer_dict.get(field_name)
        if submitted != expected:
            errors.append(f"scaffold mismatch: {field_name} {submitted!r} does not match scaffold {expected!r}")
    return errors


def validate_answer_write(answer: Any, file_key: str, scaffold: dict[str, Any]) -> list[str]:
    """Aggregate schema, scope, freshness, and line-anchoring validation.

    Returns the combined list of errors; empty means the answer is safe to write.
    """
    errors = validate_answer_schema(answer)
    errors.extend(check_answer_scope(answer, file_key, scaffold))
    errors.extend(check_answer_freshness(answer, scaffold))
    errors.extend(validate_line_anchoring(answer))
    return errors


def write_answer_atomic(target: Path, answer: dict[str, Any]) -> None:
    """Write *answer* to *target* atomically via a unique temp file + :func:`os.replace`.

    The staging file name carries the pid and a uuid so concurrent writers (for
    example a re-spawned reviewer for the same fileKey) never collide on it.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = target.parent / f"{target.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
    try:
        tmp_path.write_text(json.dumps(answer, indent=2), encoding="utf-8")
        os.replace(tmp_path, target)
    except OSError:
        with contextlib.suppress(OSError):
            tmp_path.unlink()
        raise


def _resolve_answers_dir(backfill: bool = True) -> Path | None:
    """Resolve the canonical ``answers/`` directory from the active PR state.

    The directory is always rooted at ``get_state_dir()/pull-request-review/``;
    there is deliberately no caller-supplied path override, so an (untrusted)
    subagent cannot redirect the write outside the review artifact tree.

    When the ``review.commit_hash_short`` state key is absent (e.g. it was
    written to a different scope after a bootstrap re-scope), resolution
    falls back via :func:`resolve_review_artifact_dir_name` so discovery and
    self-healing stay centralized (#1182).

    Args:
        backfill: When ``True`` (default), persists a discovered
            ``commit_hash_short`` back to state.  Pass ``False`` from
            dry-run callers to allow discovery without mutating state.

    Returns ``None`` (after printing an error) when the directory cannot be
    resolved because no usable PR id is available.
    """
    pr_value = get_value("pull_request_id")
    if pr_value is None:
        print("Error: PR ID required (pull_request_id state).", file=sys.stderr)
        return None
    if isinstance(pr_value, bool):
        print("Error: pull_request_id must be an integer, not a boolean.", file=sys.stderr)
        return None
    try:
        pull_request_id = int(pr_value)
    except (TypeError, ValueError):
        print("Error: pull_request_id must be an integer.", file=sys.stderr)
        return None

    state_dir = get_state_dir()
    commit_hash_short = get_value("review.commit_hash_short")
    dir_name = resolve_review_artifact_dir_name(pull_request_id, commit_hash_short, backfill=backfill)
    return state_dir / "pull-request-review" / dir_name / "answers"


def file_review_write_command() -> None:
    """CLI entry point for ``agdt-file-review-write``."""
    parser = argparse.ArgumentParser(
        description="Atomically validate and write a per-file review answer (v2 subagent surface).",
    )
    parser.add_argument("--file-key", required=True, help="The fileKey this answer is scoped to.")
    parser.add_argument("--answer-file", required=True, help="Path to the draft answer JSON to validate and write.")
    parser.add_argument("--dry-run", action="store_true", help="Validate only; do not write.")
    args = parser.parse_args()

    file_key = args.file_key
    if not is_safe_dir_segment(file_key):
        print(f"Error: invalid --file-key {file_key!r} (unsafe path segment).", file=sys.stderr)
        sys.exit(2)

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

    answers_dir = _resolve_answers_dir(backfill=not args.dry_run)
    if answers_dir is None:
        sys.exit(2)
    target = answers_dir / f"{file_key}{ANSWER_FILENAME_SUFFIX}"
    if not target.exists():
        print(
            f"Error: no scaffolded answer for fileKey {file_key!r} at {target}.",
            file=sys.stderr,
        )
        sys.exit(2)
    try:
        scaffold = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error: could not read scaffold answer {target}: {exc}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(scaffold, dict):
        print(f"Error: scaffold answer {target} is not a JSON object.", file=sys.stderr)
        sys.exit(2)

    scaffold_errors = validate_answer_schema(scaffold)
    if scaffold_errors:
        print(
            "Error: scaffold answer is invalid (re-run v2 review artifact generation):",
            file=sys.stderr,
        )
        for err in scaffold_errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(2)

    errors = validate_answer_write(answer, file_key, scaffold)
    if errors:
        print("Error: answer validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(f"[dry-run] answer for {file_key} is valid; not written.")
        return

    try:
        write_answer_atomic(target, answer)
    except OSError as exc:
        print(f"Error: could not write answer {target}: {exc}", file=sys.stderr)
        sys.exit(2)
    print(f"Answer written for {file_key} (status={answer.get('status')}): {target}")
