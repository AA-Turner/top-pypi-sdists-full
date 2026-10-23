# ruff: noqa: F811  (pytest fixtures imported from the sibling harness, then requested by name)
"""The crawler's resume door answers a LIVE crawl with the canonical rejoin 409 —
and a resume that dies after winning the claim hands the run back.

The rule (aidream services/runtime/FEATURE.md "Live-run refusal"): claim
atomically BEFORE any write; a door whose run is still live answers
``409 {code: "run_in_progress", live_request_id, rejoin_path}`` built by
``reconnect.run_in_progress_error`` so the client rejoins via
``POST /runtime/operations/{live_request_id}/rejoin``; a write that fails after the
claim hands the run back. Sibling suite: aidream/services/runtime/tests/
test_resume_rejoins_a_live_run.py.

SUT: ``POST /crawler/sessions/{id}/resume`` (``crawl_router.resume_crawl``) over the
REAL ``WebCrawlService.prepare_resume`` and the REAL ``claim_run_lease`` compare-and-
swap on an in-memory ``web.crawl_session`` row (harness: test_cancel_queued_session).
The runtime engine runs for real over ``InMemoryExecutionStore``.

Breaks named: a live crawl's resume answers a bare 409 naming nothing to rejoin; a
resume of a live crawl writes the row; two racing resumes both win; a resume whose
post-claim setup fails leaves the session ``running`` under a lease nobody holds.
"""

from __future__ import annotations

import importlib

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

pytest.importorskip("aidream")

from matrx_runtime import ExecutionEngine, InMemoryExecutionStore  # noqa: E402
from test_cancel_queued_session import (  # noqa: E402, F401  # pyright: ignore[reportMissingImports]
    FRESH_LEASE_AGE,
    ORG_ID,
    STALE_LEASE_AGE,
    USER_ID,
    _ctx,
    _session_row,
    _SessionTable,
    resume_worker,
    table,
)

from matrx_scraper._ext import configure_ext  # noqa: E402
from matrx_scraper.web_crawl.persistence import (  # noqa: E402
    STALE_SESSION_ERROR,
    WORKER_STOPPED_ERROR,
    WebCrawlRepository,
    utcnow,
)

crawl_router = importlib.import_module("matrx_scraper.api.crawl_router")  # the package re-exports the router object under this name
REAL_CLAIM = WebCrawlRepository.claim_run_lease
LIVE_REQUEST = "038ca293-2315-457b-9e32-9a95217d1c85"
LINK_KIND = "web_crawl_session"


@pytest.fixture
def engine(monkeypatch: pytest.MonkeyPatch) -> ExecutionEngine:
    eng = ExecutionEngine(InMemoryExecutionStore())
    monkeypatch.setattr("aidream.services.runtime.get_execution_engine", lambda: eng)
    monkeypatch.setattr("aidream.services.runtime.engine.get_execution_engine", lambda: eng)
    return eng


@pytest.fixture
def host_refusal() -> None:
    """The host wiring `package_integration._configure_matrx_scraper` performs."""
    from aidream.services.runtime.crawl_resume import crawl_run_in_progress_error

    configure_ext(crawl_run_in_progress_error=crawl_run_in_progress_error)


async def _live_crawl(eng: ExecutionEngine, session_id: str) -> None:
    from aidream.services.runtime.entry import open_request_execution

    scope = await open_request_execution(
        type="utility",
        app="aidream",
        surface="test_driver",
        user_id=USER_ID,
        organization_id=ORG_ID,
        request_id=LIVE_REQUEST,
        link_kind=LINK_KIND,
        link_id=session_id,
        holder=f"crawl:{session_id}",
        lease_seconds=240,
        allow_unknown=True,
        engine=eng,
    )
    await scope.begin()


def _snapshot(t: _SessionTable) -> dict[str, Any]:
    r = t.row
    return {"status": r.status, "version": r.version, "metadata": dict(r.metadata), "error": r.error}


