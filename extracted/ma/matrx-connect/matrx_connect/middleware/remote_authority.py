"""Bounded, explicitly trusted HTTP transport shared by admission authorities."""

from __future__ import annotations

import asyncio
import json
import math
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlsplit

import httpx

from .session_authority import SessionAuthorityUnavailable


def validate_authority_url(authority_url: str | None, timeout_seconds: float) -> str | None:
    if authority_url and authority_url.strip():
        parsed = urlsplit(authority_url)
        if (
            any(c.isspace() or ord(c) < 32 or ord(c) == 127 or c == "\\" for c in authority_url)
            or parsed.scheme != "https"
            or not parsed.hostname
            or "%" in parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or "?" in authority_url
            or "#" in authority_url
        ):
            raise ValueError("Session authority must be a trusted HTTPS URL without credentials, query or fragment")
        _ = parsed.port
        try:
            httpx.URL(authority_url)
        except httpx.InvalidURL as exc:
            raise ValueError("Session authority URL is malformed") from exc
    else:
        authority_url = None
    if isinstance(timeout_seconds, bool) or not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        raise ValueError("Session authority timeout must be finite and positive")
    return authority_url


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate authority response field")
        result[key] = value
    return result


def decode_authority_json(body: bytes | bytearray) -> object:
    """Decode the bounded response without silently accepting duplicate fields."""
    try:
        return json.loads(body, object_pairs_hook=_unique_object)
    except ValueError as exc:
        raise SessionAuthorityUnavailable("Session authority could not be checked") from exc


@dataclass(frozen=True)
class AuthorityResponse:
    status_code: int
    headers: httpx.Headers
    body: bytes


async def fetch_authority_response(
    method: Literal["GET", "POST"],
    authority_url: str | None,
    headers: dict[str, str],
    timeout_seconds: float,
) -> AuthorityResponse:
    """Fresh trusted request; only200 bodies are read, bounded to4096 bytes.

    Callers interpret status/schema and generate their own outbound responses.
    No caller cookies, body, query selectors, redirects or env proxies enter.
    """
    if authority_url is None:
        raise SessionAuthorityUnavailable("Session authority is not configured")
    try:
        async with asyncio.timeout(timeout_seconds):
            async with httpx.AsyncClient(
                timeout=timeout_seconds, follow_redirects=False, trust_env=False
            ) as client:
                async with client.stream(
                    method, authority_url,
                    headers={**headers, "Accept": "application/json", "Accept-Encoding": "identity"},
                ) as response:
                    response_headers = httpx.Headers(response.headers)
                    if response.status_code != 200:
                        return AuthorityResponse(response.status_code, response_headers, b"")
                    if response.headers.get("content-encoding", "identity").lower() != "identity":
                        raise SessionAuthorityUnavailable("Session authority returned an unsupported response")
                    body = bytearray()
                    async for chunk in response.aiter_bytes(chunk_size=4096):
                        if len(body) + len(chunk) > 4096:
                            raise SessionAuthorityUnavailable("Session authority response exceeded its bound")
                        body.extend(chunk)
                    return AuthorityResponse(200, response_headers, bytes(body))
    except asyncio.CancelledError:
        raise
    except (TimeoutError, httpx.HTTPError, ValueError) as exc:
        raise SessionAuthorityUnavailable("Session authority could not be checked") from exc


async def fetch_authority_decision(
    authority_url: str | None, authorization: str, timeout_seconds: float
) -> tuple[bool, object]:
    """401 is a refusal; every other non200/invalid response is unavailable."""
    response = await fetch_authority_response(
        "GET", authority_url, {"Authorization": authorization}, timeout_seconds
    )
    if response.status_code == 401:
        return False, None
    if response.status_code != 200:
        raise SessionAuthorityUnavailable("Session authority did not return a decision")
    return True, decode_authority_json(response.body)
