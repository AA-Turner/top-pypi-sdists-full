"""A run's close gets the drain lock in seconds, whatever the worker is sending.

One pass held the outbox's drain lock from its scan to its status write, so a
`finish()` waited behind every upload and every write of the pass: ~400 s per
run behind a swarm's 10k queued ops (#3618, F31), against its 600 s cap. Now a
pass lets go of the lock while it waits on the network for an upload (holding
that run's own lock, so no other drain sends the run meanwhile), and between two
ops when a close says it is waiting, or once it has held the lock
`PASS_HOLD_SECONDS`. These pin that the closes get through, and the parts that
matter more: no op goes twice, and each run's ops still go in queue order.
"""

from __future__ import annotations

import json
import os
import threading
import time
import uuid
from types import SimpleNamespace

import pytest

from probe._shared import oscompat
from probe.sdk import errors
from probe.sdk import journal as jm
from probe.sdk.journal import Journal, _DrainHold, _take_drain_lock, drain
from probe.sdk.run import Run

from tests.conftest import make_client
from tests.test_outbox import seeded_run


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    monkeypatch.delenv("PROBE_FINISH_TIMEOUT_SEC", raising=False)
    monkeypatch.delenv("PROBE_UPLOAD_WORKERS", raising=False)
    # Each window file goes on its own worker (`upload_fingerprinted`), which
    # the fake below can hold; the many-file doors are pinned elsewhere.
    monkeypatch.setenv("PROBE_UPLOAD_MANY", "0")
    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)


def run_id(n: int) -> str:
    return str(uuid.UUID(int=n))


class Server:
    """The worker's server: every request in arrival order, ``delay`` seconds
    each; an upload whose name is gated waits until its gate opens."""

    def __init__(self, *, delay: float = 0.0, upload_delay: float = 0.0):
        self.settings = SimpleNamespace(base_url=f"http://server-{uuid.uuid4().hex}")
        self.delay, self.upload_delay = delay, upload_delay
        self.lock = threading.Lock()
        self.log: list[tuple] = []
        self.gates: dict[str, threading.Event] = {}
        self.started: dict[str, threading.Event] = {}
        self.down = threading.Event()
        #: Upload names the server refuses for good (a 422), after their gate.
        self.refuse: set[str] = set()
        self.transport = SimpleNamespace(request=self._request)

    def gate(self, name: str) -> threading.Event:
        self.gates[name] = threading.Event()
        self.started[name] = threading.Event()
        return self.gates[name]

    def upload_fingerprinted(self, anchor, anchor_id, name, path, *, digest, size, **_kw):
        if name in self.started:
            self.started[name].set()
            assert self.gates[name].wait(60), f"{name} was never let through"
        if self.upload_delay:
            time.sleep(self.upload_delay)
        if name in self.refuse:
            raise errors.ValidationError("refused for the test", status=422)
        with self.lock:
            self.log.append(("upload", anchor_id, name))
        return {"id": f"a-{name}", "name": name, "status": "complete", "content_hash": digest}

    def _request(self, method, path, *, json_body=None, **_kw):
        if self.down.is_set():
            raise errors.ServerError("down for the test", status=503)
        if self.delay:
            time.sleep(self.delay)
        with self.lock:
            self.log.append(("http", path.split("/")[3], method, path, json.dumps(json_body, sort_keys=True)))
        return SimpleNamespace(content=b"{}", json=lambda: {}, status_code=200)

    def of_run(self, run: str) -> list[tuple]:
        with self.lock:
            return [entry for entry in self.log if entry[1] == run]


def queue_upload(queue: Journal, tmp_path, run: str, name: str, size: int = 64) -> None:
    src = tmp_path / f"src-{uuid.uuid4().hex}"
    with open(src, "wb") as handle:
        handle.truncate(size)  # sparse: a 30 MiB file costs no disk
    queue.append_upload(anchor="run", anchor_id=run, name=name, src_path=str(src), run_ref=run)


def queue_metric(queue: Journal, run: str, step: int) -> None:
    queue.append_http(
        "POST", f"/v1/runs/{run}/metrics",
        {"points": [{"key": "loss", "value": float(step), "step_index": step}]}, run_ref=run,
    )


