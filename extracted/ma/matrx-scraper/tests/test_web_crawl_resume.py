"""Resume gates + request rebuild for crashed web crawls.

`prepare_resume` re-drives a crashed session's durable frontier. These tests
pin the two pure pieces every resume flows through: the resumability gate
(`_assert_session_resumable`) and the budget-shrinking request rebuild
(`_rebuild_resume_request`). The stateful path (session load, broker guard,
sequence seeding) is exercised against the live service by the boot sweep.
"""

from __future__ import annotations

from datetime import timedelta
from types import SimpleNamespace

import pytest

from matrx_scraper.web_crawl.contracts import CrawlStartRequest
from matrx_scraper.web_crawl.service import (
    RESUME_MAX_ATTEMPTS,
    _assert_session_resumable,
    _rebuild_resume_request,
)


def _session(
    *,
    mode: str = "full",
    status: str = "failed",
    metadata: dict | None = None,
    request: dict | None = None,
) -> SimpleNamespace:
    if request is None:
        request = CrawlStartRequest(max_pages=300).model_dump(mode="json")
    return SimpleNamespace(
        scope={"mode": mode, "coverage_qualified": True, "request": request},
        status=status,
        metadata=metadata or {},
    )


# ---------------------------------------------------------------------------
# Gate
# ---------------------------------------------------------------------------


def test_crashed_full_session_is_resumable() -> None:
    dump = _assert_session_resumable(_session())
    assert dump["max_pages"] == 300


@pytest.mark.parametrize("mode", ["homepage", "initialization", "bogus", None])
def test_short_run_modes_are_not_resumable(mode) -> None:
    with pytest.raises(ValueError, match="not resumable"):
        _assert_session_resumable(_session(mode=mode))


@pytest.mark.parametrize("mode", ["full", "list", "page_fetch"])
def test_durable_frontier_modes_are_resumable(mode) -> None:
    assert _assert_session_resumable(_session(mode=mode))


@pytest.mark.parametrize("status", ["complete", "partial"])
def test_finished_sessions_are_not_resumable(status) -> None:
    with pytest.raises(ValueError, match="already finished"):
        _assert_session_resumable(_session(status=status))


def test_user_cancelled_sessions_are_not_resumable() -> None:
    """A cancel is a deliberate terminal choice — a resume must never undo it."""
    with pytest.raises(ValueError, match="cancelled"):
        _assert_session_resumable(_session(metadata={"cancel_request": {"requested": True}}))


def test_attempt_cap_stops_resurrection_loops() -> None:
    """A run that keeps dying must not be resumed forever — the durable
    attempt counter caps it across restarts."""
    ok = _session(metadata={"resume": {"attempts": RESUME_MAX_ATTEMPTS - 1}})
    assert _assert_session_resumable(ok)
    capped = _session(metadata={"resume": {"attempts": RESUME_MAX_ATTEMPTS}})
    with pytest.raises(ValueError, match="needs investigation"):
        _assert_session_resumable(capped)


def test_session_without_persisted_request_is_not_resumable() -> None:
    with pytest.raises(ValueError, match="no persisted request"):
        _assert_session_resumable(_session(request={}))


# ---------------------------------------------------------------------------
# Request rebuild
# ---------------------------------------------------------------------------


def test_rebuild_shrinks_max_pages_by_fetched() -> None:
    dump = CrawlStartRequest(max_pages=300).model_dump(mode="json")
    request = _rebuild_resume_request(dump, {"pages_fetched": 120})
    assert request.max_pages == 180
    # Everything else survives the round-trip untouched.
    assert request.seed_from_sitemap is True
    assert request.capture_screenshots is True


def test_rebuild_clamps_exhausted_budget_at_one() -> None:
    """max_pages has ge=1 — an already-satisfied budget still runs the
    terminal reconcile pass instead of failing validation."""
    dump = CrawlStartRequest(max_pages=100).model_dump(mode="json")
    assert _rebuild_resume_request(dump, {"pages_fetched": 100}).max_pages == 1
    assert _rebuild_resume_request(dump, {"pages_fetched": 5000}).max_pages == 1


