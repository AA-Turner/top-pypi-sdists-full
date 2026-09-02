import argparse
import json
import os
import re
import stat
import tempfile
from collections.abc import Mapping, Sequence
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast

from ..file_locking import locked_file
from .errors import ProviderError

ProbeClassification = Literal["ACCEPTED", "REJECTED", "AUTH_ERROR", "RETRYABLE_ERROR", "INVALID_INPUT"]
ModelAvailabilityStatus = Literal["available", "rejected", "excluded"]
ValidationSurface = Literal["model", "custom_agent", "base_ref"]

_VALIDATION_ORDER: tuple[ValidationSurface, ...] = ("model", "custom_agent", "base_ref")
_CANONICAL_BODY_PREFIX = "<!-- agdt:ref:sub-api-availability-matrix -->"
_TASK_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
_DEFAULT_MATRIX: dict[str, ModelAvailabilityStatus] = {
    "claude-opus-5": "available",
    "claude-sonnet-5": "available",
    "mai-code-1.1-flash": "available",
    "gpt-5.6-luna": "available",
    "gemini-3.1-pro-preview": "rejected",
    "claude-opus-4.8": "rejected",
    "claude-opus-4.6": "rejected",
    "claude-sonnet-4.6": "excluded",
    "gemini-3.6-flash": "excluded",
    "gpt-5.4-mini": "excluded",
}
_DEFAULT_EVIDENCE_PATH = Path("tests/fixtures/ai_providers/availability/evidence.json")
_DEFAULT_ADR_PATH = Path("docs/architecture-decisions/agent-tasks-model-availability.md")
_PUBLICATION_LOCK_FILENAME = ".availability-publication.lock"
_SUCCESS_INDICATOR_PATTERN = re.compile(r"(?<![\w/-])(?:succeeded|passed)(?![\w/-])")
_BASE_REF_VALUE_PATTERN = re.compile(
    r"""(?:'(?:[^'\\\n]|\\.)*'|"(?:[^"\\\n]|\\.)*"|`(?:[^`\\\n]|\\.)*`|refs/[^\s,;:!?]+)"""
)


def build_default_matrix() -> dict[str, ModelAvailabilityStatus]:
    """Return the currently observed Agent Tasks inventory for model availability."""
    return dict(_DEFAULT_MATRIX)


# Keep the canonical default inventory and the higher-level availability alias independent.
DEFAULT_MODEL_MATRIX = build_default_matrix()
DEFAULT_AVAILABILITY_MATRIX = build_default_matrix()


def canonicalize_matrix(matrix: Mapping[str, str] | None) -> dict[str, ModelAvailabilityStatus]:
    """Validate and normalize a model matrix to canonical lowercase status strings."""
    raw = build_default_matrix() if matrix is None else dict(matrix)
    validated: dict[str, ModelAvailabilityStatus] = {}
    original_model_names: dict[str, str] = {}
    for model_name, status in raw.items():
        if not isinstance(model_name, str) or not model_name.strip():
            raise ProviderError("Model names must be non-empty strings.", category="validation_error")
        canonical_model_name = model_name.strip()
        if not isinstance(status, str):
            raise ProviderError(
                f"Availability status for '{model_name}' must be a string, got {type(status).__name__!r}",
                category="validation_error",
            )
        canonical_status = status.strip().lower()
        if canonical_status not in {"available", "rejected", "excluded"}:
            raise ProviderError(
                f"Unsupported availability status for '{model_name}': {status!r}",
                category="validation_error",
            )
        if canonical_model_name in validated:
            original_model_name = original_model_names[canonical_model_name]
            raise ProviderError(
                f"Model name collision after normalization: {model_name!r} conflicts with existing entry "
                f"{original_model_name!r} (canonical key {canonical_model_name!r}).",
                category="validation_error",
            )
        validated[canonical_model_name] = canonical_status  # type: ignore[assignment]
        original_model_names[canonical_model_name] = model_name
    return dict(sorted(validated.items()))


def _coerce_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        return value
    return str(value)


def _contains_any(text: str, needles: Sequence[str]) -> bool:
    lower = text.lower()
    return any(needle.lower() in lower for needle in needles)


