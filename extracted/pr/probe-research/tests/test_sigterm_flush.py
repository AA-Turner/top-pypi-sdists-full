"""SIGTERM: deliver what is queued, close the run failed/preempted, die of SIGTERM.

Managed jobs (SageMaker, Vertex, Kubernetes, spot) stop a job with SIGTERM and
destroy its container about 30 s later. Python's default action for SIGTERM
ended the process at once, so the queue died with the container and the run
stayed `running` until the reaper (lane E3: 0 of 900 queued points).

Every case runs a REAL child process against the served fake: signal handlers,
the exit status and what reaches the server are process-level facts.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time

import pytest

from probe.sdk import fluent
from tests.served_fake_app import child_env, serve

#: `probe.sdk.preempt.ENV`; spelled out so the child-process cases also run
#: (and fail) against an SDK without the module.
ENV = "PROBE_SIGTERM_FLUSH_SECONDS"
STEPS = 120
KEYS = ("loss", "acc")

_PRELUDE = """
import json, os, signal, sys, time
import probe

def say(event, **fields):
    print("CHILD " + json.dumps({"event": event, **fields}), flush=True)

def loop(run, steps):
    for step in range(steps):
        probe.log({"loss": 1.0 / (step + 1), "acc": step / 1000.0}, step=step)
"""

_PLAIN = _PRELUDE + """
run = probe.init(experiment="e1", name="preempted")
loop(run, int(sys.argv[1]))
probe.update_config({"model": "tiny"})
say("ready", run_id=run.id)
while True:
    time.sleep(0.05)
"""

_THEIRS_FIRST = _PRELUDE + """
marks = sys.argv[2]

def theirs(signum, frame):
    run = probe.active_run()
    with open(marks, "w") as f:
        json.dump({"ran": True, "closed_when_theirs_ran": getattr(run, "_closed_status", None)}, f)

signal.signal(signal.SIGTERM, theirs)
run = probe.init(experiment="e1", name="preempted")
loop(run, int(sys.argv[1]))
say("ready", run_id=run.id)
while True:
    time.sleep(0.05)
"""

#: The script's own close is running (the server busy) when the SIGTERM lands.
_IN_ITS_OWN_CLOSE = _PRELUDE + """
run = probe.init(experiment="e1", name="closing")
loop(run, int(sys.argv[1]))
say("closing", run_id=run.id)
probe.finish()
say("closed", run_id=run.id)
while True:
    time.sleep(0.05)
"""

#: A framework's own stop (Lightning's SIGTERMException at the next step, HF's
#: JIT checkpoint): its handler composes the one it found -- ours, since
#: `probe.init` came first -- notes the signal, and returns; the loop then
#: stops at its next step and the script ends normally, exit 0.
_FRAMEWORK_STOP = _PRELUDE + """
run = probe.init(experiment="e1", name="preempted")
ours = signal.getsignal(signal.SIGTERM)
stop = []

def framework(signum, frame):
    stop.append(signum)
    ours(signum, frame)

signal.signal(signal.SIGTERM, framework)
loop(run, int(sys.argv[1]))
say("ready", run_id=run.id)
while not stop:
    time.sleep(0.05)
time.sleep(float(sys.argv[2]))  # the framework's own stop: a checkpoint save
say("stopped", run_id=run.id)
"""

_THEIRS_RAISES = _PRELUDE + """
how = sys.argv[2]

def theirs(signum, frame):
    if how == "exit":
        raise SystemExit(3)
    raise KeyboardInterrupt

signal.signal(signal.SIGTERM, theirs)
run = probe.init(experiment="e1", name="preempted")
loop(run, int(sys.argv[1]))
say("ready", run_id=run.id)
while True:
    time.sleep(0.05)
"""

#: A SIGTERM handler that never returns, stuck in a C call: the main thread
#: blocks on a relocked default mutex (ctypes releases the GIL, and futex
#: waits run no Python signal handler), as Lightning 2.6's notifier blocks in
#: gloo when it broadcasts from its handler to ranks that got no SIGTERM.
_STUCK_IN_C = """
import ctypes

_libc = ctypes.CDLL(None)
_mutex = ctypes.create_string_buffer(64)  # all zero: PTHREAD_MUTEX_INITIALIZER

def stuck(signum, frame):
    say("stuck")
    _libc.pthread_mutex_lock(_mutex)
    _libc.pthread_mutex_lock(_mutex)  # a default mutex relocked: never returns


class Compose:
    # lightning.pytorch.trainer.connectors.signal_connector._HandlersCompose:
    # calls its `signal_handlers` in order.
    def __init__(self, signal_handlers):
        self.signal_handlers = signal_handlers

    def __call__(self, signum, frame):
        for handler in self.signal_handlers:
            if callable(handler):
                handler(signum, frame)
