"""A Ray Tune trial's run closes when its function's thread ends -- before Ray
kills the process.

A Ray Tune function trainable runs on Ray's ``RunnerThread`` in the trial's
actor. When Tune stops the trial -- a scheduler's early stop, or the function
having returned -- ``tune.report()`` calls ``sys.exit(0)`` on that thread; the
actor's ``stop()`` does not wait for it, and the raylet SIGTERMs the actor's
process group and SIGKILLs it 200 ms later (Ray 2.58). The atexit close had
~120 ms of that: over a real network it was killed mid-request, and the run
stayed ``running`` with its lease held (environment suite against prod,
``test_ray_tune_one_run_per_trial``, trial 3).

Ray also SIGKILLs a worker's direct children as its core worker shuts down --
the detached outbox worker the trial started among them.

Here a REAL child process plays the trial actor against the served fake, with
2 s of latency on every close request: a thread of Ray's ``RunnerThread``
class (stood in for, so the suite needs no Ray; the environment suite runs
the real one) opens the run and ends with ``sys.exit``; then Ray's teardown:
SIGTERM to the process group -- whose handler, as a Ray worker's, SIGKILLs
the direct children and exits -- and SIGKILL to the group 200 ms later.
"""

from __future__ import annotations

import json
import os
import pathlib
import signal
import subprocess
import sys
import threading
import time

import pytest

from tests.served_fake_app import child_env, close_latency, serve
from tests.test_sigterm_flush import _stop_workers_of

CLOSE_LATENCY = 2.0
STEPS = 5
KEYS = ("loss", "acc")

_CHILD = """
import json, os, signal, sys, threading, time, types

def say(event, **fields):
    print("CHILD " + json.dumps({"event": event, **fields}), flush=True)

# ray/air/_internal/util.py's RunnerThread (Ray 2.58), which runs a Tune
# function trainable: a SystemExit(0) ends the thread quietly, never the
# process. Stood in under Ray's own module name.
class RunnerThread(threading.Thread):
    def run(self):
        try:
            self._target(*self._args, **self._kwargs)
        except SystemExit as exc:
            if exc.code != 0:
                say("thread-error", code=exc.code)

for name in ("ray", "ray.air", "ray.air._internal", "ray.air._internal.util"):
    sys.modules[name] = types.ModuleType(name)
sys.modules["ray.air._internal.util"].RunnerThread = RunnerThread

import probe

kind, code = sys.argv[1], int(sys.argv[2])

def trial():
    run = probe.init(experiment="e1", name="trial")
    say("opened", run_id=run.id)
    for step in range(%(steps)d):
        probe.log({"loss": 1.0 / (step + 1), "acc": step / 10.0}, step=step)
    # Tune's STOP: the tune.report() this trial waits in calls sys.exit(0).
    sys.exit(code)

def children():
    me = str(os.getpid())
    for pid in os.listdir("/proc"):
        try:
            with open(f"/proc/{pid}/stat") as f:
                if pid.isdigit() and f.read().rsplit(")", 1)[1].split()[1] == me:
                    yield int(pid)
        except (OSError, IndexError):
            pass

def ray_sigterm(signum, frame):
    # A Ray worker's SIGTERM (worker.py's main_loop handler + the core worker's
    # shutdown, kill_child_processes_on_worker_exit): SIGKILL every direct
    # child, then SystemExit -- so atexit still runs, until the group's SIGKILL.
    for pid in list(children()):
        os.kill(pid, signal.SIGKILL)
    raise SystemExit(1)

signal.signal(signal.SIGTERM, ray_sigterm)
thread = (RunnerThread if kind == "ray" else threading.Thread)(target=trial, daemon=True)
thread.start()
thread.join()
say("thread-ended")
while True:
    time.sleep(0.05)
""" % {"steps": STEPS}


@pytest.fixture
def app(app):
    app.supports_leases = True
    app.latency = close_latency(CLOSE_LATENCY)
    return app


@pytest.fixture(autouse=True)
def _own_outbox(tmp_path, monkeypatch):
    outbox = str(tmp_path / "outbox")
    monkeypatch.setenv("PROBE_OUTBOX_DIR", outbox)
    yield outbox
    _stop_workers_of(outbox)


