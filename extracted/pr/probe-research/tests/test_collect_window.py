"""The collect window (plan T2): a writer stamps `send_after` on its mergeable telemetry ops;
the detached worker and the in-process thread hold a run's lane until then; `finish()`,
`flush()` and older workers never wait for it."""

from __future__ import annotations

import json
import os
import signal
import time

import pytest

from probe.sdk.client.client import Client
from probe.sdk.delivery.journal.journal import Journal
from probe.sdk.delivery.outbox.drain import window as window_module
from probe.sdk.delivery.outbox.drain.drain import drain
from probe.sdk.delivery.outbox.drain.window import CollectWindow, LaneLoad, send_interval, stamp_send_after

from tests.conftest import make_client, open_run
from tests.fake_delivery_server import point_values, running_server, wait_for

RUN = "6f1c1d1e-0000-4000-8000-0000000000a1"
OTHER = "6f1c1d1e-0000-4000-8000-0000000000b2"


def _metric_op(run=RUN, value=1.0, step=0, **extra) -> dict:
    op = {
        "kind": "http",
        "method": "POST",
        "path": f"/v1/runs/{run}/metrics",
        "body": {"points": [{"key": "loss", "value": value, "step_index": step}]},
    }
    op.update(extra)
    return op


# -- the writer's stamp ----------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "expected"),
    [(None, 5.0), ("", 5.0), ("0", 0.0), ("2.5", 2.5), ("100", 60.0), ("-1", 0.0), ("soon", 5.0), ("nan", 5.0)],
)
def test_the_window_is_read_from_the_writers_env(monkeypatch, raw, expected):
    if raw is None:
        monkeypatch.delenv("PROBE_SEND_INTERVAL_SEC", raising=False)
    else:
        monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", raw)
    assert send_interval() == expected


def test_only_mergeable_telemetry_is_stamped():
    stamped = _metric_op()
    stamp_send_after(stamped, 5.0)
    assert stamped["send_after"] == pytest.approx(time.time() + 5.0, abs=1.0)
    step = {"kind": "http", "method": "POST", "path": f"/v1/runs/{RUN}/steps", "body": {"step_index": 3}}
    stamp_send_after(step, 5.0)
    assert "send_after" in step
    for never in (
        _metric_op(run="r-1"),  # a petname, not an id: never merged
        {**_metric_op(), "method": "PATCH"},
        {**_metric_op(), "correlation": "c-1"},
        {**_metric_op(), "kind": "upload"},
        {**_metric_op(), "body": {"points": [{"key": "loss", "value": 1.0}]}},  # no step, no clock
        {"kind": "http", "method": "POST", "path": f"/v1/runs/{RUN}/steps", "body": {"step_index": True}},
    ):
        stamp_send_after(never, 5.0)
        assert "send_after" not in never, never


def test_window_zero_leaves_the_op_byte_identical():
    op = _metric_op()
    before = json.dumps(op, sort_keys=True)
    stamp_send_after(op, 0.0)
    assert json.dumps(op, sort_keys=True) == before


def test_a_journaled_metric_carries_its_writers_window(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "3")
    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", f"/v1/runs/{RUN}/metrics", _metric_op()["body"])
    journal.append_http("PATCH", f"/v1/runs/{RUN}", {"status": "completed"}, admitted=True)
    (_, metric), (_, close) = journal.pending()
    assert metric["send_after"] == pytest.approx(time.time() + 3.0, abs=1.0)
    assert "send_after" not in close


# -- when a lane waits -------------------------------------------------------------------------


def _lane(*ops):
    return [(type("P", (), {"name": f"{n:04d}.json"})(), op) for n, op in enumerate(ops)]


def test_a_lane_waits_until_its_heads_send_after():
    window = CollectWindow(clock=lambda: 1000.0)
    held = window.hold(_lane(_metric_op(send_after=1004.0), _metric_op(send_after=1004.5)))
    assert held is not None and held.wait == pytest.approx(4.0)
    assert held.load.points == 2