def _contains_phrase_at_identifier_boundary(lower_text: str, phrases: Sequence[str]) -> bool:
    """Return True if any phrase appears in the pre-lowercased *lower_text* as a complete
    identifier-bounded token sequence.

    This prevents partial-token false positives such as ``database_ref is invalid``
    or ``base_ref is invalidated`` matching the self-contained phrase
    ``base_ref is invalid`` via plain substring search.
    Both *lower_text* and all entries in *phrases* must already be lowercased.
    """
    return any(
        bool(re.search(r"(?<![A-Za-z0-9_])" + re.escape(phrase) + r"(?![A-Za-z0-9_])", lower_text))
        for phrase in phrases
    )


def _find_earliest_phrase_at_identifier_boundary(lower_text: str, phrases: Sequence[str]) -> int | None:
    """Return the earliest start offset where any phrase appears as an identifier-bounded token sequence.

    Both *lower_text* and all entries in *phrases* must already be lowercased.
    """
    earliest: int | None = None
    for phrase in phrases:
        phrase_end = _find_marker_at_boundary(lower_text, phrase)
        if phrase_end is None:
            continue
        phrase_start = phrase_end - len(phrase)
        if earliest is None or phrase_start < earliest:
            earliest = phrase_start
    return earliest


def _find_marker_at_boundary(seg: str, marker: str) -> int | None:
    """Return the index just after the first occurrence of *marker* in *seg* that is not
    preceded or followed by an identifier character (``[A-Za-z0-9_]``), or ``None`` if no
    such occurrence exists.

    This prevents ``database_ref``/``base_refx`` from matching when ``base_ref`` is searched.
    """
    m = re.search(r"(?<![A-Za-z0-9_])" + re.escape(marker) + r"(?![A-Za-z0-9_])", seg)
    return (m.start() + len(marker)) if m is not None else None


def _iter_marker_ends_at_boundary(seg: str, marker: str) -> list[int]:
    """Return the index just after every identifier-bounded occurrence of *marker* in *seg*.

    Unlike :func:`_find_marker_at_boundary`, this considers *all* occurrences rather than
    only the first, so a later, directly-bound occurrence of *marker* is not shadowed by an
    earlier occurrence that never resolves into a failure.
    """
    pattern = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(marker) + r"(?![A-Za-z0-9_])")
    return [m.end() for m in pattern.finditer(seg)]


def _split_error_clauses(text: str) -> list[str]:
    """Split error text into clauses while preserving punctuation inside quoted spans."""
    segments: list[str] = []
    start = 0
    in_quote = False
    quote_char = ""
    length = len(text)

    idx = 0
    while idx < length:
        char = text[idx]
        prev_char = text[idx - 1] if idx > 0 else ""
        next_char = text[idx + 1] if idx + 1 < length else ""
        if char in {"'", '"', "`"} and prev_char != "\\":
            is_apostrophe = char == "'" and prev_char.isalnum() and next_char.isalnum()
            if not is_apostrophe:
                if not in_quote:
                    in_quote = True
                    quote_char = char
                elif char == quote_char:
                    in_quote = False
                    quote_char = ""

        should_split = False
        if not in_quote:
            if char in {";", "\n"}:
                should_split = True
            elif char in {".", "!", "?"}:
                should_split = idx + 1 < length and text[idx + 1].isspace()
            elif char == ",":
                tail = text[idx + 1 :].lstrip()
                for word in ("but", "however", "though", "yet"):
                    if not tail.startswith(word):
                        continue
                    next_idx = len(word)
                    should_split = next_idx == len(tail) or (not tail[next_idx].isalnum() and tail[next_idx] != "_")
                    if should_split:
                        break

        if should_split:
            segments.append(text[start:idx])
            start = idx + 1
        idx += 1

    segments.append(text[start:])
    return segments


def _looks_like_invalid_model_response(response_text: str) -> bool:
    lower = response_text.lower()
    rejection_phrases = (
        "invalid model",
        "unsupported model",
        "unknown model",
        "model not found",
        "model is not available",
        "not a valid model",
        "model unavailable",
        "unrecognized model",
    )
    model_failure_phrases = (
        "model is invalid",
        "model was invalid",
        "model is unsupported",
        "model was unsupported",
        "model is unknown",
        "model was unknown",
        "model is not found",
        "model was not found",
        "model is unavailable",
        "model was unavailable",
        "model not supported",
    )
    return _contains_phrase_at_identifier_boundary(lower, rejection_phrases) or _contains_phrase_at_identifier_boundary(
        lower, model_failure_phrases
    )


