"""Structured event recording for Phase 0 observability (spec #1812, FR-001).

This module implements the typed run/event models, sanitization, property-array
normalization, secret redaction, canonical JSON serialization, and runtime log
persistence required by FR-001, FR-010, FR-011, and FR-012. Workflow YAML and
provider-adapter integration build on top of these primitives; this module has
no I/O side effects beyond :func:`write_log`.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, unquote, urlsplit

from agentic_devtools.cli.speckit.phase0.identifiers import (
    derive_run_id,
    derive_source,
    validate_issue_id,
    validate_operation_id,
)

__all__ = [
    "SCHEMA_VERSION",
    "RUN_OUTCOMES",
    "STAGE_NAMES",
    "TERMINATION_CODES",
    "RETRY_MODES",
    "CONFIGURATION_DECISIONS",
    "PROVIDERS",
    "SOURCES",
    "MARKDOWN_ESCAPE_MAP",
    "StageEvent",
    "RunRecord",
    "Recorder",
    "sanitize_control_characters",
    "sanitize_markdown",
    "redact_secrets",
    "truncate_utf8",
    "normalize_property_entries",
    "normalize_missing_properties",
    "compute_resumability",
    "compute_next_action",
    "serialize_run_document",
    "write_log",
]

SCHEMA_VERSION = "1.0"

RUN_OUTCOMES = frozenset({"in_progress", "succeeded", "failed", "blocked", "skipped", "partial"})

STAGE_NAMES = (
    "validation",
    "property_discovery",
    "branch_creation",
    "artifact_generation",
    "commit",
    "pull_request",
    "cleanup",
    "issue_comment",
)

TERMINATION_CODES = frozenset({"workflow-cancelled", "workflow-timeout"})

RETRY_MODES = frozenset({"resumed", "restarted"})

CONFIGURATION_DECISIONS = frozenset({"enabled", "disabled", "blocked", "not-evaluated"})

PROVIDERS = frozenset({"github", "jira", "markdown"})

SOURCES = frozenset({"retry", "manual-dispatch", "repository-dispatch", "provider-event"})

# FR-001: diagnostic_code must consist of printable, non-whitespace ASCII (U+0021–U+007E).
_DIAGNOSTIC_CODE_RE = re.compile(r"^[!-~]+$")

# FR-012(a): control characters and Unicode line separators replaced with U+FFFD.
_CONTROL_CHAR_PATTERN = re.compile("[\u0000-\u001f\u007f\u0085\u2028\u2029]")
_RFC3339_UTC_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_RUN_ID_PATTERN = re.compile(r"^gh:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+:[1-9]\d*:[1-9]\d*$")

# FR-012(b): exact character-to-token Markdown escape mapping, applied in a
# single pass over the already control-sanitized text.
MARKDOWN_ESCAPE_MAP: dict[str, str] = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "`": "&#96;",
    "#": "&#35;",
    "*": "&#42;",
    "_": "&#95;",
    "[": "&#91;",
    "]": "&#93;",
    "(": "&#40;",
    ")": "&#41;",
    "|": "&#124;",
    "\\": "&#92;",
    "~": "&#126;",
    "@": "&#64;",
}

# FR-011: heuristic redaction of secrets/authorization material that may appear
# in provider or command error output. Order matters: header-shaped patterns
# are matched before bare-token patterns so the surrounding context is
# replaced as a unit. Quoted-value patterns must come before the unquoted
# key/value pattern so multi-word credential values are not missed.
_REDACTION_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    # URL userinfo (******host/…) — strip credentials before hostname.
    (
        re.compile(r"(?i)(https?://)([^@/\s]+:[^@/\s]+@)"),
        r"\1[REDACTED]@",
    ),
    # CLI flag credentials: --token VALUE, --password VALUE, --secret VALUE, etc.
    # Matches --flag or -f followed by a value that is one of:
    #   - a double-quoted string (may contain spaces): "secret value"
    #   - a single-quoted string (may contain spaces): 'secret value'
    #   - an unquoted non-whitespace token that does not start with "-"
    (
        re.compile(
            r"(?i)(?P<flag>--?(?:token|password|passwd|secret|api[-_]?key|auth(?:orization)?|key|pat|access[-_]?token|refresh[-_]?token|private[-_]?key|client[-_]?secret))"
            r"""(?P<sep>\s+)(?P<val>"[^"]*"|'[^']*'|[^\-\s]\S*)""",
        ),
        r"\g<flag>\g<sep>[REDACTED]",
    ),
    # Authorization header values (all schemes) — unquoted form.
    (
        re.compile(r"(?im)\b(authorization\s*:\s*)[^\r\n]+"),
        r"\1[REDACTED]",
    ),
    # Authorization headers in quoted JSON / dict form, preserving paired quote delimiters.
    (
        re.compile(
            r"""(?i)(?P<key_quote>["'])authorization(?P=key_quote)\s*:\s*(?P<value_quote>["'])
            (?:(?!(?P=value_quote)|\\).|\\.)*(?P=value_quote)""",
            re.VERBOSE | re.DOTALL,
        ),
        r"\g<key_quote>Authorization\g<key_quote>: \g<value_quote>[REDACTED]\g<value_quote>",
    ),
    (re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]+"), "[REDACTED]"),
    (
        re.compile(r"(?i)\bbasic\s+[A-Za-z0-9+/]+=*"),
        "[REDACTED]",
    ),
    # GitHub personal-access / app / installation tokens.
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "[REDACTED]"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), "[REDACTED]"),
    # AWS access key IDs.
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED]"),
    # JSON/string-quoted values (may contain whitespace or escaped chars); must
    # be evaluated before the unquoted pattern so "two word" secrets are caught.
    # Compound names (e.g. refresh_token, id_token, AWS_SECRET_ACCESS_KEY,
    # private_key, accessToken, refreshToken, privateKey, openaiApiKey) are
    # matched first so the full identifier is preserved in the replacement; bare
    # sensitive words follow as fallbacks. The suffix pattern is intentionally
    # broad: in a security-redaction context over-redacting benign values is
    # preferable to leaking credentials.
    (
        re.compile(
            r"(?i)(?P<kq>[\"']?)\b"
            r"(?P<kn>[a-zA-Z_]\w*[_-](?:key|token|secret|pat)|[a-zA-Z_]\w*(?:Key|Token|Secret|Pat)\b|api[_-]?key|token|secret|pat|password|passwd|client[_-]?secret)"
            r"(?P=kq)(?P<ksep>\s*[:=]\s*)"
            r"(?P<vq>[\"'])(?P<qval>(?:\\.|(?!(?P=vq)).)*)(?P=vq)"
        ),
        r"\g<kq>\g<kn>\g<kq>\g<ksep>\g<vq>[REDACTED]\g<vq>",
    ),
    # key=value / key: value style secrets (token, password, secret, api key).
    # Compound names (e.g. refresh_token, private_key, accessToken, refreshToken,
    # privateKey) are matched first; the suffix pattern is intentionally broad for
    # the same reason as above.
    # The trailing (?P=value_quote)? is intentionally optional: provider and
    # command error messages can be truncated mid-string, so an unterminated
    # quoted value must still be redacted (FR-011 conservative fallback).
    # Accepted trade-off: when the opening quote is present but the closing quote
    # is absent (truncated input), the replacement re-emits the opening quote as
    # the closing delimiter (e.g. `password: "secret` → `password: "[REDACTED]"`).
    # The output is syntactically different from the truncated input, but the
    # credential is fully suppressed, which is the security-correct outcome.
    (
        re.compile(
            r"(?i)(?P<key_quote>[\"']?)\b"
            r"(?P<key>[a-zA-Z_]\w*[_-](?:key|token|secret|pat)|[a-zA-Z_]\w*(?:Key|Token|Secret|Pat)\b|api[_-]?key|token|secret|pat|password|passwd|client[_-]?secret)"
            r"(?P=key_quote)(?P<separator>\s*[:=]\s*)"
            r"(?P<value_quote>[\"']?)(?P<value>[^\"'&,;]+)(?P=value_quote)?"
        ),
        r"\g<key_quote>\g<key>\g<key_quote>\g<separator>\g<value_quote>[REDACTED]\g<value_quote>",
    ),
)


