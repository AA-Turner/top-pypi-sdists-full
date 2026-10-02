"""The node agent as one feature, driven end to end with real processes.

The unit tests in `test_node_agent.py` prove each part in isolation, with the
process table stubbed and the pids invented. That is the wrong shape for the
one claim this feature actually makes: that when a real process dies, on a
real box, something outside it notices and says whose run it was.

So everything here spawns real OS processes and kills them for real. What is
faked is only the network: a recording transport stands in for the API, which
is the one thing that cannot be exercised without a server.

WHY THIS LANE EXISTS AT ALL. Two of the three failure modes this design
guards against are invisible to a unit test with a stubbed process table:

  * a watcher that takes the same Ctrl-C as the job it is watching, because it
    was left in the job's process group -- the unit test asserts we pass
    `start_new_session=True`, which is a claim about an argument, not about
    what the kernel then does;
  * a recycled pid, which needs two real processes and the kernel's own
    creation clock to demonstrate.

Both are verified here against the operating system rather than against a
mock of it.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

from probe.box import registry, spawn, watch

RUN = "11111111-1111-4111-8111-111111111111"

#: A child that does nothing until killed. Started with `-c` so the test needs
#: no fixture files and no import path games.
_SLEEPER = "import time; time.sleep(300)"


@pytest.fixture
def box(tmp_path: Path) -> Path:
    return tmp_path / "runs"


def _spawn_sleeper() -> subprocess.Popen:
    return subprocess.Popen(  # noqa: S603 -- argv is ours
        [sys.executable, "-c", _SLEEPER],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _wait_gone(pid: int, timeout: float = 5.0) -> bool:
    """Block until the kernel has actually reaped the pid. `kill` returns
    before the process is gone, and asserting into that window is how a test
    like this becomes flaky on a loaded machine."""
    import psutil

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not psutil.pid_exists(pid):
            return True
        time.sleep(0.02)
    return False


class _Recorder:
    """Stands in for the API. Records what the watcher would have sent."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict]] = []

    def write(self, method, path, body, **kw):
        self.calls.append((method, path, body))
        return {"ok": True}

    @property
    def spans(self) -> list[dict]:
        return [s for _, _, body in self.calls for s in body.get("spans", [])]


@pytest.fixture
def api(monkeypatch) -> _Recorder:
    recorder = _Recorder()
    monkeypatch.setattr(watch, "_client_for", lambda entry: recorder)
    return recorder


# -- the whole path, with a real death -------------------------------------------


def test_a_real_process_dying_is_noticed_and_attributed(box, api) -> None:
    """The feature's one claim, exercised: kill a real process, and the thing
    outside it reports whose run that was."""
    child = _spawn_sleeper()
    registry.register(RUN, pid=child.pid, directory=box, context="default")

    assert watch.sweep(box) == {"alive": 1, "gone": 0, "reported": 0}
    assert api.spans == [], "a living process must produce no evidence at all"

    child.kill()
    child.wait()
    assert _wait_gone(child.pid)

    tally = watch.sweep(box)

    assert tally == {"alive": 0, "gone": 1, "reported": 1}
    (span,) = api.spans
    assert span["span_type"] == "node_event"
    assert span["name"] == "process_vanished"
    assert span["attributes"]["pid"] == child.pid
    assert span["attributes"]["observer"] == "node-agent"
    assert span["attributes"]["observed_seconds"] >= 0
    ((method, path, _),) = api.calls
    assert method == "POST"
    assert path == f"/v1/runs/{RUN}/spans"


def test_the_span_is_not_a_diagnostic(box, api) -> None:
    """`app/notifications/evidence.py` parses a `diagnostic` span as a scrubbed
    exception chain. A node observation is not a traceback, and typing it as
    one would put an invented cause in a crash email."""
    child = _spawn_sleeper()
    registry.register(RUN, pid=child.pid, directory=box)
    child.kill()
    child.wait()
    _wait_gone(child.pid)

    watch.sweep(box)

    (span,) = api.spans
    assert span["span_type"] != "diagnostic"
    assert "exception" not in span["attributes"]


def test_a_clean_close_leaves_nothing_to_explain(box, api) -> None:
    """The false alarm this design most has to avoid: a run that closed itself
    properly, whose process then exits, must not read as a death."""
    child = _spawn_sleeper()
    registry.register(RUN, pid=child.pid, directory=box)

    registry.deregister(RUN, directory=box)  # what Run.finish() does
    child.kill()
    child.wait()
    _wait_gone(child.pid)

    assert watch.sweep(box) == {"alive": 0, "gone": 0, "reported": 0}
    assert api.spans == []