def _looks_like_base_ref_response(response_text: str) -> bool:
    lower = response_text.lower()
    base_ref_markers = (
        "base_ref",
        "base ref",
        "base-ref",
        "base reference",
    )
    # Self-contained phrases that already name base_ref as the failing field — these
    # require no further co-occurrence check because the field name and the verdict are
    # expressed together in a single phrase.
    self_contained_phrases = (
        "base_ref is invalid",
        "base_ref is missing",
        "base ref is invalid",
        "base ref is missing",
        "base-ref is invalid",
        "base-ref is missing",
        "base reference is invalid",
        "base reference is missing",
    )
    # Ref-scoped co-occurrence signals: these already name "ref" or "reference" as the
    # failing resource, so a same-segment check with a base_ref marker suffices.
    ref_scoped_signals = (
        "ref not found",
        "reference not found",
        "no such ref",
        "unknown ref",
        "must provide a valid ref",
    )
    # Generic failure signals: these alone cannot confirm a base_ref failure because they
    # also appear in error messages for unrelated fields (e.g. "repository not found").
    # They require tight binding — the failure phrase must follow a base_ref marker in the
    # same segment with no standalone success indicator (e.g. "succeeded", "passed")
    # between them.
    # This prevents "base_ref validation succeeded and repository not found" from being
    # classified as a base_ref failure.
    generic_failure_signals = (
        "not found",
        "does not exist",
        "nonexistent",
        "is invalid",
        "was invalid",
        "is missing",
        "was missing",
    )
    if _contains_phrase_at_identifier_boundary(lower, self_contained_phrases):
        return True
    # Split on clause separators: semicolons, newlines, contrast-clause commas
    # (`, but`, `, however`, `, though`, `, yet`), and sentence-terminating punctuation
    # (`.`, `!`, `?`) followed by whitespace. The lookahead/keyword checks ensure only
    # genuine clause boundaries trigger a split — punctuation embedded in git ref names
    # such as "refs/heads/release/1.2" is never followed by whitespace and is therefore
    # preserved, and ordinary commas inside non-contrast text are left intact. This
    # prevents mixed-surface bodies such as "base_ref validation succeeded, but
    # custom_agent is not found" from being classified as a base_ref failure because the
    # co-occurrence signals appear in a different clause.
    segments = _split_error_clauses(lower)
    # For ref-scoped signals, require the failure phrase to follow a base_ref marker in the
    # same segment with no success indicator between them. This prevents
    # "base_ref validation succeeded and repository ref not found" from being classified as a
    # base_ref failure (e.g. "ref not found" is a substring of "repository ref not found").
    #
    # For generic signals, require an even tighter predicate: the phrase between marker and
    # failure must be limited to an optional echoed ref value (as the first non-whitespace
    # token after the marker) and optional copula/punctuation.
    # This rejects unrelated resource failures such as
    # "base_ref validation pending and repository not found".
    allowed_generic_bridge_tokens = {"", ":", "-", "is", "was", "were", "be", "to be"}

    def _has_scoped_bridge(between: str) -> bool:
        if _SUCCESS_INDICATOR_PATTERN.search(between):
            return False
        stripped_between = between.lstrip()
        if stripped_between.startswith(":"):
            stripped_between = stripped_between[1:].lstrip()
        consumed = 0
        value_match = _BASE_REF_VALUE_PATTERN.match(stripped_between)
        if value_match is not None:
            consumed = value_match.end()
        remainder = stripped_between[consumed:].strip()
        return remainder in allowed_generic_bridge_tokens

    for seg in segments:
        for marker in base_ref_markers:
            for marker_end in _iter_marker_ends_at_boundary(seg, marker):
                tail = seg[marker_end:]
                for signal in ref_scoped_signals:
                    for signal_end in _iter_marker_ends_at_boundary(tail, signal):
                        signal_offset = signal_end - len(signal)
                        between = tail[:signal_offset]
                        if _has_scoped_bridge(between):
                            return True
                for signal in generic_failure_signals:
                    for signal_end in _iter_marker_ends_at_boundary(tail, signal):
                        signal_offset = signal_end - len(signal)
                        between = tail[:signal_offset]
                        if _has_scoped_bridge(between):
                            return True
    return False


def _resolve_validation_order(validation_order: Sequence[str] | None) -> tuple[ValidationSurface, ...]:
    if validation_order is None:
        return _VALIDATION_ORDER
    if tuple(validation_order) != _VALIDATION_ORDER:
        raise ProviderError(
            "validation_order must be exactly ('model', 'custom_agent', 'base_ref').",
            category="validation_error",
        )
    return _VALIDATION_ORDER


