"""The Probe service records sessions itself (plan A2, D2, D3, D39).

A real service process; a stand-in tap package (its `tap.hosted.record`
writes what it was given and waits for its stop or pause) so these pin the
service's half: `session.record` registers and records, `session.finish`
waits for the end, a newer tap restarts the service onto it, a stop pauses
every recorder and the next service resumes them, a failing recorder is tried
again, a session without a known agent is left to `tap watch`, and the
service stays up while a recorder finishes.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from probe.service import client, paths, recorders
from probe.service.protocol import Method
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the service is POSIX-only until R3")

_HOSTED = '''
import json, os, threading, time
from dataclasses import dataclass, field

ENDED, PAUSED, STOPPED, FAILED = "ended", "paused", "stopped", "failed"


@dataclass
class Controls:
    stop: threading.Event = field(default_factory=threading.Event)
    pause: threading.Event = field(default_factory=threading.Event)


def _note(session, event):
    with open(os.path.join(os.environ["HOME"], "recorded.jsonl"), "a") as handle:
        handle.write(json.dumps({"event": event, "sid": session["sid"], "version": __import__("tap").__version__,
                                 "env": session["env"].get("PROBE_TEST_MARK"), "thread_env": os.environ.get("PROBE_TEST_MARK"),
                                 "transcript": session.get("transcript")}) + "\\n")


def record(session, controls):
    from tap import threadenv
    with threadenv.install().session(session["env"]):
        _note(session, "started")
        behaviour = session["env"].get("PROBE_TEST_BEHAVIOUR", "")
        if behaviour == "fail" :
            marker = os.path.join(os.environ["HOME"], "failed-" + session["sid"])
            if not os.path.exists(marker):
                open(marker, "w").close()
                _note(session, "failing")
                return FAILED, "boom"
        while True:
            if controls.stop.wait(0.05):
                time.sleep(float(session["env"].get("PROBE_TEST_FINISH_S", "0.2")))
                _note(session, "ended")
                return ENDED, ""
            if controls.pause.is_set():
                _note(session, "paused")
                return PAUSED, ""
'''

_THREADENV = (Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap" / "tap" / "threadenv.py").read_text()


def _tap(root: Path, version: str) -> Path:
    tap = root / "tap"
    tap.mkdir(parents=True)
    (tap / "__init__.py").write_text(f'__version__ = "{version}"\n')
    (tap / "main.py").write_text("")
    (tap / "hosted.py").write_text(_HOSTED)
    (tap / "threadenv.py").write_text(_THREADENV)
    return root


def _params(sid: str, owner: dict | None, root: Path, version: str, tmp: Path, **env) -> dict:
    return {
        "sid": sid, "harness": "claude_code", "mode": "inline", "owner": owner, "generation": 1,
        "state_dir": str(tmp / "state"), "cwd": str(tmp), "transcript": str(tmp / f"{sid}.jsonl"),
        "transcript_dir": None, "tap_root": str(root), "tap_version": version,
        "env": {"HOME": os.environ["HOME"], "PROBE_TEST_MARK": sid, **env},
    }


def _events(home: Path, sid: str | None = None) -> list[dict]:
    try:
        lines = (home / "recorded.jsonl").read_text().splitlines()
    except OSError:
        return []
    found = [json.loads(line) for line in lines]
    return [e for e in found if sid is None or e["sid"] == sid]


def _saw(home: Path, sid: str, event: str, count: int = 1, timeout: float = 5.0) -> bool:
    return bool(wait_for(lambda: sum(e["event"] == event for e in _events(home, sid)) >= count, timeout))


@pytest.fixture
def agent():
    proc, owner = spawn_agent()
    yield proc, owner
    kill_agent(proc)


def test_a_session_is_registered_recorded_and_finished(service_home, agent, tmp_path):
    proc, owner = agent
    root = _tap(tmp_path / "tap-a", "0.10.0")
    service_home.start()
    answer = service_home.call(Method.SESSION_RECORD, _params("s1", owner, root, "0.10.0", tmp_path))
    assert answer["recording"] is True and answer["started"] is True and answer["pid"] > 1
    assert _saw(service_home.home, "s1", "started")
    seen = _events(service_home.home, "s1")[0]
    # Its own environment, on its own thread; never the service's.
    assert seen["thread_env"] == "s1" and seen["transcript"] == str(tmp_path / "s1.jsonl")
    assert [s["sid"] for s in service_home.call(Method.SESSION_LIST)["sessions"]] == ["s1"]
    assert service_home.call(Method.SESSION_RECORDING, {"sid": "s1"}) == {"recording": True}
    status = service_home.call(Method.STATUS)
    assert [r["sid"] for r in status["recorders"]] == ["s1"]
    # Again (each prompt's check): the same recorder, not a second one.
    again = service_home.call(Method.SESSION_RECORD, _params("s1", owner, root, "0.10.0", tmp_path))
    assert again["recording"] is True and again["started"] is False
    finished = service_home.call(Method.SESSION_FINISH, {"sid": "s1", "wait": 5})
    assert finished == {"recording": True, "finished": True}
    assert [e["event"] for e in _events(service_home.home, "s1")] == ["started", "ended"]
    assert wait_for(lambda: service_home.call(Method.SESSION_RECORDING, {"sid": "s1"}) == {"recording": False}, 3)


def test_finish_says_when_the_last_pass_outlasted_the_wait(service_home, agent, tmp_path):
    proc, owner = agent
    root = _tap(tmp_path / "tap-a", "0.10.0")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, _params("s1", owner, root, "0.10.0", tmp_path, PROBE_TEST_FINISH_S="2"))
    assert _saw(service_home.home, "s1", "started")
    assert service_home.call(Method.SESSION_FINISH, {"sid": "s1", "wait": 0.2}) == {"recording": True, "finished": False}
    assert _saw(service_home.home, "s1", "ended")
    assert service_home.call(Method.SESSION_FINISH, {"sid": "nosuch", "wait": 1}) == {"recording": False, "finished": False}


def test_a_session_without_a_known_agent_is_left_to_tap_watch(service_home, tmp_path):
    root = _tap(tmp_path / "tap-a", "0.10.0")
    service_home.start()
    answer = service_home.call(Method.SESSION_RECORD, _params("s1", None, root, "0.10.0", tmp_path))
    assert answer == {"recording": False, "reason": "no_owner"}
    assert service_home.call(Method.SESSION_LIST)["sessions"] == []


def test_a_folder_without_a_tap_is_left_to_tap_watch(service_home, agent, tmp_path):
    proc, owner = agent
    service_home.start()
    answer = service_home.call(Method.SESSION_RECORD, _params("s1", owner, tmp_path / "nothing", "0.10.0", tmp_path))
    assert answer == {"recording": False, "reason": "no_tap"}


def test_a_newer_tap_restarts_the_service_onto_it(service_home, agent, tmp_path):
    proc, owner = agent
    old = _tap(tmp_path / "tap-old", "0.10.0")
    new = _tap(tmp_path / "tap-new", "0.10.1")
    first = service_home.start()
    assert service_home.call(Method.SESSION_RECORD, _params("s1", owner, old, "0.10.0", tmp_path))["recording"]
    assert _saw(service_home.home, "s1", "started")
    answer = service_home.call(Method.SESSION_RECORD, _params("s2", owner, new, "0.10.1", tmp_path))
    assert answer == {"recording": False, "restart": True}
    assert service_home.wait_exit(first["pid"], 8), service_home.log()
    # A restart on purpose is no start to back off from (client.forget_start).
    assert first["pid"] not in [e.get("pid") for e in json.loads(paths.starts_path().read_text())["starts"]]
    # The recorder paused (no end: the session goes on) ...
    assert [e["event"] for e in _events(service_home.home, "s1")] == ["started", "paused"]
    # ... and the next service, started by the tap's next ask, loads the newer tap first.
    second = service_home.start()
    assert second["pid"] != first["pid"]
    answer = service_home.call(Method.SESSION_RECORD, _params("s2", owner, new, "0.10.1", tmp_path))
    assert answer["recording"] is True
    assert _saw(service_home.home, "s1", "started", count=2)
    assert _saw(service_home.home, "s2", "started")
    assert {e["version"] for e in _events(service_home.home) if e["event"] == "started"} == {"0.10.0", "0.10.1"}
    assert _events(service_home.home, "s1")[-1]["version"] == "0.10.1", "s1 resumed on the newer tap"


def test_a_newer_tap_that_cannot_load_restarts_the_service_once(service_home, agent, tmp_path):
    """A restart on purpose is no start to back off from, so a newer tap the
    service cannot import would restart it at every ask of that session: it
    is tried once, and then that session's own tap records it."""
    proc, owner = agent
    old = _tap(tmp_path / "tap-old", "0.10.0")
    broken = _tap(tmp_path / "tap-new", "0.10.1")
    (broken / "tap" / "main.py").write_text("raise ImportError('a tap this service cannot run')\n")
    first = service_home.start()
    assert service_home.call(Method.SESSION_RECORD, _params("s1", owner, old, "0.10.0", tmp_path))["recording"]
    assert service_home.call(Method.SESSION_RECORD, _params("s2", owner, broken, "0.10.1", tmp_path)) == \
        {"recording": False, "restart": True}
    assert service_home.wait_exit(first["pid"], 8), service_home.log()
    second = service_home.start()
    assert _saw(service_home.home, "s1", "started", count=2), service_home.log()
    answer = service_home.call(Method.SESSION_RECORD, _params("s2", owner, broken, "0.10.1", tmp_path))
    assert answer == {"recording": False, "reason": "tap_unloadable"}, answer
    assert service_home.status()["pid"] == second["pid"], "no second restart"
    assert _events(service_home.home, "s1")[-1]["version"] == "0.10.0", "s1 records on the tap that loads"


