from __future__ import annotations

import asyncio
import threading

import pytest

from matrx_scraper.web_crawl import url_identity


@pytest.mark.asyncio
async def test_crawl_relation_preparation_keeps_event_loop_responsive(monkeypatch) -> None:
    entered = threading.Event()
    release = threading.Event()
    loop_thread_id = threading.get_ident()
    worker_thread_ids: list[int] = []

    def blocking_prepare(crawl_urls, snapshots, *, root_url):
        worker_thread_ids.append(threading.get_ident())
        entered.set()
        release.wait(timeout=2)
        return [], set()

    class _Query:
        async def all(self, *, use_cache):
            return []

    class _Model:
        @classmethod
        def filter(cls, **kwargs):
            return _Query()

    async def load_pages(site_id):
        return []

    monkeypatch.setattr(url_identity, "_prepare_crawl_relations", blocking_prepare)
    monkeypatch.setattr(url_identity, "_load_site_pages", load_pages)
    monkeypatch.setattr(url_identity, "WebCrawlUrl", _Model)
    monkeypatch.setattr(url_identity, "WebSnapshot", _Model)

    task = asyncio.create_task(
        url_identity.reconcile_site_urls(
            site_id="site-id",
            organization_id="organization-id",
            user_id="user-id",
            root_url="https://example.com",
        )
    )
    assert await asyncio.to_thread(entered.wait, 1)
    await asyncio.sleep(0)
    assert not task.done()
    assert worker_thread_ids == [worker_thread_ids[0]]
    assert worker_thread_ids[0] != loop_thread_id

    task.cancel()
    release.set()
    with pytest.raises(asyncio.CancelledError):
        await task