@pytest.mark.parametrize(
    "lane",
    [
        [_metric_op(send_after=999.0)],  # past due
        [_metric_op()],  # an older writer's op, or window 0
        [_metric_op(send_after=1004.0), {**_metric_op(), "method": "PATCH"}],  # a close or PATCH behind it
        [_metric_op(send_after=1004.0, attempts=1)],  # a retry goes now (and alone)
        [_metric_op(send_after=1004.0), _metric_op(send_after=1004.0, attempts=2)],
        [_metric_op(send_after=1000.0 + 3600)],  # a wall clock stepped back an hour
    ],
)
def test_a_lane_sends_now(lane):
    assert CollectWindow(clock=lambda: 1000.0).hold(_lane(*lane)) is None


def test_a_lane_holding_a_full_post_sends_now(monkeypatch):
    from probe.sdk.delivery.outbox.drain import coalesce

    monkeypatch.setattr(coalesce, "MERGE_MAX_POINTS", 3)
    window = CollectWindow(clock=lambda: 1000.0)
    assert window.hold(_lane(*[_metric_op(send_after=1004.0)] * 2)) is not None
    assert window.hold(_lane(*[_metric_op(send_after=1004.0)] * 3)) is None


def test_a_full_load_counts_steps_and_bytes(monkeypatch):
    from probe.sdk.delivery.outbox.drain import coalesce

    monkeypatch.setattr(coalesce, "STEPS_MAX", 2)
    load = LaneLoad()
    step = {"body": {"step_index": 1}}
    load.add(step, 10)
    assert not load.full
    load.add(step, 10)
    assert load.full


# -- drain() with and without a window ---------------------------------------------------------


class _Recorder:
    def __init__(self):
        self.calls: list = []
        self.settings = type("S", (), {"token": "t", "ingest_token": None, "base_url": "http://test"})()
        outer = self

        class _Transport:
            def request(self, method, path, json_body=None, **kw):
                outer.calls.append((method, path, json_body))
                return {}

        self.transport = _Transport()

    def close(self):
        pass


def _journal_with(tmp_path, monkeypatch, *, window: str, runs=(RUN,)) -> Journal:
    monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", window)
    journal = Journal(tmp_path / "outbox", context={"name": None, "base_url": "http://test"})
    for step in range(3):
        for run in runs:
            journal.append_http("POST", f"/v1/runs/{run}/metrics", _metric_op(run, step=step)["body"])
    return journal


def test_a_drainers_pass_holds_a_run_inside_its_window(tmp_path, monkeypatch):
    journal = _journal_with(tmp_path, monkeypatch, window="5")
    recorder = _Recorder()
    report = drain(journal, client_factory=lambda ctx: recorder, window=CollectWindow())
    assert recorder.calls == []
    assert (report.delivered, report.deferred, report.remaining) == (0, 3, 3)
    assert 4.0 < report.send_in <= 5.0
    assert report.deferred_loads[RUN].points == 3


def test_finish_and_flush_never_wait_for_the_window(tmp_path, monkeypatch):
    """No `window`: `finish()`'s barrier, `flush()` and `probe outbox drain` send now."""
    journal = _journal_with(tmp_path, monkeypatch, window="5")
    recorder = _Recorder()
    report = drain(journal, client_factory=lambda ctx: recorder)
    assert report.delivered == 3 and report.deferred == 0
    assert len(recorder.calls) == 1, "the three rows still ride in one POST"


def test_a_due_window_sends_the_whole_lane_in_one_post(tmp_path, monkeypatch):
    journal = _journal_with(tmp_path, monkeypatch, window="5")
    recorder = _Recorder()
    later = CollectWindow(clock=lambda: time.time() + 6.0)
    report = drain(journal, client_factory=lambda ctx: recorder, window=later)
    assert report.delivered == 3 and len(recorder.calls) == 1