def backlog(queue: Journal, runs: list[str], total: int) -> None:
    """``total`` span writes over ``runs``, round robin, written straight into
    ops/ (appending 10,000 one by one takes ~16 s): spans are never merged into
    one POST, so the pass makes one request per op."""
    queue_metric(queue, runs[0], 0)  # the layout, and one real op to copy
    ((path, template),) = queue.pending()
    path.unlink()
    base = time.time_ns()
    for n in range(total):
        run = runs[n % len(runs)]
        op = dict(template, op_id=uuid.uuid4().hex, run_ref=run, path=f"/v1/runs/{run}/spans",
                  body={"spans": [{"n": n}]})
        (queue.ops_dir / f"{base + n:020d}-{op['op_id']}.json").write_text(json.dumps(op))


def wait_until(condition, seconds: float = 30.0) -> None:
    """Poll ``condition`` until it holds; fail (never hang) after ``seconds``."""
    give_up = time.monotonic() + seconds
    while not condition():
        assert time.monotonic() < give_up, "the drain never got there"
        time.sleep(0.01)


def in_thread(target, *args, **kwargs) -> tuple[threading.Thread, list]:
    out: list = []

    def body():
        out.append(target(*args, **kwargs))

    thread = threading.Thread(target=body, daemon=True)
    thread.start()
    return thread, out


def close_like_finish(queue: Journal, server: Server, run: str, *, deadline: float = 30.0) -> float:
    """What `Run._drain_until` does, against ``server``: barrier passes over
    ``run``, the lock polled at most 1 s at a time, until nothing of it is left.
    Returns the seconds it took."""
    started = time.monotonic()
    mine = queue.run_ops(run)
    while mine.pending():
        left = started + deadline - time.monotonic()
        assert left > 0, f"the close of {run} waited {deadline}s"
        drain(queue, run_ref=run, lock_timeout=min(left, 1.0), client_factory=lambda _c: server)
    return time.monotonic() - started


# -- the measured shape: closes behind a big upload --------------------------


@pytest.mark.parametrize("shape", ["one 30 MiB upload", "a window of uploads"])
def test_three_closes_return_in_seconds_while_a_big_upload_is_in_flight(app, tmp_path, shape):
    """The swarm's `finish()` waited ~400 s; here three closes must not wait
    for an upload of another run that never ends until they have all closed.
    On a pass that held the lock through the upload each would wait out its
    whole 20 s deadline and defer."""
    outbox = tmp_path / "outbox"
    upload_run, *closing = (seeded_run(app, tmp_path) for _ in range(4))
    assert len({upload_run, *closing}) == 4
    server = Server()
    owner = make_client(app, tmp_spool=outbox, async_writes=True)
    names = ["ckpt.pt"] if shape == "one 30 MiB upload" else ["a.pt", "b.pt", "c.pt"]
    for name in names:
        size = 30 * 2**20 if len(names) == 1 else 2**20
        queue_upload(owner.journal, tmp_path, upload_run, name, size=size)
        server.gate(name)
    runs = []
    for run in closing:
        client = make_client(app, tmp_spool=outbox, async_writes=True)
        for step in range(3):
            client.write("POST", f"/v1/runs/{run}/metrics",
                         {"points": [{"key": "loss", "value": 1.0, "step_index": step}]})
        runs.append(Run(client, {"id": run}))

    worker, report = in_thread(drain, Journal(outbox), client_factory=lambda _c: server)
    took: dict[str, float] = {}
    try:
        assert all(server.started[name].wait(30) for name in names), "the upload never started"

        def close(run: Run) -> None:
            started = time.monotonic()
            run.finish(flush_timeout=20)
            took[run.id] = time.monotonic() - started

        threads = [threading.Thread(target=close, args=(run,), daemon=True) for run in runs]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(40)
        assert not any(server.gates[name].is_set() for name in names)
    finally:
        for name in names:
            server.gates[name].set()
        worker.join(60)

    assert sorted(took) == sorted(closing), took
    assert max(took.values()) < 5, f"a close waited for another run's upload: {took}"
    for run in closing:
        assert app.runs[run]["status"] == "completed"
        assert len(app.metric_points_posted[run]) == 3
    # The worker sent the upload and nothing of the closes' runs: their writes
    # had gone by the time it took the lock back, and it read that from disk.
    assert report and report[0].delivered == len(names)
    assert sorted(entry[2] for entry in server.log if entry[0] == "upload") == sorted(names)
    assert not [entry for entry in server.log if entry[1] in closing]
    assert Journal(outbox).pending() == [] and Journal(outbox).failed() == []
    for client in [owner, *(run._client for run in runs)]:
        client.close()


