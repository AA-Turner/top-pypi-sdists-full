"""A page capture's write transaction is a handful of statements, never one per link.

2026-10-15 production stall: `_persist_rows` resolved and inserted every
link edge with its own round trips (two statements per link) inside ONE
write transaction. On link-heavy pages that held an xid for 20-45 s, and
every Supabase Realtime CDC attach (`pg_create_logical_replication_slot`)
waits for each running xid-holder — realtime timed out at 10 s and
retried in a storm all morning.

SUT: the REAL `CanonicalBodyPersister._persist_rows`. Doubled boundary:
the ORM model classes and `transaction`, which count every DB statement
issued while the transaction is open. The pinned contract: the statement
count does not grow with the number of links, and every edge still
carries the right `target_page_id`.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper.crawler import PersistRequest
from matrx_scraper.events import LinkEntry, PageSummary
from matrx_scraper.utils.url import url_hash
from matrx_scraper.web_crawl import persistence as P
from matrx_scraper.web_crawl.url_identity import CrawlIdentityResolution

SITE_ID = "d0aff5b6-0710-4848-8304-164db3c80ab7"
ORG_ID = "00000000-0000-4000-8000-0000000fffa1"
USER_ID = "00000000-0000-4000-8000-0000000fffe1"
PAGE_ID = "22913054-1933-44b8-ba94-f592f362b8c1"
KNOWN_CANONICAL = "33913054-1933-44b8-ba94-f592f362b8c2"


class Ledger:
    def __init__(self) -> None:
        self.statements: list[str] = []
        self.in_tx = False
        self.edges: list[dict[str, Any]] = []


def _install_fakes(monkeypatch: pytest.MonkeyPatch, ledger: Ledger, known_urls: set[str]) -> None:
    known_hashes = {url_hash(P._normalise_url(u)) for u in known_urls}

    def stmt(name: str) -> None:
        assert ledger.in_tx, f"{name} ran outside the transaction"
        ledger.statements.append(name)

    @asynccontextmanager
    async def fake_transaction(_db: str):
        ledger.in_tx = True
        try:
            yield
        finally:
            ledger.in_tx = False

    class FakeQuery:
        def __init__(self, kwargs: dict[str, Any]) -> None:
            self.kwargs = kwargs

        async def values(self, *_fields: str) -> list[dict[str, Any]]:
            stmt("WebPage.filter")
            return [
                {"url_hash": h, "canonical_page_id": KNOWN_CANONICAL}
                for h in self.kwargs["url_hash__in"]
                if h in known_hashes
            ]

    class FakeWebPage:
        @staticmethod
        async def get_or_none(**kwargs: Any) -> Any:
            stmt("WebPage.get_or_none")
            if kwargs.get("id") == PAGE_ID:
                return SimpleNamespace(id=PAGE_ID, deleted_at=None, canonical_page_id=PAGE_ID)
            digest = kwargs.get("url_hash")
            if digest in known_hashes:
                return SimpleNamespace(id=KNOWN_CANONICAL, canonical_page_id=KNOWN_CANONICAL)
            return None

        @staticmethod
        def filter(**kwargs: Any) -> FakeQuery:
            return FakeQuery(kwargs)

        @staticmethod
        async def update_where(*_a: Any, **_k: Any) -> int:
            stmt("WebPage.update_where")
            return 1

    class FakeSnapshot:
        @staticmethod
        async def create(**_k: Any) -> Any:
            stmt("WebSnapshot.create")
            return SimpleNamespace(id="44913054-1933-44b8-ba94-f592f362b8c3")

    class FakeEdge:
        @staticmethod
        async def create(**kwargs: Any) -> Any:
            stmt("WebLinkEdge.create")
            ledger.edges.append(kwargs)
            return SimpleNamespace(id="e")

        @staticmethod
        async def bulk_create(rows: list[dict[str, Any]], **_k: Any) -> list[Any]:
            stmt("WebLinkEdge.bulk_create")
            ledger.edges.extend(rows)
            return [{"id": "e"} for _ in rows]

    class FakeCrawlUrl:
        @staticmethod
        async def create(**_k: Any) -> Any:
            stmt("WebCrawlUrl.create")
            return SimpleNamespace(id="55913054-1933-44b8-ba94-f592f362b8c4", outcome="captured")

    async def fake_evidence(*_a: Any, **_k: Any) -> None:
        stmt("page_evidence")

    class FakeFileService:
        def __init__(self, file_manager: object) -> None:
            self.file_manager = file_manager

    monkeypatch.setattr(P, "FileService", FakeFileService)
    monkeypatch.setattr(P, "transaction", fake_transaction)
    monkeypatch.setattr(P, "WebPage", FakeWebPage)
    monkeypatch.setattr(P, "WebSnapshot", FakeSnapshot)
    monkeypatch.setattr(P, "WebLinkEdge", FakeEdge)
    monkeypatch.setattr(P, "WebCrawlUrl", FakeCrawlUrl)
    monkeypatch.setattr(
        P.WebCrawlRepository, "_record_page_evidence_in_active_transaction", fake_evidence
    )


def _persister() -> P.CanonicalBodyPersister:
    state = P.CrawlPersistenceState(
        site_id=SITE_ID,
        session_id="2b262f8c-1fbe-4575-81f5-c99c0709bd61",
        user_id=USER_ID,
        file_owner_id=USER_ID,
        organization_id=ORG_ID,
        coverage_qualified=False,
    )
    return P.CanonicalBodyPersister(
        P.WebCrawlRepository({"sub": USER_ID, "role": "authenticated"}),
        state,
        file_manager=SimpleNamespace(),  # type: ignore[arg-type]
    )


def _links(count: int) -> list[LinkEntry]:
    links: list[LinkEntry] = []
    for i in range(count):
        if i % 2:
            links.append(LinkEntry(target_url=f"https://other.example/{i}", link_type="external"))
        else:
            links.append(LinkEntry(target_url=f"https://acme.example/p{i}", link_type="internal"))
    return links


async def _run(monkeypatch: pytest.MonkeyPatch, link_count: int) -> Ledger:
    ledger = Ledger()
    _install_fakes(monkeypatch, ledger, known_urls={"https://acme.example/p0"})
    persister = _persister()
    url = "https://acme.example/page"
    summary = PageSummary(
        url=url, final_url=url, http_status=200, mime_type="html", links=_links(link_count)
    )
    await persister._persist_rows(
        request=PersistRequest(
            run_id=persister.state.session_id,
            url=url,
            final_url=url,
            body="<html></html>",
            markdown=None,
            mime_type="text/html",
            page_summary=summary,
        ),
        identity=CrawlIdentityResolution(
            requested_url=url,
            final_url=url,
            canonical_url=url,
            page_id=PAGE_ID,
            canonical_was_new=False,
        ),
        normalized=url,
        digest=url_hash(url),
        body_artifact=None,
        markdown_artifact=None,
        artifact_hashes={"body_sha256": "x"},
        reused_from_snapshot_id=None,
        screenshot_artifacts=[],
    )
    return ledger


@pytest.mark.asyncio
async def test_statement_count_does_not_grow_with_links(monkeypatch: pytest.MonkeyPatch) -> None:
    few = await _run(monkeypatch, 4)
    many = await _run(monkeypatch, 400)
    assert len(many.statements) == len(few.statements), (
        f"4 links -> {len(few.statements)} statements, 400 links -> "
        f"{len(many.statements)}: the write transaction scales with links"
    )
    assert len(many.statements) <= 10, many.statements


@pytest.mark.asyncio
async def test_every_edge_lands_with_the_right_target(monkeypatch: pytest.MonkeyPatch) -> None:
    ledger = await _run(monkeypatch, 6)
    assert [e["position"] for e in ledger.edges] == list(range(6))
    by_url = {e["target_url"]: e for e in ledger.edges}
    known = by_url[P._normalise_url("https://acme.example/p0")]
    assert known["target_page_id"] == KNOWN_CANONICAL and known["is_internal"] is True
    unknown = by_url[P._normalise_url("https://acme.example/p2")]
    assert unknown["target_page_id"] is None and unknown["is_internal"] is True
    external = by_url[P._normalise_url("https://other.example/1")]
    assert external["target_page_id"] is None and external["is_internal"] is False
    assert all(e["source_page_id"] == PAGE_ID for e in ledger.edges)
