"""Versioned reconciliation claims, not authentication or a merge authorization.

All identities, digests, inventories, and verdicts here are unverified payload
data. Provider verification, original-criteria digest verification, live-head
binding, and every independent pipeline gate remain the caller's responsibility.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
import re
from dataclasses import asdict, dataclass, fields
from typing import Any, Literal

__all__ = [
    "ReconciliationAttestation",
    "ReconciliationCriterionVerdict",
    "ReconciliationFileVerdict",
    "ReconciliationValidationError",
    "validate_reconciliation_attestation",
    "encode_reconciliation_review_body",
    "decode_reconciliation_review_body",
]

_LOGIN = r"[a-z0-9](?:[a-z0-9]|-(?=[a-z0-9])){0,38}"
_CRITERIA_SOURCE = "https://github.com/swai-factory/agentic-devtools/issues/4299#acceptance-and-safety-tests"
_CRITERION_IDS = ("AC1", "AC2", "AC3", "AC4", "AC5", "AC6", "AC7")
_MAX_BODY_LENGTH = 58_000
_FOOTER = "<!-- /agdt-reconciliation -->"
_Verdict = Literal["accepted", "rejected", "unresolved"]


@dataclass(frozen=True)
class ReconciliationFileVerdict:
    """Claim about raw file bytes and intended behavior at the reviewed head."""

    path: str
    content_sha256: str
    verdict: _Verdict
    behavior: str


@dataclass(frozen=True)
class ReconciliationCriterionVerdict:
    """Claim about one original parent acceptance criterion."""

    criterion_id: str
    verdict: _Verdict
    rationale: str


@dataclass(frozen=True)
class ReconciliationAttestation:
    """Immutable schema-v1 claims with separate repair-output and reviewed heads."""

    schema_version: int
    repository: str
    pr_number: int
    pre_repair_sha: str
    pinned_base_sha: str
    repair_output_sha: str
    reviewed_head_sha: str
    changed_files: tuple[str, ...]
    file_verdicts: tuple[ReconciliationFileVerdict, ...]
    criteria_source: str
    criteria_source_sha256: str
    criterion_verdicts: tuple[ReconciliationCriterionVerdict, ...]
    provider_evidence_ref: str
    configured_approver_login: str
    reviewer_login: str
    repair_writer_login: str


class ReconciliationValidationError(ValueError):
    """Contract failure with a stable machine-readable reason."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


def _require_pattern(value: str, pattern: str, reason: str) -> None:
    """Require a string matching the entire ASCII contract pattern."""
    if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
        raise ReconciliationValidationError(reason)


def _validate_path(path: str) -> None:
    """Validate a repository-relative Git path without normalization."""
    if (
        not isinstance(path, str)
        or not path
        or path.startswith("/")
        or re.match(r"[A-Za-z]:/", path) is not None
        or "\\" in path
        or "\0" in path
        or any(segment in ("", ".", "..") for segment in path.split("/"))
    ):
        raise ReconciliationValidationError("invalid_file_path")


def validate_reconciliation_attestation(attestation: ReconciliationAttestation) -> None:
    """Validate payload structure and consistency only; never authorize a repair."""
    if type(attestation) is not ReconciliationAttestation:
        raise ReconciliationValidationError("invalid_record_type")
    if type(attestation.schema_version) is not int or attestation.schema_version != 1:
        raise ReconciliationValidationError("unsupported_schema_version")
    _require_pattern(attestation.repository, rf"{_LOGIN}/[a-z0-9._-]{{1,100}}", "invalid_repository")
    if type(attestation.pr_number) is not int or attestation.pr_number <= 0:
        raise ReconciliationValidationError("invalid_pr_number")
    for sha in (
        attestation.pre_repair_sha,
        attestation.pinned_base_sha,
        attestation.repair_output_sha,
        attestation.reviewed_head_sha,
    ):
        _require_pattern(sha, r"[0-9a-f]{40}", "invalid_commit_sha")
    _require_pattern(attestation.criteria_source_sha256, r"[0-9a-f]{64}", "invalid_sha256")
    if attestation.criteria_source != _CRITERIA_SOURCE:
        raise ReconciliationValidationError("criterion_coverage_mismatch")
    _validate_identities(attestation)
    for collection in (attestation.changed_files, attestation.file_verdicts, attestation.criterion_verdicts):
        if type(collection) is not tuple:
            raise ReconciliationValidationError("invalid_collection_type")
    _validate_files(attestation)
    _validate_criteria(attestation.criterion_verdicts)