def sanitize_control_characters(text: str) -> str:
    """Replace ASCII control characters and Unicode line separators with U+FFFD.

    Implements FR-012(a): the guaranteed first pass applied to every untrusted
    value before any Markdown escaping or truncation.
    """
    return _CONTROL_CHAR_PATTERN.sub("\ufffd", text)


def sanitize_markdown(text: str) -> str:
    """Apply the full FR-012(a)+(b) sanitization contract for Markdown surfaces.

    Control characters are replaced first (a), then Markdown-significant
    characters are replaced with their literal tokens in a single pass over the
    already-sanitized text (b), so already-substituted entity sequences are
    never re-escaped.
    """
    sanitized = sanitize_control_characters(text)
    return "".join(MARKDOWN_ESCAPE_MAP.get(char, char) for char in sanitized)


def redact_secrets(text: str) -> str:
    """Redact credentials and authorization material from *text* (FR-011).

    This is applied before :func:`sanitize_control_characters`/
    :func:`sanitize_markdown` per FR-012's closing sentence ("Secret redaction
    defined in FR-011 is applied before sanitization"). The patterns cover
    common authorization-header, bearer-token, GitHub/AWS credential, and
    generic ``key=value`` secret shapes that may appear in provider or command
    error output.
    """
    result = text
    for pattern, replacement in _REDACTION_PATTERNS:
        result = pattern.sub(replacement, result)
    return result


