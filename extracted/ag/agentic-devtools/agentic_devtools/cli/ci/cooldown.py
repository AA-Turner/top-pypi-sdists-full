"""Durable provider cooldowns shared by the AI PR Loop workflows."""

from __future__ import annotations

import json
import logging
import os
import re
import threading
import time
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from math import isfinite
from typing import TYPE_CHECKING, Any

from agentic_devtools.cli.shared.retry import (
    DEFAULT_RATE_LIMIT_FALLBACK_DELAY,
    DEFAULT_RATE_LIMIT_MAX_DELAY,
    DEFAULT_RATE_LIMIT_SAFETY_MARGIN,
    ProviderRateLimitError,
    RateLimitDelay,
    calculate_rate_limit_delay,
)

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)

COOLDOWN_VARIABLE = "AI_PR_LOOP_PROVIDER_COOLDOWNS"
DEFAULT_PROVIDER = "github"
_SAFE_COMPONENT_RE = re.compile(r"^[A-Za-z0-9_.-]{1,128}$")
_ALLOWED_REASON_VALUES = {"rate_limit"}
_ALLOWED_SOURCE_VALUES = {"retry-after", "x-ratelimit-reset", "fallback"}
_AI_PR_LOOP_CREDENTIAL_IDENTITIES = (
    "COPILOT_GITHUB_TOKEN",
    "SPECKIT_PR_TOKEN",
    "AGDT_PR_APPROVER_PAT",
    "REPO_VARIABLE_WRITER_PAT",
)
_WRITE_LOCK = threading.RLock()


@dataclass(frozen=True)
class CooldownRecord:
    """Validated provider cooldown data safe to serialize to a repository variable."""

    resume_at: float
    reason: str = "rate_limit"
    source: str = "fallback"
    updated_at: float = 0.0

    def as_dict(self) -> dict[str, float | str]:
        return {
            "resume_at": self.resume_at,
            "reason": self.reason,
            "source": self.source,
            "updated_at": self.updated_at,
        }


def credential_identity_from_environment() -> str:
    """Return a safe logical credential identity without inspecting token contents."""
    configured = os.environ.get("AI_PR_LOOP_CREDENTIAL_IDENTITY", "").strip()
    if configured and _SAFE_COMPONENT_RE.fullmatch(configured):
        return configured
    for name in (*_AI_PR_LOOP_CREDENTIAL_IDENTITIES, "GH_TOKEN"):
        if os.environ.get(name, "").strip():
            return name
    return "GH_TOKEN"


def ai_pr_loop_credential_identities() -> tuple[str, ...]:
    """Return the full credential set the AI PR loop may use for provider work."""
    identities: list[str] = []
    configured = os.environ.get("AI_PR_LOOP_CREDENTIAL_IDENTITY", "").strip()
    if configured and _SAFE_COMPONENT_RE.fullmatch(configured):
        identities.append(configured)
    for name in _AI_PR_LOOP_CREDENTIAL_IDENTITIES:
        if name not in identities:
            identities.append(name)
    fallback = credential_identity_from_environment()
    if fallback not in identities:
        identities.append(fallback)
    return tuple(identities)


def _normalize_credential_identities(
    credential_identity: str | Iterable[str] | None,
) -> tuple[str, ...]:
    """Return validated credential identities for cooldown lookup."""
    if credential_identity is None:
        return (credential_identity_from_environment(),)
    candidates: tuple[str, ...]
    if isinstance(credential_identity, str):
        candidates = (credential_identity,)
    elif not isinstance(credential_identity, Iterable):
        return (credential_identity_from_environment(),)
    else:
        candidates = tuple(credential_identity)
    identities: list[str] = []
    for candidate in candidates:
        if not isinstance(candidate, str):
            continue
        normalized = candidate.strip()
        if normalized and _SAFE_COMPONENT_RE.fullmatch(normalized) and normalized not in identities:
            identities.append(normalized)
    return tuple(identities) or (credential_identity_from_environment(),)


def cooldown_key(
    credential_identity: str | None = None,
    *,
    provider: str = DEFAULT_PROVIDER,
) -> str:
    """Build a key from provider and a logical environment-variable identity."""
    identity = (credential_identity or credential_identity_from_environment()).strip()
    if not _SAFE_COMPONENT_RE.fullmatch(identity):
        raise ValueError("credential_identity must be a safe logical identifier")
    provider_name = provider.strip().lower()
    if not _SAFE_COMPONENT_RE.fullmatch(provider_name):
        raise ValueError("provider must be a safe logical identifier")
    return f"{provider_name}:{identity}"