def test_window_zero_drains_as_before(tmp_path, monkeypatch):
    journal = _journal_with(tmp_path, monkeypatch, window="0")
    recorder = _Recorder()
    report = drain(journal, client_factory=lambda ctx: recorder, window=CollectWindow())
    assert report.delivered == 3 and report.deferred == 0 and report.send_in is None


def test_one_runs_window_never_holds_another_run(tmp_path, monkeypatch):
    journal = _journal_with(tmp_path, monkeypatch, window="5")
    monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "0")
    journal.append_http("POST", f"/v1/runs/{OTHER}/metrics", _metric_op(OTHER)["body"])
    recorder = _Recorder()
    report = drain(journal, client_factory=lambda ctx: recorder, window=CollectWindow())
    assert [path for _, path, _ in recorder.calls] == [f"/v1/runs/{OTHER}/metrics"]
    assert report.deferred == 3


def test_a_queued_close_sends_its_run_now(tmp_path, monkeypatch):
    journal = _journal_with(tmp_path, monkeypatch, window="5")
    journal.append_http("PATCH", f"/v1/runs/{RUN}", {"status": "completed"}, admitted=True)
    recorder = _Recorder()
    report = drain(journal, client_factory=lambda ctx: recorder, window=CollectWindow())
    assert report.deferred == 0 and report.delivered == 4
    assert [method for method, _, _ in recorder.calls] == ["POST", "PATCH"]


def test_a_close_waiting_for_the_lock_sends_every_lane_now(tmp_path, monkeypatch):
    from probe._shared import oscompat

    journal = _journal_with(tmp_path, monkeypatch, window="5")
    want = open(journal.drain_want, "a+")
    oscompat.flock(want.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
    try:
        recorder = _Recorder()
        report = drain(journal, client_factory=lambda ctx: recorder, window=CollectWindow())
    finally:
        want.close()
    assert report.deferred == 0 and report.delivered == 3


def test_an_older_writers_op_in_the_lane_sends_it_now(tmp_path, monkeypatch):
    journal = _journal_with(tmp_path, monkeypatch, window="5")
    monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "0")  # an older release stamps nothing
    journal.append_http("POST", f"/v1/runs/{RUN}/metrics", _metric_op(step=9)["body"])
    recorder = _Recorder()
    report = drain(journal, client_factory=lambda ctx: recorder, window=CollectWindow())
    assert report.delivered == 4 and report.deferred == 0


# -- the drainer's sleep -----------------------------------------------------------------------


def test_the_sleep_wakes_for_a_write_that_must_go_now(tmp_path, monkeypatch):
    journal = _journal_with(tmp_path, monkeypatch, window="5")
    seen = {(str(journal.dir), path.name) for path, _ in journal.pending()}
    monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "0")
    started = time.monotonic()
    import threading

    threading.Timer(0.3, lambda: journal.append_http("POST", f"/v1/runs/{OTHER}/metrics", _metric_op(OTHER)["body"])).start()
    CollectWindow().wait(journal, seconds=5.0, seen=seen, skip=set(), loads={RUN: LaneLoad(points=3)})
    assert time.monotonic() - started < 2.0


def test_the_sleep_ignores_writes_inside_the_window(tmp_path, monkeypatch):
    journal = _journal_with(tmp_path, monkeypatch, window="5")
    seen = {(str(journal.dir), path.name) for path, _ in journal.pending()}
    import threading

    timer = threading.Timer(0.2, lambda: journal.append_http("POST", f"/v1/runs/{RUN}/metrics", _metric_op(step=7)["body"]))
    timer.start()
    started = time.monotonic()
    CollectWindow().wait(journal, seconds=1.0, seen=seen, skip=set(), loads={RUN: LaneLoad(points=3)})
    assert time.monotonic() - started >= 0.95