def test_a_stopped_service_pauses_and_the_next_one_resumes(service_home, agent, tmp_path):
    proc, owner = agent
    root = _tap(tmp_path / "tap-a", "0.10.0")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, _params("s1", owner, root, "0.10.0", tmp_path))
    assert _saw(service_home.home, "s1", "started")
    saved = json.loads((paths.service_dir() / recorders.RECORDERS_NAME).read_text())
    assert [s["sid"] for s in saved["sessions"]] == ["s1"]
    assert oct((paths.service_dir() / recorders.RECORDERS_NAME).stat().st_mode & 0o777) == "0o600"
    service_home.call(Method.STOP)
    assert service_home.wait_exit(first["pid"], 8)
    assert [e["event"] for e in _events(service_home.home, "s1")] == ["started", "paused"]
    service_home.start()
    assert _saw(service_home.home, "s1", "started", count=2), service_home.log()
    assert service_home.call(Method.SESSION_RECORDING, {"sid": "s1"}) == {"recording": True}
    assert [s["sid"] for s in service_home.call(Method.SESSION_LIST)["sessions"]] == ["s1"]


def test_a_failed_recorder_is_tried_again(service_home, agent, tmp_path, monkeypatch):
    monkeypatch.setenv(recorders.RETRY_ENV, "0.2")
    proc, owner = agent
    root = _tap(tmp_path / "tap-a", "0.10.0")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, _params("s1", owner, root, "0.10.0", tmp_path, PROBE_TEST_BEHAVIOUR="fail"))
    assert _saw(service_home.home, "s1", "started", count=2), service_home.log()
    assert [e["event"] for e in _events(service_home.home, "s1")][:3] == ["started", "failing", "started"]
    status = service_home.call(Method.STATUS)
    assert status["recorders"][0]["failures"] == 1


