from __future__ import annotations

import contextlib
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import httpx
import pytest

from matrx_scraper.sitemaps import (
    crawl_sitemap_documents,
    parse_sitemap_document,
)
from matrx_scraper.web_crawl.sitemap_sync import sync_site_sitemaps


def _response(url: str, status: int, body: str = "") -> httpx.Response:
    return httpx.Response(
        status,
        content=body.encode(),
        request=httpx.Request("GET", url),
    )


class _FakeClient:
    async def __aenter__(self) -> _FakeClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        return None


def _wire_responses(
    monkeypatch: pytest.MonkeyPatch,
    responses: dict[str, httpx.Response],
) -> AsyncMock:
    monkeypatch.setattr(
        "matrx_scraper.sitemaps.httpx.AsyncClient",
        lambda **kwargs: _FakeClient(),
    )

    def _lookup(client: object, url: str) -> tuple[str, httpx.Response]:
        if url not in responses:
            return url, _response(url, 404)
        return url, responses[url]

    safe_get = AsyncMock(side_effect=_lookup)
    monkeypatch.setattr("matrx_scraper.sitemaps._safe_get", safe_get)
    return safe_get


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def test_parse_urlset_extracts_typed_entry_fields() -> None:
    parsed = parse_sitemap_document(
        b"""<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
          <url>
            <loc>https://acme.example/a</loc>
            <lastmod>2026-07-01T12:30:00Z</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
          </url>
          <url><loc>https://acme.example/b</loc><lastmod>2026-07-02</lastmod></url>
        </urlset>"""
    )
    assert parsed.kind == "urlset"
    assert [entry.loc for entry in parsed.entries] == [
        "https://acme.example/a",
        "https://acme.example/b",
    ]
    first, second = parsed.entries
    assert first.lastmod is not None and first.lastmod.year == 2026
    assert first.changefreq == "weekly"
    assert first.priority == 0.8
    assert second.lastmod is not None and second.lastmod.tzinfo is not None
    assert second.changefreq is None and second.priority is None


def test_parse_sitemapindex_returns_child_locations() -> None:
    parsed = parse_sitemap_document(
        b"""<sitemapindex>
          <sitemap><loc>https://acme.example/child-1.xml</loc></sitemap>
          <sitemap><loc>https://acme.example/child-2.xml</loc></sitemap>
        </sitemapindex>"""
    )
    assert parsed.kind == "sitemapindex"
    assert parsed.child_locs == [
        "https://acme.example/child-1.xml",
        "https://acme.example/child-2.xml",
    ]
    assert parsed.entries == []


def test_parse_cosmetic_fields_degrade_to_none_never_raise() -> None:
    parsed = parse_sitemap_document(
        b"""<urlset>
          <url>
            <loc>https://acme.example/a</loc>
            <lastmod>not-a-date</lastmod>
            <priority>banana</priority>
          </url>
        </urlset>"""
    )
    entry = parsed.entries[0]
    assert entry.lastmod is None
    assert entry.priority is None


def test_parse_malformed_xml_raises_value_error() -> None:
    with pytest.raises(ValueError, match="malformed sitemap XML"):
        parse_sitemap_document(b"<urlset><url><loc>https://a.example/x")


def test_parse_non_sitemap_root_raises_value_error() -> None:
    with pytest.raises(ValueError, match="unsupported sitemap root"):
        parse_sitemap_document(b"<html><body>nope</body></html>")