def infer_validation_surface(
    response_body: object,
    validation_order: Sequence[str] | None = None,
) -> ValidationSurface:
    """Infer the surface that likely triggered the failure from the response text."""
    order = _resolve_validation_order(validation_order)
    text = _coerce_text(response_body).lower()
    if not text:
        return order[0]

    # Tight failure-field phrases: the surface name is the direct subject of the error.
    # Checked first so that incidental mentions of another field (e.g. "… for model X")
    # do not override the surface that is actually being rejected.
    surface_failure_wording: dict[str, tuple[str, ...]] = {
        "model": (
            "invalid model",
            "unsupported model",
            "unknown model",
            "model not found",
            "model is invalid",
            "model is unsupported",
            "model is unknown",
            "model is not found",
            "model is unavailable",
            "model was invalid",
            "model was unsupported",
            "model was unknown",
            "model was not found",
            "model was unavailable",
            "model not supported",
            "unrecognized model",
            "not a valid model",
            "model unavailable",
        ),
        "custom_agent": (
            "invalid custom_agent",
            "custom_agent is invalid",
            "custom_agent is not valid",
            "custom_agent is not found",
            "custom_agent not found",
            "custom_agent does not exist",
            "custom_agent ref not found",
            "custom_agent reference not found",
            "invalid custom agent",
            "custom agent is invalid",
            "custom agent is not valid",
            "custom agent is not found",
            "custom agent not found",
            "custom agent does not exist",
            "custom agent ref not found",
            "custom agent reference not found",
        ),
        "base_ref": (
            "ref not found",
            "reference not found",
            "no such ref",
            "unknown ref",
            "base_ref not found",
            "base_ref does not exist",
            "base_ref is invalid",
            "base_ref is missing",
            "base ref not found",
            "base ref does not exist",
            "base ref is invalid",
            "base ref is missing",
            "base reference not found",
            "base reference does not exist",
            "base reference is invalid",
            "base reference is missing",
        ),
    }

    # Bare field-name keywords used only as a fallback.
    surface_bare_keywords: dict[str, tuple[str, ...]] = {
        "model": ("model", "model_id", "model id"),
        "custom_agent": ("custom_agent", "custom agent"),
        "base_ref": ("base_ref", "base ref", "base-ref"),
    }

    # First pass: among surfaces that have an unambiguous failure-phrase match, return
    # the one whose matching phrase appears earliest in the text.  Using textual position
    # rather than validation-order position means that when multiple failure phrases are
    # present (e.g. "invalid model … ref not found"), the field most prominently named
    # in the error body wins, consistent with the second-pass tiebreaker below.
    failure_matches = [
        s for s in order if _contains_phrase_at_identifier_boundary(text, surface_failure_wording.get(s, ()))
    ]
    if failure_matches:
        if len(failure_matches) == 1:
            return failure_matches[0]
        # Multiple surfaces have failure phrases — pick the one whose phrase appears earliest.
        earliest_fp: int | None = None
        best: ValidationSurface = failure_matches[0]
        for surface in failure_matches:
            phrases = surface_failure_wording.get(surface, ())
            phrase_start = _find_earliest_phrase_at_identifier_boundary(text, phrases)
            if phrase_start is not None and (earliest_fp is None or phrase_start < earliest_fp):
                earliest_fp = phrase_start
                best = surface
        return best

    # Bridge pass: if the text satisfies the base_ref failure predicate and explicitly
    # names a base_ref surface, prefer base_ref before falling back to earliest bare
    # keyword. This avoids classifying model/context preambles as the failure surface.
    base_ref_surface_markers = ("base_ref", "base ref", "base-ref", "base reference")
    if _looks_like_base_ref_response(text) and _contains_any(text, base_ref_surface_markers):
        return "base_ref"

    # Second pass: when no tight failure phrase matched, fall back to the surface
    # whose bare keyword appears earliest in the text.  This correctly handles
    # bodies like "custom_agent 'x' is invalid for model y" where the failing
    # field name precedes a context-only mention of another field.
    earliest_pos: int | None = None
    earliest_surface: ValidationSurface = order[0]
    for surface in order:
        keywords = surface_bare_keywords.get(surface, ())
        keyword_start = _find_earliest_phrase_at_identifier_boundary(text, keywords)
        if keyword_start is not None and (earliest_pos is None or keyword_start < earliest_pos):
            earliest_pos = keyword_start
            earliest_surface = surface

    return earliest_surface


