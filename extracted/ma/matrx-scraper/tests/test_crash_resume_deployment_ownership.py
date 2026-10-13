"""A crashed crawl is auto-resumed ONLY by the deployment that last ran it.

Every scraper deployment (production, dev, a laptop) reads the ONE database, so
every crash-resume sweep sees every crashed session. On 2026-10-12 the dev
deployment's sweep — on a 4-day-old build with no AIDREAM_URL — took over
production session 8beb27cd, its workers hung, and the crawl never finished.

The fix: each run lease records `deployment`, and the sweep's candidate query
only matches sessions whose last lease its own deployment held. An unnamed
process resumes nothing. These tests run the real claim + candidate query + sweep
against an in-memory `web.crawl_session` stand-in that evaluates the same filter
kwargs the ORM receives.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import timedelta
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper.web_crawl import persistence, service as service_mod
from matrx_scraper.web_crawl.persistence import (
    STALE_SESSION_ERROR,
    WebCrawlRepository,
    set_run_deployment,
)
from matrx_utils import utcnow


def _contains(doc: Any, sub: Any) -> bool:
    """Postgres `@>` for the dict/scalar shapes the query uses."""
    if isinstance(sub, dict):
        return isinstance(doc, dict) and all(k in doc and _contains(doc[k], v) for k, v in sub.items())
    return doc == sub


def _matches(row: SimpleNamespace, filters: dict[str, Any]) -> bool:
    for key, want in filters.items():
        field, _, op = key.partition("__")
        have = getattr(row, field, None)
        if op == "":
            ok = have == want
        elif op == "in":
            ok = have in want
        elif op == "isnull":
            ok = (have is None) is want
        elif op == "gte":
            ok = have is not None and have >= want
        elif op == "json_contains":
            ok = _contains(have, want)
        else:  # pragma: no cover — a new filter must be modelled here
            raise AssertionError(f"unmodelled filter {key}")
        if not ok:
            return False
    return True


class _Query:
    def __init__(self, rows: list[SimpleNamespace], filters: dict[str, Any]) -> None:
        self._rows = [r for r in rows if _matches(r, filters)]

    def order_by(self, *_a: Any) -> _Query:
        return self

    def limit(self, n: int) -> _Query:
        self._rows = self._rows[:n]
        return self

    async def all(self) -> list[SimpleNamespace]:
        return list(self._rows)


class _FakeSessionTable:
    rows: list[SimpleNamespace] = []

    @classmethod
    def filter(cls, **filters: Any) -> _Query:
        return _Query(cls.rows, filters)

    @classmethod
    async def get_or_none(cls, *, use_cache: bool = False, **filters: Any) -> SimpleNamespace | None:
        hits = [r for r in cls.rows if _matches(r, filters)]
        return hits[0] if hits else None

    @classmethod
    async def update_where(cls, filters: dict[str, Any], **updates: Any) -> SimpleNamespace:
        hits = [r for r in cls.rows if _matches(r, filters)]
        for row in hits:
            for k, v in updates.items():
                setattr(row, k, v)
            row.version = int(row.version or 0) + 1
        return SimpleNamespace(rows_affected=len(hits))


@asynccontextmanager
async def _no_transaction(_name: str):
    yield


def _crashed_session(session_id: str, lease: dict[str, Any] | None) -> SimpleNamespace:
    return SimpleNamespace(
        id=session_id,
        status="failed",
        error=STALE_SESSION_ERROR,
        deleted_at=None,
        finished_at=utcnow(),
        updated_at=utcnow(),
        version=1,
        metadata={"run_lease": lease} if lease is not None else {},
        scope={"mode": "full"},
        created_by="00000000-0000-0000-0000-000000000001",
        organization_id="00000000-0000-0000-0000-000000000002",
        site_id="00000000-0000-0000-0000-000000000003",
    )


@pytest.fixture
def table(monkeypatch: pytest.MonkeyPatch) -> type[_FakeSessionTable]:
    _FakeSessionTable.rows = []
    monkeypatch.setattr(persistence, "WebCrawlSession", _FakeSessionTable)
    monkeypatch.setattr(persistence, "transaction", _no_transaction)
    yield _FakeSessionTable
    set_run_deployment(None)


@pytest.mark.asyncio
async def test_a_claimed_run_lease_records_the_claiming_deployment(table) -> None:
    table.rows = [_crashed_session("s-prod", None)]
    set_run_deployment("production")

    await WebCrawlRepository({}).claim_run_lease("s-prod", is_resume=False)

    assert table.rows[0].metadata["run_lease"]["deployment"] == "production"


@pytest.mark.asyncio
async def test_the_sweep_only_sees_sessions_its_own_deployment_ran(table) -> None:
    table.rows = [
        _crashed_session("s-prod", {"owner": "a", "deployment": "production"}),
        _crashed_session("s-dev", {"owner": "b", "deployment": "development"}),
        _crashed_session("s-unnamed", {"owner": "c", "deployment": None}),
        _crashed_session("s-never-ran", None),
    ]

    async def ids(deployment: str) -> set[str]:
        rows = await WebCrawlRepository.list_crash_resumable_sessions(
            lookback=timedelta(hours=2), limit=10, deployment=deployment
        )
        return {r.id for r in rows}

    # A lease with no deployment name belongs to production (UNNAMED_RUN_OWNER).
    assert await ids("production") == {"s-prod", "s-unnamed", "s-never-ran"}
    assert await ids("development") == {"s-dev"}


@pytest.fixture
def sweep(table, monkeypatch):
    """A real `resume_crashed_sessions` whose prepare/run are recorded, not run."""
    resumed: list[str] = []

    async def fake_prepare(self, ctx, session_id):  # noqa: ANN001
        resumed.append(session_id)
        return SimpleNamespace(site_id="site")

    async def fake_run(self, emitter, prepared):  # noqa: ANN001
        return None

    @asynccontextmanager
    async def fake_ctx(*_a: Any, **_k: Any):
        yield SimpleNamespace(emitter=None)

    monkeypatch.setattr(service_mod.WebCrawlService, "prepare_resume", fake_prepare)
    monkeypatch.setattr(service_mod.WebCrawlService, "run_prepared", fake_run)
    monkeypatch.setattr(service_mod, "system_app_context", fake_ctx)
    svc = service_mod.WebCrawlService.__new__(service_mod.WebCrawlService)
    return svc, resumed


@pytest.mark.asyncio
async def test_a_crawl_claimed_by_the_old_build_stays_resumable_by_production(table, sweep) -> None:
    """Transition: a lease written before the deployment stamp existed has no
    `deployment` key. Production must still continue it; dev must not."""
    svc, resumed = sweep
    old_build_lease = {"owner": "a", "epoch": 1, "host": "old-container:7"}
    table.rows = [_crashed_session("in-flight-at-deploy", old_build_lease)]

    set_run_deployment("development")
    assert await svc.resume_crashed_sessions(limit=5) == 0
    assert resumed == []

    set_run_deployment("production")
    assert await svc.resume_crashed_sessions(limit=5) == 1
    assert resumed == ["in-flight-at-deploy"]


@pytest.mark.asyncio
async def test_dev_sweep_never_resumes_a_production_crawl(table, sweep) -> None:
    """The live 2026-10-12 incident, end to end through resume_crashed_sessions."""
    svc, resumed = sweep
    table.rows = [_crashed_session("8beb27cd", {"owner": "a", "deployment": "production"})]
    resumed.clear()

    set_run_deployment("development")
    assert await svc.resume_crashed_sessions(limit=5) == 0
    assert resumed == []

    set_run_deployment(None)
    assert await svc.resume_crashed_sessions(limit=5) == 0
    assert resumed == []

    set_run_deployment("production")
    assert await svc.resume_crashed_sessions(limit=5) == 1
    assert resumed == ["8beb27cd"]


def test_the_server_declares_its_deployment_from_config(monkeypatch) -> None:
    from matrx_scraper.server.config import ServerConfig

    monkeypatch.setenv("MATRX_SCRAPER_DEPLOYMENT", "development")
    assert ServerConfig.from_env().deployment == "development"
