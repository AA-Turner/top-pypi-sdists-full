"""Wiring the collector into the SDK: default-on at run(), invisible to the
resume machinery, and every write TO the run queued in its journal.

Contracts (each maps to a locked review decision):
- run() starts a collector by default; PROBE_HW=0 / run(hw=False) disable;
  only the node-local leader starts one (LOCAL_RANK heuristics);
  finish() stops it.
- The resume guard is KIND-SCOPED: hardware's epoch steps (~29.7M) neither
  trip it nor arm it. A receipt whose last_step is implausibly high came
  from a server that predates the hw-exclusion fix — warn and skip arming
  (warn-never-gate) rather than poison every training log call.
- Under async writes, hardware batches and the inventory's env_ref PATCH are
  journal ops (plan 0.3, D2): FIFO with the run's other ops, never a direct
  write racing the drain on the server's run-row lock, `blocking=False` so
  they never hold a close. A journal refusal drops them quietly (no gap, no
  notice); a broken journal leaves them in the monitor's bounded buffer.
  Under sync writes they stay direct, so charts stay live.
- The collector and inventory hold the Run weakly: an abandoned run's
  heartbeat and collector stop when it is collected.
- Inventory mints a minimal execution record (hardware= field) only when the
  run has no env_ref yet; a real snapshot's record is never clobbered, even
  while the snapshot's PATCH is still queued.
"""

from __future__ import annotations

import errno
import functools
import gc
import json
import re
import threading
import time
import warnings

import httpx
import pytest

import probe.hw.integration as hw_integration
from probe import errors
from probe.hw.grid import HW_STEP_SECONDS, step_for
from probe.hw.monitor import HwMonitor as RealHwMonitor
from probe.hw.types import HwSample
from probe.sdk import journal as journal_module
from tests.conftest import make_client, open_run


class RecorderMonitor:
    """Stands in for HwMonitor: records lifecycle, runs no threads."""

    instances: list = []

    def __init__(self, *a, **kw):
        self.started = False
        self.finished = False
        self.kwargs = kw
        RecorderMonitor.instances.append(self)

    def start(self):
        self.started = True

    def request_stop(self):
        self.stop_requested = True

    def finish(self, timeout=None):
        self.finished = True
        self.finish_timeout = timeout


@pytest.fixture(autouse=True)
def _hw_test_env(monkeypatch):
    """Deterministic election + no real monitor threads in these tests."""
    RecorderMonitor.instances = []
    monkeypatch.setattr(hw_integration, "HwMonitor", RecorderMonitor)
    monkeypatch.setenv("LOCAL_RANK", "0")
    monkeypatch.delenv("PROBE_HW", raising=False)
    yield


def test_hw_is_on_by_default(client, app):
    """2026-09-21, reversing the opt-in revision of 2026-08-06. Opt-in left
    the hardware detectors dark where they mattered most: of 209 crashed runs
    over 30 days of production, five had any hardware series, and five of the
    fourteen crash detectors read nothing else. A bare run() collects again.
    """
    run = open_run(client, experiment="hw-e2e")
    assert run._hw_monitor is not None
    run.finish()


def test_probe_hw_env_disables(client, app, monkeypatch):
    """The escape hatch the log line has always advertised."""
    for value in ("0", "false", "off", "OFF"):
        monkeypatch.setenv("PROBE_HW", value)
        run = open_run(client, experiment="hw-e2e")
        assert run._hw_monitor is None, f"PROBE_HW={value} should disable"
        run.finish()


def test_run_hw_true_starts_monitor_and_finish_stops(client, app):
    run = open_run(client, experiment="hw-e2e", hw=True)
    monitor = run._hw_monitor
    assert monitor is not None and monitor.started

    run.finish()
    assert monitor.finished
    assert run._hw_monitor is None  # handle releases its collector on close


def test_probe_hw_env_enables(client, app, monkeypatch):
    monkeypatch.setenv("PROBE_HW", "1")
    run = open_run(client, experiment="hw-e2e")
    assert run._hw_monitor is not None
    run.finish()


def test_explicit_flag_beats_env(client, app, monkeypatch):
    """run(hw=...) is authoritative in both directions: code the author wrote
    wins over ambient environment."""
    monkeypatch.setenv("PROBE_HW", "1")
    off = open_run(client, experiment="hw-e2e", hw=False)
    assert off._hw_monitor is None
    off.finish()

    monkeypatch.setenv("PROBE_HW", "0")
    on = open_run(client, experiment="hw-e2e", hw=True)
    assert on._hw_monitor is not None
    on.finish()