def test_a_wait_held_only_by_backoffs_looks_once_a_second(tmp_path, monkeypatch):
    """Review of #3785, I7: each look lists ops/, and a run backing off may have a long queue;
    while no window holds the wait it looks every `BACKOFF_LOOK_SECONDS`, not every 0.25 s."""
    journal = _journal_with(tmp_path, monkeypatch, window="5")
    seen = {(str(journal.dir), path.name) for path, _ in journal.pending()}
    looks: list = []
    real_look = CollectWindow._look
    monkeypatch.setattr(CollectWindow, "_look", lambda self, *a: looks.append(1) or real_look(self, *a))
    CollectWindow().wait(journal, seconds=2.2, seen=seen, skip={RUN}, loads={})
    assert 1 <= len(looks) <= 3, f"{len(looks)} looks in 2.2 s"


@pytest.mark.parametrize("held", [True, False], ids=["window-held", "backoff-only"])
def test_a_short_volume_ends_a_window_wait_but_not_a_backoff(tmp_path, monkeypatch, held):
    """Review of #3785, C6, and its adversarial review: below the free-space floor a held window
    ends at once (the writer sends around an empty queue only); a backoff wait stays one, or a
    drainer would run a pass every second through the outage that filled the disk."""
    journal = _journal_with(tmp_path, monkeypatch, window="5")
    seen = {(str(journal.dir), path.name) for path, _ in journal.pending()}
    monkeypatch.setattr(window_module, "is_short_of_disk", lambda j: True)
    started = time.monotonic()
    loads = {RUN: LaneLoad(points=3)} if held else {}
    CollectWindow().wait(journal, seconds=1.5, seen=seen, skip=set() if held else {RUN}, loads=loads)
    took = time.monotonic() - started
    assert (took < 0.6) if held else (took >= 1.4), took


# -- end to end ---------------------------------------------------------------------------------


def test_finish_is_not_delayed_by_the_window(app, tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "30")
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="window")
    for step in range(20):
        run.log({"loss": 1.0 / (step + 1)}, step=step)
    started = time.monotonic()
    run.finish()
    assert time.monotonic() - started < 5.0, "finish() waited for the 30 s window"
    assert not [op for _, op in client.journal.pending() if op.get("run_ref") == run.id]


@pytest.fixture
def worker_env(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_process_test")
    monkeypatch.setenv("PROBE_OUTBOX_LINGER_S", "30")
    for name in ("PROBE_ASYNC", "PROBE_OUTBOX_DIR", "PROBE_EXPORT_INTERVAL_SEC"):
        monkeypatch.delenv(name, raising=False)


def _worker_pid(queue) -> int | None:
    try:
        return int(json.loads((queue / ".worker-caps.json").read_text())["pid"])
    except (OSError, ValueError, KeyError, TypeError):
        return None


def test_two_writers_with_different_windows_share_one_worker(worker_env, tmp_path, monkeypatch):
    """Outside voice O6: the window is each WRITER's, stamped on its ops, never the worker's env.
    Writer A (window 0) is delivered at once; writer B (5 s) waits about 5 s; one worker."""
    with running_server() as server:
        monkeypatch.setenv("PROBE_BASE_URL", server.url)
        outbox = tmp_path / "outbox"
        monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "5")
        writer_b = Client(async_writes=True, journal=Journal(outbox, context={"name": None, "base_url": server.url}))
        monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "0")
        writer_a = Client(async_writes=True, journal=Journal(outbox, context={"name": None, "base_url": server.url}))
        queue = writer_a.journal.dir
        assert writer_b.journal.dir == queue
        try:
            monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "5")
            b_at = time.monotonic()
            writer_b.write("POST", f"/v1/runs/{OTHER}/metrics", _metric_op(OTHER, value=2.0)["body"])
            assert wait_for(lambda: _worker_pid(queue) is not None, 15), "no worker started"
            worker = _worker_pid(queue)
            time.sleep(0.5)
            monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "0")
            a_at = time.monotonic()
            writer_a.write("POST", f"/v1/runs/{RUN}/metrics", _metric_op(RUN, value=1.0)["body"])
            assert wait_for(lambda: 1.0 in point_values(server), 10)
            a_took = time.monotonic() - a_at
            assert 2.0 not in point_values(server), "B's write left inside its window"
            assert wait_for(lambda: 2.0 in point_values(server), 15)
            b_took = time.monotonic() - b_at
            # Bounds with room for a busy shared box: A goes well inside B's window, B not before it.
            assert a_took < 3.0, a_took
            assert 4.0 <= b_took < 12.0, b_took
            assert _worker_pid(queue) == worker, "one worker served both writers"
        finally:
            pid = _worker_pid(queue)
            if pid:
                try:
                    os.kill(pid, getattr(signal, "SIGKILL", signal.SIGTERM))  # Windows: TerminateProcess
                except OSError:
                    pass


