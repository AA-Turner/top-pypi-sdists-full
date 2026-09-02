from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest
from matrx_scraper.utils.url import normalize_url, url_hash, url_match_key
from matrx_scraper.web_crawl.url_identity import (
    adopt_published_page_url,
    CrawlIdentityResolution,
    PageIdentityNode,
    ResolvedPageUrl,
    UrlRelation,
    build_canonical_identity_plan,
    resolve_crawl_page_identity,
)

NOW = datetime(2026, 7, 27, tzinfo=UTC)


def page(
    page_id: str,
    url: str,
    *,
    first_seen: datetime = NOW,
    latest_snapshot_id: str | None = None,
) -> PageIdentityNode:
    return PageIdentityNode(
        id=page_id,
        url=url,
        canonical_page_id=page_id,
        first_seen=first_seen,
        latest_snapshot_id=latest_snapshot_id,
    )


def relation(
    source: str,
    target: str,
    *,
    kind: str = "redirect",
    observed_at: datetime = NOW,
) -> UrlRelation:
    return UrlRelation(
        source_url=source,
        target_url=target,
        kind=kind,
        observed_at=observed_at,
    )


def test_url_normalization_and_match_key_keep_aliases_distinct() -> None:
    assert normalize_url("HTTP://WWW.Example.com/products/#fragment") == (
        "http://www.example.com/products"
    )
    assert url_match_key("http://www.example.com/products/") == url_match_key(
        "https://example.com/products"
    )
    assert normalize_url("http://www.example.com/products/") != normalize_url(
        "https://example.com/products"
    )


@pytest.mark.asyncio
async def test_fresh_observation_adopts_planned_page_with_valid_seen_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Adoption cannot transiently put first_seen after last_seen."""
    from types import SimpleNamespace

    from matrx_scraper.web_crawl.url_identity import upsert_observed_page_urls

    page_id = "11111111-1111-4111-8111-111111111111"
    planned_url = "https://customer.example/healthcare"
    planned = SimpleNamespace(
        id=page_id,
        url=planned_url,
        canonical_page_id=page_id,
        deleted_at=None,
        metadata={},
        status="planned",
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.url_identity._load_site_pages",
        AsyncMock(return_value=[planned]),
    )
    update_where = AsyncMock()
    monkeypatch.setattr("matrx_scraper.web_crawl.url_identity.WebPage.update_where", update_where)
    monkeypatch.setattr("matrx_scraper.web_crawl.url_identity.WebPage.bulk_upsert", AsyncMock())
    monkeypatch.setattr("matrx_scraper.web_crawl.url_identity.utcnow", lambda: NOW)

    await upsert_observed_page_urls(
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        urls=[planned_url],
        provenance="ga4",
    )

    adoption = next(call for call in update_where.await_args_list if call.kwargs.get("status") == "active")
    assert adoption.args[0] == {"id__in": [page_id], "status": "planned"}
    assert adoption.kwargs["first_seen"] == NOW
    assert adoption.kwargs["last_seen"] == NOW


@pytest.mark.asyncio
async def test_cms_publish_on_platform_route_adopts_planned_row_without_insert(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A /c/{site} publish moves the plan identity; it never mints row two."""
    from types import SimpleNamespace

    planned_id = "11111111-1111-4111-8111-111111111111"
    planned_url = "https://customer.example/about"
    live_url = "https://mymatrx.com/c/dev-website/about"
    planned = SimpleNamespace(
        id=planned_id,
        url=planned_url,
        canonical_page_id=planned_id,
        deleted_at=None,
        status="planned",
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.url_identity._load_site_pages",
        AsyncMock(return_value=[planned]),
    )
    update_item = AsyncMock(return_value=planned)
    monkeypatch.setattr("matrx_scraper.web_crawl.url_identity.WebPage.update_item", update_item)
    create = AsyncMock(side_effect=AssertionError("must not insert a second page"))
    monkeypatch.setattr("matrx_scraper.web_crawl.url_identity.ensure_planned_page_urls", create)

    result = await adopt_published_page_url(
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        live_url=live_url,
        planned_url=planned_url,
    )

    assert result == planned_id
    update_item.assert_awaited_once_with(
        planned_id,
        url=live_url,
        url_hash=url_hash(live_url),
        path="/c/dev-website/about",
        status="active",
    )
    create.assert_not_awaited()


def test_scheme_and_www_aliases_choose_https_root_host() -> None:
    pages = [
        page("http-www", "http://www.example.com/products"),
        page(
            "https-root",
            "https://example.com/products",
            first_seen=NOW + timedelta(days=1),
        ),
    ]

    plan = build_canonical_identity_plan(
        pages,
        [],
        root_url="https://example.com",
    )

    assert plan.canonical_by_page_id == {
        "http-www": "https-root",
        "https-root": "https-root",
    }


