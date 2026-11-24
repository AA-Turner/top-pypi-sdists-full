"""A sitemap's per-URL CPU work must not run on the event loop (live
event_loop_stall rows, workflow worker, 2026-11-16: 1.0-1.8 s freezes inside
normalize_url / validate_and_correct_url during the weekly sitemap refresh)."""

from __future__ import annotations

import asyncio
import threading
from types import SimpleNamespace

import pytest

from matrx_scraper.web_crawl import sitemap_sync, url_identity


@pytest.mark.asyncio
async def test_building_page_rows_runs_off_the_loop(monkeypatch):
    loop_thread = threading.get_ident()
    seen: list[int] = []
    real = sitemap_sync.normalize_sitemap_loc

    def spy(loc):
        seen.append(threading.get_ident())
        return real(loc)

    monkeypatch.setattr(sitemap_sync, "normalize_sitemap_loc", spy)
    doc = SimpleNamespace(
        kind="urlset",
        url="https://example.com/sitemap.xml",
        entries=[SimpleNamespace(loc="https://example.com/a")],
    )
    crawl = SimpleNamespace(documents=[doc])
    rows, memberships, skipped = await asyncio.to_thread(
        sitemap_sync._build_page_rows,
        crawl=crawl,
        sitemap_ids={doc.url: "sm1"},
        site_id="s",
        organization_id="o",
        user_id="u",
        now=None,
    )
    assert len(rows) == 1 and skipped == 0 and seen
    assert all(t != loop_thread for t in seen)


@pytest.mark.asyncio
async def test_upsert_observed_page_urls_normalizes_off_the_loop(monkeypatch):
    loop_thread = threading.get_ident()
    seen: list[int] = []
    real = url_identity.normalize_url

    def spy(u):
        seen.append(threading.get_ident())
        return real(u)

    monkeypatch.setattr(url_identity, "normalize_url", spy)

    async def stop(*a, **k):
        raise RuntimeError("stop after normalization")

    monkeypatch.setattr(url_identity, "_load_site_pages", stop)
    with pytest.raises(RuntimeError, match="stop after"):
        await url_identity.upsert_observed_page_urls(
            site_id="s", organization_id="o", user_id="u",
            urls=["https://example.com/a"], provenance="sitemap",
        )
    assert seen and all(t != loop_thread for t in seen)
