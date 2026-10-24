"""The CLI's local work goes through the Probe service (the service owns it).

    probe status / doctor  the service's own view: running, version, pid,
                           the sessions it registered (with their mode), the
                           recorders it runs, its hook hosts, the runs held,
                           its updater; "not running, and how it starts" when
                           none answers -- and none is started by asking
    probe capture off      the recorders it runs for that agent finish now
                           (`recorders.finish`), and the result says so; with
                           no service, the killswitch alone, as before
    probe exec             its run is held (`run.hold`): the updater defers
                           for it without any lock file, and lets go when the
                           process exits or releases it
    manifest refresh       a stale manifest cache is refreshed by ONE child of
                           the service (`manifest.refresh`), not a spawn per
                           command; no service (or a context it refuses):
                           the detached refresher, as before

Real service processes in a throwaway HOME (`service_harness`); the stand-ins
are the ones the other service suites use: a fake tap (`test_service_recorders`)
and `FakeCore` for the `probe.core.run` children.
"""

from __future__ import annotations

import asyncio
import contextlib
import http.server
import importlib
import json
import os
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

import probe
from probe import version_policy
from probe.cli import capture, doctor, service_calls
from probe.service import client, manifest, paths, runholds, updater
from probe.service.protocol import CheckOutcome, Method, Mode
from tests.service_fakes import FakeCore, enable_auto_update, events_until, fake_open, last_checked
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401
from tests.test_service_recorders import _events, _params, _saw, _tap

cli_main = importlib.import_module("probe.cli.main")

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the service is POSIX-only (plan S8)")

UPDATE_TOPICS = ["update.started", "update.step", "update.deferred", "update.done", "service.stopping"]
STEP = {"event": "step", "name": "persistent_install", "status": "done", "message": "CLI current", "agent": None}


@pytest.fixture
def agent():
    proc, owner = spawn_agent()
    yield proc, owner
    kill_agent(proc)


def _probe(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "probe.cli", *args], capture_output=True, text=True, timeout=120
    )


# -- probe status / probe doctor ----------------------------------------------------


def test_with_no_service_the_view_says_so_and_how_it_starts_and_starts_none(service_home):
    view = service_calls.view()
    assert (view["reach"], view["running"], view["pid"], view["sessions"]) == ("not_running", False, None, [])
    assert "probe service start" in service_calls.summary(view)
    rows = "\n".join(doctor.service_rows(view))
    assert "Probe service" in rows and "not running" in rows and "probe service start" in rows
    state = json.loads(_probe("status", "--json").stdout)
    assert state["service"]["reach"] == "not_running"
    assert service_home.service_processes() == [], "a status read must never start the service"


def test_status_and_doctor_show_what_the_service_holds(service_home, agent):
    _, owner = agent
    started = service_home.start()
    service_home.call(
        Method.SESSION_REGISTER,
        {"sid": "s-daemon", "harness": "claude_code", "mode": Mode.DAEMON, "owner": owner, "generation": 1},
    )
    held = service_calls.hold_run("run-abc")
    assert held is not None and held["pid"] == os.getpid()
    try:
        view = service_calls.view()
        assert view["reach"] == "answered" and view["running"] is True, view
        assert (view["pid"], view["version"]) == (started["pid"], started["service_version"])
        assert view["state"] in ("discovering", "running", "grace")
        assert view["sessions"] == [
            {"sid": "s-daemon", "harness": "claude_code", "mode": "daemon", "alive": True, "receipts": None}
        ]
        assert [(h["harness"], h["sessions"], h["alive"]) for h in view["harnesses"]] == [("claude_code", 1, 1)]
        assert [(r["run"], r["pid"]) for r in view["runs"]] == [("run-abc", os.getpid())]
        assert view["recorders"] == [] and view["hook_hosts"] == []
        assert set(view["update"]) == {
            "enabled", "in_progress", "step", "last_check", "last_ok", "next_check",
            "deferred_reason", "deferred_at", "deferred_since",
        }
        line = service_calls.summary(view)
        assert "1 live session" in line and "1 run in flight" in line and f"pid {started['pid']}" in line
        rows = "\n".join(doctor.service_rows(view))
        assert "s-daemon claude_code daemon" in rows and "run-abc" in rows and "Updates" in rows

        # The CLI end to end: `probe status --json` carries it (a new key only).
        state = json.loads(_probe("status", "--json").stdout)
        assert state["service"]["reach"] == "answered"
        assert state["service"]["sessions"][0]["mode"] == "daemon"
        assert {"v", "agents", "account", "versions", "errors"} <= set(state)
        human = _probe("status").stdout
        assert "Probe service      " in human and "1 live session" in human
        assert "Probe service" in _probe("doctor").stdout
    finally:
        service_calls.release_run("run-abc", held)


def test_a_service_that_never_answers_costs_status_its_timeout_and_no_more(service_home):
    """Something listens where the service's socket is and answers nothing."""
    sock_path = paths.ensure_dirs()
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(str(sock_path))
    listener.listen(4)
    try:
        began = time.monotonic()
        view = service_calls.view(timeout=0.5)
        assert time.monotonic() - began < 2.0
        assert view["reach"] == "unreachable" and view["running"] is None and "did not answer" in view["error"]
    finally:
        listener.close()
        with contextlib.suppress(OSError):
            os.unlink(sock_path)


# -- probe capture off ----------------------------------------------------------------