def test_rebuild_tolerates_missing_or_garbage_stats() -> None:
    dump = CrawlStartRequest(max_pages=50).model_dump(mode="json")
    assert _rebuild_resume_request(dump, None).max_pages == 50
    assert _rebuild_resume_request(dump, {}).max_pages == 50
    assert _rebuild_resume_request(dump, {"pages_fetched": "garbage"}).max_pages == 50
    assert _rebuild_resume_request(dump, {"pages_fetched": -3}).max_pages == 50


def test_rebuild_is_strictly_validated() -> None:
    """The rebuild goes through model_validate, so a corrupted persisted
    request fails loudly instead of producing an out-of-contract crawl."""
    with pytest.raises(Exception):
        _rebuild_resume_request({"max_pages": 100, "nonsense_field": True}, None)


# ---------------------------------------------------------------------------
# Event-sequence seeding — the resume-killer regression (2026-07-30)
# ---------------------------------------------------------------------------
#
# `prepare_resume` seeded only the crawl_url ledger counter. The event sink
# (`DurableCrawlEventSink`) restarted at 0, so the resumed run's FIRST event
# re-minted sequence 1, violated `crawl_event_session_sequence_unique`, and
# the recovery itself permanently failed the session (two live crawls killed
# this way on 2026-07-30). The sink MUST continue from the state's seeded
# `event_sequence`.


class _RecordingRepository:
    def __init__(self) -> None:
        self.sequences: list[int] = []

    async def persist_event(self, event, state) -> None:  # noqa: ANN001
        self.sequences.append(event.sequence)


class _NoopBroker:
    async def publish(self, event) -> None:  # noqa: ANN001
        return None


class _NoopEmitter:
    async def send_data(self, event) -> None:  # noqa: ANN001
        return None


def _persistence_state(**overrides):
    from matrx_scraper.web_crawl.persistence import CrawlPersistenceState

    defaults = dict(
        site_id="site-1",
        session_id="session-1",
        user_id="user-1",
        organization_id="org-1",
        file_owner_id="user-1",
        coverage_qualified=True,
    )
    defaults.update(overrides)
    return CrawlPersistenceState(**defaults)


@pytest.mark.asyncio
async def test_event_sink_continues_from_seeded_event_sequence() -> None:
    from matrx_scraper.events import CrawlWarningEvent
    from matrx_scraper.web_crawl.persistence import DurableCrawlEventSink

    repository = _RecordingRepository()
    state = _persistence_state(event_sequence=41)
    sink = DurableCrawlEventSink(repository, state, _NoopBroker(), _NoopEmitter())

    await sink.emit(CrawlWarningEvent(run_id="session-1", message="first after resume"))
    await sink.emit(CrawlWarningEvent(run_id="session-1", message="second after resume"))

    assert repository.sequences == [42, 43], (
        "a resumed sink must append after the crashed run's rows, never re-mint sequence 1"
    )


@pytest.mark.asyncio
async def test_event_sink_fresh_session_starts_at_one() -> None:
    from matrx_scraper.events import CrawlWarningEvent
    from matrx_scraper.web_crawl.persistence import DurableCrawlEventSink

    repository = _RecordingRepository()
    sink = DurableCrawlEventSink(repository, _persistence_state(), _NoopBroker(), _NoopEmitter())
    await sink.emit(CrawlWarningEvent(run_id="session-1", message="hello"))
    assert repository.sequences == [1]