def test_non_leader_rank_starts_nothing(client, app, monkeypatch):
    monkeypatch.setenv("LOCAL_RANK", "3")
    run = open_run(client, experiment="hw-e2e", hw=True)
    assert run._hw_monitor is None
    run.finish()


# -- resume machinery -------------------------------------------------------


def test_resume_guard_is_kind_scoped(client, app):
    run = open_run(client, experiment="hw-e2e", hw=False)
    run.arm_resume_guard(100)

    with pytest.raises(errors.ValidationError):
        run.log({"loss": 1.0}, step=50, strict=True)  # training kind: guarded
    with pytest.warns(UserWarning, match="DROPPED"):
        assert run.log({"loss": 1.0}, step=50) is None  # fail-open: dropped (D6)

    # Hardware's epoch steps are invisible to the guard in BOTH directions:
    # a huge step doesn't have to clear the training floor…
    run.log_hw({"gpu_temp": 40.0}, step=29_700_000)
    # …and a small hw step doesn't trip it either (different clock entirely).
    run.log_hw({"gpu_temp": 41.0}, step=50)
    run.finish()


def test_suspect_receipt_warns_and_skips_arming(client, app):
    """A last_step in hardware's epoch range means the server predates the
    receipt hw-exclusion: arming would refuse every training step. Fail open
    with one warning (warn-never-gate)."""
    run = open_run(client, experiment="hw-e2e", hw=False)
    with pytest.warns(UserWarning, match="hardware"):
        handle = client.attach_run({"id": run.id}, heartbeat=False, resume_from_step=29_700_123)
    assert handle._resume_from_step is None  # not armed
    handle.log({"loss": 1.0}, step=5)  # would raise if armed
    run.finish()


# -- transport durability ---------------------------------------------------


def test_write_durable_false_never_journals(client, app):
    run = open_run(client, experiment="hw-e2e", hw=False)
    client.async_writes = True
    try:
        client.write(
            "POST",
            f"/v1/runs/{run.id}/metrics",
            {
                "points": [
                    {
                        "key": "hw/cpu/utilization",
                        "value": 1.0,
                        "kind": "hardware",
                        "step_index": 29_700_000,
                    }
                ]
            },
            durable=False,
        )
        # Async mode journals EVERYTHING durable — durable=False must bypass
        # the journal and go straight to the wire.
        assert list(client.journal.pending()) == []
    finally:
        client.async_writes = False
        run.finish()


def test_write_durable_false_raises_on_failure_without_journaling(client, app, monkeypatch):
    """The monitor's bounded buffer is hardware's ONLY retry: the funnel must
    surface the failure (so the buffer can hold the points) and must never
    journal them (spool space belongs to training metrics)."""

    def boom(*a, **kw):
        raise errors.RosError("outage")

    monkeypatch.setattr(client.transport, "request", boom)
    with pytest.raises(errors.RosError):
        client.write("POST", "/v1/x", {"points": []}, durable=False)
    assert list(client.journal.pending()) == []


# -- inventory --------------------------------------------------------------


def test_inventory_mints_minimal_record_when_env_ref_absent(client, app):
    run = open_run(client, experiment="hw-e2e", hw=False)
    calls = []
    orig_write = client.write

    def spy(method, path, body=None, **kw):
        calls.append((method, path, body))
        return orig_write(method, path, body, **kw)

    client.write = spy
    try:
        hw_integration.publish_inventory(
            client, run_id=run.id, env_ref=None, inventory={"gpu_count": 2}
        )
    finally:
        client.write = orig_write

    posts = [c for c in calls if c[1] == "/v1/execution-records"]
    assert len(posts) == 1
    assert posts[0][2]["hardware"] == {"gpu_count": 2}
    run.finish()


def test_inventory_skips_when_snapshot_already_pinned(client, app):
    run = open_run(client, experiment="hw-e2e", hw=False)
    calls = []
    client_write = client.write
    client.write = lambda *a, **kw: calls.append(a) or client_write(*a, **kw)
    try:
        hw_integration.publish_inventory(
            client, run_id=run.id, env_ref="abc123", inventory={"gpu_count": 2}
        )
    finally:
        client.write = client_write

    assert not any("/v1/execution-records" in str(c) for c in calls)
    run.finish()


# -- the rail rides the journal (plan 0.3, D2) --------------------------------
#
# The live audit: finish() raised on 4 of 6 ten-step runs with hardware on and
# 0 of 6 with PROBE_HW=0. The rail wrote around the journal -- metric batches
# as direct POSTs and an inventory PATCH /v1/runs/{id} from a start-up thread --
# so its writes landed on the run row while the drain was delivering the run's
# own metrics, and the metric insert's NOWAIT run-row lock answered 503
# (`app/telemetry/store.py` lock_metric_run_row_nowait -> MetricWriteBusy).
# Everything below pins the fix: hardware writes to a run are journal ops,
# delivered FIFO by the one drainer, never beside it.


