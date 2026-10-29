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
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

from probe._shared import pins
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


def _late_reads(session):
    """What a real tap does long after its import: a module imported when first
    needed, and a data file read beside it."""
    try:
        import importlib
        late = importlib.import_module("tap.late")
        with open(os.path.join(os.path.dirname(late.__file__), "late.json")) as handle:
            result = {"ok": late.WORD + json.load(handle)["word"]}
    except Exception as exc:
        result = {"error": repr(exc)}
    with open(os.path.join(os.environ["HOME"], "late.jsonl"), "a") as handle:
        handle.write(json.dumps({"sid": session["sid"], **result}) + "\\n")


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
            go = os.path.join(os.environ["HOME"], "go-" + session["sid"])
            if behaviour == "lazy" and os.path.exists(go):
                os.unlink(go)
                _late_reads(session)
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


def _late_tap(root: Path, version: str) -> Path:
    """`_tap`, with a module it imports only when first needed and a data file."""
    _tap(root, version)
    (root / "tap" / "late.py").write_text('WORD = "late-"\n')
    (root / "tap" / "late.json").write_text(json.dumps({"word": version}))
    return root


def _late(home: Path, sid: str) -> list[dict]:
    try:
        lines = (home / "late.jsonl").read_text().splitlines()
    except OSError:
        return []
    return [row for row in map(json.loads, lines) if row["sid"] == sid]


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


def _restart_without(service_home, first: dict, folder: Path) -> None:
    """Stop the service, then remove `folder` as Codex does to the old
    version's when it installs a new one (an update cycle, then its restart)."""
    service_home.call(Method.STOP)
    assert service_home.wait_exit(first["pid"], 8)
    shutil.rmtree(folder)


def test_a_session_whose_tap_folder_went_resumes_on_the_tap_another_loaded(service_home, agent, tmp_path):
    """The session first in line named a removed folder: it was dropped, never
    said, and erased from recorders.json while the next session's tap loaded
    (Bucket, 2026-10-24: an update replaced the Codex tap). One tap records
    every session, so the one another session loads records it too, said
    when it is older than the session's own."""
    proc, owner = agent
    gone = _tap(tmp_path / "codex" / "probe-research-tap" / "0.10.1", "0.10.1")
    kept = _tap(tmp_path / "claude" / "tap", "0.10.0")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, _params("s1", owner, gone, "0.10.1", tmp_path))
    service_home.call(Method.SESSION_RECORD, _params("s2", owner, kept, "0.10.0", tmp_path))
    assert _saw(service_home.home, "s1", "started") and _saw(service_home.home, "s2", "started")
    _restart_without(service_home, first, gone)
    service_home.start()
    assert _saw(service_home.home, "s1", "started", count=2), service_home.log()
    assert _events(service_home.home, "s1")[-1]["version"] == "0.10.0"
    assert "recorder: session s1 resumed on tap 0.10.0 (its own 0.10.1 did not load)" in service_home.log()
    # s2 starts within RESUME_SPREAD_S; its thread is up now.
    for sid in ("s1", "s2"):
        assert service_home.call(Method.SESSION_RECORDING, {"sid": sid}) == {"recording": True}, sid
    assert "recorder: 2 session(s) resumed" in service_home.log()
    saved = json.loads((paths.service_dir() / recorders.RECORDERS_NAME).read_text())
    assert sorted(s["sid"] for s in saved["sessions"]) == ["s1", "s2"]


def test_a_session_whose_tap_folder_was_replaced_resumes_from_the_new_one(service_home, agent, tmp_path):
    """Codex's cache keeps one version folder per plugin: the removed one's
    newest version-shaped sibling that carries a tap is where it moved."""
    proc, owner = agent
    old = _tap(tmp_path / "codex" / "probe-research-tap" / "0.10.0", "0.10.0")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, _params("s1", owner, old, "0.10.0", tmp_path, PLUGIN_ROOT=str(old)))
    assert _saw(service_home.home, "s1", "started")
    _restart_without(service_home, first, old)
    _tap(old.parent / "0.9.9", "0.9.9")
    new = _tap(old.parent / "0.10.1", "0.10.1")
    _tap(old.parent / "latest", "0.11.0")  # not version-shaped: never a candidate
    service_home.start()
    assert _saw(service_home.home, "s1", "started", count=2), service_home.log()
    assert _events(service_home.home, "s1")[-1]["version"] == "0.10.1"
    assert f"tap folder {old} is gone; resuming from {new}" in service_home.log()
    (saved,) = json.loads((paths.service_dir() / recorders.RECORDERS_NAME).read_text())["sessions"]
    assert (saved["tap_root"], saved["tap_version"]) == (str(new), "0.10.1")
    assert saved["env"]["PLUGIN_ROOT"] == str(new), "as the hook's own fallback exports it"


