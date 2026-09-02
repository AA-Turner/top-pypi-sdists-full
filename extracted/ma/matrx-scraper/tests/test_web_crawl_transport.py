from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from matrx_files.cloud_sync.models import SyncResult

from matrx_scraper.api.crawl_router import router
from matrx_scraper.crawler import (
    CapturedShot,
    CrawlPersistenceError,
    PersistRequest,
    PersistResult,
    SiteCrawler,
    SiteCrawlerConfig,
)
from matrx_scraper.db.models_web import (
    CrawlEvent as WebCrawlEvent,
    CrawlSession as WebCrawlSession,
    CrawlUrl as WebCrawlUrl,
    Page as WebPage,
    PageEvidence as WebPageEvidence,
)
from matrx_scraper.db.web import WEB_DB_NAME
from matrx_scraper.events import (
    CrawlSessionCreatedEvent,
    CrawlWarningEvent,
    PageSummary,
)
from matrx_scraper.web_crawl.broker import CrawlEventBroker
from matrx_scraper.web_crawl.contracts import CrawlStartRequest
from matrx_scraper.web_crawl.persistence import (
    CanonicalBodyPersister,
    CrawlPersistenceState,
    WebCrawlRepository,
)
from matrx_scraper.web_crawl.url_identity import CrawlIdentityResolution
from matrx_scraper.server.app import create_app, _configure_standalone_filesystem
from matrx_scraper.server.config import ServerConfig


@pytest.fixture(autouse=True)
def _stub_canonical_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    async def resolve_identity(**kwargs: object) -> CrawlIdentityResolution:
        requested_url = str(kwargs["requested_url"])
        final_url = str(kwargs["final_url"])
        return CrawlIdentityResolution(
            requested_url=requested_url,
            final_url=final_url,
            canonical_url=final_url,
            page_id="22913054-1933-44b8-ba94-f592f362b8c1",
            canonical_was_new=True,
        )

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.resolve_crawl_page_identity",
        resolve_identity,
    )

    async def no_previous_snapshot(self: object, digest: str) -> None:
        return None

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.CanonicalBodyPersister._load_previous_snapshot",
        no_previous_snapshot,
    )


def _event(sequence: int) -> CrawlWarningEvent:
    return CrawlWarningEvent(
        run_id="session-1",
        session_id="session-1",
        site_id="site-1",
        sequence=sequence,
        message=f"event {sequence}",
    )


def test_event_uses_canonical_session_id() -> None:
    event = CrawlSessionCreatedEvent(run_id="session-1")
    assert event.session_id == "session-1"
    with pytest.raises(ValueError, match="same crawl session"):
        CrawlSessionCreatedEvent(run_id="one", session_id="two")


def test_crawl_command_defaults_ignore_robots_and_cover_full_site() -> None:
    request = CrawlStartRequest()
    assert request.respect_robots is False
    assert request.capture_screenshots is True
    assert request.coverage_qualified() is True
    assert CrawlStartRequest(max_depth=2).coverage_qualified() is False
    assert CrawlStartRequest(list_mode=True).coverage_qualified() is False


@pytest.mark.asyncio
async def test_startup_reaper_fails_sessions_without_recent_activity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    update = AsyncMock(return_value=SimpleNamespace(rows_affected=2))
    monkeypatch.setattr(WebCrawlSession, "update_where", update)

    assert await WebCrawlRepository.fail_stale_sessions() == 2

    filters = update.await_args.args[0]
    assert filters["status__in"] == ["queued", "running"]
    assert "updated_at__lt" in filters
    assert filters["deleted_at__isnull"] is True
    assert update.await_args.kwargs["status"] == "failed"
    assert update.await_args.kwargs["finished_at"] is not None
    assert "restarted" in update.await_args.kwargs["error"]


def test_crawl_command_rejects_invalid_regex_patterns_at_the_boundary() -> None:
    """An invalid include/exclude regex is a 422 before any session exists —
    a silently skipped pattern used to WIDEN a constrained crawl."""
    with pytest.raises(ValueError, match=r"invalid regex pattern.*\[unclosed"):
        CrawlStartRequest(include_patterns=["^/blog/", "[unclosed"])
    with pytest.raises(ValueError, match="invalid regex pattern"):
        CrawlStartRequest(exclude_patterns=["(?P<broken"])
    # Valid patterns still pass untouched.
    request = CrawlStartRequest(include_patterns=[r"^/docs/.*\.html$"])
    assert request.include_patterns == [r"^/docs/.*\.html$"]