class SteppingClock:
    """Every read is one hardware window later, so each tick completes the
    previous tick's window and the collector emits it (the real clock would
    need a minute per window)."""

    def __init__(self, start: float = 1_782_000_000.0):
        self.start = start
        self.t = start
        self._lock = threading.Lock()

    def __call__(self) -> float:
        with self._lock:
            self.t += HW_STEP_SECONDS
            return self.t


class FakeHwSource:
    """Production's source surface (families, sample, probe) and no hardware."""

    def __init__(self, inventory: dict | None = None, probe_seconds: float = 0.0):
        self.families = frozenset({"system"})
        self.inventory = dict(inventory or {})
        self.probe_seconds = probe_seconds

    def sample(self, ts):
        return [HwSample("hw/cpu/utilization", 12.5, {}, "mean")]

    def probe(self) -> dict:
        if self.probe_seconds:
            time.sleep(self.probe_seconds)  # NVML init / an exporter round trip
        return dict(self.inventory)


def _real_collector(monkeypatch, source, *, interval: str = "3600") -> SteppingClock:
    """Swap the autouse RecorderMonitor back for the REAL collector, driven by
    a stepping clock and one fake source. A long interval means the thread
    never ticks on its own and the test drives ``tick()``."""
    clock = SteppingClock()
    monkeypatch.setattr(
        hw_integration, "HwMonitor", functools.partial(RealHwMonitor, clock=clock)
    )
    monkeypatch.setattr(hw_integration, "build_sources", lambda: [source])
    monkeypatch.setenv("PROBE_HW_INTERVAL", interval)
    return clock


def _settle_hw_threads(timeout: float = 5.0) -> None:
    """Join every hardware thread still alive, so an assertion reads the state
    the rail left rather than one it is still writing."""
    for thread in threading.enumerate():
        if thread.name.startswith("probe-hw-") and thread is not threading.current_thread():
            thread.join(timeout)


def _direct(app, method: str, path: str) -> list:
    return [r for r in app.requests if r.method == method and r.url.path == path]


def _queued(client, method: str, path: str) -> list[dict]:
    return [
        op
        for _, op in client.journal.pending()
        if op.get("method") == method and op.get("path") == path
    ]


@pytest.fixture
def queued_client(app, tmp_path):
    """Async writes (the user default) with no background drainer, so a test
    can read the queue before finish() drains it. The detached worker cannot
    replay a fake transport, and the in-process exporter would empty the
    queue on every enqueue."""
    client = make_client(app, tmp_spool=tmp_path / "queued-spool")
    client.async_writes = True
    return client


def test_hw_points_are_journal_ops_not_direct_posts(queued_client, app, monkeypatch):
    client = queued_client
    clock = _real_collector(monkeypatch, FakeHwSource())
    run = open_run(client, experiment="hw-journal", hw=True)
    metrics = f"/v1/runs/{run.id}/metrics"
    try:
        run._hw_monitor.tick()
        run._hw_monitor.tick()  # completes the first window, which emits

        assert _direct(app, "POST", metrics) == [], "hardware went around the journal"
        ops = _queued(client, "POST", metrics)
        assert ops, "the completed window never reached the journal"
        points = [p for op in ops for p in op["body"]["points"]]
        assert {p["kind"] for p in points} == {"hardware"}
        # hw keeps its own clock: the epoch grid, not a training counter.
        assert {p["step_index"] for p in points} == {step_for(clock.start + HW_STEP_SECONDS)}
        for op in ops:
            # Stamped like every other metric op (0185 writer fence) ...
            assert op["body"]["session_id"] == run.session_id
            assert op["body"]["write_epoch"] == run.write_epoch
            # ... and best-effort: it rides the run's FIFO, never holds its close.
            assert op["blocking"] is False
    finally:
        run.finish()
    delivered = app.metric_points_posted.get(run.id, [])
    assert any(p["kind"] == "hardware" for p in delivered)


def test_hw_points_carry_the_write_epoch_current_when_they_emit(queued_client, app, monkeypatch):
    """`_recover_after_outage` moves a live handle to a new epoch; points
    emitted after it must carry the new one, not the epoch at start."""
    client = queued_client
    _real_collector(monkeypatch, FakeHwSource())
    run = open_run(client, experiment="hw-journal", hw=True)
    try:
        run.write_epoch = 4
        run._hw_monitor.tick()
        run._hw_monitor.tick()
        ops = _queued(client, "POST", f"/v1/runs/{run.id}/metrics")
        assert ops and {op["body"]["write_epoch"] for op in ops} == {4}
    finally:
        run.finish()