"""

#: Lightning's shape: its handler is installed AFTER `probe.init` and composes
#: ours LAST, behind a notifier that never returns (soak finding F2).
_COMPOSED_BEHIND_A_STUCK_HANDLER = _PRELUDE + _STUCK_IN_C + """
run = probe.init(experiment="e1", name="preempted")
signal.signal(signal.SIGTERM, Compose([stuck, signal.getsignal(signal.SIGTERM)]))
loop(run, int(sys.argv[1]))
say("ready", run_id=run.id)
while True:
    time.sleep(0.05)
"""

#: Theirs was there first, so ours chains it -- and it never returns.
_CHAINING_A_STUCK_HANDLER = _PRELUDE + _STUCK_IN_C + """
signal.signal(signal.SIGTERM, stuck)
run = probe.init(experiment="e1", name="preempted")
loop(run, int(sys.argv[1]))
say("ready", run_id=run.id)
while True:
    time.sleep(0.05)
"""

#: SIGTERM lands while the main thread is inside `probe.log`, holding the
#: journal's append lock: the op file's write sends the signal, then either
#: finishes after a pause (`slow`) or never does (`stuck`).
_IN_THE_APPEND_LOCK = _PRELUDE + """
from probe.sdk import journal

mode, at = sys.argv[2], int(sys.argv[1])
real = journal.write_text_atomic
calls = {"n": 0}

def write_text_atomic(path, *args, **kwargs):
    if "/ops/" in str(path):
        calls["n"] += 1
        if calls["n"] == at:
            say("sigterm", at=time.monotonic())
            os.kill(os.getpid(), signal.SIGTERM)
            time.sleep(3600 if mode == "stuck" else 0.5)
    return real(path, *args, **kwargs)

journal.write_text_atomic = write_text_atomic
run = probe.init(experiment="e1", name="preempted")
say("opened", run_id=run.id)
loop(run, at + 20)
say("never", run_id=run.id)
while True:
    time.sleep(0.05)
"""


def _events(stdout: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for line in stdout.splitlines():
        if line.startswith("CHILD "):
            event = json.loads(line[len("CHILD "):])
            out.setdefault(event["event"], event)
    return out


def _spawn(app, url: str, source: str, *args: str, budget: str | None = "10", **env: str):
    extra = {"PROBE_HW": "0", "PROBE_EPHEMERAL": "0", **env}
    if budget is not None:
        extra[ENV] = budget
    return subprocess.Popen(
        [sys.executable, "-c", source, *args],
        env=child_env(url, **extra),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _wait_for_line(proc, event: str, timeout: float = 60.0) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        line = proc.stdout.readline()
        if not line:
            break
        if line.startswith("CHILD "):
            got = json.loads(line[len("CHILD "):])
            if got["event"] == event:
                return got
    proc.kill()
    raise AssertionError(f"the child never said {event!r}: {proc.communicate()[1][-3000:]}")


def _finish(proc, timeout: float) -> tuple[int, str, str, float]:
    started = time.monotonic()
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        raise AssertionError(f"the child hung past {timeout}s after SIGTERM:\n{err[-3000:]}")
    return proc.returncode, out, err, time.monotonic() - started


def _points(app, run_id: str) -> set[tuple[int, str]]:
    return {(p["step_index"], p["key"]) for p in app.metric_points_posted.get(run_id, [])}


def _expected(steps: int) -> set[tuple[int, str]]:
    return {(step, key) for step in range(steps) for key in KEYS}


def _probe_finish(row: dict) -> dict:
    return ((row.get("summary_metrics") or row.get("summary") or {}).get("probe_finish")) or {}


def _exit_spans(app, run_id: str) -> list[dict]:
    return [s for s in app.spans.get(run_id, []) if s.get("span_type") == "process" and s.get("name") == "exit"]


def _preempted_by_sigterm(app, run_id: str, *, ours: bool = True) -> None:
    row = app.runs[run_id]
    assert row["status"] == "failed", row["status"]
    marks = _probe_finish(row)
    assert marks.get("reason") == "preempted" and marks.get("signal") == "SIGTERM", marks
    if ours:
        assert marks.get("exit_code") == 143, marks
        # The span speaks the server's language: a negative code is the
        # signal the process died on (the crash email's "stopped after
        # receiving SIGTERM").
        (span,) = _exit_spans(app, run_id)
        attributes = span["attributes"]
        assert attributes["exit_code"] == -signal.SIGTERM, span
        assert attributes["signal"] == "SIGTERM" and attributes["reason"] == "preempted", span


def _stop_workers_of(outbox: str) -> None:
    """A close that leaves writes queued hands them to a detached worker,
    which would retry this test's dead fake for hours: stop the ones this
    test's child started (found by their outbox, which is this test's own)."""
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            with open(f"/proc/{pid}/cmdline", "rb") as f:
                argv = f.read().split(b"\0")
        except OSError:
            continue
        if b"probe.sdk.outbox_worker" in argv and any(outbox.encode() in a for a in argv):
            try:
                os.kill(int(pid), signal.SIGKILL)
            except OSError:
                pass


@pytest.fixture(autouse=True)
def _own_outbox(tmp_path, monkeypatch):
    """Each case's children queue in an outbox of its own, and whatever
    detached worker they left behind is stopped with the case."""
    outbox = str(tmp_path / "outbox")
    monkeypatch.setenv("PROBE_OUTBOX_DIR", outbox)
    yield
    _stop_workers_of(outbox)


def _busy(app, on: bool) -> None:
    """Every metric POST answers production's contention 503 (Retry-After 1)
    while on: the run's writes queue in its outbox, in order."""
    app.metrics_busy_retry_after = "1"
    app.metrics_busy_next = 10**9 if on else 0


