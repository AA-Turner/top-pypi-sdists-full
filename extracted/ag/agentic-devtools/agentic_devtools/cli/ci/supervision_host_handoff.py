"""Pure validation of authorized local supervision-host admission handoffs."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from types import MappingProxyType

from agentic_devtools._bundled_skills.skills.fingerprint import canonicalize_json
from agentic_devtools.cli.ci.comment_format import normalize_ai_pr_loop_comment

HOST_ROOT_SESSION_ID = "6b1d128d-eef2-4f23-9576-81b56da1c314"
HOST_HANDOFF_MARKER = "<!-- ai-pr-loop-host-handoff:v1 -->"
_MARKER_NAMESPACE = "ai-pr-loop-host-handoff"
_AI_PR_LOOP_LABEL = "🤖 AI PR Loop ·"
_FIELDS = frozenset(
    {
        "repository",
        "target",
        "admission_role",
        "mode",
        "supervisor_run_id",
        "checkpoint",
        "host_root_session",
        "issued_at",
        "expires_at",
        "fingerprint",
    }
)
_EXPECTED_FIELDS = frozenset({"repository", "role", "mode", "supervisor_run_id", "checkpoint"})
_REPOSITORY_PATTERN = re.compile(r"[^/\s]+/[^/\s]+")
_FINGERPRINT_PATTERN = re.compile(r"[0-9a-f]{64}")
_UTC_TIMESTAMP_PATTERN = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.([0-9]+))?Z")
_COMMENT_TIMESTAMP_PATTERN = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})"
)
_MAX_LIFETIME_SECONDS = 55 * 60


class HostHandoffRejectionReason(StrEnum):
    """Distinct fail-closed outcomes for host handoff verification."""

    NO_RECORD = "no_record"
    UNTRUSTED_AUTHOR = "untrusted_author"
    EDITED_COMMENT = "edited_comment"
    MALFORMED_MARKER = "malformed_marker"
    MALFORMED_COMMENT_NODE = "malformed_comment_node"
    MALFORMED_JSON = "malformed_json"
    DUPLICATE_JSON_KEY = "duplicate_json_key"
    UNKNOWN_FIELD = "unknown_field"
    MISSING_FIELD = "missing_field"
    INVALID_FIELD_TYPE = "invalid_field_type"
    NONCANONICAL_JSON = "noncanonical_json"
    TARGET_MISMATCH = "target_mismatch"
    REPOSITORY_MISMATCH = "repository_mismatch"
    ROLE_MISMATCH = "role_mismatch"
    MODE_MISMATCH = "mode_mismatch"
    SUPERVISOR_RUN_MISMATCH = "supervisor_run_mismatch"
    CHECKPOINT_MISMATCH = "checkpoint_mismatch"
    WRONG_HOST_ROOT_SESSION = "wrong_host_root_session"
    INVALID_TIMESTAMP = "invalid_timestamp"
    FUTURE_ISSUED_AT = "future_issued_at"
    STALE_RECORD = "stale_record"
    LIFETIME_EXCEEDED = "lifetime_exceeded"
    FINGERPRINT_MISMATCH = "fingerprint_mismatch"
    MULTIPLE_MATCHING_RECORDS = "multiple_matching_records"


_STRUCTURAL_ORDER = (
    HostHandoffRejectionReason.MALFORMED_MARKER,
    HostHandoffRejectionReason.MALFORMED_COMMENT_NODE,
    HostHandoffRejectionReason.DUPLICATE_JSON_KEY,
    HostHandoffRejectionReason.MALFORMED_JSON,
    HostHandoffRejectionReason.UNKNOWN_FIELD,
    HostHandoffRejectionReason.MISSING_FIELD,
    HostHandoffRejectionReason.INVALID_FIELD_TYPE,
    HostHandoffRejectionReason.NONCANONICAL_JSON,
)
_MISMATCH_ORDER = (
    HostHandoffRejectionReason.REPOSITORY_MISMATCH,
    HostHandoffRejectionReason.TARGET_MISMATCH,
    HostHandoffRejectionReason.ROLE_MISMATCH,
    HostHandoffRejectionReason.MODE_MISMATCH,
    HostHandoffRejectionReason.SUPERVISOR_RUN_MISMATCH,
    HostHandoffRejectionReason.CHECKPOINT_MISMATCH,
)
_VALIDATION_ORDER = (
    HostHandoffRejectionReason.WRONG_HOST_ROOT_SESSION,
    HostHandoffRejectionReason.EDITED_COMMENT,
    HostHandoffRejectionReason.INVALID_TIMESTAMP,
    HostHandoffRejectionReason.FUTURE_ISSUED_AT,
    HostHandoffRejectionReason.STALE_RECORD,
    HostHandoffRejectionReason.LIFETIME_EXCEEDED,
    HostHandoffRejectionReason.FINGERPRINT_MISMATCH,
)


@dataclass(frozen=True)
class VerifyHostHandoffResult:
    """Accepted handoff payload or its deterministic rejection reason."""

    accepted: bool
    reason: HostHandoffRejectionReason | None
    payload: Mapping[str, str] | None


class _HostHandoffVerifier:
    """Validate candidate records after the host boundary has been established."""

    def __init__(self, expected: Mapping[str, str], trusted_authors: set[str], now: tuple[int, str]) -> None:
        self.expected = expected
        self.trusted_authors = trusted_authors
        self.now = now
        self.epoch = datetime(1970, 1, 1, tzinfo=UTC)

    def _parse_timestamp(self, value: str) -> tuple[int, str] | None:
        match = _UTC_TIMESTAMP_PATTERN.fullmatch(value)
        if match is None:
            return None
        try:
            whole_seconds = datetime.strptime(value[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=UTC)
        except ValueError:
            return None
        delta = whole_seconds - self.epoch
        return delta.days * 86400 + delta.seconds, (match.group(1) or "").rstrip("0")

    @staticmethod
    def _valid_comment_timestamp(value: str) -> bool:
        if _COMMENT_TIMESTAMP_PATTERN.fullmatch(value) is None:
            return False
        try:
            parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
        except ValueError:
            return False
        return parsed.tzinfo is not None and parsed.utcoffset() is not None

    @staticmethod
    def _unwrap_body(body: str) -> tuple[str, HostHandoffRejectionReason | None]:
        normalized = normalize_ai_pr_loop_comment(body)
        if normalized is None or normalized == body:
            return "", HostHandoffRejectionReason.MALFORMED_MARKER
        lines = normalized.split("\n")
        if (
            "\r" in normalized
            or len(lines) != 2
            or lines[0] != HOST_HANDOFF_MARKER
            or not body.endswith(f"\n\n{_AI_PR_LOOP_LABEL}")
        ):
            return "", HostHandoffRejectionReason.MALFORMED_MARKER
        return lines[1], None

    def _validate_payload(self, json_text: str, payload: dict[str, object]) -> HostHandoffRejectionReason | None:
        if set(payload) - _FIELDS:
            return HostHandoffRejectionReason.UNKNOWN_FIELD
        if _FIELDS - set(payload):
            return HostHandoffRejectionReason.MISSING_FIELD
        fingerprint = payload["fingerprint"]
        if (
            any(type(value) is not str for value in payload.values())
            or not isinstance(fingerprint, str)
            or _FINGERPRINT_PATTERN.fullmatch(fingerprint) is None
        ):
            return HostHandoffRejectionReason.INVALID_FIELD_TYPE
        try:
            canonical_text = canonicalize_json(payload).decode("utf-8")
        except TypeError, ValueError:
            return HostHandoffRejectionReason.NONCANONICAL_JSON
        return None if json_text == canonical_text else HostHandoffRejectionReason.NONCANONICAL_JSON

    def _parse_payload(
        self,
        json_text: str,
    ) -> tuple[dict[str, str], HostHandoffRejectionReason | None]:
        duplicate_keys: list[str] = []

        def unique_members(pairs: list[tuple[str, object]]) -> dict[str, object]:
            result: dict[str, object] = {}
            for key, value in pairs:
                if key in result:
                    duplicate_keys.append(key)
                result[key] = value
            return result

        try:
            parsed: object = json.loads(json_text, object_pairs_hook=unique_members)
        except json.JSONDecodeError:
            return {}, (
                HostHandoffRejectionReason.DUPLICATE_JSON_KEY
                if duplicate_keys
                else HostHandoffRejectionReason.MALFORMED_JSON
            )
        if duplicate_keys:
            return {}, HostHandoffRejectionReason.DUPLICATE_JSON_KEY
        if not isinstance(parsed, dict):
            return {}, HostHandoffRejectionReason.MALFORMED_JSON
        reason = self._validate_payload(json_text, parsed)
        if reason is not None:
            return {}, reason
        return {key: value for key, value in parsed.items() if isinstance(value, str)}, None

    def _parse_candidate(
        self,
        node: Mapping[str, object],
        body: str,
    ) -> tuple[dict[str, str], bool, HostHandoffRejectionReason | None]:
        json_text, reason = self._unwrap_body(body)
        if reason is not None:
            return {}, False, reason
        last_edited_at = node.get("lastEditedAt")
        if "lastEditedAt" not in node or (
            last_edited_at is not None
            and (not isinstance(last_edited_at, str) or not self._valid_comment_timestamp(last_edited_at))
        ):
            return {}, False, HostHandoffRejectionReason.MALFORMED_COMMENT_NODE
        payload, reason = self._parse_payload(json_text)
        if reason is not None:
            return {}, False, reason
        return payload, last_edited_at is not None, None

    def _context_mismatch(self, payload: Mapping[str, str]) -> HostHandoffRejectionReason | None:
        if (
            _REPOSITORY_PATTERN.fullmatch(payload["repository"]) is None
            or payload["repository"] != self.expected["repository"]
        ):
            return HostHandoffRejectionReason.REPOSITORY_MISMATCH
        if payload["target"] != "admission":
            return HostHandoffRejectionReason.TARGET_MISMATCH
        if payload["admission_role"] != "admission" or payload["admission_role"] != self.expected["role"]:
            return HostHandoffRejectionReason.ROLE_MISMATCH
        if payload["mode"] not in {"drain", "maintain"} or payload["mode"] != self.expected["mode"]:
            return HostHandoffRejectionReason.MODE_MISMATCH
        if payload["supervisor_run_id"] != self.expected["supervisor_run_id"]:
            return HostHandoffRejectionReason.SUPERVISOR_RUN_MISMATCH
        if payload["checkpoint"] != self.expected["checkpoint"]:
            return HostHandoffRejectionReason.CHECKPOINT_MISMATCH
        return None

    def _validate_candidate(
        self,
        payload: Mapping[str, str],
        edited: bool,
    ) -> list[HostHandoffRejectionReason]:
        failures: list[HostHandoffRejectionReason] = []
        if payload["host_root_session"] != HOST_ROOT_SESSION_ID:
            failures.append(HostHandoffRejectionReason.WRONG_HOST_ROOT_SESSION)
        if edited:
            failures.append(HostHandoffRejectionReason.EDITED_COMMENT)
        issued_at = self._parse_timestamp(payload["issued_at"])
        expires_at = self._parse_timestamp(payload["expires_at"])
        if issued_at is None or expires_at is None:
            failures.append(HostHandoffRejectionReason.INVALID_TIMESTAMP)
        else:
            if issued_at > self.now:
                failures.append(HostHandoffRejectionReason.FUTURE_ISSUED_AT)
            if expires_at <= self.now:
                failures.append(HostHandoffRejectionReason.STALE_RECORD)
            if expires_at > (issued_at[0] + _MAX_LIFETIME_SECONDS, issued_at[1]):
                failures.append(HostHandoffRejectionReason.LIFETIME_EXCEEDED)
        unsigned_payload = dict(payload)
        fingerprint = unsigned_payload.pop("fingerprint")
        expected_fingerprint = hashlib.sha256(canonicalize_json(unsigned_payload)).hexdigest()
        if fingerprint != expected_fingerprint:
            failures.append(HostHandoffRejectionReason.FINGERPRINT_MISMATCH)
        return failures

    def _collect_candidates(
        self,
        comments: Sequence[object],
    ) -> tuple[list[tuple[dict[str, str], bool]], list[HostHandoffRejectionReason], bool]:
        candidates: list[tuple[dict[str, str], bool]] = []
        structural_failures: list[HostHandoffRejectionReason] = []
        untrusted_candidate = False
        for raw_node in comments:
            node = raw_node if isinstance(raw_node, Mapping) else {}
            body = node.get("body")
            if not isinstance(body, str) or _MARKER_NAMESPACE not in body:
                continue
            author = node.get("author")
            login = author.get("login") if isinstance(author, Mapping) else None
            if not isinstance(login, str) or not login.strip() or login.casefold() not in self.trusted_authors:
                untrusted_candidate = True
                continue
            candidate, edited, reason = self._parse_candidate(node, body)
            if reason is not None:
                structural_failures.append(reason)
            else:
                candidates.append((candidate, edited))
        return candidates, structural_failures, untrusted_candidate

    def verify(self, comments: Sequence[object]) -> VerifyHostHandoffResult:
        candidates, structural_failures, untrusted_candidate = self._collect_candidates(comments)
        if structural_failures:
            return VerifyHostHandoffResult(False, min(structural_failures, key=_STRUCTURAL_ORDER.index), None)
        if not candidates:
            reason = (
                HostHandoffRejectionReason.UNTRUSTED_AUTHOR
                if untrusted_candidate
                else HostHandoffRejectionReason.NO_RECORD
            )
            return VerifyHostHandoffResult(False, reason, None)

        matching: list[tuple[dict[str, str], bool]] = []
        mismatches: list[HostHandoffRejectionReason] = []
        for payload, edited in candidates:
            mismatch = self._context_mismatch(payload)
            if mismatch is None:
                matching.append((payload, edited))
            else:
                mismatches.append(mismatch)
        if not matching:
            return VerifyHostHandoffResult(False, min(mismatches, key=_MISMATCH_ORDER.index), None)

        validation_failures = [
            reason for payload, edited in matching for reason in self._validate_candidate(payload, edited)
        ]
        if validation_failures:
            return VerifyHostHandoffResult(False, min(validation_failures, key=_VALIDATION_ORDER.index), None)
        if len(matching) != 1:
            return VerifyHostHandoffResult(False, HostHandoffRejectionReason.MULTIPLE_MATCHING_RECORDS, None)
        return VerifyHostHandoffResult(True, None, MappingProxyType(dict(matching[0][0])))


def verify_host_handoff(
    comments: Sequence[object],
    *,
    trusted_logins: Collection[str],
    expected: Mapping[str, str],
    now: datetime,
) -> VerifyHostHandoffResult:
    """Verify one canonical, unedited control-issue handoff from a trusted local host.

    The caller must stop before invoking this verifier in GitHub Actions, where
    control comments are written by the separate bookkeeping-token identity.
    """
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() != timedelta(0):
        raise ValueError("now must be a timezone-aware UTC datetime")
    if (
        not isinstance(expected, Mapping)
        or set(expected) != _EXPECTED_FIELDS
        or any(type(value) is not str for value in expected.values())
    ):
        raise ValueError("expected must contain exactly the five string handoff context fields")
    if isinstance(trusted_logins, (str, bytes)) or not isinstance(trusted_logins, Collection):
        raise ValueError("trusted_logins must be a collection of login strings")

    trusted_authors = {login.casefold() for login in trusted_logins if isinstance(login, str) and login.strip()}
    now_delta = now.astimezone(UTC) - datetime(1970, 1, 1, tzinfo=UTC)
    now_exact = (
        now_delta.days * 86400 + now_delta.seconds,
        f"{now_delta.microseconds:06d}".rstrip("0"),
    )
    verifier = _HostHandoffVerifier(expected, trusted_authors, now_exact)
    return verifier.verify(comments)