def test_crawl_command_rejects_duplicate_or_unknown_screenshot_kinds() -> None:
    with pytest.raises(ValueError, match="must be unique"):
        CrawlStartRequest(
            screenshot_kinds=["full_page", "full_page"]  # type: ignore[list-item]
        )
    with pytest.raises(ValueError):
        CrawlStartRequest(
            screenshot_kinds=["homepage_only"]  # type: ignore[list-item]
        )


@pytest.mark.asyncio
async def test_broker_replays_then_streams_monotonic_events() -> None:
    broker = CrawlEventBroker("session-1", replay_size=10)
    await broker.publish(_event(1))
    await broker.publish(_event(2))
    subscription = await broker.subscribe(after_sequence=1)
    assert subscription.memory_covers is True
    assert [event.sequence for event in subscription.replay] == [2]

    await broker.publish(_event(3))
    live = await asyncio.wait_for(subscription.queue.get(), timeout=1)
    assert getattr(live, "sequence", None) == 3
    await broker.close()
    assert broker.is_closed_item(await asyncio.wait_for(subscription.queue.get(), timeout=1))


@pytest.mark.asyncio
async def test_strict_crawler_propagates_event_sink_failures() -> None:
    class RaisingSink:
        async def emit(self, event: object) -> None:
            raise RuntimeError("canonical persistence unavailable")

    crawler = SiteCrawler(
        run_id="session-1",
        config=SiteCrawlerConfig(base_url="https://example.com", seed_from_sitemap=False),
        event_sink=RaisingSink(),
        strict_persistence=True,
    )
    with pytest.raises(RuntimeError, match="canonical persistence unavailable"):
        await crawler._emit(_event(1))


# A GET route on this router may only be a DERIVED read — an aggregation a
# client cannot assemble from direct Supabase row reads. Structurally that
# means: it returns a typed Pydantic shape. Starting work is always a command
# (POST) that returns the live NDJSON stream, and there is no replay endpoint —
# a GET that streams would be exactly the crawl-history/replay surface this
# router refuses to own.
DERIVED_READ_ROUTES = {
    "/crawler/sites/{site_id}/duplicate-clusters",
    "/crawler/sites/{site_id}/link-graph",
    "/crawler/sessions/{session_id}/progress-series",
    "/crawler/sessions/{session_id}/previous",
    "/crawler/sessions/{base_session_id}/diff/{compare_session_id}",
    "/crawler/sites/{site_id}/diffs",
    "/crawler/sites/{site_id}/diffs/{session_id}",
}


def test_direct_crawler_router_has_commands_and_only_derived_get_routes() -> None:
    crawler_routes = [route for route in router.routes if "/crawler/" in route.path]
    paths = {route.path for route in crawler_routes}
    assert "/crawler/sites/{site_id}/sessions" in paths
    assert "/crawler/sites/{site_id}/bootstrap" in paths
    assert "/crawler/sites/{site_id}/initialize" in paths
    assert "/crawler/sessions/{session_id}/cancel" in paths
    assert "/crawler/sessions/{session_id}/stream" not in paths
    assert DERIVED_READ_ROUTES.issubset(paths)

    for route in crawler_routes:
        if route.methods == {"GET"}:
            # A derived read hands back a typed shape; it never streams.
            assert route.response_model is not None, route.path
            assert issubclass(route.response_model, BaseModel), route.path
        else:
            # Every non-read route is a command — never GET.
            assert "GET" not in route.methods, route.path
    for path in DERIVED_READ_ROUTES:
        route = next(r for r in crawler_routes if r.path == path)
        assert route.methods == {"GET"}, path


