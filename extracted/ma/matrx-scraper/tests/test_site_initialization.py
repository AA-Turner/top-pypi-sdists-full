from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
import pytest

from matrx_scraper.events import CrawlPageFailedEvent, LinkEntry, PageSummary
from matrx_scraper.web_crawl.broker import CrawlEventBroker
from matrx_scraper.web_crawl.candidates import (
    DiscoveredCandidate,
    SiteIdentity,
    derive_site_identity,
    extract_homepage_candidates,
)
from matrx_scraper.web_crawl.contracts import (
    CrawlStartRequest,
    SitemapSyncSummary,
    UrlReconciliationSummary,
)
from matrx_scraper.web_crawl.persistence import (
    CanonicalBodyPersister,
    CrawlPersistenceState,
    HomepageCapture,
    WebCrawlRepository,
)
from matrx_scraper.web_crawl.service import PreparedCrawl, WebCrawlService
from matrx_scraper.web_crawl.sitemap_sync import SitemapSyncResult


def _response(url: str, status: int, body: str = "") -> httpx.Response:
    return httpx.Response(
        status,
        content=body.encode(),
        request=httpx.Request("GET", url),
    )


def test_candidate_extraction_uses_only_captured_homepage_data() -> None:
    html = """
    <html>
      <head>
        <title>Acme</title>
        <link rel="icon" href="/icon.svg">
      </head>
      <body>
        <header><img src="/brand.svg" alt="Acme logo"></header>
        <img class="hero-banner" src="/hero.jpg" width="1440" height="720">
        <p>Call (415) 555-1212 or fax (415) 555-3434.</p>
        <p>Email hello@acme.example.</p>
        <video src="/intro.mp4"></video>
        <iframe src="https://www.youtube.com/embed/demo-video"></iframe>
        <iframe src="https://www.googletagmanager.com/ns.html?id=GTM-EXAMPLE"></iframe>
      </body>
    </html>
    """
    summary = PageSummary(
        url="https://acme.example/",
        final_url="https://acme.example/",
        title="Acme",
        meta_description="Widgets for everyone",
        og_tags={
            "og:image": "https://cdn.acme.example/card.png",
            "og:site_name": "Acme Incorporated",
        },
        twitter_tags={"twitter:image": "/twitter.png"},
        schema_org={
            "@type": "Organization",
            "logo": {"url": "/schema-logo.png"},
            "sameAs": ["https://www.linkedin.com/company/acme"],
            "telephone": "+1 415-555-1212",
            "faxNumber": "+1 415-555-3434",
            "address": {"streetAddress": "123 Main Street"},
        },
        links=[
            LinkEntry(
                target_url="https://instagram.com/acme",
                anchor_text="Instagram",
            )
        ],
    )

    candidates = extract_homepage_candidates(
        html,
        base_url="https://acme.example/",
        summary=summary,
    )
    keys = {(item.category, item.guessed_kind, item.url) for item in candidates}

    assert ("media", "favicon", "https://acme.example/icon.svg") in keys
    assert not any(item.url == "https://acme.example/favicon.ico" for item in candidates)
    assert ("media", "logo", "https://acme.example/schema-logo.png") in keys
    assert ("media", "hero_image", "https://acme.example/hero.jpg") in keys
    assert ("media", "video", "https://acme.example/intro.mp4") in keys
    assert (
        "media",
        "video",
        "https://www.youtube.com/embed/demo-video",
    ) in keys
    assert not any("googletagmanager.com" in (item.url or "") for item in candidates)
    youtube = next(
        item for item in candidates if item.url == "https://www.youtube.com/embed/demo-video"
    )
    assert youtube.context["provider"] == "youtube"
    assert ("social", "instagram", "https://instagram.com/acme") in keys
    assert (
        "social",
        "linkedin",
        "https://www.linkedin.com/company/acme",
    ) in keys
    assert any(item.guessed_kind == "phone" for item in candidates)
    assert any(item.guessed_kind == "fax" for item in candidates)
    assert any(item.guessed_kind == "email" for item in candidates)
    assert any(item.guessed_kind == "address" for item in candidates)
    assert any(item.guessed_kind == "title" for item in candidates)
    fax_values = {item.value.get("text") for item in candidates if item.guessed_kind == "fax"}
    assert "+1 415-555-3434" in fax_values
    assert "(415) 555-3434" in fax_values
    assert not any(
        item.guessed_kind == "phone" and item.value.get("text") == "(415) 555-3434"
        for item in candidates
    )

    dedupe_keys = {
        (item.category, item.guessed_kind, item.url, str(item.value)) for item in candidates
    }
    assert len(dedupe_keys) == len(candidates)

    # Identity derivation from the same candidate set: schema.org logo beats
    # header/hint logos, og:image-as-logo (0.45) is below the identity bar,
    # description comes from the meta description.
    identity = derive_site_identity(candidates, summary=summary)
    assert identity.description == "Widgets for everyone"
    assert identity.favicon_url == "https://acme.example/icon.svg"
    assert identity.og_image_url == "https://cdn.acme.example/card.png"
    assert identity.logo_url == "https://acme.example/schema-logo.png"


