"""The Brave engine speaks more than one endpoint — and each has its own truths.

These are offline: they pin the parameter/URL contract per endpoint, which is
what silently breaks. The live behaviour they encode was verified against the
API on 2026-08-20 (each endpoint returned exactly its `max_count`).
"""

from __future__ import annotations

import pytest

from matrx_scraper.search.brave_client import (
    BRAVE_ENDPOINTS,
    BRAVE_WEB_SEARCH_URL,
    BraveSearchParams,
)


def test_web_wire_shape_is_unchanged_by_the_endpoint_split() -> None:
    """The whole point of defaulting `endpoint="web"`: an existing caller's
    request must be byte-identical to before multi-endpoint support existed."""
    params = BraveSearchParams(query="q", count=20, offset=0)
    assert params.url == BRAVE_WEB_SEARCH_URL
    assert params.to_dict() == {
        "q": "q",
        "count": 20,
        "offset": 0,
        "country": "us",
        "extra_snippets": True,
        "text_decorations": False,
        "safesearch": "off",
    }


@pytest.mark.parametrize(
    ("endpoint", "max_count"),
    [("web", 20), ("news", 50), ("videos", 50), ("images", 200)],
)
def test_count_is_clamped_to_each_endpoints_real_ceiling(endpoint: str, max_count: int) -> None:
    """Brave's ceiling differs fourfold across endpoints. Asking the image
    endpoint for 500 must yield 200, not a 422."""
    wire = BraveSearchParams(query="q", endpoint=endpoint, count=500).to_dict()
    assert wire["count"] == max_count


@pytest.mark.parametrize("endpoint", ["news", "videos", "images"])
def test_web_only_parameters_never_leak_to_other_endpoints(endpoint: str) -> None:
    """result_filter / goggles / summary / units / text_decorations are web-only.
    Sending them elsewhere is not a no-op we may rely on."""
    wire = BraveSearchParams(
        query="q",
        endpoint=endpoint,
        result_filter="web",
        goggles="$discard,site=example.com",
        summary=True,
        units="metric",
    ).to_dict()
    for leaked in ("result_filter", "goggles", "summary", "units", "text_decorations"):
        assert leaked not in wire, f"{leaked} leaked to the {endpoint} endpoint"


def test_images_endpoint_drops_offset_and_freshness() -> None:
    """The image endpoint accepts neither; both are silently ignored at best."""
    wire = BraveSearchParams(query="q", endpoint="images", offset=5, freshness="pw").to_dict()
    assert "offset" not in wire
    assert "freshness" not in wire


def test_news_keeps_extra_snippets_but_videos_does_not() -> None:
    news = BraveSearchParams(query="q", endpoint="news", extra_snippets=True).to_dict()
    videos = BraveSearchParams(query="q", endpoint="videos", extra_snippets=True).to_dict()
    assert news["extra_snippets"] is True
    assert "extra_snippets" not in videos


def test_every_endpoint_has_a_distinct_url() -> None:
    urls = [spec["url"] for spec in BRAVE_ENDPOINTS.values()]
    assert len(urls) == len(set(urls))
    assert all(url.startswith("https://api.search.brave.com/res/v1/") for url in urls)


def test_the_floor_does_not_throttle_a_pro_key() -> None:
    """🚨 Regression guard for a 30x self-inflicted throttle.

    FLOOR was 0.6s while a 1 req/sec base key was in the mix, which clamped the
    50 req/sec PRO key to 1.7 req/sec — 3% of what we pay for, and 30x the
    wall-clock on every fan-out. The floor is a cap for an over-reported header,
    never the working rate. If someone raises it back above the PRO key's
    MARGIN-adjusted interval, this fails.
    """
    from matrx_scraper.search.rate_limiter import (
        BRAVE_RATE_LIMIT_FLOOR_SECONDS,
        BRAVE_RATE_LIMIT_SAFETY_FACTOR,
        interval_for_rate,
    )

    pro_interval = BRAVE_RATE_LIMIT_SAFETY_FACTOR / 50
    assert BRAVE_RATE_LIMIT_FLOOR_SECONDS < pro_interval, (
        "FLOOR now binds for a 50 req/sec key — it is throttling the PRO key again"
    )
    assert interval_for_rate(50) == pytest.approx(pro_interval)
    # A wildly over-reported header still gets capped.
    assert interval_for_rate(100_000) == pytest.approx(BRAVE_RATE_LIMIT_FLOOR_SECONDS)