def _trial(url: str, kind: str, code: int) -> tuple[subprocess.Popen, str]:
    """Start the trial actor in a process group of its own, as Ray does, and
    wait for its thread to end. Returns the process and the run id."""
    proc = subprocess.Popen(
        [sys.executable, "-c", _CHILD, kind, str(code)],
        env=child_env(url, PROBE_HW="0", PROBE_EPHEMERAL="0"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    events: dict[str, dict] = {}
    deadline = time.monotonic() + 60
    while "thread-ended" not in events and time.monotonic() < deadline:
        line = proc.stdout.readline()
        if not line:
            break
        if line.startswith("CHILD "):
            event = json.loads(line[len("CHILD "):])
            events[event["event"]] = event
    if "thread-ended" not in events:
        os.killpg(proc.pid, signal.SIGKILL)
        raise AssertionError(f"the trial never ended: {proc.communicate()[1][-3000:]}")
    return proc, events["opened"]["run_id"]


def _ray_teardown(proc: subprocess.Popen) -> str:
    """The raylet's (`NodeManager::DisconnectClient`): SIGTERM to the actor's
    process group, SIGKILL 200 ms later. Returns the child's stderr, captured
    here since this is the only place anything still reads its pipes."""
    os.killpg(proc.pid, signal.SIGTERM)
    time.sleep(0.2)
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        _, stderr = proc.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        _, stderr = proc.communicate(timeout=30)
    return stderr or ""


def _wait_closed(app, run_id: str, timeout: float = 30.0) -> str:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline and app.runs[run_id]["status"] == "running":
        time.sleep(0.1)
    return app.runs[run_id]["status"]


#: Every place under an outbox root an op can sit (`journal.py`'s layout): the
#: queue and dead letters, the waiting room, the multipart queue -- in the root,
#: its receipt namespace (``delivery-v1``) and every credential queue
#: (``credential-v1/<fingerprint>``), which is where this child's writes go:
#: it runs with ``PROBE_TOKEN`` set.
_OP_DIRS = ("ops", "failed", "waiting", "multipart/ops", "multipart/failed", "multipart/staged")


def _outbox_op_kinds(outbox_dir: str) -> list[str]:
    """Every op still queued, waiting or dead-lettered anywhere under
    ``outbox_dir``, by its path relative to the root, with its kind, request,
    attempts and last error -- for diagnosing a close that never lands."""
    root = pathlib.Path(outbox_dir)
    found = []
    queues = sorted(
        {path.parent for path in root.rglob("ops") if path.is_dir() and path.parent.name != "multipart"}
    )
    for queue in queues or [root]:
        for sub in _OP_DIRS:
            directory = queue / sub
            if not directory.is_dir():
                continue
            for entry in sorted(directory.iterdir()):
                where = entry.relative_to(root)
                if entry.suffix != ".json":
                    found.append(f"{where}")
                    continue
                try:
                    op = json.loads(entry.read_text())
                except (OSError, ValueError) as exc:
                    found.append(f"{where}:<unreadable:{exc}>")
                    continue
                found.append(
                    f"{where}:{op.get('kind')!r} {op.get('method')} {op.get('path')} "
                    f"attempts={op.get('attempts')} last_error={op.get('last_error')!r}"
                )
    return found


def _outbox_status_and_logs(outbox_dir: str) -> str:
    """Each queue's ``status.json`` and the tail of its worker's
    ``drainer.log``: whether a sender ran there, and how it ended."""
    root = pathlib.Path(outbox_dir)
    parts = []
    for path in sorted(root.rglob("status.json")) + sorted(root.rglob("drainer.log")):
        try:
            text = path.read_text(errors="replace")
        except OSError as exc:
            text = f"<unreadable:{exc}>"
        parts.append(f"{path.relative_to(root)}: {text[-1500:]!r}")
    return "; ".join(parts) or "<no status.json or drainer.log anywhere>"


def _outbox_sender_pids(outbox_dir: str) -> list[int]:
    """PIDs of a detached ``probe.sdk.outbox_worker`` sender pointed at this
    outbox -- the atexit-restarted process this test exercises delivering the
    queued close after the trial's own process is gone."""
    pids = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            with open(f"/proc/{pid}/cmdline", "rb") as f:
                argv = f.read().split(b"\0")
        except OSError:
            continue
        if b"probe.sdk.outbox_worker" in argv and any(outbox_dir.encode() in a for a in argv):
            pids.append(int(pid))
    return pids


def _diagnose_stall(outbox_dir: str, stderr: str) -> str:
    """Says which step stalled when a close never lands: whether the op is
    still queued, whether the restarted sender ever started, and what the
    child printed to stderr before it died. A str, so pytest prints it whole
    (it truncates the repr of anything else to a line)."""
    return (
        f"queued/dead-lettered ops: {_outbox_op_kinds(outbox_dir) or ['<none>']}\n"
        f"sender pids for this outbox: {_outbox_sender_pids(outbox_dir) or ['<none running>']}\n"
        f"queue status and worker logs: {_outbox_status_and_logs(outbox_dir)}\n"
        f"child stderr tail: {stderr[-3000:]!r}"
    )


def _stalled(status: str, leases: list[tuple], outbox_dir: str, stderr: str) -> str:
    return f"status {status!r}, leases {leases!r}\n{_diagnose_stall(outbox_dir, stderr)}"


def _leases(app, run_id: str) -> list[tuple]:
    return [
        (w.get("role"), bool(w.get("released_at")), w.get("exit_status"))
        for w in app.leases.get(run_id, {}).values()
    ]


def _points(app, run_id: str) -> set[tuple[int, str]]:
    return {(p["step_index"], p["key"]) for p in app.metric_points_posted.get(run_id, [])}


@pytest.mark.parametrize(("code", "verdict"), [(0, "completed"), (3, "failed")])
def test_a_ray_trial_thread_ending_closes_its_run_before_the_kill(app, code, verdict, _own_outbox):
    """Tune stops the trial (``sys.exit(0)`` on its thread): the run closes
    ``completed`` and its lease is released, although the process group is
    SIGKILLed 200 ms after the thread ends and every close request takes 2 s
    -- the close was queued for the detached outbox worker, which delivers it.
    A trial's own ``sys.exit(3)`` closes it ``failed``.

    On a timeout, say where the close sits -- which queue under the outbox
    (this child writes to its credential's, ``credential-v1/<fingerprint>``),
    whether a sender runs, how the last one ended -- rather than just the
    run's stuck status. The 0.201.3 gate's failure read "no ops queued" from
    the root queue alone; the close was in the credential's, behind a worker
    killed mid-send (see the next test)."""
    app.seed_experiment("e1")
    with serve(app) as url:
        proc, run_id = _trial(url, "ray", code)
        stderr = _ray_teardown(proc)
        status = _wait_closed(app, run_id, timeout=90.0)
        leases = _leases(app, run_id)
        points = _points(app, run_id)
    assert status == verdict, _stalled(status, leases, _own_outbox, stderr)
    assert leases == [("owner", True, verdict)], _stalled(status, leases, _own_outbox, stderr)
    assert points == {(step, key) for step in range(STEPS) for key in KEYS}


def test_a_trial_torn_down_while_its_worker_sends_the_close_still_closes(app, _own_outbox):
    """Ray's teardown lands while the outbox worker is SENDING the close -- the
    usual case for a trial that ran long enough for its worker to be up: the
    close request is in flight (held 2 s) when Ray's shutdown SIGKILLs the
    worker. A SIGKILLed process keeps its lease until the kernel has torn it
    down, and the exit kick, a fraction of a millisecond later, read that held
    lease as a worker delivering the queue and started none: the lease release
    stayed queued and the run ``running`` (the cli 0.201.3 release gate).
    Waiting for the close request, not for time, makes this the case every
    run instead of only when a runner happens to be fast."""
    sending = threading.Event()
    latency = app.latency

    def watched(request) -> float:
        seconds = latency(request)
        if seconds:
            sending.set()  # a close request has reached the server; its reply is held
        return seconds

    app.latency = watched
    app.seed_experiment("e1")
    with serve(app) as url:
        proc, run_id = _trial(url, "ray", 0)
        if not sending.wait(60):
            os.killpg(proc.pid, signal.SIGKILL)
            raise AssertionError(f"the worker never sent the close: {proc.communicate()[1][-3000:]}")
        stderr = _ray_teardown(proc)
        status = _wait_closed(app, run_id, timeout=90.0)
        leases = _leases(app, run_id)
        points = _points(app, run_id)
    assert status == "completed", _stalled(status, leases, _own_outbox, stderr)
    assert leases == [("owner", True, "completed")], _stalled(status, leases, _own_outbox, stderr)
    assert points == {(step, key) for step in range(STEPS) for key in KEYS}


def test_a_sys_exit_on_any_other_thread_leaves_the_run_open(app):
    """Negative control: ``sys.exit`` on a plain thread ends that thread, not
    the script, so the run stays open -- the script goes on logging to it."""
    app.seed_experiment("e1")
    with serve(app) as url:
        proc, run_id = _trial(url, "plain", 0)
        time.sleep(1.0)
        status = app.runs[run_id]["status"]
        leases = _leases(app, run_id)
        os.killpg(proc.pid, signal.SIGKILL)
        proc.communicate(timeout=30)
    assert status == "running", status
    assert leases == [("owner", False, None)], leases


# -- the exit kick, past the worker Ray killed ---------------------------------

_LEASE_HOLDER = """
import sys, time
from probe._shared import oscompat

lease = open(sys.argv[1], "a+")
oscompat.flock(lease.fileno(), oscompat.LOCK_EX)
print("held", flush=True)
time.sleep(float(sys.argv[2]))
"""


class _Worker:
    """What `maybe_spawn` gets back from ``Popen``: a worker still starting."""

    def poll(self):
        return None


def _hold_the_lease(journal, seconds: float) -> subprocess.Popen:
    """Another process holds the queue's worker lease for ``seconds``, then
    exits -- the lease goes with it, as a killed worker's does once the
    kernel has torn it down."""
    from probe.sdk import outbox_worker

    holder = subprocess.Popen(
        [sys.executable, "-c", _LEASE_HOLDER, outbox_worker._lease_path(journal), str(seconds)],
        stdout=subprocess.PIPE,
        text=True,
    )
    assert holder.stdout.readline().strip() == "held"
    return holder


def _spawns(monkeypatch, journal) -> list[tuple[list, bool]]:
    """Every worker `maybe_spawn` starts, with whether the lease was free then."""
    from probe.sdk import outbox_worker

    spawned: list[tuple[list, bool]] = []

    def popen(argv, **kw):
        spawned.append((argv, outbox_worker._lease_is_free(journal)))
        return _Worker()

    monkeypatch.setattr(outbox_worker.subprocess, "Popen", popen)
    return spawned


def test_the_exit_kick_waits_for_the_killed_workers_lease(tmp_path, monkeypatch):
    """The worker Ray killed still holds its lease for a moment: the kick
    waits for it to go, then starts the worker that delivers the close.
    `maybe_spawn` alone, asked while the lease is held, starts none."""
    from probe.sdk import outbox_worker
    from probe.sdk.journal import Journal

    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", "/v1/runs/r-1/writers/w-1/release", {"exit_status": "completed"})
    holder = _hold_the_lease(journal, 0.3)
    try:
        spawned = _spawns(monkeypatch, journal)
        assert outbox_worker.maybe_spawn(str(journal.dir)) is False
        assert outbox_worker.spawn_past_a_kill(str(journal.dir), wait=10.0) is True
    finally:
        holder.kill()
        holder.communicate(timeout=30)
    assert [(argv[1:], free) for argv, free in spawned] == [
        (["-m", "probe.sdk.outbox_worker", str(journal.dir)], True)
    ]


def test_the_exit_kick_leaves_a_live_workers_queue_to_it(tmp_path, monkeypatch):
    """Negative control: a lease still held when the wait is over is a live
    worker's (a sibling trial's, on the same queue), which delivers the close:
    no second worker, and the wait is bounded."""
    from probe.sdk import outbox_worker
    from probe.sdk.journal import Journal

    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", "/v1/runs/r-1/writers/w-1/release", {"exit_status": "completed"})
    holder = _hold_the_lease(journal, 60.0)
    try:
        spawned = _spawns(monkeypatch, journal)
        started = time.monotonic()
        assert outbox_worker.spawn_past_a_kill(str(journal.dir), wait=0.2) is False
        waited = time.monotonic() - started
    finally:
        holder.kill()
        holder.communicate(timeout=30)
    assert spawned == []
    assert 0.2 <= waited < 5.0, waited