def test_candidate_extraction_does_not_invent_a_conventional_favicon() -> None:
    summary = PageSummary(
        url="https://acme.example/",
        final_url="https://acme.example/",
    )
    candidates = extract_homepage_candidates(
        "<html><head></head><body></body></html>",
        base_url="https://acme.example/",
        summary=summary,
    )

    assert not any(item.guessed_kind == "favicon" for item in candidates)
    assert derive_site_identity(candidates, summary=summary).favicon_url is None


def test_identity_logo_confidence_gate_leaves_low_trust_logo_null() -> None:
    summary = PageSummary(
        url="https://acme.example/",
        final_url="https://acme.example/",
        og_tags={"og:image": "https://cdn.acme.example/card.png"},
    )
    # Only the og:image-derived logo guess (confidence 0.45) exists.
    candidates = extract_homepage_candidates(
        "<html><body></body></html>",
        base_url="https://acme.example/",
        summary=summary,
    )
    identity = derive_site_identity(candidates, summary=summary)
    assert identity.logo_url is None
    assert identity.og_image_url == "https://cdn.acme.example/card.png"
    assert identity.description is None


def _async_stub(value):
    """An async replacement for `_build_crawler`, which is a coroutine now."""

    async def _stub(prepared, sink, **kwargs):
        return value

    return _stub


