"""Cancelling a crawl session: orphans terminate, live runs stop cooperatively.

A metadata-only cancel stamp on an orphaned queued session was a trap: no
worker polls a queued session, and the stamp's UPDATE bumps `updated_at` —
the exact freshness signal the one-active-crawl gate uses — so every Cancel
click EXTENDED the 30-minute block instead of clearing it.

SUT: `WebCrawlRepository.request_cancel`, judged by what its write leaves in the
session row and by the REAL consumers of that row:
- the one-active-crawl gate (`_session_blocks_new_crawl`),
- the worker entry that would run an existing session
  (`WebCrawlService.prepare_resume` — also the boot crash-resume path), whose
  run starts only when it claims the run lease,
- a live run's cancel watcher (`WebCrawlService._watch_for_cancel`).

Doubled: the `web.crawl_session` table (one in-memory row that applies the
filters the repository sends and bumps `updated_at`/`version` like the
`_touch_row` trigger), plus the RLS / site / DNS / sequence reads and the
lease CAS that `prepare_resume` performs — the CAS records the claim, which is
the moment a worker would start the session's work.
"""

from __future__ import annotations

import asyncio
import copy
from collections.abc import Callable
from contextlib import asynccontextmanager
from datetime import timedelta
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from matrx_scraper import _ext
from matrx_scraper._ext import configure_ext
from matrx_scraper.crawler import RENDER_HTTP_FIRST
from matrx_scraper.db.models_web import CrawlSession
from matrx_scraper.web_crawl import service as service_module
from matrx_scraper.web_crawl.contracts import CrawlStartRequest
from matrx_scraper.web_crawl.persistence import (
    RUN_LEASE_TTL,
    STALE_SESSION_ERROR,
    WebCrawlRepository,
    utcnow,
)
from matrx_scraper.web_crawl.service import WebCrawlService, _session_blocks_new_crawl

NS = "matrx_scraper.web_crawl.persistence"
ORG_ID = "5dc930e9-bd65-44a1-8369-af773f6e1a5b"
SITE_ID = "d0aff5b6-0710-4848-8304-164db3c80ab7"
USER_ID = "4cf62e4e-2679-484f-b652-034e697418df"
STALE_LEASE_AGE = RUN_LEASE_TTL + timedelta(minutes=1)
FRESH_LEASE_AGE = timedelta(seconds=5)


class _SessionTable:
    """One `web.crawl_session` row. Applies equality filters (+ `deleted_at__isnull`)
    exactly as Postgres would, and bumps `updated_at`/`version` on every UPDATE."""

    def __init__(self, row: CrawlSession) -> None:
        self.row = row
        self.between_read_and_write: Callable[[CrawlSession], None] | None = None

    def _copy(self) -> CrawlSession:
        return CrawlSession(
            **{name: copy.deepcopy(getattr(self.row, name)) for name in CrawlSession._fields}
        )

    def _matches(self, filters: dict[str, Any]) -> bool:
        for key, expected in filters.items():
            if key == "deleted_at__isnull":
                if (self.row.deleted_at is None) is not bool(expected):
                    return False
            elif "__" in key:
                raise AssertionError(f"in-memory crawl_session does not model lookup {key!r}")
            elif str(getattr(self.row, key)) != str(expected):
                return False
        return True

    async def get(self, *, use_cache: bool = True, **filters: Any) -> CrawlSession:
        assert self._matches(filters), f"no crawl_session row matches {filters}"
        snapshot = self._copy()
        if self.between_read_and_write is not None:
            concurrent_writer, self.between_read_and_write = self.between_read_and_write, None
            concurrent_writer(self.row)
        return snapshot

    async def get_or_none(self, *, use_cache: bool = True, **filters: Any) -> CrawlSession | None:
        return self._copy() if self._matches(filters) else None

    async def update_where(self, filters: dict[str, Any], **values: Any) -> SimpleNamespace:
        if not self._matches(filters):
            return SimpleNamespace(rows_affected=0)
        for name, value in values.items():
            assert name in CrawlSession._fields, f"write to unknown crawl_session column {name!r}"
            setattr(self.row, name, value)
        self.row.updated_at = utcnow()
        self.row.version = int(self.row.version or 0) + 1
        return SimpleNamespace(rows_affected=1)