@pytest.mark.parametrize("refusal", ["op_ceiling", "low_disk"])
def test_a_refusing_journal_drops_hw_points_quietly(queued_client, app, monkeypatch, refusal):
    """A full queue or the low-disk floor is the journal saying there is no
    room: hardware yields -- no exception, nothing buffered for a retry that
    would only be refused again, and nothing printed: the "dropping queued
    writes" notice means the USER's writes are being lost, and these are not
    the user's."""
    client = queued_client
    _real_collector(monkeypatch, FakeHwSource())
    run = open_run(client, experiment="hw-journal", hw=True)
    metrics = f"/v1/runs/{run.id}/metrics"
    monitor = run._hw_monitor
    saved = {
        name: getattr(journal_module, name)
        for name in ("MAX_PENDING_OPS", "MIN_FREE_BYTES", "_STATVFS_EVERY")
    }
    try:
        if refusal == "op_ceiling":
            monkeypatch.setattr(journal_module, "MAX_PENDING_OPS", 1)
            # Fill the queue to its ceiling with someone else's op.
            client.journal.append_http("POST", "/v1/runs/someone-else/metrics", {"points": []})
        else:
            monkeypatch.setattr(journal_module, "MIN_FREE_BYTES", 1 << 62)
            monkeypatch.setattr(journal_module, "_STATVFS_EVERY", 1)
        before = len(client.journal.pending())
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            for _ in range(6):
                monitor.tick()  # must not raise
        assert monitor._buffer == []
        assert len(client.journal.pending()) == before
        assert _direct(app, "POST", metrics) == []
        assert [str(w.message) for w in caught] == []
        assert client.dropped_writes == 0  # the user's own writes lost nothing
    finally:
        for name, value in saved.items():
            monkeypatch.setattr(journal_module, name, value)
        run.finish()


def test_a_broken_journal_keeps_hw_points_in_the_bounded_buffer(queued_client, app, monkeypatch):
    """Not a refusal but a broken outbox (read-only state dir, ENOSPC, flock
    ENOSYS): the monitor's bounded drop-oldest buffer holds the points and the
    next tick retries them. Never a direct POST as the fallback -- that is the
    collision this rail exists to stop."""
    client = queued_client
    _real_collector(monkeypatch, FakeHwSource())
    run = open_run(client, experiment="hw-journal", hw=True)
    metrics = f"/v1/runs/{run.id}/metrics"
    monitor = run._hw_monitor
    real_append = client.journal.append_http

    def read_only(*a, **kw):
        raise OSError(errno.EROFS, "Read-only file system")

    try:
        monkeypatch.setattr(client.journal, "append_http", read_only)
        for _ in range(3):
            monitor.tick()  # must not raise
        held = len(monitor._buffer)
        assert held, "points were lost instead of held for the next tick"
        assert _direct(app, "POST", metrics) == []

        monkeypatch.setattr(client.journal, "append_http", real_append)
        monitor.tick()
        assert monitor._buffer == []
        queued = [p for op in _queued(client, "POST", metrics) for p in op["body"]["points"]]
        assert len(queued) > held  # the held windows plus the new one
    finally:
        run.finish()


def test_inventory_env_ref_patch_is_queued_behind_the_runs_writes(client, app):
    """The execution record names no run (content-addressed, idempotent), so
    it stays a direct POST -- the PATCH needs the hash the SERVER computes. The
    PATCH is the run-row write that collided, so it becomes a journal op,
    queued after whatever the run already has in flight."""
    run = open_run(client, experiment="hw-e2e", hw=False)
    run_path = f"/v1/runs/{run.id}"
    client.async_writes = True  # queue the run's own write, as the default mode does
    try:
        run.log({"loss": 1.0}, step=0)
        hw_integration.publish_inventory(
            client, run_id=run.id, env_ref=None, inventory={"gpu_count": 2}
        )
    finally:
        client.async_writes = False

    (record,) = [
        json.loads(r.content)
        for r in _direct(app, "POST", "/v1/execution-records")
    ]
    assert record["hardware"] == {"gpu_count": 2}
    content_hash = next(
        h for h, row in app.execution_records.items() if row["hardware"] == {"gpu_count": 2}
    )
    assert _direct(app, "PATCH", run_path) == [], "the env_ref PATCH raced the drain"
    pending = [op for _, op in client.journal.pending()]
    assert [(op["method"], op["path"]) for op in pending] == [
        ("POST", f"{run_path}/metrics"),
        ("PATCH", run_path),
    ]
    assert pending[1]["body"] == {"env_ref": content_hash}
    assert pending[1]["blocking"] is False

    run.finish()
    assert app.runs[run.id]["env_ref"] == content_hash