def test_a_session_no_tap_can_resume_is_said_and_asked_again(service_home, agent, tmp_path):
    """Nothing to load: the service runs on, says which session it could not
    resume and why, and records it when its agent's next prompt asks again."""
    proc, owner = agent
    gone = _tap(tmp_path / "codex" / "probe-research-tap" / "0.10.0", "0.10.0")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, _params("s1", owner, gone, "0.10.0", tmp_path))
    assert _saw(service_home.home, "s1", "started")
    _restart_without(service_home, first, gone)
    second = service_home.start()
    assert wait_for(lambda: "recorder: session s1 not resumed: no tap loads" in service_home.log(), 5), \
        service_home.log()
    assert service_home.status()["pid"] == second["pid"]
    assert service_home.call(Method.SESSION_RECORDING, {"sid": "s1"}) == {"recording": False}
    assert json.loads((paths.service_dir() / recorders.RECORDERS_NAME).read_text())["sessions"] == []
    new = _tap(tmp_path / "codex" / "probe-research-tap" / "0.10.1", "0.10.1")
    assert service_home.call(Method.SESSION_RECORD, _params("s1", owner, new, "0.10.1", tmp_path))["recording"]
    assert _saw(service_home.home, "s1", "started", count=2), service_home.log()


def test_the_replacement_of_a_removed_tap_folder(tmp_path):
    cache = tmp_path / "probe-research-tap"
    gone = cache / "0.10.0"
    assert recorders._replacement(str(gone)) is None, "no sibling carries a tap"
    _tap(cache / "0.9.9", "0.9.9")
    _tap(cache / "0.10.2", "0.10.2")
    (cache / "0.10.10").mkdir()  # no tap inside
    _tap(cache / "next", "0.11.0")
    assert recorders._replacement(str(gone)) == (str(cache / "0.10.2"), "0.10.2")
    assert recorders._replacement(str(cache / "0.10.2")) is None, "a folder that carries a tap stays"
    # A folder that is not a version folder (a checkout, beside other plugins) is never re-resolved.
    assert recorders._replacement(str(tmp_path / "plugins" / "probe-research-tap")) is None
    # A saved path no filesystem call accepts is no tap and no replacement, never an error
    # that would stop every other session's resume.
    assert recorders._has_tap(tmp_path / "bad\0dir") is False
    assert recorders._replacement(str(tmp_path / "bad\0dir" / "0.10.0")) is None


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


def _resumable_host(tmp_path, ending: bool):
    """A host recording `s1` on a thread that stays until stopped; its tap says
    whether the session's end is down (`ending`)."""
    import threading

    started = []

    class Hosted:
        ENDED, PAUSED, STOPPED, FAILED = "ended", "paused", "stopped", "failed"

        class Controls:
            def __init__(self):
                self.stop, self.pause = threading.Event(), threading.Event()

        @staticmethod
        def record(session, controls):
            started.append(controls)
            while not controls.stop.wait(0.02) and not controls.pause.is_set():
                pass
            return Hosted.ENDED, ""

        @staticmethod
        def ending(params):
            return ending

    host = recorders.RecorderHost(log=lambda m: None, loop_getter=lambda: None)
    host.hosted = Hosted
    host._save = lambda: None
    params = _params("s1", {"pid": os.getpid(), "start_time": "1"}, tmp_path, "0.10.17", tmp_path)
    return host, params, started


def test_a_resume_while_the_recorder_finishes_starts_a_fresh_one(tmp_path):
    """Audit #10: pi's quit, then `--continue` at once. The recorder saw the
    session's end and is making its last pass; kept for the resumed session,
    it FINALIZEd and ended, and nothing recorded the resume. A fresh recorder
    takes it over once the finishing one lets go (D39)."""
    host, params, started = _resumable_host(tmp_path, ending=False)
    try:
        assert host.record(params)["started"] is True
        first = host.recordings["s1"]
        assert wait_for(lambda: len(started) == 1, 2)
        first.controls.stop.set()  # what the tap's loop does once it sees the sentinel (0.10.17)
        answer = host.record(params)
        assert answer["recording"] is True and answer["started"] is True
        assert host.recordings["s1"] is not first
        assert first.controls.stop.is_set(), "the finishing recorder must read as finishing"
        assert wait_for(lambda: len(started) == 2, 2)
    finally:
        for rec in [first, host.recordings.get("s1")]:
            if rec is not None:
                rec.controls.pause.set()
                rec.thread.join(2)