def _validate_identities(attestation: ReconciliationAttestation) -> None:
    """Check claimed login and locator consistency, not provider identity."""
    for login in (
        attestation.configured_approver_login,
        attestation.reviewer_login,
        attestation.repair_writer_login,
    ):
        _require_pattern(login, _LOGIN, "invalid_login")
    if attestation.reviewer_login != attestation.configured_approver_login:
        raise ReconciliationValidationError("reviewer_not_configured_approver")
    if attestation.reviewer_login == attestation.repair_writer_login:
        raise ReconciliationValidationError("reviewer_is_repair_writer")
    expected_ref = f"github://{attestation.repository}/pull/{attestation.pr_number}/reviews"
    if attestation.provider_evidence_ref != expected_ref:
        raise ReconciliationValidationError("invalid_provider_evidence_ref")


def _require_inventory(values: tuple[str, ...], duplicate_reason: str) -> None:
    """Require unique identifiers in lexicographic order."""
    if len(set(values)) != len(values):
        raise ReconciliationValidationError(duplicate_reason)
    if tuple(sorted(values)) != values:
        raise ReconciliationValidationError("noncanonical_order")


def _validate_files(attestation: ReconciliationAttestation) -> None:
    """Require exact, accepted, behavior-described coverage of the claimed inventory."""
    if not attestation.changed_files:
        raise ReconciliationValidationError("file_inventory_empty")
    for path in attestation.changed_files:
        _validate_path(path)
    _require_inventory(attestation.changed_files, "duplicate_file")
    for file_record in attestation.file_verdicts:
        _validate_file_record(file_record)
    file_paths = tuple(record.path for record in attestation.file_verdicts)
    _require_inventory(file_paths, "duplicate_file")
    if file_paths != attestation.changed_files:
        raise ReconciliationValidationError("file_verdict_coverage_mismatch")


def _validate_file_record(file_record: ReconciliationFileVerdict) -> None:
    """Require a structurally valid accepted file claim."""
    if type(file_record) is not ReconciliationFileVerdict:
        raise ReconciliationValidationError("invalid_record_type")
    _validate_path(file_record.path)
    _require_pattern(file_record.content_sha256, r"[0-9a-f]{64}", "invalid_sha256")
    if file_record.verdict not in ("accepted", "rejected", "unresolved"):
        raise ReconciliationValidationError("invalid_file_verdict")
    if file_record.verdict != "accepted":
        raise ReconciliationValidationError(f"file_verdict_{file_record.verdict}")
    if not isinstance(file_record.behavior, str) or not file_record.behavior.strip():
        raise ReconciliationValidationError("empty_file_behavior")


def _validate_criteria(records: tuple[ReconciliationCriterionVerdict, ...]) -> None:
    """Require accepted claims covering all seven original criterion IDs."""
    for criterion_record in records:
        if type(criterion_record) is not ReconciliationCriterionVerdict:
            raise ReconciliationValidationError("invalid_record_type")
        if criterion_record.criterion_id not in _CRITERION_IDS:
            raise ReconciliationValidationError("criterion_coverage_mismatch")
        if criterion_record.verdict not in ("accepted", "rejected", "unresolved"):
            raise ReconciliationValidationError("invalid_criterion_verdict")
        if criterion_record.verdict != "accepted":
            raise ReconciliationValidationError(f"criterion_verdict_{criterion_record.verdict}")
        if not isinstance(criterion_record.rationale, str) or not criterion_record.rationale.strip():
            raise ReconciliationValidationError("empty_criterion_rationale")
    criterion_ids = tuple(record.criterion_id for record in records)
    _require_inventory(criterion_ids, "duplicate_criterion")
    if criterion_ids != _CRITERION_IDS:
        raise ReconciliationValidationError("criterion_coverage_mismatch")