def _as_record(value: Any) -> CooldownRecord | None:
    if not isinstance(value, dict):
        return None
    resume_at = value.get("resume_at")
    updated_at = value.get("updated_at", 0.0)
    if not isinstance(resume_at, (int, float)) or isinstance(resume_at, bool):
        return None
    if not isinstance(updated_at, (int, float)) or isinstance(updated_at, bool):
        return None
    reason = value.get("reason", "rate_limit")
    source = value.get("source", "fallback")
    if not isinstance(reason, str) or not isinstance(source, str):
        return None
    normalized_reason = reason.strip()
    normalized_source = source.strip()
    if normalized_reason not in _ALLOWED_REASON_VALUES or normalized_source not in _ALLOWED_SOURCE_VALUES:
        return None
    if not isfinite(float(resume_at)) or not isfinite(float(updated_at)) or resume_at < 0 or updated_at < 0:
        return None
    return CooldownRecord(float(resume_at), normalized_reason, normalized_source, float(updated_at))


def _is_valid_cooldown_key(key: str) -> bool:
    provider_name, separator, credential_identity = key.partition(":")
    return bool(
        separator
        and key.count(":") == 1
        and _SAFE_COMPONENT_RE.fullmatch(provider_name)
        and _SAFE_COMPONENT_RE.fullmatch(credential_identity)
    )


def parse_cooldowns(raw: str | None, *, now: float | None = None) -> dict[str, CooldownRecord]:
    """Parse and validate cooldown JSON, dropping malformed and expired entries."""
    current = time.time() if now is None else float(now)
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        logger.warning("Ignoring malformed %s repository variable", COOLDOWN_VARIABLE)
        return {}
    records = payload.get("provider_cooldowns") if isinstance(payload, dict) else None
    if not isinstance(records, dict):
        return {}
    result: dict[str, CooldownRecord] = {}
    max_resume_at = current + DEFAULT_RATE_LIMIT_MAX_DELAY
    for key, value in records.items():
        if not isinstance(key, str) or not _is_valid_cooldown_key(key):
            continue
        record = _as_record(value)
        if record is not None and current < record.resume_at <= max_resume_at:
            result[key] = record
    return result


def serialize_cooldowns(records: dict[str, CooldownRecord]) -> str:
    """Serialize validated records using the repository variable schema."""
    return json.dumps(
        {"provider_cooldowns": {key: record.as_dict() for key, record in sorted(records.items())}},
        sort_keys=True,
        separators=(",", ":"),
    )


def merge_cooldown(
    raw: str | None,
    *,
    key: str,
    record: CooldownRecord,
    now: float | None = None,
) -> str:
    """Merge a cooldown without ever shortening an existing active cooldown."""
    records = parse_cooldowns(raw, now=now)
    existing = records.get(key)
    if existing is not None and existing.resume_at >= record.resume_at:
        return serialize_cooldowns(records)
    records[key] = record
    return serialize_cooldowns(records)


def _preserves_cooldown_records(
    expected: dict[str, CooldownRecord],
    actual: dict[str, CooldownRecord],
) -> bool:
    """Return whether a verified write retained every expected active record."""
    return all(
        (observed := actual.get(key)) is not None and observed.resume_at >= record.resume_at
        for key, record in expected.items()
    )


def read_cooldowns(
    provider: CIPlatformProvider,
    *,
    now: float | None = None,
    use_writer_token: bool = False,
) -> dict[str, CooldownRecord]:
    """Read active cooldowns; unavailable state fails open for scheduling."""
    try:
        return parse_cooldowns(provider.get_variable(COOLDOWN_VARIABLE, use_writer_token=use_writer_token), now=now)
    except ProviderRateLimitError as exc:
        if exc.is_rate_limit:
            raise
        logger.warning("Could not read provider cooldowns; continuing fail-open: %s", type(exc).__name__)
        return {}
    except Exception as exc:
        logger.warning("Could not read provider cooldowns; continuing fail-open: %s", type(exc).__name__)
        return {}