def _session_row(*, status: str, lease_age: timedelta | None) -> CrawlSession:
    now = utcnow()
    metadata: dict[str, Any] = {}
    if lease_age is not None:
        signalled_at = (now - lease_age).isoformat()
        metadata["run_lease"] = {
            "owner": "worker-lease-token",
            "epoch": 1,
            "acquired_at": signalled_at,
            "heartbeat_at": signalled_at,
            "host": "worker-host",
        }
    request = CrawlStartRequest(
        max_pages=50,
        max_depth=2,
        render_mode=RENDER_HTTP_FIRST,
        capture_screenshots=False,
        screenshot_kinds=[],
    )
    return CrawlSession(
        id=str(uuid4()),
        organization_id=ORG_ID,
        site_id=SITE_ID,
        created_by=USER_ID,
        updated_by=USER_ID,
        created_at=now - timedelta(minutes=2),
        updated_at=now - timedelta(seconds=10),
        deleted_at=None,
        version=3,
        metadata=metadata,
        status=status,
        trigger="manual",
        scope={"mode": "full", "coverage_qualified": True, "request": request.model_dump(mode="json")},
        stats={},
        started_at=(now - timedelta(minutes=1)) if status == "running" else None,
        finished_at=None,
        error=None,
    )


@pytest.fixture
def table(monkeypatch: pytest.MonkeyPatch) -> Callable[[CrawlSession], _SessionTable]:
    def install(row: CrawlSession) -> _SessionTable:
        session_table = _SessionTable(row)

        @asynccontextmanager
        async def transaction(_db: str):
            yield None

        monkeypatch.setattr(f"{NS}.transaction", transaction)
        monkeypatch.setattr(f"{NS}.WebCrawlSession.get", session_table.get)
        monkeypatch.setattr(f"{NS}.WebCrawlSession.get_or_none", session_table.get_or_none)
        monkeypatch.setattr(f"{NS}.WebCrawlSession.update_where", session_table.update_where)
        return session_table

    return install


@pytest.fixture
def resume_worker(monkeypatch: pytest.MonkeyPatch) -> Callable[[_SessionTable], SimpleNamespace]:
    """The real `prepare_resume` with only its I/O doubled. `claimed` records every
    run-lease claim — the step after which the session's work would start."""
    saved_ext = dict(_ext._registry)

    def install(session_table: _SessionTable) -> SimpleNamespace:
        claimed: list[str] = []

        async def assert_session_access(_repo: WebCrawlRepository, session_id: str) -> CrawlSession:
            row = await session_table.get_or_none(id=session_id, deleted_at__isnull=True)
            assert row is not None
            return row

        async def claim_run_lease(
            _repo: WebCrawlRepository, session_id: str, *, is_resume: bool
        ) -> tuple[str, int]:
            claimed.append(session_id)
            return "resume-lease-token", 1

        monkeypatch.setattr(WebCrawlRepository, "assert_session_access", assert_session_access)
        monkeypatch.setattr(WebCrawlRepository, "assert_site_editor", AsyncMock(return_value=None))
        monkeypatch.setattr(
            WebCrawlRepository,
            "site_identity",
            AsyncMock(return_value=("https://acme.example/", ORG_ID, USER_ID)),
        )
        monkeypatch.setattr(WebCrawlRepository, "claim_run_lease", claim_run_lease)
        monkeypatch.setattr(WebCrawlRepository, "max_url_sequence", AsyncMock(return_value=0))
        monkeypatch.setattr(WebCrawlRepository, "max_event_sequence", AsyncMock(return_value=0))
        monkeypatch.setattr(service_module, "validate_public_http_url", AsyncMock(return_value=None))
        configure_ext(
            file_manager=SimpleNamespace(
                sync_engine=SimpleNamespace(_config=SimpleNamespace(storage_backend="s3")),
                cloud=SimpleNamespace(is_configured=lambda scheme: scheme == "s3"),
            )
        )
        return SimpleNamespace(service=WebCrawlService(), claimed=claimed)

    yield install
    _ext._registry.clear()
    _ext._registry.update(saved_ext)