def test_finish_recorders_finishes_that_agents_recorders_only(service_home, agent, tmp_path):
    _, owner = agent
    root = _tap(tmp_path / "tap-a", "0.10.0")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, _params("s1", owner, root, "0.10.0", tmp_path))
    other = _params("s2", owner, root, "0.10.0", tmp_path)
    other["harness"] = "codex"
    service_home.call(Method.SESSION_RECORD, other)
    assert _saw(service_home.home, "s1", "started") and _saw(service_home.home, "s2", "started")

    done = service_calls.finish_recorders("claude_code", wait=5)
    assert done is not None and (done.finished, done.unfinished) == (["s1"], [])
    assert [e["event"] for e in _events(service_home.home, "s1")] == ["started", "ended"]
    assert service_home.call(Method.SESSION_RECORDING, {"sid": "s2"}) == {"recording": True}
    assert "recorders.finish: 1 recorder(s) of claude_code asked to finish" in service_home.log()
    # Nothing of that agent left: an empty answer, not an error.
    assert service_home.call(Method.RECORDERS_FINISH, {"harness": "claude_code"}) == {
        "finished": [], "unfinished": [],
    }


_FINISH_AS_NNP = """
import ctypes, json, sys
assert ctypes.CDLL(None, use_errno=True).prctl(38, 1, 0, 0, 0) == 0  # PR_SET_NO_NEW_PRIVS
from probe.cli import service_calls
done = service_calls.finish_recorders(sys.argv[1], wait=1)
print(json.dumps({"error": done.error, "refused": done.refused, "still": done.still_recording,
                  "finished": done.finished}))
"""


def test_a_caller_the_service_refuses_is_told_what_it_still_records(service_home, agent, tmp_path):
    """Codex P2 (round 4): from inside a sandbox (here no_new_privs) the
    service takes no work, and capture off read that as "not confirmed, run
    this again" for good. It reads what the service records instead (READ):
    this agent's live recordings by name, another agent's never."""
    if not sys.platform.startswith("linux"):
        pytest.skip("no-new-privs is Linux's")
    _, owner = agent
    root = _tap(tmp_path / "tap-a", "0.10.0")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, _params("s1", owner, root, "0.10.0", tmp_path))
    other = _params("s2", owner, root, "0.10.0", tmp_path)
    other["harness"] = "codex"
    service_home.call(Method.SESSION_RECORD, other)
    assert _saw(service_home.home, "s1", "started") and _saw(service_home.home, "s2", "started")

    def finish(harness: str) -> dict:
        done = subprocess.run([sys.executable, "-c", _FINISH_AS_NNP, harness], capture_output=True, text=True,
                              timeout=60)
        assert done.returncode == 0, done.stderr
        return json.loads(done.stdout.strip().splitlines()[-1])

    assert finish("claude_code") == {"error": None, "refused": True, "still": ["s1"], "finished": []}
    assert finish("kimi_code") == {"error": None, "refused": True, "still": [], "finished": []}
    assert service_home.call(Method.SESSION_RECORDING, {"sid": "s1"}) == {"recording": True}, "nothing stopped"


@pytest.fixture
def capture_device(service_home, tmp_path, monkeypatch):
    """`test_setup_wizard.isolate`'s device: Claude Code's tap folder paired,
    the CLI config, and no server to revoke against."""
    tap_dir = tmp_path / "tap-state"
    tap_dir.mkdir()
    (tap_dir / ".token").write_text("ros_ing_paired")
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(tap_dir))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / "pi-agent"))
    for name in ("PROBE_AGENT", "PROBE_TAP_SOURCE", "PROBE_INGEST_TOKEN"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(capture, "revoke_capture_device", lambda *a, **k: None)
    return tap_dir


def test_capture_off_says_what_the_service_stopped(service_home, agent, tmp_path, capture_device):
    _, owner = agent
    root = _tap(tmp_path / "tap-a", "0.10.0")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, _params("s1", owner, root, "0.10.0", tmp_path))
    assert _saw(service_home.home, "s1", "started")

    result = capture.turn_off(capture.OffMode.DISABLE)

    assert (capture_device / ".disabled").exists()
    assert (result.service_answered, result.hosted_finished, result.hosted_unfinished) == (True, ["s1"], [])
    assert result.verified, result.summary()
    assert result.summary().endswith("The Probe service stopped recording 1 session.")
    assert _saw(service_home.home, "s1", "ended")


def test_a_recorder_still_finishing_keeps_off_unverified(service_home, agent, tmp_path, capture_device, monkeypatch):
    _, owner = agent
    root = _tap(tmp_path / "tap-a", "0.10.0")
    service_home.start()
    service_home.call(
        Method.SESSION_RECORD, _params("s1", owner, root, "0.10.0", tmp_path, PROBE_TEST_FINISH_S="3")
    )
    assert _saw(service_home.home, "s1", "started")
    monkeypatch.setattr(service_calls, "FINISH_WAIT_S", 0.3)

    result = capture.turn_off(capture.OffMode.DISABLE)

    assert (result.hosted_finished, result.hosted_unfinished) == ([], ["s1"])
    assert result.daemon_stopped is False and result.verified is False
    assert "uploader still running" in result.summary()
    assert any("still finishing the recording of 1 session(s) (s1)" in w for w in result.warnings)