_SENSITIVE_QUERY_KEYS = frozenset(
    {"access_token", "authorization", "api_key", "client_secret", "password", "secret", "token", "pat"}
)

_CAMEL_UPPER_BOUNDARY = re.compile(r"([A-Z]+)([A-Z][a-z])")
_CAMEL_LOWER_BOUNDARY = re.compile(r"([a-z\d])([A-Z])")


def _normalize_query_key(key: str) -> str:
    """Normalize a query parameter key to snake_case for sensitive-key detection.

    Handles camelCase boundaries (``accessToken`` → ``access_token``,
    ``APIKey`` → ``api_key``), hyphen separators (``api-key`` → ``api_key``),
    and case folding so that camelCase and hyphenated forms are matched against
    :data:`_SENSITIVE_QUERY_KEYS` in the same way as their snake_case equivalents.
    """
    s = _CAMEL_UPPER_BOUNDARY.sub(r"\1_\2", key)
    s = _CAMEL_LOWER_BOUNDARY.sub(r"\1_\2", s)
    return s.lower().replace("-", "_")


def _contains_redactable_secret(value: str) -> bool:
    return redact_secrets(value) != value


def _decode_to_fixed_point(value: str) -> str:
    """Repeatedly percent-decode *value* until no further change occurs.

    A single :func:`~urllib.parse.unquote` call cannot detect doubly
    percent-encoded secrets such as ``token%253Ds3cr3t`` (first pass yields
    ``token%3Ds3cr3t``; only the second pass exposes ``token=s3cr3t``).
    """
    while True:
        decoded = unquote(value)
        if decoded == value:
            return value
        value = decoded


