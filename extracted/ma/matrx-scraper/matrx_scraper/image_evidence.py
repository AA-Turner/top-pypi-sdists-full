"""Bounded image metadata capture for the canonical page image inventory."""

from __future__ import annotations

import asyncio
import struct
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import urljoin

import httpx

from matrx_scraper.utils.url import validate_public_http_url

IMAGE_EVIDENCE_MAX_REQUESTS = 20
IMAGE_EVIDENCE_MAX_BYTES = 2 * 1024 * 1024
IMAGE_EVIDENCE_CONCURRENCY = 4
IMAGE_EVIDENCE_MAX_REDIRECTS = 5
IMAGE_EVIDENCE_TIMEOUT_S = 10.0
IMAGE_EVIDENCE_USER_AGENT = "MatrxScraperBot/0.1 (+https://aimatrx.com)"

UrlValidator = Callable[[str], Awaitable[None]]


def image_dimensions(data: bytes) -> tuple[int, int] | None:
    """Read dimensions from common image headers without an optional imaging dependency."""
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:6] in {b"GIF87a", b"GIF89a"} and len(data) >= 10:
        return struct.unpack("<HH", data[6:10])
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP" and len(data) >= 30:
        kind = data[12:16]
        if kind == b"VP8X":
            return (
                1 + int.from_bytes(data[24:27], "little"),
                1 + int.from_bytes(data[27:30], "little"),
            )
        if kind == b"VP8 " and data[23:26] == b"\x9d\x01\x2a":
            return (
                int.from_bytes(data[26:28], "little") & 0x3FFF,
                int.from_bytes(data[28:30], "little") & 0x3FFF,
            )
        if kind == b"VP8L" and data[20] == 0x2F:
            bits = int.from_bytes(data[21:25], "little")
            return (1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF))
    if data.startswith(b"\xff\xd8"):
        offset = 2
        while offset + 9 <= len(data):
            if data[offset] != 0xFF:
                offset += 1
                continue
            marker = data[offset + 1]
            offset += 2
            if marker in {0xD8, 0xD9} or 0xD0 <= marker <= 0xD7:
                continue
            if offset + 2 > len(data):
                break
            size = int.from_bytes(data[offset : offset + 2], "big")
            if size < 2 or offset + size > len(data):
                break
            if marker in {
                0xC0,
                0xC1,
                0xC2,
                0xC3,
                0xC5,
                0xC6,
                0xC7,
                0xC9,
                0xCA,
                0xCB,
                0xCD,
                0xCE,
                0xCF,
            }:
                return (
                    int.from_bytes(data[offset + 5 : offset + 7], "big"),
                    int.from_bytes(data[offset + 3 : offset + 5], "big"),
                )
            offset += size
    return None


def _format_from_content_type(value: str | None) -> str | None:
    mime = (value or "").split(";", 1)[0].strip().lower()
    aliases = {"image/jpeg": "jpg", "image/svg+xml": "svg"}
    if mime in aliases:
        return aliases[mime]
    return mime.removeprefix("image/") if mime.startswith("image/") else None


async def _capture_one(
    http: httpx.AsyncClient,
    url: str,
    *,
    validate_url: UrlValidator,
) -> dict[str, Any]:
    current = url
    try:
        for redirect_count in range(IMAGE_EVIDENCE_MAX_REDIRECTS + 1):
            await validate_url(current)
            async with http.stream("GET", current) as response:
                if response.is_redirect:
                    location = response.headers.get("location")
                    if not location:
                        return {"capture_status": "http_error", "http_status": response.status_code}
                    if redirect_count == IMAGE_EVIDENCE_MAX_REDIRECTS:
                        return {
                            "capture_status": "redirect_limit",
                            "http_status": response.status_code,
                        }
                    current = urljoin(current, location)
                    continue
                status = response.status_code
                content_type = response.headers.get("content-type")
                declared = response.headers.get("content-length")
                if declared and declared.isdigit() and int(declared) > IMAGE_EVIDENCE_MAX_BYTES:
                    return {
                        "capture_status": "too_large",
                        "http_status": status,
                        "bytes": int(declared),
                        "content_type": content_type,
                        "actual_format": _format_from_content_type(content_type),
                    }
                body = bytearray()
                async for chunk in response.aiter_bytes():
                    body.extend(chunk)
                    if len(body) > IMAGE_EVIDENCE_MAX_BYTES:
                        return {
                            "capture_status": "too_large",
                            "http_status": status,
                            "bytes": len(body),
                            "content_type": content_type,
                            "actual_format": _format_from_content_type(content_type),
                        }
                evidence: dict[str, Any] = {
                    "capture_status": "complete" if status < 400 else "http_error",
                    "http_status": status,
                    "bytes": len(body),
                    "content_type": content_type,
                    "actual_format": _format_from_content_type(content_type),
                    "final_url": str(response.url),
                }
                dimensions = image_dimensions(bytes(body))
                if dimensions:
                    evidence["natural_width"], evidence["natural_height"] = dimensions
                return evidence
        raise AssertionError("redirect loop escaped its bound")
    except ValueError as exc:
        return {"capture_status": "blocked_url", "capture_error": type(exc).__name__}
    except (httpx.HTTPError, OSError) as exc:
        return {"capture_status": "network_error", "capture_error": type(exc).__name__}


async def enrich_image_inventory(
    items: list[dict[str, Any]],
    *,
    client: httpx.AsyncClient | None = None,
    validate_url: UrlValidator = validate_public_http_url,
) -> None:
    """Enrich a page inventory in place with one request per distinct bounded URL."""
    capture_url_by_item: dict[int, str] = {}
    urls: list[str] = []
    for item in items:
        candidates = [*(item.get("picture_sources") or []), item.get("src")]
        capture_url = next(
            (
                candidate
                for candidate in candidates
                if isinstance(candidate, str) and candidate.startswith(("http://", "https://"))
            ),
            None,
        )
        if capture_url is not None:
            capture_url_by_item[id(item)] = capture_url
            item["capture_url"] = capture_url
            if capture_url not in urls:
                urls.append(capture_url)
    selected = urls[:IMAGE_EVIDENCE_MAX_REQUESTS]
    selected_set = set(selected)
    for item in items:
        capture_url = capture_url_by_item.get(id(item))
        if capture_url not in selected_set:
            item["capture_status"] = "skipped_limit" if capture_url else "missing_url"

    owns_client = client is None
    http = client or httpx.AsyncClient(
        timeout=IMAGE_EVIDENCE_TIMEOUT_S,
        follow_redirects=False,
        headers={"User-Agent": IMAGE_EVIDENCE_USER_AGENT},
    )
    semaphore = asyncio.Semaphore(IMAGE_EVIDENCE_CONCURRENCY)

    async def bounded(url: str) -> tuple[str, dict[str, Any]]:
        async with semaphore:
            return url, await _capture_one(http, url, validate_url=validate_url)

    try:
        captured = dict(await asyncio.gather(*(bounded(url) for url in selected)))
    finally:
        if owns_client:
            await http.aclose()
    for item in items:
        evidence = captured.get(capture_url_by_item.get(id(item)))
        if evidence is not None:
            item.update(evidence)