def test_a_refused_capture_off_matches_recorders_as_the_service_does(monkeypatch):
    """Review: a recorder whose registration had already gone (its last pass
    still running) was missed, and capture off said "off". The recorder's own
    harness counts first; one with no harness known counts as possibly this
    agent's -- named, never claimed off."""
    from probe.service import protocol

    status = {"recorders": [
        {"sid": "own", "alive": True, "harness": "claude_code"},  # registration gone
        {"sid": "theirs", "alive": True, "harness": "codex"},
        {"sid": "registered", "alive": True},  # an older service: no harness field
        {"sid": "unknown", "alive": True},  # neither
        {"sid": "done", "alive": False, "harness": "claude_code"},
    ]}
    listing = {"sessions": [{"sid": "registered", "harness": "claude_code"}, {"sid": "theirs", "harness": "codex"}]}

    def refused(*a, **k):
        raise client.ServiceError(protocol.ErrorCode.REFUSED, "refused", {"reason": "sandboxed"})

    monkeypatch.setattr(service_calls, "_reachable", lambda: True)
    monkeypatch.setattr(client, "finish_recorders", refused)
    monkeypatch.setattr(client, "call", lambda method, *a, **k: status if method == Method.STATUS else listing)
    done = service_calls.finish_recorders("claude_code")
    assert (done.refused, done.error) == (True, None)
    assert done.still_recording == ["own", "registered", "unknown"]


def test_capture_off_from_inside_a_sandbox_succeeds_when_nothing_of_it_is_recorded(capture_device, monkeypatch):
    """Refused (a sandbox), and the service records nothing of this agent:
    there is nothing to stop, so off is off -- not "run this again"."""
    monkeypatch.setattr(capture, "_finish_hosted_recorders",
                        lambda source: service_calls.Finished(refused=True, still_recording=[]))
    result = capture.turn_off(capture.OffMode.DISABLE)
    assert result.daemon_stopped is not False and result.verified, (result.summary(), result.warnings)
    assert not any("could not confirm" in w or "run this again" in w for w in result.warnings), result.warnings


def test_capture_off_from_inside_a_sandbox_says_what_still_runs_and_how_to_stop_it(capture_device, monkeypatch):
    monkeypatch.setattr(capture, "_finish_hosted_recorders",
                        lambda source: service_calls.Finished(refused=True, still_recording=["s1"]))
    result = capture.turn_off(capture.OffMode.DISABLE)
    assert result.daemon_stopped is False and result.verified is False
    (said,) = [w for w in result.warnings if "still records" in w]
    assert "1 session(s) of this agent (s1)" in said and "takes no requests from inside a sandbox" in said
    assert "upload nothing more" in said and "outside this sandbox" in said
    assert not any("run this again" in w for w in result.warnings), "no advice that cannot succeed"


def test_capture_off_is_not_verified_when_the_service_could_not_be_asked(service_home, capture_device, monkeypatch):
    """Its socket is there and the call fails (no answer in time): a recorder
    it hosts may still be uploading, so "off" is not claimed (Codex P1)."""
    monkeypatch.setattr(service_calls, "FINISH_WAIT_S", 0.1)
    monkeypatch.setattr(service_calls, "FINISH_TIMEOUT_S", 0.3)
    sock_path = paths.ensure_dirs()
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(str(sock_path))
    listener.listen(4)
    try:
        result = capture.turn_off(capture.OffMode.DISABLE)
    finally:
        listener.close()
        with contextlib.suppress(OSError):
            os.unlink(sock_path)
    assert result.service_answered is False and result.daemon_stopped is False and result.verified is False
    assert any("could not confirm" in w for w in result.warnings), result.warnings
    assert "uploader still running" in result.summary()


def _older_service(sock_path: Path, recorders: list) -> threading.Thread:
    """A service from before `recorders.finish`: hello, `-32601` for it, and
    a `service.status` listing `recorders`."""
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(str(sock_path))
    listener.listen(4)
    listener.settimeout(10)

    def serve() -> None:
        with listener:
            for _ in range(2):  # recorders.finish, then service.status
                try:
                    conn, _ = listener.accept()
                except OSError:
                    return
                with conn, conn.makefile("rwb") as stream:
                    for line in stream:
                        message = json.loads(line)
                        if message["method"] == "service.hello":
                            answer = {"jsonrpc": "2.0", "id": message["id"], "result": {"api": 1}}
                        elif message["method"] == "service.status":
                            answer = {"jsonrpc": "2.0", "id": message["id"], "result": {"recorders": recorders}}
                        else:
                            answer = {"jsonrpc": "2.0", "id": message["id"],
                                      "error": {"code": -32601, "message": "unknown method"}}
                        stream.write((json.dumps(answer) + "\n").encode())
                        stream.flush()
                        if message["method"] != "service.hello":
                            break

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    return thread


@pytest.mark.parametrize(("recorders", "verified"), [([], True), ([{"sid": "s1", "alive": True}], False)])
def test_capture_off_against_an_older_service(service_home, capture_device, recorders, verified):
    """It cannot be asked to finish its recorders: none hosted is confirmed
    off; one hosted cannot be confirmed stopped (it stops at its next
    killswitch check)."""
    sock_path = paths.ensure_dirs()
    thread = _older_service(sock_path, recorders)
    try:
        result = capture.turn_off(capture.OffMode.DISABLE)
    finally:
        thread.join(5)
        with contextlib.suppress(OSError):
            os.unlink(sock_path)
    assert result.verified is verified, (result.summary(), result.warnings)
    if not verified:
        assert any("could not confirm" in w and "older" in w for w in result.warnings), result.warnings


