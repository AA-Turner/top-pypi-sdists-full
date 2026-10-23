"""The service's updater (plan X1, R2, R3, D3, D4, Q4): real service, real processes.

A cycle runs CLI-and-plugins (one `probe.core.run update` child), then the
desktop app's own updater, then reads the installed CLI version and restarts
the service when it moved. Step 1 runs only on a quiet machine: a daemon
worker's lock, a run lock, `wizard.lock` or a running action defers it (with a
skip `probe doctor` reads, and a retry when a session ends), and the update
barrier is up while it runs, which a CLI start waits for. A cycle holds the
service alive. Automatic updates off: nothing runs. The CLI and the plugin hook
ask the service instead of spawning their own updater while the switch is on.

`FakeCore` plays the `probe.core.run` children, `fake_open` macOS's `open` (it
writes the app's report as the app would), `fake_app` a `Probe.app` bundle.
"""

from __future__ import annotations

import asyncio
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
from probe.service import appupdate, barrier, client, paths
from probe.service import updater
from probe.service.protocol import Method, Mode, StopReason
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
def test_a_cycle_runs_cli_and_plugins_then_the_app_then_reads_the_version(service_home, machine, monkeypatch):
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_launcher_secret")
    app = fake_app(service_home.home)
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        started = _check_now(conn, "session")
        assert started["outcome"] == "started"
        seen = _done(conn)
        status = conn.call(Method.UPDATE_STATUS)
    steps = [(e["step"], e.get("state")) for e in seen if e["topic"] == "update.step" and "state" in e]
    assert steps == [
        ("cli_and_plugins", "started"),
        ("cli_and_plugins", "done"),
        ("app", "started"),
        ("app", "done"),
        ("self", "done"),
    ]
    forwarded = [e["event"] for e in seen if e["topic"] == "update.step" and "event" in e]
    assert [e["event"] for e in forwarded] == ["step", "done"]
    done = seen[-1]
    assert done["cycle_id"] == started["cycle_id"] and done["ok"] is True and done["restart"] is False
    assert done["steps"]["app"]["outcome"] == "updated" and done["steps"]["app"]["version_after"] == "0.1.4"
    # In that order, as processes: the update child, then `open`, then the version read.
    (update,) = machine.calls("update")
    (version,) = machine.calls("version")
    (opened,) = open_calls(service_home.home)
    assert update["at"] < opened["at"] < version["at"]
    assert opened["argv"] == ["-n", "-g", "-j", str(app), "--args", "--background-update"]
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


def test_a_running_action_defers_the_update_and_the_update_holds_the_slot(service_home, machine):
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
    # The other way round: while the update step runs, an action is busy.
    slow = service_home.home / "update-may-finish"
    machine.plan("update", steps=[{"wait": str(slow)}])
    with service_home.connect() as conn:
        assert wait_for(lambda: conn.call(Method.STATUS)["actions"]["running"] is None, 5.0)
        assert _check_now(conn)["outcome"] == "started"
        wait_for(lambda: machine.calls("update"), 10.0)
        with pytest.raises(client.ServiceError) as raised:
            conn.call(Method.ACTION_RUN, {"action": "logout", "params": {}, "client_request_id": "b"})
        assert raised.value.code == -32010 and raised.value.data["holder"]["kind"] == "update"
        with pytest.raises(client.ServiceError) as stop:
            conn.call(Method.STOP)
        assert stop.value.data == {"reason": "updating"}
        slow.touch()


def test_a_cli_start_waits_for_the_barrier(service_home):
    token = "t" * 32
    barrier.raise_barrier(token)  # this test process stands in for the service
    script = "import sys; from probe._entry import main; sys.exit(main(['--version']))"
    started = time.monotonic()
    child = subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(1.0)
    assert child.poll() is None  # still waiting: nothing of the CLI imported yet
    barrier.lower(token)
    out, err = child.communicate(timeout=60)
    assert child.returncode == 0, err
    assert probe.__version__ in out
    assert time.monotonic() - started >= 1.0


def test_a_cli_start_gives_up_busy_and_the_update_s_own_children_pass(service_home, monkeypatch):
    from probe import _entry
    from probe.daemon import worker

    token = "u" * 32
    barrier.raise_barrier(token)
    monkeypatch.setattr(barrier, "WAIT_S", 0.2)
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
        "from probe import _entry; barrier.WAIT_S = 0.2; rc = _entry.main(['log', 'loss', '1']); "
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


@no_real_app
def test_a_restart_for_a_new_cli_waits_for_a_running_action(service_home, machine):
    """The update lets go of the mutating slot after its first step, so an
    action can start while the app step runs. A new CLI then restarts the
    service -- after that action, never under it (it would read as stopped)."""
    machine.plan("version", stdout={"cli_version": "9.9.9"})
    gate = service_home.home / "action-may-finish"
    machine.plan("logout", steps=[{"wait": str(gate)}])
    fake_open(service_home.home / "bin", delay=1.5)
    fake_app(service_home.home)
    first = service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        _check_now(conn)
        events_until(conn, lambda e: e["topic"] == "update.step" and e.get("step") == "app", 20.0)
        body = {"action": "logout", "params": {}, "client_request_id": "mid"}
        action_id = conn.call(Method.ACTION_RUN, body)["action_id"]
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


# -- the desktop app (D3, X4) --------------------------------------------------


