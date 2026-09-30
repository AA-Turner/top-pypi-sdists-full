"""A crawled page becomes a Source (SOURCE-CONVERGENCE §4.7).

SUT: ``CanonicalBodyPersister.__call__`` → ``_land_snapshot`` and the landing builder
``source_landing.crawl_snapshot_landing``. Doubled boundaries: the artifact write, the row write
(returns the committed snapshot's ids), the snapshot pointer update, and the door itself (the
injected ``source_landing`` hook — the real door is exercised in aidream's
``tests/test_crawl_snapshot_landing.py``).

Pinned:

* with NO hook registered the persister refuses BEFORE any artifact or row is written;
* a committed snapshot lands as a ``web_page`` Source: origin row = the ``web.page``, original =
  the snapshot's body file BY ID (no second S3 copy), ``crawl`` origin, ``internal``, unkept, filed
  under its site with signal=False (a structural filing is not a Keep), text = the markdown's sections;
* the snapshot is pointed at the Source (``processed_document_id``);
* a door refusal is announced as a crawl warning and the capture stands.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest
from matrx_files.cloud_sync.models import SyncResult

from matrx_scraper import _ext
from matrx_scraper.crawler import PersistRequest, PersistResult
from matrx_scraper.events import PageSummary
from matrx_scraper.source_landing import (
    SourceLandingFailed,
    SourceLandingNotConfigured,
    crawl_snapshot_landing,
)
from matrx_scraper.web_crawl import persistence as persistence_mod
from matrx_scraper.web_crawl.persistence import (
    CanonicalBodyPersister,
    CrawlPersistenceState,
    WebCrawlRepository,
)
from matrx_scraper.web_crawl.url_identity import CrawlIdentityResolution

ORG_ID = "00000000-0000-4000-8000-0000000fffa1"
USER_ID = "00000000-0000-4000-8000-0000000fffe1"
SITE_ID = "d0aff5b6-0710-4848-8304-164db3c80ab7"
SESSION_ID = "2b262f8c-1fbe-4575-81f5-c99c0709bd61"
PAGE_ID = "22913054-1933-44b8-ba94-f592f362b8c1"
SNAPSHOT_ID = "33913054-1933-44b8-ba94-f592f362b8c2"
DOC_ID = "44913054-1933-44b8-ba94-f592f362b8c3"
URL = "https://acme.example/pricing/"
BODY = "<html><body><h1>Pricing</h1><p>Widgets cost one dollar.</p></body></html>"
MARKDOWN = "# Pricing\nWidgets cost one dollar.\n## Bulk\nTen for nine."


class Hook:
    def __init__(self, fail: Exception | None = None) -> None:
        self.calls: list[dict[str, Any]] = []
        self.fail = fail

    async def __call__(self, landing: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(landing)
        if self.fail is not None:
            raise self.fail
        return {"processed_document_id": DOC_ID, "source_id": PAGE_ID, "notices": [], "kept": False}


@pytest.fixture
def registry(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    fresh: dict[str, Any] = {}
    monkeypatch.setattr(_ext, "_registry", fresh)
    return fresh


@pytest.fixture
def snapshot_updates(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    async def resolve_identity(**kwargs: Any) -> CrawlIdentityResolution:
        final_url = str(kwargs["final_url"])
        return CrawlIdentityResolution(
            requested_url=str(kwargs["requested_url"]),
            final_url=final_url,
            canonical_url=final_url,
            page_id=PAGE_ID,
            canonical_was_new=True,
        )

    class FakeFileService:
        def __init__(self, file_manager: object) -> None:
            self.file_manager = file_manager

    monkeypatch.setattr(persistence_mod, "resolve_crawl_page_identity", resolve_identity)
    monkeypatch.setattr(persistence_mod, "FileService", FakeFileService)
    update = AsyncMock(return_value=1)
    monkeypatch.setattr(persistence_mod.WebSnapshot, "update_where", update)
    return update


def _persister() -> tuple[CanonicalBodyPersister, AsyncMock, AsyncMock]:
    state = CrawlPersistenceState(
        site_id=SITE_ID,
        session_id=SESSION_ID,
        user_id=USER_ID,
        file_owner_id=USER_ID,
        organization_id=ORG_ID,
        coverage_qualified=False,
    )
    persister = CanonicalBodyPersister(
        WebCrawlRepository({"sub": USER_ID, "role": "authenticated"}),
        state,
        file_manager=SimpleNamespace(sync_engine=SimpleNamespace(hard_delete_and_purge_async=AsyncMock())),  # type: ignore[arg-type]
    )
    persister._load_previous_snapshot = AsyncMock(return_value=None)  # type: ignore[method-assign]
    count = {"n": 0}

    async def fake_write(**kwargs: Any) -> SyncResult:
        count["n"] += 1
        return SyncResult(
            file_id=f"file-{count['n']}-{kwargs['artifact_kind']}",
            storage_uri=f"s3://canonical/{count['n']}",
            version_number=1,
            is_new=True,
            published_to_web=False,
        )

    write = AsyncMock(side_effect=fake_write)
    persister._write_artifact = write  # type: ignore[method-assign]

    async def fake_rows(**kwargs: Any) -> PersistResult:
        return PersistResult(
            body_file_id=kwargs["body_artifact"].file_id,
            markdown_file_id=kwargs["markdown_artifact"].file_id if kwargs["markdown_artifact"] else None,
            page_id=PAGE_ID,
            snapshot_id=SNAPSHOT_ID,
        )

    rows = AsyncMock(side_effect=fake_rows)
    persister._persist_rows = rows  # type: ignore[method-assign]
    return persister, write, rows


def _request(markdown: str | None = MARKDOWN, engine: str | None = "http") -> PersistRequest:
    return PersistRequest(
        run_id=SESSION_ID,
        url=URL,
        final_url=URL,
        body=BODY,
        markdown=markdown,
        mime_type="text/html",
        page_summary=PageSummary(url=URL, final_url=URL, http_status=200, mime_type="html", title="Acme pricing"),
        engine=engine,
    )


@pytest.mark.asyncio
async def test_unwired_hook_refuses_before_anything_is_written(registry: dict[str, Any], snapshot_updates: AsyncMock) -> None:
    persister, write, rows = _persister()
    with pytest.raises(SourceLandingNotConfigured, match="configure_ext\\(source_landing"):
        await persister(_request())
    assert write.await_count == 0
    assert rows.await_count == 0
    assert snapshot_updates.await_count == 0


@pytest.mark.asyncio
async def test_committed_snapshot_lands_as_an_internal_unkept_web_page_source(
    registry: dict[str, Any], snapshot_updates: AsyncMock
) -> None:
    hook = Hook()
    registry["source_landing"] = hook
    persister, _write, _rows = _persister()

    result = await persister(_request(engine="browser"))

    assert len(hook.calls) == 1
    landing = hook.calls[0]
    assert landing["source_kind"] == "web_page"
    assert landing["source_id"] == PAGE_ID
    assert landing["canonical_identity"] == "https://acme.example/pricing"
    assert landing["name"] == "Acme pricing"
    assert landing["published_to_web"] is False
    assert landing["keep"] is False
    # Filed under its site, structurally: never a Keep.
    assert landing["attach_to"] == [
        {"entity_type": "web_site", "entity_id": SITE_ID, "label": "crawled_page", "signal": False}
    ]
    assert landing["organization_id"] == ORG_ID
    # The original is the snapshot's body file, by id — the door uploads nothing.
    assert landing["original"] == {"bytes_b64": None, "file_id": "file-1-response_body", "mime_type": "text/html"}
    prov = landing["provenance"]
    assert (prov["origin_client"], prov["capture_method"], prov["user_id"]) == ("crawl", "browser", USER_ID)
    assert [p["locator"]["heading_path"] for p in landing["portions"]] == [["Pricing"], ["Pricing", "Bulk"]]
    assert landing["structured"]["web_snapshot_id"] == SNAPSHOT_ID
    # The snapshot points at its Source.
    snapshot_updates.assert_awaited_once_with({"id": SNAPSHOT_ID}, processed_document_id=DOC_ID)
    assert result.warnings == []


@pytest.mark.asyncio
async def test_a_refused_landing_is_a_crawl_warning_and_the_capture_stands(
    registry: dict[str, Any], snapshot_updates: AsyncMock
) -> None:
    registry["source_landing"] = Hook(fail=SourceLandingFailed("origin_unreachable", "Not yours.", remedy="ask"))
    persister, _write, _rows = _persister()

    result = await persister(_request())

    assert result.snapshot_id == SNAPSHOT_ID
    assert snapshot_updates.await_count == 0
    assert len(result.warnings) == 1
    warning = result.warnings[0]
    assert "not saved as a Source" in warning["message"]
    assert warning["context"]["code"] == "origin_unreachable"


@pytest.mark.asyncio
async def test_a_page_with_no_markdown_writes_its_snapshot_and_lands_nothing(
    registry: dict[str, Any], snapshot_updates: AsyncMock
) -> None:
    hook = Hook()
    registry["source_landing"] = hook
    persister, _write, _rows = _persister()

    result = await persister(_request(markdown=None))

    assert result.snapshot_id == SNAPSHOT_ID
    assert hook.calls == []


def test_builder_without_a_body_file_carries_no_original_and_backfill_origin() -> None:
    landing = crawl_snapshot_landing(
        markdown=MARKDOWN,
        url=URL,
        title=None,
        page_id=PAGE_ID,
        body_file_id=None,
        body_mime_type=None,
        organization_id=ORG_ID,
        user_id=USER_ID,
        origin_client="backfill",
    )
    assert landing is not None
    assert landing["original"] is None
    assert landing["name"] == "acme.example/pricing"
    assert landing["provenance"]["origin_client"] == "backfill"
    assert landing["attach_to"] == []  # no site named, nothing to file under
    assert crawl_snapshot_landing(
        markdown="   ", url=URL, title=None, page_id=PAGE_ID, body_file_id=None,
        body_mime_type=None, organization_id=ORG_ID, user_id=USER_ID,
    ) is None


@pytest.mark.asyncio
async def test_http_hook_lands_over_the_bridge_when_a_long_crawls_login_expired(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A crawl runs for hours; the login it started under expires. The same person and
    organization land over the platform bridge instead of every later page failing with 401."""
    from matrx_scraper.server import source_landing_http as mod

    sent: list[dict[str, Any]] = []
    answers = [
        SimpleNamespace(status_code=401, json=lambda: {"code": "token_expired"}, text=""),
        SimpleNamespace(status_code=201, json=lambda: {"processed_document_id": DOC_ID}, text=""),
    ]

    class Client:
        def __init__(self, *a: Any, **k: Any) -> None: ...
        async def __aenter__(self) -> Client:
            return self
        async def __aexit__(self, *a: Any) -> None: ...
        async def post(self, url: str, json: dict[str, Any], headers: dict[str, str]) -> Any:
            sent.append({"url": url, "headers": headers})
            return answers.pop(0)

    monkeypatch.setattr(mod.httpx, "AsyncClient", Client)
    monkeypatch.setattr(mod, "_context", lambda: SimpleNamespace(token="jwt", metadata={"jwt_claims": {"sub": USER_ID}}))
    hook = mod.make_http_landing_hook(aidream_url="https://aidream.test", service_token="svc")
    landed = await hook({"organization_id": ORG_ID, "provenance": {"user_id": USER_ID}})

    assert landed["processed_document_id"] == DOC_ID
    assert [s["url"] for s in sent] == [
        "https://aidream.test/api/sources/land",
        "https://aidream.test/api/sources/internal/land",
    ]
    assert sent[1]["headers"]["Authorization"] == "Bearer svc"
    assert sent[1]["headers"]["X-Matrx-User-Id"] == USER_ID
    assert sent[1]["headers"]["X-Organization-Id"] == ORG_ID