def test_the_service_stays_while_a_recorder_finishes(service_home, agent, tmp_path, monkeypatch):
    """The agent exited (its registration ends with it) but its recorder is
    still on its last pass: the service waits for it, then goes idle."""
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "0.5")
    proc, owner = agent
    root = _tap(tmp_path / "tap-a", "0.10.0")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, _params("s1", owner, root, "0.10.0", tmp_path))
    assert _saw(service_home.home, "s1", "started")
    kill_agent(proc)
    assert wait_for(lambda: service_home.call(Method.SESSION_LIST)["sessions"] == [], 5)
    status = service_home.call(Method.STATUS)
    assert status["state"] == "running", "a recorder still runs"
    service_home.call(Method.SESSION_FINISH, {"sid": "s1", "wait": 5})
    assert service_home.wait_exit(status["pid"], 8), "idle once the recorder finished"


def test_the_tap_client_falls_back_when_the_service_cannot_record(service_home, tmp_path, monkeypatch):
    """`tap record` against a real service: no owner record, so the service
    says no and the hook starts `tap watch` (exit 1, no marker)."""
    tap_root = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap"
    env = {**os.environ, "PROBE_TAP_HOSTED": "1", "PYTHONPATH": str(tap_root),
           "PROBE_RESEARCH_TAP_PLUGIN_DIR": str(tmp_path / "plugin")}
    service_home.start()
    sid = "00000000-0000-4000-8000-00000000a2a2"
    done = subprocess.run(
        [sys.executable, "-m", "tap", "record", "--session-id", sid, "--cwd", str(tmp_path),
         "--transcript", str(tmp_path / "t.jsonl"), "--plugin-root", str(tap_root)],
        env=env, capture_output=True, text=True, timeout=20, check=False,
    )
    assert done.returncode == 1, done.stderr
    assert not Path(f"/tmp/probe-research-tap-watcher-{sid}.hosted").exists()


