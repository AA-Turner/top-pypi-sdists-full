"""A failed progress-log write never kills the command it describes.

Progress rows are a log for viewers who reconnect. When the FIRST one was
persisted before the command's `try`, one failed insert killed the command and
left its session `running` until the 30-minute stale reaper. Now the failure is
captured loudly, the event still streams, and the command finishes and settles.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper.web_crawl import persistence as persistence_module
from matrx_scraper.web_crawl import service as service_module
from matrx_scraper.web_crawl.contracts import SitemapSyncProgressEvent, SitemapSyncSummary
from matrx_scraper.web_crawl.persistence import DurableCrawlEventSink
from matrx_scraper.web_crawl.service import WebCrawlService


class _Emitter:
    def __init__(self) -> None:
        self.sent: list[dict[str, Any]] = []
        self.ended = False

    async def send_data(self, event: dict[str, Any]) -> None:
        self.sent.append(event)

    async def send_end(self) -> None:
        self.ended = True


def _state() -> SimpleNamespace:
    return SimpleNamespace(
        run_lease_token="lease-1",
        session_id="session-1",
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        event_sequence=0,
    )


class _BrokenLogRepository:
    def __init__(self) -> None:
        self.completed: list[dict[str, Any]] = []
        self.failed: list[str] = []

    async def persist_command_event(self, payload: dict[str, Any], state: object) -> None:
        raise RuntimeError("insert into web.crawl_event failed")

    async def mark_session_running(self, session_id: str, *, lease_token: str | None) -> None:
        return None

    async def complete_session(self, session_id: str, stats: dict[str, Any], *, lease_token: str | None) -> bool:
        self.completed.append(stats)
        return True

    async def fail_session(self, session_id: str, error: str, *, lease_token: str | None) -> None:
        self.failed.append(error)


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    kinds: list[str] = []

    async def capture(exc: BaseException, *, kind: str, context: dict[str, Any] | None = None) -> None:
        kinds.append(kind)

    monkeypatch.setattr(persistence_module, "capture_error", capture)
    return kinds


@pytest.mark.asyncio
async def test_a_failed_progress_insert_is_captured_and_the_event_still_streams(captured: list[str]) -> None:
    emitter = _Emitter()
    sink = DurableCrawlEventSink(_BrokenLogRepository(), _state(), None, emitter)  # type: ignore[arg-type]

    await sink.emit_command(
        SitemapSyncProgressEvent(
            site_id="site-1",
            session_id="session-1",
            status="started",
            message="Syncing sitemaps…",
            summary=SitemapSyncSummary(),
        )
    )

    assert [e["status"] for e in emitter.sent] == ["started"]
    assert captured == ["web_crawl_command_event_persist_failed"]


@pytest.mark.asyncio
async def test_the_command_finishes_and_settles_its_session_when_the_log_is_down(
    captured: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    async def sync_site_sitemaps(**_: Any) -> Any:
        return SimpleNamespace(summary=SitemapSyncSummary(found=2, urls=10), errors=[])

    async def reconcile_site_urls(**_: Any) -> None:
        return None

    monkeypatch.setattr(service_module, "sync_site_sitemaps", sync_site_sitemaps)
    monkeypatch.setattr(service_module, "reconcile_site_urls", reconcile_site_urls)
    repository = _BrokenLogRepository()
    prepared = SimpleNamespace(
        site_id="site-1",
        session_id="session-1",
        state=_state(),
        repository=repository,
        root_url="https://x.test/",
    )
    emitter = _Emitter()

    await WebCrawlService().run_sitemap_sync(emitter, prepared)  # type: ignore[arg-type]

    assert repository.failed == []
    assert len(repository.completed) == 1
    assert [e["status"] for e in emitter.sent] == ["started", "ok"]
    assert emitter.ended