@pytest.mark.parametrize(
    ("legacy", "raised"),
    [
        (FileNotFoundError, FileNotFoundError),
        (ConnectionRefusedError, FileNotFoundError),
        (TimeoutError, TimeoutError),
        (PermissionError, PermissionError),
    ],
)
def test_the_legacy_socket_says_no_service_only_when_it_has_none(service_home, monkeypatch, legacy, raised):
    """This machine's socket absent, the one a service from before the machine
    key listens at tried next: only absent or unlistened there too is "no
    service"; its timeout or a foreign folder is that, not a missing socket
    (Codex P2)."""

    def at(cls, path, timeout):
        if path == paths.socket_path():
            raise FileNotFoundError(str(path))
        raise legacy(str(path))

    monkeypatch.setattr(client.Connection, "_at", classmethod(at))
    with pytest.raises(OSError) as excinfo:
        client.Connection.open(0.2)
    assert type(excinfo.value) is raised


def test_capture_off_is_not_verified_when_a_legacy_service_times_out(service_home, capture_device, monkeypatch):
    legacy = paths.legacy_socket_path()
    paths.private_dir(legacy.parent)
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(str(legacy))
    real_at = client.Connection._at.__func__  # noqa: SLF001

    def at(cls, path, timeout):
        if path == legacy:
            raise TimeoutError("timed out")  # a running legacy service that did not take the connection
        return real_at(cls, path, timeout)

    monkeypatch.setattr(client.Connection, "_at", classmethod(at))
    try:
        result = capture.turn_off(capture.OffMode.DISABLE)
    finally:
        listener.close()
        with contextlib.suppress(OSError):
            os.unlink(legacy)
    assert result.verified is False and any("could not confirm" in w for w in result.warnings), result.warnings


def test_capture_off_with_no_service_is_what_it_was(capture_device):
    result = capture.turn_off(capture.OffMode.DISABLE)
    assert (result.service_answered, result.hosted_finished) == (False, [])
    assert result.verified and "Probe service" not in result.summary()


# -- probe exec -------------------------------------------------------------------------


@pytest.fixture
def updates(service_home, monkeypatch):
    """`test_service_updater.machine`: automatic updates on, a fake CLI
    interpreter, last checked an hour ago (not due, outside the cooldown)."""
    core = FakeCore(service_home.home)
    core.plan("update", steps=[{"event": STEP}])
    core.plan("version", stdout={"cli_version": probe.__version__})
    bin_dir = service_home.home / "bin"
    fake_open(bin_dir)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    enable_auto_update(service_home.home)
    last_checked(hours_ago=1)
    return core


#: A stand-in `probe exec`: holds its run for itself (as `service_calls.hold_run`
#: does), says so, releases it when told, and exits when its stdin closes.
_EXEC = (
    "import os, sys\n"
    "from probe.service import client\n"
    "owner = client.owner_of(os.getpid())\n"
    "print(client.hold_run(sys.argv[1], owner).get('held'), flush=True)\n"
    "if sys.stdin.readline().strip() == 'release':\n"
    "    client.release_run(sys.argv[1], owner)\n"
    "    print('released', flush=True)\n"
    "    sys.stdin.readline()\n"
)


class _Exec:
    def __init__(self, run: str) -> None:
        self.proc = subprocess.Popen(
            [sys.executable, "-c", _EXEC, run], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
        )
        assert self.proc.stdout.readline().strip() == "True"

    def release(self) -> None:
        self.proc.stdin.write("release\n")
        self.proc.stdin.flush()
        assert self.proc.stdout.readline().strip() == "released"

    def exit(self) -> None:
        with contextlib.suppress(OSError):
            self.proc.stdin.close()
        self.proc.wait(timeout=10)

    def kill(self) -> None:
        with contextlib.suppress(OSError):
            self.proc.kill()
        self.proc.wait(timeout=10)


@pytest.fixture
def exec_run():
    started: list[_Exec] = []

    def start(run: str) -> _Exec:
        started.append(_Exec(run))
        return started[-1]

    yield start
    for one in started:
        one.kill()


def test_a_held_run_defers_the_update_until_its_process_exits(service_home, updates, exec_run):
    """No run lock anywhere: the hold alone says a run is in flight. Its
    release does not let the update in while that `probe exec` still runs
    (still importing from the env an update replaces): its exit does."""
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        wrapper = exec_run("r-1")
        conn.call(Method.UPDATE_CHECK_NOW, {"trigger": "cli"})
        assert events_until(conn, lambda e: e["topic"] == "update.done", 20)[-1]["deferred"] == "run_in_flight"
        assert updates.calls("update") == []
        wrapper.release()
        assert conn.call(Method.STATUS)["runs"] == []
        time.sleep(updater.SESSION_END_RETRY_S + 2)
        assert updates.calls("update") == [], "updated under a `probe exec` that had not exited yet"
        wrapper.exit()
    # ... and the deferred update gets its retry, as after a session's end.
    assert wait_for(lambda: updates.calls("update"), 15), service_home.log()


def test_a_hold_whose_process_dies_goes_with_it(service_home, exec_run):
    service_home.start()
    wrapper = exec_run("r-1")
    assert [r["run"] for r in service_home.call(Method.STATUS)["runs"]] == ["r-1"]
    wrapper.kill()
    assert wait_for(lambda: service_home.call(Method.STATUS)["runs"] == [], 5), service_home.log()