def test_a_sigterm_delivers_the_queue_closes_the_run_failed_and_still_dies_by_sigterm(app):
    """The E3 managed-job shape: writes queue behind a busy server, then the
    platform sends SIGTERM (the server healthy again). Everything queued
    arrives within the budget, the run closes failed/preempted with exit code
    143 recorded, and the process still ends killed by SIGTERM."""
    app.seed_experiment("e1")
    _busy(app, True)
    with serve(app) as url:
        proc = _spawn(app, url, _PLAIN, str(STEPS))
        ready = _wait_for_line(proc, "ready")
        run_id = ready["run_id"]
        queued = len(_expected(STEPS) - _points(app, run_id))
        _busy(app, False)
        proc.send_signal(signal.SIGTERM)
        returncode, _, err, took = _finish(proc, timeout=30)
    assert queued > 0, "nothing was queued when the SIGTERM landed: the case tests nothing"
    assert returncode == -signal.SIGTERM, (returncode, err[-3000:])
    assert took < 10 + 2, took
    assert _points(app, run_id) == _expected(STEPS), err[-3000:]
    assert app.runs[run_id]["config"].get("model") == "tiny"
    _preempted_by_sigterm(app, run_id)


def test_a_handler_installed_before_init_runs_first_then_ours(app, tmp_path):
    """Theirs (Lightning's, torchrun's, the script's own) was there when the
    run opened: it runs first -- the run still open -- and ours after it.
    Theirs returned, so it may have a stop of its own to make; this script
    has none and trains on, so once all but the close's reserve of the budget
    is spent ours closes the run and ends the process: the same result."""
    app.seed_experiment("e1")
    marks = tmp_path / "theirs.json"
    budget = 4.0
    _busy(app, True)
    with serve(app) as url:
        proc = _spawn(app, url, _THEIRS_FIRST, str(STEPS), str(marks), budget=str(budget))
        run_id = _wait_for_line(proc, "ready")["run_id"]
        _busy(app, False)
        proc.send_signal(signal.SIGTERM)
        returncode, _, err, took = _finish(proc, timeout=30)
    assert json.loads(marks.read_text()) == {"ran": True, "closed_when_theirs_ran": None}
    assert returncode == -signal.SIGTERM, (returncode, err[-3000:])
    assert budget / 2 - 0.5 < took < budget + 2, took  # the grace, then the close
    assert _points(app, run_id) == _expected(STEPS), err[-3000:]
    _preempted_by_sigterm(app, run_id)


def test_a_framework_that_stops_on_its_own_is_not_cut_short(app):
    """Lightning and Hugging Face's JIT checkpoint handle SIGTERM themselves:
    their handler returns, and the job stops at its next step (saving a
    checkpoint) and exits 0. Ours must not kill it in between: the script
    ends as it would have, and its close on the way out delivers the queue and
    marks the run failed/preempted -- with no exit code, since the process
    chose its own (0)."""
    app.seed_experiment("e1")
    _busy(app, True)
    with serve(app) as url:
        proc = _spawn(app, url, _FRAMEWORK_STOP, str(STEPS), "1.0")
        run_id = _wait_for_line(proc, "ready")["run_id"]
        _busy(app, False)
        proc.send_signal(signal.SIGTERM)
        returncode, out, err, took = _finish(proc, timeout=30)
    assert returncode == 0, (returncode, err[-3000:])
    assert "stopped" in _events(out), err[-3000:]
    assert _points(app, run_id) == _expected(STEPS), err[-3000:]
    _preempted_by_sigterm(app, run_id, ours=False)
    assert "exit_code" not in _probe_finish(app.runs[run_id])


