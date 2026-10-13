"""Site-command progress lands in web.crawl_event BEFORE it streams.

Live 2026-10-12: sitemap/GSC/link/URL-reconciliation/analysis sync and the
initialize steps sent their progress to the NDJSON stream only
(`emitter.send_data`). `web.crawl_event` had never held a single one of those
rows, so a browser whose socket dropped had nothing to follow and the
frontend's follower read every healthy long command as stalled after 10
minutes. SUT: `DurableCrawlEventSink.emit_command` (sequence → persist → send)
and the runners that now use it. Doubled: the repository (its calls ARE the
persisted contract) and the emitter.

The second half pins the payload shape the frontend's movement rule reads:
every counter path in the frontend's `PROGRESS_COUNTERS`
(matrx-frontend features/marketing/crawler/follow-session.ts) must exist on
the event contract that is stored. Rename a summary field and this fails here
before the follower silently stops seeing movement.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from matrx_scraper.web_crawl import service as service_module
from matrx_scraper.web_crawl.analysis import AnalysisRunResult
from matrx_scraper.web_crawl.contracts import (
    AnalysisProgressEvent,
    AnalysisSummary,
    GscSyncProgressEvent,
    LinkCheckProgressEvent,
    LinkResolutionProgressEvent,
    LinkScoreProgressEvent,
    SitemapSyncProgressEvent,
    UrlReconciliationProgressEvent,
)
from matrx_scraper.web_crawl.persistence import DurableCrawlEventSink
from matrx_scraper.web_crawl.service import PreparedAnalysis, WebCrawlService


class _OrderedEmitter:
    def __init__(self, log: list[str]) -> None:
        self.log = log
        self.events: list[object] = []

    async def send_data(self, event: object) -> None:
        self.log.append("send")
        self.events.append(event)

    async def send_end(self) -> None:
        self.log.append("end")


def _state() -> SimpleNamespace:
    return SimpleNamespace(
        run_lease_token="lease-1",
        session_id="session-1",
        site_id="site-1",
        organization_id="org-1",
        user_id="user-1",
        event_sequence=0,
    )


@pytest.mark.asyncio
async def test_every_analysis_progress_event_is_persisted_before_it_streams(monkeypatch):
    log: list[str] = []
    persisted: list[dict] = []

    async def persist(payload: dict, _state: object) -> None:
        log.append("persist")
        persisted.append(dict(payload))

    repository = SimpleNamespace(
        mark_session_running=AsyncMock(),
        fail_session=AsyncMock(return_value=True),
        complete_session=AsyncMock(return_value=True),
        heartbeat_run_lease=AsyncMock(return_value=True),
        persist_command_event=persist,
    )
    service = WebCrawlService()
    monkeypatch.setattr(service, "_refresh_site_probe", AsyncMock())

    async def finish(**_kwargs):
        return AnalysisRunResult(AnalysisSummary(pages_analyzed=7, checks_run=40))

    monkeypatch.setattr(service_module, "analyze_site_pages", finish)
    emitter = _OrderedEmitter(log)
    await service.run_analysis(
        emitter,
        PreparedAnalysis(
            site_id="site-1",
            session_id="session-1",
            root_url="https://example.com",
            repository=repository,
            state=_state(),
        ),
    )

    assert persisted, "analysis progress never reached web.crawl_event"
    assert {row["event_type"] for row in persisted} == {"analysis_progress"}
    # Sequenced on the session's one counter, in order, gap-free.
    assert [row["sequence"] for row in persisted] == list(range(1, len(persisted) + 1))
    # Persist strictly before each send: a viewer can always find what it saw.
    sends = [index for index, entry in enumerate(log) if entry == "send"]
    persists = [index for index, entry in enumerate(log) if entry == "persist"]
    assert len(sends) == len(persists)
    assert all(p < s for p, s in zip(persists, sends))
    # The stored row and the wire carry the same shape, counters included.
    final = persisted[-1]
    assert final["status"] == "ok"
    assert final["summary"]["pages_analyzed"] == 7
    assert final["summary"]["checks_run"] == 40
    assert emitter.events[-1] == final


@pytest.mark.asyncio
async def test_a_command_sink_needs_no_replay_broker():
    stored: list[dict] = []

    async def persist(payload: dict, _state: object) -> None:
        stored.append(payload)

    repository = SimpleNamespace(persist_command_event=persist)
    emitter = _OrderedEmitter([])
    sink = DurableCrawlEventSink(repository, _state(), None, emitter)  # type: ignore[arg-type]

    await sink.emit_command(
        SitemapSyncProgressEvent(
            site_id="site-1",
            session_id="session-1",
            status="progress",
            message="Read 3 sitemaps",
            summary={"found": 3, "urls": 120, "pages_upserted": 40},
        )
    )

    assert stored[0]["sequence"] == 1
    assert stored[0]["run_id"] == "session-1"
    assert stored[0]["summary"]["pages_upserted"] == 40


# The frontend's movement counters (follow-session.ts PROGRESS_COUNTERS), by
# stored event type. Keep the two in step: each side has a test.
FRONTEND_PROGRESS_COUNTERS: dict[str, tuple[type, list[str]]] = {
    "sitemap_sync_progress": (
        SitemapSyncProgressEvent,
        ["summary.found", "summary.urls", "summary.pages_upserted"],
    ),
    "gsc_sync_progress": (GscSyncProgressEvent, ["summary.pages", "summary.stats_rows"]),
    "url_reconciliation_progress": (
        UrlReconciliationProgressEvent,
        ["summary.pages_scanned", "summary.relations_scanned"],
    ),
    "link_resolution_progress": (
        LinkResolutionProgressEvent,
        ["summary.scanned", "summary.resolved", "summary.unresolved"],
    ),
    "link_check_progress": (
        LinkCheckProgressEvent,
        ["summary.internal_scanned", "summary.internal_updated", "summary.external_checked"],
    ),
    "link_score_progress": (
        LinkScoreProgressEvent,
        ["summary.nodes", "summary.edges_scanned", "summary.pages_scored"],
    ),
    "analysis_progress": (
        AnalysisProgressEvent,
        ["summary.pages_analyzed", "summary.checks_run", "summary.results_written"],
    ),
}


@pytest.mark.parametrize("event_type", sorted(FRONTEND_PROGRESS_COUNTERS))
def test_every_frontend_counter_path_is_a_number_on_the_stored_contract(event_type: str):
    model, paths = FRONTEND_PROGRESS_COUNTERS[event_type]
    assert model.model_fields["event_type"].default == event_type
    stored = model(
        site_id="site-1", session_id="session-1", status="progress", message="m", summary={}
    ).model_dump(mode="json")
    for path in paths:
        value: object = stored
        for part in path.split("."):
            assert isinstance(value, dict) and part in value, f"{event_type}: no {path}"
            value = value[part]
        assert isinstance(value, int), f"{event_type}: {path} is not a counter"