def _validate_diagnostic_url(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("diagnostic_url must be a string")
    if any(ord(char) <= 0x20 or ord(char) == 0x7F for char in value):
        raise ValueError("diagnostic_url must not contain whitespace or control characters")
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        _ = parsed.port
    except ValueError as exc:
        raise ValueError("diagnostic_url must be an absolute HTTPS URL") from exc
    if parsed.scheme.lower() != "https" or not parsed.netloc or hostname is None:
        raise ValueError("diagnostic_url must be an absolute HTTPS URL")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("diagnostic_url must not contain userinfo")
    if parsed.fragment:
        raise ValueError("diagnostic_url must not contain URL fragments")
    if (
        _contains_redactable_secret(value)
        or _contains_redactable_secret(_decode_to_fixed_point(parsed.path))
        or _contains_redactable_secret(_decode_to_fixed_point(parsed.query))
    ):
        raise ValueError("diagnostic_url must not contain secrets or authorization material")
    query_pairs = parse_qsl(parsed.query, keep_blank_values=True)
    if any(_normalize_query_key(key) in _SENSITIVE_QUERY_KEYS for key, _ in query_pairs):
        raise ValueError("diagnostic_url must not contain sensitive query parameters")
    for key, query_value in query_pairs:
        decoded_pairs = (
            _decode_to_fixed_point(key),
            _decode_to_fixed_point(query_value),
            _decode_to_fixed_point(f"{key}={query_value}"),
        )
        if any(_contains_redactable_secret(candidate) for candidate in decoded_pairs):
            raise ValueError("diagnostic_url must not contain secrets or authorization material")
    return value


def truncate_utf8(text: str, *, byte_limit: int = 1024, prefix_limit: int = 1018, marker: str = "\u2026[T]") -> str:
    """Truncate *text* to at most *byte_limit* UTF-8 bytes (FR-012(e)).

    When the UTF-8 encoding of *text* exceeds *byte_limit* bytes, the value is
    truncated to the longest UTF-8-safe prefix that fits within the available
    budget (``min(prefix_limit, byte_limit - len(marker.encode()))`` bytes)
    and *marker* is appended, so the result is guaranteed to be at most
    *byte_limit* bytes.

    Raises:
        ValueError: If *prefix_limit* is negative, or if *marker*'s UTF-8
            encoding is longer than *byte_limit*.
    """
    if prefix_limit < 0:
        raise ValueError(f"prefix_limit must be non-negative, got {prefix_limit}")

    encoded = text.encode("utf-8")
    if len(encoded) <= byte_limit:
        return text

    marker_bytes = len(marker.encode("utf-8"))
    if marker_bytes > byte_limit:
        raise ValueError(f"marker is {marker_bytes} bytes, which exceeds byte_limit={byte_limit}")

    effective_prefix_limit = min(prefix_limit, byte_limit - marker_bytes)
    prefix_bytes = encoded[:effective_prefix_limit]
    while prefix_bytes:
        try:
            prefix_text = prefix_bytes.decode("utf-8")
            break
        except UnicodeDecodeError:
            prefix_bytes = prefix_bytes[:-1]
    else:
        prefix_text = ""

    return f"{prefix_text}{marker}"


def _sort_key(value: str) -> bytes:
    """Sort key producing ascending bytewise UTF-8 order (FR-001)."""
    return value.encode("utf-8")


def _require_non_empty_string(value: object, *, field_name: str) -> str:
    """Return *value* when it is a non-empty string, else raise ValueError."""
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


def normalize_property_entries(
    entries: list[dict[str, str]] | None,
    *,
    name_key: str = "name",
    value_key: str | None = None,
) -> list[dict[str, str]]:
    """Sort and deduplicate a property-mapping array by ascending UTF-8 order.

    Used for ``capturedProperties`` and ``excludedProperties`` (FR-001): each
    entry is a mapping keyed by *name_key* plus one additional descriptive
    field; entries are ordered by ascending bytewise UTF-8 order of the name
    field with duplicate names removed (first occurrence wins).

    When *value_key* is supplied the output entries are whitelisted to the two
    permitted keys (*name_key* and *value_key*), and the value field is
    redacted through :func:`redact_secrets` before being stored (FR-011).
    Extra keys in the caller-supplied entries are silently discarded.

    Args:
        entries: The unordered property-mapping entries, or ``None``.
        name_key: The dict key holding the property name (default ``"name"``).
        value_key: When given, the only additional key retained in the output.
            Extra keys are dropped; the value is passed through
            :func:`redact_secrets` to guard against leaking authorization
            material (FR-011).

    Returns:
        A new list, sorted and deduplicated; ``[]`` when *entries* is falsy.
    """
    if not entries:
        return []

    deduped: dict[str, dict[str, str]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError(f"each entry in property list must be a dict, got {type(entry).__name__!r}")
        name = _require_non_empty_string(entry.get(name_key), field_name=name_key)
        name = sanitize_control_characters(redact_secrets(name))
        if name not in deduped:
            if value_key is not None:
                raw_value = _require_non_empty_string(entry.get(value_key), field_name=value_key)
                kept: dict[str, str] = {
                    name_key: name,
                    value_key: redact_secrets(raw_value),
                }
            else:
                kept = {**entry, name_key: name}
            deduped[name] = kept

    return [deduped[name] for name in sorted(deduped, key=_sort_key)]


def normalize_missing_properties(values: list[str] | None) -> list[str]:
    """Sort and deduplicate ``missingProperties`` by ascending UTF-8 order (FR-001)."""
    if not values:
        return []
    return sorted(
        dict.fromkeys(
            sanitize_control_characters(
                redact_secrets(_require_non_empty_string(value, field_name="missingProperties"))
            )
            for value in values
        ),
        key=_sort_key,
    )


# FR-010: deterministic resumability mapping from last stage + retained durable outputs.
def compute_resumability(
    *,
    last_stage: str | None,
    artifact_branch: str | None,
    artifact_path: str | None,
    commit_sha: str | None,
) -> str:
    """Compute the FR-010 resumability token for a ``failed``/``partial`` run.

    Args:
        last_stage: ``run.lastStage``, or ``None``.
        artifact_branch: ``run.artifactBranch``, or ``None``.
        artifact_path: ``run.artifactPath``, or ``None``.
        commit_sha: ``run.commitSha``, or ``None``.

    Returns:
        ``"retry-safe:from-start"`` or ``"resume-safe:<stage>"`` per the exact
        FR-010 mapping.
    """
    if last_stage in (None, "validation", "property_discovery", "branch_creation", "cleanup", "issue_comment"):
        return "retry-safe:from-start"
    if last_stage == "artifact_generation":
        return "resume-safe:artifact_generation" if artifact_branch is not None else "retry-safe:from-start"
    if last_stage == "commit":
        return (
            "resume-safe:commit"
            if artifact_branch is not None and artifact_path is not None
            else "retry-safe:from-start"
        )
    if last_stage == "pull_request":
        return (
            "resume-safe:pull_request"
            if artifact_branch is not None and artifact_path is not None and commit_sha is not None
            else "retry-safe:from-start"
        )
    return "retry-safe:from-start"


def compute_next_action(
    *,
    final_outcome: str,
    last_stage: str | None,
    artifact_branch: str | None,
    artifact_path: str | None,
    commit_sha: str | None,
) -> str:
    """Compute the FR-010 ``Next Action`` value for FR-003/FR-004 projections.

    Args:
        final_outcome: One of :data:`RUN_OUTCOMES`.
        last_stage: ``run.lastStage``, or ``None``.
        artifact_branch: ``run.artifactBranch``, or ``None``.
        artifact_path: ``run.artifactPath``, or ``None``.
        commit_sha: ``run.commitSha``, or ``None``.

    Returns:
        One of ``"none"``, ``"manual-intervention-required"``,
        ``"resume-safe:<stage>"``, or ``"retry-safe:from-start"``.
    """
    if final_outcome in ("succeeded", "skipped"):
        return "none"
    if final_outcome == "blocked":
        return "manual-intervention-required"
    if final_outcome in ("failed", "partial"):
        return compute_resumability(
            last_stage=last_stage,
            artifact_branch=artifact_branch,
            artifact_path=artifact_path,
            commit_sha=commit_sha,
        )
    raise ValueError(f"Cannot derive next action for in-progress final_outcome: {final_outcome!r}")


@dataclass
class StageEvent:
    """A single Phase 0 stage transition record (FR-001)."""

    sequence: int
    stage: str
    status: str
    timestamp: str
    message: str
    diagnostic_code: str | None = None
    captured_properties: list[dict[str, str]] = field(default_factory=list)
    excluded_properties: list[dict[str, str]] = field(default_factory=list)
    missing_properties: list[str] = field(default_factory=list)
    diagnostic_url: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "stage": self.stage,
            "status": self.status,
            "timestamp": self.timestamp,
            "diagnosticCode": self.diagnostic_code,
            "message": self.message,
            "capturedProperties": self.captured_properties,
            "excludedProperties": self.excluded_properties,
            "missingProperties": self.missing_properties,
            "diagnosticUrl": self.diagnostic_url,
        }


@dataclass
class RunRecord:
    """The FR-001 ``run`` object: stable identity, decisions, and outcome state."""

    repository: str
    workflow_run_id: int
    workflow_run_attempt: int
    run_id: str
    operation_id: str
    issue_id: str
    trigger: str
    source: str
    provider: str
    configuration_decision: str
    configuration_reason: str
    started_at: str
    updated_at: str
    workflow_run_url: str
    retry_of_run_id: str | None = None
    retry_mode: str | None = None
    issue_type: str | None = None
    selected_template: str | None = None
    final_outcome: str = "in_progress"
    last_stage: str | None = None
    freshness: str = "not-evaluated"
    artifact_branch: str | None = None
    artifact_path: str | None = None
    commit_sha: str | None = None
    pull_request_url: str | None = None
    termination_code: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "repository": self.repository,
            "workflowRunId": self.workflow_run_id,
            "workflowRunAttempt": self.workflow_run_attempt,
            "runId": self.run_id,
            "operationId": self.operation_id,
            "issueId": self.issue_id,
            "retryOfRunId": self.retry_of_run_id,
            "retryMode": self.retry_mode,
            "trigger": self.trigger,
            "source": self.source,
            "provider": self.provider,
            "issueType": (
                sanitize_control_characters(redact_secrets(self.issue_type)) if self.issue_type is not None else None
            ),
            "configurationDecision": self.configuration_decision,
            "configurationReason": sanitize_control_characters(redact_secrets(self.configuration_reason)),
            "selectedTemplate": (
                sanitize_control_characters(redact_secrets(self.selected_template))
                if self.selected_template is not None
                else None
            ),
            "finalOutcome": self.final_outcome,
            "lastStage": self.last_stage,
            "startedAt": self.started_at,
            "updatedAt": self.updated_at,
            "freshness": self.freshness,
            "artifactBranch": (
                sanitize_control_characters(redact_secrets(self.artifact_branch))
                if self.artifact_branch is not None
                else None
            ),
            "artifactPath": (
                sanitize_control_characters(redact_secrets(self.artifact_path))
                if self.artifact_path is not None
                else None
            ),
            "commitSha": (
                sanitize_control_characters(redact_secrets(self.commit_sha)) if self.commit_sha is not None else None
            ),
            "workflowRunUrl": self.workflow_run_url,
            "pullRequestUrl": self.pull_request_url,
        }


