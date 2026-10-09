"""Pre-cutover check of the configured session endpoint and installed resolver."""

from __future__ import annotations

import asyncio
import json
import os

import httpx
from matrx_connect.middleware.remote_session import RemoteSessionResolver


async def check_authority(authority_url: str | None, *, timeout_seconds: float = 5) -> None:
    resolver = RemoteSessionResolver(authority_url, timeout_seconds=timeout_seconds)
    if resolver.authority_url is None:
        raise RuntimeError("MATRX_SESSION_AUTHORITY_URL is required")
    async with asyncio.timeout(timeout_seconds):
        async with httpx.AsyncClient(
            timeout=timeout_seconds, follow_redirects=False, trust_env=False
        ) as client:
            async with client.stream(
                "GET", resolver.authority_url, headers={"Accept-Encoding": "identity"}
            ) as response:
                if (
                    response.status_code != 401
                    or response.headers.get("content-encoding", "identity") != "identity"
                ):
                    raise RuntimeError("Session authority contract unavailable")
                body = bytearray()
                async for chunk in response.aiter_bytes(chunk_size=4096):
                    if len(body) + len(chunk) > 4096:
                        raise RuntimeError("Session authority response too large")
                    body.extend(chunk)
                if json.loads(body) != {"code": "invalid_session"}:
                    raise RuntimeError("Session authority contract mismatch")


if __name__ == "__main__":
    asyncio.run(check_authority(os.environ.get("MATRX_SESSION_AUTHORITY_URL")))
    print("Session authority contract available; authenticated admission is verified per request.")
