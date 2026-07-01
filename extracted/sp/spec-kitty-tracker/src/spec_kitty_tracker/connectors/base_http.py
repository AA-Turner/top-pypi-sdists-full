from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from spec_kitty_tracker.errors import ConnectorRequestError, classify_http_status


def _parse_retry_after_seconds(value: str | None) -> int | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    if text.isdigit():
        return int(text)
    return None


class HTTPConnectorBase:
    def __init__(
        self,
        *,
        base_url: str,
        headers: Mapping[str, str] | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float = 30.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._headers = dict(headers or {})
        self._owned_client = client is None
        self._client = client or httpx.AsyncClient(timeout=timeout)

    async def close(self) -> None:
        if self._owned_client:
            await self._client.aclose()

    async def __aenter__(self) -> HTTPConnectorBase:
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.close()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        merged_headers = dict(self._headers)
        if headers:
            merged_headers.update(headers)

        url = path if path.startswith("http") else f"{self._base_url}/{path.lstrip('/')}"

        response = await self._client.request(
            method,
            url,
            params=params,
            json=json_body,
            headers=merged_headers,
        )

        if response.status_code >= 400:
            retry_after = _parse_retry_after_seconds(response.headers.get("Retry-After"))
            raise ConnectorRequestError(
                f"HTTP {response.status_code} for {method} {url}: {response.text}",
                status_code=response.status_code,
                failure_class=classify_http_status(response.status_code),
                retry_after_seconds=retry_after,
            )

        if response.content:
            parsed = response.json()
            if isinstance(parsed, dict):
                return parsed
            return {"items": parsed}
        return {}
