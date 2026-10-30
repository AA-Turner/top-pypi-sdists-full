"""The service's updater (plan X1, R2, R3, D3, D4, Q4): real service, real processes.

A cycle runs CLI-and-plugins (one `probe.core.run update` child), then the
desktop app's step (handed to the open app, never a launch of it), then reads
the installed CLI version and restarts the service when it moved. Step 1 runs only on a quiet machine: a daemon
worker's lock, a run lock, `wizard.lock` or a running action defers it (with a
skip `probe doctor` reads, and a retry when a session ends), and the update
barrier is up while it runs, which a CLI start waits for. A cycle holds the
service alive. Automatic updates off: nothing runs. The CLI and the plugin hook
ask the service instead of spawning their own updater while the switch is on.

`FakeCore` plays the `probe.core.run` children, `fake_open` macOS's `open`
(every call recorded: the service must never make one), `fake_app` a
`Probe.app` bundle. The desktop app is a connection whose hello says `app`.
"""

from __future__ import annotations

import contextlib
import fcntl
import importlib.util
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest

import probe
from probe._shared import installs as installs_mod
from probe.service import appupdate, barrier, client, paths
from probe.service import updater
from probe.service.protocol import Client, Method, Mode, StopReason
from tests.service_fakes import (
    FakeCore,
    autoupdate_state,
    enable_auto_update,
    events_until,
    fake_app,
    fake_open,
    last_checked,
    open_calls,
)
from tests.service_harness import (  # noqa: F401 -- service_home is a fixture
    kill_agent,
    pid_running,
    service_home,
    spawn_agent,
    wait_for,
)

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")

_ROOT = Path(__file__).resolve().parent.parent
#: The service looks in /Applications before ~/Applications, and a test cannot
#: move that: on a Mac with the desktop app installed, the real bundle is found
#: instead of the fake one these tests build.
no_real_app = pytest.mark.skipif(
    (Path("/Applications") / appupdate.APP_NAME).exists(), reason="a real /Applications/Probe.app is found first"
)
#: A closed app is `skipped: app_closed` where there is no desktop app (Linux,
#: where these run in CI). On macOS the service installs a closed app's update
#: itself, from the real release: tests/test_service_appinstall.py.
closed_app_skips = pytest.mark.skipif(
    sys.platform == "darwin", reason="on macOS the service installs a closed app's update (test_service_appinstall.py)"
)
UPDATE_TOPICS = ["update.started", "update.step", "update.deferred", "update.done", "service.stopping"]
STEP = {"event": "step", "name": "persistent_install", "status": "done", "message": "CLI current", "agent": None}


@pytest.fixture
def machine(service_home, monkeypatch):
    """A machine with automatic updates on, a fake CLI interpreter, and an
    `open` on PATH. The last update check was an hour ago: not due when the
    service starts, and outside `update.check_now`'s cooldown."""
    core = FakeCore(service_home.home)
    core.plan("update", steps=[{"event": STEP}])
    core.plan("version", stdout={"cli_version": probe.__version__})
    bin_dir = service_home.home / "bin"
    fake_open(bin_dir)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    enable_auto_update(service_home.home)
    last_checked(hours_ago=1)
    return core


def _check_now(conn, trigger="cli") -> dict:
    return conn.call(Method.UPDATE_CHECK_NOW, {"trigger": trigger})


def _done(conn, timeout=20.0) -> list[dict]:
    return events_until(conn, lambda e: e["topic"] == "update.done", timeout)