def _router_resume(session_id: str):
    return crawl_router.resume_crawl(session_id, _ctx())  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_resuming_a_live_crawl_names_the_rejoin_and_writes_nothing(
    table, resume_worker, engine, host_refusal
) -> None:
    row = _session_row(status="running", lease_age=FRESH_LEASE_AGE)
    t = table(row)
    resume_worker(t)
    await _live_crawl(engine, str(row.id))
    before = _snapshot(t)

    with pytest.raises(HTTPException) as refused:
        await _router_resume(str(row.id))

    assert refused.value.status_code == 409
    body = refused.value.detail
    assert body["code"] == body["error"] == "run_in_progress"
    assert body["live_request_id"] == LIVE_REQUEST
    assert body["rejoin_path"] == f"/runtime/operations/{LIVE_REQUEST}/rejoin"
    assert body["session_id"] == str(row.id)
    assert _snapshot(t) == before, "a resume of a live crawl wrote the session row"


@pytest.mark.asyncio
async def test_a_host_without_the_spine_keeps_the_plain_409(table, resume_worker) -> None:
    row = _session_row(status="running", lease_age=FRESH_LEASE_AGE)
    resume_worker(table(row))

    with pytest.raises(HTTPException) as refused:
        await _router_resume(str(row.id))

    assert refused.value.status_code == 409
    assert "already active" in str(refused.value.detail)


@pytest.mark.asyncio
async def test_two_racing_resumes_never_both_win(
    table, resume_worker, engine, host_refusal, monkeypatch
) -> None:
    """Both read the crashed row; the lease compare-and-swap lets exactly one through,
    and the loser gets the canonical 409 (not a 503, not a second run)."""
    import asyncio

    row = _session_row(status="failed", lease_age=STALE_LEASE_AGE)
    row.error = STALE_SESSION_ERROR
    row.finished_at = utcnow()
    t = table(row)
    resume_worker(t)
    monkeypatch.setattr(WebCrawlRepository, "claim_run_lease", REAL_CLAIM)
    sid = str(row.id)

    # The winner's run shows up on the spine the moment it claims.
    real_claim = REAL_CLAIM

    async def claim_then_open(repo, session_id, **kw):
        token = await real_claim(repo, session_id, **kw)
        await _live_crawl(engine, session_id)
        return token

    monkeypatch.setattr(WebCrawlRepository, "claim_run_lease", claim_then_open)
    monkeypatch.setattr(
        crawl_router, "create_streaming_response", lambda *a, **k: SimpleNamespace(headers={})
    )
    results = await asyncio.gather(_router_resume(sid), _router_resume(sid), return_exceptions=True)

    losers = [r for r in results if isinstance(r, HTTPException)]
    winners = [r for r in results if not isinstance(r, BaseException)]
    assert len(winners) == 1 and len(losers) == 1, results
    assert losers[0].status_code == 409
    assert losers[0].detail["code"] == "run_in_progress"
    assert losers[0].detail["live_request_id"] == LIVE_REQUEST


@pytest.mark.asyncio
async def test_a_setup_that_fails_after_the_claim_hands_the_run_back(
    table, resume_worker, monkeypatch
) -> None:
    row = _session_row(status="failed", lease_age=STALE_LEASE_AGE)
    row.error = STALE_SESSION_ERROR
    row.finished_at = utcnow()
    t = table(row)
    worker = resume_worker(t)
    monkeypatch.setattr(WebCrawlRepository, "claim_run_lease", REAL_CLAIM)

    async def boom(*_a: Any, **_k: Any) -> int:
        raise ConnectionError("db went away after the claim")

    monkeypatch.setattr(WebCrawlRepository, "max_url_sequence", boom)

    with pytest.raises(ConnectionError):
        await worker.service.prepare_resume(_ctx(), str(row.id))

    assert t.row.status == "failed", "the session stayed `running` under a lease nobody holds"
    assert t.row.error == WORKER_STOPPED_ERROR
    assert worker.service.brokers.get(str(row.id)) is None, "the broker leaked"

    # ...so a retry is not locked out for a lease TTL: the door opens again.
    monkeypatch.setattr(WebCrawlRepository, "max_url_sequence", AsyncMock(return_value=0))
    prepared = await worker.service.prepare_resume(_ctx(), str(row.id))
    assert t.row.status == "running"
    await worker.service.brokers.remove(str(row.id), prepared.broker)
    await prepared.broker.close()