# ---------------------------------------------------------------------------
# Bounded crawl
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_crawl_expands_indexes_recursively_within_depth_bound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    origin = "https://acme.example"
    responses = {
        f"{origin}/robots.txt": _response(f"{origin}/robots.txt", 200, "Sitemap: /custom.xml\n"),
        f"{origin}/sitemap.xml": _response(
            f"{origin}/sitemap.xml",
            200,
            """<sitemapindex>
              <sitemap><loc>https://acme.example/level-1.xml</loc></sitemap>
            </sitemapindex>""",
        ),
        f"{origin}/level-1.xml": _response(
            f"{origin}/level-1.xml",
            200,
            """<sitemapindex>
              <sitemap><loc>https://acme.example/level-2.xml</loc></sitemap>
            </sitemapindex>""",
        ),
        f"{origin}/level-2.xml": _response(
            f"{origin}/level-2.xml",
            200,
            """<sitemapindex>
              <sitemap><loc>https://acme.example/too-deep.xml</loc></sitemap>
            </sitemapindex>""",
        ),
        f"{origin}/custom.xml": _response(
            f"{origin}/custom.xml",
            200,
            "<urlset><url><loc>https://acme.example/custom</loc></url></urlset>",
        ),
    }
    safe_get = _wire_responses(monkeypatch, responses)

    crawl = await crawl_sitemap_documents(f"{origin}/", max_depth=2)

    fetched = {call.args[1] for call in safe_get.await_args_list}
    assert f"{origin}/level-2.xml" in fetched
    assert f"{origin}/too-deep.xml" not in fetched
    assert crawl.truncated is True
    assert any("depth limit" in reason for reason in crawl.truncation_reasons)
    kinds = {doc.url: doc.kind for doc in crawl.documents}
    assert kinds[f"{origin}/sitemap.xml"] == "sitemapindex"
    assert kinds[f"{origin}/custom.xml"] == "urlset"
    parents = {doc.url: doc.parent_url for doc in crawl.documents}
    assert parents[f"{origin}/level-1.xml"] == f"{origin}/sitemap.xml"
    assert parents[f"{origin}/level-2.xml"] == f"{origin}/level-1.xml"
    assert parents[f"{origin}/custom.xml"] is None


@pytest.mark.asyncio
async def test_crawl_enforces_document_count_bound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    origin = "https://acme.example"
    children = "".join(
        f"<sitemap><loc>https://acme.example/child-{i}.xml</loc></sitemap>" for i in range(10)
    )
    responses = {
        f"{origin}/sitemap.xml": _response(
            f"{origin}/sitemap.xml", 200, f"<sitemapindex>{children}</sitemapindex>"
        ),
    }
    for i in range(10):
        responses[f"{origin}/child-{i}.xml"] = _response(
            f"{origin}/child-{i}.xml",
            200,
            f"<urlset><url><loc>https://acme.example/p{i}</loc></url></urlset>",
        )
    _wire_responses(monkeypatch, responses)

    crawl = await crawl_sitemap_documents(f"{origin}/", max_docs=4)

    assert crawl.truncated is True
    assert any("document limit" in reason for reason in crawl.truncation_reasons)
    assert len(crawl.documents) <= 4


@pytest.mark.asyncio
async def test_crawl_enforces_url_bound_and_flags_truncation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    origin = "https://acme.example"
    urls = "".join(f"<url><loc>https://acme.example/p{i}</loc></url>" for i in range(20))
    responses = {
        f"{origin}/sitemap.xml": _response(
            f"{origin}/sitemap.xml", 200, f"<urlset>{urls}</urlset>"
        ),
    }
    _wire_responses(monkeypatch, responses)

    crawl = await crawl_sitemap_documents(f"{origin}/", max_urls=5)

    assert crawl.truncated is True
    assert any("URL limit" in reason for reason in crawl.truncation_reasons)
    assert crawl.url_total == 5
    assert crawl.documents[0].url_count == 5


@pytest.mark.asyncio
async def test_crawl_records_malformed_document_loudly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    origin = "https://acme.example"
    responses = {
        f"{origin}/sitemap.xml": _response(
            f"{origin}/sitemap.xml", 200, "<urlset><url><loc>broken"
        ),
    }
    _wire_responses(monkeypatch, responses)

    crawl = await crawl_sitemap_documents(f"{origin}/")

    failed = [doc for doc in crawl.documents if doc.fetch_error]
    assert len(failed) == 1
    assert failed[0].kind == "unknown"
    assert "malformed sitemap XML" in failed[0].fetch_error
    assert crawl.errors


@pytest.mark.asyncio
async def test_crawl_treats_missing_sitemaps_as_absent_not_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    origin = "https://acme.example"
    _wire_responses(monkeypatch, {})

    crawl = await crawl_sitemap_documents(f"{origin}/")

    assert crawl.documents == []
    assert crawl.errors == []
    assert crawl.truncated is False