def _is_rfc3339_utc_timestamp(value: object) -> bool:
    if not isinstance(value, str) or _RFC3339_UTC_PATTERN.fullmatch(value) is None:
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def _is_valid_run_id(value: object) -> bool:
    return isinstance(value, str) and _RUN_ID_PATTERN.fullmatch(value) is not None


def _validate_nullable_string_field(value: object, field_name: str) -> None:
    """Raise *ValueError* if *value* is non-None but not a non-empty string."""
    if value is not None and (not isinstance(value, str) or not value):
        raise ValueError(f"{field_name} must be a non-empty string or null, got {value!r}")


def _validate_https_url(value: object, field_name: str) -> None:
    """Raise *ValueError* unless *value* is a non-empty absolute HTTPS URL string."""
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be a non-empty string")
    if any(ord(c) <= 0x20 or ord(c) == 0x7F for c in value):
        raise ValueError(f"{field_name} must not contain whitespace or control characters")
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        _ = parsed.port  # raises ValueError for non-numeric ports
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a valid absolute HTTPS URL") from exc
    if parsed.scheme.lower() != "https" or not parsed.netloc or hostname is None:
        raise ValueError(f"{field_name} must be an absolute HTTPS URL")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError(f"{field_name} must not contain userinfo")


def _validate_document_invariants(run: RunRecord, events: list[StageEvent]) -> None:
    try:
        expected_run_id = derive_run_id(run.repository, run.workflow_run_id, run.workflow_run_attempt)
    except ValueError as exc:
        raise ValueError("Invalid run coordinate fields for run_id derivation") from exc
    if run.run_id != expected_run_id:
        raise ValueError("run_id must match repository/workflow_run_id/workflow_run_attempt")
    if not validate_operation_id(run.operation_id):
        raise ValueError(f"Invalid operation_id: {run.operation_id!r}")
    if not validate_issue_id(run.issue_id):
        raise ValueError(f"Invalid issue_id: {run.issue_id!r}")
    if not isinstance(run.trigger, str) or not run.trigger:
        raise ValueError("trigger must be a non-empty string")
    if not isinstance(run.configuration_reason, str) or not run.configuration_reason:
        raise ValueError("configuration_reason must be a non-empty string")
    _validate_https_url(run.workflow_run_url, "workflow_run_url")
    if run.pull_request_url is not None:
        _validate_https_url(run.pull_request_url, "pull_request_url")
    _validate_nullable_string_field(run.issue_type, "issue_type")
    _validate_nullable_string_field(run.selected_template, "selected_template")
    _validate_nullable_string_field(run.artifact_branch, "artifact_branch")
    _validate_nullable_string_field(run.artifact_path, "artifact_path")
    _validate_nullable_string_field(run.commit_sha, "commit_sha")
    if run.final_outcome not in RUN_OUTCOMES:
        raise ValueError(f"Unknown final_outcome: {run.final_outcome!r}")
    if run.source not in SOURCES:
        raise ValueError(f"Unknown source: {run.source!r}")
    if run.configuration_decision not in CONFIGURATION_DECISIONS:
        raise ValueError(f"Unknown configuration_decision: {run.configuration_decision!r}")
    if run.configuration_decision == "disabled" and run.final_outcome not in {"skipped", "failed"}:
        raise ValueError(
            f"final_outcome must be 'skipped' or 'failed' when configuration_decision is 'disabled', "
            f"got final_outcome={run.final_outcome!r}"
        )
    if run.configuration_decision == "disabled" and run.final_outcome == "failed" and run.termination_code is None:
        raise ValueError("termination_code must be set for a 'disabled' run with final_outcome='failed'")
    if run.configuration_decision == "blocked" and run.final_outcome not in {"blocked", "failed"}:
        raise ValueError(
            f"final_outcome must be 'blocked' or 'failed' when configuration_decision is 'blocked', "
            f"got final_outcome={run.final_outcome!r}"
        )
    if run.configuration_decision == "blocked" and run.final_outcome == "failed" and run.termination_code is None:
        raise ValueError("termination_code must be set for a 'blocked' run with final_outcome='failed'")
    if run.configuration_decision == "not-evaluated" and run.final_outcome != "failed":
        raise ValueError(
            f"final_outcome must be 'failed' when configuration_decision is 'not-evaluated', "
            f"got final_outcome={run.final_outcome!r}"
        )
    if run.configuration_decision == "not-evaluated" and run.freshness != "not-evaluated":
        raise ValueError("freshness must be 'not-evaluated' when configuration_decision is 'not-evaluated'")
    if run.configuration_decision == "not-evaluated" and run.termination_code is None:
        raise ValueError("termination_code must be set when configuration_decision is 'not-evaluated'")
    if run.provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: {run.provider!r}")
    if run.termination_code is not None and run.termination_code not in TERMINATION_CODES:
        raise ValueError(f"Unknown termination code: {run.termination_code!r}")
    if run.termination_code is not None and run.final_outcome != "failed":
        raise ValueError(
            f"termination_code may only be set when final_outcome is 'failed', got final_outcome={run.final_outcome!r}"
        )
    if run.last_stage is not None and run.last_stage not in STAGE_NAMES:
        raise ValueError(f"Unknown last_stage: {run.last_stage!r}")
    if run.freshness not in {"fresh", "stale", "unknown-freshness", "not-evaluated"}:
        raise ValueError(f"Unknown freshness: {run.freshness!r}")
    if run.configuration_decision == "disabled" and run.freshness != "not-evaluated":
        raise ValueError("freshness must be 'not-evaluated' when configuration_decision is 'disabled'")
    if not _is_rfc3339_utc_timestamp(run.started_at):
        raise ValueError(f"Invalid started_at timestamp: {run.started_at!r}")
    if not _is_rfc3339_utc_timestamp(run.updated_at):
        raise ValueError(f"Invalid updated_at timestamp: {run.updated_at!r}")
    is_retry_operation = run.operation_id.startswith("gh-retry:")
    if is_retry_operation:
        if not _is_valid_run_id(run.retry_of_run_id):
            raise ValueError("retry_of_run_id must be a canonical runId when operation_id is a retry operation")
        if run.retry_of_run_id == run.run_id:
            raise ValueError("retry_of_run_id must reference a prior run, not the current run_id")
        # Validate that the run_id/attempt embedded in the retry operation_id match this record.
        # Format: gh-retry:<chain_op_id>:<decision_time>:<workflow_run_id>:<workflow_run_attempt>
        # validate_operation_id already confirmed the format, so int() cannot raise here.
        tail = run.operation_id.rsplit(":", 2)
        embedded_run_id = int(tail[-2])
        embedded_attempt = int(tail[-1])
        if embedded_run_id != run.workflow_run_id or embedded_attempt != run.workflow_run_attempt:
            raise ValueError(
                "retry operation_id run/attempt coordinates must match "
                f"workflow_run_id={run.workflow_run_id} and workflow_run_attempt={run.workflow_run_attempt}"
            )
    elif run.retry_of_run_id is not None:
        raise ValueError("retry_of_run_id must be null for non-retry operation_id values")
    if is_retry_operation:
        if run.retry_mode not in RETRY_MODES:
            raise ValueError(
                f"retry_mode must be one of {sorted(RETRY_MODES)!r} for retry operations, got {run.retry_mode!r}"
            )
    elif run.retry_mode is not None:
        raise ValueError("retry_mode must be null for non-retry operation_id values")
    expected_source = derive_source(
        run.trigger,
        retry_of_run_id=run.retry_of_run_id,
        operation_id=run.operation_id,
    )
    if run.source != expected_source:
        raise ValueError(f"source must match derived source {expected_source!r}, got {run.source!r}")
    for expected_sequence, event in enumerate(events, start=1):
        if isinstance(event.sequence, bool) or not isinstance(event.sequence, int):
            raise ValueError(f"event.sequence must be a positive integer, got {event.sequence!r}")
        if event.sequence != expected_sequence:
            raise ValueError("events must have contiguous sequence numbers starting at 1")
        if event.stage not in STAGE_NAMES:
            raise ValueError(f"Unknown event stage: {event.stage!r}")
        if event.status not in RUN_OUTCOMES:
            raise ValueError(f"Unknown event status: {event.status!r}")
        if not _is_rfc3339_utc_timestamp(event.timestamp):
            raise ValueError(f"Invalid event timestamp: {event.timestamp!r}")

    if not events and run.last_stage is not None:
        raise ValueError("run.last_stage must be null when no events are recorded")
    if not events:
        is_disabled_skip = run.configuration_decision == "disabled" and run.final_outcome == "skipped"
        is_pre_stage_termination = run.final_outcome == "failed" and run.termination_code in {
            "workflow-cancelled",
            "workflow-timeout",
        }
        if not is_disabled_skip and not is_pre_stage_termination:
            raise ValueError(
                "events may be empty only for disabled/skipped runs or pre-stage cancelled/timeout failures"
            )
    if events and run.last_stage != events[-1].stage:
        raise ValueError("run.last_stage must equal the stage of the last recorded event")


