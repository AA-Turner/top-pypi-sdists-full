"""A browser worker never ends itself because the server is merely unreachable.

Before 2026-10-17 the lease watchdog ended the task 150 s after the last
renewal, whatever the reason. With the renewer suspended that day, every Cloud
Computer ended itself. Now silence makes the worker ASK the server
(``lease_watchdog``) and only a definite "ended" stops it.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

import httpx
import pytest

pytest.importorskip("playwright", reason="playwright not installed (browser extra)")

from matrx_scraper.cloud_browser.worker import runtime  # noqa: E402
from matrx_scraper.cloud_browser.worker.lease_watchdog import (  # noqa: E402
    LeaseCheck,
    WatchdogState,
    lease_check_url,
    probe_control_plane,
)
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker  # noqa: E402



class _Context:
    def __init__(self) -> None:
        self.closed = 0

    async def close(self) -> None:
        self.closed += 1


class _Lock:
    def __init__(self) -> None:
        self.held = True

    def release(self) -> None:
        self.held = False


def _lapsed_worker(monkeypatch, answers: list[LeaseCheck]) -> tuple[BrowserWorker, list, _Context]:
    worker = BrowserWorker(worker_id="worker-watchdog")
    worker.run_id = "run-1"
    worker.health = "healthy"
    worker.queue_state = "open"
    worker._bootstrapped = True
    context = _Context()
    worker._context = context
    worker._pw = None
    worker._lock = _Lock()
    ended: list = []
    worker._end_process = lambda: ended.append(True)
    asked: list = []

    async def probe() -> LeaseCheck:
        asked.append(True)
        return answers[min(len(asked), len(answers)) - 1]

    worker._lease_probe = probe
    worker._lease_expires_at = datetime.now(UTC) - timedelta(seconds=1)
    monkeypatch.setattr(runtime, "LEASE_WATCHDOG_TICK_SECONDS", 0.01)
    monkeypatch.setattr(runtime, "LEASE_WATCHDOG_GRACE_SECONDS", 0.0)
    return worker, ended, context


async def test_an_unreachable_server_never_ends_the_worker(monkeypatch) -> None:
    worker, ended, context = _lapsed_worker(
        monkeypatch, [LeaseCheck("unknown", detail="ConnectError: unreachable")]
    )
    worker.enable_lease_watchdog()
    worker._start_lease_watchdog()
    await asyncio.sleep(0.3)  # ~30 watchdog ticks, every lease long lapsed
    assert ended == []
    assert context.closed == 0
    assert worker.health == "healthy"
    assert worker._lease_watchdog is not None and not worker._lease_watchdog.done()
    worker._lease_watchdog.cancel()


async def test_a_failing_renewer_with_a_live_run_keeps_the_worker(monkeypatch) -> None:
    worker, ended, context = _lapsed_worker(monkeypatch, [LeaseCheck("live")])
    worker.enable_lease_watchdog()
    for n in range(20):
        assert await worker._lease_watchdog_tick(datetime.now(UTC) + timedelta(minutes=n)) is False
    assert ended == [] and context.closed == 0


async def test_the_unreachable_limit_from_the_server_is_honoured(monkeypatch) -> None:
    worker, ended, _ = _lapsed_worker(
        monkeypatch,
        [LeaseCheck("live", unreachable_max_seconds=60), LeaseCheck("unknown")],
    )
    worker.enable_lease_watchdog()
    t0 = datetime.now(UTC)
    assert await worker._lease_watchdog_tick(t0) is False  # live; learns the 60 s limit
    assert await worker._lease_watchdog_tick(t0 + timedelta(seconds=30)) is False  # unreachable starts
    assert await worker._lease_watchdog_tick(t0 + timedelta(seconds=60)) is False  # 30 s < 60 s
    assert await worker._lease_watchdog_tick(t0 + timedelta(seconds=91)) is True
    assert ended == [True]


async def test_a_released_run_on_a_cloud_computer_stops_the_run_and_keeps_the_machine(
    monkeypatch,
) -> None:
    worker, ended, context = _lapsed_worker(monkeypatch, [LeaseCheck("ended")])
    worker.enable_lease_watchdog(keep_process_on_ended_run=True)
    assert await worker._lease_watchdog_tick(datetime.now(UTC)) is False
    assert ended == []
    assert context.closed == 1
    assert worker._lock is not None and worker._lock.held is False
    assert worker.health == "stopped" and worker.queue_state == "closed"
    assert worker._terminating is False
    # Exactly the shape the next bootstrap reuses (``_reset_after_stopped_run``).
    assert worker._bootstrapped and worker.health == "stopped" and worker.queue_state == "closed"
    # And the watchdog is quiet afterwards: no lease, nothing to watch.
    assert await worker._lease_watchdog_tick(datetime.now(UTC) + timedelta(hours=1)) is False


async def test_a_released_run_on_a_fleet_worker_ends_the_process(monkeypatch) -> None:
    worker, ended, context = _lapsed_worker(monkeypatch, [LeaseCheck("ended")])
    worker.enable_lease_watchdog()
    assert await worker._lease_watchdog_tick(datetime.now(UTC)) is True
    assert ended == [True] and context.closed == 1


async def test_a_renewal_clears_the_unreachable_clock(monkeypatch) -> None:
    worker, ended, _ = _lapsed_worker(
        monkeypatch, [LeaseCheck("unknown", unreachable_max_seconds=60)]
    )
    worker.enable_lease_watchdog()
    t0 = datetime.now(UTC)
    await worker._lease_watchdog_tick(t0)
    assert worker._watchdog_state.unreachable_since == t0
    worker._lease_expires_at = t0 + timedelta(hours=2)  # a heartbeat renewed it
    await worker._lease_watchdog_tick(t0 + timedelta(seconds=40))
    assert worker._watchdog_state.unreachable_since is None
    assert ended == []


def test_probes_are_spaced_by_the_server_interval() -> None:
    state = WatchdogState()
    t0 = datetime.now(UTC)
    state.decide(LeaseCheck("live", probe_interval_seconds=45), t0)
    assert state.probe_due(t0 + timedelta(seconds=44)) is False
    assert state.probe_due(t0 + timedelta(seconds=45)) is True


def test_lease_check_url_comes_from_the_bootstrap_callback() -> None:
    assert (
        lease_check_url("https://server.app.matrxserver.com/browser-manager/worker-events")
        == "https://server.app.matrxserver.com/browser-worker/lease-check"
    )
    assert lease_check_url("stub://events") is None
    assert lease_check_url(None) is None


async def test_probe_reads_every_non_answer_as_unknown() -> None:
    def answer(status: int, body: dict | None = None):
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(status, json=body or {})

        return httpx.AsyncClient(transport=httpx.MockTransport(handler))

    url = "https://server.example/browser-worker/lease-check"
    kw = {"run_id": "r", "activation_key": "a", "worker_id": "w", "timeout_seconds": 5.0}
    live = await probe_control_plane(
        url,
        client=answer(200, {"verdict": "live", "probe_interval_seconds": 30, "unreachable_max_seconds": 0}),
        **kw,
    )
    assert (live.verdict, live.probe_interval_seconds, live.unreachable_max_seconds) == ("live", 30, 0)
    assert (await probe_control_plane(url, client=answer(200, {"verdict": "ended"}), **kw)).verdict == "ended"
    for client in (answer(503), answer(500), answer(200, {"verdict": "maybe"})):
        assert (await probe_control_plane(url, client=client, **kw)).verdict == "unknown"

    def refuse(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("unreachable")

    down = httpx.AsyncClient(transport=httpx.MockTransport(refuse))
    assert (await probe_control_plane(url, client=down, **kw)).verdict == "unknown"
    assert (await probe_control_plane(None, **kw)).verdict == "unknown"


def test_before_any_answer_the_worker_asks_every_tick_and_never_gives_up() -> None:
    state = WatchdogState()
    t0 = datetime.now(UTC)
    for n in range(100):
        now = t0 + timedelta(hours=n)
        assert state.probe_due(now) is True
        assert state.decide(LeaseCheck("unknown"), now) == "stay"