@pytest.mark.parametrize("how, returncode", [("exit", 3), ("interrupt", -signal.SIGINT)])
def test_a_chained_handler_that_raises_still_gets_the_close_on_the_way_out(app, how, returncode):
    """Theirs raises (a SystemExit, a KeyboardInterrupt): the process ends its
    way, and the close on the way out (atexit here) still delivers the queue
    and closes the run failed/preempted -- not `canceled` for the
    KeyboardInterrupt, not `failed` without a reason."""
    app.seed_experiment("e1")
    _busy(app, True)
    with serve(app) as url:
        proc = _spawn(app, url, _THEIRS_RAISES, str(STEPS), how)
        run_id = _wait_for_line(proc, "ready")["run_id"]
        _busy(app, False)
        proc.send_signal(signal.SIGTERM)
        got, _, err, took = _finish(proc, timeout=30)
    assert got == returncode, (got, err[-3000:])
    assert took < 10 + 2 + 2, took
    assert _points(app, run_id) == _expected(STEPS), err[-3000:]
    _preempted_by_sigterm(app, run_id, ours=False)


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="glibc mutex layout")
@pytest.mark.parametrize(
    "source", [_COMPOSED_BEHIND_A_STUCK_HANDLER, _CHAINING_A_STUCK_HANDLER],
    ids=["composed-behind-it", "chaining-it"],
)
def test_a_handler_stuck_in_a_c_call_still_gets_the_run_closed(app, source):
    """The 7-day soak's F2: on a pod delete, rank 0's Lightning handler
    broadcast to ranks that got no SIGTERM and blocked in gloo for good; ours,
    composed after it, never ran, and the run stayed `running` until torchrun
    SIGKILLed the process. Now ours runs first (the first `probe.log` moves it
    to the front of a Lightning-shaped composition), its grace is armed before
    theirs runs, and when the main thread does not answer the worker's
    re-signal -- a C call runs no handler -- the worker closes the run itself
    and ends the process within the budget."""
    app.seed_experiment("e1")
    budget = 6.0
    with serve(app) as url:
        proc = _spawn(app, url, source, str(STEPS), budget=str(budget))
        run_id = _wait_for_line(proc, "ready")["run_id"]
        proc.send_signal(signal.SIGTERM)
        returncode, out, err, took = _finish(proc, timeout=30)
    assert "stuck" in _events(out), err[-3000:]  # theirs ran, and never returned
    assert returncode == preempt_exit_code(), (returncode, err[-3000:])
    assert took < budget + 2, took
    assert "closed the run from another thread" in err, err[-3000:]
    assert _points(app, run_id) == _expected(STEPS), err[-3000:]
    _preempted_by_sigterm(app, run_id)


def preempt_exit_code() -> int:
    """What the worker exits with: SIGTERM's default action needs the main
    thread, so it is the code a shell reports for SIGTERM."""
    return 128 + signal.SIGTERM


@pytest.mark.parametrize("throwaway", [True, False], ids=["throwaway-disk", "durable-disk"])
def test_what_cannot_go_out_in_time_on_a_throwaway_disk_is_counted_and_the_close_sent(
    app, throwaway
):
    """The server stays busy through the whole budget. On a throwaway disk
    the queue dies with the container, so the close goes out directly,
    counting what is lost; on durable storage it is queued behind that data
    as any close is (the worker, or the next process on that disk, delivers
    both), and the run reads `running` until then."""
    app.seed_experiment("e1")
    budget = 3.0
    _busy(app, True)
    with serve(app) as url:
        proc = _spawn(
            app, url, _PLAIN, str(STEPS), budget=str(budget),
            PROBE_EPHEMERAL="1" if throwaway else "0",
        )
        run_id = _wait_for_line(proc, "ready")["run_id"]
        proc.send_signal(signal.SIGTERM)
        returncode, _, err, took = _finish(proc, timeout=30)
    assert returncode == -signal.SIGTERM, (returncode, err[-3000:])
    assert took < budget + 2, took
    row = app.runs[run_id]
    if throwaway:
        _preempted_by_sigterm(app, run_id)
        marks = _probe_finish(row)
        assert marks["undelivered"] > 0 and marks["outbox"] == "PROBE_EPHEMERAL=1", marks
        assert "which goes with this machine" in err, err[-3000:]
    else:
        assert row["status"] == "running"
        assert "probe_finish.deferred" in err, err[-3000:]


def test_a_sigterm_during_the_scripts_own_close_lets_it_finish_then_dies(app):
    """The close already running on the main thread is doing what ours would:
    it is let run (to the budget), keeps the verdict it was closing with, and
    only then does the process die of SIGTERM."""
    app.seed_experiment("e1")
    _busy(app, True)
    with serve(app) as url:
        proc = _spawn(app, url, _IN_ITS_OWN_CLOSE, str(STEPS), PROBE_FINISH_TIMEOUT_SEC="60")
        run_id = _wait_for_line(proc, "closing")["run_id"]
        time.sleep(1.0)  # inside finish(), retrying the busy server
        proc.send_signal(signal.SIGTERM)
        _busy(app, False)
        returncode, out, err, took = _finish(proc, timeout=30)
    assert returncode == -signal.SIGTERM, (returncode, err[-3000:])
    assert "closed" not in _events(out)  # died before its next line, as SIGTERM would
    assert took < 10 + 2, took
    assert _points(app, run_id) == _expected(STEPS), err[-3000:]
    assert app.runs[run_id]["status"] == "completed", err[-3000:]