def test_the_in_process_thread_sleeps_through_a_stalled_run(worker_env, tmp_path, monkeypatch):
    """Audit C3 / R4: during a 503 outage the thread used to run a drain pass per `log()` (each
    wake skipped the stalled run and rescanned the queue). It now sleeps on the run's backoff."""
    from probe.sdk.delivery.outbox.drainers import in_process

    passes: list[float] = []
    real_drain = in_process.drain

    def counting_drain(*a, **k):
        passes.append(time.monotonic())
        return real_drain(*a, **k)

    monkeypatch.setattr(in_process, "drain", counting_drain)
    monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "0")
    with running_server() as server:
        server.unavailable = True
        client = Client(
            base_url=server.url,
            token="probe_pat_process_test",
            async_writes=True,
            drain_interval=1.0,
            journal=Journal(tmp_path / "outbox", context={"name": None, "base_url": server.url}),
        )
        try:
            for step in range(100):
                client.write("POST", f"/v1/runs/{RUN}/metrics", _metric_op(step=step)["body"])
                time.sleep(0.02)
            assert len(passes) <= 6, f"{len(passes)} passes for 100 writes in 2 s of outage"
        finally:
            client.close(timeout=1.0)
    assert window_module.LOOK_SECONDS <= 0.25


def test_the_in_process_thread_sees_another_clients_write_during_a_long_backoff(worker_env, tmp_path, monkeypatch):
    """Review I1: the thread slept on its own wake event through a run's backoff (up to 300 s), so
    a write another client queued to a HEALTHY run waited for it: 13 s against 0.1 s before the
    window. The thread now looks at the queue while it waits."""
    from probe.sdk.delivery.outbox import drainers

    monkeypatch.setattr(drainers.detached, "maybe_spawn", lambda d=None: False)  # only the thread delivers
    monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "0")
    with running_server() as server:
        monkeypatch.setenv("PROBE_BASE_URL", server.url)
        server.refusing[RUN] = "30"  # RUN backs off for 30 s
        outbox = tmp_path / "outbox"
        context = {"name": None, "base_url": server.url}
        thread_client = Client(
            base_url=server.url,
            token="probe_pat_process_test",
            async_writes=True,
            drain_interval=1.0,
            journal=Journal(outbox, context=context),
        )
        other = Client(async_writes=True, auto_drain=True, journal=Journal(outbox, context=context))
        try:
            thread_client.write("POST", f"/v1/runs/{RUN}/metrics", _metric_op(RUN)["body"])
            assert wait_for(lambda: server.count(f"{RUN}/metrics") >= 1, 10), "RUN was never tried"
            time.sleep(1.0)  # the thread is asleep on RUN's backoff now
            wrote_at = time.monotonic()
            other.write("POST", f"/v1/runs/{OTHER}/metrics", _metric_op(OTHER, value=2.0)["body"])
            landed = wait_for(lambda: 2.0 in point_values(server), 10)
            took = time.monotonic() - wrote_at
            assert landed, "the healthy run's write waited for another run's backoff"
            assert took < 4.0, took
        finally:
            thread_client.close(timeout=1.0)