@pytest.mark.filterwarnings("ignore:probe. env_ref was queued, not confirmed")
@pytest.mark.parametrize("async_writes", [False, True], ids=["sync", "async"])
def test_inventory_never_clobbers_the_env_ref_a_snapshot_pinned(
    app, monkeypatch, snapshot_repo, tmp_path, async_writes
):
    """The rule was dead since the rail shipped: it asked the handle for an
    `env_ref` attribute Run never had, so every hw-on run minted a
    hardware-only record and PATCHed it over the snapshot's, and whichever
    PATCH landed last decided the run's code record. Queued FIFO, the
    inventory's would ALWAYS land last -- so the handle now knows what its own
    snapshot pinned, even while that PATCH is still queued (async)."""
    monkeypatch.chdir(snapshot_repo)
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "1")
    _real_collector(monkeypatch, FakeHwSource(inventory={"gpu_count": 8}))
    client = make_client(
        app,
        tmp_spool=tmp_path / "outbox",
        async_writes=async_writes,
        **({"drain_interval": 0.05} if async_writes else {}),
    )
    try:
        run = open_run(client, experiment="hw-snap", hw=True)
        snapshot_hash = next(h for h, row in app.execution_records.items() if row.get("code"))
        run.finish()
        _settle_hw_threads()
        client.flush()
    finally:
        client.close()

    assert app.runs[run.id]["env_ref"] == snapshot_hash
    pinned = [
        json.loads(r.content).get("env_ref")
        for r in _direct(app, "PATCH", f"/v1/runs/{run.id}")
    ]
    assert set(pinned) - {None} == {snapshot_hash}, pinned