def classify_probe_response(
    status_code: int,
    response_body: object = None,
    *,
    validation_order: Sequence[str] | None = None,
) -> ProbeClassification:
    """Classify a single Agent Tasks probe response according to the validation order contract."""
    if isinstance(status_code, bool) or not isinstance(status_code, int):
        raise ProviderError("status_code must be an integer.", category="validation_error")
    _resolve_validation_order(validation_order)

    if status_code in {401, 403}:
        return "AUTH_ERROR"
    if status_code == 429 or 500 <= status_code <= 599:
        return "RETRYABLE_ERROR"

    response_text = _coerce_text(response_body)
    if status_code == 400:
        if _looks_like_invalid_model_response(response_text):
            return "REJECTED"
        return "INVALID_INPUT"
    if status_code == 412:
        if (
            _looks_like_base_ref_response(response_text)
            and infer_validation_surface(response_text, validation_order) == "base_ref"
        ):
            return "ACCEPTED"
        return "INVALID_INPUT"
    return "INVALID_INPUT"


# Backward-compatible aliases retained for existing callers and compatibility shims.
classify_response = classify_probe_response
classify_probe_result = classify_probe_response


@dataclass(frozen=True)
class ProbeObservation:
    model: str
    surface: str
    status_code: int
    classification: ProbeClassification
    body_excerpt: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.model, str) or not self.model.strip():
            raise ProviderError("model must be a non-empty string.", category="validation_error")
        if not isinstance(self.surface, str) or self.surface not in {"model", "custom_agent", "base_ref"}:
            raise ProviderError("surface must be one of: model, custom_agent, base_ref.", category="validation_error")
        if isinstance(self.status_code, bool) or not isinstance(self.status_code, int):
            raise ProviderError("status_code must be an integer.", category="validation_error")
        if not isinstance(self.classification, str) or self.classification not in {
            "ACCEPTED",
            "REJECTED",
            "AUTH_ERROR",
            "RETRYABLE_ERROR",
            "INVALID_INPUT",
        }:
            raise ProviderError(
                "classification must be a valid ProbeClassification value.",
                category="validation_error",
            )
        if not isinstance(self.body_excerpt, str):
            raise ProviderError("body_excerpt must be a string.", category="validation_error")


# Keep the dataclass names usable as semantic aliases for the same observation record.
ProbeOutcome = ProbeObservation
ProbeResult = ProbeObservation


def _validate_task_id(task_id: str, context: str) -> None:
    if not _TASK_ID_PATTERN.fullmatch(task_id):
        raise ProviderError(
            f"Snapshot {context} {task_id!r} does not match ^[A-Za-z0-9_-]+$.",
            category="validation_error",
        )


def _extract_task_ids(payload: object) -> set[str]:
    if isinstance(payload, Mapping):
        if "tasks" in payload:
            tasks = payload["tasks"]
            if tasks is None:
                raise ProviderError(
                    "Snapshot 'tasks' key is present but null; expected a list or mapping.",
                    category="validation_error",
                )
            if isinstance(tasks, (str, bytes, bytearray)) or not isinstance(tasks, (Mapping, Sequence)):
                raise ProviderError(
                    "Snapshot 'tasks' key must contain a list or mapping.",
                    category="validation_error",
                )
            return _extract_task_ids(tasks)
        if "task_ids" in payload:
            task_ids = payload["task_ids"]
            if task_ids is None:
                raise ProviderError(
                    "Snapshot 'task_ids' key is present but null; expected a list.",
                    category="validation_error",
                )
            if isinstance(task_ids, (str, bytes, bytearray)) or not isinstance(task_ids, Sequence):
                raise ProviderError(
                    "Snapshot 'task_ids' key must contain a non-string sequence.",
                    category="validation_error",
                )
            return _extract_task_ids(task_ids)
        if "id" in payload:
            task_id = payload["id"]
            if isinstance(task_id, str) and task_id:
                _validate_task_id(task_id, "task id")
                return {task_id}
            raise ProviderError("Snapshot task id must be a non-empty string.", category="validation_error")
        if payload:
            raise ProviderError(
                "Snapshot mapping must contain 'tasks', 'task_ids', or 'id'; "
                f"got keys: {sorted(str(k) for k in payload)}.",
                category="validation_error",
            )
        return set()

    if isinstance(payload, Sequence) and not isinstance(payload, (str, bytes, bytearray)):
        ids: set[str] = set()
        for item in payload:
            if isinstance(item, str):
                if not item:
                    raise ProviderError(
                        "Snapshot sequence entries must be non-empty task-id strings or mappings with string 'id'.",
                        category="validation_error",
                    )
                task_id_str: str = item
            elif isinstance(item, Mapping):
                candidate = item.get("id")
                if not isinstance(candidate, str) or not candidate:
                    raise ProviderError(
                        "Snapshot sequence task entries must contain a non-empty string 'id'.",
                        category="validation_error",
                    )
                task_id_str = candidate
            else:
                raise ProviderError(
                    "Snapshot sequence entries must be task-id strings or mappings with string 'id'.",
                    category="validation_error",
                )
            _validate_task_id(task_id_str, "sequence task id")
            if task_id_str in ids:
                raise ProviderError(
                    f"Snapshot sequence contains duplicate task id {task_id_str!r}.",
                    category="validation_error",
                )
            ids.add(task_id_str)
        return ids

    if isinstance(payload, str):
        if not payload:
            raise ProviderError("Snapshot task id string must be non-empty.", category="validation_error")
        _validate_task_id(payload, "task id string")
        return {payload}

    raise ProviderError("Snapshot payload must be a mapping or sequence of task ids.", category="validation_error")