def _canonical_json(payload: Any) -> bytes:
    """Serialize canonical ASCII JSON as UTF-8 bytes."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode(
        "utf-8"
    )


def encode_reconciliation_review_body(attestation: ReconciliationAttestation) -> str:
    """Encode a complete claim, enforcing the envelope size before field validation."""
    if type(attestation) is not ReconciliationAttestation:
        raise ReconciliationValidationError("invalid_record_type")
    try:
        payload = _canonical_json(asdict(attestation))
    except TypeError, ValueError, RecursionError:
        # Non-JSON caller values have no encodable body to size. Validation
        # supplies their precise reason without coercing the original records.
        validate_reconciliation_attestation(attestation)
        raise ReconciliationValidationError("invalid_record_type") from None
    encoded = base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")
    digest = hashlib.sha256(payload).hexdigest()
    body = f"<!-- agdt-reconciliation:v1 sha256={digest} -->\n{encoded}\n{_FOOTER}"
    if len(body) > _MAX_BODY_LENGTH:
        raise ReconciliationValidationError("review_body_too_large")
    validate_reconciliation_attestation(attestation)
    return body


def _json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate keys at every JSON object depth."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReconciliationValidationError("invalid_json")
        result[key] = value
    return result


def _record_from_json[Record: ReconciliationAttestation | ReconciliationFileVerdict | ReconciliationCriterionVerdict](
    record_type: type[Record], payload: Any
) -> Record:
    """Require the exact key set before constructing a frozen record."""
    if type(payload) is not dict:
        raise ReconciliationValidationError("invalid_record_type")
    expected = {field.name for field in fields(record_type)}
    if payload.keys() - expected:
        raise ReconciliationValidationError("unknown_field")
    if expected - payload.keys():
        raise ReconciliationValidationError("missing_field")
    return record_type(**payload)


def _decode_base64url(encoded: str) -> bytes:
    """Decode strictly unpadded, canonical RFC 4648 URL-safe Base64."""
    if re.fullmatch(r"[A-Za-z0-9_-]+", encoded) is None:
        raise ReconciliationValidationError("invalid_base64url")
    try:
        payload = base64.b64decode(encoded + "=" * (-len(encoded) % 4), altchars=b"-_", validate=True)
    except binascii.Error as exc:
        raise ReconciliationValidationError("invalid_base64url") from exc
    if base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=") != encoded:
        raise ReconciliationValidationError("invalid_base64url")
    return payload


def decode_reconciliation_review_body(body: str) -> ReconciliationAttestation:
    """Decode only one exact canonical block; do not authenticate its claims."""
    if not isinstance(body, str):
        raise ReconciliationValidationError("malformed_metadata")
    if len(body) > _MAX_BODY_LENGTH:
        raise ReconciliationValidationError("review_body_too_large")
    lines = body.split("\n")
    if len(lines) != 3:
        raise ReconciliationValidationError("malformed_metadata")
    header = re.fullmatch(r"<!-- agdt-reconciliation:v1 sha256=([0-9a-f]{64}) -->", lines[0])
    if header is None or lines[2] != _FOOTER:
        raise ReconciliationValidationError("malformed_metadata")
    payload = _decode_base64url(lines[1])
    if hashlib.sha256(payload).hexdigest() != header[1]:
        raise ReconciliationValidationError("payload_digest_mismatch")
    try:
        data = json.loads(payload.decode("utf-8"), object_pairs_hook=_json_object)
        canonical = _canonical_json(data)
    except (ValueError, RecursionError) as exc:
        raise ReconciliationValidationError("invalid_json") from exc
    if canonical != payload:
        raise ReconciliationValidationError("noncanonical_payload")
    _record_from_json(ReconciliationAttestation, data)
    record_types: tuple[
        tuple[str, type[ReconciliationFileVerdict] | type[ReconciliationCriterionVerdict] | None], ...
    ] = (
        ("changed_files", None),
        ("file_verdicts", ReconciliationFileVerdict),
        ("criterion_verdicts", ReconciliationCriterionVerdict),
    )
    for key, record_type in record_types:
        collection = data[key]
        if type(collection) is not list:
            raise ReconciliationValidationError("invalid_collection_type")
        data[key] = tuple(
            _record_from_json(record_type, record) if record_type is not None else record for record in collection
        )
    attestation = _record_from_json(ReconciliationAttestation, data)
    validate_reconciliation_attestation(attestation)
    return attestation