def test_every_capped_read_reports_what_its_cap_dropped() -> None:
    """A capped aggregate that reports only what it KEPT reads as 'this is
    everything'. `web.link_edge` holds ~610k rows — the omission counters are
    the contract that keeps a 1,000-node graph from posing as the whole site.
    """
    from matrx_scraper.web_crawl.contracts import (
        DuplicateCluster,
        DuplicateClusterReport,
        LinkGraph,
        ProgressSeries,
    )

    required = {
        DuplicateClusterReport: {
            "clusters_total",
            "clusters_returned",
            "clusters_omitted",
            "max_clusters",
            "scan_truncated",
        },
        DuplicateCluster: {"page_count", "pages_omitted"},
        LinkGraph: {
            "nodes_total",
            "nodes_returned",
            "nodes_omitted",
            "edges_total",
            "edges_returned",
            "edges_omitted",
            "max_nodes",
            "max_edges",
            "scan_truncated",
        },
        ProgressSeries: {
            "points_total",
            "points_returned",
            "points_omitted",
            "max_points",
            "sample_stride",
            "scan_truncated",
        },
    }
    for model, fields in required.items():
        assert fields.issubset(set(model.model_fields)), model.__name__


def test_standalone_cors_exposes_direct_crawl_session_headers() -> None:
    app = create_app(ServerConfig())
    cors = next(
        middleware for middleware in app.user_middleware if middleware.cls is CORSMiddleware
    )
    exposed = set(cors.kwargs["expose_headers"])
    assert {"X-Crawl-Session-Id", "X-Site-Id"}.issubset(exposed)


def test_append_only_model_columns_match_canonical_authority() -> None:
    crawl_url_fields = WebCrawlUrl._meta.fields
    assert {
        "sequence",
        "discovered_from_page_id",
        "is_in_scope",
        "reason_code",
        "completed_at",
    }.issubset(crawl_url_fields)
    assert "parent_url" not in crawl_url_fields
    assert "finished_at" not in crawl_url_fields

    crawl_event_fields = WebCrawlEvent._meta.fields
    assert {
        "sequence",
        "phase",
        "level",
        "message",
        "page_id",
        "crawl_url_id",
    }.issubset(crawl_event_fields)

    assert {
        "source_type",
        "source_binding_id",
        "external_key",
        "is_present",
        "first_seen_at",
        "last_seen_at",
        "last_checked_at",
        "evidence",
    }.issubset(WebPageEvidence._meta.fields)


@pytest.mark.asyncio
async def test_site_editor_check_uses_claim_bound_public_iam_function(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = WebCrawlRepository({"sub": "user-1", "role": "authenticated"})
    entered_rls = False
    calls: list[tuple[object, ...]] = []

    @asynccontextmanager
    async def fake_rls():
        nonlocal entered_rls
        entered_rls = True
        try:
            yield
        finally:
            entered_rls = False

    async def fake_call_function(*args: object, **kwargs: object) -> bool:
        assert entered_rls is True
        calls.append((*args, kwargs))
        return True

    monkeypatch.setattr(repository, "rls", fake_rls)
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.call_function",
        fake_call_function,
    )

    site_id = "d0aff5b6-0710-4848-8304-164db3c80ab7"
    await repository.assert_site_editor(site_id, "user-1")

    assert calls == [
        (
            WEB_DB_NAME,
            "iam",
            "has_access",
            "web_site",
            UUID(site_id),
            "editor",
            {"mode": "scalar"},
        )
    ]