@pytest.fixture
def app_home(tmp_path, monkeypatch):
    if (Path("/Applications") / appupdate.APP_NAME).exists():
        pytest.skip("a real /Applications/Probe.app is found first")
    home = tmp_path / "home"
    (home / ".local" / "state" / "probe" / "service").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    bin_dir = home / "bin"
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return home


def _app_update(**kwargs) -> dict:
    return asyncio.run(appupdate.update(**kwargs))


@pytest.mark.parametrize(
    ("bundle", "capability", "outcome"),
    [
        ("ai.prbe.desktop", None, "not_capable"),
        ("ai.prbe.desktop", 0, "not_capable"),
        ("com.example.other", 1, "not_installed"),
    ],
)
def test_the_app_is_launched_only_when_it_is_ours_and_capable(app_home, bundle, capability, outcome):
    fake_open(app_home / "bin")
    fake_app(app_home, bundle_id=bundle, capability=capability)
    assert _app_update(timeout=1.0)["outcome"] == outcome
    assert open_calls(app_home) == []


def test_no_app_installed_launches_nothing(app_home):
    fake_open(app_home / "bin")
    assert _app_update(timeout=1.0) == {"outcome": "not_installed"}
    assert open_calls(app_home) == []


def test_a_running_app_is_never_launched(app_home):
    fake_open(app_home / "bin")
    app = fake_app(app_home)
    executable = app / "Contents" / "MacOS" / "Probe"
    running = subprocess.Popen([str(executable), "30"], executable=shutil.which("sleep"))
    try:
        assert wait_for(lambda: appupdate.running(app), 5.0)
        result = _app_update(timeout=1.0)
    finally:
        running.kill()
        running.wait()
    assert result["outcome"] == "running"
    assert open_calls(app_home) == []


def test_the_app_s_report_for_this_attempt_is_read(app_home):
    fake_open(app_home / "bin", result="failed", delay=0.3)
    app = fake_app(app_home)
    result = _app_update(timeout=10.0, poll=0.05)
    assert result == {
        "app": str(app),
        "outcome": "failed",
        "version_before": "0.1.3",
        "version_after": "0.1.3",
        "error": "signature check failed",
    }
    (opened,) = open_calls(app_home)
    assert opened["argv"] == ["-n", "-g", "-j", str(app), "--args", "--background-update"]


def test_a_copy_never_opened_is_not_launched(app_home):
    """A downloaded Probe.app nobody has opened yet still carries
    com.apple.quarantine: launching it would show Gatekeeper's prompt."""
    fake_open(app_home / "bin")
    fake_app(app_home, quarantined=True)
    assert _app_update(timeout=1.0)["outcome"] == "quarantined"
    assert open_calls(app_home) == []


def test_an_app_that_found_itself_running_checked_nothing(app_home):
    """`current` with an error is the app's own "another Probe holds my lock":
    it checked nothing, so it is a running app (asked again next cycle)."""
    fake_open(app_home / "bin", result="current", error="Probe is already running; it installs its own updates")
    fake_app(app_home)
    result = _app_update(timeout=10.0, poll=0.05)
    assert result["outcome"] == "running" and "already running" in result["error"]
    assert len(open_calls(app_home)) == 1


@pytest.mark.parametrize("report", ["none", "an earlier attempt's"])
def test_no_report_for_this_attempt_times_out(app_home, report):
    if report == "none":
        fake_open(app_home / "bin", result=None)
    else:
        fake_open(app_home / "bin", result="updated", finished_offset=-3600)
    fake_app(app_home)
    result = _app_update(timeout=0.5, poll=0.05)
    assert result["outcome"] == "timeout"
    assert len(open_calls(app_home)) == 1


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


def _spawn_worker(state: Path, sid: str, mode: str, *, supervised: bool = True) -> subprocess.Popen:
    """A stand-in worker; `supervised`: under a stand-in `tap watch` (its session
    live), else straight under this test (its session ended)."""
    (state / "daemon").mkdir(parents=True, exist_ok=True)
    script = state.parent / f"worker-{sid}.py"
    script.write_text(_WORKER)
    argv = [sys.executable, str(script), str(state), sid, mode, "daemon", "worker"]
    if supervised:
        supervisor = state.parent / "supervisor.py"
        supervisor.write_text(_SUPERVISOR)
        argv = [sys.executable, str(supervisor), "tap", "watch", *argv]
    proc = subprocess.Popen(argv)
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


@pytest.mark.parametrize("held", ["runs/r-1.flock", "daemon/s-old.lock"])
def test_a_day_of_deferral_ends_in_an_update(service_home, machine, monkeypatch, held):
    """A run that never ends, or a worker that cannot be asked (no pid: an
    older worker), defers at most DEFER_LIMIT_S; then the update goes ahead."""
    monkeypatch.setenv("PROBE_SERVICE_DEFER_LIMIT_S", "1")
    lock = _hold(service_home.home / ".local" / "state" / "probe" / held)
    try:
        service_home.start()
        with service_home.connect() as conn:
            conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
            _check_now(conn)
            first = _done(conn)[-1]["deferred"]
            assert first in ("run_in_flight", "daemon_recording")
            assert conn.call(Method.UPDATE_STATUS)["deferred_since"] is not None
            time.sleep(1.2)
            _check_now(conn)
            last = _done(conn)[-1]
        assert last["deferred"] is None, service_home.log()
        assert last["steps"]["cli_and_plugins"]["forced"] == first
        assert machine.calls("update")
        with service_home.connect() as conn:
            assert conn.call(Method.UPDATE_STATUS)["deferred_since"] is None
    finally:
        lock.close()


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