class RunRowLocks:
    """Production's run-row locking, in front of the fake API.

    `app/telemetry/store.py`: a metric insert queues on the per-run series
    lock, then takes the run row `FOR NO KEY UPDATE NOWAIT` -- any other
    writer holding the row answers 503 "concurrent telemetry write"
    (MetricWriteBusy). A run-row writer (PATCH /v1/runs/{id}, a heartbeat)
    WAITS for the row, then holds it. Every write to a run holds for `hold`
    seconds, the latency that makes an overlap observable at all.

    `overlaps` counts writes to a run that ARRIVED while another write to the
    same run was in flight -- from one process, the number this fix drives to
    zero. `busy` counts the 503s actually served.
    """

    _METRICS = re.compile(r"^/v1/runs/([^/]+)/metrics$")
    _ROW = re.compile(r"^/v1/runs/([^/]+)(?:/heartbeat)?$")
    _ANY = re.compile(r"^/v1/runs/([^/]+)(?:/|$)")

    def __init__(self, inner, *, hold: float):
        self.inner = inner
        self.hold = hold
        self.overlaps = 0
        self.busy = 0
        self._guard = threading.Lock()
        self._in_flight: dict[str, int] = {}
        self._series: dict[str, threading.Lock] = {}
        self._rows: dict[str, threading.Lock] = {}

    def _locks(self, run_id: str):
        with self._guard:
            return (
                self._series.setdefault(run_id, threading.Lock()),
                self._rows.setdefault(run_id, threading.Lock()),
            )

    def __call__(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        found = self._ANY.match(path)
        if request.method == "GET" or found is None:
            return self.inner(request)
        run_id = found.group(1)
        with self._guard:
            if self._in_flight.get(run_id):
                self.overlaps += 1
            self._in_flight[run_id] = self._in_flight.get(run_id, 0) + 1
        try:
            series, row = self._locks(run_id)
            if request.method == "POST" and self._METRICS.match(path):
                with series:
                    if not row.acquire(blocking=False):
                        with self._guard:
                            self.busy += 1
                        return httpx.Response(
                            503,
                            json={"detail": "concurrent telemetry write; retry this ingest batch"},
                        )
                    try:
                        time.sleep(self.hold)
                        return self.inner(request)
                    finally:
                        row.release()
            if request.method in ("PATCH", "POST") and self._ROW.match(path):
                with row:
                    time.sleep(self.hold)
                    return self.inner(request)
            time.sleep(self.hold)
            return self.inner(request)
        finally:
            with self._guard:
                self._in_flight[run_id] -= 1


def _short_runs(
    app,
    tmp_path,
    monkeypatch,
    *,
    hw: bool | None,
    runs: int,
    locks: RunRowLocks,
    step_seconds: float = 0.0,
):
    """The live audit's shape: N runs, ten log() calls each, then finish(),
    through the default write mode (async; the in-process exporter stands in
    for the detached worker, which cannot replay a fake transport)."""
    _real_collector(
        monkeypatch,
        FakeHwSource(inventory={"cpu_count": 4}, probe_seconds=0.15),
        interval="0.05",
    )
    monkeypatch.setattr(app, "handler", locks)
    client = make_client(
        app, tmp_spool=tmp_path / "outbox", async_writes=True, drain_interval=0.05
    )
    raised, opened = [], []
    try:
        for i in range(runs):
            run = open_run(client, experiment="hw-short", name=f"short-{i}", hw=hw)
            opened.append(run)
            for step in range(10):
                run.log({"loss": 1.0 / (step + 1)}, step=step)
                if step_seconds:
                    time.sleep(step_seconds)
            try:
                run.finish()
            except Exception as exc:  # noqa: BLE001 -- the count IS the assertion
                raised.append(f"{type(exc).__name__}: {exc}")
    finally:
        _settle_hw_threads()
        client.close()
    return raised, opened


def test_hw_on_never_overlaps_writes_to_its_own_run(app, tmp_path, monkeypatch):
    locks = RunRowLocks(app.handler, hold=0.03)
    # Slow enough steps that the collector ticks mid-run: a completed window
    # is emitted and delivered, not only the inventory.
    raised, (run,) = _short_runs(
        app, tmp_path, monkeypatch, hw=True, runs=1, locks=locks, step_seconds=0.04
    )
    assert raised == []
    assert locks.overlaps == 0, f"{locks.overlaps} writes to the run overlapped"
    assert locks.busy == 0
    delivered = app.metric_points_posted.get(run.id, [])
    assert any(p["kind"] == "hardware" for p in delivered)
    assert [p for p in delivered if p["kind"] == "model"]
    inventory = app.execution_records[app.runs[run.id]["env_ref"]]
    assert inventory["hardware"] == {"cpu_count": 4}


def test_six_short_runs_with_hw_on_all_finish(app, tmp_path, monkeypatch):
    """Regression for the live bug: 4 of 6 raised with hardware on."""
    locks = RunRowLocks(app.handler, hold=0.03)
    raised, opened = _short_runs(app, tmp_path, monkeypatch, hw=True, runs=6, locks=locks)
    assert raised == [], raised
    assert locks.busy == 0 and locks.overlaps == 0
    assert [app.runs[r.id]["status"] for r in opened] == ["completed"] * 6


def test_six_short_runs_with_hw_off_all_finish(app, tmp_path, monkeypatch):
    """Negative control: the lock fake alone breaks nothing, and hw off is
    unchanged -- no collector, no hardware points, no inventory."""
    monkeypatch.setenv("PROBE_HW", "0")
    locks = RunRowLocks(app.handler, hold=0.03)
    raised, opened = _short_runs(app, tmp_path, monkeypatch, hw=None, runs=6, locks=locks)
    assert raised == [], raised
    assert locks.busy == 0
    assert all(r._hw_monitor is None for r in opened)
    points = [p for r in opened for p in app.metric_points_posted.get(r.id, [])]
    assert points and all(p["kind"] == "model" for p in points)
    assert not any(row.get("hardware") for row in app.execution_records.values())
    assert [app.runs[r.id]["status"] for r in opened] == ["completed"] * 6


# -- review of #1999 ------------------------------------------------------------


def _settle_hw_threads_named(name: str, timeout: float = 5.0) -> None:
    for thread in threading.enumerate():
        if thread.name == name:
            thread.join(timeout)


def _wait_for(predicate, timeout: float = 5.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return predicate()


def test_a_refused_hw_point_records_no_capture_gap_but_a_users_write_does(
    app, tmp_path, monkeypatch
):
    """A capture gap and the "dropping queued writes" notice both say the
    USER's data is being lost (and lane 0.1 reports them on the run). A
    refused hardware batch is neither. Control: the user's own write refused
    by the same floor still records its gap and prints its notice."""
    _real_collector(monkeypatch, FakeHwSource())
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, drain_interval=3600)
    run = open_run(client, experiment="hw-gap", hw=True)
    saved = {name: getattr(journal_module, name) for name in ("MIN_FREE_BYTES", "_STATVFS_EVERY")}

    def gaps() -> int:
        return sum(len(p.get("gaps") or []) for p in client.journal.producer_report())

    # One of the run's writes queued while there was room: under the floor its
    # next write can then not be sent around it (plan 1.5's direct send), so
    # the control below is refused, as every write under the floor was before.
    # Paused, or the exporter delivers it first and the lane is empty again.
    client.journal.pause()
    run.log({"loss": 0.5}, step=0)
    try:
        monkeypatch.setattr(journal_module, "MIN_FREE_BYTES", 1 << 62)
        monkeypatch.setattr(journal_module, "_STATVFS_EVERY", 1)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            for _ in range(4):
                run._hw_monitor.tick()
            assert gaps() == 0 and [str(w.message) for w in caught] == []

            run.log({"loss": 1.0}, step=1)  # the control: real data refused
            # >= 1, not == 1: today the journal AND Client._enqueue each note
            # the same refusal (lane 0.1's concern, not this rail's).
            assert gaps() >= 1
            assert any("dropping queued writes" in str(w.message) for w in caught)
    finally:
        for name, value in saved.items():
            monkeypatch.setattr(journal_module, name, value)
        run.finish()
        client.close()


@pytest.mark.parametrize("async_writes", [False, True], ids=["sync", "async"])
def test_hw_points_reach_the_server_while_the_run_is_live(app, tmp_path, monkeypatch, async_writes):
    """Live charts in both write modes. Sync (`PROBE_ASYNC=0`) has no drainer
    while the run lives, so a queued point would sit on disk until finish()
    (and be stranded by a SIGKILL): there the rail stays direct."""
    _real_collector(monkeypatch, FakeHwSource())
    client = make_client(
        app,
        tmp_spool=tmp_path / "outbox",
        async_writes=async_writes,
        **({"drain_interval": 0.05} if async_writes else {}),
    )
    run = open_run(client, experiment="hw-live", hw=True)
    try:
        run._hw_monitor.tick()
        run._hw_monitor.tick()

        def live() -> list:
            points = app.metric_points_posted.get(run.id, [])
            return [p for p in points if p["kind"] == "hardware"]

        assert _wait_for(lambda: live()), "hardware points never left the machine mid-run"
        assert all(p["step_index"] >= hw_integration.SUSPECT_RESUME_FLOOR for p in live())
    finally:
        run.finish()
        client.close()


@pytest.mark.parametrize("async_writes", [False, True], ids=["sync", "async"])
def test_a_run_shorter_than_one_interval_records_its_hardware(app, tmp_path, monkeypatch, async_writes):
    """A run over before the collector's first tick (interval 15 s; here an
    hour) recorded no hardware: windows went out only once closed, and the
    close only flushed. Found by the environment suite (lane E3): a job under
    a minute had no hardware at all. Now the close's last pass samples on the
    collector thread and sends the open window, queued ahead of the close."""
    _real_collector(monkeypatch, FakeHwSource())
    client = make_client(
        app,
        tmp_spool=tmp_path / "outbox",
        async_writes=async_writes,
        **({"drain_interval": 0.05} if async_writes else {}),
    )
    try:
        run = open_run(client, experiment="hw-short-lived", hw=True)
        run.log({"loss": 0.5}, step=0)
        run.finish()
    finally:
        client.close()
    hardware = [p for p in app.metric_points_posted.get(run.id, []) if p["kind"] == "hardware"]
    assert [(p["key"], p["value"]) for p in hardware] == [("hw/cpu/utilization", 12.5)]
    assert hardware[0]["step_index"] >= hw_integration.SUSPECT_RESUME_FLOOR
    assert app.runs[run.id]["status"] == "completed"


def test_an_abandoned_run_with_hw_on_stops_its_beat_and_its_collector(client, app, monkeypatch):
    """test_run_heartbeat.py::test_dropping_the_handle_stops_the_beat, with
    hardware ON (the user default). The collector thread outlives any caller;
    had it held the Run strongly, the handle would never be collected and its
    heartbeat would beat until the process exits."""
    _real_collector(monkeypatch, FakeHwSource(inventory={"cpu_count": 4}))
    run = open_run(client, experiment="e", name="r", heartbeat=False, hw=True)
    assert run._hw_monitor is not None
    run.start_heartbeat(0.01)
    beat = run._hb_thread
    collector = run._hw_monitor._thread
    rid = run.id  # captured up front so no closure below pins the handle
    assert _wait_for(lambda: app.run_heartbeats.get(rid, 0) >= 1)
    _settle_hw_threads_named("probe-hw-inventory")
    del run
    gc.collect()
    beat.join(timeout=5)
    collector.join(timeout=5)
    assert not beat.is_alive(), "the Run is pinned: its heartbeat never stops"
    assert not collector.is_alive(), "the collector outlived its abandoned run"


@pytest.mark.filterwarnings("ignore:probe. env_ref was queued, not confirmed")
@pytest.mark.parametrize("async_writes", [False, True], ids=["sync", "async"])
def test_a_later_snapshot_beats_the_hardware_inventory(
    app, monkeypatch, snapshot_repo, tmp_path, async_writes
):
    """Opened without the auto-snapshot, the inventory pins its record first;
    a snapshot() the user takes afterwards must win in both write modes. Sync
    sends both PATCHes direct in that order; async queues them in that order.
    (A queued sync-mode inventory PATCH would land at finish(), AFTER the
    snapshot's direct one.)"""
    monkeypatch.chdir(snapshot_repo)
    _real_collector(monkeypatch, FakeHwSource(inventory={"cpu_count": 4}))
    client = make_client(
        app,
        tmp_spool=tmp_path / "outbox",
        async_writes=async_writes,
        **({"drain_interval": 3600} if async_writes else {}),
    )
    try:
        run = open_run(client, experiment="e", name="r", hw=True, snapshot=False)
        _settle_hw_threads_named("probe-hw-inventory")  # inventory pinned first
        run.snapshot()
        snapshot_hash = next(h for h, row in app.execution_records.items() if row.get("code"))
        run.finish()
        client.flush()
    finally:
        client.close()
    assert app.runs[run.id]["env_ref"] == snapshot_hash


def test_a_slow_inventory_post_never_holds_finish(app, tmp_path, monkeypatch):
    """The inventory's execution-record POST can take the transport's full
    30 s. finish() waits for it at most briefly; the PATCH it queues later
    never holds a close anyway."""
    _real_collector(monkeypatch, FakeHwSource(inventory={"cpu_count": 4}))
    inner = app.handler
    release = threading.Event()

    def slow(request: httpx.Request):
        if request.url.path == "/v1/execution-records" and b"cpu_count" in request.content:
            release.wait(10.0)
        return inner(request)

    monkeypatch.setattr(app, "handler", slow)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, drain_interval=0.05)
    try:
        run = open_run(client, experiment="e", name="r", hw=True)
        run.log({"loss": 1.0}, step=0)
        started = time.monotonic()
        run.finish()
        took = time.monotonic() - started
        assert took < 1.0, f"finish() took {took:.2f}s behind the inventory POST"
        assert app.runs[run.id]["status"] == "completed"
    finally:
        release.set()
        _settle_hw_threads_named("probe-hw-inventory")
        client.close()