@pytest.mark.asyncio
async def test_site_editor_check_rejects_false_public_iam_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = WebCrawlRepository({"sub": "user-1", "role": "authenticated"})

    @asynccontextmanager
    async def fake_rls():
        yield

    async def fake_call_function(*args: object, **kwargs: object) -> bool:
        return False

    monkeypatch.setattr(repository, "rls", fake_rls)
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.call_function",
        fake_call_function,
    )

    with pytest.raises(PermissionError, match="site editor access is required"):
        await repository.assert_site_editor(
            "d0aff5b6-0710-4848-8304-164db3c80ab7",
            "user-1",
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("page_mime", "has_html_metrics"),
    [("html", True), ("json", False)],
)
async def test_standalone_filesystem_supports_parser_and_canonical_persistence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    reset_matrx_settings: None,
    page_mime: str,
    has_html_metrics: bool,
) -> None:
    base_dir = tmp_path / "standalone-scraper"
    configured = _configure_standalone_filesystem(ServerConfig(base_dir=str(base_dir)))

    assert configured == str(base_dir)
    assert base_dir.is_dir()

    body_file_id = "62913054-1933-44b8-ba94-f592f362b8c1"
    screenshot_file_id = "72913054-1933-44b8-ba94-f592f362b8c1"

    class FakeFileService:
        def __init__(self, file_manager: object) -> None:
            self.file_manager = file_manager

        async def upload_with_intent(self, content: bytes, **kwargs: object) -> dict:
            file_id = (
                screenshot_file_id if str(kwargs["file_path"]).endswith(".png") else body_file_id
            )
            return {
                "result": SyncResult(
                    file_id=file_id,
                    storage_uri=f"s3://canonical/{file_id}",
                    version_number=1,
                    is_new=True,
                    visibility="internal",
                )
            }

    monkeypatch.setattr("matrx_scraper.web_crawl.persistence.FileService", FakeFileService)
    fake_file_manager = SimpleNamespace(managed_delete_async=AsyncMock())

    repository = WebCrawlRepository({"sub": "user-1", "role": "authenticated"})
    repository._record_page_evidence_in_active_transaction = AsyncMock()
    state = CrawlPersistenceState(
        site_id="d0aff5b6-0710-4848-8304-164db3c80ab7",
        session_id="2b262f8c-1fbe-4575-81f5-c99c0709bd61",
        user_id="4cf62e4e-2679-484f-b652-034e697418df",
        file_owner_id="4cf62e4e-2679-484f-b652-034e697418df",
        organization_id="5dc930e9-bd65-44a1-8369-af773f6e1a5b",
        coverage_qualified=True,
    )
    persister = CanonicalBodyPersister(
        repository,
        state,
        file_manager=fake_file_manager,  # type: ignore[arg-type]
    )

    page_id = UUID("22913054-1933-44b8-ba94-f592f362b8c1")
    snapshot_id = UUID("32913054-1933-44b8-ba94-f592f362b8c1")
    crawl_url_id = UUID("42913054-1933-44b8-ba94-f592f362b8c1")
    screenshot_id = UUID("52913054-1933-44b8-ba94-f592f362b8c1")
    full_page_png = (
        b"\x89PNG\r\n\x1a\n"
        + (13).to_bytes(4, "big")
        + b"IHDR"
        + (1440).to_bytes(4, "big")
        + (3200).to_bytes(4, "big")
    )

    @asynccontextmanager
    async def fake_transaction(*args, **kwargs):
        yield

    monkeypatch.setattr("matrx_scraper.web_crawl.persistence.transaction", fake_transaction)
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.WebPage.get_or_none",
        AsyncMock(return_value=None),
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.WebPage.create",
        AsyncMock(return_value=SimpleNamespace(id=page_id, deleted_at=None)),
    )
    monkeypatch.setattr("matrx_scraper.web_crawl.persistence.WebPage.update_where", AsyncMock())
    snapshot_create = AsyncMock(return_value=SimpleNamespace(id=snapshot_id))
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.WebSnapshot.create",
        snapshot_create,
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.WebCrawlUrl.create",
        AsyncMock(return_value=SimpleNamespace(id=crawl_url_id, outcome="captured")),
    )
    screenshot_create = AsyncMock(return_value=SimpleNamespace(id=screenshot_id))
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.WebScreenshot.create",
        screenshot_create,
    )
    prune = AsyncMock(return_value={"superseded": 0, "pruned": 0})
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.prune_screenshot_history",
        prune,
    )

    result = await persister(
        PersistRequest(
            run_id=state.session_id,
            url="https://example.com/",
            final_url="https://example.com/",
            body="<html><body>captured</body></html>",
            markdown=None,
            screenshots=[
                CapturedShot(
                    kind="full_page",
                    width=0,
                    height=0,
                    bytes=full_page_png,
                )
            ],
            page_summary=PageSummary(
                url="https://example.com/",
                final_url="https://example.com/",
                http_status=200,
                mime_type=page_mime,
                structured_data={
                    "schema_types": ["Article"],
                    "json_ld": [{"@type": "Article"}],
                    "json_ld_raw": ['{"@type":"Article"}'],
                },
                image_inventory=[{"src": "https://example.com/hero.jpg", "alt": "Hero"}],
                resources={
                    "count": 1,
                    "counts": {"image": 1},
                    "items": [
                        {
                            "kind": "image",
                            "url": "https://example.com/hero.jpg",
                        }
                    ],
                },
                page_identity={
                    "cms": "wordpress",
                    "featured_image": "https://example.com/hero.jpg",
                },
            ),
        )
    )

    assert result.page_id == str(page_id)
    assert result.snapshot_id == str(snapshot_id)
    assert result.body_file_id == body_file_id
    assert result.screenshot_file_ids == {"full_page": screenshot_file_id}
    assert snapshot_create.await_args.kwargs["body_file_id"] == body_file_id
    assert (snapshot_create.await_args.kwargs["seo_metrics"] is not None) is has_html_metrics
    assert (snapshot_create.await_args.kwargs["audit_metrics"] is not None) is has_html_metrics
    assert snapshot_create.await_args.kwargs["extracted"]["content_type"] == page_mime
    assert snapshot_create.await_args.kwargs["structured_data"]["json_ld"] == [{"@type": "Article"}]
    assert snapshot_create.await_args.kwargs["images"]["items"][0]["alt"] == "Hero"
    assert snapshot_create.await_args.kwargs["extracted"]["resources"]["count"] == 1
    assert snapshot_create.await_args.kwargs["extracted"]["page_identity"]["cms"] == "wordpress"
    assert screenshot_create.await_args.kwargs["file_id"] == screenshot_file_id
    assert screenshot_create.await_args.kwargs["width"] == 1440
    assert screenshot_create.await_args.kwargs["height"] == 3200
    page_create = WebPage.create
    assert page_create.await_args.kwargs["content_type_last"] == page_mime
    page_update = WebPage.update_where
    assert page_update.await_args.kwargs["content_type_last"] == page_mime
    prune.assert_awaited_once()
    assert prune.await_args.kwargs["keys"] == {(str(page_id), "full")}


