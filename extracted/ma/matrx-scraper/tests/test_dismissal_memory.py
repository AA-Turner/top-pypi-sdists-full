"""Dismissal memory — Arman's ruling (2026-08-08): the crawler represents
REALITY. A user "delete" of a crawler-observed row is a DISMISSAL — hidden,
but if a later crawl/sync re-observes it, it comes back visibly AND
permanently carries the fact that the user dismissed it before. Never
silently ignored, never forgotten.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest

from matrx_scraper.crawler import (
    PersistResult,
    RENDER_BROWSER_WITH_SCREENSHOT,
    SiteCrawler,
    SiteCrawlerConfig,
)
from matrx_scraper.browser_pool import FetchWithCaptureResult
from matrx_scraper.events import CrawlWarningEvent
from matrx_scraper.queue_backend import InMemoryQueueBackend
from matrx_scraper.web_crawl.url_identity import (
    PageIdentityNode,
    RevivedDismissal,
    _alias_visibility_updates,
    append_dismissal_marker,
    upsert_observed_page_urls,
)

TOMBSTONE = datetime(2026, 3, 1, tzinfo=UTC)
NS = "matrx_scraper.web_crawl.url_identity"


# ---------------------------------------------------------------------------
# Marker helper
# ---------------------------------------------------------------------------


def test_first_dismissal_cycle_records_the_original_timestamp() -> None:
    metadata = append_dismissal_marker(
        {"existing": "kept"}, dismissed_at=TOMBSTONE, session_id="session-1"
    )
    assert metadata["existing"] == "kept"
    assert len(metadata["dismissals"]) == 1
    marker = metadata["dismissals"][0]
    assert marker["dismissed_at"] == TOMBSTONE.isoformat()
    assert marker["revive_reason"] == "reobserved"
    assert marker["revived_by_session"] == "session-1"
    assert marker["revived_at"]


def test_second_cycle_appends_and_preserves_the_first() -> None:
    first = append_dismissal_marker({}, dismissed_at=TOMBSTONE, session_id="s-1")
    second_tombstone = datetime(2026, 5, 1, tzinfo=UTC)
    second = append_dismissal_marker(first, dismissed_at=second_tombstone, session_id="s-2")
    assert len(second["dismissals"]) == 2
    assert second["dismissals"][0]["dismissed_at"] == TOMBSTONE.isoformat()
    assert second["dismissals"][1]["dismissed_at"] == second_tombstone.isoformat()
    assert second["dismissals"][1]["revived_by_session"] == "s-2"
    # The input dict is never mutated in place.
    assert len(first["dismissals"]) == 1


# ---------------------------------------------------------------------------
# Page revive path
# ---------------------------------------------------------------------------


def _page(
    *,
    url: str,
    deleted_at: datetime | None,
    metadata: dict[str, Any] | None = None,
) -> SimpleNamespace:
    page_id = "11111111-1111-4111-8111-111111111111"
    return SimpleNamespace(
        id=page_id,
        url=url,
        canonical_page_id=page_id,
        deleted_at=deleted_at,
        metadata=metadata or {},
    )


def _wire(monkeypatch: pytest.MonkeyPatch, page: SimpleNamespace) -> AsyncMock:
    monkeypatch.setattr(f"{NS}._load_site_pages", AsyncMock(return_value=[page]))
    update_where = AsyncMock()
    monkeypatch.setattr(f"{NS}.WebPage.update_where", update_where)
    monkeypatch.setattr(f"{NS}.WebPage.bulk_upsert", AsyncMock())

    @asynccontextmanager
    async def fake_transaction(*_args: object, **_kwargs: object):
        yield

    monkeypatch.setattr(f"{NS}.transaction", fake_transaction)
    return update_where


@pytest.mark.asyncio
async def test_reobserved_dismissed_page_carries_the_dismissal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    url = "https://example.com/dismissed"
    page = _page(url=url, deleted_at=TOMBSTONE)
    update_where = _wire(monkeypatch, page)
    revived: list[RevivedDismissal] = []

    await upsert_observed_page_urls(
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        urls=[url],
        provenance="sitemap",
        session_id="session-9",
        revived=revived,
    )

    revive_call = next(
        c for c in update_where.await_args_list if c.kwargs.get("deleted_at", "sentinel") is None
    )
    dismissals = revive_call.kwargs["metadata"]["dismissals"]
    assert dismissals[0]["dismissed_at"] == TOMBSTONE.isoformat()
    assert dismissals[0]["revived_by_session"] == "session-9"
    assert len(revived) == 1
    assert revived[0].url == url
    assert revived[0].dismissal_count == 1


@pytest.mark.asyncio
async def test_second_dismiss_revive_cycle_appends_history(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    url = "https://example.com/dismissed-twice"
    prior_cycle = append_dismissal_marker(
        {}, dismissed_at=datetime(2026, 1, 1, tzinfo=UTC), session_id="s-old"
    )
    page = _page(url=url, deleted_at=TOMBSTONE, metadata=prior_cycle)
    update_where = _wire(monkeypatch, page)
    revived: list[RevivedDismissal] = []

    await upsert_observed_page_urls(
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        urls=[url],
        provenance="crawl",
        session_id="s-new",
        revived=revived,
    )

    revive_call = next(
        c for c in update_where.await_args_list if c.kwargs.get("deleted_at", "sentinel") is None
    )
    dismissals = revive_call.kwargs["metadata"]["dismissals"]
    assert len(dismissals) == 2
    assert dismissals[0]["revived_by_session"] == "s-old"
    assert dismissals[1]["dismissed_at"] == TOMBSTONE.isoformat()
    assert dismissals[1]["revived_by_session"] == "s-new"
    assert revived[0].dismissal_count == 2


@pytest.mark.asyncio
async def test_never_dismissed_page_gets_no_marker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    url = "https://example.com/alive"
    page = _page(url=url, deleted_at=None)
    update_where = _wire(monkeypatch, page)
    revived: list[RevivedDismissal] = []

    await upsert_observed_page_urls(
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        urls=[url],
        provenance="sitemap",
        session_id="session-9",
        revived=revived,
    )

    assert revived == []
    for call in update_where.await_args_list:
        assert "metadata" not in call.kwargs
        assert call.kwargs.get("deleted_at", "sentinel") != None  # noqa: E711


@pytest.mark.asyncio
async def test_historical_reconciliation_never_revives_a_dismissal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    url = "https://example.com/dismissed"
    page = _page(url=url, deleted_at=TOMBSTONE)
    update_where = _wire(monkeypatch, page)
    revived: list[RevivedDismissal] = []

    resolutions = await upsert_observed_page_urls(
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        urls=[url],
        provenance="crawl",
        revived=revived,
        fresh_observation=False,
    )

    assert resolutions[url].canonical_page_id == str(page.id)
    assert revived == []
    assert update_where.await_args_list == []


def test_batch_reconciliation_only_dismisses_live_aliases() -> None:
    canonical = PageIdentityNode(
        id="canonical",
        url="https://example.com/page",
        canonical_page_id="canonical",
        first_seen=TOMBSTONE,
        deleted_at=TOMBSTONE,
        latest_snapshot_id=None,
    )
    alias = PageIdentityNode(
        id="alias",
        url="https://www.example.com/page",
        canonical_page_id="alias",
        first_seen=TOMBSTONE,
        deleted_at=None,
        latest_snapshot_id=None,
    )

    updates = _alias_visibility_updates(
        [canonical, alias],
        {"canonical": "canonical", "alias": "canonical"},
        dismissed_at=TOMBSTONE,
    )

    assert updates == [{"id": "alias", "deleted_at": TOMBSTONE}]


# ---------------------------------------------------------------------------
# The durable crawl_warning on the session (never silent)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_persister_revive_warnings_become_crawl_warning_events(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def allow_test_url(url: str) -> None:
        return None

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    body = " ".join(["Useful dismissal memory regression content"] * 80)
    html = f"<html><head><title>Page</title></head><body>{body}</body></html>"

    class BrowserPool:
        async def fetch_with_capture(self, url: str, **kwargs: Any) -> FetchWithCaptureResult:
            return FetchWithCaptureResult(
                content=html,
                response_url=url,
                status_code=200,
                headers={"content-type": "text/html"},
                title="Page",
                screenshots=[],
            )

    class RevivingPersister:
        async def record_screenshots_expected(self, count: int) -> None:
            return None

        async def record_screenshots_captured(self, count: int) -> None:
            return None

        async def __call__(self, request: Any) -> PersistResult:
            return PersistResult(
                body_file_id="body-1",
                page_id="page-1",
                snapshot_id="snap-1",
                warnings=[
                    {
                        "message": (
                            "Re-observed a page you previously dismissed — it is "
                            "visible again and remembers the dismissal: "
                            f"{request.url}"
                        ),
                        "context": {
                            "reason": "revived_after_dismissal",
                            "url": request.url,
                            "dismissal_count": 1,
                        },
                    }
                ],
            )

    class CapturingSink:
        def __init__(self) -> None:
            self.events: list[Any] = []

        async def emit(self, event: Any) -> None:
            self.events.append(event)

    sink = CapturingSink()
    crawler = SiteCrawler(
        run_id="dismissal-warning",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=1,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            render_mode=RENDER_BROWSER_WITH_SCREENSHOT,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        body_persister=RevivingPersister(),
        browser_pool=BrowserPool(),
    )
    await crawler.run()

    warnings = [e for e in sink.events if isinstance(e, CrawlWarningEvent)]
    revive_warnings = [w for w in warnings if w.context.get("reason") == "revived_after_dismissal"]
    assert len(revive_warnings) == 1
    assert "previously dismissed" in revive_warnings[0].message
    assert revive_warnings[0].context["url"] == "https://x.test/"