@pytest.mark.asyncio
async def test_update_site_identity_fills_only_null_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OBSERVED identity must never overwrite a value the user may have set —
    only null/empty columns are filled."""

    import contextlib

    from matrx_scraper.web_crawl import persistence as p

    @contextlib.asynccontextmanager
    async def _fake_transaction(_db: str):
        yield None

    monkeypatch.setattr(p, "transaction", _fake_transaction)
    site = SimpleNamespace(
        description="User-authored description",
        favicon_url=None,
        og_image_url="",
        logo_url=None,
    )
    monkeypatch.setattr(p.WebSite, "get_or_none", AsyncMock(return_value=site))
    update = AsyncMock(return_value=SimpleNamespace(rows_affected=1))
    monkeypatch.setattr(p.WebSite, "update_where", update)

    repository = WebCrawlRepository({"sub": "user-1", "role": "authenticated"})
    result = await repository.update_site_identity(
        "site-1",
        SiteIdentity(
            description="Observed description",
            favicon_url="https://acme.example/icon.svg",
            og_image_url="https://cdn.acme.example/card.png",
            logo_url=None,
        ),
    )

    assert result == {
        "written": ["favicon_url", "og_image_url"],
        "skipped_existing": ["description"],
    }
    update.assert_awaited_once_with(
        {"id": "site-1"},
        favicon_url="https://acme.example/icon.svg",
        og_image_url="https://cdn.acme.example/card.png",
    )


@pytest.mark.asyncio
async def test_discovered_item_writes_are_idempotent_by_url_or_stable_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    insert = AsyncMock()
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.DiscoveredItem.bulk_insert_ignore",
        insert,
    )
    repository = WebCrawlRepository({"sub": "user-1", "role": "authenticated"})
    state = CrawlPersistenceState(
        site_id="site-1",
        session_id="session-1",
        user_id="user-1",
        organization_id="org-1",
        file_owner_id="user-1",
        coverage_qualified=False,
        brand_id="brand-1",
    )
    candidates = [
        DiscoveredCandidate(
            category="media",
            guessed_kind="logo",
            url="https://acme.example/logo.svg",
            context={"where": "header"},
            confidence=0.9,
        ),
        DiscoveredCandidate(
            category="fact",
            guessed_kind="phone",
            value={"text": "+1 415-555-1212"},
            context={"where": "schema.org"},
            confidence=0.98,
        ),
    ]

    first_counts = await repository.persist_discovered_items(
        state,
        candidates,
        snapshot_id="snapshot-1",
    )
    first_rows = [call.args[0] for call in insert.await_args_list]
    insert.reset_mock()
    second_counts = await repository.persist_discovered_items(
        state,
        candidates,
        snapshot_id="snapshot-1",
    )
    second_rows = [call.args[0] for call in insert.await_args_list]

    assert first_counts == second_counts == {"media": 1, "fact": 1}
    assert first_rows == second_rows
    # ONE statement for the whole batch, arbitrated by the DB's dedup index —
    # (brand_id, category, guessed_kind, url, value_hash) NULLS NOT DISTINCT,
    # value_hash being the STORED GENERATED md5(value::text) column (never
    # inserted). Two url-less facts with different values must both land.
    assert len(first_rows) == 1 and len(first_rows[0]) == 2
    assert first_rows[0][0]["status"] == "pending"
    assert first_rows[0][0]["source"] == "homepage_scrape"
    assert insert.await_args_list[0].kwargs["on_conflict"] == [
        "brand_id",
        "category",
        "guessed_kind",
        "url",
        "value_hash",
    ]


@pytest.mark.asyncio
async def test_url_null_facts_with_different_values_both_land_and_batch_self_dedupes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The production initialize failure: two DIFFERENT phone facts (url=NULL)
    collided under the old (brand, category, kind, url) arbiter. With
    value_hash in the arbiter both must be submitted; an exact in-batch
    duplicate must be dropped BEFORE the statement (ON CONFLICT cannot skip a
    duplicate arriving twice in one INSERT)."""

    insert = AsyncMock()
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.DiscoveredItem.bulk_insert_ignore",
        insert,
    )
    repository = WebCrawlRepository({"sub": "user-1", "role": "authenticated"})
    state = CrawlPersistenceState(
        site_id="site-1",
        session_id="session-1",
        user_id="user-1",
        organization_id="org-1",
        file_owner_id="user-1",
        coverage_qualified=False,
        brand_id="brand-1",
    )
    phone = DiscoveredCandidate(
        category="fact",
        guessed_kind="phone",
        value={"text": "+1 415-555-1212"},
        context={"where": "header"},
        confidence=0.9,
    )
    other_phone = DiscoveredCandidate(
        category="fact",
        guessed_kind="phone",
        value={"text": "+1 415-555-9999"},
        context={"where": "footer"},
        confidence=0.8,
    )
    counts = await repository.persist_discovered_items(
        state,
        [phone, other_phone, phone],
        snapshot_id="snapshot-1",
    )
    assert counts == {"fact": 2}
    assert insert.await_count == 1
    rows = insert.await_args_list[0].args[0]
    assert len(rows) == 2
    assert rows[0]["id"] != rows[1]["id"]
    assert all("value_hash" not in row for row in rows)