def test_crawl_persistence_error_exposes_only_safe_stream_message() -> None:
    error = CrawlPersistenceError()

    assert error.error_info.error_type == "canonical_crawl_persistence_error"
    assert error.error_info.user_message == str(error)
    assert "constraint" not in str(error).lower()
    assert "\x1b" not in str(error)


@pytest.mark.asyncio
async def test_canonical_persister_archives_xml_with_its_real_format_and_mime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeFileService:
        def __init__(self, file_manager: object) -> None:
            self.file_manager = file_manager

    monkeypatch.setattr("matrx_scraper.web_crawl.persistence.FileService", FakeFileService)
    state = CrawlPersistenceState(
        site_id="d0aff5b6-0710-4848-8304-164db3c80ab7",
        session_id="2b262f8c-1fbe-4575-81f5-c99c0709bd61",
        user_id="4cf62e4e-2679-484f-b652-034e697418df",
        file_owner_id="4cf62e4e-2679-484f-b652-034e697418df",
        organization_id="5dc930e9-bd65-44a1-8369-af773f6e1a5b",
        coverage_qualified=False,
    )
    persister = CanonicalBodyPersister(
        WebCrawlRepository({"sub": state.user_id, "role": "authenticated"}),
        state,
        file_manager=SimpleNamespace(),  # type: ignore[arg-type]
    )
    body_result = SyncResult(
        file_id="xml-body-file",
        storage_uri="s3://canonical/xml-body-file",
        version_number=1,
        is_new=True,
        visibility="internal",
    )
    write = AsyncMock(return_value=body_result)
    persister._write_artifact = write  # type: ignore[method-assign]
    persister._persist_rows = AsyncMock(  # type: ignore[method-assign]
        return_value=PersistResult(
            body_file_id=body_result.file_id,
            page_id="xml-page",
            snapshot_id="xml-snapshot",
        )
    )
    kml = '<?xml version="1.0"?><kml><Document><name>Locations</name></Document></kml>'

    result = await persister(
        PersistRequest(
            run_id=state.session_id,
            url="https://datadestruction.com/locations.kml",
            final_url="https://datadestruction.com/locations.kml",
            body=kml,
            markdown=None,
            mime_type="text/xml; charset=UTF-8",
            page_summary=PageSummary(
                url="https://datadestruction.com/locations.kml",
                final_url="https://datadestruction.com/locations.kml",
                http_status=200,
                mime_type="xml",
            ),
        )
    )

    assert result.body_file_id == "xml-body-file"
    assert write.await_count == 1
    write_kwargs = write.await_args.kwargs
    assert write_kwargs["file_path"].endswith("/body.xml")
    assert write_kwargs["content"] == kml
    assert write_kwargs["mime_type"] == "text/xml"
    assert write_kwargs["artifact_kind"] == "response_body"