def _hold(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = open(path, "a+")  # noqa: SIM115 -- the caller closes it
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    return handle


# -- a cycle ------------------------------------------------------------------


@no_real_app
@closed_app_skips
def test_a_cycle_runs_cli_and_plugins_then_the_app_then_reads_the_version(service_home, machine, monkeypatch):
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_launcher_secret")
    fake_app(service_home.home)
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        started = _check_now(conn, "session")
        assert started["outcome"] == "started" and "app" not in started  # nobody asked for the app
        seen = _done(conn)
        status = conn.call(Method.UPDATE_STATUS)
    steps = [(e["step"], e.get("state")) for e in seen if e["topic"] == "update.step" and "state" in e]
    assert steps == [
        ("cli_and_plugins", "started"),
        ("cli_and_plugins", "done"),
        ("app", "skipped"),
        ("self", "done"),
    ]
    forwarded = [e["event"] for e in seen if e["topic"] == "update.step" and "event" in e]
    assert [e["event"] for e in forwarded] == ["step", "done"]
    done = seen[-1]
    assert done["cycle_id"] == started["cycle_id"] and done["ok"] is True and done["restart"] is False
    # The app is installed but not open: nothing is launched, and its next launch is due.
    assert done["steps"]["app"] == {"state": "skipped", "outcome": "app_closed", "version": "0.1.3"}
    assert open_calls(service_home.home) == []
    assert status["app"]["due"] is True and status["app"]["reason"] == "never_checked"
    assert status["app"]["last_check"] is None and status["app"]["last"] is None
    # In that order, as processes: the update child, then the version read.
    (update,) = machine.calls("update")
    (version,) = machine.calls("version")
    assert update["at"] < version["at"]
    # The child: the barrier up, its token and the trigger in its env, no launcher credential.
    assert update["barrier"] is True
    assert update["env"]["PROBE_UPDATE_BARRIER_TOKEN"]
    assert update["env"]["PROBE_AUTOUPDATE_TRIGGER"] == "session_start"
    assert update["env"]["PROBE_TOKEN"] is None
    assert not paths.barrier_path().exists()
    assert status["in_progress"] is False and status["last_result"]["ok"] is True
    assert status["last_check"] > time.time() - 60
    # Just checked: another check_now within the cooldown changes nothing.
    with service_home.connect() as conn:
        assert _check_now(conn)["outcome"] == "recent"
    assert len(machine.calls("update")) == 1


def test_a_due_check_runs_after_discovery_and_not_before(service_home, machine, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_DISCOVERY_S", "1.5")
    paths.update_state_path().unlink()  # never checked: due at once
    service_home.start()
    time.sleep(0.8)
    assert machine.calls("update") == []  # discovering: no updates (X6)
    assert wait_for(lambda: machine.calls("update"), 10.0)
    assert wait_for(lambda: not service_home.call(Method.UPDATE_STATUS)["in_progress"], 10.0)


def test_check_now_while_discovering_is_scheduled(service_home, machine, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_DISCOVERY_S", "1.5")
    service_home.start()  # the fixture's check an hour ago: not due on its own
    with service_home.connect() as conn:
        assert _check_now(conn) == {"outcome": "scheduled"}
    assert wait_for(lambda: machine.calls("update"), 10.0)


def test_automatic_updates_off_runs_nothing(service_home, machine):
    enable_auto_update(service_home.home, False)
    paths.update_state_path().unlink()  # due, if updates were on
    fake_app(service_home.home)
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        assert _check_now(conn) == {"outcome": "deferred", "reason": "auto_update_off"}
        assert conn.next_event(2.0)["reason"] == "auto_update_off"
        assert conn.call(Method.UPDATE_STATUS)["enabled"] is False
    time.sleep(0.5)
    assert machine.calls() == [] and open_calls(service_home.home) == []


# -- quiet check and barrier (X1) ----------------------------------------------


def test_a_daemon_worker_defers_the_update_until_its_session_ends(service_home, machine):
    lock = _hold(service_home.home / ".local" / "state" / "probe" / "daemon" / "s-daemon.lock")
    service_home.start()
    agent, owner = spawn_agent()
    try:
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            conn.call(
                Method.SESSION_REGISTER,
                {"sid": "s-daemon", "harness": "test", "mode": Mode.DAEMON, "owner": owner, "generation": 1},
            )
            assert _check_now(conn)["outcome"] == "started"
            seen = _done(conn)
            assert [e["reason"] for e in seen if e["topic"] == "update.deferred"] == ["daemon_recording"]
            assert seen[-1]["deferred"] == "daemon_recording" and seen[-1]["ok"] is False
            assert conn.call(Method.UPDATE_STATUS)["deferred"]["reason"] == "daemon_recording"
        assert machine.calls("update") == []
        skip = autoupdate_state(service_home.home)["last_skip"]
        assert skip["reason"] == "a Probe daemon is recording" and skip["trigger"] == "cli"
        # The session ends and its worker lets go: the update is retried by itself.
        lock.close()
        kill_agent(agent)
        assert wait_for(lambda: machine.calls("update"), 10.0), service_home.log()
    finally:
        lock.close()
        kill_agent(agent)


def test_a_worker_draining_after_its_session_ended_is_waited_for(service_home, machine):
    """In production the agent goes first (session.ended) and its worker then
    drains its queue, holding its lock, for minutes: the retry after the
    session ends finds it busy, and looks again until it lets go."""
    lock = _hold(service_home.home / ".local" / "state" / "probe" / "daemon" / "s-drain.lock")
    service_home.start()
    agent, owner = spawn_agent()
    try:
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            conn.call(
                Method.SESSION_REGISTER,
                {"sid": "s-drain", "harness": "test", "mode": Mode.DAEMON, "owner": owner, "generation": 1},
            )
            _check_now(conn)
            assert _done(conn)[-1]["deferred"] == "daemon_recording"
        kill_agent(agent)  # the session ends first ...
        time.sleep(3.0)  # ... past the first retry, while its worker drains ...
        assert machine.calls("update") == []
        lock.close()  # ... then lets go
        assert wait_for(lambda: machine.calls("update"), 10.0), service_home.log()
    finally:
        lock.close()
        kill_agent(agent)


def test_a_daemon_session_in_another_state_dir_defers_the_update(service_home, machine):
    """A session run with XDG_STATE_HOME keeps its worker's lock out of the
    service's sight (the service's own state is fixed under $HOME, plan X2).
    It registered in daemon mode: that alone says a worker records."""
    service_home.start()
    agent, owner = spawn_agent()
    try:
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            conn.call(
                Method.SESSION_REGISTER,
                {"sid": "s-xdg", "harness": "test", "mode": Mode.DAEMON, "owner": owner, "generation": 1},
            )
            _check_now(conn)
            assert _done(conn)[-1]["deferred"] == "daemon_recording"
        assert machine.calls("update") == []
        kill_agent(agent)
        assert wait_for(lambda: machine.calls("update"), 10.0), service_home.log()
    finally:
        kill_agent(agent)


def test_a_lock_taken_while_the_barrier_settles_defers_the_update(service_home, machine):
    """The second look, after the barrier and its settle (X1): a worker that
    passed the barrier a moment before it was raised and takes its lock
    during the settle is seen, and nothing is updated."""
    import threading

    lock_path = service_home.home / ".local" / "state" / "probe" / "daemon" / "s-late.lock"
    service_home.start()
    held: dict = {}

    def late_worker() -> None:
        if wait_for(paths.barrier_path().exists, 10.0, interval=0.005):
            time.sleep(0.3)  # inside BARRIER_SETTLE_S
            held["lock"] = _hold(lock_path)

    thread = threading.Thread(target=late_worker)
    thread.start()
    try:
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            seen = _done(conn)
    finally:
        thread.join()
        if "lock" in held:
            held["lock"].close()
    assert "lock" in held
    assert seen[-1]["deferred"] == "daemon_recording"
    assert machine.calls("update") == []


def test_a_deferred_update_is_tried_again_by_the_next_service(service_home, machine):
    lock = _hold(service_home.home / ".local" / "state" / "probe" / "wizard.lock")
    first = service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        _check_now(conn)
        assert _done(conn)[-1]["deferred"] == "setup_running"
        conn.call(Method.STOP)
    assert service_home.wait_exit(first["pid"], 5.0)
    lock.close()
    service_home.start()  # not due on its own (checked an hour ago): the deferral is
    assert wait_for(lambda: machine.calls("update"), 10.0), service_home.log()
    assert machine.calls("update")[0]["env"]["PROBE_AUTOUPDATE_TRIGGER"] == "cli"


@pytest.mark.parametrize(
    ("held", "reason", "skip"),
    [
        ("runs/r-1.flock", "run_in_flight", "run in flight"),
        ("wizard.lock", "setup_running", "another Probe setup is running"),
    ],
)
def test_a_run_or_a_setup_defers_the_update(service_home, machine, held, reason, skip):
    lock = _hold(service_home.home / ".local" / "state" / "probe" / held)
    try:
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            seen = _done(conn)
    finally:
        lock.close()
    assert seen[-1]["deferred"] == reason
    assert machine.calls("update") == []
    assert autoupdate_state(service_home.home)["last_skip"]["reason"] == skip


def test_a_running_action_defers_the_update_and_an_action_waits_for_the_update(service_home, machine):
    gate = service_home.home / "release"
    machine.plan("logout", steps=[{"wait": str(gate)}])
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        conn.call(Method.ACTION_RUN, {"action": "logout", "params": {}, "client_request_id": "a"})
        wait_for(lambda: machine.calls("logout"), 5.0)
        _check_now(conn)
        assert _done(conn)[-1]["deferred"] == "action_running"
        gate.touch()
    # The other way round: an action asked for while the update step holds the
    # slot is queued, never refused (the app opens, starting a cycle, and a
    # setting is changed at once), and runs once that step lets go.
    slow = service_home.home / "update-may-finish"
    machine.plan("update", steps=[{"wait": str(slow)}])
    with service_home.connect() as conn:
        assert wait_for(lambda: conn.call(Method.STATUS)["actions"]["running"] is None, 5.0)
        assert _check_now(conn)["outcome"] == "started"
        wait_for(lambda: machine.calls("update"), 10.0)
        answer = conn.call(Method.ACTION_RUN, {"action": "logout", "params": {}, "client_request_id": "b"})
        waiting = answer["action_id"]
        assert answer == {"action_id": waiting, "queued": True}
        assert conn.call(Method.ACTION_STATUS, {"action_id": waiting})["state"] == "queued"
        assert conn.call(Method.STATUS)["actions"] == {"running": None, "queued": [waiting]}
        # An Update while the update runs is that same work: still busy.
        with pytest.raises(client.ServiceError) as raised:
            conn.call(Method.ACTION_RUN, {"action": "update", "params": {}, "client_request_id": "c"})
        assert raised.value.code == -32010 and raised.value.data["holder"]["kind"] == "update"
        with pytest.raises(client.ServiceError) as stop:
            conn.call(Method.STOP)
        assert stop.value.data == {"reason": "updating"}
        time.sleep(0.5)
        assert len(machine.calls("logout")) == 1, "nothing runs under the update"
        released = time.time()
        slow.touch()
        assert wait_for(
            lambda: conn.call(Method.ACTION_STATUS, {"action_id": waiting})["state"] == "done", 20.0
        ), service_home.log()
        status = conn.call(Method.ACTION_STATUS, {"action_id": waiting})
    assert status["done"]["ok"] is True, status
    assert machine.calls("logout")[1]["at"] >= released
    journal = [json.loads(line) for line in (paths.actions_dir() / f"{waiting}.jsonl").read_text().splitlines()]
    assert [line["type"] for line in journal][:3] == ["accepted", "queued", "child"]
    assert journal[1]["holder"]["kind"] == "update"


def test_a_cli_start_waits_for_the_barrier(service_home):
    token = "t" * 32
    barrier.raise_barrier(token)  # this test process stands in for the service
    script = (
        "import sys; from probe import _entry\n"
        "_entry.main = None\n"  # nothing past the barrier runs: only whether it waited
        "_entry._rerun = lambda argv: print('rerun', argv) or 0\n"  # re-runs on the new code once it is done
        "busy = _entry._update_barrier(['log', 'loss', '0.1']); print('passed' if busy is None else busy)"
    )
    started = time.monotonic()
    child = subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(1.0)
    assert child.poll() is None  # still waiting: nothing of the CLI imported yet
    barrier.lower(token)
    out, err = child.communicate(timeout=60)
    assert child.returncode == 0 and out.split("\n")[0] == "rerun ['log', 'loss', '0.1']", (out, err)
    assert time.monotonic() - started >= 1.0


@pytest.mark.parametrize("kind", ["side-by-side", "plugins-only", "pinned-env", "hook", "read-only", "in-place"])
def test_a_cli_start_during_an_update_runs_on_the_installed_version_at_once(service_home, monkeypatch, kind):
    """Every `probe` waited up to 10 s during an update, then exited 75 (live
    test, 2026-10-24): a training loop's `probe log`, a hook's call, `probe
    status`. An update side by side (D6), or of the plugins only, replaces
    nothing a `probe` runs from: it runs on the installed version at once. A
    process already pinned to a version env (`probe-versions/<v>`) is never
    replaced either. Only an in-place update still holds a start back: a hook
    never waits (busy at once); every other command, a read-only one too,
    waits it out (IN_PLACE_WAIT_S) rather than fail an agent mid-work."""
    from probe import _entry

    monkeypatch.setattr(_entry, "IN_PLACE_WAIT_S", 1.0)
    token = "v" * 32
    barrier.raise_barrier(token)
    if kind in ("side-by-side", "plugins-only"):
        # What the updater writes for them (`raise_barrier(..., replaces_cli=False)`).
        record = json.loads(paths.barrier_path().read_text())
        paths.barrier_path().write_text(json.dumps({**record, "replaces_cli": False}))
    if kind == "pinned-env":
        monkeypatch.setattr(sys, "prefix", "/home/x/.local/share/uv/probe-versions/0.300.0/probe-research")
    if kind == "hook":
        monkeypatch.setenv(barrier.DEADLINE_ENV, repr(time.time() + 8))
    argv = ["status"] if kind == "read-only" else ["log", "loss", "0.1"]
    try:
        started = time.monotonic()
        busy = _entry._update_barrier(argv)
        took = time.monotonic() - started
    finally:
        barrier.lower(token)
    if kind in ("side-by-side", "plugins-only", "pinned-env"):
        assert busy is None and took < 0.5, (busy, took)
    elif kind == "hook":
        assert busy == barrier.BUSY_EXIT_CODE and took < 0.5, (busy, took)
    else:
        assert busy == barrier.BUSY_EXIT_CODE and took >= _entry.IN_PLACE_WAIT_S - 0.2, (busy, took)


@pytest.mark.parametrize(("deadline", "never"), [
    (8.0, True),        # a hook's own call: its turn is the deadline
    (-5.0, True),       # just past: the hook is out of time, still a hook
    (-3600.0, False),   # a detached job that outlived its hook waits as any command
    ("nan", False),
    ("not a number", False),
    (None, False),
])
def test_only_a_live_hook_deadline_never_waits(monkeypatch, deadline, never):
    """`barrier.budget()` reads a deadline more than STALE_DEADLINE_S past as a
    process the hook left behind, which waits like any command: `_never_waits`
    held every PROBE_HOOK_DEADLINE a hook, so such a job answered busy at once
    during an in-place update."""
    from probe import _entry

    if deadline is None:
        monkeypatch.delenv(barrier.DEADLINE_ENV, raising=False)
    elif isinstance(deadline, float):
        monkeypatch.setenv(barrier.DEADLINE_ENV, repr(time.time() + deadline))
    else:
        monkeypatch.setenv(barrier.DEADLINE_ENV, deadline)
    assert _entry._never_waits(["log", "loss", "0.1"]) is never
    assert barrier.hook_deadline_live() is never


def test_the_barrier_knows_a_version_env_as_installs_does():
    assert barrier.PINNED_DIR == f"/{installs_mod.VERSIONS_DIRNAME}/"
    assert barrier.pinned("/h/.local/share/uv/probe-versions/1.2.3/probe-research") is True
    assert barrier.pinned("/h/.local/share/uv/tools/probe-research") is False
    barrier.raise_barrier("w" * 32, replaces_cli=False)
    try:
        assert barrier.read()["replaces_cli"] is False
    finally:
        barrier.lower("w" * 32)


def test_a_cli_start_gives_up_busy_and_the_update_s_own_children_pass(service_home, monkeypatch):
    from probe import _entry
    from probe.daemon import worker

    token = "u" * 32
    barrier.raise_barrier(token)
    monkeypatch.setattr(barrier, "WAIT_S", 0.2)
    monkeypatch.setattr(_entry, "IN_PLACE_WAIT_S", 0.2)
    try:
        assert _entry._update_barrier(["log", "loss", "0.1"]) == barrier.BUSY_EXIT_CODE == 75
        assert _entry._update_barrier(["daemon", "worker", "--session-id", "s"]) == barrier.WORKER_BUSY_EXIT_CODE
        assert barrier.WORKER_BUSY_EXIT_CODE == worker.EXIT_RESPAWN_LATER
        argv = ["--session-id", "s", "--transcript", "/nonexistent", "--cwd", "/"]
        assert worker.main(argv) == worker.EXIT_RESPAWN_LATER
        monkeypatch.setenv(barrier.TOKEN_ENV, token)
        assert _entry._update_barrier(["--version"]) is None
    finally:
        barrier.lower(token)
    assert _entry._update_barrier(["--version"]) is None


def test_a_busy_cli_start_imports_nothing_of_the_cli(service_home):
    """The barrier is checked BEFORE `probe.cli` is imported (R2): a start the
    barrier turns away has loaded nothing from the files being replaced."""
    script = (
        "import sys; from probe.service import barrier; barrier.raise_barrier('t' * 32); "
        "from probe import _entry; barrier.WAIT_S = 0.2; _entry.IN_PLACE_WAIT_S = 0.2; rc = _entry.main(['log', 'loss', '1']); "
        "print(rc, any(m == 'probe.cli' or m.startswith('probe.cli.') for m in sys.modules))"
    )
    out = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=60)
    assert out.stdout.split() == ["75", "False"], out.stderr


def test_a_stale_barrier_stops_nothing(service_home):
    dead = subprocess.Popen([sys.executable, "-c", "pass"])
    dead.wait()
    paths.barrier_path().write_text(
        json.dumps({"pid": dead.pid, "start_time": "1", "token": "x", "created_at": time.time()})
    )
    assert barrier.wait(0.0) is True
    paths.barrier_path().write_text(
        json.dumps({"pid": os.getpid(), "start_time": "1", "token": "x", "created_at": time.time() - 3600})
    )
    assert barrier.wait(0.0) is True


def test_a_service_stopped_mid_update_leaves_the_barrier_to_the_update(service_home, machine):
    """A service stopped while its update child runs (a signal, the end of its
    10-minute hold) must not take the barrier down with it: `uv tool upgrade`
    is still replacing the CLI's env. The barrier names the child once it
    runs, so it stops CLI starts exactly as long as the child does."""
    gate = service_home.home / "update-may-finish"
    machine.plan("update", steps=[{"wait": str(gate)}])
    status = service_home.start()
    with service_home.connect() as conn:
        assert _check_now(conn)["outcome"] == "started"
    assert wait_for(lambda: machine.calls("update"), 10.0)
    (update,) = machine.calls("update")
    assert wait_for(lambda: (barrier.read() or {}).get("pid") == update["pid"], 5.0), barrier.read()
    os.kill(status["pid"], signal.SIGTERM)
    assert service_home.wait_exit(status["pid"], 5.0), service_home.log()
    try:
        assert pid_running(update["pid"]), "the service's exit killed its update child"
        assert barrier.wait(0.0) is False, "the barrier went down with the service while the update ran"
    finally:
        gate.touch()
    assert wait_for(lambda: not pid_running(update["pid"]), 10.0)
    assert barrier.wait(0.0) is True


# -- lifetime and self ---------------------------------------------------------


@pytest.mark.heavy
def test_a_cycle_holds_the_service_alive(service_home, machine, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "1")
    slow = service_home.home / "update-may-finish"
    machine.plan("update", steps=[{"wait": str(slow)}])
    status = service_home.start()
    with service_home.connect() as conn:
        assert _check_now(conn)["outcome"] == "started"
    wait_for(lambda: machine.calls("update"), 10.0)
    time.sleep(2.0)  # twice the grace, with no session and no app window
    assert pid_running(status["pid"]), service_home.log()
    slow.touch()
    assert service_home.wait_exit(status["pid"], 10.0), service_home.log()
    assert "stopping (idle)" in service_home.log()


def test_a_cycle_holds_the_service_while_its_update_child_runs_and_then_hold_s_again(monkeypatch):
    """Plan fool-proof-updates B2 (R4): a cycle the keeper asked for has no
    session to keep the service up, and its update child may run up to its time
    limit (30 min), well past HOLD_S (10 min). It is held while that child
    runs, hard-capped at the child's own limit and stop grace (past which the
    child is killed), then HOLD_S for the rest of the cycle."""
    import asyncio

    from probe.service import children

    u = updater.Updater(version="1.0.0", emit=lambda topic, payload: None, changed=lambda: None,
                        stop=lambda reason: None, action_running=lambda: False, discovering=lambda: False)
    monkeypatch.setattr(updater, "BARRIER_SETTLE_S", 0)
    left: dict = {}

    class Child:
        pid = os.getpid()

        def poll(self):
            return None

    async def run_events(action, request, *, on_start, **_kw):
        on_start(Child())
        left["child"] = u.hold_until - time.monotonic()
        return 0

    async def quiet():
        return updater.Busy()

    monkeypatch.setattr(children, "run_events", run_events)

    async def cycle():
        u._loop = asyncio.get_running_loop()
        u._look_off_loop = quiet
        u._hold(updater.HOLD_S)
        left["start"] = u.hold_until - time.monotonic()
        await u._apply("c0ffee", "keeper", "token", [], {}, False, False)
        left["rest"] = u.hold_until - time.monotonic()
        u.close()

    asyncio.run(cycle())
    cap = u.update_timeout_s + u.update_stop_grace_s
    assert updater.HOLD_S - 5 < left["start"] <= updater.HOLD_S
    assert cap - 5 < left["child"] <= cap and cap > updater.HOLD_S, "held for as long as the child may run"
    assert updater.HOLD_S - 5 < left["rest"] <= updater.HOLD_S, "then HOLD_S again, not the child's cap"


def test_a_new_cli_version_restarts_the_service_after_the_cycle(service_home, machine):
    machine.plan("version", stdout={"cli_version": "9.9.9"})
    first = service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        _check_now(conn)
        seen = events_until(conn, lambda e: e["topic"] == "service.stopping", 20.0)
    topics = [e["topic"] for e in seen]
    assert topics.index("update.done") < topics.index("service.stopping")
    assert seen[-1] == {"topic": "service.stopping", "reason": "update"}
    done = next(e for e in seen if e["topic"] == "update.done")
    assert done["restart"] is True and done["steps"]["self"]["to_version"] == "9.9.9"
    assert service_home.wait_exit(first["pid"], 5.0)
    second = service_home.start()  # the next ensure starts the new code
    assert second["pid"] != first["pid"]
    assert second["update"]["last_result"]["restart"] is True
    assert machine.calls("update").__len__() == 1  # just checked: no second cycle


def test_a_restart_for_a_new_cli_waits_for_a_running_action(service_home, machine):
    """The update lets go of the mutating slot after its first step, so an
    action can start while the later steps run. A new CLI then restarts the
    service -- after that action, never under it (it would read as stopped)."""
    version_read = service_home.home / "version-may-answer"
    machine.plan("version", stdout={"cli_version": "9.9.9"}, before=[{"wait": str(version_read)}])
    gate = service_home.home / "action-may-finish"
    machine.plan("logout", steps=[{"wait": str(gate)}])
    first = service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        _check_now(conn)
        events_until(conn, lambda e: e["topic"] == "update.step" and e.get("step") == "app", 20.0)
        body = {"action": "logout", "params": {}, "client_request_id": "mid"}
        action_id = conn.call(Method.ACTION_RUN, body)["action_id"]
        version_read.touch()  # the self step reads the new version only now
        done = events_until(conn, lambda e: e["topic"] == "update.done", 20.0)[-1]
        assert done["restart"] is True
        time.sleep(1.0)
        assert pid_running(first["pid"]), service_home.log()
        with pytest.raises(client.ServiceError) as busy:
            conn.call(Method.ACTION_RUN, {**body, "client_request_id": "next"})
        assert busy.value.code == -32010
        gate.touch()
        stopping = events_until(conn, lambda e: e["topic"] == "service.stopping", 10.0)[-1]
        assert stopping == {"topic": "service.stopping", "reason": "update"}
    assert service_home.wait_exit(first["pid"], 5.0)
    service_home.start()
    with service_home.connect() as conn:
        status = conn.call(Method.ACTION_STATUS, {"action_id": action_id})
    assert status["state"] == "done" and status["done"]["ok"] is True, status


def test_actions_queued_behind_an_update_run_in_order_before_its_restart(service_home, machine):
    """Settings changed while a cycle installs a new CLI wait in line, run in
    the order they were asked for once the update step lets go, and the restart
    onto the new CLI comes after the last of them: none is lost to it."""
    machine.plan("version", stdout={"cli_version": "9.9.9"})
    slow = service_home.home / "update-may-finish"
    machine.plan("update", steps=[{"wait": str(slow)}])
    # The last one still runs when the cycle ends: the restart must wait for it.
    last = service_home.home / "last-may-finish"
    machine.plan("workspace_limit", steps=[{"wait": str(last)}])
    first = service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": [*UPDATE_TOPICS, "action.done"]})
        _check_now(conn)
        wait_for(lambda: machine.calls("update"), 10.0)
        asked = [
            ("session_default", {"state": "read"}, "default"),
            ("recorder", {"who_records": "daemon"}, "recorder"),
            ("workspace_limit", {"workspace": None}, "limit"),
        ]
        ids = []
        for action, params, crid in asked:
            answer = conn.call(Method.ACTION_RUN, {"action": action, "params": params, "client_request_id": crid})
            assert answer.get("queued") is True, answer
            ids.append(answer["action_id"])
        assert conn.call(Method.STATUS)["actions"]["queued"] == ids
        slow.touch()
        seen = events_until(conn, lambda e: e["topic"] == "update.done", 30.0)
        last.touch()
        seen += events_until(conn, lambda e: e["topic"] == "service.stopping", 30.0)
    done = [e["action_id"] for e in seen if e["topic"] == "action.done"]
    assert done == ids, service_home.log()
    assert seen[-1] == {"topic": "service.stopping", "reason": "update"}
    update_done = next(e for e in seen if e["topic"] == "update.done")
    assert update_done["restart"] is True
    ran = [call["action"] for call in machine.calls() if call["action"] in {a for a, _p, _c in asked}]
    assert ran == [action for action, _p, _c in asked]
    assert "restarting once the running and queued actions end" in service_home.log()
    assert service_home.wait_exit(first["pid"], 5.0)
    service_home.start()
    with service_home.connect() as conn:
        statuses = [conn.call(Method.ACTION_STATUS, {"action_id": i}) for i in ids]
    assert [(s["state"], s["done"]["ok"]) for s in statuses] == [("done", True)] * 3, statuses


def test_a_setting_waits_for_a_person_s_update_action(service_home, machine):
    """The app's Update runs as an action and holds the slot as a cycle does: a
    setting changed meanwhile waits for it, then runs."""
    gate = service_home.home / "update-may-finish"
    machine.plan("update", steps=[{"wait": str(gate)}])
    service_home.start()
    with service_home.connect() as conn:
        update = conn.call(Method.ACTION_RUN, {"action": "update", "params": {}, "client_request_id": "button"})
        wait_for(lambda: machine.calls("update"), 10.0)
        answer = conn.call(
            Method.ACTION_RUN, {"action": "session_default", "params": {"state": "on"}, "client_request_id": "on"}
        )
        assert answer == {"action_id": answer["action_id"], "queued": True}
        released = time.time()
        gate.touch()
        assert wait_for(
            lambda: conn.call(Method.ACTION_STATUS, {"action_id": answer["action_id"]})["state"] == "done", 20.0
        ), service_home.log()
        statuses = [conn.call(Method.ACTION_STATUS, {"action_id": i}) for i in (update["action_id"], answer["action_id"])]
    assert [s["done"]["ok"] for s in statuses] == [True, True], statuses
    (setting,) = machine.calls("session_default")
    assert setting["at"] >= released and json.loads(setting["stdin"]) == {"state": "on"}


def test_a_person_s_update_action_that_installs_a_new_cli_restarts_the_service(service_home, machine):
    """The app's Update runs as an action, outside a cycle: when it moved the
    CLI, this service is old code, and restarts as a cycle's self step would."""
    machine.plan("version", stdout={"cli_version": "9.9.9"})
    first = service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": ["action.done", "service.stopping"]})
        conn.call(Method.ACTION_RUN, {"action": "update", "params": {}, "client_request_id": "button"})
        seen = events_until(conn, lambda e: e["topic"] == "service.stopping", 20.0)
    assert [e["topic"] for e in seen] == ["action.done", "service.stopping"]
    assert seen[-1]["reason"] == "update"
    assert service_home.wait_exit(first["pid"], 5.0)
    assert len(machine.calls("version")) == 1


def test_a_cycle_makes_the_next_status_fresh(service_home, machine):
    """An update changes every version `probe status` reports."""
    machine.plan("status", stdout={"cli": {"version": "x"}})
    service_home.start()
    with service_home.connect() as conn:
        conn.sock.settimeout(60)
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        conn.call(Method.STATUS_GET)
        conn.call(Method.STATUS_GET)
        assert len(machine.calls("status")) == 1
        _check_now(conn)
        _done(conn)
        conn.call(Method.STATUS_GET)
    assert len(machine.calls("status")) == 2


# -- the desktop app: the service decides, the app's own updater acts ---------------
#
# The service never launches the app (no `open`, no hidden copy): an open app
# that takes `app.check` is handed its check, a closed one is checked at its
# next launch, and the app's launch check is answered `app: {due, reason}`.

#: The topics the desktop app's link takes (`app.check` only reaches a hello `app`).
APP_TOPICS = ["app.check", *UPDATE_TOPICS]


def _app_window(service_home, *, topics=APP_TOPICS):
    """The desktop app's link to the service, as an open app keeps it."""
    conn = service_home.connect(who=Client.APP, keepalive=True)
    conn.call(Method.EVENTS_SUBSCRIBE, {"topics": topics})
    return conn


def _launch_check(conn, **app) -> dict:
    return conn.call(Method.UPDATE_CHECK_NOW, {"trigger": "app", "app": {"version": "0.1.3", **app}})


def _report(conn, result: str, **extra) -> dict:
    after = "0.1.4" if result in ("updated", "ready") else "0.1.3"
    params = {"result": result, "version_before": "0.1.3", "version_after": after, **extra}
    return conn.call(Method.UPDATE_APP_RESULT, params)


def _app_step(seen: list, state: str | None = None) -> dict:
    steps = [e for e in seen if e["topic"] == "update.step" and e.get("step") == "app"]
    steps = [e for e in steps if state is None or e.get("state") == state]
    assert steps, seen
    return steps[-1]


def _drain(conn, quiet: float = 0.5) -> list:
    """Every event `conn` has waiting, until none comes for `quiet` seconds."""
    seen = []
    while (event := conn.next_event(quiet)) is not None:
        seen.append(event)
    return seen


def _quiet(service_home) -> dict:
    status = wait_for(lambda: (s := service_home.call(Method.UPDATE_STATUS)) and not s["in_progress"] and s, 10.0)
    assert status, service_home.log()
    return status


def _restart(service_home, *, last_check_hours_ago: float | None) -> None:
    """Stop the service, move its last cycle back (the rest of its record as
    it is) and start it again, so the next check runs a cycle."""
    pid = _quiet(service_home) and service_home.status()["pid"]
    service_home.call(Method.STOP)
    assert service_home.wait_exit(pid, 10.0), service_home.log()
    if last_check_hours_ago is not None:
        record = json.loads(paths.update_state_path().read_text(encoding="utf-8"))
        record["last_check"] = time.time() - last_check_hours_ago * 3600
        paths.update_state_path().write_text(json.dumps(record), encoding="utf-8")
    service_home.start()


def _next_cycle(service_home, previous: str | None) -> dict:
    """`update.status` once a cycle after `previous` is done, whatever started it."""
    with service_home.connect() as conn:
        assert _check_now(conn)["outcome"] in ("started", "running", "scheduled", "recent")

    def finished():
        status = service_home.call(Method.UPDATE_STATUS)
        last = status.get("last_result") or {}
        return status if last.get("cycle_id") not in (None, previous) and not status["in_progress"] else None

    status = wait_for(finished, 20.0)
    assert status, service_home.log()
    return status


@no_real_app
@closed_app_skips
@pytest.mark.parametrize(
    ("machine_has", "outcome"),
    [
        ("an app, closed", {"state": "skipped", "outcome": "app_closed", "version": "0.1.3"}),
        ("an app never opened", {"state": "skipped", "outcome": "app_closed", "version": "0.1.3"}),
        ("no app", {"state": "skipped", "outcome": "not_installed"}),
        ("an older app, open", {"state": "skipped", "outcome": "app_not_listening"}),
        ("an app, open", {"state": "delegated", "outcome": "app_check_sent"}),
    ],
)
def test_no_cycle_ever_launches_the_app(service_home, machine, machine_has, outcome):
    """Whatever the machine has, the app step starts no process: the open app
    is handed its check, anything else waits for the app's next launch."""
    if machine_has != "no app":
        fake_app(service_home.home, quarantined=machine_has == "an app never opened")
    service_home.start()
    window = None
    if machine_has == "an older app, open":
        window = _app_window(service_home, topics=UPDATE_TOPICS)  # an older build takes no app.check
    elif machine_has == "an app, open":
        window = _app_window(service_home)
    try:
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            assert _check_now(conn)["outcome"] == "started"
            done = _done(conn)[-1]
            status = conn.call(Method.UPDATE_STATUS)
    finally:
        if window is not None:
            window.close()
    assert open_calls(service_home.home) == []
    step = {k: v for k, v in done["steps"]["app"].items() if k != "delegated_at"}
    assert step == outcome
    assert done["ok"] is True
    if outcome["state"] == "skipped":
        # Nothing was handed over: the app's next launch is due.
        assert status["app"]["due"] is True and status["app"]["last_check"] is None
    else:
        assert status["app"]["reason"] == "in_progress" and status["app"]["last_check"] > time.time() - 60


@no_real_app
@closed_app_skips
def test_an_app_open_then_closed_is_not_launched_by_the_next_cycle(service_home, machine):
    """The bug this replaced: while the app ran the app step recorded no
    check, so the first cycle after the app closed launched a hidden copy
    of it (`open -g ... --background-update`: a Dock icon for seconds and
    "Stop Running in Background"). An app open (here an older build, which
    takes no `app.check`) and then closed: the next cycle starts nothing,
    and the app's next launch is due."""
    app = fake_app(service_home.home)
    service_home.start()
    executable = app / "Contents" / "MacOS" / "Probe"
    process = subprocess.Popen([str(executable), "60"], executable=shutil.which("sleep"))  # the app runs
    try:
        with _app_window(service_home, topics=UPDATE_TOPICS):
            first = _next_cycle(service_home, None)["last_result"]
    finally:
        process.kill()
        process.wait()
    # Closed now: the next cycle.
    _restart(service_home, last_check_hours_ago=7)
    second = _next_cycle(service_home, first["cycle_id"])
    assert open_calls(service_home.home) == []
    assert first["steps"]["app"] == {"state": "skipped", "outcome": "app_not_listening"}
    assert second["last_result"]["steps"]["app"]["outcome"] == "app_closed"
    assert second["app"]["due"] is True and second["app"]["reason"] == "never_checked"


@no_real_app
def test_an_open_app_is_sent_app_check_and_its_result_is_the_app_step(service_home, machine):
    fake_app(service_home.home)
    service_home.start()
    with _app_window(service_home) as app, service_home.connect() as cli:
        # A connection that is not the app's never gets `app.check`, subscribed or not.
        cli.call(Method.EVENTS_SUBSCRIBE, {"topics": APP_TOPICS})
        started = _check_now(cli)
        assert started["outcome"] == "started"
        seen = events_until(app, lambda e: e["topic"] == "update.done", 20.0)
        cli_seen = events_until(cli, lambda e: e["topic"] == "update.done", 20.0)
        assert [e for e in seen if e["topic"] == "app.check"] == [
            {"topic": "app.check", "cycle_id": started["cycle_id"]}
        ]
        delegated = _app_step(seen)
        assert delegated["state"] == "delegated" and delegated["outcome"] == "app_check_sent"
        assert seen[-1]["steps"]["app"]["state"] == "delegated"
        status = cli.call(Method.UPDATE_STATUS)["app"]
        assert status["due"] is False and status["reason"] == "in_progress" and status["listening"] == 1
        last = status["last"]
        assert last["state"] == "delegated" and last["cycle_id"] == started["cycle_id"] and last["via"] == "app.check"
        assert last["trigger"] == "cli" and status["last_check"] == last["delegated_at"]
        # The app's own updater installed 0.1.4 (it runs after a restart):
        answer = _report(app, "updated", cycle_id=started["cycle_id"])
        assert answer["recorded"] is True
        assert answer["app"]["due"] is False and answer["app"]["reason"] == "checked_recently"
        assert answer["app"]["last"]["state"] == "done" and answer["app"]["last"]["result"] == "updated"
        step = _app_step(events_until(app, lambda e: e["topic"] == "update.step" and e.get("step") == "app", 5.0))
        assert step == {
            "topic": "update.step",
            "cycle_id": started["cycle_id"],
            "step": "app",
            "state": "done",
            "outcome": "updated",
            "version_before": "0.1.3",
            "version_after": "0.1.4",
            "delegated_at": last["delegated_at"],
        }
        cli_seen += events_until(cli, lambda e: e["topic"] == "update.step" and e.get("step") == "app", 5.0)
        assert not [e for e in cli_seen if e["topic"] == "app.check"]
        # The cycle's record says what the app did.
        result = cli.call(Method.UPDATE_STATUS)["last_result"]
        assert result["cycle_id"] == started["cycle_id"] and result["ok"] is True
        assert result["steps"]["app"]["state"] == "done" and result["steps"]["app"]["outcome"] == "updated"
        # Not a report: refused, nothing recorded.
        for bad in ({}, {"result": "installed"}, {"result": "updated", "version_after": 5}, {"result": "failed", "error": 1}):
            with pytest.raises(client.ServiceError) as raised:
                app.call(Method.UPDATE_APP_RESULT, bad)
            assert raised.value.code == -32602, bad
    assert open_calls(service_home.home) == []


def _on_disk() -> dict:
    """The updater's state file, as written (not what the service holds in memory)."""
    return json.loads(paths.update_state_path().read_text(encoding="utf-8"))


def test_the_app_s_launch_check_is_answered_due_or_not(service_home, machine):
    """`update.check_now {trigger: app, app: {version}}` runs the cycle as
    ever and answers the app's own check in `app`: due, it is the app's now,
    written to the state file before the answer, kept across a restart, and
    no `app.check` follows; the app's report is that cycle's app step."""
    version_read = service_home.home / "version-may-answer"
    machine.plan("version", stdout={"cli_version": probe.__version__}, before=[{"wait": str(version_read)}])
    service_home.start()
    with _app_window(service_home) as app:
        first = _launch_check(app)
        assert first["outcome"] == "started"
        assert first["app"] == {"due": True, "reason": "never_checked", "cycle_id": first["cycle_id"]}
        # On disk by the time the answer came, while the cycle still runs.
        on_disk = _on_disk()
        assert app.call(Method.UPDATE_STATUS)["in_progress"] is True
        assert on_disk["app"]["state"] == "delegated" and on_disk["app"]["cycle_id"] == first["cycle_id"]
        assert on_disk["app"]["via"] == "update.check_now" and on_disk["app"]["version"] == "0.1.3"
        assert on_disk["app"]["trigger"] == "app" and on_disk["app"]["owner"] is None
        assert on_disk["last_app_check"] == on_disk["app"]["delegated_at"]
        status = app.call(Method.UPDATE_STATUS)["app"]
        assert status["due"] is False and status["reason"] == "in_progress"
        seen = events_until(app, lambda e: e["topic"] == "update.step" and e.get("step") == "app", 20.0)
        assert _app_step(seen)["state"] == "delegated" and _app_step(seen)["outcome"] == "already_delegated"
        version_read.touch()
        seen += events_until(app, lambda e: e["topic"] == "update.done", 20.0)
        assert not [e for e in seen if e["topic"] == "app.check"]
        assert seen[-1]["steps"]["app"]["state"] == "delegated"
    # A restart while the app still checks: the check is still the app's.
    _restart(service_home, last_check_hours_ago=None)
    assert _on_disk()["app"] == on_disk["app"]
    with _app_window(service_home) as app:
        status = app.call(Method.UPDATE_STATUS)
        assert status["app"]["reason"] == "in_progress" and status["app"]["last"] == on_disk["app"]
        assert _report(app, "current", cycle_id=first["cycle_id"])["recorded"] is True
        status = app.call(Method.UPDATE_STATUS)
        assert status["last_result"]["steps"]["app"]["state"] == "done"
        assert status["last_result"]["steps"]["app"]["outcome"] == "current"
        assert _on_disk()["app"]["result"] == "current"
        # Checked: another launch within CHECK_EVERY_S is not due ...
        again = _launch_check(app)
        assert again["outcome"] == "recent"
        assert again["app"] == {"due": False, "reason": "checked_recently", "cycle_id": None}
        # ... unless forced (a person's "Check for updates") ...
        assert _launch_check(app, force=True)["app"] == {"due": True, "reason": "forced", "cycle_id": None}
        _report(app, "failed", error="the update server could not be reached")
        # ... or the last one failed: due again at the next launch.
        assert _launch_check(app)["app"] == {"due": True, "reason": "last_failed", "cycle_id": None}
        _report(app, "current")
        assert app.call(Method.UPDATE_STATUS)["app"]["reason"] == "checked_recently"
        # Automatic updates off: never due on its own.
        enable_auto_update(service_home.home, False)
        off = _launch_check(app)
        assert off["outcome"] == "deferred"
        assert off["app"] == {"due": False, "reason": "auto_update_off", "cycle_id": None}
        enable_auto_update(service_home.home, True)
        # An older app sends no `app` and gets none; only the app's trigger takes one.
        assert "app" not in app.call(Method.UPDATE_CHECK_NOW, {"trigger": "app"})
        for bad in (
            {"trigger": "cli", "app": {"version": "0.1.3"}},
            {"trigger": "app", "app": "0.1.3"},
            {"trigger": "app", "app": {"force": "yes"}},
            {"trigger": "app", "app": {"version": 3}},
        ):
            with pytest.raises(client.ServiceError) as raised:
                app.call(Method.UPDATE_CHECK_NOW, bad)
            assert raised.value.code == -32602, bad
    assert open_calls(service_home.home) == []


@no_real_app
def test_app_check_goes_to_the_newest_app_only_and_its_close_fails_the_check(service_home, machine):
    """Two app connections that take `app.check` (an app relaunched before
    its old link closed, say): one hand-off reaches one of them, the newest,
    which owns it. Closed before it reports, the check is failed and due again."""
    service_home.start()
    older = _app_window(service_home)
    newer = _app_window(service_home)
    try:
        with service_home.connect() as cli:
            cli.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            started = _check_now(cli)
            assert started["outcome"] == "started"
            newer_seen = events_until(newer, lambda e: e["topic"] == "update.done", 20.0)
            older_seen = events_until(older, lambda e: e["topic"] == "update.done", 20.0)
            assert [e for e in newer_seen if e["topic"] == "app.check"] == [
                {"topic": "app.check", "cycle_id": started["cycle_id"]}
            ]
            assert [e for e in older_seen if e["topic"] == "app.check"] == []
            status = cli.call(Method.UPDATE_STATUS)["app"]
            assert status["listening"] == 2 and status["reason"] == "in_progress"
            assert isinstance(status["last"]["owner"], int) and _on_disk()["app"]["owner"] == status["last"]["owner"]
            # The app that has the check quits before it reports.
            newer.close()
            seen = events_until(
                cli, lambda e: e["topic"] == "update.step" and e.get("step") == "app" and e.get("state") == "failed", 5.0
            )
            failed = _app_step(seen, "failed")
            assert failed["cycle_id"] == started["cycle_id"] and failed["owner_gone"] is True
            status = cli.call(Method.UPDATE_STATUS)
            assert status["app"]["due"] is True and status["app"]["reason"] == "last_failed"
            assert status["app"]["last"]["owner_gone"] is True
            assert status["last_result"]["steps"]["app"]["state"] == "failed"
            # The other app's connection closing changes nothing more.
            older.close()
            time.sleep(0.3)
            assert cli.call(Method.UPDATE_STATUS)["app"]["last"] == status["app"]["last"]
    finally:
        older.close()
        newer.close()
    assert open_calls(service_home.home) == []


def test_force_never_hands_over_a_second_check_while_one_is_in_the_app_s_hands(service_home, machine):
    """`force` passes over the interval, never over a check the app has not
    reported yet: one check at a time."""
    service_home.start()
    with _app_window(service_home) as app:
        first = _launch_check(app)
        assert first["app"]["due"] is True
        handed = _on_disk()["app"]
        forced = _launch_check(app, force=True)
        assert forced["app"] == {"due": False, "reason": "in_progress", "cycle_id": None}
        assert _on_disk()["app"] == handed  # the same check, not a second one
        assert _report(app, "current", cycle_id=first["cycle_id"])["recorded"] is True
        # Reported: now force passes over the interval.
        assert _launch_check(app, force=True)["app"]["reason"] == "forced"


def test_a_report_for_an_earlier_check_never_settles_the_current_one(service_home, machine):
    """A report's `cycle_id` names the check it answers: one for an earlier
    check (it arrived late) changes nothing; one with none (an older app
    build) answers the check in the app's hands."""
    service_home.start()
    window = _app_window(service_home)
    with service_home.connect() as cli:
        cli.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        earlier = _check_now(cli)
        events_until(window, lambda e: e["topic"] == "app.check", 20.0)
        _done(cli)
        window.close()  # the app quit mid-check: that check is failed
        events_until(
            cli, lambda e: e["topic"] == "update.step" and e.get("step") == "app" and e.get("state") == "failed", 5.0
        )
    _quiet(service_home)
    with _app_window(service_home) as app:
        # Its next launch is handed a new check (no cycle: one just ran).
        current = _launch_check(app)
        assert current["outcome"] == "recent"
        assert current["app"] == {"due": True, "reason": "last_failed", "cycle_id": None}
        handed = _on_disk()["app"]
        late = _report(app, "updated", cycle_id=earlier["cycle_id"])
        assert late["recorded"] is False and late["reason"] == "stale"
        assert _on_disk()["app"] == handed
        assert app.call(Method.UPDATE_STATUS)["app"]["reason"] == "in_progress"
        settled = _report(app, "current")
        assert settled["recorded"] is True
        assert settled["app"]["last"]["delegated_at"] == handed["delegated_at"]
        assert settled["app"]["last"]["result"] == "current"


def test_a_second_report_of_a_settled_check_changes_nothing(service_home, machine):
    """The app reports twice (a retry after a lost answer, say): the second
    report, the same or not, changes nothing, and the cycle's app step is the
    first report's."""
    version_read = service_home.home / "version-may-answer"
    machine.plan("version", stdout={"cli_version": probe.__version__}, before=[{"wait": str(version_read)}])
    service_home.start()
    with _app_window(service_home) as app:
        first = _launch_check(app)
        events_until(app, lambda e: e["topic"] == "update.step" and e.get("step") == "app", 20.0)
        assert _report(app, "current", cycle_id=first["cycle_id"])["recorded"] is True
        reported = _on_disk()
        for again in (
            {"result": "current", "cycle_id": first["cycle_id"]},
            {"result": "current"},
            {"result": "failed", "error": "offline", "cycle_id": first["cycle_id"]},
        ):
            answer = _report(app, **again)
            assert answer["recorded"] is False and answer["reason"] == "duplicate", again
        assert _on_disk() == reported
        version_read.touch()  # the cycle ends after both reports
        done = events_until(app, lambda e: e["topic"] == "update.done", 20.0)[-1]
        assert done["steps"]["app"]["state"] == "done" and done["steps"]["app"]["outcome"] == "current"
        last = _quiet(service_home)["last_result"]
        assert last["steps"]["app"]["state"] == "done" and last["ok"] is True


@no_real_app
def test_a_ready_update_stops_the_timeout_and_holds_off_a_second_check(service_home, machine, monkeypatch):
    """`ready`: the open app downloaded and verified 0.1.4, which installs
    when it quits. The check's timeout stops, no second check is handed over
    while it waits (the app's own forced check included, and after the app
    quit), and the check stays open for ONE final report."""
    monkeypatch.setenv("PROBE_SERVICE_APP_RESULT_TIMEOUT_S", "2")
    service_home.start()
    window = _app_window(service_home)
    try:
        with service_home.connect() as cli:
            cli.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            started = _check_now(cli)
            events_until(window, lambda e: e["topic"] == "app.check", 20.0)
            _done(cli)
            ready = _report(window, "ready", cycle_id=started["cycle_id"])
            assert ready["recorded"] is True
            assert ready["app"]["due"] is False and ready["app"]["reason"] == "in_progress"
            last = ready["app"]["last"]
            assert last["state"] == "ready" and last["result"] == "ready" and last["version_after"] == "0.1.4"
            assert "reported_at" not in last
            step = _app_step(events_until(
                cli, lambda e: e["topic"] == "update.step" and e.get("step") == "app" and e.get("state") == "ready", 5.0
            ))
            assert step["outcome"] == "ready" and step["version_after"] == "0.1.4"
            assert cli.call(Method.UPDATE_STATUS)["last_result"]["steps"]["app"]["state"] == "ready"
            time.sleep(2.5)  # past the 2 s timeout: still ready, never failed
            assert _on_disk()["app"]["state"] == "ready"
            # The open app's own "Check for updates" while it waits: no second check.
            assert _launch_check(window, force=True)["app"] == {"due": False, "reason": "in_progress", "cycle_id": None}
            assert _on_disk()["app"]["state"] == "ready"
            for again in ("ready", "current"):
                answer = _report(window, again, cycle_id=started["cycle_id"])
                assert answer["recorded"] is False and answer["reason"] == "duplicate", again
    finally:
        window.close()
    # The app quit to install it: the check stays ready.
    assert wait_for(lambda: service_home.call(Method.UPDATE_STATUS)["app"]["listening"] == 0, 5.0)
    assert _on_disk()["app"]["state"] == "ready"
    # A later cycle hands nothing over while the update waits, the app open or not.
    _restart(service_home, last_check_hours_ago=7)
    with _app_window(service_home) as app:
        status = _next_cycle(service_home, started["cycle_id"])
        assert status["last_result"]["steps"]["app"] == {
            "state": "skipped", "outcome": "ready_waiting", "version_after": "0.1.4"
        }
        assert not [e for e in _drain(app) if e["topic"] == "app.check"]
        # The one final report closes it, and is not a duplicate.
        final = _report(app, "updated", cycle_id=started["cycle_id"])
        assert final["recorded"] is True
        last = final["app"]["last"]
        assert last["state"] == "done" and last["result"] == "updated" and last["version_after"] == "0.1.4"
        assert last["reported_at"] is not None
        assert _report(app, "updated", cycle_id=started["cycle_id"])["reason"] == "duplicate"
    assert open_calls(service_home.home) == []


@no_real_app
@pytest.mark.parametrize(
    ("launched", "answer", "state", "result"),
    [
        ("0.1.4", {"due": False, "reason": "checked_recently"}, "done", "updated"),  # it installed at the quit
        ("0.1.3", {"due": True, "reason": "last_failed"}, "failed", "failed"),  # it did not: due again
    ],
)
def test_the_next_launch_settles_a_waiting_update_by_the_version_it_runs(
    service_home, machine, launched, answer, state, result
):
    """A `ready` update whose app quit before it said more: the app's next
    launch check settles it by the version that launch runs."""
    service_home.start()
    window = _app_window(service_home)
    with service_home.connect() as cli:
        started = _check_now(cli)
        events_until(window, lambda e: e["topic"] == "app.check", 20.0)
        assert _report(window, "ready", cycle_id=started["cycle_id"])["recorded"] is True
    _quiet(service_home)
    window.close()  # the app quits to install it
    assert wait_for(lambda: service_home.call(Method.UPDATE_STATUS)["app"]["listening"] == 0, 5.0)
    assert _on_disk()["app"]["state"] == "ready"
    with _app_window(service_home) as app:
        got = _launch_check(app, version=launched)
        assert {k: got["app"][k] for k in ("due", "reason")} == answer
        seen = events_until(
            app, lambda e: e["topic"] == "update.step" and e.get("step") == "app" and e.get("state") == state, 5.0
        )
        settled = _app_step(seen, state)
        assert settled["cycle_id"] == started["cycle_id"] and settled["outcome"] == result
        last = app.call(Method.UPDATE_STATUS)["app"]["last"]
        if result == "updated":
            assert last["state"] == "done" and last["version_after"] == "0.1.4" and last["settled_at_launch"] is True
        else:
            # Due again: this launch is handed a new check.
            assert last["state"] == "delegated" and last["via"] == "update.check_now"
    assert open_calls(service_home.home) == []


#: The app step the service before this one recorded, by its outcome.
_OLD_STEP_STATE = {"updated": "done", "current": "done", "failed": "failed", "timeout": "failed"}


@pytest.mark.parametrize(
    ("old_outcome", "due"),
    [
        ("updated", False),
        ("current", False),
        ("quarantined", True),
        ("not_installed", True),
        ("not_capable", True),
        ("failed", True),
        ("timeout", True),
        ("checked_recently", True),  # the check before that one: its outcome is unknown
    ],
)
def test_a_check_the_older_service_recorded_counts_only_when_the_app_was_found_current(
    service_home, machine, old_outcome, due
):
    """The service before this one wrote `last_app_check` for every launch
    attempt, also for an app it never checked. Only an `updated` or `current`
    one is a recent check; anything else leaves the next launch due."""
    an_hour_ago = time.time() - 3600
    step = {"state": _OLD_STEP_STATE.get(old_outcome, "skipped"), "outcome": old_outcome, "version_before": "0.1.3"}
    paths.update_state_path().write_text(json.dumps({
        "v": 1,
        "last_check": an_hour_ago,
        "last_app_check": an_hour_ago,
        "last_result": {"cycle_id": "c-old", "at": an_hour_ago, "trigger": "schedule", "ok": True, "restart": False,
                        "steps": {"app": step}},
    }), encoding="utf-8")
    service_home.start()
    with _app_window(service_home) as app:
        status = app.call(Method.UPDATE_STATUS)["app"]
        answer = _launch_check(app)
    if due:
        assert status["due"] is True and status["reason"] == "never_checked" and status["last_check"] is None
        assert answer["app"]["due"] is True and answer["app"]["reason"] == "never_checked"
    else:
        assert status["due"] is False and status["reason"] == "checked_recently"
        assert status["last_check"] == an_hour_ago and status["last"]["result"] == old_outcome
        assert answer["app"] == {"due": False, "reason": "checked_recently", "cycle_id": None}


def test_a_delegated_check_that_never_reports_reads_as_failed_and_is_due_again(service_home, machine, monkeypatch):
    """The app crashed mid-check: past APP_RESULT_TIMEOUT_S its delegation is
    failed (an `update.step` like any step's), the next launch is due, and a
    late report still counts."""
    monkeypatch.setenv("PROBE_SERVICE_APP_RESULT_TIMEOUT_S", "1")
    service_home.start()
    with _app_window(service_home) as app:
        first = _launch_check(app)
        assert first["app"]["due"] is True
        seen = events_until(
            app, lambda e: e["topic"] == "update.step" and e.get("step") == "app" and e.get("state") == "failed", 20.0
        )
        failed = _app_step(seen, "failed")
        assert failed["cycle_id"] == first["cycle_id"] and failed["outcome"] == "failed"
        assert failed["timed_out"] is True and failed["error"] == "no result from the app within 1 s"
        status = _quiet(service_home)
        assert status["app"]["due"] is True and status["app"]["reason"] == "last_failed"
        assert status["app"]["last"]["state"] == "failed" and status["app"]["last"]["timed_out"] is True
        assert status["last_result"]["steps"]["app"]["state"] == "failed"
        assert status["last_result"]["ok"] is False
        # The app reports after all: that is the check's result.
        late = _report(app, "current")
        assert late["app"]["reason"] == "checked_recently" and late["app"]["last"]["state"] == "done"
        assert "timed_out" not in late["app"]["last"]
        assert app.call(Method.UPDATE_STATUS)["last_result"]["steps"]["app"]["outcome"] == "current"
    assert open_calls(service_home.home) == []


def test_only_a_caller_that_may_run_work_records_the_app_s_result():
    """`update.app_result` only records, but what it records decides when the
    app checks next: a caller in a sandbox is refused it (WORK), as an error,
    never a quiet success."""
    from probe.service import server

    assert server.METHOD_POLICY[Method.UPDATE_APP_RESULT] == server.Policy.WORK
    assert Method.UPDATE_APP_RESULT not in server.CONFINED_ANSWERS


# -- who asks: the CLI and the plugin hook (Q4) ------------------------------------


def _load_hook():
    path = _ROOT / "plugins" / "probe-research" / "hooks" / "version_check.py"
    spec = importlib.util.spec_from_file_location("_service_switch_version_check", path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(path.parent))
    return module


def _fake_probe(bin_dir: Path, service_exit: int) -> Path:
    bin_dir.mkdir(parents=True, exist_ok=True)
    path = bin_dir / "probe"
    path.write_text(
        f"#!{sys.executable}\n"
        "import json, os, sys\n"
        "with open(os.path.join(os.path.dirname(__file__), 'calls.log'), 'a') as handle:\n"
        "    handle.write(json.dumps(sys.argv[1:]) + '\\n')\n"
        f"sys.exit({service_exit} if sys.argv[1:2] == ['service'] else 0)\n"
    )
    path.chmod(0o755)
    return path


@pytest.mark.parametrize(
    ("service_exit", "calls"),
    [
        (0, [["service", "check-now", "--trigger", "session"]]),
        # A CLI older than the service (usage error), or a service that does
        # not start: the wizard's update, as before the service.
        (2, [["service", "check-now", "--trigger", "session"], ["wizard", "--action", "update", "--yes"]]),
        # Turned away by the update barrier: the service is updating now.
        (75, [["service", "check-now", "--trigger", "session"]]),
    ],
)
def test_the_hook_asks_the_service_and_falls_back_to_the_wizard(tmp_path, monkeypatch, service_exit, calls):
    hook = _load_hook()
    probe_bin = _fake_probe(tmp_path / "bin", service_exit)
    monkeypatch.setattr(hook, "_autoupdate_settings", lambda: {"enabled": True})
    hook._spawn_autoupdate(str(probe_bin))
    log = tmp_path / "bin" / "calls.log"
    assert wait_for(lambda: log.exists() and len(log.read_text().splitlines()) == len(calls), 10.0)
    time.sleep(0.3)
    assert [json.loads(line) for line in log.read_text().splitlines()] == calls


_MANAGED_BIN = ("uv", "tools", "probe-research", "bin")
_PROJECT_BIN = ("project", ".venv", "bin")


@pytest.mark.parametrize(
    ("bin_dir", "here", "default_folder", "asks"),
    [
        # The machine's managed CLI with no choice on record: on.
        (_MANAGED_BIN, None, None, True),
        (_MANAGED_BIN, {"enabled": False}, None, False),
        # Turned off under the default folder (the service's), this session
        # running with XDG_STATE_HOME elsewhere: off all the same.
        (_MANAGED_BIN, None, {"enabled": False}, False),
        # A `probe` in a researcher's own project env: opt-in (plan D4).
        (_PROJECT_BIN, None, None, False),
        (_PROJECT_BIN, {"enabled": True}, None, True),
    ],
    ids=["managed-no-choice", "managed-off", "managed-off-in-default-folder", "project-no-choice",
         "project-opted-in"],
)
def test_the_hook_reads_the_setting_for_the_probe_it_would_update(
    tmp_path, monkeypatch, bin_dir, here, default_folder, asks
):
    """The plugin's SessionStart hook applies the same rule as the CLI
    (`version_policy.autoupdate_state`, plan C2), for the `probe` it runs, and
    writes nothing: the default is never written down (an older hook or CLI
    would read it as a person's opt-in)."""
    for name, sub in (("HOME", "home"), ("XDG_STATE_HOME", "state"), ("XDG_CONFIG_HOME", "config"),
                      ("CLAUDE_CONFIG_DIR", "claude"), ("CODEX_HOME", "codex"), ("PI_CODING_AGENT_DIR", "pi")):
        monkeypatch.setenv(name, str(tmp_path / sub))
    hook = _load_hook()
    probe_bin = _fake_probe(tmp_path.joinpath(*bin_dir), 0)
    records = [tmp_path / "state" / "probe" / "autoupdate.json",
               tmp_path / "home" / ".local" / "state" / "probe" / "autoupdate.json"]
    for record, state in zip(records, (here, default_folder)):
        if state is not None:
            record.parent.mkdir(parents=True)
            record.write_text(json.dumps(state))
    before = [record.read_text() if record.exists() else None for record in records]
    spawned: list = []
    monkeypatch.setattr(hook.subprocess, "Popen", lambda argv, **_kw: spawned.append(argv))
    hook._spawn_autoupdate(str(probe_bin))
    assert bool(spawned) is asks
    assert [record.read_text() if record.exists() else None for record in records] == before


def test_the_service_reads_an_off_saved_in_a_live_session_s_state_folder(tmp_path, monkeypatch):
    """The service starts with no XDG_STATE_HOME and reads the default state
    folder. A person who runs with XDG_STATE_HOME may have turned automatic
    updates off there (before `save` wrote both folders): a live session's
    folder (D13) is read too, and that off stands."""
    from probe import version_policy

    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    monkeypatch.setattr(version_policy, "managed_cli", lambda path=None: True)
    session_state = tmp_path / "xdg-state" / "probe"
    assert updater.auto_update_enabled([session_state]) is True
    session_state.mkdir(parents=True)
    (session_state / "autoupdate.json").write_text(json.dumps({"enabled": False}))
    assert updater.auto_update_enabled([session_state]) is False


def test_the_cli_asks_the_service_instead_of_spawning_an_updater(monkeypatch):
    import types

    cli_main = importlib.import_module("probe.cli.main")  # the module (`probe.cli.main` is also a function)
    spawned: list = []
    fake = types.SimpleNamespace(
        Popen=lambda argv, **_kw: spawned.append(("service", argv, None)), DEVNULL=subprocess.DEVNULL
    )
    monkeypatch.setattr(cli_main, "subprocess", fake)
    monkeypatch.setattr(cli_main, "_spawn_detached", lambda argv, env: spawned.append(("detached", argv, env)))
    from probe.service import client as service_client

    monkeypatch.setattr(service_client, "runtime_python", lambda: sys.executable)
    cli_main._spawn_update("--apply-if-newer", trigger="session_start")
    ((how, argv, _env),) = spawned
    assert how == "service"
    assert argv == [
        sys.executable, "-I", "-m", "probe.service.client", "check-now", "--trigger", "session",
        "--wait-for-pid", str(os.getpid()),
    ]
    # An install the service cannot start from (no runtime.json, no uv tool
    # env: pip, pipx) keeps the old updater, or its updates would be dropped.
    spawned.clear()
    monkeypatch.setattr(service_client, "runtime_python", lambda: None)
    cli_main._spawn_update("--apply-if-newer", trigger="session_start")
    assert [how for how, _, _ in spawned] == ["detached"]


def test_check_now_waits_for_the_command_that_asked(service_home, machine):
    """The CLI asks from its root callback, before its own command runs: the
    update must not replace the env under that command (`--wait-for-pid`)."""
    import threading

    asker = subprocess.Popen(["sleep", "1.0"])
    threading.Thread(target=asker.wait, daemon=True).start()  # reaped as it exits, as a shell would
    started = time.monotonic()
    assert client.main(["check-now", "--trigger", "cli", "--wait-for-pid", str(asker.pid)]) == 0
    assert time.monotonic() - started >= 0.9
    assert asker.poll() is not None
    assert wait_for(lambda: machine.calls("update"), 10.0)


def test_check_now_from_the_client_starts_the_service(service_home, machine):
    machine.plan("version", stdout={"cli_version": probe.__version__})
    answer = client.check_now("cli", wait=5.0)
    assert answer["outcome"] in ("started", "running")
    assert wait_for(lambda: machine.calls("update"), 10.0)


def test_the_trigger_is_recorded_as_asked_and_reported_as_the_server_knows_it(service_home, machine):
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        started = _check_now(conn, "app")
        seen = _done(conn)
        status = conn.call(Method.UPDATE_STATUS)
        with pytest.raises(client.ServiceError) as raised:
            _check_now(conn, "session_start")  # a report word, not a check trigger
        assert raised.value.code == -32602
    assert started["outcome"] == "started"
    assert seen[0] == {"topic": "update.started", "cycle_id": started["cycle_id"], "trigger": "app"}
    assert seen[-1]["trigger"] == "app" and status["last_result"]["trigger"] == "app"
    # The update report has no `app` yet: an automatic check, under `cli`.
    assert machine.calls("update")[0]["env"]["PROBE_AUTOUPDATE_TRIGGER"] == "cli"


def test_an_update_child_that_wrote_no_done_failed(service_home, machine):
    machine.plan("update", steps=[{"event": STEP}, {"exit": 0}])  # exits 0 before its `done`
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        _check_now(conn)
        done = _done(conn)[-1]
    assert done["steps"]["cli_and_plugins"]["state"] == "failed" and done["ok"] is False


def test_an_update_that_did_not_complete_failed(service_home, machine):
    """The update child exits 0 and says `complete: false` when a step it ran
    failed or was skipped (a CLI install that left nothing while the plugins
    moved: live test C, 2026-10-24). Read as done, every surface said `(ok)`,
    nothing counted the failure and the next try was six hours off: it is a
    failed step, a cycle not ok, one failure in a row, and a sooner retry."""
    machine.plan("update", steps=[
        {"event": STEP},
        {"event": {"event": "done", "ok": True, "complete": False, "exit_code": 0, "steps": []}},
        {"exit": 0},
    ])
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        _check_now(conn)
        done = _done(conn)[-1]
        status = conn.call(Method.UPDATE_STATUS)
    step = done["steps"]["cli_and_plugins"]
    assert step["state"] == "failed" and step["complete"] is False and done["ok"] is False, step
    saved = json.loads(paths.update_state_path().read_text())
    assert saved["failed_in_a_row"] == 1 and saved["last_result"]["ok"] is False
    assert status["last_result"]["ok"] is False
    assert 0 < status["next_check"] - status["last_check"] < updater.CHECK_EVERY_S


@pytest.mark.parametrize("reachable, streak", [(False, 0), (True, 1), (None, 1)])
def test_an_update_that_failed_offline_is_not_a_failure_in_a_row(service_home, machine, reachable, streak):
    """Offline, `uv tool upgrade` fails every cycle, and three in a row were an
    `update_failed` report about a laptop on a plane. A failed cycle whose
    release manifest got no answer at all does not count; one it answered (or
    an older CLI's read that cannot say) still does."""
    machine.plan("update", steps=[
        {"event": STEP},
        {"event": {"event": "done", "ok": False, "complete": False, "exit_code": 1, "steps": []}},
        {"exit": 1},
    ])
    answer = {"cli_version": probe.__version__, "cli_latest": None}
    if reachable is not None:
        answer["reachable"] = reachable
    machine.plan("version", stdout=answer)
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        _check_now(conn)
        done = _done(conn)[-1]
    assert done["steps"]["cli_and_plugins"]["state"] == "failed" and done["ok"] is False
    saved = json.loads(paths.update_state_path().read_text())
    assert saved["failed_in_a_row"] == streak and saved["last_result"]["ok"] is False
    assert saved["last_result"].get("offline", False) is (reachable is False)


def test_failures_in_a_row_retry_sooner_up_to_the_usual_interval():
    check = updater.Updater(
        version="1", emit=lambda *a: None, changed=lambda: None, stop=lambda r: None,
        action_running=lambda: False, discovering=lambda: False,
    )
    seen = []
    for streak in (0, 1, 2, 3, 4, 10):
        check.state["failed_in_a_row"] = streak
        seen.append(check.interval())
    assert seen == [updater.CHECK_EVERY_S, 3600, 7200, 14400, updater.CHECK_EVERY_S, updater.CHECK_EVERY_S]


# -- an update child past its time limit (UPDATE_TIMEOUT_S) ---------------------------


def _state_dir(service_home) -> Path:
    return service_home.home / ".local" / "state" / "probe"


def _pid_in(path: Path) -> int:
    assert wait_for(lambda: path.exists() and path.read_text().strip(), 10.0), f"{path} never written"
    return int(path.read_text())


#: The update's own command ignores SIGTERM: started ignoring it (inherited),
#: the update itself answering it again after.
_ITS_COMMAND_IGNORES = ([{"ignore": "SIGTERM"}], [{"default": "SIGTERM"}])


@pytest.mark.parametrize(
    ("plan", "grace", "stopped_by", "exit_code"),
    [
        (([], []), None, "SIGTERM", 143),
        (([{"ignore": "SIGTERM"}], []), "1", "SIGKILL", 137),
        (_ITS_COMMAND_IGNORES, "1", "SIGKILL", 143),
    ],
    ids=["answers-sigterm", "ignores-sigterm", "its-command-ignores-sigterm"],
)
def test_an_update_past_the_time_limit_is_stopped_and_the_next_cycle_can_run(
    service_home, machine, monkeypatch, plan, grace, stopped_by, exit_code
):
    """An update child that never returned kept its cycle in progress for good:
    every `update.check_now` answered `running`, and no update ran again. Past
    the limit its process group is stopped (SIGTERM, then SIGKILL past the
    grace to whatever is left of it), the step fails saying why, in the record
    `probe doctor` prints too, and the barrier and the slot are let go."""
    monkeypatch.setenv("PROBE_SERVICE_UPDATE_TIMEOUT_S", "1")
    if grace:
        monkeypatch.setenv("PROBE_SERVICE_UPDATE_STOP_GRACE_S", grace)
    command = service_home.home / "command.pid"
    before_spawn, after_spawn = plan
    machine.plan("update", steps=[
        *before_spawn,
        {"event": STEP},
        {"lock": str(_state_dir(service_home) / "wizard.lock")},
        {"spawn": ["sleep", "60"], "pidfile": str(command)},
        *after_spawn,
        {"wait": str(service_home.home / "never")},
    ])
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        assert _check_now(conn)["outcome"] == "started"
        done = _done(conn, timeout=15.0)[-1]
        status = conn.call(Method.UPDATE_STATUS)
        again = _check_now(conn)
    step = done["steps"]["cli_and_plugins"]
    assert step["state"] == "failed" and done["ok"] is False, step
    assert step["detail"] == "the update ran past 1 s and was stopped"
    assert (step["stopped_by"], step["exit_code"]) == (stopped_by, exit_code)
    (child,) = machine.calls("update")
    assert not pid_running(child["pid"])
    assert wait_for(lambda: not pid_running(_pid_in(command)), 5.0), "the command the update ran outlived the stop"
    assert status["in_progress"] is False
    assert again["outcome"] != "running", again
    assert barrier.wait(0.0) is True
    attempt = autoupdate_state(service_home.home)["last_attempt"]
    assert (attempt["ok"], attempt["detail"]) == (False, "the update ran past 1 s and was stopped")


def test_the_next_service_stops_an_update_a_service_before_it_left_running_past_the_limit(
    service_home, machine, monkeypatch
):
    """A service stopped under its update leaves the child running (it must
    outlive the service) and the barrier naming it. The next service found its
    `wizard.lock` and deferred, cycle after cycle, for good: a setup is never
    overridden. Past the limit that child -- and only it -- is stopped first."""
    command = service_home.home / "command.pid"
    machine.plan("update", steps=[
        {"lock": str(_state_dir(service_home) / "wizard.lock")},
        {"spawn": ["sleep", "60"], "pidfile": str(command)},
        {"wait": str(service_home.home / "never")},
    ])
    first = service_home.start()
    with service_home.connect() as conn:
        assert _check_now(conn)["outcome"] == "started"
    assert wait_for(lambda: machine.calls("update"), 10.0)
    (old,) = machine.calls("update")
    assert wait_for(lambda: (barrier.read() or {}).get("pid") == old["pid"], 5.0), barrier.read()
    spawned = _pid_in(command)  # written after the lock was taken
    os.kill(first["pid"], signal.SIGTERM)
    assert service_home.wait_exit(first["pid"], 5.0), service_home.log()
    assert pid_running(old["pid"]), "the service's exit killed its update child"

    machine.plan("update", steps=[{"event": STEP}])
    monkeypatch.setenv("PROBE_SERVICE_UPDATE_TIMEOUT_S", "1")
    time.sleep(max(0.0, 1.2 - (time.time() - barrier.read()["created_at"])))
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        assert _check_now(conn)["outcome"] == "started"
        done = _done(conn)[-1]
    assert done["deferred"] is None, done
    step = done["steps"]["cli_and_plugins"]
    assert step["state"] == "done", step
    assert step["stopped_previous"]["pid"] == old["pid"]
    assert step["stopped_previous"]["stopped_by"] == "SIGTERM"
    detail = "the update a service before this one started ran past 1 s and was stopped"
    assert step["stopped_previous"]["detail"] == detail
    assert not pid_running(old["pid"]) and wait_for(lambda: not pid_running(spawned), 5.0)
    assert len(machine.calls("update")) == 2  # and the update ran
    attempt = autoupdate_state(service_home.home)["last_attempt"]
    assert (attempt["ok"], attempt["detail"]) == (False, detail)


#: A `probe wizard` in a terminal, as far as wizard.lock goes: not an update child.
_PERSON_S_WIZARD = r"""
import fcntl, os, sys, time
lock = open(sys.argv[1], "a")
fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
open(sys.argv[2], "w").close()
while os.path.isdir(os.path.dirname(sys.argv[2])):
    time.sleep(0.05)
"""


@pytest.mark.parametrize("holder", ["the-app-s-update-action", "a-reused-pid", "a-person-s-wizard"])
def test_a_wizard_lock_the_barrier_does_not_prove_ours_is_never_overridden(service_home, machine, monkeypatch, holder):
    """Only the update child the barrier names, still that exact process (pid
    and kernel start time) and running `probe.core.run update`, is ever
    stopped. The app's Update action is an update child by its command line but
    raises no barrier; a reused pid has another start time; a person's
    `probe wizard` is not an update child. Each keeps its lock, and the update
    defers as it always did."""
    wizard = _state_dir(service_home) / "wizard.lock"
    ready = service_home.home / "holder-ready"
    if holder == "a-person-s-wizard":
        argv = [sys.executable, "-c", _PERSON_S_WIZARD, str(wizard), str(ready)]
    else:
        machine.plan("update", steps=[
            {"lock": str(wizard)}, {"touch": str(ready)}, {"wait": str(service_home.home / "never")}
        ])
        argv = [str(machine.python), "-I", "-m", "probe.core.run", "update"]
    wizard.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, start_new_session=True)
    try:
        assert wait_for(ready.exists, 10.0)
        if holder != "the-app-s-update-action":
            from probe.service import procid

            start = procid.start_time(proc.pid) if holder == "a-person-s-wizard" else "1"
            paths.barrier_path().write_text(json.dumps(
                {"pid": proc.pid, "start_time": start, "token": "t", "created_at": time.time() - 3600}
            ))
        monkeypatch.setenv("PROBE_SERVICE_UPDATE_TIMEOUT_S", "1")
        time.sleep(1.2)
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            done = _done(conn)[-1]
        assert done["deferred"] == "setup_running", done
        assert "stopped_previous" not in done["steps"]["cli_and_plugins"]
        assert proc.poll() is None, f"{holder} was stopped"
    finally:
        with contextlib.suppress(OSError):
            os.killpg(proc.pid, signal.SIGKILL)
        proc.wait(5)


def test_an_overrun_is_only_past_its_limit_and_never_this_process(service_home):
    """`overrun_update`'s age and self checks (the identity checks run against
    real services above). The age is the barrier's, written as the child
    started; a clock set back reads as not past."""
    sleeper = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)", "-m", "probe.core.run", "update"],
        start_new_session=True,
    )
    try:
        from probe.service import procid

        start = wait_for(lambda: procid.start_time(sleeper.pid), 5.0)

        def named(pid, created_at):
            paths.barrier_path().write_text(json.dumps(
                {"pid": pid, "start_time": procid.start_time(pid), "token": "t", "created_at": created_at}
            ))

        now = time.time()
        assert updater.overrun_update(60.0) is None  # no barrier
        named(sleeper.pid, now - 30)
        assert updater.overrun_update(60.0, now) is None  # not past the limit yet
        named(sleeper.pid, now + 3600)
        assert updater.overrun_update(60.0, now) is None  # the clock went back
        named(os.getpid(), now - 3600)
        assert updater.overrun_update(60.0, now) is None  # this process
        named(sleeper.pid, now - 3600)
        assert updater.overrun_update(60.0, now) == updater.Overrun(sleeper.pid, start, now - 3600)
    finally:
        sleeper.kill()
        sleeper.wait(5)


