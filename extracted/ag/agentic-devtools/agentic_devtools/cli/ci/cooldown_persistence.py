"""Persistence implementation for durable provider cooldowns."""

from __future__ import annotations

import json
import logging
import time
from typing import TYPE_CHECKING, Any

import agentic_devtools.cli.ci.cooldown as cooldown
from agentic_devtools.cli.ci.cooldown_document import _merge_payloads, _preserves_cooldown_records, _variable_payload
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


def persist_cooldown(
    provider: CIPlatformProvider,
    error: ProviderRateLimitError,
    *,
    now: float | None = None,
    retries: int = 3,
    observed_at: float | None = None,
) -> tuple[str, cooldown.CooldownRecord] | None:
    """Persist a cooldown using current time for validation and observation time for its expiry."""
    current = time.time() if now is None else float(now)
    event_time = current if observed_at is None else float(observed_at)
    identity = error.credential_identity or cooldown.credential_identity_from_environment()
    key = cooldown.cooldown_key(identity, provider=error.provider or cooldown.DEFAULT_PROVIDER)
    delay: RateLimitDelay = calculate_rate_limit_delay(
        retry_after_seconds=error.retry_after_seconds,
        reset_timestamp=error.reset_timestamp,
        now=event_time,
        fallback_delay=DEFAULT_RATE_LIMIT_FALLBACK_DELAY,
        safety_margin=DEFAULT_RATE_LIMIT_SAFETY_MARGIN,
        max_delay=DEFAULT_RATE_LIMIT_MAX_DELAY,
    )
    record = cooldown.CooldownRecord(
        resume_at=delay.resume_at,
        reason="rate_limit",
        source=error.source if error.source in cooldown._ALLOWED_SOURCE_VALUES else delay.source,
        updated_at=event_time,
    )
    known_records: dict[str, cooldown.CooldownRecord] = {}
    known_payload: dict[str, Any] = {}
    with cooldown._WRITE_LOCK:
        for attempt in range(max(1, retries)):
            try:
                raw = provider.get_variable(cooldown.COOLDOWN_VARIABLE, use_writer_token=True)
                known_payload = _merge_payloads(known_payload, _variable_payload(raw))
                observed_records = cooldown.parse_cooldowns(raw, now=current)
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
                merged = cooldown.serialize_cooldowns(records, raw=json.dumps(known_payload), now=current)
                provider.set_variable(cooldown.COOLDOWN_VARIABLE, merged)
                verified_raw = provider.get_variable(cooldown.COOLDOWN_VARIABLE, use_writer_token=True)
                verified_payload = _variable_payload(verified_raw)
                expected_payload = _variable_payload(merged)
                known_payload = _merge_payloads(known_payload, verified_payload)
                verified_records = cooldown.parse_cooldowns(verified_raw, now=current)
                effective = verified_records.get(key)
                expected_records = {item_key: item for item_key, item in records.items() if item.resume_at > current}
                if (
                    not _preserves_cooldown_records(expected_records, verified_records)
                    or _merge_payloads(expected_payload, verified_payload) != verified_payload
                ):
                    logger.warning("Provider cooldown write was stale; reconciling records before retrying")
                    continue
                if effective is None:
                    return None
                return key, effective
            except Exception as exc:
                logger.warning("Could not persist provider cooldown; retrying: %s", type(exc).__name__)
                if attempt + 1 < max(1, retries):
                    time.sleep(1.0)
    logger.warning("Provider cooldown could not be persisted; keeping rate-limit pause in effect")
    return None