@pytest.mark.asyncio
async def test_initialize_screenshots_never_stamp_homepage_screenshot_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The DB guard requires site.homepage_screenshot_id to reference
    kind='homepage'. Initialize captures only the four responsive kinds, so
    the step must persist screenshots WITHOUT touching web.site at all —
    stamping any of them was the production CheckViolationError [23514]."""

    import contextlib

    from matrx_scraper.web_crawl import persistence as p

    @contextlib.asynccontextmanager
    async def _fake_transaction(_db: str):
        yield None

    monkeypatch.setattr(p, "transaction", _fake_transaction)
    monkeypatch.setattr(p, "resolve_screenshot_dimensions", lambda w, h, b: (w, h))

    site_update = AsyncMock()
    monkeypatch.setattr(p.WebSite, "update_where", site_update)

    created: list[dict] = []

    async def _create(**kwargs: object) -> SimpleNamespace:
        created.append(kwargs)
        return SimpleNamespace(id=f"screenshot-{len(created)}")

    monkeypatch.setattr(p.WebScreenshot, "create", AsyncMock(side_effect=_create))

    class _EmptyQuery:
        def order_by(self, *_args: object) -> _EmptyQuery:
            return self

        async def first(self) -> None:
            return None

        async def all(self) -> list[object]:
            return []

    monkeypatch.setattr(p.WebScreenshot, "filter", lambda **_kw: _EmptyQuery())

    state = CrawlPersistenceState(
        site_id="site-1",
        session_id="session-1",
        user_id="user-1",
        organization_id="org-1",
        file_owner_id="user-1",
        coverage_qualified=False,
        site_initialization=True,
    )
    persister = CanonicalBodyPersister.__new__(CanonicalBodyPersister)
    persister.repository = SimpleNamespace()
    persister.state = state
    persister.file_manager = SimpleNamespace()
    persister._write_artifact = AsyncMock(  # type: ignore[method-assign]
        return_value=SimpleNamespace(file_id="file-1", is_new=True)
    )

    from matrx_scraper.crawler import CapturedShot

    shots = [
        CapturedShot(kind=kind, width=100, height=100, bytes=b"png")
        for kind in ("desktop_full", "desktop_fold", "mobile_full", "mobile_fold")
    ]
    capture = HomepageCapture(
        html="<html></html>",
        summary=PageSummary(url="https://acme.example/", final_url="https://acme.example/"),
        page_id="page-1",
        snapshot_id="snapshot-1",
        final_url="https://acme.example/",
    )

    screenshot_ids, prune_counts = await persister.persist_initialization_screenshots(
        shots, capture=capture
    )

    assert set(screenshot_ids) == {
        "desktop_full",
        "desktop_fold",
        "mobile_full",
        "mobile_fold",
    }
    assert prune_counts == {"superseded": 0, "pruned": 0}
    site_update.assert_not_awaited()
    assert all("homepage_screenshot_id" not in row for row in created)


@pytest.mark.asyncio
async def test_screenshot_retention_keeps_current_plus_three_and_soft_deletes_rest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Re-running captures for the same (page, kind) keeps exactly the current
    row + 3 priors; older rows get soft-deleted along with their files.files
    rows (soft-delete only — storage purge belongs to the media machinery)."""

    import contextlib

    from matrx_scraper.web_crawl import persistence as p
    from matrx_scraper.web_crawl.persistence import prune_screenshot_history

    @contextlib.asynccontextmanager
    async def _fake_transaction(_db: str):
        yield None

    monkeypatch.setattr(p, "transaction", _fake_transaction)

    # 6 live rows, newest first (as ".order_by('-created_at')" returns them).
    rows = [SimpleNamespace(id=f"shot-{index}", file_id=f"file-{index}") for index in range(6)]

    class _Query:
        def order_by(self, *_args: object) -> _Query:
            return self

        async def all(self) -> list[SimpleNamespace]:
            return rows

    filters_seen: list[dict] = []

    def _filter(**kwargs: object) -> _Query:
        filters_seen.append(kwargs)
        return _Query()

    monkeypatch.setattr(p.WebScreenshot, "filter", _filter)
    screenshot_update = AsyncMock()
    monkeypatch.setattr(p.WebScreenshot, "update_where", screenshot_update)
    file_soft_delete = AsyncMock(return_value=True)
    file_manager = SimpleNamespace(
        sync_engine=SimpleNamespace(db=SimpleNamespace(soft_delete_file_async=file_soft_delete))
    )

    counts = await prune_screenshot_history(
        site_id="site-1",
        keys={("page-1", "desktop_fold")},
        file_manager=file_manager,
    )

    assert counts == {"superseded": 5, "pruned": 2}
    # The two OLDEST rows (indexes 4 and 5) are soft-deleted; newest 4 stay.
    deleted_ids = {call.args[0]["id"] for call in screenshot_update.await_args_list}
    assert deleted_ids == {"shot-4", "shot-5"}
    assert all("deleted_at" in call.kwargs for call in screenshot_update.await_args_list)
    deleted_files = {call.args[0] for call in file_soft_delete.await_args_list}
    assert deleted_files == {"file-4", "file-5"}
    assert filters_seen == [
        {
            "site_id": "site-1",
            "kind": "desktop_fold",
            "deleted_at__isnull": True,
            "page_id": "page-1",
        }
    ]