#: A process group's leader that starts two commands in its group and writes
#: their pids. `ignore`: it and its commands ignore SIGTERM; `kids-ignore`: only
#: its commands do (inherited at their start, so before any signal can come);
#: `note`: it notes a SIGTERM (`<pids>.term`) and runs on.
_GROUP = r"""
import os, signal, subprocess, sys, time
if sys.argv[2] in ("ignore", "kids-ignore"):
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
kids = [subprocess.Popen(["sleep", "60"]) for _ in range(2)]
if sys.argv[2] == "kids-ignore":
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
if sys.argv[2] == "note":
    signal.signal(signal.SIGTERM, lambda *_: open(sys.argv[1] + ".term", "w").close())
with open(sys.argv[1] + ".tmp", "w") as out:
    out.write(" ".join(str(k.pid) for k in kids))
os.replace(sys.argv[1] + ".tmp", sys.argv[1])
time.sleep(60)
"""


def _group(tmp_path, mode: str) -> tuple[subprocess.Popen, int, int]:
    """`_GROUP` as a group leader of its own, reaped by a thread here as soon
    as it exits (as init reaps one whose service is gone): its group then
    holds only what is left of it. With its two commands' pids."""
    import threading

    pids = tmp_path / "pids"
    leader = subprocess.Popen([sys.executable, "-c", _GROUP, str(pids), mode], start_new_session=True)
    _STAND_INS.append(leader)  # its group killed at the test's end, pass or fail
    threading.Thread(target=leader.wait, daemon=True).start()
    assert wait_for(pids.exists, 10.0)
    first, second = (int(p) for p in pids.read_text().split())
    return leader, first, second


