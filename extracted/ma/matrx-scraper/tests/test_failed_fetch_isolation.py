"""Transient fetch failures must never corrupt canonical page state.

Canonical presence changes ONLY on authoritative negative HTTP evidence:
410 (immediate gone + soft delete) and 404 (debounced via consecutive
misses, same shape as coverage reconciliation). A network/timeout/render/
5xx/429 failure records its crawl_url outcome but leaves the existing
page's status exactly as the last authoritative observation set it.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from matrx_scraper.events import CrawlPageFailedEvent
from matrx_scraper.web_crawl.persistence import (
    GONE_AFTER_CONSECUTIVE_MISSES,
    CrawlPersistenceState,
    WebCrawlRepository,
    failed_fetch_disposition,
    url_hash,
)

# ---------------------------------------------------------------------------
# Pure disposition rules
# ---------------------------------------------------------------------------


def test_410_is_immediately_gone_and_soft_deleted() -> None:
    d = failed_fetch_disposition(410)
    assert d.authoritative and d.status == "gone" and d.soft_delete


def test_404_debounces_missing_then_gone() -> None:
    first = failed_fetch_disposition(404, prior_consecutive_misses=0)
    assert first.authoritative
    assert first.status == "missing"
    assert first.soft_delete is False
    assert first.consecutive_misses == 1

    at_threshold = failed_fetch_disposition(
        404, prior_consecutive_misses=GONE_AFTER_CONSECUTIVE_MISSES - 1
    )
    assert at_threshold.status == "gone"
    assert at_threshold.soft_delete is True
    assert at_threshold.consecutive_misses == GONE_AFTER_CONSECUTIVE_MISSES


@pytest.mark.parametrize("http_status", [None, 429, 500, 502, 503, 520, 403])
def test_transient_failures_are_never_authoritative(http_status) -> None:
    d = failed_fetch_disposition(http_status)
    assert d.authoritative is False
    assert d.status is None
    assert d.soft_delete is False
    assert d.consecutive_misses is None


# ---------------------------------------------------------------------------
# Persistence integration (model methods mocked)
# ---------------------------------------------------------------------------


def _state() -> CrawlPersistenceState:
    return CrawlPersistenceState(
        site_id="site-1",
        session_id="session-1",
        user_id="user-1",
        organization_id="org-1",
        file_owner_id="user-1",
        coverage_qualified=True,
    )


def _event(url: str = "https://acme.example/page") -> CrawlPageFailedEvent:
    return CrawlPageFailedEvent(
        run_id="session-1",
        url=url,
        error_class="TimeoutError",
        error_message="fetch timed out",
        ts=datetime.now(UTC).isoformat(),
    )


def _existing_page(status: str = "active") -> SimpleNamespace:
    return SimpleNamespace(id=uuid4(), deleted_at=None, status=status)


def _wire(
    monkeypatch: pytest.MonkeyPatch,
    *,
    page,
    evidence_row=None,
    http_status: int | None = None,
):
    ns = "matrx_scraper.web_crawl.persistence"
    page_update = AsyncMock()
    page_create = AsyncMock(return_value=_existing_page("missing"))
    monkeypatch.setattr(f"{ns}.WebPage.get_or_none", AsyncMock(return_value=page))
    monkeypatch.setattr(f"{ns}.WebPage.update_where", page_update)
    monkeypatch.setattr(f"{ns}.WebPage.create", page_create)
    monkeypatch.setattr(
        f"{ns}.WebPage.get",
        AsyncMock(return_value=SimpleNamespace(soft_delete=AsyncMock())),
    )
    crawl_url_create = AsyncMock(return_value=SimpleNamespace(id=uuid4()))
    monkeypatch.setattr(f"{ns}.WebCrawlUrl.create", crawl_url_create)
    evidence_get = AsyncMock(return_value=evidence_row)
    evidence_update = AsyncMock()
    evidence_create = AsyncMock()
    monkeypatch.setattr(f"{ns}.WebPageEvidence.get_or_none", evidence_get)
    monkeypatch.setattr(f"{ns}.WebPageEvidence.update_where", evidence_update)
    monkeypatch.setattr(f"{ns}.WebPageEvidence.create", evidence_create)
    return SimpleNamespace(
        page_update=page_update,
        page_create=page_create,
        crawl_url_create=crawl_url_create,
        evidence_update=evidence_update,
        evidence_create=evidence_create,
    )


@pytest.mark.asyncio
async def test_transient_failure_leaves_existing_page_status_untouched(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A timeout on a page that crawled fine yesterday must not mark it
    missing — the exact corruption this change removes."""
    page = _existing_page("active")
    prior_evidence = SimpleNamespace(
        id=uuid4(),
        is_present=True,
        evidence={"consecutive_misses": 0, "outcome": "captured"},
    )
    mocks = _wire(monkeypatch, page=page, evidence_row=prior_evidence)
    state = _state()  # no fetched entry -> http_status None (network failure)

    repo = WebCrawlRepository({})
    await repo._persist_failed_url_in_active_transaction(_event(), state)

    # The page row was never touched — no status write, no status_last write.
    assert mocks.page_update.await_count == 0
    assert mocks.page_create.await_count == 0
    # The crawl_url failure outcome IS recorded.
    assert mocks.crawl_url_create.await_count == 1
    assert mocks.crawl_url_create.await_args.kwargs["outcome"] == "failed"
    # Evidence: presence verdict + consecutive_misses preserved, check recorded.
    kwargs = mocks.evidence_update.await_args.kwargs
    assert "is_present" not in kwargs
    assert kwargs["evidence"]["consecutive_misses"] == 0
    assert "last_checked_at" in kwargs