def test_a_worker_the_services_recorder_started_is_a_live_sessions(monkeypatch):
    """The updater's draining check (D7): a worker whose parent is this
    service is draining only once its session is no longer recorded here."""
    from probe.service import updater

    child = subprocess.Popen(["sleep", "30"])
    try:
        recorded = {"s1"}
        monkeypatch.setattr(updater, "_hosted_live", lambda sid: sid in recorded)
        assert updater._session_ended(child.pid, "s1") is False
        recorded.clear()
        assert updater._session_ended(child.pid, "s1") is True
        monkeypatch.setattr(updater, "_hosted_live", None)
        assert updater._session_ended(child.pid, "s1") is True
    finally:
        child.kill()
        child.wait()


def test_the_client_side_knows_the_methods():
    from probe.service import protocol

    assert {Method.SESSION_RECORD, Method.SESSION_RECORDING, Method.SESSION_FINISH} <= protocol.METHODS
    assert recorders.RETRY_ENV in client.ENV_ALLOWLIST


def test_a_caller_in_a_sandbox_is_left_to_tap_watch(service_home, agent, tmp_path):
    """Its recorder would run outside the sandbox with the PATH it sent."""
    if not sys.platform.startswith("linux"):
        pytest.skip("no-new-privs is Linux's")
    proc, owner = agent
    root = _tap(tmp_path / "tap-a", "0.10.0")
    service_home.start()
    script = (
        "import ctypes, json, sys\n"
        "assert ctypes.CDLL(None, use_errno=True).prctl(38, 1, 0, 0, 0) == 0\n"
        "from probe.service import client\n"
        "from probe.service.protocol import Client\n"
        "print(json.dumps(client.call('session.record', json.loads(sys.argv[1]), client=Client.TAP, client_version='t')))\n"
    )
    params = _params("s1", owner, root, "0.10.0", tmp_path)
    done = subprocess.run([sys.executable, "-c", script, json.dumps(params)], capture_output=True, text=True,
                          timeout=20, env=os.environ.copy())
    assert json.loads(done.stdout) == {"recording": False, "reason": "sandboxed"}, done.stderr
    assert service_home.call(Method.SESSION_LIST)["sessions"] == []


def test_a_restart_asks_each_sessions_worker_to_hand_over(tmp_path, monkeypatch):
    """The service is a hosted session's worker's parent: at its restart the
    worker would see its parent gone and end the session (fail the writer
    requests waiting, release its lease). Asked to hand over, dated ahead, it
    hands over to the next service's worker instead (critic R2 P1)."""
    import asyncio
    import fcntl
    import time as _time

    host = recorders.RecorderHost(log=lambda m: None, loop_getter=lambda: None)
    state = tmp_path / "state"
    (state / "daemon").mkdir(parents=True)
    lock = state / "daemon" / "s1.lock"
    held = open(lock, "a")  # noqa: SIM115 -- a live worker holds its lock
    fcntl.flock(held.fileno(), fcntl.LOCK_EX)

    class Controls:
        def __init__(self):
            import threading

            self.stop, self.pause = threading.Event(), threading.Event()

    try:
        live = recorders.Recording("s1", {"sid": "s1", "state_dir": str(state)}, Controls())
        ending = recorders.Recording("s2", {"sid": "s2", "state_dir": str(state)}, Controls())
        ending.controls.stop.set()
        host.recordings = {"s1": live, "s2": ending}
        monkeypatch.setattr(host, "_save", lambda: None)
        asyncio.run(host.close())
        marker = state / "daemon" / "s1.handover"
        assert marker.stat().st_mtime > _time.time() + recorders.HANDOVER_AHEAD_S - 30
        assert live.controls.pause.is_set()
        assert not ending.controls.pause.is_set(), "a finishing session finishes, never paused"
        assert not (state / "daemon" / "s2.handover").exists()
    finally:
        held.close()