@pytest.mark.asyncio
async def test_completed_event_waits_for_resume_safe_completion_barrier() -> None:
    from matrx_scraper.events import CrawlCompletedEvent
    from matrx_scraper.web_crawl.persistence import DurableCrawlEventSink

    order: list[str] = []

    class _OrderedRepository(_RecordingRepository):
        async def persist_event(self, event, state) -> None:  # noqa: ANN001
            order.append("persisted")
            await super().persist_event(event, state)

    async def barrier() -> None:
        order.append("link-status")

    repository = _OrderedRepository()
    sink = DurableCrawlEventSink(
        repository,
        _persistence_state(),
        _NoopBroker(),
        _NoopEmitter(),
        before_completed=barrier,
    )
    await sink.emit(
        CrawlCompletedEvent(
            run_id="session-1",
            pages_fetched=1,
            pages_failed=0,
            issues_count=0,
            duration_ms=1,
        )
    )

    assert order == ["link-status", "persisted"]


@pytest.mark.asyncio
async def test_failed_completion_barrier_leaves_success_event_unpersisted() -> None:
    from matrx_scraper.events import CrawlCompletedEvent
    from matrx_scraper.web_crawl.persistence import DurableCrawlEventSink

    async def barrier() -> None:
        raise RuntimeError("link evidence write failed")

    repository = _RecordingRepository()
    sink = DurableCrawlEventSink(
        repository,
        _persistence_state(),
        _NoopBroker(),
        _NoopEmitter(),
        before_completed=barrier,
    )
    with pytest.raises(RuntimeError, match="link evidence write failed"):
        await sink.emit(
            CrawlCompletedEvent(
                run_id="session-1",
                pages_fetched=1,
                pages_failed=0,
                issues_count=0,
                duration_ms=1,
            )
        )

    assert repository.sequences == []


def test_prepare_resume_seeds_both_monotonic_counters() -> None:
    """The load-bearing wiring, pinned against a silent deletion.

    Seeding `state.event_sequence` is ONE line in `prepare_resume`; delete it
    and the incident recurs with every other test in this file still green
    (that is exactly how it shipped). Assert the source calls BOTH repository
    seeders and assigns BOTH counters — a structural check, because the live
    stateful path has no test harness here.
    """
    import inspect

    from matrx_scraper.web_crawl.service import WebCrawlService

    source = inspect.getsource(WebCrawlService.prepare_resume)
    assert "max_url_sequence" in source, "crawl_url ledger counter must be seeded"
    assert "max_event_sequence" in source, "crawl_event counter must be seeded"
    assert "state.url_sequence =" in source
    assert "state.event_sequence =" in source


def test_repository_exposes_both_sequence_seeders() -> None:
    from matrx_scraper.web_crawl.persistence import WebCrawlRepository

    assert callable(WebCrawlRepository.max_url_sequence)
    assert callable(WebCrawlRepository.max_event_sequence)


# ---------------------------------------------------------------------------
# Cross-process resume — the run lease (2026-08-04)
# ---------------------------------------------------------------------------
#
# Seeding `event_sequence` fixed SEQUENTIAL, single-process resume only. Two
# processes (the resume endpoint vs. a live run, or two containers' boot
# sweeps) still both passed the in-process broker guard, both seeded from the
# same MAX(sequence), collided on `crawl_event_session_sequence_unique` — and
# the LOSER's error path marked the WINNER's session failed.
#
# Two independent layers now close it, each sufficient alone:
#   1. a durable run lease (CAS on the row's `version`) — only one claimant
#      runs, and every session-status write is gated on holding it;
#   2. a recoverable sequence collision — re-read MAX and retry instead of
#      failing the run.


def _leased_session(
    *,
    status: str = "running",
    owner: str | None = "owner-a",
    heartbeat_age: timedelta = timedelta(seconds=5),
    **overrides,
):
    from matrx_scraper.web_crawl.persistence import utcnow

    metadata = dict(overrides.pop("metadata", None) or {})
    if owner is not None:
        metadata["run_lease"] = {
            "owner": owner,
            "epoch": 1,
            "host": "box:1",
            "heartbeat_at": (utcnow() - heartbeat_age).isoformat(),
        }
    session = _session(status=status, metadata=metadata, **overrides)
    session.updated_at = utcnow() - heartbeat_age
    return session


def test_live_lease_means_the_session_is_running_somewhere() -> None:
    from matrx_scraper.web_crawl.persistence import run_lease_is_live

    assert run_lease_is_live(_leased_session()) is True


