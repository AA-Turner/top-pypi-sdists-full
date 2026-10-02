"""Authentication helpers: access key exchange and auto-refreshing token providers.

Token providers use the Borg pattern — all instances sharing the same
(base_url, access_key) pair share a single cached token, so multiple
``Islo()`` clients with the same API key never trigger duplicate exchanges.
"""

from __future__ import annotations

import asyncio
import threading
import time
import typing

import httpx


def exchange_access_key(
    base_url: str,
    access_key: str,
    *,
    timeout: float = 10.0,
) -> dict[str, typing.Any]:
    """Exchange an Islo API key for a short-lived JWT.

    Returns the JSON response containing ``session_jwt``, ``refresh_jwt``,
    ``cookie_domain``, ``cookie_path``, ``cookie_max_age``, and ``cookie_expiration``.
    """
    response = httpx.post(
        f"{base_url}/auth/token",
        json={"access_key": access_key},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    if "session_token" not in data:
        raise KeyError(f"Expected 'session_token' in exchange response, got keys: {list(data.keys())}")
    return data


class _SyncTokenState:
    """Shared mutable state for a single (base_url, access_key) pair."""

    __slots__ = ("token", "expires_at", "lock")

    def __init__(self):
        self.token: str | None = None
        self.expires_at: float = 0.0
        self.lock = threading.Lock()


class SyncTokenProvider:
    """Callable token provider with proactive refresh for synchronous clients.

    Uses the Borg pattern: all instances with the same ``(base_url, access_key)``
    share cached token state, avoiding duplicate exchanges.

    Usage::

        client = Islo(api_key="ak_...")  # provider created automatically
    """

    _shared: typing.ClassVar[dict[tuple[str, str], _SyncTokenState]] = {}

    def __init__(
        self,
        base_url: str,
        access_key: str,
        *,
        refresh_margin_sec: float = 60.0,
    ):
        self._base_url = base_url
        self._access_key = access_key
        self._refresh_margin = refresh_margin_sec
        key = (base_url, access_key)
        if key not in self._shared:
            self._shared[key] = _SyncTokenState()
        self._state = self._shared[key]

    def __call__(self) -> str:
        s = self._state
        if s.token and time.monotonic() < s.expires_at:
            return s.token

        with s.lock:
            if s.token and time.monotonic() < s.expires_at:
                return s.token
            return self._refresh()

    def _refresh(self) -> str:
        data = exchange_access_key(self._base_url, self._access_key)
        s = self._state
        s.token = data["session_token"]
        s.expires_at = time.monotonic() + self._token_ttl(data)
        return s.token

    def _token_ttl(self, data: dict) -> float:
        max_age = data.get("cookie_max_age", 600)
        return max(max_age - self._refresh_margin, 0)


class _AsyncTokenState:
    """Shared mutable state for async providers."""

    __slots__ = ("token", "expires_at", "lock")

    def __init__(self):
        self.token: str | None = None
        self.expires_at: float = 0.0
        self.lock = asyncio.Lock()


class AsyncTokenProvider:
    """Callable token provider with proactive refresh for async clients.

    Uses the Borg pattern: all instances with the same ``(base_url, access_key)``
    share cached token state, avoiding duplicate exchanges.

    Usage::

        client = AsyncIslo(api_key="ak_...")  # provider created automatically
    """

    _shared: typing.ClassVar[dict[tuple[str, str], _AsyncTokenState]] = {}

    def __init__(
        self,
        base_url: str,
        access_key: str,
        *,
        refresh_margin_sec: float = 60.0,
    ):
        self._base_url = base_url
        self._access_key = access_key
        self._refresh_margin = refresh_margin_sec
        key = (base_url, access_key)
        if key not in self._shared:
            self._shared[key] = _AsyncTokenState()
        self._state = self._shared[key]

    async def __call__(self) -> str:
        s = self._state
        if s.token and time.monotonic() < s.expires_at:
            return s.token

        async with s.lock:
            if s.token and time.monotonic() < s.expires_at:
                return s.token
            return await self._refresh()

    async def _refresh(self) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/auth/token",
                json={"access_key": self._access_key},
                timeout=10.0,
            )
        response.raise_for_status()
        data = response.json()
        s = self._state
        s.token = data["session_token"]
        max_age = data.get("cookie_max_age", 600)
        s.expires_at = time.monotonic() + max(max_age - self._refresh_margin, 0)
        return s.token