def _ctx() -> SimpleNamespace:
    return SimpleNamespace(is_authenticated=True, user_id=USER_ID, token=None, email=None)


async def _attempt_resume(worker: SimpleNamespace, session_id: str) -> BaseException | None:
    try:
        prepared = await worker.service.prepare_resume(_ctx(), session_id)
    except Exception as exc:  # noqa: BLE001 — the refusal itself is under test
        return exc
    await worker.service.brokers.remove(session_id, prepared.broker)
    await prepared.broker.close()
    return None


async def _watcher_stops(service: WebCrawlService, session_table: _SessionTable) -> Mock:
    crawler = SimpleNamespace(cancel=Mock())
    try:
        await asyncio.wait_for(
            service._watch_for_cancel(
                str(session_table.row.id),
                crawler,  # type: ignore[arg-type]
                WebCrawlRepository({}),
                lease_token=None,
            ),
            timeout=3.0,
        )
    except TimeoutError:
        pytest.fail("the live run's cancel watcher never saw the cancel request")
    return crawler.cancel


ORPHANS = pytest.mark.parametrize(
    "lease_age", [None, STALE_LEASE_AGE], ids=["never-leased", "stale-lease"]
)


@ORPHANS
@pytest.mark.asyncio
async def test_cancelling_an_orphaned_queued_session_terminates_it_as_partial(
    table: Callable[[CrawlSession], _SessionTable], lease_age: timedelta | None
) -> None:
    session_table = table(_session_row(status="queued", lease_age=lease_age))

    await WebCrawlRepository({}).request_cancel(str(session_table.row.id), USER_ID)

    row = session_table.row
    assert row.status == "partial"  # the canceled -> partial mapping
    assert row.finished_at is not None
    assert "cancel" in (row.error or "")
    assert row.metadata["cancel_request"]["requested"] is True
    assert row.metadata["cancel_request"]["requested_by"] == USER_ID


@ORPHANS
@pytest.mark.asyncio
async def test_a_cancelled_orphan_no_longer_blocks_a_new_crawl(
    table: Callable[[CrawlSession], _SessionTable], lease_age: timedelta | None
) -> None:
    session_table = table(_session_row(status="queued", lease_age=lease_age))

    await WebCrawlRepository({}).request_cancel(str(session_table.row.id), USER_ID)

    assert not _session_blocks_new_crawl(session_table.row), (
        "the cancelled session still blocks a new crawl of its site — the Cancel "
        "click refreshed the very freshness signal the gate reads"
    )


@ORPHANS
@pytest.mark.asyncio
async def test_a_worker_never_starts_a_cancelled_orphan(
    table: Callable[[CrawlSession], _SessionTable],
    resume_worker: Callable[[_SessionTable], SimpleNamespace],
    lease_age: timedelta | None,
) -> None:
    session_table = table(_session_row(status="queued", lease_age=lease_age))
    worker = resume_worker(session_table)

    await WebCrawlRepository({}).request_cancel(str(session_table.row.id), USER_ID)
    outcome = await _attempt_resume(worker, str(session_table.row.id))

    assert worker.claimed == [], "a worker claimed the run of a session the user cancelled"
    assert isinstance(outcome, ValueError), f"expected a not-resumable refusal, got {outcome!r}"


