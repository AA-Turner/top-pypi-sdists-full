"""Level 1: web_crawl.presets — crawl-preset CRUD + recrawl-config derivation.

The forcing function here is BEHAVIOUR, not call shape: every test asserts what
a user would observe (which config comes back, in what order, whether a use is
counted) rather than which ORM method was called. Mocked models — no live DB.

Two properties get the most attention because losing either is silent:

* the derivation ORDER — a rescrape that quietly falls back to defaults when
  the user pinned a preset would run a different crawl than the one requested;
* an unparseable stored config STAYS VISIBLE — it must never vanish from the
  list and must never be coerced into a crawl nobody configured.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import UTC, datetime

import pytest

from matrx_orm import OrderBy
from matrx_orm.core.expressions import Expression

from matrx_scraper.web_crawl import presets as P
from matrx_scraper.web_crawl.contracts import (
    CrawlPresetSaveRequest,
    CrawlStartRequest,
)

SITE = "11111111-1111-1111-1111-111111111111"
OTHER_SITE = "99999999-9999-9999-9999-999999999999"
PRESET = "22222222-2222-2222-2222-222222222222"
SESSION = "33333333-3333-3333-3333-333333333333"


class _Row:
    """A stand-in for a generated model instance."""

    def __init__(self, **kwargs):
        self.id = kwargs.pop("id", PRESET)
        self.site_id = kwargs.pop("site_id", SITE)
        self.name = kwargs.pop("name", "Nightly")
        self.description = kwargs.pop("description", None)
        self.config = kwargs.pop("config", {})
        self.last_used_at = kwargs.pop("last_used_at", None)
        self.use_count = kwargs.pop("use_count", 0)
        self.created_at = kwargs.pop("created_at", None)
        self.updated_at = kwargs.pop("updated_at", None)
        for key, value in kwargs.items():
            setattr(self, key, value)


class _QB:
    def __init__(self, rows, calls):
        self._rows = rows
        self._calls = calls

    def order_by(self, *terms):
        self._calls.append(("order_by", terms))
        return self

    def limit(self, n):
        self._calls.append(("limit", n))
        return self

    async def all(self, **kwargs):
        return self._rows


class _UpdateResult:
    def __init__(self, rows_affected: int):
        self.rows_affected = rows_affected


class _FakeModel:
    """Records writes and serves canned reads for one model class."""

    def __init__(self, *, rows=None, get_row=None, upsert_row=None, rows_affected=1):
        self.rows = rows or []
        self.get_row = get_row
        self.upsert_row = upsert_row
        self.rows_affected = rows_affected
        self.calls: list = []

    def filter(self, **kwargs):
        self.calls.append(("filter", kwargs))
        return _QB(self.rows, self.calls)

    async def get_or_none(self, **kwargs):
        self.calls.append(("get_or_none", kwargs))
        return self.get_row

    async def upsert(self, data, conflict_fields=None, update_fields=None):
        self.calls.append(
            ("upsert", data, tuple(conflict_fields or ()), tuple(update_fields or ()))
        )
        return self.upsert_row or _Row(**{k: v for k, v in data.items() if k != "deleted_at"})

    async def update_where(self, filters, **updates):
        self.calls.append(("update_where", filters, updates))
        return _UpdateResult(self.rows_affected)


class _FakeRepository:
    """Stands in for WebCrawlRepository — only the RLS seam matters here."""

    def __init__(self):
        self.rls_entered = 0

    @asynccontextmanager
    async def rls(self):
        self.rls_entered += 1
        yield


@pytest.fixture
def repo() -> _FakeRepository:
    return _FakeRepository()


def _presets(repo) -> P.CrawlPresetRepository:
    return P.CrawlPresetRepository(repo)


def _valid_config(**overrides) -> dict:
    return CrawlStartRequest(**overrides).model_dump(mode="json")


# ---------------------------------------------------------------------------
# Listing


@pytest.mark.asyncio
async def test_list_orders_recently_used_first_and_scopes_to_live_rows(monkeypatch, repo):
    model = _FakeModel(
        rows=[
            _Row(id="a", name="Recent", config=_valid_config(max_pages=10)),
            _Row(id="b", name="Never", config=_valid_config()),
        ]
    )
    monkeypatch.setattr(P, "WebCrawlPreset", model)

    records = await _presets(repo).list_for_site(SITE)

    assert [r.id for r in records] == ["a", "b"]
    assert records[0].config is not None and records[0].config.max_pages == 10
    # Soft-deleted presets must not surface, and the recency order is the DB's.
    assert ("filter", {"site_id": SITE, "deleted_at__isnull": True}) in model.calls
    order_terms = next(c[1] for c in model.calls if c[0] == "order_by")
    assert isinstance(order_terms[0], OrderBy)
    # Assert the SQL it renders, not its attribute names: NULLS LAST is what
    # keeps a never-used preset from jumping to the top of the list.
    assert order_terms[0].as_sql([]) == "last_used_at DESC NULLS LAST"
    assert order_terms[1] == "name"
    assert repo.rls_entered == 1


@pytest.mark.asyncio
async def test_unparseable_config_stays_visible_and_flagged(monkeypatch, repo):
    model = _FakeModel(rows=[_Row(id="a", name="Broken", config={"max_pages": -5})])
    monkeypatch.setattr(P, "WebCrawlPreset", model)

    (record,) = await _presets(repo).list_for_site(SITE)

    # It must NOT disappear, and it must NOT be silently coerced into a crawl.
    assert record.name == "Broken"
    assert record.config is None
    assert record.config_error
    assert record.raw_config == {"max_pages": -5}


# ---------------------------------------------------------------------------
# Save / touch / delete


@pytest.mark.asyncio
async def test_save_upserts_by_site_and_name_and_revives_a_deleted_preset(monkeypatch, repo):
    model = _FakeModel(upsert_row=_Row(name="Nightly", config=_valid_config(max_pages=42)))
    monkeypatch.setattr(P, "WebCrawlPreset", model)

    record = await _presets(repo).save(
        SITE,
        CrawlPresetSaveRequest(name="Nightly", config=CrawlStartRequest(max_pages=42)),
    )

    assert record.config is not None and record.config.max_pages == 42
    (_, data, conflict, update) = next(c for c in model.calls if c[0] == "upsert")
    assert conflict == ("site_id", "name")
    # Re-saving a name the user deleted must restore it, not fail on a unique
    # key they cannot see.
    assert "deleted_at" in update
    assert data["deleted_at"] is None
    assert data["site_id"] == SITE


@pytest.mark.asyncio
async def test_touch_bumps_the_counter_atomically(monkeypatch, repo):
    model = _FakeModel()
    monkeypatch.setattr(P, "WebCrawlPreset", model)

    await _presets(repo).touch(PRESET)

    (_, filters, updates) = next(c for c in model.calls if c[0] == "update_where")
    assert filters == {"id": PRESET, "deleted_at__isnull": True}
    assert updates["last_used_at"] is not None
    # A read-modify-write would lose an increment when two crawls start at
    # once; this must render as `use_count = use_count + 1` in one statement.
    bump = updates["use_count"]
    assert isinstance(bump, Expression)
    assert bump.field_name == "use_count"
    assert (bump.operator, bump.value) == ("+", 1)


@pytest.mark.asyncio
async def test_delete_is_soft_and_reports_when_nothing_matched(monkeypatch, repo):
    model = _FakeModel(rows_affected=0)
    monkeypatch.setattr(P, "WebCrawlPreset", model)

    assert await _presets(repo).delete(PRESET) is False

    (_, filters, updates) = next(c for c in model.calls if c[0] == "update_where")
    assert filters == {"id": PRESET, "deleted_at__isnull": True}
    assert updates["deleted_at"] is not None


# ---------------------------------------------------------------------------
# Recrawl derivation — the order is the contract


@pytest.mark.asyncio
async def test_named_preset_wins_and_reports_itself(monkeypatch, repo):
    model = _FakeModel(get_row=_Row(name="Nightly", config=_valid_config(max_pages=7)))
    monkeypatch.setattr(P, "WebCrawlPreset", model)

    resolved = await P.derive_recrawl_config(_presets(repo), SITE, preset_id=PRESET)

    assert resolved.source == "preset"
    assert resolved.preset_id == PRESET
    assert resolved.preset_name == "Nightly"
    assert resolved.config.max_pages == 7


@pytest.mark.asyncio
async def test_named_preset_from_another_site_is_refused(monkeypatch, repo):
    model = _FakeModel(get_row=_Row(site_id=OTHER_SITE, config=_valid_config()))
    monkeypatch.setattr(P, "WebCrawlPreset", model)

    with pytest.raises(PermissionError):
        await P.derive_recrawl_config(_presets(repo), SITE, preset_id=PRESET)


@pytest.mark.asyncio
async def test_named_preset_that_no_longer_validates_raises_rather_than_running_defaults(
    monkeypatch, repo
):
    model = _FakeModel(get_row=_Row(config={"max_pages": -5}))
    monkeypatch.setattr(P, "WebCrawlPreset", model)

    # Silently running a DIFFERENT crawl than the one named is the failure this
    # forbids; the user asked for that preset.
    with pytest.raises(ValueError):
        await P.derive_recrawl_config(_presets(repo), SITE, preset_id=PRESET)


@pytest.mark.asyncio
async def test_site_pinned_default_preset_is_used_when_none_is_named(monkeypatch, repo):
    site = _Row(id=SITE, settings={"crawl": {"default_preset_id": PRESET}})
    monkeypatch.setattr(P, "WebSite", _FakeModel(get_row=site))
    monkeypatch.setattr(
        P,
        "WebCrawlPreset",
        _FakeModel(get_row=_Row(name="Pinned", config=_valid_config(max_pages=11))),
    )

    resolved = await P.derive_recrawl_config(_presets(repo), SITE)

    assert resolved.source == "site_default_preset"
    assert resolved.preset_name == "Pinned"
    assert resolved.config.max_pages == 11


@pytest.mark.asyncio
async def test_a_deleted_pinned_preset_degrades_to_the_last_session(monkeypatch, repo):
    site = _Row(id=SITE, settings={"crawl": {"default_preset_id": PRESET}})
    monkeypatch.setattr(P, "WebSite", _FakeModel(get_row=site))
    monkeypatch.setattr(P, "WebCrawlPreset", _FakeModel(get_row=None))
    monkeypatch.setattr(
        P,
        "WebCrawlSession",
        _FakeModel(
            rows=[
                _Row(
                    id=SESSION,
                    scope={"mode": "full", "request": _valid_config(max_pages=33)},
                    created_at=datetime(2026, 8, 1, tzinfo=UTC),
                )
            ]
        ),
    )

    resolved = await P.derive_recrawl_config(_presets(repo), SITE)

    # A pinned preset someone deleted must not brick the button.
    assert resolved.source == "last_session"
    assert resolved.session_id == SESSION
    assert resolved.config.max_pages == 33


@pytest.mark.asyncio
async def test_non_crawl_sessions_are_skipped_when_looking_back(monkeypatch, repo):
    monkeypatch.setattr(P, "WebSite", _FakeModel(get_row=_Row(id=SITE, settings={})))
    monkeypatch.setattr(P, "WebCrawlPreset", _FakeModel(get_row=None))
    monkeypatch.setattr(
        P,
        "WebCrawlSession",
        _FakeModel(
            rows=[
                # A sitemap sync is not a crawl config anyone re-runs.
                _Row(id="s1", scope={"mode": "gsc_sync"}),
                _Row(id="s2", scope={"mode": "page_fetch", "request": _valid_config()}),
                _Row(id=SESSION, scope={"mode": "list", "request": _valid_config(max_pages=5)}),
            ]
        ),
    )

    resolved = await P.derive_recrawl_config(_presets(repo), SITE)

    assert resolved.source == "last_session"
    assert resolved.session_id == SESSION
    assert resolved.config.max_pages == 5


@pytest.mark.asyncio
async def test_a_session_request_that_no_longer_validates_is_skipped(monkeypatch, repo):
    monkeypatch.setattr(P, "WebSite", _FakeModel(get_row=_Row(id=SITE, settings={})))
    monkeypatch.setattr(P, "WebCrawlPreset", _FakeModel(get_row=None))
    monkeypatch.setattr(
        P,
        "WebCrawlSession",
        _FakeModel(
            rows=[
                _Row(id="stale", scope={"mode": "full", "request": {"max_pages": -1}}),
                _Row(id=SESSION, scope={"mode": "full", "request": _valid_config(max_pages=9)}),
            ]
        ),
    )

    resolved = await P.derive_recrawl_config(_presets(repo), SITE)

    assert resolved.session_id == SESSION
    assert resolved.config.max_pages == 9


@pytest.mark.asyncio
async def test_a_site_with_no_history_still_gets_a_runnable_config(monkeypatch, repo):
    monkeypatch.setattr(P, "WebSite", _FakeModel(get_row=_Row(id=SITE, settings={})))
    monkeypatch.setattr(P, "WebCrawlPreset", _FakeModel(get_row=None))
    monkeypatch.setattr(P, "WebCrawlSession", _FakeModel(rows=[]))

    resolved = await P.derive_recrawl_config(_presets(repo), SITE)

    # The button always has something to run — never a None the caller must
    # special-case.
    assert resolved.source == "defaults"
    assert resolved.config == CrawlStartRequest()


# ---------------------------------------------------------------------------
# Transport


def test_preset_and_rescrape_routes_are_mounted_with_the_right_verbs():
    """One-click rescrape must take NO required body.

    A rescrape route that demands a full `CrawlStartRequest` is the exact gap
    this closed: there would be no canonical one-click path at all.
    """

    from matrx_scraper.api.crawl_router import router

    mounted = {}
    for route in router.routes:
        mounted.setdefault(route.path, set()).update(route.methods)

    assert mounted.get("/crawler/sites/{site_id}/presets") == {"GET", "POST"}
    assert mounted.get("/crawler/sites/{site_id}/presets/{preset_id}") == {"DELETE"}
    assert mounted.get("/crawler/sites/{site_id}/recrawl-config") == {"GET"}
    assert mounted.get("/crawler/sites/{site_id}/rescrape") == {"POST"}

    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router)
    schema = app.openapi()["paths"]["/crawler/sites/{site_id}/rescrape"]["post"]
    assert not schema.get("requestBody", {}).get("required", False), schema.get("requestBody")