def test_a_live_recorder_asked_again_is_kept(tmp_path):
    host, params, started = _resumable_host(tmp_path, ending=False)
    try:
        host.record(params)
        first = host.recordings["s1"]
        assert host.record(params)["started"] is False
        assert host.recordings["s1"] is first and not first.controls.stop.is_set()
    finally:
        host.recordings["s1"].controls.pause.set()
        host.recordings["s1"].thread.join(2)


_OLD_STYLE_HOSTED = '''
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
                                 "env": None, "thread_env": None, "transcript": None}) + "\\n")


def record(session, controls):
    # A tap before 0.10.17: its loop finishes when it sees the sentinel, and
    # says nothing to the service (no `stop`).
    _note(session, "started")
    sentinel = session["env"]["PROBE_TEST_SENTINEL"]
    while True:
        if controls.pause.wait(0.05):
            _note(session, "paused")
            return PAUSED, ""
        if controls.stop.is_set() or os.path.exists(sentinel):
            _note(session, "finishing")
            time.sleep(1.0)
            _note(session, "ended")
            return ENDED, ""
'''


def test_an_older_taps_finishing_recorder_is_replaced_through_the_restart_onto_the_callers_tap(
    service_home, agent, tmp_path
):
    """Why `RecorderHost.record` needs no guess for a tap before 0.10.17 (its
    loop says nothing when it sees the session's end, and the caller removed
    the sentinel before asking): a resume comes from a newer tap, which
    restarts the service onto it, and the next service records the resumed
    session on that tap."""
    proc, owner = agent
    old = tmp_path / "tap-old"
    (old / "tap").mkdir(parents=True)
    (old / "tap" / "__init__.py").write_text('__version__ = "0.10.16"\n')
    (old / "tap" / "main.py").write_text("")
    (old / "tap" / "hosted.py").write_text(_OLD_STYLE_HOSTED)
    (old / "tap" / "threadenv.py").write_text(_THREADENV)
    new = _tap(tmp_path / "tap-new", "0.10.17")
    sentinel = tmp_path / "s1.shutdown"
    first = service_home.start()
    params = _params("s1", owner, old, "0.10.16", tmp_path, PROBE_TEST_SENTINEL=str(sentinel))
    assert service_home.call(Method.SESSION_RECORD, params)["recording"] is True
    assert _saw(service_home.home, "s1", "started")
    sentinel.touch()  # pi's quit
    assert _saw(service_home.home, "s1", "finishing")
    sentinel.unlink()  # the resume's `tap start` clears it, then asks
    resume = _params("s1", owner, new, "0.10.17", tmp_path, PROBE_TEST_SENTINEL=str(sentinel))
    assert service_home.call(Method.SESSION_RECORD, resume) == {"recording": False, "restart": True}
    assert service_home.wait_exit(first["pid"], 8), service_home.log()
    service_home.start()
    assert service_home.call(Method.SESSION_RECORD, resume)["recording"] is True
    started = lambda: [e for e in _events(service_home.home, "s1") if e["event"] == "started"]  # noqa: E731
    assert wait_for(lambda: started() and started()[-1]["version"] == "0.10.17", 5), _events(service_home.home, "s1")
    assert service_home.call(Method.SESSION_RECORDING, {"sid": "s1"}) == {"recording": True}


def test_a_recorder_taking_its_claim_says_so_at_once(tmp_path):
    """The hint lane reads only sessions whose recorder holds the claim
    (`hints.followed`), and slept with no timer when none did: a lone
    session's `session.record` woke it before its recorder took the claim, so
    the first prompt's hint came ~17 s late (live test E, 2026-10-24). The tap's
    loop publishes its claim (`Controls.claim`): the service hears it then."""
    import threading

    heard = []
    claimed = threading.Event()

    class Hosted:
        ENDED, PAUSED, STOPPED, FAILED = "ended", "paused", "stopped", "failed"

        class Controls:  # as the tap's `hosted.Controls` (0.10.6+)
            def __init__(self):
                self.stop, self.pause = threading.Event(), threading.Event()
                self.claimed = None

            def claim(self, folder):
                self.claimed = folder

        @staticmethod
        def record(session, controls):
            publish = getattr(controls, "claim", None)  # as `tap.main` takes it (`WatchConfig.claimed`)
            publish("/journal")
            claimed.set()
            controls.stop.wait(5)
            publish(None)
            return Hosted.ENDED, ""

    host = recorders.RecorderHost(log=lambda m: None, loop_getter=lambda: None, claimed=heard.append)
    host.hosted = Hosted
    host._save = lambda: None
    host._start({"sid": "s1"})
    assert claimed.wait(2)
    assert heard == ["s1"] and host.recordings["s1"].controls.claimed == "/journal"
    host.recordings["s1"].controls.stop.set()
    host.recordings["s1"].thread.join(2)
    assert heard == ["s1", "s1"]