# ---------------------------------------------------------------------------
# DB sync (model methods mocked; verifies upsert contracts + provenance rules)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_sync_upserts_sitemaps_pages_and_memberships(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    origin = "https://acme.example"
    responses = {
        f"{origin}/sitemap.xml": _response(
            f"{origin}/sitemap.xml",
            200,
            """<sitemapindex>
              <sitemap><loc>https://acme.example/pages.xml</loc></sitemap>
            </sitemapindex>""",
        ),
        f"{origin}/pages.xml": _response(
            f"{origin}/pages.xml",
            200,
            """<urlset>
              <url>
                <loc>https://acme.example/a</loc>
                <lastmod>2026-07-01</lastmod>
                <changefreq>daily</changefreq>
                <priority>0.9</priority>
              </url>
              <url><loc>https://acme.example/a</loc></url>
              <url><loc>https://acme.example/b</loc></url>
              <url><loc>mailto:not-a-page@acme.example</loc></url>
            </urlset>""",
        ),
    }
    _wire_responses(monkeypatch, responses)

    @contextlib.asynccontextmanager
    async def fake_transaction(_db: str):
        yield None

    monkeypatch.setattr("matrx_scraper.web_crawl.sitemap_sync.transaction", fake_transaction)

    sitemap_upserts: list[tuple[dict, dict]] = []

    async def fake_sitemap_upsert(data, **kwargs):
        sitemap_upserts.append((data, kwargs))
        return SimpleNamespace(id=uuid4(), fetch_error=None, deleted_at=None)

    sitemap_update_where = AsyncMock()
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebSitemap.upsert",
        fake_sitemap_upsert,
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebSitemap.update_where",
        sitemap_update_where,
    )

    page_matches: list[dict] = []

    async def fake_page_matcher(**kwargs):
        page_matches.append(kwargs)
        return {
            url: SimpleNamespace(canonical_page_id=f"page-{index}")
            for index, url in enumerate(kwargs["urls"])
        }

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.upsert_observed_page_urls",
        fake_page_matcher,
    )

    membership_upserts: list[tuple[list[dict], dict]] = []

    async def fake_membership_bulk_upsert(rows, **kwargs):
        membership_upserts.append((rows, kwargs))
        return [SimpleNamespace(id=uuid4(), deleted_at=None) for _ in rows]

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebPageSitemap.bulk_upsert",
        fake_membership_bulk_upsert,
    )

    result = await sync_site_sitemaps(
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        root_url=f"{origin}/",
    )

    # Sitemap rows: index + child, child linked to parent, arbiter (site_id, url).
    assert len(sitemap_upserts) == 2
    for data, kwargs in sitemap_upserts:
        assert kwargs["on_conflict"] == ["site_id", "url"]
    index_data = sitemap_upserts[0][0]
    child_data = sitemap_upserts[1][0]
    assert index_data["kind"] == "sitemapindex"
    assert index_data["parent_sitemap_id"] is None
    assert child_data["kind"] == "urlset"
    assert child_data["parent_sitemap_id"] is not None

    # Pages: deduped (a, b) and delegated to the one canonical matcher.
    assert len(page_matches) == 1
    matched = page_matches[0]
    assert matched["site_id"] == "site-1"
    assert matched["provenance"] == "sitemap"
    assert set(matched["urls"]) == {
        "https://acme.example/a",
        "https://acme.example/b",
    }

    # Memberships: one per (page, sitemap) with lastmod/changefreq/priority.
    assert len(membership_upserts) == 1
    member_rows, member_kwargs = membership_upserts[0]
    assert member_kwargs["on_conflict"] == ["page_id", "sitemap_id"]
    assert member_kwargs["update_fields"] == [
        "lastmod",
        "changefreq",
        "priority",
        "last_seen",
    ]
    assert len(member_rows) == 2
    by_priority = {row["priority"] for row in member_rows}
    assert 0.9 in by_priority

    assert result.summary.found == 2
    assert result.summary.urls == 4  # raw urlset entry count (pre-dedupe)
    assert result.summary.pages_upserted == 2
    assert result.summary.truncated is False
    # The mailto entry is skipped loudly.
    assert any("could not be corrected" in error for error in result.errors)


