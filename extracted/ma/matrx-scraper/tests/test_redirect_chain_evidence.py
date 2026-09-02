"""Redirect-hop evidence contract.

Three laws under test:
  1. `_build_summary` NEVER fabricates a redirect status. When no transport
     chain exists, the synthesized hop carries status=None — the old code
     stamped a fake 301 over real 302/307/308/browser redirects.
  2. Non-HTML summaries carry the chain too (it used to be HTML-only).
  3. `crawl_url_fetch_metadata` sanitizes hops into the persisted
     `web.crawl_url.metadata` shape — presence of the `redirect_chain` key is
     the "this crawl records hop evidence" capability marker the frontend
     reports rely on.
"""

from __future__ import annotations


from matrx_scraper.crawler import (
    RENDER_HTTP_ONLY,
    SiteCrawler,
    SiteCrawlerConfig,
)
from matrx_scraper.orchestrator import ScrapeResult
from matrx_scraper.queue_backend import InMemoryQueueBackend, QueueItem
from matrx_scraper.web_crawl.persistence import crawl_url_fetch_metadata


class _NullSink:
    async def emit(self, event) -> None:  # pragma: no cover - unused
        return None


def _crawler() -> SiteCrawler:
    return SiteCrawler(
        run_id="run-redirect-evidence",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=1,
            render_mode=RENDER_HTTP_ONLY,
        ),
        event_sink=_NullSink(),
        queue_backend=InMemoryQueueBackend(),
    )


def test_build_summary_keeps_real_transport_chain() -> None:
    chain = [
        {"status": 302, "url": "https://x.test/old"},
        {"status": 200, "url": "https://x.test/new"},
    ]
    result = ScrapeResult(
        url="https://x.test/old",
        response_url="https://x.test/new",
        success=True,
        content_type="html",
        status_code=200,
        raw_html="<html><body><p>hello world</p></body></html>",
        redirect_chain=chain,
    )
    summary = _crawler()._build_summary(
        result, QueueItem("https://x.test/old", 0, None, "seed"), 10, 100, None
    )
    assert summary.redirect_chain == chain


def test_build_summary_never_fabricates_a_301() -> None:
    result = ScrapeResult(
        url="https://x.test/old",
        response_url="https://x.test/new",
        success=True,
        content_type="html",
        status_code=200,
        raw_html="<html><body><p>hello world</p></body></html>",
    )
    summary = _crawler()._build_summary(
        result, QueueItem("https://x.test/old", 0, None, "seed"), 10, 100, None
    )
    assert summary.redirect_chain == [
        {"status": None, "url": "https://x.test/old"},
        {"status": 200, "url": "https://x.test/new"},
    ]


def test_build_summary_non_html_carries_chain() -> None:
    chain = [
        {"status": 301, "url": "https://x.test/doc"},
        {"status": 200, "url": "https://x.test/doc.pdf"},
    ]
    result = ScrapeResult(
        url="https://x.test/doc",
        response_url="https://x.test/doc.pdf",
        success=True,
        content_type="pdf",
        status_code=200,
        raw_text="pdf text",
        redirect_chain=chain,
    )
    summary = _crawler()._build_summary(
        result, QueueItem("https://x.test/doc", 0, None, "seed"), 10, 100, None
    )
    assert summary.redirect_chain == chain


def test_crawl_url_fetch_metadata_sanitizes_hops() -> None:
    meta = crawl_url_fetch_metadata(
        [
            {"status": 301, "url": "https://x.test/a"},
            {"status": "junk", "url": "https://x.test/b"},
            {"url": ""},  # no url — dropped
            "not-a-dict",  # dropped
            {"status": None, "url": "https://x.test/c"},
        ]
    )
    assert meta == {
        "redirect_chain": [
            {"status": 301, "url": "https://x.test/a"},
            {"status": None, "url": "https://x.test/b"},
            {"status": None, "url": "https://x.test/c"},
        ]
    }


def test_crawl_url_fetch_metadata_presence_marker_on_empty() -> None:
    # Even with no chain at all, the key is present — that presence is the
    # capability marker separating "no redirect" from "pre-hop-capture crawl".
    assert crawl_url_fetch_metadata(None) == {"redirect_chain": []}


def test_crawl_url_fetch_metadata_caps_hops() -> None:
    hops = [{"status": 302, "url": f"https://x.test/{i}"} for i in range(100)]
    assert len(crawl_url_fetch_metadata(hops)["redirect_chain"]) == 25
