"""A crawl started with ``X-Matrx-Test-Run`` declares ``app.test_run`` for EVERY write it causes.

``platform._stamp_test_run`` stamps a row only when the writing transaction opened with ``app.test_run``
— which matrx-orm emits from the session-context provider at every top-level BEGIN. So "is this row
stamped" is exactly "what does ``session_context_gucs()`` return at the moment of the write". This pins it
for the three legs a crawl writes on:

1. the request itself (the session row is inserted inside the request);
2. the async work the request starts — the streaming task and any ``detached_task`` it spawns for the
   crawl's OWN rows (``carry_test_run=True``), which begin with a FRESH context;
3. a continuation with NO request at all (resume / crash-resume sweep), which knows the run only from the
   stamp persisted on the session's scope.

And the other direction: no header, nothing declared, nothing stamped.
"""

from __future__ import annotations

import asyncio
import contextvars
from types import SimpleNamespace
from typing import Any

import httpx
import pytest
from matrx_orm import configure_session_context, session_context_gucs
from matrx_utils import detached_task
from matrx_utils.source_guard import stable_source
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from matrx_scraper.test_stamp import (
    HEADER,
    TEST_RUN_GUC,
    install_test_run_stamp,
    scope_test_run_id,
    stamp_scope,
)
from matrx_scraper.web_crawl.service import PreparedCrawl, WebCrawlService

RUN = "6f1c2d3e-4a5b-4c6d-8e7f-901234567890"


@pytest.fixture
def app_and_writes(monkeypatch: pytest.MonkeyPatch):
    """A scraper-shaped app: the request persists a session scope and starts the crawl detached."""
    writes: dict[str, dict[str, str]] = {}
    sessions: dict[str, dict[str, Any]] = {}
    done = asyncio.Event()

    async def fake_body(self, emitter, prepared) -> None:  # the real run's writes, observed
        writes["worker"] = session_context_gucs()

        async def tail() -> None:  # e.g. fire-and-forget post-crawl work on this crawl's own rows
            writes["worker_detached"] = session_context_gucs()
            done.set()

        detached_task(tail(), carry_test_run=True)

    monkeypatch.setattr(WebCrawlService, "_run_prepared", fake_body)

    async def start(request: Request) -> JSONResponse:
        scope = stamp_scope({"mode": "full"})
        writes["request"] = session_context_gucs()  # the session-row insert
        sessions["s1"] = scope
        prepared = PreparedCrawl(
            site_id="site", session_id="s1", root_url="https://example.com", request=None,  # type: ignore[arg-type]
            repository=None, state=None, broker=None, test_run_id=scope_test_run_id(scope),  # type: ignore[arg-type]
        )
        detached_task(WebCrawlService().run_prepared(SimpleNamespace(), prepared))
        return JSONResponse({"ok": True})

    app = Starlette(routes=[Route("/start", start, methods=["POST"])])
    install_test_run_stamp(app)
    yield app, writes, sessions, done
    configure_session_context(None)


async def _post(app, headers: dict[str, str]) -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://t") as client:
        assert (await client.post("/start", headers=headers)).status_code == 200


@pytest.mark.asyncio
async def test_a_test_crawl_declares_its_run_on_every_leg(app_and_writes) -> None:
    app, writes, sessions, done = app_and_writes
    await _post(app, {HEADER: RUN})
    await asyncio.wait_for(done.wait(), 2)
    assert writes["request"] == {TEST_RUN_GUC: RUN}
    assert writes["worker"] == {TEST_RUN_GUC: RUN}
    assert writes["worker_detached"] == {TEST_RUN_GUC: RUN}
    assert sessions["s1"]["test_run_id"] == RUN


@pytest.mark.asyncio
async def test_a_persons_crawl_declares_nothing(app_and_writes) -> None:
    app, writes, sessions, done = app_and_writes
    await _post(app, {})
    await asyncio.wait_for(done.wait(), 2)
    assert writes == {"request": {}, "worker": {}, "worker_detached": {}}
    assert "test_run_id" not in sessions["s1"]


@pytest.mark.asyncio
async def test_a_continuation_with_no_request_re_declares_the_persisted_stamp(app_and_writes) -> None:
    """Resume / crash-resume: no header, a fresh context — only the session's scope knows the run."""
    _app, writes, _sessions, done = app_and_writes
    prepared = PreparedCrawl(
        site_id="site", session_id="s1", root_url="https://example.com", request=None,  # type: ignore[arg-type]
        repository=None, state=None, broker=None,  # type: ignore[arg-type]
        test_run_id=scope_test_run_id({"mode": "full", "test_run_id": RUN}),
    )
    await asyncio.create_task(
        WebCrawlService().run_prepared(SimpleNamespace(), prepared), context=contextvars.Context()
    )
    await asyncio.wait_for(done.wait(), 2)
    assert writes["worker"] == {TEST_RUN_GUC: RUN}
    assert writes["worker_detached"] == {TEST_RUN_GUC: RUN}