@pytest.mark.parametrize(
    ("mode", "expected"),
    [("answer", "SIGTERM"), ("ignore", "SIGKILL"), ("kids-ignore", "SIGKILL"), ("group-member", "SIGTERM")],
)
def test_a_previous_update_is_stopped_with_its_group_and_never_its_neighbours(tmp_path, mode, expected):
    """`stop_process`: an update child of this version leads its own group,
    which is stopped whole (SIGTERM, then SIGKILL past the grace to whatever
    is left of it, a command that ignores SIGTERM included); one an older
    service started shares that service's group with other processes, so only
    it is signalled, never its neighbours."""
    import asyncio

    from probe.service import procid

    leader, first, second = _group(tmp_path, "answer" if mode == "group-member" else mode)
    target = first if mode == "group-member" else leader.pid
    how = asyncio.run(updater.stop_process(target, procid.start_time(target), 1.0))
    assert how == expected
    if mode == "group-member":
        assert wait_for(lambda: not pid_running(first), 5.0)
        assert pid_running(second) and leader.poll() is None, "a neighbour in its group was stopped"
    else:
        assert wait_for(lambda: leader.poll() is not None, 5.0)
        assert wait_for(lambda: not pid_running(first) and not pid_running(second), 5.0), "its commands outlived it"
    assert asyncio.run(updater.stop_process(target, "not-its-start", 1.0)) == updater.Stopped.GONE


