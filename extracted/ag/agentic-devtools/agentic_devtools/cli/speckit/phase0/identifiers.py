"""Identifier derivation, validation, and canonicalization for Phase 0 observability.

This module implements the identity contracts defined by spec #1812 FR-001:

- ``runId`` — the per-attempt correlation identity (``gh:<owner>/<repo>:<workflow_run_id>:<workflow_run_attempt>``).
- ``operationId`` — the semantic delivery/retry identity used for duplicate-delivery
  suppression, derived from a webhook delivery ID, a retry decision, or (as a last
  resort) a canonical hash of the provider event payload.
- ``issueId`` — the percent-encoded, provider-neutral, token-safe issue reference.

All functions here are pure and deterministic: given the same inputs they always
produce the same output, with no I/O and no reliance on wall-clock time except
where a timestamp is explicitly supplied by the caller.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import UTC, datetime
from typing import Any

__all__ = [
    "OPERATION_ID_PATTERN",
    "ISSUE_ID_LITERAL_PATTERN",
    "format_rfc3339_utc",
    "format_compact_utc_timestamp",
    "derive_run_id",
    "derive_operation_id_from_delivery",
    "derive_operation_id_fallback",
    "derive_retry_operation_id",
    "validate_operation_id",
    "validate_issue_id",
    "canonicalize_json",
    "encode_issue_id",
    "decode_issue_id",
    "derive_source",
]

# operationId is restricted to ASCII letters, digits, hyphen, underscore, and
# colon. ``validate_operation_id`` applies the stricter canonical form checks.
OPERATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9_:-]+$")
_DELIVERY_OPERATION_ID_PATTERN = re.compile(r"^gh-event:[A-Za-z0-9_:-]+$")
_FALLBACK_OPERATION_ID_PATTERN = re.compile(r"^gh-event-fallback:[0-9a-f]{64}$")
_RETRY_OPERATION_ID_PATTERN = re.compile(
    r"^gh-retry:"
    r"(?P<chain_operation_id>(?:gh-event:[A-Za-z0-9_:-]+|gh-event-fallback:[0-9a-f]{64})):"
    r"(?P<retry_decision_time>\d{8}T\d{6}Z):"
    r"(?P<workflow_run_id>[1-9]\d*):"
    r"(?P<workflow_run_attempt>[1-9]\d*)$"
)

# issueId literal (unescaped) characters permitted outside of %HH escape sequences.
ISSUE_ID_LITERAL_PATTERN = re.compile(r"^[A-Za-z0-9._/#:%-]+$")

_REPOSITORY_SLUG_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")

_PERCENT_ENCODE_LITERAL = re.compile(rb"^[A-Za-z0-9._/#:-]$")
_PERCENT_ESCAPE_PATTERN = re.compile(r"%([0-9A-Fa-f]{2})")


def _ensure_utc(dt: datetime) -> datetime:
    """Return *dt* as a timezone-aware UTC datetime.

    Naive datetimes are treated as already being in UTC (the caller's
    responsibility), matching how workflow timestamps are typically produced.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def format_rfc3339_utc(dt: datetime) -> str:
    """Format *dt* as the canonical ``YYYY-MM-DDTHH:mm:ssZ`` RFC3339 UTC form.

    Sub-second precision is dropped; the FR-001/FR-004 contract uses whole-second
    resolution with a literal ``Z`` suffix (no ``+00:00`` offset form).
    """
    utc = _ensure_utc(dt)
    return utc.strftime("%Y-%m-%dT%H:%M:%SZ")


def format_compact_utc_timestamp(dt: datetime) -> str:
    """Format *dt* as the compact ``YYYYMMDDTHHMMSSZ`` retry-decision timestamp.

    This is the 16-character token used inside ``gh-retry:`` operation IDs
    (FR-001); it contains only ASCII digits, ``T``, and ``Z``.
    """
    utc = _ensure_utc(dt)
    return utc.strftime("%Y%m%dT%H%M%SZ")


def derive_run_id(repository: str, workflow_run_id: int, workflow_run_attempt: int) -> str:
    """Derive the canonical ``runId`` for a workflow attempt (FR-001).

    Args:
        repository: The ``<owner>/<repo>`` slug.
        workflow_run_id: The GitHub Actions workflow run ID (positive integer).
        workflow_run_attempt: The GitHub Actions workflow run attempt number
            (positive integer).

    Returns:
        ``gh:<owner>/<repo>:<workflow_run_id>:<workflow_run_attempt>``.

    Raises:
        ValueError: If *repository* is not an ``owner/repo`` slug, or if either
            integer argument is not a positive integer.
    """
    if not isinstance(repository, str) or _REPOSITORY_SLUG_PATTERN.fullmatch(repository) is None:
        raise ValueError(f"Invalid repository slug: {repository!r}")
    if isinstance(workflow_run_id, bool) or not isinstance(workflow_run_id, int) or workflow_run_id <= 0:
        raise ValueError(f"workflow_run_id must be a positive integer, got {workflow_run_id!r}")
    if isinstance(workflow_run_attempt, bool) or not isinstance(workflow_run_attempt, int) or workflow_run_attempt <= 0:
        raise ValueError(f"workflow_run_attempt must be a positive integer, got {workflow_run_attempt!r}")
    return f"gh:{repository}:{workflow_run_id}:{workflow_run_attempt}"