def assert_task_snapshot_invariant(before_probe: object, after_probe: object) -> dict[str, object]:
    """Verify the zero-cost task mutation invariant for a non-destructive probe."""
    before_ids = _extract_task_ids(before_probe)
    after_ids = _extract_task_ids(after_probe)
    before_count = len(before_ids)
    after_count = len(after_ids)
    count_delta = after_count - before_count
    new_ids = after_ids - before_ids

    if count_delta != 0 or new_ids:
        raise ProviderError(
            "Task snapshot invariant violated: task_count_delta must be 0 and no new task IDs may be created.",
            category="logic_error",
        )

    return {
        "task_count_delta": count_delta,
        "task_ids_before": sorted(before_ids),
        "task_ids_after": sorted(after_ids),
        "new_task_ids": sorted(new_ids),
    }


# Preserve the original validator naming while exposing the invariant helper by its newer name.
validate_task_snapshot = assert_task_snapshot_invariant


def render_canonical_body(matrix: Mapping[str, str] | None = None) -> str:
    """Render the canonical body of the availability matrix with the required marker prefix."""
    rendered = canonicalize_matrix(matrix)
    lines = [
        _CANONICAL_BODY_PREFIX,
        "",
        "# Agent Tasks model availability matrix",
        "",
        "| Model | Status |",
        "| --- | --- |",
    ]
    for model_name, status in sorted(rendered.items()):
        lines.append(f"| {_render_markdown_table_cell(model_name)} | {_render_markdown_table_cell(status)} |")
    lines.append("")
    return "\n".join(lines)


# Compatibility alias for the canonical markdown body generator used in older tooling.
build_canonical_body = render_canonical_body


def render_adoption_note(
    matrix: Mapping[str, str] | None = None,
    evidence_path: str | Path | None = None,
) -> str:
    """Render a Markdown ADR summary with the model matrix for publication.

    Args:
        matrix: Model availability mapping to render.  ``None`` falls back to
            the default matrix returned by :func:`build_default_matrix`.
        evidence_path: Path to the evidence JSON file referenced in the ADR
            body.  ``None`` falls back to ``_DEFAULT_EVIDENCE_PATH``.
    """
    rendered = canonicalize_matrix(matrix)
    resolved_evidence_path = Path(evidence_path) if evidence_path is not None else _DEFAULT_EVIDENCE_PATH
    lines = [
        "# Agent Tasks model availability matrix",
        "",
        "**Status**: Accepted",
        "",
        "**Summary**: The Agent Tasks API rejects known-invalid models and accepts valid models when the",
        "base reference is a zero-cost non-existent ref.  The validation order is `model -> custom_agent -> base_ref`.",
        "",
        "## Observed inventory",
        "",
        "| Model | Status |",
        "| --- | --- |",
    ]
    for model_name, status in sorted(rendered.items()):
        lines.append(f"| {_render_markdown_table_cell(model_name)} | {_render_markdown_table_cell(status)} |")
    lines.extend(
        [
            "",
            "## Evidence",
            "",
            "- Validation order: `model -> custom_agent -> base_ref`",
            "- Negative control: `agdt-control-invalid-model-do-not-implement` must return HTTP 400",
            "- Positive control: a known-good model must return HTTP 412 with a base-ref body predicate",
            "- Snapshot invariant: `task_count_delta == 0` and the task ID set is unchanged",
            "",
            "The published evidence is stored in " + _render_markdown_code_span(str(resolved_evidence_path)) + ".",
        ]
    )
    return "\n".join(lines) + "\n"