@pytest.mark.realtime
def test_a_cancelled_stop_sends_nothing_more(tmp_path):
    """The service stopping while it stops a previous update: once its SIGTERM
    is out, no SIGKILL follows from an abandoned wait (a thread did, before)."""
    import asyncio

    from probe.service import procid

    leader, _, _ = _group(tmp_path, "note")
    noted = tmp_path / "pids.term"

    async def cancel_after_the_sigterm() -> None:
        task = asyncio.ensure_future(updater.stop_process(leader.pid, procid.start_time(leader.pid), 2.0))
        deadline = time.monotonic() + 10.0
        while not noted.exists() and time.monotonic() < deadline:
            await asyncio.sleep(0.02)
        assert noted.exists(), "no SIGTERM reached it"
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(cancel_after_the_sigterm())
    time.sleep(2.5)  # past the grace, where the SIGKILL would have come
    assert leader.poll() is None, "a cancelled stop went on to kill it"


#: In a process that reaps nothing and is its orphans' reaper (Linux's
#: PR_SET_CHILD_SUBREAPER): a group whose leader answers SIGTERM and whose
#: command ignores it, stopped. Both end as zombies nobody reaps.
_UNREAPED = r"""
import asyncio, ctypes, os, subprocess, sys, time
from probe.service import children, procid
ctypes.CDLL(None).prctl(36, 1)  # PR_SET_CHILD_SUBREAPER
ready = sys.argv[1]
leader = subprocess.Popen([sys.executable, "-c", (
    "import signal, subprocess, sys, time\n"
    "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
    "subprocess.Popen(['sleep', '60'])\n"
    "signal.signal(signal.SIGTERM, signal.SIG_DFL)\n"
    "open(sys.argv[1], 'w').close()\n"
    "time.sleep(60)\n"), ready], start_new_session=True)
while not os.path.exists(ready):
    time.sleep(0.02)
start = procid.start_time(leader.pid)
async def there():
    return procid.alive(leader.pid, start) is True
how = asyncio.run(children.stop(leader=there, send=lambda sig: os.killpg(leader.pid, sig), group=leader.pid, grace=1.0))
print(how)
"""


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="PR_SET_CHILD_SUBREAPER is Linux's")
def test_a_stopped_group_left_as_unreaped_zombies_reads_as_stopped(tmp_path):
    """A group whose members are dead but not reaped (a reaper that is slow, or
    none, as in a container without an init) is stopped, not `running`: a
    zombie is gone. The command that ignored SIGTERM took the SIGKILL."""
    done = subprocess.run(
        [sys.executable, "-c", _UNREAPED, str(tmp_path / "ready")], capture_output=True, text=True, timeout=60
    )
    assert done.returncode == 0, done.stderr[-2000:]
    assert done.stdout.split() == [updater.Stopped.SIGKILL]