def test_stale_heartbeat_is_a_crash_and_stays_resumable() -> None:
    """Past the TTL the reaper owns the session — resume must NOT be blocked,
    or a real crash becomes permanently unrecoverable."""
    from matrx_scraper.web_crawl.persistence import RUN_LEASE_TTL, run_lease_is_live

    assert run_lease_is_live(_leased_session(heartbeat_age=RUN_LEASE_TTL * 2)) is False


def test_fresh_progress_signal_keeps_stale_heartbeat_live() -> None:
    """Progress touches ``updated_at`` even if a heartbeat write was missed.

    The integrity watchdog and stale-session transition must use the same latest
    signal or a healthy crawl is simultaneously classified live and crashed.
    """
    from matrx_scraper.web_crawl.persistence import RUN_LEASE_TTL, run_lease_is_live, utcnow

    session = _leased_session(heartbeat_age=RUN_LEASE_TTL * 2)
    session.updated_at = utcnow()

    assert run_lease_is_live(session) is True


def test_a_terminal_session_never_reads_as_live() -> None:
    from matrx_scraper.web_crawl.persistence import run_lease_is_live

    assert run_lease_is_live(_leased_session(status="failed")) is False


def test_pre_lease_running_session_falls_back_to_updated_at() -> None:
    """A session written by the previous build carries no lease at all. A fresh
    `updated_at` still means somebody is very likely on it — fail closed."""
    from matrx_scraper.web_crawl.persistence import RUN_LEASE_TTL, run_lease_is_live

    assert run_lease_is_live(_leased_session(owner=None)) is True
    assert run_lease_is_live(_leased_session(owner=None, heartbeat_age=RUN_LEASE_TTL * 2)) is False


def test_resume_is_refused_while_another_process_holds_the_lease() -> None:
    """The regression itself: this used to sail through and produce two live
    runs of one session. RuntimeError (not ValueError) so the endpoint 409s."""
    with pytest.raises(RuntimeError, match="already active"):
        _assert_session_resumable(_leased_session())


def test_resume_still_allowed_after_the_lease_goes_stale() -> None:
    from matrx_scraper.web_crawl.persistence import RUN_LEASE_TTL

    session = _leased_session(status="failed", heartbeat_age=RUN_LEASE_TTL * 2)
    assert _assert_session_resumable(session)


def test_lease_filter_pins_a_write_to_its_owner() -> None:
    """Terminal writes carry this filter, which is why a loser can no longer
    stamp `failed` over the winner's live session."""
    from matrx_scraper.web_crawl.persistence import _lease_filter

    assert _lease_filter("tok") == {"metadata__json_contains": {"run_lease": {"owner": "tok"}}}
    # No token (legacy/unleased caller) must not silently filter to nothing
    # matching — it degrades to the previous unconditional behaviour.
    assert _lease_filter(None) == {}


def test_lease_gated_writes_are_threaded_through_every_terminal_path() -> None:
    """Structural pin: `fail_session` is the write that made the bug
    destructive. Every call site must pass this run's token."""
    import inspect

    from matrx_scraper.web_crawl.service import WebCrawlService

    source = inspect.getsource(WebCrawlService)
    fail_calls = source.count("repository.fail_session(")
    assert fail_calls
    assert source.count("lease_token=prepared.state.run_lease_token") >= fail_calls


# --- Layer two: a sequence collision is recoverable, never run-fatal --------


class _CollidingRepository(_RecordingRepository):
    """Fails the first `collisions` writes with the real unique violation."""

    def __init__(self, collisions: int, ledger_max: int) -> None:
        super().__init__()
        self.collisions = collisions
        self.ledger_max = ledger_max
        self.attempts = 0

    async def persist_event(self, event, state) -> None:  # noqa: ANN001
        self.attempts += 1
        if self.attempts <= self.collisions:
            from matrx_orm import IntegrityError

            raise IntegrityError(
                constraint="unique",
                original_error=Exception(
                    "duplicate key value violates unique constraint "
                    '"crawl_event_session_sequence_unique"'
                ),
            )
        await super().persist_event(event, state)

    async def max_event_sequence(self, session_id: str) -> int:  # noqa: ANN001
        return self.ledger_max