def test_a_recycled_pid_is_not_the_dead_run(box, api) -> None:
    """Against the real kernel clock, not a stubbed one: a second process
    standing in for one that took the dead one's number must not read as the
    original run still running.

    THE SPACING IS LOAD-BEARING AND IS ABOUT THE PLATFORM, not about this
    code. Linux reads a process's start time from `/proc/[pid]/stat` in clock
    ticks -- 100 Hz, so 10ms resolution -- and two processes spawned back to
    back land in the SAME TICK with byte-identical timestamps. macOS reports
    microseconds, so the first version of this test passed locally and failed
    on both CI Pythons.

    Real pid reuse cannot hit that window: the kernel must cycle through its
    whole pid space first, which is thousands of process creations and orders
    of magnitude more than 10ms. So the guard is sound and the TEST was
    artificial. Sleeping one tick is what makes the simulation honest on every
    platform rather than only on the one I develop on.
    """
    first = _spawn_sleeper()
    registry.register(RUN, pid=first.pid, directory=box)
    first.kill()
    first.wait()
    _wait_gone(first.pid)

    # One clock tick, so the second process is distinguishable from the first
    # on a 100 Hz platform as well as on a microsecond one.
    time.sleep(0.05)

    # A different live process, rewritten into the entry as if it had inherited
    # the id. Its creation time is its own, so identity must reject it.
    second = _spawn_sleeper()
    try:
        path = next(box.glob("*.json"))
        entry = json.loads(path.read_text())
        entry["pid"] = second.pid  # the id is "reused"
        path.write_text(json.dumps(entry))  # create_time still the first one's

        tally = watch.sweep(box)

        assert tally["gone"] == 1, (
            "a live process wearing the dead one's id must not read as the run "
            "still running -- that is the failure that hides a death forever"
        )
        assert len(api.spans) == 1
    finally:
        second.kill()
        second.wait()


def test_several_runs_on_one_box_are_attributed_separately(box, api) -> None:
    """One watcher, many jobs -- the ordinary case on a shared machine."""
    runs = {
        "aaaaaaaa-1111-4111-8111-111111111111": _spawn_sleeper(),
        "bbbbbbbb-2222-4222-8222-222222222222": _spawn_sleeper(),
        "cccccccc-3333-4333-8333-333333333333": _spawn_sleeper(),
    }
    for run_id, proc in runs.items():
        registry.register(run_id, pid=proc.pid, directory=box)

    doomed = "bbbbbbbb-2222-4222-8222-222222222222"
    runs[doomed].kill()
    runs[doomed].wait()
    _wait_gone(runs[doomed].pid)

    try:
        tally = watch.sweep(box)

        assert tally == {"alive": 2, "gone": 1, "reported": 1}
        ((_, path, _),) = api.calls
        assert doomed in path, "the right run, not just some run"
        assert {e["run_id"] for e in registry.entries(box)} == set(runs) - {doomed}
    finally:
        for run_id, proc in runs.items():
            if run_id != doomed:
                proc.kill()
                proc.wait()


@pytest.mark.parametrize("sig", [signal.SIGKILL, signal.SIGTERM, signal.SIGINT])
def test_every_kind_of_death_is_noticed(box, api, sig) -> None:
    """The watcher reports that the process is GONE and never guesses why. All
    three of these are indistinguishable from outside, which is exactly why the
    evidence it writes says 'vanished' and not a cause."""
    child = _spawn_sleeper()
    registry.register(RUN, pid=child.pid, directory=box)
    child.send_signal(sig)
    child.wait()
    assert _wait_gone(child.pid)

    assert watch.sweep(box)["gone"] == 1
    (span,) = api.spans
    assert span["attributes"]["event"] == "process_vanished"


# -- the watcher process, spawned for real ----------------------------------------


def test_the_watcher_survives_a_signal_aimed_at_the_job(box, monkeypatch) -> None:
    """THE PROPERTY A MOCK CANNOT PROVE. A watcher left in the training job's
    process group takes the same Ctrl-C the job takes -- and a Ctrl-C is one of
    the deaths it exists to observe. The unit test asserts we pass
    `start_new_session=True`; this asserts the kernel then honours it.
    """
    import psutil

    monkeypatch.setenv("PROBE_BOX", "1")
    assert spawn.maybe_spawn(box) is True

    # Find it: a detached child is not in `Popen`'s hands any more.
    deadline = time.monotonic() + 10.0
    watcher = None
    while time.monotonic() < deadline and watcher is None:
        for proc in psutil.process_iter(["pid", "cmdline"]):
            cmdline = proc.info.get("cmdline") or []
            if "probe.box" in cmdline and proc.pid != os.getpid():
                watcher = proc
                break
        time.sleep(0.05)
    assert watcher is not None, "the watcher never started"

    try:
        assert os.getpgid(watcher.pid) != os.getpgid(os.getpid()), (
            "the watcher shares the job's process group; a Ctrl-C would take both"
        )
        # Signal THIS process's group, the way a terminal does. The watcher is
        # in its own, so it must be untouched.
        os.killpg(os.getpgid(os.getpid()), signal.SIGCONT)
        time.sleep(0.2)
        assert watcher.is_running(), "the watcher died with the job's group"
    finally:
        try:
            watcher.kill()
            watcher.wait(timeout=5)
        except Exception:  # noqa: BLE001 -- best effort teardown
            pass