@pytest.mark.asyncio
async def test_initialization_step_failure_does_not_stop_independent_steps(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    summary = PageSummary(
        url="https://acme.example/",
        final_url="https://acme.example/",
        title="Acme",
    )
    state = CrawlPersistenceState(
        site_id="site-1",
        session_id="session-1",
        user_id="user-1",
        organization_id="org-1",
        file_owner_id="user-1",
        coverage_qualified=False,
        site_initialization=True,
        brand_id="brand-1",
        homepage_capture=HomepageCapture(
            html="<html><title>Acme</title></html>",
            summary=summary,
            page_id="page-1",
            snapshot_id="snapshot-1",
            final_url="https://acme.example/",
        ),
    )
    repository = SimpleNamespace(
        persist_event=AsyncMock(),
        update_initialization=AsyncMock(),
        update_site_identity=AsyncMock(
            return_value={"written": ["description"], "skipped_existing": []}
        ),
        persist_discovered_items=AsyncMock(return_value={"identity": 1}),
        fail_session=AsyncMock(),
    )
    broker = CrawlEventBroker("session-1")
    prepared = PreparedCrawl(
        site_id="site-1",
        session_id="session-1",
        root_url="https://acme.example/",
        request=CrawlStartRequest(
            max_pages=1,
            max_depth=0,
            list_mode=True,
            capture_screenshots=False,
            screenshot_kinds=[],
        ),
        repository=repository,
        state=state,
        broker=broker,
    )
    crawler = SimpleNamespace(run=AsyncMock())
    persister = SimpleNamespace(
        persist_initialization_screenshots=AsyncMock(
            return_value=(
                {
                    "desktop_full": "shot-1",
                    "desktop_fold": "shot-2",
                    "mobile_full": "shot-3",
                    "mobile_fold": "shot-4",
                },
                {"superseded": 1, "pruned": 0},
            )
        )
    )
    browser = SimpleNamespace(
        fetch_with_capture=AsyncMock(
            return_value=SimpleNamespace(
                screenshots=[
                    SimpleNamespace(kind=kind, width=100, height=100, bytes=b"png")
                    for kind in (
                        "desktop_full",
                        "desktop_fold",
                        "mobile_full",
                        "mobile_fold",
                    )
                ]
            )
        )
    )
    emitter = SimpleNamespace(send_data=AsyncMock(), send_end=AsyncMock())
    service = WebCrawlService()
    monkeypatch.setattr(
        service,
        "_build_crawler",
        # `_build_crawler` is async since 2026-08-20 — it loads the site's
        # host-pacing memory before constructing the crawler.
        _async_stub((crawler, persister)),
    )
    monkeypatch.setattr(service, "_watch_for_cancel", AsyncMock())
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.service.sync_site_sitemaps",
        AsyncMock(side_effect=RuntimeError("sitemap service unavailable")),
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.service.extract_homepage_candidates",
        lambda *args, **kwargs: [
            DiscoveredCandidate(
                category="identity",
                guessed_kind="title",
                value={"text": "Acme"},
                confidence=0.99,
            )
        ],
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.service.has_ext",
        lambda name: name == "browser_pool",
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.service.get_ext",
        lambda name: browser if name == "browser_pool" else None,
    )

    await service.run_initialize(emitter, prepared)

    persister.persist_initialization_screenshots.assert_awaited_once()
    repository.persist_discovered_items.assert_awaited_once()
    repository.update_site_identity.assert_awaited_once()
    emitter.send_end.assert_awaited_once()
    steps = [
        call.args[0]
        for call in emitter.send_data.await_args_list
        if getattr(call.args[0], "event_type", None) == "initialize_step"
    ]
    # The identity step (homepage + immediate site write) completes BEFORE any
    # concurrent step starts — the seconds-not-minutes contract.
    assert (steps[0].step, steps[0].status) == ("identity", "started")
    identity_done = next(
        index
        for index, event in enumerate(steps)
        if event.step == "identity" and event.status == "complete"
    )
    assert steps[identity_done].counts["written"] == 1
    assert all(
        index > identity_done
        for index, event in enumerate(steps)
        if event.step in {"screenshots", "sitemaps", "discovered"}
    )
    assert any(
        event.step == "sitemaps" and event.status == "failed" and event.error for event in steps
    )
    assert any(
        event.step == "screenshots" and event.status == "complete" and event.counts["captured"] == 4
        for event in steps
    )
    assert any(
        event.step == "discovered" and event.status == "complete" and event.counts["identity"] == 1
        for event in steps
    )
    # The durable summary channel still emits the terminal site_update event.
    site_updates = [
        call.args[0]
        for call in emitter.send_data.await_args_list
        if getattr(call.args[0], "event_type", None) == "site_initialization_progress"
    ]
    assert any(event.step == "site_update" and event.status == "ok" for event in site_updates)