def test_a_hold_is_kept_once_released_once_and_survives_a_restart(service_home, exec_run, agent):
    first = service_home.start()
    wrapper = exec_run("r-1")
    assert [r["run"] for r in service_home.call(Method.STATUS)["runs"]] == ["r-1"]
    service_home.call(Method.STOP)
    assert service_home.wait_exit(first["pid"], 5.0)
    assert (paths.service_dir() / runholds.RUNS_NAME).stat().st_mode & 0o777 == 0o600
    service_home.start()  # the next service picks it up from runs.json
    assert [r["run"] for r in service_home.call(Method.STATUS)["runs"]] == ["r-1"]
    wrapper.release()  # into the service it never spoke to
    assert service_home.call(Method.RUN_RELEASE, {"run": "r-1"}) == {"released": 0}
    assert service_home.call(Method.STATUS)["runs"] == []
    # A caller holds for itself (or a process it runs under), never for another.
    _, unrelated = agent
    assert service_home.call(Method.RUN_HOLD, {"run": "r-2", "owner": unrelated}) == {
        "held": False, "reason": "not_caller",
    }
    mine = client.owner_of(os.getpid())
    assert service_home.call(Method.RUN_HOLD, {"run": "r-3", "owner": mine}) == {"held": True}
    assert service_home.call(Method.RUN_HOLD, {"run": "r-3", "owner": mine}) == {"held": True}  # one hold
    assert [r["run"] for r in service_home.call(Method.STATUS)["runs"]] == ["r-3"]
    assert service_home.call(Method.RUN_RELEASE, {"run": "r-3", "owner": mine}) == {"released": 1}
    wrapper.exit()
    gone = {"pid": wrapper.proc.pid, "start_time": "1"}
    assert service_home.call(Method.RUN_HOLD, {"run": "r-4", "owner": gone}) == {"held": False, "reason": "owner_gone"}


def test_a_released_owner_still_holds_the_update_off_until_it_exits(service_home, updates, exec_run, agent):
    """A retry another session's end armed must not update under a `probe
    exec` that released its run and is still cleaning up (Codex P2)."""
    _, owner = agent
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        wrapper = exec_run("r-1")
        conn.call(Method.UPDATE_CHECK_NOW, {"trigger": "cli"})
        assert events_until(conn, lambda e: e["topic"] == "update.done", 20)[-1]["deferred"] == "run_in_flight"
        wrapper.release()
        # Another session ends: its retry comes SESSION_END_RETRY_S later.
        conn.call(Method.SESSION_REGISTER, {"sid": "s-x", "harness": "codex", "mode": Mode.INLINE,
                                            "owner": owner, "generation": 1})
        conn.call(Method.SESSION_END, {"sid": "s-x", "generation": 1})
        time.sleep(updater.SESSION_END_RETRY_S + 2)
        assert updates.calls("update") == [], "updated under a released `probe exec` still running"
        wrapper.exit()
    assert wait_for(lambda: updates.calls("update"), 15), service_home.log()


def test_a_released_owner_still_holds_the_update_off_across_a_restart(service_home, updates, exec_run):
    """Released, then the service restarts before that `probe exec` exits:
    the next service must still not update under its cleanup (Codex P2)."""
    first = service_home.start()
    wrapper = exec_run("r-1")
    wrapper.release()
    service_home.call(Method.STOP)
    assert service_home.wait_exit(first["pid"], 5.0)
    service_home.start()
    assert service_home.call(Method.STATUS)["runs"] == []  # released: not listed
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": UPDATE_TOPICS})
        conn.call(Method.UPDATE_CHECK_NOW, {"trigger": "cli"})
        assert events_until(conn, lambda e: e["topic"] == "update.done", 20)[-1]["deferred"] == "run_in_flight"
        assert updates.calls("update") == []
        wrapper.exit()
    assert wait_for(lambda: updates.calls("update"), 15), service_home.log()


def test_only_the_holder_or_a_process_it_runs_under_releases_a_hold(service_home, exec_run):
    """Run ids are in `probe status`: anyone could name one (Codex P1)."""
    service_home.start()
    wrapper = exec_run("r-1")
    # This process is the wrapper's parent, not the wrapper nor one it runs under.
    assert service_home.call(Method.RUN_RELEASE, {"run": "r-1"}) == {"released": 0}
    named = {"pid": wrapper.proc.pid, "start_time": client.owner_of(wrapper.proc.pid)["start_time"]}
    assert service_home.call(Method.RUN_RELEASE, {"run": "r-1", "owner": named}) == {"released": 0}
    assert [r["run"] for r in service_home.call(Method.STATUS)["runs"]] == ["r-1"]
    wrapper.release()
    assert service_home.call(Method.STATUS)["runs"] == []


def test_a_hold_taken_while_the_files_are_scanned_is_seen(monkeypatch):
    """`run_held` read before the scan's await missed a hold the service took
    meanwhile, and the update went ahead in place (Codex P1)."""
    held = {"now": False}

    def scanning(**_kwargs):
        held["now"] = True  # a `probe exec` holds its run while the scan runs
        return updater.Busy()

    monkeypatch.setattr(updater, "look", scanning)
    up = updater.Updater(
        version="1", emit=lambda *a: None, changed=lambda: None, stop=lambda r: None,
        action_running=lambda: False, discovering=lambda: False, run_held=lambda: held["now"],
    )
    assert asyncio.run(up._look_off_loop()).reasons() == ["run_in_flight"]  # noqa: SLF001


def test_a_hold_while_an_update_is_applied_is_refused(tmp_path, monkeypatch):
    """Admission and the update's last check are one step on the loop: a hold
    the update child could no longer see is refused, never acknowledged (the
    run's lock and the update barrier are what it has then) (Codex P1)."""
    from probe.service import server
    from probe.service.registry import Registry

    monkeypatch.setattr(updater, "_hosted_live", updater._hosted_live)  # noqa: SLF001 -- Service sets it
    service = server.Service(registry=Registry(tmp_path / "sessions.json"))
    service.updater.applying = True
    conn = server.Connection(None, peer_pid=os.getpid())
    answer = asyncio.run(service._run_hold(conn, {"run": "r-1", "owner": client.owner_of(os.getpid())}))  # noqa: SLF001
    assert answer == {"held": False, "reason": "updating"}
    assert not service.runs.live()