def _serialize_event(event: StageEvent) -> dict[str, Any]:
    if event.diagnostic_code is not None and _DIAGNOSTIC_CODE_RE.fullmatch(event.diagnostic_code) is None:
        raise ValueError(
            f"diagnostic_code must be printable non-whitespace ASCII (U+0021-U+007E): {event.diagnostic_code!r}"
        )
    _validate_diagnostic_url(event.diagnostic_url)
    payload = event.to_dict()
    payload["message"] = sanitize_control_characters(redact_secrets(event.message))
    payload["capturedProperties"] = normalize_property_entries(event.captured_properties, value_key="templateSection")
    payload["excludedProperties"] = normalize_property_entries(event.excluded_properties, value_key="reason")
    payload["missingProperties"] = normalize_missing_properties(event.missing_properties)
    return payload


def serialize_run_document(run: RunRecord, events: list[StageEvent]) -> dict[str, Any]:
    """Assemble the exact FR-001 top-level structured-log JSON document."""
    _validate_document_invariants(run, events)
    return {
        "schemaVersion": SCHEMA_VERSION,
        "terminationCode": run.termination_code,
        "run": run.to_dict(),
        "events": [_serialize_event(event) for event in events],
    }


def write_log(document: dict[str, Any], path: str | Path) -> None:
    """Write the FR-001 structured-log *document* as a single UTF-8 JSON file.

    Args:
        document: The document produced by :func:`serialize_run_document`.
        path: The destination path (parent directories are created as needed).
    """
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class Recorder:
    """Accumulates :class:`StageEvent` records for one Phase 0 run.

    The recorder owns sequence assignment, message sanitization (secret
    redaction followed by control-character sanitization), property-array
    normalization, and keeping ``run.lastStage``/``run.updatedAt`` in sync with
    the most recently recorded event.
    """

    def __init__(self, run: RunRecord) -> None:
        self.run = run
        self.events: list[StageEvent] = []

    def record(
        self,
        *,
        stage: str,
        status: str,
        message: str,
        timestamp: str,
        diagnostic_code: str | None = None,
        captured_properties: list[dict[str, str]] | None = None,
        excluded_properties: list[dict[str, str]] | None = None,
        missing_properties: list[str] | None = None,
        diagnostic_url: str | None = None,
    ) -> StageEvent:
        """Record one stage event, assigning the next sequence number.

        Args:
            stage: One of :data:`STAGE_NAMES`.
            status: One of :data:`RUN_OUTCOMES`.
            message: A single-line, user-safe description (sanitized here).
            timestamp: The RFC3339 UTC event timestamp.
            diagnostic_code: Optional ASCII-printable diagnostic code.
            captured_properties: Optional unsorted list of ``{"name", "templateSection"}``.
            excluded_properties: Optional unsorted list of ``{"name", "reason"}``.
            missing_properties: Optional unsorted list of property-name strings.
            diagnostic_url: Optional absolute HTTPS diagnostic URL.

        Returns:
            The recorded :class:`StageEvent`.
        """
        if stage not in STAGE_NAMES:
            raise ValueError(f"Unknown Phase 0 stage: {stage!r}")
        if status not in RUN_OUTCOMES:
            raise ValueError(f"Unknown Phase 0 status: {status!r}")
        if diagnostic_code is not None and _DIAGNOSTIC_CODE_RE.fullmatch(diagnostic_code) is None:
            raise ValueError(
                f"diagnostic_code must be printable non-whitespace ASCII (U+0021-U+007E): {diagnostic_code!r}"
            )

        sanitized_message = sanitize_control_characters(redact_secrets(message))

        event = StageEvent(
            sequence=len(self.events) + 1,
            stage=stage,
            status=status,
            timestamp=timestamp,
            message=sanitized_message,
            diagnostic_code=diagnostic_code,
            captured_properties=normalize_property_entries(captured_properties, value_key="templateSection"),
            excluded_properties=normalize_property_entries(excluded_properties, value_key="reason"),
            missing_properties=normalize_missing_properties(missing_properties),
            diagnostic_url=_validate_diagnostic_url(diagnostic_url),
        )
        self.events.append(event)
        self.run.last_stage = stage
        self.run.updated_at = timestamp
        return event

    def finalize(
        self, *, final_outcome: str, termination_code: str | None = None, updated_at: str | None = None
    ) -> None:
        """Set the run's terminal outcome and optional termination code."""
        if final_outcome not in RUN_OUTCOMES:
            raise ValueError(f"Unknown Phase 0 final outcome: {final_outcome!r}")
        if final_outcome == "in_progress":
            raise ValueError("'in_progress' is not a valid terminal outcome for finalize()")
        if termination_code is not None and termination_code not in TERMINATION_CODES:
            raise ValueError(f"Unknown termination code: {termination_code!r}")
        if termination_code is not None and final_outcome != "failed":
            raise ValueError(
                f"termination_code may only be set when final_outcome is 'failed', got final_outcome={final_outcome!r}"
            )
        self.run.final_outcome = final_outcome
        self.run.termination_code = termination_code
        if updated_at is not None:
            self.run.updated_at = updated_at

    def to_document(self) -> dict[str, Any]:
        """Assemble the full FR-001 structured-log document for this run."""
        return serialize_run_document(self.run, self.events)