@pytest.mark.asyncio
async def test_sync_reports_truncation_in_summary_and_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    origin = "https://acme.example"
    urls = "".join(f"<url><loc>https://acme.example/p{i}</loc></url>" for i in range(10))
    responses = {
        f"{origin}/sitemap.xml": _response(
            f"{origin}/sitemap.xml", 200, f"<urlset>{urls}</urlset>"
        ),
    }
    _wire_responses(monkeypatch, responses)

    @contextlib.asynccontextmanager
    async def fake_transaction(_db: str):
        yield None

    monkeypatch.setattr("matrx_scraper.web_crawl.sitemap_sync.transaction", fake_transaction)

    async def fake_sitemap_upsert(data, **kwargs):
        return SimpleNamespace(id=uuid4(), fetch_error=None, deleted_at=None)

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebSitemap.upsert",
        fake_sitemap_upsert,
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebSitemap.update_where",
        AsyncMock(),
    )

    async def fake_bulk_upsert(rows, **kwargs):
        return [SimpleNamespace(id=uuid4(), deleted_at=None) for _ in rows]

    async def fake_page_matcher(**kwargs):
        return {
            url: SimpleNamespace(canonical_page_id=f"page-{index}")
            for index, url in enumerate(kwargs["urls"])
        }

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.upsert_observed_page_urls",
        fake_page_matcher,
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebPageSitemap.bulk_upsert",
        fake_bulk_upsert,
    )

    result = await sync_site_sitemaps(
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        root_url=f"{origin}/",
        max_urls=3,
    )

    assert result.summary.truncated is True
    assert result.summary.urls == 3
    assert result.summary.pages_upserted == 3
    assert any("URL limit" in error for error in result.errors)


@pytest.mark.asyncio
async def test_two_urls_resolving_to_one_page_upsert_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Two DISTINCT sitemap URLs can resolve to ONE canonical page.

    Sending both memberships in a single INSERT ... ON CONFLICT DO UPDATE is a
    hard Postgres CardinalityViolationError ("cannot affect row a second
    time") that killed the whole sync for datadestruction.com. The batch must
    carry the conflict key at most once.
    """
    origin = "https://acme.example"
    responses = {
        f"{origin}/sitemap.xml": _response(
            f"{origin}/sitemap.xml",
            200,
            """<urlset>
                <url><loc>https://acme.example/a</loc><priority>0.5</priority></url>
                <url><loc>https://acme.example/b</loc><priority>0.9</priority></url>
            </urlset>""",
        ),
    }
    _wire_responses(monkeypatch, responses)

    @contextlib.asynccontextmanager
    async def fake_transaction(_db: str):
        yield None

    monkeypatch.setattr("matrx_scraper.web_crawl.sitemap_sync.transaction", fake_transaction)

    async def fake_sitemap_upsert(data, **kwargs):
        return SimpleNamespace(id=uuid4(), fetch_error=None, deleted_at=None)

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebSitemap.upsert",
        fake_sitemap_upsert,
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebSitemap.update_where",
        AsyncMock(),
    )

    # Both observed URLs collapse onto ONE canonical page — exactly what the
    # real identity matcher does for an alias / trailing-slash pair.
    async def fake_page_matcher(**kwargs):
        return {url: SimpleNamespace(canonical_page_id="page-shared") for url in kwargs["urls"]}

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.upsert_observed_page_urls",
        fake_page_matcher,
    )

    membership_upserts: list[list[dict]] = []

    async def fake_membership_bulk_upsert(rows, **kwargs):
        keys = [(row["page_id"], row["sitemap_id"]) for row in rows]
        # This is what Postgres enforces — a duplicate key inside one
        # statement raises CardinalityViolationError.
        assert len(keys) == len(set(keys)), f"duplicate conflict keys: {keys}"
        membership_upserts.append(rows)
        return [SimpleNamespace(id=uuid4(), deleted_at=None) for _ in rows]

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebPageSitemap.bulk_upsert",
        fake_membership_bulk_upsert,
    )

    result = await sync_site_sitemaps(
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        root_url=f"{origin}/",
    )

    assert len(membership_upserts) == 1
    rows = membership_upserts[0]
    assert len(rows) == 1
    # Forcing check: the collapse is real work, not a vacuous assertion — with
    # the de-duplication disabled the same input produces the duplicate key
    # Postgres rejects.
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.dedupe_upsert_rows",
        lambda rows, **kwargs: list(rows),
    )
    with pytest.raises(AssertionError, match="duplicate conflict keys"):
        await sync_site_sitemaps(
            site_id="site-1",
            organization_id="org-1",
            user_id="user-1",
            root_url=f"{origin}/",
        )
    # Last occurrence wins — identical to what the statement itself would do.
    assert rows[0]["priority"] == 0.9
    assert rows[0]["page_id"] == "page-shared"
    # Both observed URLs still resolved — only the membership write collapsed.
    assert result.summary.pages_upserted == 2


@pytest.mark.asyncio
async def test_resync_revives_soft_deleted_sitemap_and_memberships(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A soft-deleted sitemap (or membership) that re-syncs EXISTS again —
    the upsert path must clear deleted_at, not refresh an invisible row."""
    origin = "https://acme.example"
    responses = {
        f"{origin}/sitemap.xml": _response(
            f"{origin}/sitemap.xml",
            200,
            "<urlset><url><loc>https://acme.example/a</loc></url></urlset>",
        ),
    }
    _wire_responses(monkeypatch, responses)

    @contextlib.asynccontextmanager
    async def fake_transaction(_db: str):
        yield None

    monkeypatch.setattr("matrx_scraper.web_crawl.sitemap_sync.transaction", fake_transaction)

    from datetime import UTC, datetime

    tombstone = datetime(2026, 1, 1, tzinfo=UTC)
    sitemap_row_id = uuid4()

    async def fake_sitemap_upsert(data, **kwargs):
        return SimpleNamespace(id=sitemap_row_id, fetch_error=None, deleted_at=tombstone)

    sitemap_update_where = AsyncMock()
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebSitemap.upsert",
        fake_sitemap_upsert,
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebSitemap.update_where",
        sitemap_update_where,
    )

    async def fake_page_matcher(**kwargs):
        return {
            url: SimpleNamespace(canonical_page_id=f"page-{index}")
            for index, url in enumerate(kwargs["urls"])
        }

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.upsert_observed_page_urls",
        fake_page_matcher,
    )

    membership_row_id = uuid4()

    async def fake_membership_bulk_upsert(rows, **kwargs):
        return [SimpleNamespace(id=membership_row_id, deleted_at=tombstone) for _ in rows]

    membership_update_where = AsyncMock()
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebPageSitemap.bulk_upsert",
        fake_membership_bulk_upsert,
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.sitemap_sync.WebPageSitemap.update_where",
        membership_update_where,
    )

    await sync_site_sitemaps(
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        root_url=f"{origin}/",
    )

    # The soft-deleted sitemap row was revived.
    revives = [
        call
        for call in sitemap_update_where.await_args_list
        if call.kwargs.get("deleted_at", "sentinel") is None
    ]
    assert revives and revives[0].args[0] == {"id": str(sitemap_row_id)}
    # The soft-deleted membership row was revived too.
    assert membership_update_where.await_count == 1
    filters = membership_update_where.await_args.args[0]
    assert filters == {"id__in": [str(membership_row_id)]}
    assert membership_update_where.await_args.kwargs == {"deleted_at": None}