@pytest.mark.asyncio
async def test_initialization_records_root_fetch_failure_once_and_skips_dependents(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state = CrawlPersistenceState(
        site_id="site-1",
        session_id="session-1",
        user_id="user-1",
        organization_id="org-1",
        file_owner_id="user-1",
        coverage_qualified=False,
        site_initialization=True,
        brand_id="brand-1",
    )
    await state.record_failed(
        CrawlPageFailedEvent(
            run_id="session-1",
            url="https://acme.example/",
            error_class="RateLimited",
            error_message="HTTP 429: host kept rate-limiting after 5 throttled retries",
            attempt=6,
        )
    )
    repository = SimpleNamespace(
        persist_event=AsyncMock(),
        update_initialization=AsyncMock(),
        fail_session=AsyncMock(),
    )
    prepared = PreparedCrawl(
        site_id="site-1",
        session_id="session-1",
        root_url="https://acme.example/",
        request=CrawlStartRequest(
            max_pages=1,
            max_depth=0,
            list_mode=True,
            capture_screenshots=False,
            screenshot_kinds=[],
        ),
        repository=repository,
        state=state,
        broker=CrawlEventBroker("session-1"),
    )
    crawler = SimpleNamespace(run=AsyncMock())
    emitter = SimpleNamespace(send_data=AsyncMock(), send_end=AsyncMock())
    service = WebCrawlService()
    monkeypatch.setattr(service, "_build_crawler", _async_stub((crawler, None)))
    monkeypatch.setattr(service, "_watch_for_cancel", AsyncMock())
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.service.sync_site_sitemaps",
        AsyncMock(
            return_value=SitemapSyncResult(
                SitemapSyncSummary(found=1, urls=4, pages_upserted=4),
                [],
            )
        ),
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.service.reconcile_site_urls",
        AsyncMock(return_value=SimpleNamespace(summary=UrlReconciliationSummary(pages_scanned=4))),
    )

    await service.run_initialize(emitter, prepared)

    events = [
        call.args[0]
        for call in emitter.send_data.await_args_list
        if getattr(call.args[0], "event_type", None) == "initialize_step"
    ]
    assert [(event.step, event.status) for event in events] == [
        ("identity", "started"),
        ("identity", "failed"),
        ("screenshots", "skipped"),
        ("sitemaps", "started"),
        ("sitemaps", "complete"),
        ("discovered", "skipped"),
    ]
    identity_error = next(
        event.error for event in events if event.step == "identity" and event.status == "failed"
    )
    assert identity_error is not None
    assert "RateLimited: HTTP 429" in identity_error

    persisted_summaries = [
        call.args[1] for call in repository.update_initialization.await_args_list
    ]
    final_summary = persisted_summaries[-1]
    assert final_summary["screenshots"] == {"captured": 0}
    assert final_summary["discovered"] == {}
    assert final_summary["errors"] == [
        {
            "step": "identity",
            "error_type": "RuntimeError",
            "message": (
                "Homepage fetch failed — RateLimited: HTTP 429: host kept "
                "rate-limiting after 5 throttled retries"
            ),
        }
    ]
    emitter.send_end.assert_awaited_once()

@pytest.mark.asyncio
async def test_prepare_initialize_uses_browser_for_authoritative_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A WAF's generic HTTP 403 must not define the site's identity result."""
    from matrx_scraper.crawler import RENDER_BROWSER_ALWAYS
    from matrx_scraper.web_crawl import service as service_module

    service = WebCrawlService()
    prepared = SimpleNamespace(
        repository=SimpleNamespace(site_brand_id=AsyncMock(return_value="brand-1")),
        state=SimpleNamespace(brand_id=None),
    )
    prepare_start = AsyncMock(return_value=prepared)
    monkeypatch.setattr(service, "prepare_start", prepare_start)
    monkeypatch.setattr(service_module, "has_ext", lambda name: name == "browser_pool")

    result = await service.prepare_initialize(SimpleNamespace(), "site-1")

    request = prepare_start.await_args.args[2]
    assert request.render_mode == RENDER_BROWSER_ALWAYS
    assert request.capture_screenshots is False
    assert result.state.brand_id == "brand-1"


@pytest.mark.asyncio
async def test_prepare_initialize_fails_before_session_without_browser_pool(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper.web_crawl import service as service_module

    service = WebCrawlService()
    prepare_start = AsyncMock()
    monkeypatch.setattr(service, "prepare_start", prepare_start)
    monkeypatch.setattr(service_module, "has_ext", lambda _name: False)

    with pytest.raises(RuntimeError, match="initialization requires the browser pool"):
        await service.prepare_initialize(SimpleNamespace(), "site-1")

    prepare_start.assert_not_awaited()