class _Ctx:
    def __init__(self, args: list[str]) -> None:
        self.args = args


class _Result:
    returncode = 0


def test_exec_holds_its_run_and_releases_it_before_the_update_check(monkeypatch):
    order: list[tuple] = []
    owner = {"pid": os.getpid(), "start_time": "x"}
    monkeypatch.setattr(service_calls, "hold_run", lambda run_id: order.append(("hold", run_id)) or owner)
    monkeypatch.setattr(service_calls, "release_run", lambda run_id, who: order.append(("release", run_id, who)))
    monkeypatch.setattr(cli_main, "_apply_deferred_update", lambda: order.append(("apply",)))
    monkeypatch.setattr(cli_main, "_client", lambda *a, **k: contextlib.nullcontext(object()))

    class _Handle:
        id = "run-uuid"

        def execute(self, *_a, **_k):
            order.append(("execute",))
            return _Result()

    monkeypatch.setattr(cli_main, "_run_handle", lambda *_a, **_k: _Handle())
    import typer

    with pytest.raises(typer.Exit):
        cli_main.exec(_Ctx(["--", "true"]), run="r1", cwd=None)
    assert order == [("hold", "run-uuid"), ("execute",), ("release", "run-uuid", owner), ("apply",)]


def test_exec_with_no_service_runs_as_before(monkeypatch):
    """No service answers (this suite's HOME has none): no hold, no release."""
    released: list = []
    monkeypatch.setattr(service_calls, "release_run", lambda *a: released.append(a))
    monkeypatch.setattr(cli_main, "_apply_deferred_update", lambda: None)
    monkeypatch.setattr(cli_main, "_client", lambda *a, **k: contextlib.nullcontext(object()))

    class _Handle:
        id = "run-uuid"

        def execute(self, *_a, **_k):
            return _Result()

    monkeypatch.setattr(cli_main, "_run_handle", lambda *_a, **_k: _Handle())
    import typer

    with pytest.raises(typer.Exit) as excinfo:
        cli_main.exec(_Ctx(["--", "true"]), run="r1", cwd=None)
    assert excinfo.value.exit_code == 0 and released == []
    assert service_calls.hold_run("run-uuid") is None


# -- the manifest ---------------------------------------------------------------------------


@pytest.fixture
def no_spawn(monkeypatch):
    spawned: list = []
    monkeypatch.setattr(cli_main, "_spawn_detached", lambda argv, env: spawned.append(argv))
    monkeypatch.delenv("PROBE_VERSION_CACHE", raising=False)
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    return spawned


def test_a_stale_manifest_is_refreshed_by_one_child_of_the_service(service_home, no_spawn, monkeypatch):
    core = FakeCore(service_home.home)
    gate = service_home.home / "gate"
    answer = {"cli_version": "1.0.0", "cli_latest": "9.9.9", "ok": True, "fetched_at": 1234}
    core.plan("version", before=[{"wait": str(gate)}], stdout=answer)
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.test:3128")
    service_home.start()

    began = time.monotonic()
    cli_main._spawn_version_refresh()
    assert time.monotonic() - began < 2.0, "the command must not wait for the fetch"
    assert no_spawn == [], "a service answered: no detached refresher"
    assert wait_for(lambda: core.calls("version"), 10), service_home.log()
    (call,) = core.calls("version")
    assert json.loads(call["stdin"]) == {"refresh": True}
    # The caller's own network settings and folders reach the child.
    assert call["env"]["HTTPS_PROXY"] == "http://proxy.test:3128"
    assert call["env"]["XDG_CONFIG_HOME"] == os.environ["XDG_CONFIG_HOME"]

    context = service_calls.manifest_context()
    assert client.refresh_manifest(context)["outcome"] == CheckOutcome.RUNNING  # joins the one in flight
    gate.touch()
    done = client.refresh_manifest(context, wait=10)
    assert done["outcome"] in (CheckOutcome.RUNNING, CheckOutcome.RECENT) and done["done"] is True
    assert done["result"] == {"ok": True, "fetched_at": 1234, "cli_latest": "9.9.9", "exit_code": 0}
    assert client.refresh_manifest(context)["outcome"] == CheckOutcome.RECENT  # within the cooldown
    assert len(core.calls("version")) == 1


def test_no_service_or_a_context_it_refuses_spawns_the_refresher_as_before(service_home, no_spawn, monkeypatch):
    cli_main._spawn_version_refresh()  # no service runs
    assert len(no_spawn) == 1 and "probe.cli.version_refresh" in no_spawn[0]
    version_policy.release_refresh()
    service_home.start()
    # The service runs children only for an https endpoint this machine signed in to.
    monkeypatch.setenv("PROBE_BASE_URL", "http://127.0.0.1:9")
    cli_main._spawn_version_refresh()
    assert len(no_spawn) == 2
    version_policy.release_refresh()
    monkeypatch.delenv("PROBE_BASE_URL")
    # A cache the service cannot be told about.
    monkeypatch.setenv("PROBE_VERSION_CACHE", str(service_home.home / "elsewhere.json"))
    cli_main._spawn_version_refresh()
    assert len(no_spawn) == 3