# ---------------------------------------------------------------------------
# <loc> normalization — ONE gate: validate/correct, then normalize
# ---------------------------------------------------------------------------


def test_scheme_less_loc_is_corrected_not_mangled() -> None:
    """`normalize_url` assumes a schemed URL; a scheme-less sitemap `<loc>`
    (a routinely-seen malformation) must be CORRECTED to https first — the
    same recovery the crawl seed path applies — never mangled or dropped."""
    from matrx_scraper.web_crawl.sitemap_sync import normalize_sitemap_loc

    assert normalize_sitemap_loc("www.example.com/pricing") == "https://www.example.com/pricing"
    assert normalize_sitemap_loc("example.com/pricing") == "https://example.com/pricing"


def test_unrecoverable_locs_return_none() -> None:
    from matrx_scraper.web_crawl.sitemap_sync import normalize_sitemap_loc

    assert normalize_sitemap_loc("javascript:void(0)") is None
    assert normalize_sitemap_loc("ftp://example.com/file") is None
    assert normalize_sitemap_loc("") is None
    # Internal/localhost targets are rejected, not ingested as pages.
    assert normalize_sitemap_loc("http://localhost/admin") is None
    assert normalize_sitemap_loc("http://10.0.0.1/panel") is None


def test_valid_locs_still_normalize_identically() -> None:
    from matrx_scraper.utils.url import normalize_url
    from matrx_scraper.web_crawl.sitemap_sync import normalize_sitemap_loc

    for loc in (
        "https://example.com/page",
        "https://example.com/page/",
        "http://www.example.com/a?b=1",
    ):
        assert normalize_sitemap_loc(loc) == normalize_url(loc)
