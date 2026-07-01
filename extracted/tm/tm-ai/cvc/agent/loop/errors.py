"""Error classification taxonomy and jittered backoff.

Replaces scattered string-matching with a structured pipeline:
HTTP status + body → Classification → recovery action.
"""
from __future__ import annotations

import random
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any


class FailoverReason(str, Enum):
    AUTH = "auth"
    AUTH_PERMANENT = "auth_permanent"
    BILLING = "billing"
    RATE_LIMIT = "rate_limit"
    OVERLOADED = "overloaded"
    SERVER_ERROR = "server_error"
    TIMEOUT = "timeout"
    CONTEXT_OVERFLOW = "context_overflow"
    PAYLOAD_TOO_LARGE = "payload_too_large"
    IMAGE_TOO_LARGE = "image_too_large"
    MODEL_NOT_FOUND = "model_not_found"
    PROVIDER_POLICY_BLOCKED = "provider_policy_blocked"
    UNKNOWN = "unknown"


class RecoveryAction(str, Enum):
    RETRY = "retry"                     # wait + retry same credential
    ROTATE_CREDENTIAL = "rotate"        # try next pooled credential
    FALLBACK_PROVIDER = "fallback"      # switch provider entirely
    COMPRESS_CONTEXT = "compress"       # shrink prompt
    ABORT = "abort"                     # surface to user


@dataclass
class Classification:
    reason: FailoverReason
    action: RecoveryAction
    status_code: int | None = None
    message: str = ""
    retry_after: float | None = None
    raw: Any = None


_REASON_TO_ACTION = {
    FailoverReason.AUTH: RecoveryAction.ROTATE_CREDENTIAL,
    FailoverReason.AUTH_PERMANENT: RecoveryAction.FALLBACK_PROVIDER,
    FailoverReason.BILLING: RecoveryAction.FALLBACK_PROVIDER,
    FailoverReason.RATE_LIMIT: RecoveryAction.ROTATE_CREDENTIAL,
    FailoverReason.OVERLOADED: RecoveryAction.RETRY,
    FailoverReason.SERVER_ERROR: RecoveryAction.RETRY,
    FailoverReason.TIMEOUT: RecoveryAction.RETRY,
    FailoverReason.CONTEXT_OVERFLOW: RecoveryAction.COMPRESS_CONTEXT,
    FailoverReason.PAYLOAD_TOO_LARGE: RecoveryAction.COMPRESS_CONTEXT,
    FailoverReason.IMAGE_TOO_LARGE: RecoveryAction.ABORT,
    FailoverReason.MODEL_NOT_FOUND: RecoveryAction.FALLBACK_PROVIDER,
    FailoverReason.PROVIDER_POLICY_BLOCKED: RecoveryAction.FALLBACK_PROVIDER,
    FailoverReason.UNKNOWN: RecoveryAction.ABORT,
}


def classify_http(status: int | None, body: str = "", *, exception: BaseException | None = None) -> Classification:
    body_lower = (body or "").lower()
    msg = (body or "")[:500]

    if exception is not None:
        ename = type(exception).__name__.lower()
        if "timeout" in ename:
            return _mk(FailoverReason.TIMEOUT, status, msg)

    if status is None:
        return _mk(FailoverReason.UNKNOWN, status, msg)

    if status == 401:
        if "invalid" in body_lower and "key" in body_lower:
            return _mk(FailoverReason.AUTH_PERMANENT, status, msg)
        return _mk(FailoverReason.AUTH, status, msg)
    if status == 402 or "billing" in body_lower or "insufficient_quota" in body_lower:
        return _mk(FailoverReason.BILLING, status, msg)
    if status == 403:
        if "policy" in body_lower or "blocked" in body_lower or "moderation" in body_lower:
            return _mk(FailoverReason.PROVIDER_POLICY_BLOCKED, status, msg)
        return _mk(FailoverReason.AUTH_PERMANENT, status, msg)
    if status == 404:
        if "model" in body_lower:
            return _mk(FailoverReason.MODEL_NOT_FOUND, status, msg)
        return _mk(FailoverReason.UNKNOWN, status, msg)
    if status == 408 or status == 504:
        return _mk(FailoverReason.TIMEOUT, status, msg)
    if status == 413:
        if "image" in body_lower:
            return _mk(FailoverReason.IMAGE_TOO_LARGE, status, msg)
        return _mk(FailoverReason.PAYLOAD_TOO_LARGE, status, msg)
    if status == 429:
        retry = _parse_retry_after(body_lower)
        c = _mk(FailoverReason.RATE_LIMIT, status, msg)
        c.retry_after = retry
        return c
    if status == 422 and ("context" in body_lower or "too long" in body_lower or "max_tokens" in body_lower):
        return _mk(FailoverReason.CONTEXT_OVERFLOW, status, msg)
    if status in (529,) or "overloaded" in body_lower:
        return _mk(FailoverReason.OVERLOADED, status, msg)
    if 500 <= status < 600:
        return _mk(FailoverReason.SERVER_ERROR, status, msg)
    if status == 400 and "context" in body_lower:
        return _mk(FailoverReason.CONTEXT_OVERFLOW, status, msg)

    return _mk(FailoverReason.UNKNOWN, status, msg)


def _mk(reason: FailoverReason, status: int | None, msg: str) -> Classification:
    return Classification(reason=reason, action=_REASON_TO_ACTION[reason], status_code=status, message=msg)


def _parse_retry_after(body: str) -> float | None:
    import re
    m = re.search(r"retry[\s_-]?after['\":\s]+(\d+(?:\.\d+)?)", body)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    return None


# ─────────────────────────────────────────────────────────
# 2.4 — Jittered backoff
# ─────────────────────────────────────────────────────────

_seed_lock = threading.Lock()
_seed_counter = 0


def _next_seed() -> int:
    global _seed_counter
    with _seed_lock:
        _seed_counter += 1
        return int(time.monotonic_ns()) ^ _seed_counter


def jittered_backoff(
    attempt: int,
    base_delay: float = 5.0,
    max_delay: float = 120.0,
    jitter_ratio: float = 0.5,
) -> float:
    """Compute exponential backoff with bounded random jitter.

    delay = min(max_delay, base_delay * 2**attempt) * uniform(1-j, 1+j)
    """
    attempt = max(0, int(attempt))
    raw = min(max_delay, base_delay * (2 ** attempt))
    rng = random.Random(_next_seed())
    j = max(0.0, min(1.0, jitter_ratio))
    factor = rng.uniform(max(0.0, 1.0 - j), 1.0 + j)
    return max(0.0, min(max_delay, raw * factor))


__all__ = [
    "FailoverReason",
    "RecoveryAction",
    "Classification",
    "classify_http",
    "jittered_backoff",
]