def derive_operation_id_from_delivery(delivery_id: str) -> str:
    """Derive the canonical ``operationId`` for the initial delivery of a provider event.

    Args:
        delivery_id: The GitHub webhook delivery identifier.

    Returns:
        ``gh-event:<delivery_id>``.

    Raises:
        ValueError: If *delivery_id* is empty or contains characters outside the
            permitted ``operationId`` charset.
    """
    if not isinstance(delivery_id, str) or not delivery_id:
        raise ValueError("delivery_id must be a non-empty string")
    operation_id = f"gh-event:{delivery_id}"
    if not validate_operation_id(operation_id):
        raise ValueError(f"delivery_id produces an invalid operationId: {delivery_id!r}")
    return operation_id


def _jcs_float(value: float) -> str:
    """Serialize *value* per RFC 8785 §3.2.2 / ECMAScript §7.1.12.1.

    Uses the shortest round-trip decimal representation with ECMAScript's
    output-format rules: fixed decimal for k ≤ n ≤ 21 and -6 < n ≤ 0,
    exponential notation otherwise.  Negative zero is mapped to ``"0"``.
    """
    # RFC 8785 §3.2.2: both +0.0 and -0.0 serialize as "0".
    if value == 0.0:
        return "0"

    sign = ""
    if value < 0:
        sign = "-"
        value = -value

    # repr() produces the shortest decimal string that round-trips to *value*,
    # which matches ECMAScript's requirement for the shortest representation.
    r = repr(value)

    if "e" in r:
        # Python repr uses exponential form, e.g. "1e+20", "1.5e-07".
        coeff_str, exp_str = r.split("e")
        python_exp = int(exp_str)
        # Strip the decimal point to obtain the coefficient digits.
        s = coeff_str.replace(".", "")
        k = len(s)
        # ECMAScript convention: value = s × 10^(n-k).
        # Python form:           value = (s / 10^(k-1)) × 10^python_exp
        # Therefore: n = python_exp + 1 (independent of k).
        n = python_exp + 1
    else:
        # Python repr uses fixed decimal form, e.g. "1.5", "100.0", "0.001".
        if "." in r:
            int_part, frac_part = r.split(".")
        else:
            int_part, frac_part = r, ""  # pragma: no cover  # Python repr always includes "."
        # Determine n (decimal exponent offset): the number of integer digits,
        # which may be zero or negative for fractions whose integer part is "0".
        if int_part == "0":
            # e.g. "0.001" → 2 leading zeros → n = -2
            leading_zeros = len(frac_part) - len(frac_part.lstrip("0"))
            n = -leading_zeros
        else:
            n = len(int_part)
        # Build the coefficient, stripping trailing and (for <1 numbers) leading zeros.
        s = (int_part + frac_part).rstrip("0").lstrip("0") or "0"

    k = len(s)

    # ECMAScript §7.1.12.1 output-format selection.
    if k <= n <= 21:
        # Append trailing zeros; e.g. 1e20 → "100000000000000000000".
        return sign + s + "0" * (n - k)
    if 0 < n <= 21:
        # Fixed notation with decimal point; e.g. 12.34 → "12.34".
        return sign + s[:n] + "." + s[n:]
    if -6 < n <= 0:
        # Fixed notation with leading zeros; e.g. 1e-6 → "0.000001".
        return sign + "0." + "0" * (-n) + s
    # Exponential notation; e.g. 1e-7 → "1e-7", 1.5e30 → "1.5e+30".
    exp_val = n - 1
    coeff_out = s if k == 1 else s[0] + "." + s[1:]
    exp_sign = "+" if exp_val >= 0 else "-"
    return sign + coeff_out + "e" + exp_sign + str(abs(exp_val))