def test_a_recorder_that_stepped_back_takes_the_session_when_asked_again(tmp_path):
    """Another recorder (the session's own `tap watch`) held the claim, so its
    loop returned and it waits to look again (15 s). A `session.record` for
    the session after that watcher let go (`hooks/tap_handover.py` asks once
    more) has it look again at once."""
    import threading

    tries = []

    class Hosted:
        ENDED, PAUSED, STOPPED, FAILED = "ended", "paused", "stopped", "failed"

        class Controls:
            def __init__(self):
                self.stop, self.pause = threading.Event(), threading.Event()

        @staticmethod
        def record(session, controls):
            tries.append(time.monotonic())
            if len(tries) == 1:
                return Hosted.STOPPED, "returned 0"  # claimed elsewhere
            controls.stop.wait(5)
            return Hosted.ENDED, ""

    host = recorders.RecorderHost(log=lambda m: None, loop_getter=lambda: None)
    host.hosted = Hosted
    host._save = lambda: None
    host._valid = lambda params: params
    host._start({"sid": "s1"})
    assert wait_for(lambda: len(tries) == 1 and host.recordings["s1"].last.startswith("stopped"), 2)
    assert host.record({"sid": "s1"}) == {"recording": True, "started": False, "pid": os.getpid()}
    assert wait_for(lambda: len(tries) == 2, 2), "it waited out its 15 s instead"
    assert tries[1] - tries[0] < 3
    host.recordings["s1"].controls.stop.set()
    host.recordings["s1"].thread.join(5)


def test_a_codex_tap_update_never_breaks_the_running_services_tap(service_home, agent, tmp_path):
    """Codex keeps ONE version folder of a plugin and deletes it when it
    installs the next (audit #14); this machine's service had imported its tap
    from there. The tap reads its own files long after its import: a module it
    imports when first needed, a data file beside it. The service imports from
    a copy of its own (`recorders._pin`), so neither breaks under it."""
    proc, owner = agent
    cache = tmp_path / "codex" / "plugins" / "cache" / "research-os-agent" / "probe-research-tap"
    old = _late_tap(cache / "0.10.18", "0.10.18")
    service_home.start()
    params = _params("s1", owner, old, "0.10.18", tmp_path, PROBE_TEST_BEHAVIOUR="lazy", PLUGIN_ROOT=str(old))
    assert service_home.call(Method.SESSION_RECORD, params)["recording"] is True
    assert _saw(service_home.home, "s1", "started")
    shutil.rmtree(old)  # Codex installs 0.10.19 and removes the folder the service loaded
    _late_tap(cache / "0.10.19", "0.10.19")
    (service_home.home / "go-s1").touch()
    assert wait_for(lambda: _late(service_home.home, "s1"), 5), service_home.log()
    assert _late(service_home.home, "s1") == [{"sid": "s1", "ok": "late-0.10.18"}], "the tap it loaded, whole"
    assert service_home.call(Method.SESSION_RECORDING, {"sid": "s1"}) == {"recording": True}
    copies = [p for p in (paths.service_dir() / recorders.TAPS_NAME).iterdir() if not p.name.startswith(".")]
    assert [p.name.split("-")[0] for p in copies] == ["0.10.18"]
    assert f"recorder: tap 0.10.18 loaded from {old} (its copy {copies[0]})" in service_home.log()


def _pin_dir(monkeypatch, tmp_path) -> Path:
    monkeypatch.setattr(paths, "service_dir", lambda: tmp_path / "service")
    return tmp_path / "service" / recorders.TAPS_NAME


def test_a_tap_is_copied_once_per_version_and_files(tmp_path, monkeypatch):
    store = _pin_dir(monkeypatch, tmp_path)
    root = _late_tap(tmp_path / "cache" / "0.10.18", "0.10.18")
    first = recorders._pin(str(root), "0.10.18")
    assert first.parent == store and (first / "tap" / "late.json").is_file() and (first / pins.PIN_DONE).is_file()
    assert recorders._pin(str(root), "0.10.18") == first, "the same files: the same copy"
    (root / "tap" / "late.py").write_text('WORD = "edited-"\n')  # a checkout edited in place
    second = recorders._pin(str(root), "0.10.18")
    assert second != first and (second / "tap" / "late.py").read_text() == 'WORD = "edited-"\n'
    # A copy cut short (no PIN_DONE) is made again, never used.
    (second / pins.PIN_DONE).unlink()
    (second / "tap" / "late.py").unlink()
    assert recorders._pin(str(root), "0.10.18") == second and (second / "tap" / "late.py").is_file()