def _render_markdown_code_span(value: str) -> str:
    """Render a single-line Markdown code span that cannot be terminated early."""
    normalized = " ".join(value.splitlines())
    longest_run = max((len(match.group(0)) for match in re.finditer(r"`+", normalized)), default=0)
    ticks = "`" * max(1, longest_run + 1)
    if normalized.startswith("`") or normalized.endswith("`"):
        return f"{ticks} {normalized} {ticks}"
    return f"{ticks}{normalized}{ticks}"


def _render_markdown_table_cell(value: str) -> str:
    """Escape a Markdown table cell value while keeping the text readable."""
    return " ".join(value.splitlines()).replace("\\", "\\\\").replace("|", r"\|")


def _write_files_atomically(contents_by_target: dict[Path, str]) -> None:
    """Write each target atomically: stage to a temp file, then rename into place.

    Each individual ``os.replace`` is atomic per target. If a later replace fails, a
    best-effort rollback restores already-replaced targets to prior contents (or removes
    ones that did not exist before). Rollback failures are suppressed, so partial updates
    may remain while the original replace failure is re-raised.
    """
    previous_contents: dict[Path, str | None] = {
        target: target.read_text(encoding="utf-8") if target.exists() else None for target in contents_by_target
    }
    previous_modes: dict[Path, int | None] = {
        target: stat.S_IMODE(target.stat().st_mode) if target.exists() else None for target in contents_by_target
    }
    temp_paths: list[tuple[Path, str]] = []
    replaced_targets: list[Path] = []
    try:
        for target, content in contents_by_target.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=target.parent)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as fh:
                    fh.write(content)
                    existing_mode = previous_modes[target]
                    if existing_mode is not None:
                        try:
                            os.fchmod(fh.fileno(), existing_mode)
                        except (AttributeError, OSError):
                            os.chmod(tmp, existing_mode)
            except BaseException:
                # os.fdopen may have raised before taking ownership of fd;
                # close it defensively to avoid a descriptor leak.  If fdopen
                # succeeded but write() raised, the context-manager already
                # closed the descriptor, so we swallow the resulting EBADF.
                # BaseException (not Exception) is caught here so that
                # KeyboardInterrupt and SystemExit do not leak the raw fd or
                # the temporary file.
                try:
                    os.close(fd)
                except OSError:
                    pass
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
                raise
            temp_paths.append((target, tmp))

        for target, tmp in temp_paths:
            os.replace(tmp, target)
            replaced_targets.append(target)
    except BaseException:
        # Best-effort rollback: restore targets already replaced via atomic temp-file
        # replacement. Rollback exceptions are suppressed so the original failure
        # remains visible to the caller.
        # BaseException (not Exception) catches KeyboardInterrupt and SystemExit so
        # that a signal arriving after partial replacements still triggers rollback.
        for target in reversed(replaced_targets):
            prev = previous_contents[target]
            try:
                if prev is None:
                    target.unlink(missing_ok=True)
                else:
                    fd, tmp = tempfile.mkstemp(dir=target.parent)
                    try:
                        with os.fdopen(fd, "w", encoding="utf-8") as fh:
                            fh.write(prev)
                            existing_mode = cast(int, previous_modes[target])
                            try:
                                os.fchmod(fh.fileno(), existing_mode)
                            except (AttributeError, OSError):
                                os.chmod(tmp, existing_mode)
                        os.replace(tmp, target)
                    except Exception:
                        try:
                            os.close(fd)
                        except OSError:
                            pass
                        try:
                            os.unlink(tmp)
                        except OSError:
                            pass
            except Exception:
                # Rollback is best-effort per target; continue so the original
                # publication failure remains the surfaced error.
                pass
        raise
    finally:
        for _, tmp in temp_paths:
            try:
                os.unlink(tmp)
            except OSError:
                pass