def test_a_service_refresh_that_did_not_land_leaves_the_refresh_to_the_cli(service_home, no_spawn):
    """An older core refuses `{"refresh": true}` (exit 2, no answer): the cache
    stays stale, the service answers `recent` for its cooldown, and the CLI
    then refreshes it itself instead of going without (critic finding)."""
    core = FakeCore(service_home.home)
    core.plan("version", stdout=None, exit=2)
    service_home.start()
    cli_main._spawn_version_refresh()
    assert no_spawn == []
    context = service_calls.manifest_context()
    done = client.refresh_manifest(context, wait=10)
    assert done["done"] is True and done["result"]["ok"] is False and done["result"]["exit_code"] == 2
    assert "error" in done["result"]
    version_policy.release_refresh()  # this process's claim, as if it had aged out
    cli_main._spawn_version_refresh()
    assert client.refresh_manifest(context)["outcome"] == CheckOutcome.RECENT
    assert len(no_spawn) == 1 and len(core.calls("version")) == 1


_SANDBOXED = (
    "import ctypes, json, sys\n"
    "assert ctypes.CDLL(None, use_errno=True).prctl(38, 1, 0, 0, 0) == 0  # PR_SET_NO_NEW_PRIVS\n"
    "import os\n"
    "from probe.service import client\n"
    "params = json.loads(sys.argv[2])\n"
    "if params.get('owner') == 'self':\n"
    "    params['owner'] = client.owner_of(os.getpid())\n"
    "try:\n"
    "    print(json.dumps({'answered': client.call(sys.argv[1], params, client_version='t')}))\n"
    "except client.ServiceError as exc:\n"
    "    print(json.dumps({'code': exc.code, 'data': exc.data}))\n"
)


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="no_new_privs is Linux's")
@pytest.mark.parametrize(
    ("method", "params"),
    [
        (Method.MANIFEST_REFRESH, {}),
        (Method.RECORDERS_FINISH, {"harness": "claude_code"}),
        (Method.RUN_HOLD, {"run": "r-1", "owner": "self"}),
        (Method.RUN_RELEASE, {"run": "r-1"}),
    ],
)
def test_a_caller_in_a_sandbox_is_refused(service_home, method, params):
    """Its refresh child would fetch and write outside the sandbox, with the
    config and cache folders it named; a recorder it stops is outside it too;
    a hold it took would persist outside it and keep updates off, and one it
    released would be another's (Codex P1, P2)."""
    service_home.start()
    done = subprocess.run(
        [sys.executable, "-c", _SANDBOXED, method, json.dumps(params)], capture_output=True, text=True,
        timeout=30, env=os.environ.copy(),
    )
    assert json.loads(done.stdout) == {"code": -32012, "data": {"reason": "sandboxed"}}, done.stderr