@pytest.mark.asyncio
async def test_5xx_records_status_last_but_not_presence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    page = _existing_page("active")
    mocks = _wire(monkeypatch, page=page)
    state = _state()
    url = "https://acme.example/page"
    state.fetched[url] = SimpleNamespace(  # type: ignore[assignment]
        http_status=503, mime_type="text/html", final_url=None
    )

    repo = WebCrawlRepository({})
    await repo._persist_failed_url_in_active_transaction(_event(url), state)

    assert mocks.page_update.await_count == 1
    kwargs = mocks.page_update.await_args.kwargs
    assert kwargs["http_status_last"] == 503
    assert "status" not in kwargs


@pytest.mark.asyncio
async def test_404_debounce_marks_missing_then_gone_at_threshold(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    url = "https://acme.example/page"

    # First 404: missing, not soft-deleted.
    page = _existing_page("active")
    prior = SimpleNamespace(id=uuid4(), is_present=True, evidence={"consecutive_misses": 0})
    mocks = _wire(monkeypatch, page=page, evidence_row=prior)
    state = _state()
    state.fetched[url] = SimpleNamespace(  # type: ignore[assignment]
        http_status=404, mime_type="text/html", final_url=None
    )
    repo = WebCrawlRepository({})
    await repo._persist_failed_url_in_active_transaction(_event(url), state)
    assert mocks.page_update.await_args_list[0].kwargs["status"] == "missing"
    assert state.gone_pages == 0
    assert mocks.evidence_update.await_args.kwargs["evidence"]["consecutive_misses"] == 1

    # Miss at the threshold: gone + soft delete.
    page = _existing_page("missing")
    prior = SimpleNamespace(
        id=uuid4(),
        is_present=False,
        evidence={"consecutive_misses": GONE_AFTER_CONSECUTIVE_MISSES - 1},
    )
    mocks = _wire(monkeypatch, page=page, evidence_row=prior)
    state = _state()
    state.fetched[url] = SimpleNamespace(  # type: ignore[assignment]
        http_status=404, mime_type="text/html", final_url=None
    )
    await repo._persist_failed_url_in_active_transaction(_event(url), state)
    statuses = [c.kwargs.get("status") for c in mocks.page_update.await_args_list]
    assert "gone" in statuses
    assert state.gone_pages == 1


@pytest.mark.asyncio
async def test_410_still_soft_deletes_immediately(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    url = "https://acme.example/page"
    page = _existing_page("active")
    mocks = _wire(monkeypatch, page=page)
    state = _state()
    state.fetched[url] = SimpleNamespace(  # type: ignore[assignment]
        http_status=410, mime_type="text/html", final_url=None
    )
    repo = WebCrawlRepository({})
    await repo._persist_failed_url_in_active_transaction(_event(url), state)
    statuses = [c.kwargs.get("status") for c in mocks.page_update.await_args_list]
    assert "gone" in statuses
    assert state.gone_pages == 1


@pytest.mark.asyncio
async def test_brand_new_url_that_never_succeeded_is_created_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mocks = _wire(monkeypatch, page=None)
    state = _state()
    repo = WebCrawlRepository({})
    await repo._persist_failed_url_in_active_transaction(_event(), state)
    assert mocks.page_create.await_count == 1
    assert mocks.page_create.await_args.kwargs["status"] == "missing"
    assert state.new_pages == 1
    # Its first evidence row records absence (never seen successfully).
    assert mocks.evidence_create.await_args.kwargs["is_present"] is False


@pytest.mark.asyncio
async def test_already_soft_deleted_page_is_not_re_soft_deleted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A 410 (or threshold 404) on a page that is ALREADY soft-deleted must
    not re-stamp deleted_at or inflate gone_pages."""
    url = "https://acme.example/page"
    page = _existing_page("gone")
    page.deleted_at = datetime(2026, 1, 1, tzinfo=UTC)
    mocks = _wire(monkeypatch, page=page)
    state = _state()
    state.fetched[url] = SimpleNamespace(  # type: ignore[assignment]
        http_status=410, mime_type="text/html", final_url=None
    )

    repo = WebCrawlRepository({})
    await repo._persist_failed_url_in_active_transaction(_event(url), state)

    assert state.gone_pages == 0
    assert mocks.page_update.await_count == 0
    # The crawl_url failure fact is still recorded.
    assert mocks.crawl_url_create.await_count == 1


@pytest.mark.asyncio
async def test_404_miss_is_counted_once_per_session_across_reconcile(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The failure path and the coverage reconcile pass must not each count
    the same 404 — one crawl is ONE miss, so a persistently-404 page goes
    gone on the third crawl, never the second."""
    url = "https://acme.example/page"
    page = _existing_page("active")
    page.url_hash = url_hash(url)
    prior = SimpleNamespace(id=uuid4(), is_present=True, evidence={"consecutive_misses": 0})
    mocks = _wire(monkeypatch, page=page, evidence_row=prior)
    ns = "matrx_scraper.web_crawl.persistence"
    # Reconcile loads the site's live pages: return the same page.
    monkeypatch.setattr(
        f"{ns}.WebPage.filter",
        lambda **kwargs: SimpleNamespace(all=AsyncMock(return_value=[page])),
    )
    state = _state()
    state.fetched[url] = SimpleNamespace(  # type: ignore[assignment]
        http_status=404, mime_type="text/html", final_url=None
    )

    repo = WebCrawlRepository({})
    await repo._persist_failed_url_in_active_transaction(_event(url), state)
    assert page.url_hash in state.missed_hashes

    summary = await repo._reconcile_in_active_transaction(state)

    # Reconcile skipped the page the failure path already evidenced:
    # no second status write, no second consecutive_misses increment.
    status_writes = [c for c in mocks.page_update.await_args_list if "status" in c.kwargs]
    assert len(status_writes) == 1
    evidence_writes = [
        c.kwargs["evidence"].get("consecutive_misses")
        for c in mocks.evidence_update.await_args_list
        if "evidence" in c.kwargs
    ]
    assert evidence_writes == [1]
    assert summary["missing"] == 0 and summary["gone"] == 0