def curate_availability_matrix(
    *,
    dry_run: bool = False,
    publish: bool = False,
    matrix: Mapping[str, str] | None = None,
    evidence_path: str | Path | None = None,
    doc_path: str | Path | None = None,
) -> dict[str, Any]:
    """Persist or dry-run the availability matrix and the supporting evidence payload."""
    if dry_run and publish:
        raise ProviderError("`dry_run` and `publish` cannot be used together.", category="validation_error")

    resolved_matrix = canonicalize_matrix(matrix)
    evidence = {
        "marker": _CANONICAL_BODY_PREFIX,
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "validation_order": list(_VALIDATION_ORDER),
        "matrix": resolved_matrix,
        "body": render_canonical_body(resolved_matrix),
    }

    if dry_run:
        return evidence

    repo_root: Path | None = None

    def _repo_root_or_error(target_name: str) -> Path:
        nonlocal repo_root
        if repo_root is None:
            cwd = Path.cwd().resolve()
            for parent in [cwd, *cwd.parents]:
                if (parent / ".git").exists():
                    repo_root = parent
                    break
        if repo_root is None:
            raise ProviderError(
                f"Cannot resolve default {target_name} path because no repository root was found from "
                f"{Path.cwd()!s}; provide an explicit --{target_name}-path value.",
                category="validation_error",
            )
        return repo_root

    evidence_target = (
        Path(evidence_path) if evidence_path is not None else _repo_root_or_error("evidence") / _DEFAULT_EVIDENCE_PATH
    )

    def _lock_path_for_target(target: Path) -> Path:
        # Derive the lock identity from the resolved output target itself
        # (not the current process's working tree/repo root). This ensures
        # that two processes writing to the same explicit absolute
        # ``evidence_path``/``doc_path`` always contend on the same lock,
        # even when launched from different checkouts.
        # Place the lock under the already-ignored ``.agdt-temp/`` directory
        # beside the target so publication never creates untracked files in
        # the working tree.
        resolved = target.resolve(strict=False)
        lock_dir = resolved.parent / ".agdt-temp"
        lock_dir.mkdir(parents=True, exist_ok=True)
        return lock_dir / f"{resolved.name}{_PUBLICATION_LOCK_FILENAME}"

    if publish:
        publish_target = Path(doc_path) if doc_path is not None else _repo_root_or_error("doc") / _DEFAULT_ADR_PATH
        resolved_evidence_target = evidence_target.resolve(strict=False)
        resolved_publish_target = publish_target.resolve(strict=False)
        if resolved_evidence_target == resolved_publish_target:
            raise ProviderError(
                "`evidence_path` and `doc_path` must not resolve to the same file.",
                category="validation_error",
            )
        # Keep the ADR's embedded reference stable across checkouts: use the
        # canonical relative default unless the caller explicitly supplied a
        # custom evidence path. ``evidence_target`` (which may be an
        # absolute, checkout-specific path) is still used for the actual
        # write below.
        adr_evidence_reference = evidence_path if evidence_path is not None else _DEFAULT_EVIDENCE_PATH
        adr_content = render_adoption_note(resolved_matrix, evidence_path=adr_evidence_reference)
        # Acquire both target locks in a deterministic order (sorted by
        # resolved path) so every writer touching either artifact contends
        # on the same locks regardless of argument order.
        lock_targets = sorted((resolved_evidence_target, resolved_publish_target), key=lambda p: p.as_posix())
        with ExitStack() as stack:
            for lock_target in lock_targets:
                stack.enter_context(locked_file(_lock_path_for_target(lock_target), mode="r+"))
            _write_files_atomically(
                {
                    evidence_target: json.dumps(evidence, indent=2, sort_keys=True) + "\n",
                    publish_target: adr_content,
                }
            )
    else:
        with locked_file(_lock_path_for_target(evidence_target), mode="r+"):
            _write_files_atomically({evidence_target: json.dumps(evidence, indent=2, sort_keys=True) + "\n"})

    return evidence


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Curate the Agent Tasks availability matrix snapshot.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the matrix without writing files",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="publish the ADR summary alongside the evidence",
    )
    parser.add_argument(
        "--evidence-path",
        type=str,
        default=None,
        help=f"Path to the evidence JSON file (default: <repo-root>/{_DEFAULT_EVIDENCE_PATH.as_posix()})",
    )
    parser.add_argument(
        "--doc-path",
        type=str,
        default=None,
        help=f"Path to the published ADR markdown (default: <repo-root>/{_DEFAULT_ADR_PATH.as_posix()})",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    result = curate_availability_matrix(
        dry_run=args.dry_run,
        publish=args.publish,
        evidence_path=args.evidence_path,
        doc_path=args.doc_path,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
