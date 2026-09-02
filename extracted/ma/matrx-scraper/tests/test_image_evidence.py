from __future__ import annotations

import struct

import httpx
import pytest

from matrx_scraper.image_evidence import (
    IMAGE_EVIDENCE_MAX_BYTES,
    IMAGE_EVIDENCE_MAX_REQUESTS,
    enrich_image_inventory,
    image_dimensions,
)


def png(width: int, height: int, payload: bytes = b"") -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + struct.pack(">II", width, height) + payload
    )


async def allow(_url: str) -> None:
    return None


def test_image_dimensions_reads_png_header() -> None:
    assert image_dimensions(png(1600, 900)) == (1600, 900)


@pytest.mark.asyncio
async def test_capture_deduplicates_and_records_status_bytes_dimensions_and_format() -> None:
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        if request.url.path == "/broken.jpg":
            return httpx.Response(404, content=b"missing", headers={"content-type": "image/jpeg"})
        return httpx.Response(200, content=png(1200, 800), headers={"content-type": "image/png"})

    items = [
        {"src": "https://example.com/hero.png", "width": 300},
        {"src": "https://example.com/hero.png", "width": 600},
        {"src": "https://example.com/broken.jpg"},
    ]
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await enrich_image_inventory(items, client=client, validate_url=allow)

    assert calls.count("https://example.com/hero.png") == 1
    assert items[0]["http_status"] == 200
    assert items[0]["bytes"] == len(png(1200, 800))
    assert (items[0]["natural_width"], items[0]["natural_height"]) == (1200, 800)
    assert items[0]["actual_format"] == "png"
    assert items[1]["natural_width"] == 1200
    assert items[2]["capture_status"] == "http_error"
    assert items[2]["http_status"] == 404


@pytest.mark.asyncio
async def test_capture_is_bounded_and_marks_unmeasured_inventory_honestly() -> None:
    calls = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, content=png(1, 1), headers={"content-type": "image/png"})

    items = [
        {"src": f"https://example.com/{index}.png"}
        for index in range(IMAGE_EVIDENCE_MAX_REQUESTS + 3)
    ]
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await enrich_image_inventory(items, client=client, validate_url=allow)

    assert calls == IMAGE_EVIDENCE_MAX_REQUESTS
    assert all(item["capture_status"] == "skipped_limit" for item in items[-3:])


@pytest.mark.asyncio
async def test_network_failure_is_recorded_without_fabricating_status_or_bytes() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route", request=request)

    items = [{"src": "https://example.com/offline.png"}]
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await enrich_image_inventory(items, client=client, validate_url=allow)

    assert items[0]["capture_status"] == "network_error"
    assert items[0]["capture_error"] == "ConnectError"
    assert "http_status" not in items[0]
    assert "bytes" not in items[0]


@pytest.mark.asyncio
async def test_declared_oversize_body_is_not_downloaded() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={
                "content-type": "image/jpeg",
                "content-length": str(IMAGE_EVIDENCE_MAX_BYTES + 1),
            },
        )

    items = [{"src": "https://example.com/huge.jpg"}]
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await enrich_image_inventory(items, client=client, validate_url=allow)
    assert items[0]["capture_status"] == "too_large"
    assert items[0]["bytes"] == IMAGE_EVIDENCE_MAX_BYTES + 1


@pytest.mark.asyncio
async def test_redirect_target_is_revalidated_before_following() -> None:
    validated: list[str] = []

    async def validate(url: str) -> None:
        validated.append(url)
        if url == "http://127.0.0.1/private.png":
            raise ValueError("private target")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(302, headers={"location": "http://127.0.0.1/private.png"})

    items = [{"src": "https://example.com/redirect.png"}]
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await enrich_image_inventory(items, client=client, validate_url=validate)
    assert validated == ["https://example.com/redirect.png", "http://127.0.0.1/private.png"]
    assert items[0]["capture_status"] == "blocked_url"