@pytest.mark.asyncio
async def test_canonical_persister_never_deletes_an_access_denied_duplicate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeFileService:
        def __init__(self, file_manager: object) -> None:
            self.file_manager = file_manager

    monkeypatch.setattr("matrx_scraper.web_crawl.persistence.FileService", FakeFileService)
    purge = AsyncMock()
    file_manager = SimpleNamespace(sync_engine=SimpleNamespace(hard_delete_and_purge_async=purge))
    state = CrawlPersistenceState(
        site_id="d0aff5b6-0710-4848-8304-164db3c80ab7",
        session_id="2b262f8c-1fbe-4575-81f5-c99c0709bd61",
        user_id="4cf62e4e-2679-484f-b652-034e697418df",
        file_owner_id="4cf62e4e-2679-484f-b652-034e697418df",
        organization_id="5dc930e9-bd65-44a1-8369-af773f6e1a5b",
        coverage_qualified=False,
    )
    persister = CanonicalBodyPersister(
        WebCrawlRepository({"sub": state.user_id, "role": "authenticated"}),
        state,
        file_manager=file_manager,  # type: ignore[arg-type]
    )
    upload = AsyncMock(side_effect=PermissionError("canonical duplicate is not reachable"))
    persister.files = SimpleNamespace(
        upload_with_intent=upload,
    )

    with pytest.raises(PermissionError, match="canonical duplicate is not reachable"):
        await persister._write_artifact(
            file_path="system-files/scraper/capture/body.md",
            content="# Captured",
            mime_type="text/markdown",
            artifact_kind="markdown_body",
            capture_id="capture-1",
        )

    upload.assert_awaited_once()
    purge.assert_not_awaited()


@pytest.mark.asyncio
async def test_failed_persistence_purges_every_new_artifact_by_exact_identity() -> None:
    body = SyncResult(
        file_id="body-file",
        storage_uri="s3://canonical/body-file",
        version_number=1,
        is_new=True,
        visibility="internal",
    )
    markdown = SyncResult(
        file_id="markdown-file",
        storage_uri="s3://canonical/markdown-file",
        version_number=1,
        is_new=True,
        visibility="internal",
    )
    screenshot = SyncResult(
        file_id="screenshot-file",
        storage_uri="s3://canonical/screenshot-file",
        version_number=1,
        is_new=True,
        visibility="internal",
    )
    purge = AsyncMock()
    file_manager = SimpleNamespace(sync_engine=SimpleNamespace(hard_delete_and_purge_async=purge))
    state = CrawlPersistenceState(
        site_id="d0aff5b6-0710-4848-8304-164db3c80ab7",
        session_id="2b262f8c-1fbe-4575-81f5-c99c0709bd61",
        user_id="4cf62e4e-2679-484f-b652-034e697418df",
        file_owner_id="4cf62e4e-2679-484f-b652-034e697418df",
        organization_id="5dc930e9-bd65-44a1-8369-af773f6e1a5b",
        coverage_qualified=False,
    )
    persister = CanonicalBodyPersister(
        WebCrawlRepository({"sub": state.user_id, "role": "authenticated"}),
        state,
        file_manager=file_manager,  # type: ignore[arg-type]
    )
    persister._write_artifact = AsyncMock(  # type: ignore[method-assign]
        side_effect=[body, markdown, screenshot]
    )
    persister._persist_rows = AsyncMock(  # type: ignore[method-assign]
        side_effect=RuntimeError("transaction rejected")
    )

    with pytest.raises(RuntimeError, match="transaction rejected"):
        await persister(
            PersistRequest(
                run_id=state.session_id,
                url="https://example.com/",
                final_url="https://example.com/",
                body="<html><body>captured</body></html>",
                markdown="# Captured",
                screenshots=[
                    CapturedShot(
                        kind="viewport_desktop",
                        width=1440,
                        height=900,
                        bytes=b"png",
                    )
                ],
                page_summary=PageSummary(
                    url="https://example.com/",
                    final_url="https://example.com/",
                    http_status=200,
                ),
            )
        )

    assert [call.args for call in purge.await_args_list] == [
        ("screenshot-file", "s3://canonical/screenshot-file"),
        ("markdown-file", "s3://canonical/markdown-file"),
        ("body-file", "s3://canonical/body-file"),
    ]