def test_sigterm_inside_probe_log_holding_the_append_lock_waits_for_it_then_closes(app):
    """The likeliest place for the signal: the main thread inside `probe.log`,
    holding the journal's append flock. The close must not wait on it from the
    interrupted frame (a deadlock); it lets the write finish, then closes, and
    everything arrives."""
    app.seed_experiment("e1")
    at = 40
    with serve(app) as url:
        proc = _spawn(app, url, _IN_THE_APPEND_LOCK, str(at), "slow")
        run_id = _wait_for_line(proc, "opened")["run_id"]
        sent = _wait_for_line(proc, "sigterm")["at"]
        returncode, out, err, _ = _finish(proc, timeout=30)
    took = time.monotonic() - sent
    assert returncode == -signal.SIGTERM, (returncode, err[-3000:])
    assert "never" not in _events(out)
    assert took < 10 + 2, took
    # The write the signal interrupted is the `at`-th op; everything up to it
    # was queued, and all of it arrives.
    delivered = {step for step, _ in _points(app, run_id)}
    assert delivered and delivered == set(range(max(delivered) + 1)), sorted(delivered)[-5:]
    assert max(delivered) >= at // 2 - 1, max(delivered)
    _preempted_by_sigterm(app, run_id)


def test_sigterm_while_the_append_lock_is_never_released_still_exits_on_time(app):
    """The frame holding the append lock never returns (a hung fsync): the
    close cannot take the lock, and must not wait for it past the budget. The
    process says so and dies of SIGTERM within budget + 2 s."""
    app.seed_experiment("e1")
    budget = 4.0
    with serve(app) as url:
        proc = _spawn(app, url, _IN_THE_APPEND_LOCK, "10", "stuck", budget=str(budget))
        _wait_for_line(proc, "opened")
        sent = _wait_for_line(proc, "sigterm")["at"]
        returncode, _, err, _ = _finish(proc, timeout=budget + 20)
    took = time.monotonic() - sent
    assert returncode == -signal.SIGTERM, (returncode, err[-3000:])
    assert took < budget + 2, took
    assert "could not be closed within 4s (PROBE_SIGTERM_FLUSH_SECONDS)" in err, err[-3000:]


def test_zero_turns_it_off_sigterm_kills_at_once_as_before(app):
    """Negative control: PROBE_SIGTERM_FLUSH_SECONDS=0 is today's behaviour --
    no handler, the process dies at once, the queue stays behind, the run is
    left `running` for the reaper."""
    app.seed_experiment("e1")
    _busy(app, True)
    with serve(app) as url:
        proc = _spawn(app, url, _PLAIN, str(STEPS), budget="0")
        run_id = _wait_for_line(proc, "ready")["run_id"]
        _busy(app, False)
        proc.send_signal(signal.SIGTERM)
        returncode, _, _, took = _finish(proc, timeout=30)
    assert returncode == -signal.SIGTERM
    assert took < 2, took
    assert app.runs[run_id]["status"] == "running"
    assert _points(app, run_id) != _expected(STEPS)


# -- in-process: who owns SIGTERM, and when ---------------------------------------


@pytest.fixture
def _clean_binding():
    """fluent keeps process state on purpose (see test_fluent.py)."""
    yield
    fluent._current.set(None)
    fluent._process_default = None
    fluent._unbound.clear()
    fluent._exit_status = "completed"
    fluent._exit_recorded = False
    fluent._exit_exception = None
    fluent._exit_code = None
    fluent._exit_via = None


@pytest.fixture
def preempt():
    from probe.sdk import preempt

    return preempt


@pytest.fixture
def opened(app, monkeypatch, _clean_binding, preempt):
    """`probe.init` against the in-process fake, on this (main) thread."""
    from tests.conftest import make_client

    app.seed_experiment("e1")
    monkeypatch.delenv(ENV, raising=False)

    def open_run():
        return fluent.init(client=make_client(app), experiment="e1", name="r")

    return open_run


def _theirs(signum, frame):  # pragma: no cover -- never delivered
    pass


def test_init_puts_ours_in_front_and_finish_gives_sigterm_back(opened, preempt):
    assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL
    opened()
    assert signal.getsignal(signal.SIGTERM) is preempt._on_sigterm
    fluent.finish()
    assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL


def test_a_handler_there_before_init_is_chained_and_handed_back(opened, preempt):
    signal.signal(signal.SIGTERM, _theirs)
    opened()
    assert signal.getsignal(signal.SIGTERM) is preempt._on_sigterm
    assert preempt._state.previous is _theirs
    fluent.finish()
    assert signal.getsignal(signal.SIGTERM) is _theirs


def test_a_handler_installed_after_init_is_left_in_place_at_close(opened, preempt):
    """Re-checked at close: a handler that replaced ours after the run opened
    keeps working, never overwritten with what ours had replaced."""
    opened()
    assert signal.getsignal(signal.SIGTERM) is preempt._on_sigterm
    signal.signal(signal.SIGTERM, _theirs)
    fluent.finish()
    assert signal.getsignal(signal.SIGTERM) is _theirs


class _Composed:
    """Lightning's `_HandlersCompose` shape (`signal_handlers`, called in
    order); `test_lightning_logger.py` checks the real one has it."""

    def __init__(self, signal_handlers):
        self.signal_handlers = signal_handlers

    def __call__(self, signum, frame):  # pragma: no cover -- never delivered
        for handler in self.signal_handlers:
            handler(signum, frame)