def test_only_one_watcher_starts_when_many_runs_race(box, monkeypatch) -> None:
    """Sixty-four ranks start together; the lease makes all but one a no-op."""
    monkeypatch.setenv("PROBE_BOX", "1")
    started: list[object] = []
    monkeypatch.setattr(spawn.subprocess, "Popen", lambda *a, **k: started.append(a) or object())

    held = spawn.hold_lease(box)
    assert held is not None
    for _ in range(64):
        spawn.maybe_spawn(box)
    assert started == [], "a watcher already holds the box"

    held.close()
    for _ in range(64):
        spawn.maybe_spawn(box)
    assert len(started) == 64, (
        "without a holder each call spawns; the real lease is taken by the "
        "watcher itself at startup, which this stub cannot do"
    )


def test_the_watcher_exits_on_its_own_when_the_box_goes_quiet(box, monkeypatch) -> None:
    """Otherwise it idles forever on somebody's laptop."""
    monkeypatch.setenv("PROBE_BOX", "1")
    monkeypatch.setenv("PROBE_BOX_DIR", str(box))
    # Through the environment, which is the only channel a DETACHED watcher
    # has. Patching the module constant was the first attempt and could not
    # work: the default binds at definition time, and nothing holds a handle
    # to this process to pass it anything.
    monkeypatch.setenv("PROBE_BOX_INTERVAL", "0.1")
    monkeypatch.setenv("PROBE_BOX_IDLE_EXIT", "0.5")
    env = dict(os.environ)

    proc = subprocess.Popen(  # noqa: S603
        [sys.executable, "-m", "probe.box"],
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        assert proc.wait(timeout=20) == 0, "a quiet box must let the watcher retire"
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()


# -- it must never touch the run ---------------------------------------------------


def test_registration_survives_an_unwritable_directory(tmp_path, monkeypatch) -> None:
    """Fail-open is the contract: a broken registry costs the box its knowledge
    of one run and costs the researcher nothing."""
    blocked = tmp_path / "blocked"
    blocked.mkdir()
    blocked.chmod(0o500)
    try:
        assert registry.register(RUN, directory=blocked / "runs") is None
        assert registry.entries(blocked / "runs") == []
    finally:
        blocked.chmod(0o700)


def test_a_broken_api_never_raises_at_the_watcher(box, monkeypatch) -> None:
    def explode(entry):
        raise RuntimeError("the API is down")

    monkeypatch.setattr(watch, "_client_for", explode)
    child = _spawn_sleeper()
    registry.register(RUN, pid=child.pid, directory=box)
    child.kill()
    child.wait()
    _wait_gone(child.pid)

    tally = watch.sweep(box)

    assert tally == {"alive": 0, "gone": 1, "reported": 0}
    assert registry.entries(box) == [], "and it stops watching rather than spinning"


def test_the_watcher_never_signals_anything_it_watches(box, api, monkeypatch) -> None:
    """It is an observer: it may ASK whether a process exists, and may never
    disturb one.

    Signal 0 is the asking. `kill(pid, 0)` delivers nothing and is how POSIX
    answers "is this pid alive" -- it is what `psutil.pid_exists` calls, so
    banning it outright would ban the feature. Everything else is a real
    signal and must never appear.
    """
    real_kill = os.kill
    delivered: list[tuple] = []

    def watched_kill(pid, sig, *rest):
        if sig != 0:
            delivered.append((pid, sig))
        return real_kill(pid, sig, *rest)

    monkeypatch.setattr(os, "kill", watched_kill)
    monkeypatch.setattr(os, "killpg", lambda *a: delivered.append(a))

    child = _spawn_sleeper()
    try:
        registry.register(RUN, pid=child.pid, directory=box)
        watch.sweep(box)  # alive
        assert delivered == [], "watching a live process must disturb nothing"
        real_kill(child.pid, signal.SIGKILL)  # the test's own kill, not the agent's
        child.wait()
        _wait_gone(child.pid)
        delivered.clear()
        watch.sweep(box)  # gone
    finally:
        if child.poll() is None:
            real_kill(child.pid, signal.SIGKILL)
            child.wait()

    assert delivered == [], "the node agent must never deliver a signal"