def test_a_recorded_session_asked_again_keeps_its_links_registration(service_home, agent, tmp_path):
    """A second SessionStart (a resume, a compaction, the prompt check) must
    not register a new generation over the one its link holds (critic R2)."""
    proc, owner = agent
    root = _tap(tmp_path / "tap-a", "0.10.0")
    service_home.start()
    first = _params("s1", owner, root, "0.10.0", tmp_path)
    service_home.call(Method.SESSION_RECORD, first)
    (listed,) = service_home.call(Method.SESSION_LIST)["sessions"]
    again = {**first, "generation": first["generation"] + 1000, "mode": "daemon"}
    assert service_home.call(Method.SESSION_RECORD, again)["started"] is False
    (after,) = service_home.call(Method.SESSION_LIST)["sessions"]
    assert after.get("generation") == listed.get("generation") and after.get("mode") == listed.get("mode")


def test_a_tap_this_service_cannot_run_is_left_to_tap_watch(tmp_path, monkeypatch):
    """The CLI (and so the service) runs on Python 3.10; the tap needs 3.11. A
    recorder that would fail at its first pass must not be acknowledged (the
    hook would then start no `tap watch`) (Codex R2)."""
    # In this process, not a service's: a suite run before this one (the
    # wizard's) may have imported the real `tap`, which `_load` would reuse.
    for name in [n for n in sys.modules if n == "tap" or n.startswith("tap.")]:
        monkeypatch.delitem(sys.modules, name)
    host = recorders.RecorderHost(log=lambda m: None, loop_getter=lambda: None)
    root = _tap(tmp_path / "tap-a", "0.10.0")
    monkeypatch.setattr(recorders, "MIN_PYTHON", (99, 0))
    assert host._load(str(root), "0.10.0") is False
    monkeypatch.setattr(recorders, "MIN_PYTHON", (3, 0))
    broken = _tap(tmp_path / "tap-b", "0.10.0")
    (broken / "tap" / "main.py").write_text("raise ImportError('needs StrEnum')\n")
    assert host._load(str(broken), "0.10.0") is False


def test_a_session_end_during_a_retry_wait_runs_the_last_pass_at_once(tmp_path):
    """Waiting after a failed pass, its SessionEnd comes: the last pass runs
    then (and FINALIZE), not after the wait, and never not at all (Codex R2)."""
    import threading

    calls = []

    class Hosted:
        ENDED, PAUSED, STOPPED, FAILED = "ended", "paused", "stopped", "failed"

        class Controls:
            def __init__(self):
                self.stop, self.pause = threading.Event(), threading.Event()

        @staticmethod
        def record(session, controls):
            calls.append(controls.stop.is_set())
            return (Hosted.ENDED, "") if controls.stop.is_set() else (Hosted.FAILED, "boom")

    host = recorders.RecorderHost(log=lambda m: None, loop_getter=lambda: None)
    host.hosted = Hosted
    rec = recorders.Recording("s1", {"sid": "s1"}, Hosted.Controls())
    thread = threading.Thread(target=host._guard, args=(rec,))
    thread.start()
    assert wait_for(lambda: calls == [False], 2)  # failed, now waiting 5 s
    rec.controls.stop.set()
    thread.join(2)
    assert not thread.is_alive() and calls == [False, True]


def test_an_ending_session_is_never_asked_to_hand_over(tmp_path):
    """Its SessionEnd came (a `/clear` never calls finish): no next worker
    will take its queue, so its worker drains it itself (Codex R2)."""
    import asyncio
    import fcntl
    import threading

    class Controls:
        def __init__(self):
            self.stop, self.pause = threading.Event(), threading.Event()

    host = recorders.RecorderHost(log=lambda m: None, loop_getter=lambda: None)
    host.hosted = type("H", (), {"ending": staticmethod(lambda params: params["sid"] == "ending")})
    state = tmp_path / "state"
    (state / "daemon").mkdir(parents=True)
    held = []
    for sid in ("ending", "live"):
        handle = open(state / "daemon" / f"{sid}.lock", "a")  # noqa: SIM115
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        held.append(handle)
    try:
        host.recordings = {sid: recorders.Recording(sid, {"sid": sid, "state_dir": str(state)}, Controls())
                           for sid in ("ending", "live")}
        host._save = lambda: None
        asyncio.run(host.close())
        assert not (state / "daemon" / "ending.handover").exists()
        assert (state / "daemon" / "live.handover").exists()
    finally:
        for handle in held:
            handle.close()
