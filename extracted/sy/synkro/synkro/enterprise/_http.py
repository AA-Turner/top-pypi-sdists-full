"""HTTP client wrappers with retry logic and error mapping."""

from __future__ import annotations

import time

import httpx

import synkro
from synkro.enterprise.errors import (
    SynkroAPIError,
    SynkroAuthError,
    SynkroNotFoundError,
    SynkroRateLimitError,
)

MAX_RETRIES = 3
INITIAL_BACKOFF = 1.0
RETRYABLE_STATUS_CODES = {429, 502, 503, 504}


def _raise_for_status(resp: httpx.Response) -> None:
    """Map HTTP status codes to SDK error classes."""
    if resp.is_success:
        return

    if resp.status_code == 401:
        raise SynkroAuthError("Invalid or expired API key")

    if resp.status_code == 404:
        raise SynkroNotFoundError("Resource not found")

    if resp.status_code == 429:
        raise SynkroRateLimitError(
            "Rate limit exceeded",
            retry_after=resp.headers.get("Retry-After"),
        )

    detail = resp.text
    try:
        body = resp.json()
        if isinstance(body, dict) and "error" in body:
            detail = body["error"]
    except Exception:
        pass

    raise SynkroAPIError(f"{resp.status_code}: {detail}", status_code=resp.status_code)


def _default_headers(api_key: str) -> dict[str, str]:
    return {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "User-Agent": f"synkro-python/{synkro.__version__}",
    }


class BaseHTTPClient:
    """Synchronous HTTP client with retries."""

    def __init__(self, base_url: str, api_key: str, timeout: float = 30.0):
        self._client = httpx.Client(
            base_url=base_url,
            headers=_default_headers(api_key),
            timeout=timeout,
        )

    def get(self, path: str, params: dict | None = None) -> dict:
        return self._request("GET", path, params=params)

    def post(self, path: str, json: dict | None = None) -> dict:
        return self._request("POST", path, json=json)

    def patch(self, path: str, json: dict) -> dict:
        return self._request("PATCH", path, json=json)

    def delete(self, path: str, params: dict | None = None) -> dict:
        return self._request("DELETE", path, params=params)

    def _request(self, method: str, path: str, **kwargs) -> dict:
        backoff = INITIAL_BACKOFF
        last_exc: Exception | None = None

        for attempt in range(MAX_RETRIES + 1):
            resp = self._client.request(method, path, **kwargs)

            if resp.status_code not in RETRYABLE_STATUS_CODES:
                _raise_for_status(resp)
                return resp.json()

            last_exc = SynkroRateLimitError(
                f"Retry {attempt + 1}/{MAX_RETRIES + 1}: {resp.status_code}",
                retry_after=resp.headers.get("Retry-After"),
            )

            if attempt < MAX_RETRIES:
                time.sleep(backoff)
                backoff *= 2

        raise last_exc  # type: ignore[misc]

    def close(self) -> None:
        self._client.close()


class AsyncBaseHTTPClient:
    """Asynchronous HTTP client with retries."""

    def __init__(self, base_url: str, api_key: str, timeout: float = 30.0):
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers=_default_headers(api_key),
            timeout=timeout,
        )

    async def get(self, path: str, params: dict | None = None) -> dict:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, json: dict | None = None) -> dict:
        return await self._request("POST", path, json=json)

    async def patch(self, path: str, json: dict) -> dict:
        return await self._request("PATCH", path, json=json)

    async def delete(self, path: str, params: dict | None = None) -> dict:
        return await self._request("DELETE", path, params=params)

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        import asyncio

        backoff = INITIAL_BACKOFF
        last_exc: Exception | None = None

        for attempt in range(MAX_RETRIES + 1):
            resp = await self._client.request(method, path, **kwargs)

            if resp.status_code not in RETRYABLE_STATUS_CODES:
                _raise_for_status(resp)
                return resp.json()

            last_exc = SynkroRateLimitError(
                f"Retry {attempt + 1}/{MAX_RETRIES + 1}: {resp.status_code}",
                retry_after=resp.headers.get("Retry-After"),
            )

            if attempt < MAX_RETRIES:
                await asyncio.sleep(backoff)
                backoff *= 2

        raise last_exc  # type: ignore[misc]

    async def close(self) -> None:
        await self._client.aclose()