def test_redirect_chain_flattens_every_hop_to_final_page() -> None:
    pages = [
        page("a", "https://example.com/a"),
        page("b", "https://example.com/b"),
        page("c", "https://example.com/c"),
    ]
    relations = [
        relation("https://example.com/a", "https://example.com/b"),
        relation("https://example.com/b", "https://example.com/c"),
    ]

    plan = build_canonical_identity_plan(
        pages,
        relations,
        root_url="https://example.com",
    )

    assert set(plan.canonical_by_page_id.values()) == {"c"}


def test_declared_canonical_wins_after_redirect_chain() -> None:
    pages = [
        page("a", "https://example.com/a"),
        page("b", "https://example.com/b"),
        page("canonical", "https://example.com/preferred"),
    ]
    relations = [
        relation("https://example.com/a", "https://example.com/b"),
        relation(
            "https://example.com/b",
            "https://example.com/preferred",
            kind="canonical",
        ),
    ]

    plan = build_canonical_identity_plan(
        pages,
        relations,
        root_url="https://example.com",
    )

    assert set(plan.canonical_by_page_id.values()) == {"canonical"}


def test_newer_direct_observation_overrides_stale_redirect() -> None:
    pages = [
        page("a", "https://example.com/a"),
        page("b", "https://example.com/b"),
    ]
    relations = [
        relation(
            "https://example.com/a",
            "https://example.com/b",
            observed_at=NOW - timedelta(days=1),
        ),
        relation(
            "https://example.com/a",
            "https://example.com/a",
            kind="direct",
            observed_at=NOW,
        ),
    ]

    plan = build_canonical_identity_plan(
        pages,
        relations,
        root_url="https://example.com",
    )

    assert set(plan.canonical_by_page_id.values()) == {"a"}


def test_redirect_cycle_is_reported_and_resolved_deterministically() -> None:
    pages = [
        page("a", "https://example.com/a"),
        page("b", "https://example.com/b"),
    ]
    relations = [
        relation("https://example.com/a", "https://example.com/b"),
        relation("https://example.com/b", "https://example.com/a"),
    ]

    plan = build_canonical_identity_plan(
        pages,
        relations,
        root_url="https://example.com",
    )

    assert plan.cycle_count == 1
    assert set(plan.canonical_by_page_id.values()) == {"a"}


@pytest.mark.asyncio
async def test_crawl_identity_casts_last_seen_as_timestamptz(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requested_url = "https://example.com/old"
    final_url = "https://example.com/new"
    requested_page_id = "11111111-1111-4111-8111-111111111111"
    final_page_id = "22222222-2222-4222-8222-222222222222"

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.url_identity.WebPage.exists",
        AsyncMock(return_value=True),
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.url_identity.upsert_observed_page_urls",
        AsyncMock(
            return_value={
                requested_url: ResolvedPageUrl(
                    observed_url=requested_url,
                    observed_page_id=requested_page_id,
                    canonical_page_id=requested_page_id,
                    canonical_url=requested_url,
                ),
                final_url: ResolvedPageUrl(
                    observed_url=final_url,
                    observed_page_id=final_page_id,
                    canonical_page_id=final_page_id,
                    canonical_url=final_url,
                ),
            }
        ),
    )
    batch_update = AsyncMock(return_value=2)
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.url_identity.bulk_update_by_pk",
        batch_update,
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.url_identity.WebPage.update_where",
        AsyncMock(),
    )

    @asynccontextmanager
    async def fake_transaction(*_args: object, **_kwargs: object):
        yield

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.url_identity.transaction",
        fake_transaction,
    )

    result = await resolve_crawl_page_identity(
        site_id="33333333-3333-4333-8333-333333333333",
        organization_id="44444444-4444-4444-8444-444444444444",
        user_id="55555555-5555-4555-8555-555555555555",
        root_url="https://example.com",
        requested_url=requested_url,
        final_url=final_url,
        redirect_chain=[],
        declared_canonical_url=None,
    )

    assert isinstance(result, CrawlIdentityResolution)
    assert result.page_id == final_page_id
    assert batch_update.await_args.kwargs["casts"] == {
        "id": "uuid",
        "canonical_page_id": "uuid",
        "last_seen": "timestamptz",
    }


# ---------------------------------------------------------------------------
# Identity Contract — per-rule locks on THE canonical stored identity.
#
# `normalize_url` is the ONE canonicalizer (Identity Contract; feeds url_hash).
# These tests pin each rule it applies AND each rule it deliberately does NOT
# (so completing the spec is caught as a deliberate, migration-coupled change,
# never a silent hash shift). See utils/url.py::normalize_url.
# ---------------------------------------------------------------------------


