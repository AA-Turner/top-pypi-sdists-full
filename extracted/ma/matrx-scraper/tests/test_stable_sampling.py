from __future__ import annotations

import random

import pytest

from matrx_scraper import crawler
from matrx_scraper.sampling import StableHashSampler, stable_hash_sample


def test_stable_hash_sample_is_order_independent() -> None:
    items = [f"https://x.test/category/{index}" for index in range(1000)]
    reversed_items = list(reversed(items))
    shuffled_items = list(items)
    random.Random(42).shuffle(shuffled_items)

    expected = stable_hash_sample(items, 50, key=lambda url: url)

    assert stable_hash_sample(reversed_items, 50, key=lambda url: url) == expected
    assert stable_hash_sample(shuffled_items, 50, key=lambda url: url) == expected
    assert len(expected) == 50


def test_stable_hash_sampler_deduplicates_retained_items() -> None:
    sampler = StableHashSampler[str](10, key=lambda value: value)

    sampler.extend(["a", "a", "b", "b", "c"])

    assert sorted(sampler.items()) == ["a", "b", "c"]


def test_stable_hash_sample_rejects_invalid_limit() -> None:
    with pytest.raises(ValueError, match="limit must be at least 1"):
        StableHashSampler[str](0, key=lambda value: value)


@pytest.mark.asyncio
async def test_sitemap_discovery_samples_entire_urlset(monkeypatch) -> None:
    urls = [f"https://x.test/catalog/{index}" for index in range(1000)]
    body = (
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{url}</loc></url>" for url in urls)
        + "</urlset>"
    ).encode()

    class _Response:
        def __init__(self, status_code: int, content: bytes = b"") -> None:
            self.status_code = status_code
            self.content = content
            self.text = content.decode()

    class _Client:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args) -> None:
            return None

        async def get(self, url: str):
            if url.endswith("/sitemap.xml"):
                return _Response(200, body)
            return _Response(404)

    monkeypatch.setattr(crawler.httpx, "AsyncClient", lambda **_kwargs: _Client())

    discovered = await crawler._discover_sitemap_urls(
        "https://x.test/",
        user_agent="test",
        max_urls=50,
    )

    expected = stable_hash_sample(
        urls,
        50,
        key=lambda url: url,
        namespace="sitemap-urls:x.test",
    )
    assert discovered == expected
    assert discovered != urls[:50]