def active_cooldown(
    provider: CIPlatformProvider,
    *,
    credential_identity: str | Iterable[str] | None = None,
    provider_name: str = DEFAULT_PROVIDER,
    now: float | None = None,
    use_writer_token: bool = False,
) -> tuple[str, CooldownRecord] | None:
    """Return the longest active cooldown matching one or more provider credentials."""
    records = read_cooldowns(provider, now=now, use_writer_token=use_writer_token)
    active: tuple[str, CooldownRecord] | None = None
    for identity in _normalize_credential_identities(credential_identity):
        key = cooldown_key(identity, provider=provider_name)
        record = records.get(key)
        if record is not None and (active is None or record.resume_at > active[1].resume_at):
            active = (key, record)
    return active


def persist_cooldown(
    provider: CIPlatformProvider,
    error: ProviderRateLimitError,
    *,
    now: float | None = None,
    retries: int = 3,
) -> tuple[str, CooldownRecord] | None:
    """Persist a monotonic provider cooldown using bounded read/merge/write attempts.

    Cross-process safety relies on the read/merge/verify/retry loop: each attempt
    reads the current variable, merges all known records, writes the merged state,
    and verifies that no concurrent writer shortened an active cooldown. The
    in-process ``_WRITE_LOCK`` serializes concurrent callers within the same process.
    """
    current = time.time() if now is None else float(now)
    identity = error.credential_identity or credential_identity_from_environment()
    key = cooldown_key(identity, provider=error.provider or DEFAULT_PROVIDER)
    delay: RateLimitDelay = calculate_rate_limit_delay(
        retry_after_seconds=error.retry_after_seconds,
        reset_timestamp=error.reset_timestamp,
        now=current,
        fallback_delay=DEFAULT_RATE_LIMIT_FALLBACK_DELAY,
        safety_margin=DEFAULT_RATE_LIMIT_SAFETY_MARGIN,
        max_delay=DEFAULT_RATE_LIMIT_MAX_DELAY,
    )
    record = CooldownRecord(
        resume_at=delay.resume_at,
        reason="rate_limit",
        source=error.source if error.source in _ALLOWED_SOURCE_VALUES else delay.source,
        updated_at=current,
    )
    known_records: dict[str, CooldownRecord] = {}
    with _WRITE_LOCK:
        for _ in range(max(1, retries)):
            try:
                raw = provider.get_variable(COOLDOWN_VARIABLE, use_writer_token=True)
                observed_records = parse_cooldowns(raw, now=current)
                for observed_key, observed_record in observed_records.items():
                    known_record = known_records.get(observed_key)
                    if known_record is None or (
                        observed_record.resume_at > known_record.resume_at
                        or (
                            observed_record.resume_at == known_record.resume_at
                            and observed_record.updated_at > known_record.updated_at
                        )
                    ):
                        known_records[observed_key] = observed_record
                records = dict(known_records)
                existing = records.get(key)
                if existing is None or existing.resume_at < record.resume_at:
                    records[key] = record
                merged = serialize_cooldowns(records)
                provider.set_variable(COOLDOWN_VARIABLE, merged)
                verified_raw = provider.get_variable(COOLDOWN_VARIABLE, use_writer_token=True)
                verified_records = parse_cooldowns(verified_raw, now=current)
                effective = verified_records.get(key)
                if not _preserves_cooldown_records(records, verified_records):
                    logger.warning("Provider cooldown write was stale; reconciling records before retrying")
                    continue
                if effective is None:  # pragma: no cover - covered by the preservation check
                    continue
                return key, effective
            except Exception as exc:
                logger.warning("Could not persist provider cooldown; retrying: %s", type(exc).__name__)
                if _ + 1 < max(1, retries):
                    time.sleep(1.0)
    logger.warning("Provider cooldown could not be persisted; keeping rate-limit pause in effect")
    return None


def format_resume_at(timestamp: float) -> str:
    """Format an epoch timestamp as a sanitized UTC value for logs and annotations."""
    return datetime.fromtimestamp(timestamp, UTC).isoformat().replace("+00:00", "Z")


__all__ = [
    "COOLDOWN_VARIABLE",
    "CooldownRecord",
    "active_cooldown",
    "ai_pr_loop_credential_identities",
    "cooldown_key",
    "credential_identity_from_environment",
    "format_resume_at",
    "merge_cooldown",
    "parse_cooldowns",
    "persist_cooldown",
    "read_cooldowns",
    "serialize_cooldowns",
]