class TestCanonicalIdentityRulesApplied:
    def test_scheme_and_host_are_lowercased(self):
        assert normalize_url("HTTPS://Example.COM/x") == "https://example.com/x"

    def test_path_case_is_preserved(self):
        # Paths are case-sensitive — must NOT be lowercased.
        assert normalize_url("https://example.com/A/b") == "https://example.com/A/b"

    def test_fragment_is_stripped(self):
        assert normalize_url("https://example.com/x#frag") == "https://example.com/x"

    def test_empty_path_becomes_root(self):
        assert normalize_url("https://example.com") == "https://example.com/"

    def test_trailing_slash_stripped_except_root(self):
        assert normalize_url("https://example.com/a/") == "https://example.com/a"
        assert normalize_url("https://example.com/") == "https://example.com/"

    def test_is_idempotent_for_schemed_input(self):
        once = normalize_url("HTTPS://Example.COM/a/?b=1#f")
        assert normalize_url(once) == once


class TestCanonicalIdentityRulesDeferred:
    """These currently pass THROUGH unchanged. Applying any of them re-hashes
    stored pages, so each is a deliberate migration-coupled decision. If one of
    these starts failing, someone changed the stored identity — that MUST ship
    with a re-hash migration, never alone."""

    def test_default_port_is_not_yet_removed(self):
        assert normalize_url("https://example.com:443/x") == "https://example.com:443/x"

    def test_tracking_params_are_not_yet_removed(self):
        assert (
            normalize_url("https://example.com/p?utm_source=x&id=5")
            == "https://example.com/p?utm_source=x&id=5"
        )

    def test_query_order_is_not_yet_normalized(self):
        assert normalize_url("https://example.com/a?b=2&a=1") == "https://example.com/a?b=2&a=1"

    def test_KNOWN_BUG_schemeless_input_is_mangled(self):
        # BUG: a scheme-less URL handed straight to the identity function comes out
        # malformed ("https:example.com/x" — no "//", host stuck in the path) because
        # urlparse reads it as a bare path. In practice ingestion sources supply
        # absolute URLs and the input-acceptance layer (url_utils.normalize_url) adds
        # the scheme first, so this rarely bites — but it is a real latent defect in
        # THE stored identity. Fixing it changes stored-identity output, so it ships
        # with the Identity-Contract-completion migration, never alone. This test
        # LOCKS the current (wrong) output so the fix is a deliberate, visible change.
        assert normalize_url("example.com/x") == "https:example.com/x"


class TestUrlMatchKeyIsADistinctLooserAlias:
    """url_match_key is NOT the identity — it's a scheme/www-insensitive alias
    matcher. It MUST collapse aliases the identity keeps distinct."""

    def test_www_and_scheme_collapse_only_in_the_match_key(self):
        a = "http://www.example.com/p"
        b = "https://example.com/p"
        assert normalize_url(a) != normalize_url(b)  # identity keeps them distinct
        assert url_match_key(a) == url_match_key(b)  # alias key collapses them


# ---------------------------------------------------------------------------
# Revive on re-observation — a soft-deleted page that is observed again exists
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_observed_url_revives_soft_deleted_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from types import SimpleNamespace

    from matrx_scraper.web_crawl.url_identity import upsert_observed_page_urls

    page_id = "11111111-1111-4111-8111-111111111111"
    url = "https://example.com/revived"
    tombstone = datetime(2026, 1, 1, tzinfo=UTC)
    page = SimpleNamespace(
        id=page_id,
        url=url,
        canonical_page_id=page_id,
        deleted_at=tombstone,
    )

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.url_identity._load_site_pages",
        AsyncMock(return_value=[page]),
    )
    update_where = AsyncMock()
    monkeypatch.setattr("matrx_scraper.web_crawl.url_identity.WebPage.update_where", update_where)
    monkeypatch.setattr("matrx_scraper.web_crawl.url_identity.WebPage.bulk_upsert", AsyncMock())

    @asynccontextmanager
    async def fake_transaction(*_args: object, **_kwargs: object):
        yield

    monkeypatch.setattr("matrx_scraper.web_crawl.url_identity.transaction", fake_transaction)

    resolutions = await upsert_observed_page_urls(
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        urls=[url],
        provenance="sitemap",
    )

    assert resolutions[url].canonical_page_id == page_id
    revive_calls = [
        call
        for call in update_where.await_args_list
        if call.kwargs.get("deleted_at", "sentinel") is None
    ]
    assert revive_calls, "soft-deleted page must be revived on re-observation"
    assert revive_calls[0].args[0] == {"id": page_id}
    # Dismissal memory: the revive permanently records the dismiss cycle.
    marker = revive_calls[0].kwargs["metadata"]["dismissals"][0]
    assert marker["dismissed_at"] == tombstone.isoformat()
    assert marker["revive_reason"] == "reobserved"