@pytest.mark.asyncio
async def test_control_the_resume_worker_does_claim_an_uncancelled_crashed_session(
    table: Callable[[CrawlSession], _SessionTable],
    resume_worker: Callable[[_SessionTable], SimpleNamespace],
) -> None:
    """Proves the harness above reaches the claim, so its empty `claimed` means refusal."""
    row = _session_row(status="failed", lease_age=STALE_LEASE_AGE)
    row.error = STALE_SESSION_ERROR
    row.finished_at = utcnow()
    session_table = table(row)
    worker = resume_worker(session_table)

    outcome = await _attempt_resume(worker, str(row.id))

    assert outcome is None
    assert worker.claimed == [str(row.id)]


@pytest.mark.asyncio
async def test_cancelling_a_queued_session_with_a_live_lease_stops_its_worker_cooperatively(
    table: Callable[[CrawlSession], _SessionTable],
) -> None:
    """A worker just claimed this session — terminating the row would race it."""
    session_table = table(_session_row(status="queued", lease_age=FRESH_LEASE_AGE))

    await WebCrawlRepository({}).request_cancel(str(session_table.row.id), USER_ID)

    assert session_table.row.status == "queued"
    assert session_table.row.finished_at is None
    cancel = await _watcher_stops(WebCrawlService(), session_table)
    cancel.assert_called_once_with()


@pytest.mark.asyncio
async def test_a_cooperatively_cancelled_session_is_never_resumed_after_its_worker_dies(
    table: Callable[[CrawlSession], _SessionTable],
    resume_worker: Callable[[_SessionTable], SimpleNamespace],
) -> None:
    """Break: the reaper fails the dead worker's session with the STALE marker, the
    crash-resume sweep picks it up, and the crawl the user cancelled runs anyway."""
    session_table = table(_session_row(status="queued", lease_age=FRESH_LEASE_AGE))
    worker = resume_worker(session_table)
    await WebCrawlRepository({}).request_cancel(str(session_table.row.id), USER_ID)
    # The worker dies before honouring the stamp; the stale reaper fails the row.
    session_table.row.status = "failed"
    session_table.row.error = STALE_SESSION_ERROR
    session_table.row.finished_at = utcnow()

    outcome = await _attempt_resume(worker, str(session_table.row.id))

    assert worker.claimed == [], "the crash-resume worker restarted a session the user cancelled"
    assert isinstance(outcome, ValueError), f"expected a not-resumable refusal, got {outcome!r}"


@pytest.mark.asyncio
async def test_cancelling_a_running_session_stops_its_run_without_rewriting_its_status(
    table: Callable[[CrawlSession], _SessionTable],
) -> None:
    session_table = table(_session_row(status="running", lease_age=FRESH_LEASE_AGE))

    await WebCrawlRepository({}).request_cancel(str(session_table.row.id), USER_ID)

    row = session_table.row
    assert row.status == "running"
    assert row.finished_at is None
    assert row.error is None
    assert row.metadata["cancel_request"]["requested"] is True
    cancel = await _watcher_stops(WebCrawlService(), session_table)
    cancel.assert_called_once_with()


@pytest.mark.asyncio
async def test_cancel_racing_a_worker_start_never_clobbers_the_now_running_session(
    table: Callable[[CrawlSession], _SessionTable],
) -> None:
    """The row is read as an orphan, then a worker claims it before the terminal
    write lands: the status-filtered UPDATE must miss and the stamp still land."""
    session_table = table(_session_row(status="queued", lease_age=None))

    def worker_claims_it(row: CrawlSession) -> None:
        row.status = "running"
        row.started_at = utcnow()

    session_table.between_read_and_write = worker_claims_it

    await WebCrawlRepository({}).request_cancel(str(session_table.row.id), USER_ID)

    row = session_table.row
    assert row.status == "running", "the cancel overwrote a run that had just started"
    assert row.finished_at is None
    assert row.metadata["cancel_request"]["requested"] is True