@pytest.mark.asyncio
async def test_sequence_collision_re_reads_the_ledger_and_retries() -> None:
    from matrx_scraper.events import CrawlWarningEvent
    from matrx_scraper.web_crawl.persistence import DurableCrawlEventSink

    repository = _CollidingRepository(collisions=1, ledger_max=99)
    sink = DurableCrawlEventSink(repository, _persistence_state(), _NoopBroker(), _NoopEmitter())
    await sink.emit(CrawlWarningEvent(run_id="session-1", message="after a collision"))

    assert repository.attempts == 2
    assert repository.sequences == [100], (
        "the retry must continue past the LEDGER's max, not re-mint the "
        "colliding sequence — and it must not fail the run"
    )
    # And the sink keeps counting from there.
    await sink.emit(CrawlWarningEvent(run_id="session-1", message="next"))
    assert repository.sequences == [100, 101]


@pytest.mark.asyncio
async def test_sequence_recovery_is_bounded() -> None:
    """Recovery is not an infinite loop: a permanently colliding ledger still
    surfaces the error rather than spinning."""
    from matrx_scraper.events import CrawlWarningEvent
    from matrx_orm import IntegrityError
    from matrx_scraper.web_crawl.persistence import (
        EVENT_SEQUENCE_MAX_RETRIES,
        DurableCrawlEventSink,
    )

    repository = _CollidingRepository(collisions=10_000, ledger_max=0)
    sink = DurableCrawlEventSink(repository, _persistence_state(), _NoopBroker(), _NoopEmitter())
    with pytest.raises(IntegrityError):
        await sink.emit(CrawlWarningEvent(run_id="session-1", message="hopeless"))
    assert repository.attempts == EVENT_SEQUENCE_MAX_RETRIES


def test_only_the_event_sequence_constraint_is_recoverable() -> None:
    """Narrow on purpose — every other integrity error is a real bug and must
    keep failing the run."""
    from matrx_orm import IntegrityError

    from matrx_scraper.web_crawl.persistence import _is_event_sequence_collision

    hit = IntegrityError(
        constraint="unique",
        original_error=Exception(
            'duplicate key value violates unique constraint "crawl_event_session_sequence_unique"'
        ),
    )
    other_unique = IntegrityError(
        constraint="unique",
        original_error=Exception(
            'duplicate key value violates unique constraint "crawl_url_session_sequence_unique"'
        ),
    )
    fk = IntegrityError(
        constraint="foreign_key", original_error=Exception("violates foreign key constraint")
    )
    assert _is_event_sequence_collision(hit) is True
    assert _is_event_sequence_collision(other_unique) is False
    assert _is_event_sequence_collision(fk) is False


# ---------------------------------------------------------------------------
# Boot-sweep eligibility markers
# ---------------------------------------------------------------------------


def test_graceful_shutdown_marker_is_pinned_for_boot_sweep() -> None:
    """Deploys cancel workers GRACEFULLY; the session fails with
    WORKER_STOPPED_ERROR, not STALE_SESSION_ERROR. The boot sweep matches the
    error string exactly, so the marker written by run_prepared and the
    constant the candidate query filters on must never drift (a mid-crawl
    deploy would otherwise permanently kill the crawl — observed live
    2026-08-08)."""
    from matrx_scraper.web_crawl.persistence import WORKER_STOPPED_ERROR

    assert WORKER_STOPPED_ERROR == "CancelledError: crawler worker stopped before completion"
    import inspect

    from matrx_scraper.web_crawl.persistence import WebCrawlRepository

    source = inspect.getsource(WebCrawlRepository.list_crash_resumable_sessions)
    assert "WORKER_STOPPED_ERROR" in source
    assert "STALE_SESSION_ERROR" in source