class _Manifest(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 -- the stdlib's name
        body = json.dumps({"cli": {"latest": "9.9.9", "min": "0.0.1"}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        pass


def _core_version(tmp_path: Path, base: str) -> subprocess.CompletedProcess:
    env = {
        **os.environ,
        "HOME": str(tmp_path),
        "PROBE_BASE_URL": base,
        "PROBE_VERSION_CACHE": str(tmp_path / "cache.json"),
        "PROBE_TELEMETRY": "off",
    }
    return subprocess.run(
        [sys.executable, "-I", "-m", "probe.core.run", "version"],
        input='{"refresh": true}', capture_output=True, text=True, env=env, timeout=60,
    )


def test_core_version_refresh_writes_the_cache_as_the_clis_refresher(tmp_path):
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Manifest)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        done = _core_version(tmp_path, f"http://127.0.0.1:{server.server_address[1]}")
    finally:
        server.shutdown()
    assert done.returncode == 0, done.stderr
    answer = json.loads(done.stdout)
    assert answer["cli_latest"] == "9.9.9" and answer["ok"] is True and isinstance(answer["fetched_at"], int)
    cached = json.loads((tmp_path / "cache.json").read_text())
    assert cached["ok"] is True and cached["manifest"]["cli"]["latest"] == "9.9.9"


def test_core_version_refresh_records_a_failed_fetch_and_says_so(tmp_path):
    done = _core_version(tmp_path, "http://127.0.0.1:9")
    assert done.returncode == 0, done.stderr
    answer = json.loads(done.stdout)
    assert answer["ok"] is False and answer["cli_latest"] is None
    assert json.loads((tmp_path / "cache.json").read_text())["ok"] is False  # the back-off, as the CLI's


# -- units -------------------------------------------------------------------------------


def test_run_holds_load_only_live_owners(tmp_path):
    path = tmp_path / runholds.RUNS_NAME
    alive = {(10, "a"): True, (11, "b"): False}
    holds = runholds.RunHolds(path, owner_alive=lambda pid, start: alive.get((pid, start)))
    assert holds.add("r-1", {"pid": 10, "start_time": "a"})[1] is True
    assert holds.add("r-1", {"pid": 10, "start_time": "a"})[1] is False
    holds.add("r-2", {"pid": 11, "start_time": "b"})
    again = runholds.RunHolds(path, owner_alive=lambda pid, start: alive.get((pid, start)))
    (loaded,) = again.load()
    assert loaded.run == "r-1"
    assert again.release("r-1", {(99, "x")}) == []  # not the caller's
    assert again.release("r-1", {(10, "a")}, pid=99) == []
    assert again.release("r-1", {(10, "a")}) == [loaded]
    assert again.public() == [] and again.live()  # unlisted, still busy until its process exits
    assert again.drop(loaded) and not again.live()


def test_a_released_hold_is_saved_until_its_process_exits(tmp_path):
    path = tmp_path / runholds.RUNS_NAME
    holds = runholds.RunHolds(path, owner_alive=lambda pid, start: True)
    hold, _ = holds.add("r-1", {"pid": 10, "start_time": "a"})
    holds.release("r-1", {(10, "a")})
    again = runholds.RunHolds(path, owner_alive=lambda pid, start: True)
    (loaded,) = again.load()
    assert again.live() and again.public() == [], "a restarted service must still hold updates off"
    assert again.drop(loaded) and not again.live()
    assert runholds.RunHolds(path).load() == [], "gone once its process exited"


def test_run_holds_refuse_past_the_limit_never_dropping_one(tmp_path, monkeypatch):
    monkeypatch.setattr(runholds, "MAX_HOLDS", 1)
    holds = runholds.RunHolds(tmp_path / runholds.RUNS_NAME)
    assert holds.add("r-1", {"pid": 10, "start_time": "a"})[0] is not None
    assert holds.add("r-2", {"pid": 11, "start_time": "b"}) == (None, False)
    assert [h["run"] for h in holds.public()] == ["r-1"]


def test_released_holds_count_toward_the_limit_and_a_restart_keeps_every_hold(tmp_path, monkeypatch):
    """Codex review of 573c4ed99: a released owner still running took no room,
    so more than MAX_HOLDS could be saved and a restart dropped the rest."""
    monkeypatch.setattr(runholds, "MAX_HOLDS", 1)
    path = tmp_path / runholds.RUNS_NAME
    holds = runholds.RunHolds(path, owner_alive=lambda pid, start: True)
    assert holds.add("r-1", {"pid": 10, "start_time": "a"})[0] is not None
    holds.release("r-1", {(10, "a")})
    assert holds.add("r-2", {"pid": 11, "start_time": "b"}) == (None, False), "the released owner still runs"
    assert holds.add("r-1", {"pid": 10, "start_time": "a"})[0] is not None, "holding the same run again fits"
    # A file written before the combined limit, with more than it allows: all kept.
    import json
    data = json.loads(path.read_text())
    data["holds"].append({**data["holds"][0], "run": "r-9", "owner": {"pid": 12, "start_time": "c"},
                          "released": True})
    path.write_text(json.dumps(data))
    again = runholds.RunHolds(path, owner_alive=lambda pid, start: True)
    assert len(again.load()) == 2


def test_the_quiet_check_reads_a_hold_without_scanning_lock_files(monkeypatch):
    from probe._shared import run_lock

    def scanned(*_a, **_k):
        raise AssertionError("a held run needs no lock-file scan")

    monkeypatch.setattr(run_lock, "any_live", scanned)
    assert updater.look(action_running=False, run_held=True).run is True
    held = updater.Updater(
        version="1", emit=lambda *a: None, changed=lambda: None, stop=lambda r: None,
        action_running=lambda: False, discovering=lambda: False, run_held=lambda: True,
    )
    assert held._look().reasons() == ["run_in_flight"]  # noqa: SLF001


def test_the_refresher_runs_one_child_per_context_and_reports_a_failure(monkeypatch):
    runs: list = []
    gate = asyncio.Event()

    async def run_read(action, request, *, env_extra, timeout):
        runs.append((action, request, env_extra))
        await gate.wait()
        if env_extra.get("X") == "fail":
            raise OSError("no python")
        return 0, {"ok": True, "fetched_at": 5, "cli_latest": "2.0.0"}

    monkeypatch.setattr(manifest.children, "run_read", run_read)

    async def scenario():
        changes: list = []
        refresher = manifest.ManifestRefresher(changed=lambda: changes.append(refresher.in_flight()))
        first = await refresher.refresh({"X": "a"})
        second = await refresher.refresh({"X": "a"})
        failing = await refresher.refresh({"X": "fail"})
        assert refresher.in_flight()
        gate.set()
        done = await refresher.refresh({"X": "a"}, wait=2)
        failed = await refresher.refresh({"X": "fail"}, wait=2)
        await asyncio.sleep(0.05)  # each refresh's last `changed` is called soon after it ends
        return first, second, failing, done, failed, refresher, changes

    first, second, failing, done, failed, refresher, changes = asyncio.run(scenario())
    assert (first["outcome"], second["outcome"], failing["outcome"]) == ("started", "running", "started")
    assert done["done"] is True and done["result"]["cli_latest"] == "2.0.0"
    assert failed["result"]["ok"] is False and "could not start" in failed["result"]["error"]
    assert len(runs) == 2 and runs[0][:2] == ("version", {"refresh": True})
    assert not refresher.in_flight() and changes[-1] is False


def test_doctor_lists_a_few_and_counts_the_rest():
    view = service_calls._filled(  # noqa: SLF001
        {
            "service_version": "1.2.3", "pid": 42, "state": "running", "started_at": 0,
            "recorders": [{"sid": f"session-{i:02d}-long-id", "alive": True, "last": "", "failures": 0}
                          for i in range(7)],
            "update": {"enabled": True, "in_progress": False, "last_check": 0, "last_result": {"ok": False},
                       "next_check": 10, "deferred": {"at": 0, "reason": "run_in_flight"}, "deferred_since": 0},
        },
        {"sessions": []},
    )
    rows = doctor.service_rows(view)
    assert sum("recording" in r for r in rows) == doctor.SERVICE_ROWS_SHOWN
    assert any("+2 more" in r for r in rows)
    assert any("Update deferred" in r and "run_in_flight" in r for r in rows)
    assert any("(failed)" in r for r in rows)
    assert "update deferred: run_in_flight" in service_calls.summary(view)