def canonicalize_json(payload: Any) -> bytes:
    """Serialize *payload* to canonical, deterministic UTF-8 JSON bytes.

    This is an RFC 8785 (JSON Canonicalization Scheme)-compatible helper: object
    member names are sorted (by Unicode code point, matching JCS's UTF-16
    code-unit ordering for the code-point ranges used by this repository's
    identifiers), arrays preserve their original order, and the output contains
    no insignificant whitespace.

    Args:
        payload: A JSON-compatible value: ``None``, ``bool``, ``int``, ``float``,
            ``str``, a ``list``/``tuple`` of JSON-compatible values, or a
            ``dict`` with string keys and JSON-compatible values.

    Returns:
        The canonical UTF-8 encoded JSON byte sequence.

    Raises:
        TypeError: If *payload* (or any nested value) is not JSON-compatible.
    """

    def _validate_utf8_string(value: str, *, context: str) -> str:
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise TypeError(f"canonicalize_json requires UTF-8 encodable {context}") from exc
        return value

    def _validate(value: Any) -> Any:
        if value is None or type(value) in (bool, int):
            return value
        if type(value) is str:
            return _validate_utf8_string(value, context="strings")
        if type(value) is float:
            if not math.isfinite(value):
                raise TypeError("canonicalize_json does not support non-finite floats")
            return value
        if isinstance(value, (list, tuple)):
            return [_validate(item) for item in value]
        if isinstance(value, dict):
            for key in value:
                if not isinstance(key, str):
                    raise TypeError(f"canonicalize_json requires string keys, got {key!r} ({type(key).__name__})")
                _validate_utf8_string(key, context="object member names")
            return {key: _validate(val) for key, val in value.items()}
        raise TypeError(f"canonicalize_json does not support value of type {type(value).__name__}: {value!r}")

    validated = _validate(payload)

    # JCS orders object names by their UTF-16 code units, rather than Python's
    # Unicode code-point ordering for names containing supplementary characters.
    def _canonical(value: Any) -> str:
        if value is None:
            return "null"
        if value is True:
            return "true"
        if value is False:
            return "false"
        if type(value) is int:
            as_float = float(value)
            if int(as_float) != value:
                raise TypeError(
                    "canonicalize_json does not support integers not exactly"
                    f" representable as IEEE-754 double: {value!r}"
                )
            return _jcs_float(as_float)
        if type(value) is float:
            return _jcs_float(value)
        if type(value) is str:
            return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        if isinstance(value, list):
            return "[" + ",".join(_canonical(item) for item in value) + "]"
        if isinstance(value, dict):
            keys = sorted(value, key=lambda key: key.encode("utf-16-be"))
            return "{" + ",".join(f"{_canonical(key)}:{_canonical(value[key])}" for key in keys) + "}"
        raise TypeError(f"canonicalize_json does not support value of type {type(value).__name__}")  # pragma: no cover

    text = _canonical(validated)
    return text.encode("utf-8")


def derive_operation_id_fallback(payload: Any) -> str:
    """Derive the fallback ``operationId`` when no delivery identifier is available.

    Args:
        payload: The JSON-compatible provider event payload (run-specific
            metadata such as ``workflowRunId``, ``workflowRunAttempt``, and
            ``runId`` MUST NOT be included per FR-001).

    Returns:
        ``gh-event-fallback:<sha256_lower_hex>`` where the digest is computed
        over :func:`canonicalize_json` of *payload*.
    """
    digest = hashlib.sha256(canonicalize_json(payload)).hexdigest()
    return f"gh-event-fallback:{digest}"


def derive_retry_operation_id(
    chain_operation_id: str,
    retry_decision_time: datetime,
    workflow_run_id: int,
    workflow_run_attempt: int,
) -> str:
    """Derive the canonical ``operationId`` for an intentional retry (FR-001).

    Args:
        chain_operation_id: The originating (non-retry) operation's ``operationId``.
        retry_decision_time: The UTC time the retry was decided.
        workflow_run_id: The triggering workflow run's ID (positive integer).
        workflow_run_attempt: The triggering workflow run's attempt number
            (positive integer).

    Returns:
        ``gh-retry:<chainOperationId>:<compact_utc_timestamp>:<workflowRunId>:<workflowRunAttempt>``.

    Raises:
        ValueError: If *chain_operation_id* is not a valid operationId, or if
            the integer arguments are not positive integers.
    """
    if not validate_operation_id(chain_operation_id):
        raise ValueError(f"Invalid chain_operation_id: {chain_operation_id!r}")
    if chain_operation_id.startswith("gh-retry:"):
        raise ValueError(
            f"chain_operation_id must be an initial-delivery operationId, not a retry: {chain_operation_id!r}"
        )
    if isinstance(workflow_run_id, bool) or not isinstance(workflow_run_id, int) or workflow_run_id <= 0:
        raise ValueError(f"workflow_run_id must be a positive integer, got {workflow_run_id!r}")
    if isinstance(workflow_run_attempt, bool) or not isinstance(workflow_run_attempt, int) or workflow_run_attempt <= 0:
        raise ValueError(f"workflow_run_attempt must be a positive integer, got {workflow_run_attempt!r}")
    compact_ts = format_compact_utc_timestamp(retry_decision_time)
    return f"gh-retry:{chain_operation_id}:{compact_ts}:{workflow_run_id}:{workflow_run_attempt}"


