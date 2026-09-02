"""Automatic broken-link evidence: same-crawl truth, polite redirects, resume rounds."""

from __future__ import annotations

from types import SimpleNamespace

import httpx
import pytest

from matrx_scraper.crawler import _normalise_url
from matrx_scraper.web_crawl import link_check as mod
from matrx_scraper.web_crawl.contracts import LinkCheckSummary, LinkResolutionSummary
from matrx_scraper.web_crawl.persistence import url_hash


def test_internal_status_uses_same_crawl_failure_without_page_registry_row() -> None:
    target = "https://example.com/missing"
    status = mod._select_internal_status(
        source_snapshot_id="source-snapshot",
        target_url=target,
        target_page_id=None,
        session_by_snapshot={"source-snapshot": "crawl-2"},
        same_session_status_by_page={},
        crawl_status_by_session_hash={("crawl-2", url_hash(_normalise_url(target))): 404},
        snapshot_by_page={},
        statuses_by_snapshot={},
    )

    assert status == 404, "a failed target must not need a web.page row to become evidence"


def test_internal_status_prefers_accepted_same_crawl_snapshot_over_later_failure() -> None:
    target = "https://example.com/"
    status = mod._select_internal_status(
        source_snapshot_id="source-snapshot",
        target_url=target,
        target_page_id="home-page",
        session_by_snapshot={"source-snapshot": "crawl-2"},
        same_session_status_by_page={("crawl-2", "home-page"): 200},
        crawl_status_by_session_hash={("crawl-2", url_hash(_normalise_url(target))): 403},
        snapshot_by_page={"home-page": "home-snapshot"},
        statuses_by_snapshot={"home-snapshot": 200},
    )

    assert status == 200, "a duplicate retry must not override an accepted capture"


def test_internal_status_falls_back_for_pre_ledger_edges() -> None:
    status = mod._select_internal_status(
        source_snapshot_id="legacy-source",
        target_url="https://example.com/about",
        target_page_id="about-page",
        session_by_snapshot={},
        same_session_status_by_page={},
        crawl_status_by_session_hash={},
        snapshot_by_page={"about-page": "about-snapshot"},
        statuses_by_snapshot={"about-snapshot": 200},
    )

    assert status == 200


@pytest.mark.asyncio
async def test_external_check_follows_redirects_and_records_final_status() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/old":
            return httpx.Response(301, headers={"location": "/missing"})
        return httpx.Response(404)

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), follow_redirects=True
    ) as client:
        checker = mod._PoliteChecker(client, concurrency=1, spacing_s=0)
        status = await checker.check("https://example.com/old")

    assert status == 404


@pytest.mark.asyncio
async def test_precompletion_link_check_drains_bounded_rounds(monkeypatch) -> None:
    from matrx_scraper.web_crawl import service as service_mod

    checks = 0

    async def resolve(**_kwargs):
        return SimpleNamespace(summary=LinkResolutionSummary(resolved=3))

    async def check(**_kwargs):
        nonlocal checks
        checks += 1
        return SimpleNamespace(
            summary=LinkCheckSummary(
                external_checked=500 if checks == 1 else 7,
                external_edges_updated=500 if checks == 1 else 7,
                external_truncated=checks == 1,
            )
        )

    monkeypatch.setattr(service_mod, "resolve_site_link_targets", resolve)
    monkeypatch.setattr(service_mod, "check_site_links", check)
    prepared = SimpleNamespace(mode="full", site_id="site-1", session_id="crawl-1")

    await service_mod.WebCrawlService()._populate_link_status_before_completion(prepared)

    assert checks == 2, "completion must drain every bounded target round"