def test_a_log_puts_ours_in_front_of_a_handler_that_composed_it_last(opened, preempt):
    """Lightning composes ours LAST, behind a notifier that may never return;
    the next `log` moves ours to the front of that list, once, keeping the
    rest in order. A handler of any other shape is left alone."""
    run = opened()
    composed = _Composed([_theirs, print, preempt._on_sigterm])
    signal.signal(signal.SIGTERM, composed)
    try:
        run.log({"loss": 1.0}, step=0)
        assert composed.signal_handlers == [preempt._on_sigterm, _theirs, print]
        run.log({"loss": 0.5}, step=1)
        assert composed.signal_handlers == [preempt._on_sigterm, _theirs, print]
        without_ours = _Composed([_theirs])
        signal.signal(signal.SIGTERM, without_ours)
        run.log({"loss": 0.25}, step=2)
        assert without_ours.signal_handlers == [_theirs]
        signal.signal(signal.SIGTERM, _theirs)
        run.log({"loss": 0.125}, step=3)
        assert signal.getsignal(signal.SIGTERM) is _theirs
    finally:
        signal.signal(signal.SIGTERM, preempt._on_sigterm)
        fluent.finish()


def test_an_ignored_sigterm_stays_ignored(opened, preempt):
    opened()
    assert signal.getsignal(signal.SIGTERM) is preempt._on_sigterm  # the contrast
    fluent.finish()
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    opened()
    assert signal.getsignal(signal.SIGTERM) is signal.SIG_IGN
    fluent.finish()


def test_a_run_opened_off_the_main_thread_installs_nothing(opened, preempt):
    import threading

    opened()
    assert signal.getsignal(signal.SIGTERM) is preempt._on_sigterm  # the contrast
    fluent.finish()
    done = []
    worker = threading.Thread(target=lambda: done.append(opened()))
    worker.start()
    worker.join(30)
    assert done, "init did not return"
    assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL
    done[0].finish()


def test_zero_installs_nothing(opened, monkeypatch, preempt):
    opened()
    assert signal.getsignal(signal.SIGTERM) is preempt._on_sigterm  # the contrast
    fluent.finish()
    monkeypatch.setenv(ENV, "0")
    opened()
    assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL
    fluent.finish()


@pytest.mark.parametrize("raw, seconds", [("", 20.0), ("7.5", 7.5), ("0", 0.0), ("-3", 0.0), ("soon", 20.0)])
def test_the_budget_reads_its_variable(monkeypatch, preempt, raw, seconds):
    monkeypatch.setenv(ENV, raw)
    assert preempt.budget_seconds() == seconds


def test_the_process_exit_code_is_what_a_shell_reports_for_sigterm(preempt):
    assert preempt.EXIT_CODE == 128 + int(signal.SIGTERM) == 143


def test_a_forked_child_without_a_run_of_its_own_dies_as_before(opened, preempt):
    """A DataLoader worker inherits the handler, not the run: SIGTERM there is
    the default action, at once, and closes nothing of the parent's."""
    opened()
    assert signal.getsignal(signal.SIGTERM) is preempt._on_sigterm  # what it inherits
    pid = os.fork()
    if pid == 0:  # pragma: no cover -- the child
        try:
            os.kill(os.getpid(), signal.SIGTERM)
            time.sleep(10)
        finally:
            os._exit(7)
    _, status = os.waitpid(pid, 0)
    assert os.WIFSIGNALED(status) and os.WTERMSIG(status) == signal.SIGTERM
    assert fluent.active_run() is not None and fluent.active_run()._closed_status is None
    fluent.finish()


def test_the_sdk_boundary_is_the_outermost_probe_frame(preempt):
    """The close waits for the main thread to leave the SDK entirely: the
    frame the signal interrupted may be a library the SDK called, with the
    lock-holding SDK frame below it."""
    import types

    def frame(filename: str, back=None):
        return types.SimpleNamespace(f_code=compile("0", filename, "eval"), f_back=back)

    sdk = preempt._SDK_ROOT
    user = frame("/home/me/train.py")
    outer = frame(sdk + "sdk/fluent.py", user)
    inner = frame(sdk + "sdk/journal.py", outer)
    library = frame("/usr/lib/python3.12/json/encoder.py", inner)
    assert preempt._sdk_boundary(library) == (outer, False)
    assert preempt._sdk_boundary(user) == (None, False)


_CAPTURING = _PRELUDE + """
data, out, folder = sys.argv[2], sys.argv[3], sys.argv[4]
run = probe.init(experiment="e1", name="preempted-reads", outputs=folder)
open(data, "rb").read()
with open(out, "wb") as handle:
    handle.write(b"w" * 100)
say("ready", run_id=run.id)
while True:
    time.sleep(0.05)
"""