def test_old_copies_go_but_never_the_one_loading(tmp_path, monkeypatch):
    store = _pin_dir(monkeypatch, tmp_path)
    made, now = [], time.time()
    for n in range(pins.PIN_KEEP + 2):
        made.append(recorders._pin(str(_late_tap(tmp_path / "cache" / f"0.10.{n}", f"0.10.{n}")), f"0.10.{n}"))
        os.utime(made[-1], (now - 100 + n, now - 100 + n))
    week_old = recorders._pin(str(_late_tap(tmp_path / "cache" / "0.9.0", "0.9.0")), "0.9.0")
    os.utime(week_old, (now - pins.PIN_KEEP_S - 60,) * 2)
    stale = store / ".0.10.9-x.123.456"
    stale.mkdir()
    os.utime(stale, (1, 1))
    loading = recorders._pin(str(tmp_path / "cache" / "0.10.0"), "0.10.0")  # the oldest, loaded again
    assert loading == made[0]
    left = sorted(p.name for p in store.iterdir() if p.is_dir())  # the store also holds its lock file
    # The one loading, and the newest-used PIN_KEEP others; never a leftover.
    assert left == sorted(p.name for p in [made[0], *made[-pins.PIN_KEEP:]])


def test_a_tap_that_cannot_be_copied_loads_in_place(tmp_path, monkeypatch):
    def refuse(root, version):
        raise OSError("no space left on device")

    monkeypatch.setattr(recorders, "_pin", refuse)
    lines = []
    host = recorders.RecorderHost(log=lines.append, loop_getter=lambda: None)
    root = _late_tap(tmp_path / "cache" / "0.10.18", "0.10.18")
    try:
        assert host._load(str(root), "0.10.18")
        assert (host.tap_root, host.tap_copy) == (str(root), str(root))
    finally:
        sys.path[:] = [p for p in sys.path if p != str(root)]
        for name in [n for n in sys.modules if n == "tap" or n.startswith("tap.")]:
            sys.modules.pop(name, None)
    assert any("cannot copy the tap" in line and "no space left" in line for line in lines)


@pytest.mark.parametrize("change", ["a-module-arrives", "a-module-grows"])
def test_a_tap_written_while_it_is_copied_is_never_used(tmp_path, monkeypatch, change):
    """An agent still installing the tap as the service copies it (Codex's
    newest folder, picked by listing): the copy holds part of it. It is never
    marked done or imported; the service loads the tap in place instead."""
    import shutil

    store = _pin_dir(monkeypatch, tmp_path)
    root = _late_tap(tmp_path / "cache" / "0.10.18", "0.10.18")
    real = shutil.copytree

    def copy_then_write(src, dst, *args, **kwargs):
        done = real(src, dst, *args, **kwargs)
        if change == "a-module-arrives":
            (root / "tap" / "arrived.py").write_text("X = 1\n")  # the installer, still writing
        else:
            with open(root / "tap" / "late.py", "a") as handle:
                handle.write("MORE = 2\n")
        return done

    monkeypatch.setattr(shutil, "copytree", copy_then_write)
    with pytest.raises(OSError, match="changed while it was copied"):
        recorders._pin(str(root), "0.10.18")
    assert not [p for p in store.iterdir() if (p / pins.PIN_DONE).exists()], "no copy marked done"
    assert not [p for p in store.iterdir() if p.is_dir()], "its part copy is gone too"
    lines = []
    host = recorders.RecorderHost(log=lines.append, loop_getter=lambda: None)
    try:
        assert host._load(str(root), "0.10.18")
        assert host.tap_copy == str(root), "loaded in place"
    finally:
        sys.path[:] = [p for p in sys.path if p != str(root)]
        for name in [n for n in sys.modules if n == "tap" or n.startswith("tap.")]:
            sys.modules.pop(name, None)
    assert any("changed while it was copied" in line for line in lines)
    monkeypatch.setattr(shutil, "copytree", real)
    whole = recorders._pin(str(root), "0.10.18")  # once it holds still: copied
    assert (whole / pins.PIN_DONE).is_file() and (whole / "tap" / "late.py").read_text().endswith(
        "MORE = 2\n" if change == "a-module-grows" else 'WORD = "late-"\n')