#: A group leader that, on SIGTERM, starts a command ignoring SIGTERM (its pid
#: to `<path>.late`) and exits at once. `with-anchor`: it also started one such
#: command at its own start, which outlives it.
_SPAWNS_ON_TERM = r"""
import os, signal, subprocess, sys, time
path, mode = sys.argv[1], sys.argv[2]
IGNORING = [sys.executable, "-c", "import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(60)"]
def late(*_):
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    child = subprocess.Popen(IGNORING)
    with open(path + ".late.tmp", "w") as out:
        out.write(str(child.pid))
    os.replace(path + ".late.tmp", path + ".late")
    os._exit(0)
pids = []
if mode == "with-anchor":
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    pids.append(subprocess.Popen(IGNORING).pid)
signal.signal(signal.SIGTERM, late)
with open(path + ".tmp", "w") as out:
    out.write(" ".join(map(str, pids)))
os.replace(path + ".tmp", path)
time.sleep(60)
"""


@pytest.mark.realtime
@pytest.mark.parametrize("mode", ["with-anchor", "alone"])
def test_a_command_started_as_the_group_is_stopped_is_found_or_never_signalled(tmp_path, mode):
    """Once the leader is gone its group's number can name another group, so
    the group is listed and signalled only while a process of it that was
    listed is still there. A command the leader starts on its way out is found
    through one that outlives it (`with-anchor`: killed past the grace), and
    with none left to prove the group is still its own (`alone`) it is never
    signalled: the stop says `running` instead of claiming the group is gone."""
    import asyncio
    import threading

    from probe.service import procid

    path = tmp_path / "pids"
    leader = subprocess.Popen([sys.executable, "-c", _SPAWNS_ON_TERM, str(path), mode], start_new_session=True)
    _STAND_INS.append(leader)
    threading.Thread(target=leader.wait, daemon=True).start()
    assert wait_for(path.exists, 10.0)
    early = [int(p) for p in path.read_text().split()]
    late_pid = None
    try:
        how = asyncio.run(updater.stop_process(leader.pid, procid.start_time(leader.pid), 1.0))
        late_pid = _pid_in(Path(str(path) + ".late"))
        if mode == "with-anchor":
            assert how == updater.Stopped.SIGKILL
            assert wait_for(lambda: not pid_running(late_pid) and not any(pid_running(p) for p in early), 5.0)
        else:
            assert how == updater.Stopped.RUNNING
            assert pid_running(late_pid), "a process nobody could prove to be of its group was signalled"
    finally:
        for pid in [*early, *([late_pid] if late_pid else [])]:
            with contextlib.suppress(OSError):
                os.kill(pid, signal.SIGKILL)


#: A group leader whose command, on SIGTERM, leaves the group (`setsid`, as a
#: daemon the run started on purpose would) and runs on (`<path>.left` once out).
_LEAVES_ON_TERM = r"""
import os, signal, subprocess, sys, time
path = sys.argv[1]
LEAVER = [sys.executable, "-c", (
    "import os, signal, sys, time\n"
    "def leave(*_):\n"
    "    os.setsid()\n"
    "    open(sys.argv[1], 'w').close()\n"
    "signal.signal(signal.SIGTERM, leave)\n"
    "open(sys.argv[1] + '.ready', 'w').close()\n"
    "time.sleep(60)\n"), path + ".left"]
kid = subprocess.Popen(LEAVER)
while not os.path.exists(path + ".left.ready"):
    time.sleep(0.02)
with open(path + ".tmp", "w") as out:
    out.write(str(kid.pid))
os.replace(path + ".tmp", path)
time.sleep(60)
"""


def test_a_process_that_left_the_group_is_neither_its_anchor_nor_signalled(tmp_path):
    """A command that left the group (a daemon the update started on purpose)
    proves nothing about the group's number once the leader is gone: it is
    not waited for, and nothing more is sent its way or to the group."""
    import asyncio
    import threading

    from probe.service import procid

    path = tmp_path / "pids"
    leader = subprocess.Popen([sys.executable, "-c", _LEAVES_ON_TERM, str(path)], start_new_session=True)
    _STAND_INS.append(leader)
    threading.Thread(target=leader.wait, daemon=True).start()
    kid = _pid_in(path)
    try:
        how = asyncio.run(updater.stop_process(leader.pid, procid.start_time(leader.pid), 1.0))
        assert (tmp_path / "pids.left").exists(), "it never left the group"
        assert how == updater.Stopped.SIGTERM  # done once its group was gone, not anchored by the one that left
        assert pid_running(kid), "a process that left the group was killed"
    finally:
        with contextlib.suppress(OSError):
            os.kill(kid, signal.SIGKILL)


def test_this_service_s_child_whose_identity_could_not_be_read_is_never_signalled(tmp_path):
    """`Popen.wait` reaps before it sets `returncode`, so "not reaped yet" is
    proven only by the kernel start time read as the child started. Without
    it nothing is sent (on POSIX), and the stop says the child is still there."""
    import asyncio

    from probe.service import children

    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], start_new_session=True)
    _STAND_INS.append(child)

    async def at_the_limit():
        exited = asyncio.get_running_loop().create_future()
        return await children._stop_overrun(child, exited, 1.0, None)

    overran = asyncio.run(at_the_limit())
    assert overran.how == children.Stopped.RUNNING and overran.code is None
    assert child.poll() is None, "a child with no identity to prove it by was signalled"


def test_the_stopped_update_keeps_what_its_child_recorded_since_it_started(service_home, monkeypatch):
    from probe._shared import autoupdate

    monkeypatch.setenv("XDG_STATE_HOME", str(service_home.home / ".local" / "state"))
    autoupdate.record_attempt(autoupdate.Attempt(at=int(time.time()) - 3600, ok=True, from_version="0.1.0"))
    assert updater.record_stopped("stopped", version="0.2.0", since=time.time() - 60)
    first = autoupdate.load().last_attempt
    assert (first.ok, first.detail, first.from_version) == (False, "stopped", "0.2.0")  # older: replaced

    since = time.time() - 1
    autoupdate.record_attempt(autoupdate.Attempt(
        at=int(time.time()), ok=True, from_version="0.2.0", plugin_ok=False, plugin_detail="codex: x",
    ))
    assert updater.record_stopped("ran past 30 min", version="0.2.0", since=since)
    kept = autoupdate.load().last_attempt
    assert (kept.ok, kept.detail, kept.plugin_ok, kept.plugin_detail) == (False, "ran past 30 min", False, "codex: x")

    # Its lock held (by a child that would not stop, say): skipped, never waited on.
    with _hold(autoupdate.state_dir() / "state.lock"):
        assert updater.record_stopped("later", version="0.2.0", since=since) is False
    assert autoupdate.load().last_attempt.detail == "ran past 30 min"


# -- busy machines still update (plan D7, D12, D13, D33, D11, D14) ------------------

#: A stand-in `probe daemon worker`: holds its session's lock, says it takes
#: requests (the marker the updater reads its pid from), and on SIGTERM leaves
#: at once when its `.handover` marker is fresh, as the real one does at its
#: next model round; without it, it would drain its queue (here: never leaves).
_WORKER = r"""
import fcntl, json, os, signal, sys, time
state, sid, mode = sys.argv[1], sys.argv[2], sys.argv[3]
lock = open(os.path.join(state, "daemon", sid + ".lock"), "a")
fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
marker = os.path.join(state, "reads", "requests", sid)
os.makedirs(marker, exist_ok=True)
with open(os.path.join(marker, ".worker.json"), "w") as f:
    json.dump({"pid": os.getpid(), "requests": 1}, f)
handover = os.path.join(state, "daemon", sid + ".handover")
stopping = {"on": False}
def term(*_):
    stopping["on"] = True
signal.signal(signal.SIGTERM, term)
open(os.path.join(state, sid + ".ready"), "w").close()
while True:
    time.sleep(0.05)
    if stopping["on"] and mode == "hands-over":
        try:
            fresh = time.time() - os.stat(handover).st_mtime < 10
        except OSError:
            fresh = False
        if fresh:
            open(os.path.join(state, sid + ".handed-over"), "w").close()
            sys.exit(0)
"""


#: Stands in for `tap watch`, the supervisor every live session's worker runs
#: under: the updater tells a live session's worker from one finishing an ended
#: session's queue by its parent.
_SUPERVISOR = r"""
import subprocess, sys
child = subprocess.Popen(sys.argv[3:])
sys.exit(child.wait())
"""


