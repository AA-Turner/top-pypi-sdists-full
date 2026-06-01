"""Process-wide cache for delegated bucket credentials.

When users pickle an icechunk Session and ship it to many workers, every
unpickled task can independently call the arraylake server for fresh
credentials when the embedded ones expire. This module gives the client a
single per-process cache so all consumers in a worker process share one
in-flight refresh.

Validity follows ``Cache-Control: max-age`` semantics: cached creds are
served while ``expires_at - CLOCK_SKEW_SAFETY > now``. The 30s safety only
protects against worker/server NTP-level clock drift; it is not a
pre-refresh window.

The cache is loop-agnostic: callers may live on any asyncio event loop in
the process. In-flight refreshes are coalesced via the singleflight
pattern using a single ``concurrent.futures.Future`` per key as the shared
result channel; each waiter bridges into its own loop via
``asyncio.wrap_future``. The race for who runs the fetcher is resolved by
``dict.setdefault``, which is atomic under the CPython GIL.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Literal

from arraylake.log_util import get_logger
from arraylake.types import OrgName, Platform, TempCredentials

logger = get_logger(__name__)


CLOCK_SKEW_SAFETY = timedelta(seconds=30)


@dataclass(eq=True, frozen=True)
class CredentialCacheKey:
    api_url: str
    auth_key: int
    scope: Literal["repo", "bucket"]
    org: OrgName
    identifier: str
    platform: Platform
    access: Literal["read", "write"] = "read"


@dataclass
class _Entry:
    creds: TempCredentials
    expires_at: datetime | None


_CACHE: dict[CredentialCacheKey, _Entry] = {}
_INFLIGHT: dict[CredentialCacheKey, concurrent.futures.Future[TempCredentials]] = {}


def _fresh(entry: _Entry | None, now: datetime) -> TempCredentials | None:
    if entry is None or entry.expires_at is None:
        return None
    if entry.expires_at - CLOCK_SKEW_SAFETY > now:
        return entry.creds
    return None


async def get_or_refresh(
    key: CredentialCacheKey,
    fetcher: Callable[[], Awaitable[TempCredentials]],
    *,
    use_cache: bool = True,
) -> TempCredentials:
    if not use_cache:
        return await fetcher()

    cached = _fresh(_CACHE.get(key), datetime.now(UTC))
    if cached is not None:
        return cached

    my_future: concurrent.futures.Future[TempCredentials] = concurrent.futures.Future()
    existing = _INFLIGHT.setdefault(key, my_future)
    if existing is not my_future:
        return await asyncio.wrap_future(existing)

    try:
        cached = _fresh(_CACHE.get(key), datetime.now(UTC))
        if cached is not None:
            my_future.set_result(cached)
            return cached

        creds = await fetcher()
        exp = creds.expiration
        if exp is not None and exp.tzinfo is None:
            exp = exp.replace(tzinfo=UTC)
        now = datetime.now(UTC)
        if exp is not None and exp - CLOCK_SKEW_SAFETY <= now:
            logger.warning(
                "delegated credentials returned with lifetime <= clock-skew safety; server contract violation",
                remaining_seconds=(exp - now).total_seconds(),
                api_url=key.api_url,
                org=key.org,
                identifier=key.identifier,
            )
        _CACHE[key] = _Entry(creds=creds, expires_at=exp)
        my_future.set_result(creds)
        return creds
    except BaseException as e:
        my_future.set_exception(e)
        raise
    finally:
        _INFLIGHT.pop(key, None)


def clear() -> None:
    _CACHE.clear()
    _INFLIGHT.clear()
