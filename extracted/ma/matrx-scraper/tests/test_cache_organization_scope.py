"""The page cache is TENANT data: every write names its organization, every
read is filtered by it.

`scraper.scrape_parsed_page` is an org-scoped entity whose `organization_id` is
NOT NULL with no column default and no stamping trigger in the live database, so
a cache write that names no organization must REFUSE — not default, not guess,
not hand the choice to a trigger (`common-docs/policies/
context-is-carried-never-rebuilt.md` rule 4). And because the row is scoped, a
hit must belong to the SAME organization: serving one tenant another tenant's
scraped copy of a page is a cross-tenant read.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from matrx_scraper.cache import (
    CacheOrganizationRequired,
    MemoryCache,
    TwoTierCache,
    resolve_cache_organization_id,
)

ORG_A = "11111111-1111-1111-1111-111111111111"
ORG_B = "22222222-2222-2222-2222-222222222222"


class _Rows:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def limit(self, _n: int) -> _Rows:
        return self

    async def values(self, *_fields: str) -> list[dict[str, Any]]:
        return self._rows


class FakePage:
    """Records every L2 call the cache makes, and answers reads by filter."""

    def __init__(self) -> None:
        self.created: list[dict[str, Any]] = []
        self.updates: list[tuple[dict[str, Any], dict[str, Any]]] = []
        self.rows: list[dict[str, Any]] = []

    def filter(self, **kwargs: Any) -> _Rows:
        matched = [
            r
            for r in self.rows
            if r["page_name"] == kwargs["page_name"]
            and r["organization_id"] == kwargs["organization_id"]
        ]
        return _Rows(matched)

    async def update_where(self, where: dict[str, Any], **values: Any) -> None:
        self.updates.append((where, values))

    async def create(self, **values: Any) -> None:
        self.created.append(values)
        self.rows.append(values)


def _cache() -> tuple[TwoTierCache, FakePage]:
    cache = TwoTierCache()
    page = FakePage()
    cache._page = page
    return cache, page


def _row(page_name: str, organization_id: str) -> dict[str, Any]:
    now = datetime.now(UTC)
    return {
        "page_name": page_name,
        "organization_id": organization_id,
        "content": {"text": organization_id},
        "url": "https://example.com/a",
        "domain": "example.com",
        "scraped_at": now,
        "expires_at": now + timedelta(days=1),
        "content_type": "html",
        "char_count": 3,
        "validity": "active",
    }


async def _set(cache: TwoTierCache, key: str, **kwargs: Any) -> None:
    await cache.set(
        key=key,
        url="https://example.com/a",
        domain="example.com",
        content={"text": "hello"},
        content_type="html",
        char_count=5,
        **kwargs,
    )


@pytest.mark.asyncio
async def test_write_lands_the_explicit_organization() -> None:
    cache, page = _cache()

    await _set(cache, "example_com__a", organization_id=ORG_A)

    assert len(page.created) == 1
    assert page.created[0]["organization_id"] == ORG_A
    # The supersede of the previous active row is scoped to the same tenant —
    # otherwise one organization's re-scrape would mark another's row stale.
    assert page.updates[0][0]["organization_id"] == ORG_A


@pytest.mark.asyncio
async def test_write_without_an_organization_refuses_and_writes_nothing() -> None:
    cache, page = _cache()

    with pytest.raises(CacheOrganizationRequired) as exc:
        await _set(cache, "example_com__a")

    assert "organization" in str(exc.value)
    assert page.created == []
    assert page.updates == []
    # And nothing was cached in memory either, so a later read cannot answer
    # from a write that never happened.
    assert len(cache._memory) == 0


@pytest.mark.asyncio
async def test_write_takes_the_carried_context_when_no_argument_is_given() -> None:
    from matrx_utils.ctx import SimpleUserContext, clear_manual_context, set_manual_context

    cache, page = _cache()
    token = set_manual_context(SimpleUserContext(user_id="u", organization_id=ORG_B))
    try:
        await _set(cache, "example_com__a")
    finally:
        clear_manual_context(token)

    assert page.created[0]["organization_id"] == ORG_B


@pytest.mark.asyncio
async def test_read_is_scoped_to_the_same_organization() -> None:
    cache, page = _cache()
    page.rows.append(_row("example_com__a", ORG_A))

    assert await cache.get("example_com__a", organization_id=ORG_A) is not None
    # Another tenant asking for the same URL gets a MISS, not the first
    # tenant's scraped copy.
    assert await cache.get("example_com__a", organization_id=ORG_B) is None


@pytest.mark.asyncio
async def test_the_memory_tier_is_partitioned_too() -> None:
    cache, _page = _cache()

    await _set(cache, "example_com__a", organization_id=ORG_A)

    assert await cache.get("example_com__a", organization_id=ORG_A) is not None
    assert await cache.get("example_com__a", organization_id=ORG_B) is None


@pytest.mark.asyncio
async def test_read_without_an_organization_refuses() -> None:
    cache, _page = _cache()

    with pytest.raises(CacheOrganizationRequired):
        await cache.get("example_com__a")


@pytest.mark.asyncio
async def test_invalidate_is_scoped_and_refuses_without_an_organization() -> None:
    cache, page = _cache()

    await cache.invalidate("example_com__a", organization_id=ORG_A)
    assert page.updates[-1][0]["organization_id"] == ORG_A

    with pytest.raises(CacheOrganizationRequired):
        await cache.invalidate("example_com__a")


@pytest.mark.asyncio
async def test_memory_cache_partitions_by_organization_without_refusing() -> None:
    """The no-DB desktop lane has no tenancy at all, so MemoryCache keeps
    working — but it still never serves one organization another's entry."""
    cache = MemoryCache()

    await cache.set(
        key="example_com__a",
        url="https://example.com/a",
        domain="example.com",
        content={"text": "a"},
        content_type="html",
        char_count=1,
        organization_id=ORG_A,
    )

    assert await cache.get("example_com__a", organization_id=ORG_A) is not None
    assert await cache.get("example_com__a", organization_id=ORG_B) is None
    assert await cache.get("example_com__a") is None  # the org-less partition


def test_resolver_prefers_the_explicit_value_over_the_carried_one() -> None:
    from matrx_utils.ctx import SimpleUserContext, clear_manual_context, set_manual_context

    token = set_manual_context(SimpleUserContext(user_id="u", organization_id=ORG_B))
    try:
        assert resolve_cache_organization_id(ORG_A) == ORG_A
        assert resolve_cache_organization_id() == ORG_B
    finally:
        clear_manual_context(token)
