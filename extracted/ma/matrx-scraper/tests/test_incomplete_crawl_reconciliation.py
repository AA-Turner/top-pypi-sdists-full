from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper.events import CrawlWarningEvent
from matrx_scraper.web_crawl import service as service_mod


class _Sink:
    def __init__(self) -> None:
        self.events: list[Any] = []

    async def emit(self, event: Any) -> None:
        self.events.append(event)


def _prepared() -> Any:
    return SimpleNamespace(
        site_id="site-1",
        session_id="session-1",
        root_url="https://example.com/",
        state=SimpleNamespace(organization_id="org-1", user_id="user-1"),
    )


@pytest.mark.asyncio
async def test_incomplete_crawl_reconciles_positive_url_facts(monkeypatch) -> None:
    calls: list[dict[str, str]] = []

    async def _reconcile(**kwargs: str) -> None:
        calls.append(kwargs)

    monkeypatch.setattr(service_mod, "reconcile_site_urls", _reconcile)
    sink = _Sink()

    await service_mod.WebCrawlService()._reconcile_urls_after_incomplete_crawl(_prepared(), sink)

    assert calls == [
        {
            "site_id": "site-1",
            "organization_id": "org-1",
            "user_id": "user-1",
            "root_url": "https://example.com/",
        }
    ]
    assert sink.events == []


@pytest.mark.asyncio
async def test_incomplete_crawl_reconciliation_failure_is_durable(monkeypatch) -> None:
    async def _reconcile(**_kwargs: str) -> None:
        raise RuntimeError("identity write failed")

    monkeypatch.setattr(service_mod, "reconcile_site_urls", _reconcile)
    sink = _Sink()

    await service_mod.WebCrawlService()._reconcile_urls_after_incomplete_crawl(_prepared(), sink)

    assert len(sink.events) == 1
    event = sink.events[0]
    assert isinstance(event, CrawlWarningEvent)
    assert event.context == {"reason": "incomplete_crawl_url_reconciliation_failed"}
    assert "identity write failed" in event.message