# -- a long pass of JSON writes ----------------------------------------------


def test_a_close_gets_the_lock_from_a_10k_op_pass_at_its_next_op(tmp_path):
    """No upload at all: 10,000 span writes of 50 runs, 2 ms each, a 20 s pass.
    The closing run queues its last writes once the pass has read the queue (so
    the pass will not send them), and says it is waiting: the pass gives the
    lock up at its next op. The pass used to keep it to its end."""
    queue = Journal(tmp_path / "outbox")
    runs = [run_id(n) for n in range(1, 51)]
    backlog(queue, runs, 10_000)
    mine = run_id(999)
    server = Server(delay=0.002)

    worker, _ = in_thread(drain, Journal(queue.dir), client_factory=lambda _c: server)
    try:
        wait_until(lambda: len(server.log) >= 50)  # the pass is under way
        for step in range(3):
            queue_metric(queue, mine, step)
        queue.append_http("PATCH", f"/v1/runs/{mine}", {"status": "completed"}, run_ref=mine)
        took = close_like_finish(queue, server, mine)
        sent_meanwhile = len(server.log)
    finally:
        server.down.set()  # every lane stalls at its next op: the pass ends
        worker.join(60)

    assert took < 3, f"the close waited {took:.1f}s for the pass"
    assert sent_meanwhile < 5_000, "the pass had nearly finished: nothing was shown"
    assert [entry[2] for entry in server.of_run(mine)] == ["POST", "PATCH"], (
        "its three points go as one POST, then the close"
    )


def test_an_older_close_that_only_polls_gets_the_lock_within_a_hold(tmp_path, monkeypatch):
    """An older release's `finish()` polls the lock and says nothing; the pass
    lets go once it has held the lock `PASS_HOLD_SECONDS` (R11)."""
    monkeypatch.setattr(jm, "PASS_HOLD_SECONDS", 0.5)
    queue = Journal(tmp_path / "outbox")
    backlog(queue, [run_id(n) for n in range(1, 21)], 4_000)
    server = Server(delay=0.002)
    worker, _ = in_thread(drain, Journal(queue.dir), client_factory=lambda _c: server)
    handle = open(queue.drain_lock, "a+")
    try:
        wait_until(lambda: len(server.log) >= 20)
        started = time.monotonic()
        got = _take_drain_lock(handle, wait_for_lock=True, timeout=10.0)  # no `want`
        waited = time.monotonic() - started
        if got:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
    finally:
        handle.close()
        server.down.set()
        worker.join(60)
    assert got and waited < 3, f"an older close waited {waited:.1f}s"


# -- order and exactly-once, everything at once ------------------------------