def test_a_sigterm_close_still_sends_what_the_run_read_and_wrote(app, tmp_path):
    """The read and write lists (lineage) are finalized in the close, within
    its bound -- the SIGTERM close's too: what the run read and wrote reaches
    the server, and the process still dies of SIGTERM on time."""
    import hashlib

    app.seed_experiment("e1")
    folder = tmp_path / "work"
    folder.mkdir()
    data, out = folder / "train.bin", folder / "ckpt.bin"
    data.write_bytes(b"d" * 300)
    with serve(app) as url:
        proc = _spawn(app, url, _CAPTURING, "0", str(data), str(out), str(folder),
                      PROBE_CAPTURE_READS="1", PROBE_CAPTURE_OUTPUTS="1")
        run_id = _wait_for_line(proc, "ready")["run_id"]
        proc.send_signal(signal.SIGTERM)
        returncode, _, err, took = _finish(proc, timeout=30)
    assert returncode == -signal.SIGTERM, (returncode, err[-3000:])
    assert took < 10 + 2, took
    _preempted_by_sigterm(app, run_id)
    reads = [r for b in app.__dict__.get("run_inputs", {}).get(run_id, []) for r in b["inputs"]]
    writes = [r for b in app.__dict__.get("run_outputs", {}).get(run_id, []) for r in b["outputs"]]
    assert [(r["path"], r["content_hash"]) for r in reads if r["path"] == str(data)] == [
        (str(data), hashlib.sha256(b"d" * 300).hexdigest())
    ], err[-3000:]
    assert [(r["path"], r["content_hash"]) for r in writes] == [
        (str(out), hashlib.sha256(b"w" * 100).hexdigest())
    ], err[-3000:]


#: The SIGTERM lands INSIDE the script's own `print`. CPython's BufferedWriter
#: checks for signals between the writes of a flush with the stream's lock
#: held, so the handler runs with sys.stdout's lock taken, and the main thread
#: keeps it while it waits for the close. The release gate hit this by timing
#: (a SIGTERM right after `say("ready")` under a busy runner); the raw layer
#: here only fixes the moment. The lock is the real BufferedWriter's, and the
#: log capture is on, as in the gate.
_SIGTERM_INSIDE_PRINT = _PRELUDE + """
import io

class Raw(io.RawIOBase):
    def writable(self):
        return True

    def write(self, data):
        written = os.write(1, data)
        if b"sigterm-here" in bytes(data):
            os.kill(os.getpid(), signal.SIGTERM)  # handled before this returns
        return written

run = probe.init(experiment="e1", name="preempted-in-print", outputs=sys.argv[2])
loop(run, int(sys.argv[1]))
say("ready", run_id=run.id)
sys.stdout = io.TextIOWrapper(io.BufferedWriter(Raw()), write_through=True)
print("sigterm-here", flush=True)
say("never")
while True:
    time.sleep(0.05)
"""


def test_a_sigterm_inside_a_print_still_closes_the_run(app, tmp_path):
    """Release gate 36503631939 (`AssertionError: running`, 2-3 in 12 on a
    busy box): the SIGTERM close ran on the worker thread while the main
    thread, parked in the handler, held sys.stdout's lock -- the handler had
    run inside the flush of a `print`. The close's log capture flushed
    sys.stdout before restoring the descriptors, waited on that lock for the
    whole budget, and the process died with the run still `running`. The
    close now keeps off both streams on its thread."""
    app.seed_experiment("e1")
    folder = tmp_path / "work"
    folder.mkdir()
    with serve(app) as url:
        proc = _spawn(app, url, _SIGTERM_INSIDE_PRINT, str(STEPS), str(folder),
                      PROBE_CAPTURE_OUTPUTS="1")
        run_id = _wait_for_line(proc, "ready")["run_id"]
        returncode, out, err, took = _finish(proc, timeout=30)
    assert "never" not in _events(out), err[-3000:]
    assert returncode == -signal.SIGTERM, (returncode, err[-3000:])
    assert "could not be closed" not in err, err[-3000:]
    assert took < 10 + 2, took
    assert _points(app, run_id) == _expected(STEPS), err[-3000:]
    _preempted_by_sigterm(app, run_id)


class _HeldStream:
    """A text stream whose BufferedWriter lock another thread holds until
    `release`: what the main thread does when a signal handler ran inside
    its flush. The lock is the real BufferedWriter's."""

    def __init__(self):
        import io
        import threading

        self.entered, self.released = threading.Event(), threading.Event()
        outer = self

        class Raw(io.RawIOBase):
            def writable(self):
                return True

            def write(self, data):
                outer.entered.set()
                outer.released.wait(30)
                return len(data)

        self.stream = io.TextIOWrapper(io.BufferedWriter(Raw()), write_through=True)
        self.holder = threading.Thread(target=self._print, daemon=True)
        self.holder.start()
        assert self.entered.wait(5)

    def _print(self):
        print("held", file=self.stream, flush=True)  # the flush holds the lock

    def release(self):
        self.released.set()
        self.holder.join(5)


def _returns_within(seconds: float, fn) -> bool:
    import threading

    done = threading.Event()

    def run():
        try:
            fn()
        finally:
            done.set()

    threading.Thread(target=run, daemon=True).start()
    return done.wait(seconds)