@pytest.mark.parametrize(
    ("named", "env", "window"),
    [(1.0, None, 1.0), (None, "0.5", 0.5), (30.0, None, 5.0), (None, None, 5.0)],
    ids=["drain_interval", "env", "longer-than-the-window", "none-named"],
)
def test_an_explicit_drain_interval_caps_the_window(app, tmp_path, monkeypatch, named, env, window):
    """Review I18: a writer that asked for delivery every N seconds (`drain_interval`,
    `PROBE_EXPORT_INTERVAL_SEC`) is held at most N, not the 5 s window. A writer that named
    none keeps the window."""
    monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "5")
    if env is None:
        monkeypatch.delenv("PROBE_EXPORT_INTERVAL_SEC", raising=False)
    else:
        monkeypatch.setenv("PROBE_EXPORT_INTERVAL_SEC", env)
    kwargs = {"drain_interval": named} if named is not None else {"auto_drain": False}
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, **kwargs)
    try:
        before = time.time()
        client.journal.append_http("POST", f"/v1/runs/{RUN}/metrics", _metric_op()["body"])
        [(_, op)] = client.journal.pending()
        assert op["send_after"] - before == pytest.approx(window, abs=0.5)
    finally:
        client.close(timeout=1.0)


def test_the_shipped_defaults_end_to_end(worker_env, tmp_path, monkeypatch):
    """Review test gap: the suite pins window 0 and per-op fsync, so the shipped defaults (a 5 s
    window, the timed fsync) never ran end to end. A writer at both, a real detached worker:
    its rows go out together after about the window, and the flusher took their fsyncs."""
    from probe.sdk.delivery.journal import flusher as flusher_module

    if os.name == "nt":
        pytest.skip("Windows defaults to the per-op fsync")
    monkeypatch.delenv("PROBE_SEND_INTERVAL_SEC", raising=False)
    monkeypatch.delenv("PROBE_OUTBOX_FSYNC", raising=False)
    monkeypatch.setattr(flusher_module, "_FLUSHER", None)  # this test's own flusher
    with running_server(features=("steps_batch",)) as server:
        monkeypatch.setenv("PROBE_BASE_URL", server.url)
        client = Client(async_writes=True, journal=Journal(tmp_path / "outbox", context={"name": None, "base_url": server.url}))
        queue = client.journal.dir
        try:
            started = time.monotonic()
            for step in range(20):
                client.write("POST", f"/v1/runs/{RUN}/metrics", _metric_op(value=float(step), step=step)["body"])
                client.write("POST", f"/v1/runs/{RUN}/steps", {"step_index": step, "attributes": {"phase": "train"}})
            flusher = flusher_module._FLUSHER
            assert flusher is not None and flusher._thread is not None, "log() left its fsyncs to the flusher"
            assert wait_for(lambda: len(point_values(server)) == 20, 20), point_values(server)
            took = time.monotonic() - started
            assert 4.0 <= took < 15.0, took

            def steps_landed() -> list:
                bodies = [body for _, path, body, _ in server.requests() if path.endswith("/steps/batch")]
                return [step["step_index"] for body in bodies for step in (body or {}).get("steps") or []]

            assert wait_for(lambda: sorted(steps_landed()) == list(range(20)), 10), steps_landed()
            assert server.count("/metrics") <= 2 and 1 <= server.count("/steps/batch") <= 2
            assert server.count(f"{RUN}/steps") == 0, "no step record went alone"
            assert wait_for(lambda: not flusher._paths and not flusher._in_flight, 3), "and forced them to disk"
        finally:
            pid = _worker_pid(queue)
            if pid:
                try:
                    os.kill(pid, getattr(signal, "SIGKILL", signal.SIGTERM))  # Windows: TerminateProcess
                except OSError:
                    pass