#: Every stand-in worker a test started: their process groups are killed when
#: it ends, pass or fail (`_no_stand_in_left`). `proc.kill()` alone killed only
#: the stand-in `tap watch`, and its worker lived on, an orphan, for hours.
_STAND_INS: list = []


@pytest.fixture(autouse=True)
def _no_stand_in_left():
    yield
    while _STAND_INS:
        proc = _STAND_INS.pop()
        with contextlib.suppress(OSError):
            os.killpg(proc.pid, signal.SIGKILL)  # its own group: the stand-in and the worker under it
        with contextlib.suppress(Exception):
            proc.wait(5)


def _spawn_worker(state: Path, sid: str, mode: str, *, supervised: bool = True) -> subprocess.Popen:
    """A stand-in worker; `supervised`: under a stand-in `tap watch` (its session
    live), else straight under this test (its session ended). In a process
    group of its own, killed whole at the test's end."""
    (state / "daemon").mkdir(parents=True, exist_ok=True)
    script = state.parent / f"worker-{sid}.py"
    script.write_text(_WORKER)
    argv = [sys.executable, str(script), str(state), sid, mode, "daemon", "worker"]
    if supervised:
        supervisor = state.parent / "supervisor.py"
        supervisor.write_text(_SUPERVISOR)
        argv = [sys.executable, str(supervisor), "tap", "watch", *argv]
    proc = subprocess.Popen(argv, start_new_session=True)
    _STAND_INS.append(proc)
    assert wait_for(lambda: (state / f"{sid}.ready").exists(), 10.0)
    return proc


def _register_daemon(conn, sid, owner, state_dir=None):
    params = {"sid": sid, "harness": "test", "mode": Mode.DAEMON, "owner": owner, "generation": 1}
    if state_dir is not None:
        params["state_dir"] = str(state_dir)
    conn.call(Method.SESSION_REGISTER, params)


@no_real_app
def test_a_worker_hands_over_and_the_update_runs_without_waiting_for_its_session(service_home, machine):
    machine.plan("version", stdout={"cli_version": "0.1.0", "cli_latest": "9.9.9"})  # a newer CLI is out
    state = service_home.home / ".local" / "state" / "probe"
    worker = _spawn_worker(state, "s-busy", "hands-over")
    agent, owner = spawn_agent()
    try:
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _register_daemon(conn, "s-busy", owner, state)
            assert _check_now(conn)["outcome"] == "started"
            seen = _done(conn, timeout=30.0)
        assert seen[-1]["deferred"] is None, service_home.log()
        assert worker.wait(timeout=10) == 0  # the stand-in tap watch exits with its worker
        assert (state / "s-busy.handed-over").exists()
        (call,) = machine.calls("update")
        assert call["barrier"]  # the barrier went up only after the worker left
        # The session goes on: nothing waited for it to end, and nothing is held now.
        assert pid_running(agent.pid)
        assert not barrier.hold_path().exists()
        assert not (state / "daemon" / "s-busy.handover").exists()
    finally:
        worker.kill()
        kill_agent(agent)


def test_a_worker_that_will_not_hand_over_defers_and_lets_workers_start_again(service_home, machine, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_WORKER_STOP_S", "1")
    state = service_home.home / ".local" / "state" / "probe"
    worker = _spawn_worker(state, "s-stuck", "drains")
    try:
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            assert _done(conn, timeout=30.0)[-1]["deferred"] == "daemon_recording"
        assert machine.calls("update") == []
        assert not barrier.workers_held()
    finally:
        worker.kill()


def test_new_workers_come_back_later_while_the_running_ones_hand_over(service_home):
    from probe import _entry

    token = "w" * 32
    barrier.hold_workers(token)  # this test process stands in for the service
    try:
        assert _entry._update_barrier(["daemon", "worker", "--session-id", "s"]) == barrier.WORKER_BUSY_EXIT_CODE
        assert _entry._update_barrier(["log", "loss", "0.1"]) is None  # every other command runs on
    finally:
        barrier.release_workers(token)
    assert _entry._update_barrier(["daemon", "worker", "--session-id", "s"]) is None


@pytest.mark.parametrize(
    ("held", "reason", "told"),
    [
        ("runs/r-1.flock", "run_in_flight", "run_in_flight"),
        ("daemon/s-old.lock", "daemon_recording", None),
        # A setup whose lock says nothing of since when (a holder from before
        # the record): this service's own deferral counts it (C1).
        ("wizard.lock", "setup_running", "setup_running"),
    ],
)
def test_a_day_of_deferral_ends_in_an_update(service_home, machine, monkeypatch, held, reason, told):
    """A run that never ends, a worker that cannot be asked (no pid: an older
    worker), or a setup left open, defers at most DEFER_LIMIT_S; then the
    update goes ahead, and the child is told what it goes past."""
    monkeypatch.setenv("PROBE_SERVICE_DEFER_LIMIT_S", "1")
    lock = _hold(service_home.home / ".local" / "state" / "probe" / held)
    try:
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            first = _done(conn)[-1]["deferred"]
            assert first == reason
            assert conn.call(Method.UPDATE_STATUS)["deferred_since"] is not None
            time.sleep(1.2)
            _check_now(conn)
            last = _done(conn)[-1]
        assert last["deferred"] is None, service_home.log()
        assert last["steps"]["cli_and_plugins"]["forced"] == first
        assert machine.calls("update")[-1]["env"]["PROBE_UPDATE_FORCED"] == told
        with service_home.connect() as conn:
            assert conn.call(Method.UPDATE_STATUS)["deferred_since"] is None
    finally:
        lock.close()


@pytest.mark.parametrize(
    ("holder", "held_for", "deferred"),
    [
        ("wizard.lock", 25 * 3600, None),
        ("wizard.lock", 60, "setup_running"),
        # A menu waiting on a person holds no lock; on this machine the update
        # would move its files (in place), so its marker holds it off, a day at most.
        ("wizard.menu", 25 * 3600, None),
        ("wizard.menu", 60, "setup_running"),
    ],
)
def test_a_setup_that_has_held_the_lock_a_day_is_updated_past_at_once(
    service_home, machine, holder, held_for, deferred
):
    """A `probe wizard` menu left open held every update off for good: a setup
    was never overridden (C1). Its holder's record (pid, start time, since
    when) says how long it has held the device, so a day of that is past the
    limit at this service's first look, however long the service itself has
    deferred; one that took it a minute ago still defers."""
    from probe.service import procid

    record = json.dumps({"pid": os.getpid(), "start": procid.start_time(os.getpid()), "at": time.time() - held_for})
    if holder == "wizard.lock":
        lock = _hold(_state_dir(service_home) / "wizard.lock")
        lock.write(record)
        lock.flush()
    else:
        _state_dir(service_home).mkdir(parents=True, exist_ok=True)
        (_state_dir(service_home) / f"wizard.menu.{os.getpid()}").write_text(record)
        lock = open(os.devnull)  # noqa: SIM115 -- closed below, as the lock is
    try:
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            done = _done(conn)[-1]
    finally:
        lock.close()
    assert done["deferred"] == deferred, service_home.log()
    calls = machine.calls("update")
    if deferred is None:
        assert done["steps"]["cli_and_plugins"]["forced"] == "setup_running"
        assert calls[-1]["env"]["PROBE_UPDATE_FORCED"] == "setup_running"
    else:
        assert calls == []


@pytest.mark.parametrize(
    ("side_by_side", "waited", "updates", "forced"),
    [
        (True, 60, True, []),  # a switch leaves the files the menu runs from where they are
        (False, 60, False, None),  # in place, or the first switch: they would move under it
        (False, 25 * 3600, True, ["setup_running"]),  # a day of waiting at most
    ],
)
def test_a_waiting_menu_holds_off_only_an_update_that_moves_its_files(monkeypatch, side_by_side, waited, updates, forced):
    """The menu lets go of wizard.lock while it waits on a person (C1), and
    marks that it waits instead: the files it runs from must not be moved
    under it mid-write. Only an update in place or the first switch would; a
    side-by-side switch goes on beside it."""
    import asyncio

    monkeypatch.setattr(updater, "look", lambda **_kw: updater.Busy(menu=True, menu_since=time.time() - waited))
    monkeypatch.setattr(updater, "side_by_side", lambda: side_by_side)

    async def login_env(**_kw):
        return {}

    monkeypatch.setattr(updater.loginenv, "child_env", login_env)
    up = updater.Updater(
        version="0.325.0", emit=lambda *a: None, changed=lambda: None, stop=lambda r: None,
        action_running=lambda: False, discovering=lambda: False,
    )
    applied: list = []

    async def apply(cycle_id, trigger, token, forced, login, skip_cli, held):
        applied.append(forced)
        return {"state": "done"}

    up._apply = apply  # noqa: SLF001 -- the barrier and the child are other tests'
    out = asyncio.run(up._core_step("c-1", "cli"))  # noqa: SLF001
    assert (applied, out.get("reason")) == (([forced] if updates else []), (None if updates else "setup_running"))


def test_a_session_s_own_state_dir_is_looked_in(service_home, machine, tmp_path):
    """A session run with XDG_STATE_HOME names its state folder when it
    registers (D13): its worker's lock is found there, and a daemon session
    whose folder holds no worker defers nothing."""
    other = Path(tempfile.mkdtemp(prefix="xdg-", dir=service_home.home)) / "probe"
    agent, owner = spawn_agent()
    try:
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _register_daemon(conn, "s-xdg", owner, other)
            lock = _hold(other / "wizard.lock")
            try:
                _check_now(conn)
                assert _done(conn)[-1]["deferred"] == "setup_running"
            finally:
                lock.close()
        assert machine.calls("update") == []
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            assert _done(conn)[-1]["deferred"] is None, service_home.log()
        assert machine.calls("update")
    finally:
        kill_agent(agent)


def test_the_update_child_gets_the_login_shell_s_path_and_settings(service_home, machine, monkeypatch):
    """The service's own environment is clean (X2); the update child's PATH and
    proxy come from the login shell, read for it (D11, D14)."""
    shell = service_home.home / "bin" / "fake-login-shell"
    shell.parent.mkdir(parents=True, exist_ok=True)
    shell.write_text(
        "#!/bin/sh\n"
        "# called as: fake-login-shell -ilc <script>\n"
        "export HTTPS_PROXY=http://proxy.example:3128\n"
        "export UV_INDEX_URL=https://mirror.example/simple\n"
        "export PATH=/opt/nvm/bin:$PATH\n"
        'echo "a profile banner"\n'
        'exec /bin/sh -c "$2"\n'
    )
    shell.chmod(0o755)
    monkeypatch.setenv("SHELL", str(shell))
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        _check_now(conn)
        _done(conn)
    (call,) = machine.calls("update")
    assert call["env"]["HTTPS_PROXY"] == "http://proxy.example:3128"
    assert call["env"]["UV_INDEX_URL"] == "https://mirror.example/simple"
    assert call["env"]["PATH"].split(":")[0] == "/opt/nvm/bin"
    assert str(service_home.home / ".local" / "bin") in call["env"]["PATH"].split(":")
    # Never stored: not in the service's own files.
    for path in paths.service_dir().rglob("*"):
        if path.is_file():
            assert b"proxy.example" not in path.read_bytes(), path


def test_a_hook_waits_for_the_barrier_only_until_its_own_deadline(service_home, monkeypatch):
    from probe import _entry

    token = "d" * 32
    barrier.raise_barrier(token)
    try:
        monkeypatch.setenv(barrier.DEADLINE_ENV, str(time.time() + 1.0))
        started = time.monotonic()
        assert _entry._update_barrier(["hook", "x"]) == barrier.BUSY_EXIT_CODE
        assert time.monotonic() - started < 2.0  # not WAIT_S (10 s)
        monkeypatch.setenv(barrier.DEADLINE_ENV, str(time.time() - 5))
        assert barrier.budget() == 0.0
        # Inherited by a job the hook left running, long after: an ordinary wait.
        monkeypatch.setenv(barrier.DEADLINE_ENV, str(time.time() - 3600))
        assert barrier.budget() == barrier.WAIT_S
        monkeypatch.setenv(barrier.DEADLINE_ENV, "not a number")
        assert barrier.budget() == barrier.WAIT_S
    finally:
        barrier.lower(token)


def test_a_forced_update_tells_the_child_so_it_does_not_defer_again(service_home, machine, monkeypatch):
    """After DEFER_LIMIT_S the cycle decided to update past a live run; the
    child's own run check must not undo that (D33)."""
    monkeypatch.setenv("PROBE_SERVICE_DEFER_LIMIT_S", "1")
    lock = _hold(service_home.home / ".local" / "state" / "probe" / "runs" / "r-1.flock")
    try:
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            _done(conn)
            time.sleep(1.2)
            _check_now(conn)
            _done(conn)
    finally:
        lock.close()
    (call,) = machine.calls("update")
    assert call["env"]["PROBE_UPDATE_FORCED"] == "run_in_flight"


def test_the_child_skips_its_run_check_only_when_the_service_forced_it(monkeypatch, tmp_path):
    from probe.cli import upgrading

    assert upgrading.FORCED_ENV == "PROBE_UPDATE_FORCED"
    from probe.service import updater

    assert updater.FORCED_ENV == upgrading.FORCED_ENV


def test_a_cli_start_waits_for_a_barrier_from_before_the_machine_key(service_home, monkeypatch):
    """The service that installs this code ran the older code: its barrier is
    in the shared folder (`paths.legacy_barrier_path`)."""
    from probe import _entry

    from probe.service import procid

    record = {"pid": os.getpid(), "start_time": procid.start_time(os.getpid()), "token": "o" * 32,
              "created_at": time.time()}
    paths.private_dir(paths.root_dir())
    paths.legacy_barrier_path().write_text(json.dumps(record))
    monkeypatch.setattr(barrier, "WAIT_S", 0.2)
    try:
        assert _entry._update_barrier(["log", "loss", "1"]) == barrier.BUSY_EXIT_CODE
    finally:
        paths.legacy_barrier_path().unlink()
    assert _entry._update_barrier(["log", "loss", "1"]) is None


def test_with_the_cli_current_the_workers_run_on_and_only_plugins_update(service_home, machine):
    """Nothing new for the env the workers run from: they are never stopped (D7)."""
    machine.plan("version", stdout={"cli_version": probe.__version__, "cli_latest": probe.__version__})
    state = service_home.home / ".local" / "state" / "probe"
    worker = _spawn_worker(state, "s-current", "hands-over")
    agent, owner = spawn_agent()
    try:
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _register_daemon(conn, "s-current", owner, state)
            _check_now(conn)
            assert _done(conn, timeout=30.0)[-1]["deferred"] is None, service_home.log()
        (call,) = machine.calls("update")
        assert call["env"]["PROBE_UPDATE_SKIP_CLI"] == "1"
        assert worker.poll() is None and not (state / "s-current.handed-over").exists()
    finally:
        worker.kill()
        kill_agent(agent)


def test_the_worker_of_an_ended_session_finishes_its_queue_untouched(service_home, machine):
    """No successor would take over its queue: it is waited for, never stopped."""
    machine.plan("version", stdout={"cli_version": "0.1.0", "cli_latest": "9.9.9"})
    state = service_home.home / ".local" / "state" / "probe"
    worker = _spawn_worker(state, "s-ended", "hands-over", supervised=False)  # its tap watch is gone
    try:
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            assert _done(conn, timeout=30.0)[-1]["deferred"] == "daemon_recording"
        assert machine.calls("update") == []
        assert worker.poll() is None and not (state / "s-ended.handed-over").exists()
    finally:
        worker.kill()


def test_a_run_that_just_started_is_not_updated_under_after_a_day_of_worker_waits(service_home, machine, monkeypatch):
    """Each reason's own 24 h: a day of waiting on a worker does not override a
    run that started a minute ago (D33)."""
    monkeypatch.setenv("PROBE_SERVICE_DEFER_LIMIT_S", "3600")
    state = service_home.home / ".local" / "state" / "probe"
    machine.plan("version", stdout={"cli_version": "0.1.0", "cli_latest": "9.9.9"})
    record = json.loads(paths.update_state_path().read_text()) if paths.update_state_path().exists() else {"v": 1}
    record["deferred_since"] = {"daemon_recording": time.time() - 7200}
    paths.update_state_path().parent.mkdir(parents=True, exist_ok=True)
    paths.update_state_path().write_text(json.dumps(record))
    lock = _hold(state / "runs" / "r-new.flock")
    worker = _spawn_worker(state, "s-gone", "drains", supervised=False)
    try:
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            assert _done(conn)[-1]["deferred"] == "run_in_flight"
            since = conn.call(Method.UPDATE_STATUS)["deferred_since"]
        assert machine.calls("update") == []
        assert since is not None
    finally:
        lock.close()
        worker.kill()


def test_a_plugins_only_update_is_a_success_not_a_failed_cli_step():
    from probe.cli import upgrading

    res = upgrading.cli_left_alone("1.2.3")
    assert (res.ok, res.changed, res.before, res.after) == (True, False, "1.2.3", "1.2.3")


def test_the_first_switch_waits_for_a_quiet_machine(monkeypatch):
    """It moves the folder every running process reads through (Codex R2 #1)."""
    from probe._shared import installs

    monkeypatch.setattr(installs, "usable", lambda tools=None: True)
    monkeypatch.setattr(installs, "needs_migration", lambda tools=None: True)
    assert updater.side_by_side() is False
    monkeypatch.setattr(installs, "needs_migration", lambda tools=None: False)
    assert updater.side_by_side() is True


def test_a_moved_worker_is_asked_for_long_enough(tmp_path, monkeypatch):
    """The service exits right after asking: the hand-over marker is dated
    ahead by the stop window, so a worker whose model round outlasts 10 s
    still hands over (Codex R2 #10)."""
    import time as _time

    state = tmp_path / "state"
    worker = _spawn_worker(state, "s-1", "hands-over")
    try:
        monkeypatch.setattr(updater, "_is_worker", lambda pid, sid: True)
        assert updater.hand_over_workers([state]) == 1
        marker = state / "daemon" / "s-1.handover"
        assert marker.stat().st_mtime > _time.time() + updater.WORKER_STOP_S - 60
        assert worker.wait(timeout=10) == 0
    finally:
        worker.kill()


def test_the_guard_starts_when_the_service_really_stops(monkeypatch):
    """Not when the cycle ends: a running action defers the stop, and a guard
    started then reads the still-serving service as one that will not go
    (critic R2 #6)."""
    spawned = []
    u = updater.Updater(version="0.1.0", emit=lambda *a: None, changed=lambda: None, stop=lambda r: None,
                        action_running=lambda: False, discovering=lambda: False)
    monkeypatch.setattr(u, "_spawn_guard", spawned.append)
    u.before_exit(StopReason.UPDATE)
    assert spawned == [], "no switch, no guard"
    u.guard_pending = "0.2.0"  # the cycle switched; its restart waits for an action
    assert spawned == []
    u.before_exit("tap_update")  # stopped first for another reason: the next one is the new version all the same
    assert spawned == ["0.2.0"] and u.guard_pending is None
    u.before_exit(StopReason.UPDATE)
    assert spawned == ["0.2.0"]


# -- after an update: what open sessions read follows it (plan C9) ----------------


def _claude_cache(home: Path) -> Path:
    return home / ".claude" / "plugins" / "cache" / "research-os-agent"


def _ledger(home: Path, **installed: Path) -> None:
    ledger = home / ".claude" / "plugins" / "installed_plugins.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(json.dumps({"version": 2, "plugins": {
        f"{name}@research-os-agent": [{"scope": "user", "installPath": str(path)}] for name, path in installed.items()
    }}))