def _is_compact_utc_timestamp(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y%m%dT%H%M%SZ")
    except ValueError:
        return False
    return True


def validate_operation_id(value: str) -> bool:
    """Return whether *value* is a syntactically valid ``operationId`` (FR-001)."""
    if not isinstance(value, str) or OPERATION_ID_PATTERN.fullmatch(value) is None:
        return False
    if _DELIVERY_OPERATION_ID_PATTERN.fullmatch(value) is not None:
        return True
    if _FALLBACK_OPERATION_ID_PATTERN.fullmatch(value) is not None:
        return True
    retry_match = _RETRY_OPERATION_ID_PATTERN.fullmatch(value)
    if retry_match is None:
        return False
    return _is_compact_utc_timestamp(retry_match.group("retry_decision_time"))


def encode_issue_id(provider_native_reference: str) -> str:
    """Percent-encode a provider-native issue reference into a canonical ``issueId``.

    Any literal ``%`` byte is escaped first as ``%25``; every other byte outside
    the permitted literal set (ASCII letters, digits, ``-``, ``_``, ``.``, ``/``,
    ``#``, ``:``) is escaped as ``%HH`` using uppercase hexadecimal (FR-001).
    The result is reversible via :func:`decode_issue_id`.

    Args:
        provider_native_reference: The canonical provider-native issue reference,
            e.g. ``"owner/repo#123"``, ``"PROJ-123"``, or a repo-relative path.

    Returns:
        The percent-encoded ``issueId``.

    Raises:
        ValueError: If *provider_native_reference* is empty.
    """
    if not isinstance(provider_native_reference, str) or not provider_native_reference:
        raise ValueError("provider_native_reference must be a non-empty string")

    result: list[str] = []
    for byte in provider_native_reference.encode("utf-8"):
        char_bytes = bytes([byte])
        if char_bytes == b"%":
            result.append("%25")
        elif _PERCENT_ENCODE_LITERAL.match(char_bytes):
            result.append(char_bytes.decode("ascii"))
        else:
            result.append(f"%{byte:02X}")
    return "".join(result)


def decode_issue_id(encoded: str) -> str:
    """Reverse :func:`encode_issue_id`, reconstructing the original reference.

    Args:
        encoded: A percent-encoded ``issueId`` value.

    Returns:
        The original provider-native issue reference.
    """

    def _replace(match: re.Match[str]) -> str:
        return chr(int(match.group(1), 16))

    # Percent-decode byte-by-byte through latin-1 round-trip so that multi-byte
    # UTF-8 sequences reassemble correctly before final UTF-8 decoding.
    raw = _PERCENT_ESCAPE_PATTERN.sub(_replace, encoded)
    return raw.encode("latin-1").decode("utf-8")


def validate_issue_id(value: str) -> bool:
    """Return whether *value* is a syntactically valid encoded ``issueId`` (FR-001)."""
    if not isinstance(value, str) or not value:
        return False
    if ISSUE_ID_LITERAL_PATTERN.fullmatch(value) is None:
        return False
    try:
        return encode_issue_id(decode_issue_id(value)) == value
    except UnicodeError:
        return False


def derive_source(
    event_name: str,
    *,
    retry_of_run_id: str | None,
    operation_id: str,
) -> str:
    """Derive the FR-001 ``source`` field using the required first-match precedence.

    Args:
        event_name: The exact ``github.event_name`` value for the invocation.
        retry_of_run_id: The ``retryOfRunId`` value (``None`` for non-retries).
        operation_id: The derived ``operationId`` for this run.

    Returns:
        One of ``"retry"``, ``"manual-dispatch"``, ``"repository-dispatch"``, or
        ``"provider-event"``.
    """
    is_retry_operation = operation_id.startswith("gh-retry:")
    if retry_of_run_id is not None and is_retry_operation:
        return "retry"
    if event_name == "workflow_dispatch" and retry_of_run_id is None:
        return "manual-dispatch"
    if event_name == "repository_dispatch" and retry_of_run_id is None:
        return "repository-dispatch"
    if (
        retry_of_run_id is None
        and (operation_id.startswith("gh-event:") or operation_id.startswith("gh-event-fallback:"))
        and event_name not in ("workflow_dispatch", "repository_dispatch")
    ):
        return "provider-event"
    raise ValueError(
        "Unable to derive source: no precedence rule matched for "
        f"event_name={event_name!r}, retry_of_run_id={retry_of_run_id!r}, operation_id={operation_id!r}"
    )
