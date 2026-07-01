"""Pool-aware retry wrapper.

Wraps any callable that performs a provider API request so that:
  - 429 / quota-exhausted → mark current credential exhausted, rotate to next
  - 401 / token-expired   → refresh OAuth token (if refresh hook provided), retry
  - 5xx / transient       → exponential backoff retry (max N)

Usage:
    from cvc.agent.pool_retry import call_with_pool_retry
    result = call_with_pool_retry(
        provider="copilot",
        api_call=lambda cred: do_request(cred.runtime_api_key),
        max_attempts=4,
    )
"""
from __future__ import annotations

import logging
import random
import time
from typing import Any, Callable, Optional

from cvc.agent.credential_pool import CredentialPool, PooledCredential, get_pool

logger = logging.getLogger(__name__)


# ── Error classification ──────────────────────────────────────────────

class RateLimitError(Exception):
    """Raised when provider returns 429 or quota-exhausted."""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after


class TokenExpiredError(Exception):
    """Raised when provider returns 401 unauthorized (token expired)."""


class TransientError(Exception):
    """Raised on 5xx server errors — retry with backoff."""


def classify_http_error(status_code: int, body: str = "") -> Optional[Exception]:
    """Map an HTTP status code to one of the typed errors above."""
    if status_code == 429:
        return RateLimitError(f"Rate limited: {body[:200]}")
    if status_code == 401:
        return TokenExpiredError(f"Token expired: {body[:200]}")
    if status_code == 403 and "quota" in body.lower():
        return RateLimitError(f"Quota exhausted: {body[:200]}")
    if 500 <= status_code < 600:
        return TransientError(f"Server error {status_code}: {body[:200]}")
    return None


# ── Main retry driver ────────────────────────────────────────────────

def call_with_pool_retry(
    *,
    provider: str,
    api_call: Callable[[PooledCredential], Any],
    refresh_token: Optional[Callable[[PooledCredential], PooledCredential]] = None,
    max_attempts: int = 4,
    backoff_base: float = 1.0,
    pool: Optional[CredentialPool] = None,
) -> Any:
    """Execute api_call with pool-aware retry semantics.

    Args:
        provider: provider name (e.g. "copilot", "anthropic")
        api_call: callable(credential) → result. Must raise RateLimitError /
                  TokenExpiredError / TransientError on failure.
        refresh_token: optional callable to refresh an OAuth token in-place.
                       Must return the (possibly mutated) credential.
        max_attempts: total attempts across all credentials in the pool.
        backoff_base: starting backoff in seconds (doubles each retry).
        pool: optional CredentialPool instance (defaults to global).

    Returns:
        Whatever api_call returns on success.

    Raises:
        RuntimeError if all credentials are exhausted or max_attempts hit.
    """
    p = pool or get_pool()
    last_error: Optional[Exception] = None
    tried_credential_ids: set[str] = set()

    for attempt in range(max_attempts):
        cred = p.select(provider)
        if not cred:
            # Try to fall back to env-only (no pool entry)
            if attempt == 0:
                last_error = RuntimeError(f"No available credentials for provider '{provider}'")
            break

        if cred.id in tried_credential_ids and last_error and not isinstance(last_error, TransientError):
            # We've cycled back — pool is exhausted
            break
        tried_credential_ids.add(cred.id)

        try:
            result = api_call(cred)
            p.mark_used(cred)
            return result

        except RateLimitError as e:
            last_error = e
            logger.warning("[%s] credential %s rate-limited; rotating", provider, cred.id)
            p.mark_exhausted(cred, error_code=429,
                             reset_at=(time.time() + e.retry_after) if e.retry_after else None)
            continue  # try next credential

        except TokenExpiredError as e:
            last_error = e
            if refresh_token:
                logger.info("[%s] credential %s token expired; refreshing", provider, cred.id)
                try:
                    cred = refresh_token(cred)
                    p.update(cred)
                    # Retry same credential immediately with refreshed token
                    result = api_call(cred)
                    p.mark_used(cred)
                    return result
                except Exception as refresh_exc:
                    logger.error("[%s] refresh failed: %s; rotating", provider, refresh_exc)
                    p.mark_exhausted(cred, error_code=401, reset_at=time.time() + 3600)
                    continue
            else:
                p.mark_exhausted(cred, error_code=401, reset_at=time.time() + 3600)
                continue

        except TransientError as e:
            last_error = e
            sleep = backoff_base * (2 ** attempt) + random.uniform(0, 0.5)
            logger.warning("[%s] transient error: %s; retrying in %.1fs", provider, e, sleep)
            time.sleep(sleep)
            continue

        except Exception:
            # Unknown error — don't retry, propagate
            raise

    raise RuntimeError(
        f"Pool retry exhausted for provider '{provider}' after {max_attempts} attempts. "
        f"Last error: {last_error}"
    )


__all__ = [
    "RateLimitError",
    "TokenExpiredError",
    "TransientError",
    "classify_http_error",
    "call_with_pool_retry",
]
