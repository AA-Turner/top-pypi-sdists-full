from __future__ import annotations

import asyncio
import socket

import pytest

from matrx_scraper.utils.url import (
    validate_and_correct_url,
    validate_public_http_url,
)


@pytest.mark.parametrize(
    "url",
    [
        "http://127.0.0.1/admin",
        "http://10.0.0.8/",
        "http://169.254.169.254/latest/meta-data/",
        "http://[::1]/",
        "http://localhost/",
    ],
)
def test_literal_non_public_targets_are_rejected(url: str) -> None:
    with pytest.raises(ValueError):
        validate_and_correct_url(url)


@pytest.mark.asyncio
async def test_dns_resolution_to_private_address_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loop = asyncio.get_running_loop()

    async def private_getaddrinfo(*args: object, **kwargs: object) -> list[tuple]:
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.10.0.4", 443))]

    monkeypatch.setattr(loop, "getaddrinfo", private_getaddrinfo)
    with pytest.raises(ValueError, match="non-public IP"):
        await validate_public_http_url("https://example.test/")