def test_start_persists_and_resume_reads_the_stamp() -> None:
    """The real doors: prepare_start writes the stamp onto the session scope; prepare_resume reads it back."""
    start = stable_source(WebCrawlService.prepare_start)
    assert "stamp_scope(scope)" in start and "test_run_id=scope_test_run_id(scope)" in start
    assert "test_run_id=scope_test_run_id(" in stable_source(WebCrawlService.prepare_resume)
    assert "declared_test_run(prepared.test_run_id)" in stable_source(WebCrawlService.run_prepared)


def test_the_scraper_server_installs_the_stamp() -> None:
    from matrx_scraper.server.app import create_app

    assert "install_test_run_stamp(app)" in stable_source(create_app)


@pytest.mark.asyncio
async def test_a_persons_crawl_resumed_under_a_test_header_stays_unstamped(app_and_writes) -> None:
    """An ambient test run (header / detached carrier) must never leak into an UNSTAMPED session's rows."""
    from matrx_scraper.test_stamp import test_run_scope

    _app, writes, _sessions, done = app_and_writes
    prepared = PreparedCrawl(
        site_id="site", session_id="s1", root_url="https://example.com", request=None,  # type: ignore[arg-type]
        repository=None, state=None, broker=None,  # type: ignore[arg-type]
        test_run_id=scope_test_run_id({"mode": "full"}),
    )
    with test_run_scope(RUN):
        await WebCrawlService().run_prepared(SimpleNamespace(), prepared)
    await asyncio.wait_for(done.wait(), 2)
    assert writes["worker"] == {}
    assert writes["worker_detached"] == {}


@pytest.mark.asyncio
async def test_the_stamp_never_crosses_a_detached_hop_that_did_not_opt_in() -> None:
    """The carrier is opt-in (2026-10-28): a sweep or tail a test crawl triggers runs unstamped unless its
    spawner declares it writes the crawl's own rows — it may touch other people's sessions."""
    from matrx_scraper.test_stamp import test_run_gucs, test_run_scope

    configure_session_context(test_run_gucs)
    try:
        async def probe() -> dict[str, str]:
            return session_context_gucs()

        with test_run_scope(RUN):
            assert await detached_task(probe()) == {}
            assert await detached_task(probe(), carry_test_run=True) == {TEST_RUN_GUC: RUN}
    finally:
        configure_session_context(None)


class _Reaped(Exception):
    pass


@pytest.mark.asyncio
async def test_a_test_start_reaps_other_peoples_stale_sessions_unstamped(monkeypatch: pytest.MonkeyPatch) -> None:
    """``prepare_start`` reaps EVERYONE's stale sessions inline before claiming its lane. Under a baseline test
    header that UPDATE would claim them for cleanup, so it runs as no test run at all (review 2026-10-28)."""
    from matrx_scraper.test_stamp import current_test_run_id, test_run_scope
    from matrx_scraper.web_crawl import service as svc
    from matrx_scraper.web_crawl.contracts import CrawlStartRequest

    seen: list[str | None] = []

    async def reap() -> int:
        seen.append(current_test_run_id())
        raise _Reaped  # stop: the reap is this test's subject

    class _Repo:
        def __init__(self, *_a: Any) -> None: ...

        async def assert_site_editor(self, *_a: Any) -> None: ...

        async def site_root(self, *_a: Any) -> str:
            return "https://example.com"

        fail_stale_sessions = staticmethod(reap)

    s3 = SimpleNamespace(sync_engine=SimpleNamespace(_config=SimpleNamespace(storage_backend="s3")),
                         cloud=SimpleNamespace(is_configured=lambda _b: True))
    monkeypatch.setattr(svc, "has_ext", lambda _n: True)
    monkeypatch.setattr(svc, "get_ext", lambda _n: s3)
    monkeypatch.setattr(svc, "build_user_claims", lambda _c: {})
    monkeypatch.setattr(svc, "WebCrawlRepository", _Repo)

    async def ok_url(_u: str) -> None:
        return None

    monkeypatch.setattr(svc, "validate_public_http_url", ok_url)
    with test_run_scope(RUN):
        with pytest.raises(_Reaped):
            await WebCrawlService().prepare_start(SimpleNamespace(user_id="u"), "site", CrawlStartRequest())
        assert current_test_run_id() == RUN, "the request keeps its own stamp"
    assert seen == [None]