def test_a_finished_runs_monitor_is_not_kept_alive_by_its_run(app, tmp_path, monkeypatch):
    """The abandoned-run finalizer holds only the collector's stop flag: a
    finished run that the caller keeps referenced must not pin its monitor."""
    import weakref

    monkeypatch.setenv("LOCAL_RANK", "0")
    monkeypatch.delenv("PROBE_HW", raising=False)
    _real_collector(monkeypatch, FakeHwSource(inventory={"cpu_count": 4}))
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, drain_interval=3600)
    runs, monitors = [], []
    for i in range(5):
        run = open_run(client, experiment="e", name=f"r{i}", hw=True, snapshot=False)
        monitors.append(weakref.ref(run._hw_monitor))
        run.finish()
        runs.append(run)
    _settle_hw_threads()
    gc.collect()
    client.close()
    assert [m() for m in monitors] == [None] * 5


@pytest.mark.filterwarnings("ignore:probe. env_ref was queued, not confirmed")
@pytest.mark.parametrize("async_writes", [False, True], ids=["sync", "async"])
def test_an_abandoned_run_keeps_the_snapshot_its_handle_pinned(app, monkeypatch, snapshot_repo, tmp_path, async_writes):
    """snapshot() pins while the inventory's record POST is in flight, then the
    handle is dropped: the inventory must not read "run gone" as "nothing
    pinned" and overwrite the snapshot's env_ref."""
    monkeypatch.setenv("LOCAL_RANK", "0")
    monkeypatch.delenv("PROBE_HW", raising=False)
    monkeypatch.chdir(snapshot_repo)
    _real_collector(monkeypatch, FakeHwSource(inventory={"cpu_count": 4}))
    inner = app.handler
    in_post, release = threading.Event(), threading.Event()

    def slow(request):
        if request.url.path == "/v1/execution-records" and b"cpu_count" in request.content:
            in_post.set()
            release.wait(10)
        return inner(request)

    monkeypatch.setattr(app, "handler", slow)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=async_writes,
                         **({"drain_interval": 3600} if async_writes else {}))
    run = open_run(client, experiment="e", name="r", hw=True, snapshot=False)
    rid = run.id
    assert in_post.wait(5)
    run.snapshot()
    snapshot_hash = next(h for h, row in app.execution_records.items() if row.get("code"))
    del run
    gc.collect()
    release.set()
    _settle_hw_threads()
    client.flush()
    client.close()
    assert app.runs[rid]["env_ref"] == snapshot_hash