def _probe_plugin(home: Path, version: str, mark: str) -> Path:
    root = _claude_cache(home) / "probe-research" / version
    (root / "hooks").mkdir(parents=True)
    (root / "hooks" / "statusline.py").write_text(f"# renderer {mark}\n")
    (root / "hooks" / "_session_marker.py").write_text(f"# marker reader {mark}\n")
    return root


@pytest.mark.parametrize("cli_moved", [False, True], ids=["plugins-only", "new-cli"])
def test_after_an_update_open_sessions_read_the_installed_copy(service_home, machine, cli_moved):
    """An update replaced the plugins under open sessions. The hooks follow at
    their next event; the status-line renderer, the managed block and the
    recorders' tap followed only a NEW session (live test D, 2026-10-24): the
    swarm ran 20 minutes after an update on the old renderer, block and tap.
    After the cycle the renderer is the installed copy's, the note sync runs
    `agent-rules refresh` and the reconcile that rewrites the block, and the
    service restarts onto the installed tap, the session's recorder resuming
    on it with nothing lost. With a new CLI the next service (the new code)
    does it."""
    from tests.test_service_recorders import _events, _params, _saw, _tap

    home = service_home.home
    machine.plan("cli", exit=0)
    if cli_moved:
        machine.plan("version", stdout={"cli_version": "999.0.0"})
    old_tap = _tap(_claude_cache(home) / "probe-research-tap" / "0.10.0", "0.10.0")
    old_plugin = _probe_plugin(home, "0.170.0", "old")
    _ledger(home, **{"probe-research": old_plugin, "probe-research-tap": old_tap})
    (home / ".claude" / "probe-research-statusline").mkdir(parents=True)
    (home / ".claude" / "probe-research-statusline" / "statusline.py").write_text("# renderer old\n")
    proc, owner = spawn_agent()
    try:
        first = service_home.start()
        params = _params("s1", owner, old_tap, "0.10.0", home)
        assert service_home.call(Method.SESSION_RECORD, params)["recording"]
        assert _saw(home, "s1", "started")
        # The update installs the new plugin and tap (Claude Code keeps the old folders).
        new_tap = _tap(_claude_cache(home) / "probe-research-tap" / "0.10.1", "0.10.1")
        new_plugin = _probe_plugin(home, "0.171.0", "new")
        _ledger(home, **{"probe-research": new_plugin, "probe-research-tap": new_tap})
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            _done(conn)
        assert service_home.wait_exit(first["pid"], 15), service_home.log()
        if cli_moved:
            # The new code's service follows up once it starts (a session's next ask).
            second = service_home.start()
            assert second["pid"] != first["pid"]
        assert _saw(home, "s1", "started", count=2, timeout=15), service_home.log()
        assert _events(home, "s1")[-1]["version"] == "0.10.1", "s1 resumed on the installed tap"
        assert [e["event"] for e in _events(home, "s1")] == ["started", "paused", "started"]
        renderer = home / ".claude" / "probe-research-statusline" / "statusline.py"
        assert wait_for(lambda: renderer.read_text() == "# renderer new\n", 10), renderer.read_text()
        calls = wait_for(lambda: len(machine.stand_in_calls("cli")) >= 2 and machine.stand_in_calls("cli"), 15)
        assert calls, service_home.log()
        ran = [(c["args"], c["env"]["PROBE_AGENT"]) for c in calls]
        assert (["agent-rules", "refresh"], "claude_code") in ran and (["notes", "sync"], None) in ran, ran
    finally:
        kill_agent(proc)


def test_the_first_start_after_an_older_services_update_follows_it_up(service_home):
    """The update that brings this code is run by a service before it, which
    marks nothing: the first service of the new version follows up the update
    the last cycle restarted onto it, once; a later start does not, nor does a
    fresh machine's first start."""
    def checker():
        return updater.Updater(
            version="2.0.0", emit=lambda *a: None, changed=lambda: None, stop=lambda r: None,
            action_running=lambda: False, discovering=lambda: False,
        )

    assert checker().take_followup() is False, "a fresh machine has no update to follow"
    paths.update_state_path().write_text(json.dumps({"v": 1, "last_check": time.time(), "last_result": {
        "ok": True, "at": time.time(), "restart": True,
        "steps": {"self": {"state": "done", "from_version": "1.0.0", "to_version": "2.0.0", "restart": True}}}}))
    assert checker().take_followup() is True
    assert checker().take_followup() is False, "once"
    old = json.loads(paths.update_state_path().read_text())
    assert old["followed_version"] == "2.0.0"
    paths.update_state_path().write_text(json.dumps({**old, "followed_version": "1.9.0"}))
    assert checker().take_followup() is True, "a version moved by hand since the last follow-up"


@pytest.mark.parametrize("argv", [["session", "status"], ["--version"], ["log", "loss", "0.1"]])
def test_a_start_that_waited_out_an_in_place_update_runs_again_on_the_new_code(service_home, monkeypatch, argv):
    """A machine's first update is in place and long: `probe session status`
    and `probe --version` answered busy (exit 75) to agents mid-work, and a
    start that waited went on with the old `probe.service` modules it had
    imported under the new CLI (`module 'probe.service.procid' has no
    attribute 'exists'`; release gate, 2026-10-25). Now every non-hook start
    waits it out and runs again in a fresh interpreter."""
    import threading

    from probe import _entry

    reran = []
    monkeypatch.setattr(_entry, "_rerun", lambda a: reran.append(a) or 0)
    token = "r" * 32
    barrier.raise_barrier(token)
    threading.Timer(0.5, barrier.lower, args=(token,)).start()
    assert _entry._update_barrier(argv) == 0
    assert reran == [argv]


def test_the_rerun_execs_a_fresh_interpreter_with_the_same_command_and_stops_after_max(monkeypatch):
    from probe import _entry

    calls = []
    monkeypatch.setattr(_entry.os if hasattr(_entry, "os") else __import__("os"), "execve",
                        lambda path, args, env: calls.append((path, args, env.get(_entry.RERUN_ENV))))
    monkeypatch.delenv(_entry.RERUN_ENV, raising=False)
    monkeypatch.setattr(sys, "orig_argv", [sys.executable, "/x/bin/probe", "session", "status"], raising=False)
    if os.name != "nt":
        _entry._rerun(None)
        assert calls == [(sys.executable, [sys.executable, "/x/bin/probe", "session", "status"], "1")]
        _entry._rerun(["log", "loss"])
        assert calls[-1][1] == [sys.executable, "-m", "probe", "log", "loss"]
    # Past MAX_RERUNS a cleared wait runs on in this process instead of again.
    token = "m" * 32
    monkeypatch.setenv(_entry.RERUN_ENV, str(_entry.MAX_RERUNS))
    monkeypatch.setattr(_entry, "_rerun", lambda a: pytest.fail("re-ran past MAX_RERUNS"))
    barrier.raise_barrier(token)
    import threading

    threading.Timer(0.3, barrier.lower, args=(token,)).start()
    assert _entry._update_barrier(["status"]) is None


def _version_env(home: Path, version: str) -> Path:
    env = home / ".local" / "share" / "uv" / "probe-versions" / version / "probe-research"
    python = installs_mod.env_python(env)
    python.parent.mkdir(parents=True)
    python.write_text("#!/bin/sh\n")
    python.chmod(0o755)
    return env.resolve()


def test_a_stale_runtime_json_follows_the_switch_before_the_restart(service_home, monkeypatch):
    """10-28, probe demo: the update switched the tool path to 0.342.0 but
    runtime.json still named 0.339.0's interpreter, so the version read said
    0.339.0, the restart started 0.339.0 and its guard, watching for 0.339.0
    from 0.342.0's env, switched a good update back. runtime.json now follows
    the tool path, and the version the restart and guard expect is that env's."""
    old, new = _version_env(service_home.home, "0.1.0"), _version_env(service_home.home, "0.2.0")
    client.write_runtime(str(installs_mod.env_python(old)), "0.1.0")
    monkeypatch.setattr(installs_mod, "active", lambda tools=None: new)
    monkeypatch.setattr(installs_mod, "env_version", lambda env, **kw: {new: "0.2.0", old: "0.1.0"}.get(env))

    assert updater.runtime_follows_switch("0.1.0") == "0.2.0"
    assert json.loads(paths.runtime_path().read_text()) == {
        "python": str(installs_mod.env_python(new)), "cli_version": "0.2.0"}
    assert client.runtime_python() == str(installs_mod.env_python(new))


def test_runtime_json_naming_the_switched_env_is_left_alone(service_home, monkeypatch):
    new = _version_env(service_home.home, "0.2.0")
    client.write_runtime(str(installs_mod.env_python(new)), "0.2.0")
    before = paths.runtime_path().read_text()
    monkeypatch.setattr(installs_mod, "active", lambda tools=None: new)
    monkeypatch.setattr(installs_mod, "env_version", lambda env, **kw: pytest.fail("no version read needed"))
    assert updater.runtime_follows_switch("0.2.0") == "0.2.0"
    assert paths.runtime_path().read_text() == before


@pytest.mark.parametrize("layout", ["none", "unreadable"])
def test_no_switch_layout_leaves_runtime_json_and_the_version_alone(service_home, monkeypatch, layout):
    """A machine without side-by-side installs (pipx, in place), or whose
    layout cannot be read, restarts on what it read, as before: never held."""
    old = _version_env(service_home.home, "0.1.0")
    client.write_runtime(str(installs_mod.env_python(old)), "0.1.0")

    def active(tools=None):
        if layout == "unreadable":
            raise RuntimeError("no uv")
        return None

    monkeypatch.setattr(installs_mod, "active", active)
    assert updater.runtime_follows_switch("0.1.0") == "0.1.0"


@pytest.mark.parametrize("case", ["version unreadable", "raises", "uninstalling"])
def test_a_disagreement_that_cannot_be_put_right_restarts_nothing(service_home, monkeypatch, case):
    """Reviewer: returning the stale version still restarted (the env moved)
    with a guard watching for it from the new env, the 10-28 failure again.
    None: no restart this time."""
    old, new = _version_env(service_home.home, "0.1.0"), _version_env(service_home.home, "0.2.0")
    client.write_runtime(str(installs_mod.env_python(old)), "0.1.0")
    before = paths.runtime_path().read_text()
    monkeypatch.setattr(installs_mod, "active", lambda tools=None: new)

    def version(env, **kw):
        if case == "raises":
            raise OSError("no uv")
        return "0.2.0" if case == "uninstalling" else None

    monkeypatch.setattr(installs_mod, "env_version", version)
    if case == "uninstalling":
        monkeypatch.setattr(client, "uninstall_barrier", lambda: {"at": 1.0})
    assert updater.runtime_follows_switch("0.1.0") is None
    assert paths.runtime_path().read_text() == before


def test_the_self_step_and_the_update_action_expect_the_switched_version(service_home, monkeypatch):
    """Both places that decide a restart (and its guard's version) ask
    `runtime_follows_switch`, not runtime.json's interpreter alone.
    MUTATION: drop either call."""
    import asyncio

    from probe.service import children

    async def read(action, params, timeout):
        return 0, {"cli_version": "0.1.0"}

    monkeypatch.setattr(children, "run_read", read)
    monkeypatch.setattr(updater, "runtime_follows_switch", lambda installed: "0.2.0")
    monkeypatch.setattr(updater, "_env_moved", lambda started=None: False)
    monkeypatch.setattr(installs_mod, "active", lambda tools=None: Path("/v/0.2.0"))
    stops = []
    u = updater.Updater(version="0.1.0", emit=lambda *a: None, changed=lambda: None, stop=stops.append,
                        action_running=lambda: False, discovering=lambda: False)
    monkeypatch.setattr(u, "followup", lambda moved: None)
    monkeypatch.setattr(u, "mark_followup", lambda cycle: None)

    done, restart = asyncio.run(u._self("c1"))
    assert restart is True and done["to_version"] == "0.2.0"
    asyncio.run(u._after_update_action())
    assert u.guard_pending == "0.2.0" and stops == [StopReason.UPDATE]

    monkeypatch.setattr(updater, "runtime_follows_switch", lambda installed: None)
    monkeypatch.setattr(updater, "_env_moved", lambda started=None: True)  # the env did move
    u.guard_pending, stops[:] = None, []
    done, restart = asyncio.run(u._self("c3"))
    assert restart is False, "a disagreement it cannot put right restarts nothing"
    asyncio.run(u._after_update_action())
    assert u.guard_pending is None and stops == []