def test_each_runs_ops_go_once_and_in_order_with_closes_and_a_worker_interleaving(tmp_path):
    """Six runs, each: a point, an upload, a point, a span, an upload, its close.
    A worker drains everything while three closes drain their own runs, uploads
    0.2 s each. Every op lands once; a run's uploads may pass its points (as the
    window always let them), and nothing else moves. Its two points may ride one
    POST once the upload between them has gone."""
    queue = Journal(tmp_path / "outbox")
    runs = [run_id(n) for n in range(1, 7)]
    for run in runs:
        queue_metric(queue, run, 1)
        queue_upload(queue, tmp_path, run, f"{run}-first.pt")
        queue_metric(queue, run, 2)
        queue.append_http("POST", f"/v1/runs/{run}/spans", {"spans": []}, run_ref=run)
        queue_upload(queue, tmp_path, run, f"{run}-second.pt")
        queue.append_http("PATCH", f"/v1/runs/{run}", {"status": "completed"}, run_ref=run)
    server = Server(delay=0.01, upload_delay=0.2)

    worker, _ = in_thread(drain, Journal(queue.dir), client_factory=lambda _c: server)
    closes = [in_thread(close_like_finish, Journal(queue.dir), server, run)[0] for run in runs[:3]]
    for thread in closes:
        thread.join(60)
    worker.join(60)
    for _ in range(20):  # what the worker's one pass left
        if not Journal(queue.dir).pending():
            break
        drain(Journal(queue.dir), client_factory=lambda _c: server)
    assert not Journal(queue.dir).pending()

    for run in runs:
        seen = server.of_run(run)
        uploads = [entry[2] for entry in seen if entry[0] == "upload"]
        assert sorted(uploads) == sorted([f"{run}-first.pt", f"{run}-second.pt"]), uploads
        points = sorted(
            point["step_index"]
            for entry in seen
            if entry[0] == "http" and entry[3].endswith("/metrics")
            for point in json.loads(entry[4])["points"]
        )
        assert points == [1, 2], f"run {run}: a point went twice or never: {points}"
        writes = [(e[2], e[3].rsplit("/", 1)[-1]) for e in seen if e[0] == "http"]
        assert writes[-2:] == [("POST", "spans"), ("PATCH", run)], f"run {run}: {writes}"
        at = {
            entry[2] if entry[0] == "upload" else entry[3].rsplit("/", 1)[-1]: i
            for i, entry in enumerate(seen)
        }
        last_point = max(i for i, e in enumerate(seen) if e[0] == "http" and e[3].endswith("/metrics"))
        # A run's uploads may pass its points (the window always let them);
        # nothing passes its span or its close.
        assert last_point < at["spans"], seen
        assert at[f"{run}-first.pt"] < at["spans"] < at[f"{run}-second.pt"] < at[run], seen
    assert Journal(queue.dir).failed() == []


# -- a run another drain is sending -------------------------------------------


def test_a_run_another_drain_is_sending_waits_and_the_rest_go(tmp_path):
    """Another drain holds run A's lock (its drain lock let go for A's upload):
    this pass leaves A -- its later ops too -- as held, not failed, and sends
    everything else."""
    queue = Journal(tmp_path / "outbox")
    a, b = run_id(1), run_id(2)
    queue_metric(queue, a, 1)
    queue.append_http("PATCH", f"/v1/runs/{a}", {"status": "completed"}, run_ref=a)
    queue_metric(queue, b, 1)
    other = _DrainHold(queue, None, urgent=False)
    assert other._keep({a})  # what `away` takes while that drain sends A's upload
    server = Server()
    try:
        report = drain(queue, client_factory=lambda _c: server)
    finally:
        other.close()

    assert report.busy_runs == {a}
    assert report.stalled_runs[a].held and report.stalled_runs[a].wake_by
    assert server.of_run(a) == [] and len(server.of_run(b)) == 1
    assert report.delivered == 1 and report.dead_lettered == 0
    assert drain(queue, client_factory=lambda _c: server).delivered == 2
    assert [entry[2] for entry in server.of_run(a)] == ["POST", "PATCH"]


def test_a_close_never_waits_past_its_deadline_to_take_the_lock_back(tmp_path):
    """A close lets go of the lock for its own upload, and an older release's
    drain, which knows nothing of run locks, takes it and keeps it. The close
    still returns at its deadline (`Run.finish`'s one budget, plan 0.6): its
    upload stays queued for the next drain and its run's lock is dropped."""
    from probe.sdk import transport

    queue = Journal(tmp_path / "outbox")
    run = run_id(1)
    queue_upload(queue, tmp_path, run, "late.pt")
    server = Server()
    gate = server.gate("late.pt")
    holder = open(queue.drain_lock, "a+")

    def older_drain() -> None:
        assert server.started["late.pt"].wait(10)
        oscompat.flock(holder.fileno(), oscompat.LOCK_EX)
        gate.set()

    taker = threading.Thread(target=older_drain, daemon=True)
    taker.start()
    try:
        started = time.monotonic()
        with transport.deadline_scope(time.monotonic() + 2.0):
            report = drain(queue, run_ref=run, lock_timeout=1.0, client_factory=lambda _c: server)
        took = time.monotonic() - started
    finally:
        taker.join(10)
        oscompat.flock(holder.fileno(), oscompat.LOCK_UN)
        holder.close()

    assert took < 3.5, f"the close waited {took:.1f}s past a 2 s deadline"
    assert report.deadline_reached
    assert len(queue.pending()) == 1, "its upload waits for the next drain"
    assert not _DrainHold(queue, None, urgent=False).busy(run), "its run's lock was dropped"