@pytest.mark.parametrize("which", ["stdout", "stderr"])
def test_the_close_thread_never_waits_on_a_stream_another_thread_holds(
    monkeypatch, capfd, which
):
    """The two ways the SIGTERM close touched the streams -- its warnings and
    the log capture's flush before it restores the descriptors -- return at
    once on a thread inside `streams_off_limits`, whoever holds the stream's
    lock; the warning still reaches fd 2. Negative control: outside it, the
    same flush waits on the lock."""
    from probe.sdk import logcapture, safe_warn

    held = _HeldStream()
    try:
        monkeypatch.setattr(sys, which, held.stream)
        monkeypatch.setattr(sys, f"__{which}__", held.stream)

        def guarded():
            with safe_warn.streams_off_limits():
                safe_warn.warn("probe: the close's warning")
                logcapture._flush_python_streams()

        assert _returns_within(2.0, guarded)
        assert not _returns_within(0.5, logcapture._flush_python_streams)
    finally:
        held.release()
    assert "probe: the close's warning" in capfd.readouterr().err
    assert safe_warn.streams_allowed()  # the guard ends with its block


#: Local-only finalizers (`_inputs.finalize`'s hashing wait, the hardware
#: collector) each bound themselves to "half of what's left" -- correctly
#: bounded on their own, but with NOTHING to stop them together from spending
#: the WHOLE budget: 50% then 50% of the remainder is 75%, leaving no more
#: than the drain's own reserve. Under real scheduling delay a bounded wait
#: routinely takes its FULL share (a `Thread.join(timeout)` starved of CPU
#: returns only at `timeout`, and getting the CPU back to even COMPUTE "what
#: is left" for the next step costs more on top) -- this prelude fakes that
#: deterministically, no load or luck needed, by making both steps sleep 1.6x
#: their granted share (the measured slack a correctly-bounded wait still
#: loses to scheduling before the caller runs again) and giving the fake
#: server a flat 0.6s per request, close to what a loopback call costs when
#: every core is oversubscribed.
_SLOW_LOCAL_FINALIZERS = _PRELUDE + """
from probe.sdk import inputs as _inputs

data, out, folder = sys.argv[2], sys.argv[3], sys.argv[4]
FACTOR = 1.6

real_finalize = _inputs.finalize

def slow_finalize(client, run_id, *, wait_s=_inputs.FINISH_WAIT_S, ignore=None):
    time.sleep(max(0.0, wait_s) * FACTOR)
    return real_finalize(client, run_id, wait_s=0.0, ignore=ignore)

_inputs.finalize = slow_finalize

class _SlowHW:
    def finish(self, timeout=0.0):
        time.sleep(max(0.0, timeout) * FACTOR)

run = probe.init(experiment="e1", name="preempted-reads", outputs=folder)
run._hw_monitor = _SlowHW()
open(data, "rb").read()
with open(out, "wb") as handle:
    handle.write(b"w" * 100)
say("ready", run_id=run.id)
while True:
    time.sleep(0.05)
"""


def test_a_sigterm_close_survives_local_finalizers_that_use_their_whole_budget(app, tmp_path):
    """Regression test for the read/write capture flake (dry run 36471965949,
    test_a_sigterm_close_still_sends_what_the_run_read_and_wrote): lineage
    hashing and the hardware collector each individually respect their own
    "half of what's left" bound, but chained one after the other that is 75%
    of the WHOLE close budget -- and `_close_within` computed its delivery
    reserve from the ORIGINAL deadline, not from what was left once they were
    done. Under real scheduling delay both routinely spend more than their
    nominal share (see `_SLOW_LOCAL_FINALIZERS`), so the drain and the
    terminal status write were left with ~0s: the run stayed `running`
    (`AssertionError: running`) even though the process still died by SIGTERM
    on time. This reproduces that deterministically -- no CPU load needed --
    and fails on the code before `_close_reserve`/`finalize_ceiling` (run.py)
    protected the reserve from the local finalizers (verified: FAILS with
    `status="running"` on that code, in ~9.4s -- the process ran out its
    whole budget with the close still unfinished; PASSES here every time)."""
    app.seed_experiment("e1")
    app.latency = lambda request: 0.6
    folder = tmp_path / "work"
    folder.mkdir()
    data, out = folder / "train.bin", folder / "ckpt.bin"
    data.write_bytes(b"d" * 300)
    with serve(app) as url:
        proc = _spawn(app, url, _SLOW_LOCAL_FINALIZERS, "0", str(data), str(out), str(folder),
                      PROBE_CAPTURE_READS="1", PROBE_CAPTURE_OUTPUTS="1")
        run_id = _wait_for_line(proc, "ready")["run_id"]
        proc.send_signal(signal.SIGTERM)
        returncode, _, err, took = _finish(proc, timeout=30)
    assert returncode == -signal.SIGTERM, (returncode, err[-3000:])
    assert took < 12 + 2, took
    row = app.runs[run_id]
    assert row["status"] == "failed", (row["status"], err[-3000:])