def test_an_import_queue_never_lets_go():
    """A receipt queue's receipts are written in queue order on the drain's own
    thread: it keeps its lock through its uploads, as before."""
    hold = _DrainHold(SimpleNamespace(receipt_enabled=True), None, urgent=True)
    assert hold.yields is False
    assert hold.busy("any-run") is False
    with hold.away({"any-run"}):
        assert hold.let_go == 0


def test_an_upload_set_aside_while_it_was_on_the_network_is_not_written_back(tmp_path):
    """A pass sends run A's upload with the lock let go. Meanwhile `probe outbox
    discard` (or an older release's drain), which knows no run locks, takes the
    lock and sets the op aside; then the server refuses the upload. The op stays
    where that drain put it: never written back into ops/, never dead-lettered,
    and no reference row is recorded for it."""
    queue = Journal(tmp_path / "outbox")
    run = run_id(1)
    queue_upload(queue, tmp_path, run, "ckpt.pt")
    ((path, _),) = queue.pending()
    server = Server()
    gate = server.gate("ckpt.pt")
    server.refuse.add("ckpt.pt")
    discarded = queue.dir / "discarded"

    def set_aside() -> None:
        assert server.started["ckpt.pt"].wait(10)
        handle = open(queue.drain_lock, "a+")
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX)
        discarded.mkdir(exist_ok=True)
        os.replace(path, discarded / path.name)
        oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
        handle.close()
        gate.set()

    other = threading.Thread(target=set_aside, daemon=True)
    other.start()
    report = drain(queue, client_factory=lambda _c: server)
    other.join(10)

    assert queue.pending() == [] and queue.failed() == []
    assert [p.name for p in discarded.glob("*.json")] == [path.name]
    assert report.dead_lettered == 0
    assert not [entry for entry in server.log if entry[0] == "http"], "a reference row for a write set aside"


def test_a_close_that_says_it_waits_but_never_comes_costs_a_pass_little(tmp_path, monkeypatch):
    """A close stopped (Ctrl-Z) while it says it is waiting: the pass waits for
    it once, `_WANT_WAIT_SECONDS`, then ignores it for a while, longer each time.
    Without that each of these 200 ops would wait for it."""
    monkeypatch.setattr(jm, "_WANT_WAIT_SECONDS", 0.2)
    queue = Journal(tmp_path / "outbox")
    backlog(queue, [run_id(n) for n in range(1, 11)], 200)
    stuck = open(queue.drain_want, "a+")
    oscompat.flock(stuck.fileno(), oscompat.LOCK_SH)
    try:
        started = time.monotonic()
        report = drain(queue, client_factory=lambda _c: Server())
        took = time.monotonic() - started
    finally:
        stuck.close()
    assert report.delivered == 200
    assert took < 2, f"a waiter that never came cost the pass {took:.1f}s"


def test_after_letting_go_a_pass_reads_a_changed_op_again_and_skips_a_gone_one(tmp_path):
    queue = Journal(tmp_path / "outbox")
    queue_metric(queue, run_id(1), 1)
    queue_metric(queue, run_id(1), 2)
    hold = _DrainHold(queue, None, urgent=False)
    (first, one), (second, two) = queue._scan_ops(stamps=hold.stamps)[0]
    assert hold.fresh(second, two), "until the pass lets go, nothing is looked at"
    hold.let_go = 1
    first.write_text(json.dumps(dict(one, attempts=3, last_error="ServerError: busy")))
    second.unlink()
    assert hold.fresh(first, one) and one["attempts"] == 3, "another drain's change, read in place"
    assert not hold.fresh(second, two), "another drain sent it"


@pytest.mark.skipif(not os.path.isdir("/proc/self/fd"), reason="counts descriptors through /proc")
def test_asking_about_many_runs_keeps_no_descriptor_open(tmp_path):
    """A pass asks about every run it meets; a descriptor kept per run-lock slot
    would be 256 more (macOS allows 256 in all)."""
    queue = Journal(tmp_path / "outbox")
    queue._ensure()
    hold = _DrainHold(queue, None, urgent=False)
    before = len(os.listdir("/proc/self/fd"))
    assert not any(hold.busy(run_id(n)) for n in range(600))
    assert len(os.listdir("/proc/self/fd")) <= before
    hold.close()
