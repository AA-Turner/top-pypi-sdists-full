"""A real Probe service reports what fails here, once each, with consent (crash-report plan T6).

End to end: a real service in a throwaway HOME, a stand-in tap package for its
recorders, `FakeWorker` for the daemon worker its supervisor starts, real hook
host processes, and `FakeCore` playing `probe.core.run report` (PR 2a's read):
each report call's params are what the service sent. What these hold:

  * a hosted recorder that keeps failing: one `recorder` report about its session;
  * a SIGKILLed service: the next one reports `service_crash` once, and a stop
    on purpose after it is none; on Windows only a recorded crash
    (`last-crash.json`) is one, and a kill that recorded none is none;
  * a daemon worker that gives up: one `worker` report about its session;
  * a hook host that keeps dying: one `hook_host` report after the third;
  * a guard rejection (`guard.json` ok false): one `update_rejected`, naming the version;
  * a session whose environment turns reports off: none;
  * `hooks.run` events that exit 2 (a Stop message delivered, a veto): none;
  * the update barrier up: none, while it is.
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import time
from pathlib import Path

import pytest

from probe.service import barrier, paths, workers
from probe.service.protocol import Method
from tests.service_fakes import FakeCore, FakeWorker
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401

# The service runs on Windows too (R3): what it does not do there is skipped
# test by test, with the reason.
WINDOWS = os.name == "nt"

HOOKS = Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks"

#: A tap whose recorder fails at every pass (`PROBE_TEST_BEHAVIOUR=fail`), or
#: hands its session's daemon worker to the service (`=worker`) as
#: `tap.companion_supervisor` does, then waits for its stop or pause.
_HOSTED = '''
import json, os, threading
from dataclasses import dataclass, field

ENDED, PAUSED, STOPPED, FAILED = "ended", "paused", "stopped", "failed"


@dataclass
class Controls:
    stop: threading.Event = field(default_factory=threading.Event)
    pause: threading.Event = field(default_factory=threading.Event)
    workers: object = None


def _note(env, sid, event):
    with open(os.path.join(env["HOME"], "recorded.jsonl"), "a") as handle:
        handle.write(json.dumps({"sid": sid, "event": event}) + "\\n")


def record(session, controls):
    env, sid = session["env"], session["sid"]
    behaviour = env.get("PROBE_TEST_BEHAVIOUR", "")
    if behaviour == "fail":
        _note(env, sid, "failing")
        return FAILED, "RuntimeError: the transcript would not parse"
    link = None
    if behaviour == "worker":
        state = os.path.join(env["HOME"], ".local", "state", "probe")

        def switch():
            try:
                word = open(os.path.join(state, "sessions", sid + ".state")).read().strip() or None
            except OSError:
                word = None
            return word, word == "daemon"

        link = controls.workers
        link.supervise({"sid": sid, "transcript": session["transcript"], "cwd": session["cwd"],
                        "source": "claude_code", "daemon_dir": os.path.join(state, "daemon"), "env": env,
                        "switch": switch})
    _note(env, sid, "recording")
    while True:
        if controls.stop.wait(0.05):
            if link is not None:
                link.release()
            return ENDED, ""
        if controls.pause.is_set():
            return PAUSED, ""
'''

REPORT = {"sent": True, "id": "r-1", "skipped": None, "path": None}


def _tap(root: Path) -> Path:
    (root / "tap").mkdir(parents=True)
    (root / "tap" / "__init__.py").write_text('__version__ = "0.10.0"\n')
    (root / "tap" / "main.py").write_text("")
    (root / "tap" / "hosted.py").write_text(_HOSTED)
    return root


class Live:
    def __init__(self, sh, core: FakeCore, worker: FakeWorker, owner: dict, root: Path, tmp: Path) -> None:
        self.sh, self.core, self.worker, self.owner, self.root, self.tmp = sh, core, worker, owner, root, tmp

    def reports(self) -> list[dict]:
        return [json.loads(call["stdin"]) for call in self.core.calls("report")]

    def record(self, sid: str, *, mode: str = "inline", **env) -> dict:
        params = {
            "sid": sid, "harness": "claude_code", "mode": mode, "owner": self.owner, "generation": 1,
            "state_dir": str(self.sh.home / ".local" / "state" / "probe"), "cwd": str(self.tmp),
            "transcript": str(self.tmp / f"{sid}.jsonl"), "transcript_dir": None, "tap_root": str(self.root),
            "tap_version": "0.10.0", "env": {"HOME": str(self.sh.home), **env},
        }
        return self.sh.call(Method.SESSION_RECORD, params)

    def consenting_session(self, sid: str = "c1") -> None:
        """A live session whose registrant said its environment allows reports
        (a tap from this release): a machine family needs every live one's yes."""
        answer = self.sh.call(Method.SESSION_REGISTER, {
            "sid": sid, "harness": "pi", "mode": "inline", "owner": self.owner, "generation": 1, "report_env": True,
        })
        assert answer["alive"] is True

    def events(self, sid: str, event: str) -> int:
        try:
            lines = (self.sh.home / "recorded.jsonl").read_text().splitlines()
        except OSError:
            return 0
        return sum(1 for line in lines if json.loads(line) == {"sid": sid, "event": event})


@pytest.fixture
def live(service_home, monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_SERVICE_REPORTS", "1")
    monkeypatch.setenv("PROBE_SERVICE_WATCH_S", "0.2")
    monkeypatch.setenv("PROBE_SERVICE_RECORDER_RETRY_S", "0.05")
    monkeypatch.setenv(workers.POLL_ENV, "0.05")
    core = FakeCore(service_home.home)
    core.plan("report", stdout=REPORT)
    worker = FakeWorker(service_home.home)
    agent, owner = spawn_agent()
    try:
        yield Live(service_home, core, worker, owner, _tap(tmp_path / "tap-a"), tmp_path)
    finally:
        kill_agent(agent)
        for pid in worker.live_pids():  # none on Windows: no worker supervision there
            with __import__("contextlib").suppress(OSError):
                os.kill(pid, signal.SIGKILL)


def _settled(live: Live, seconds: float = 1.0) -> list[dict]:
    """The report calls once `seconds` more passed (five scans): none more came."""
    time.sleep(seconds)
    return live.reports()


def test_a_hosted_recorder_that_keeps_failing_is_reported_once(live):
    live.sh.start()
    assert live.record("s1", PROBE_TEST_BEHAVIOUR="fail")["recording"] is True
    assert wait_for(live.reports, 15), live.sh.log()
    assert wait_for(lambda: live.events("s1", "failing") >= 6, 10)
    (report,) = _settled(live)
    assert report["auto"] is True and report["family"] == "recorder" and report["reason"] == "failing"
    # "s1" is no UUID: the `report` read would refuse it, so it rides in the facts.
    assert report["sid"] is None and report["facts"]["session"] == "s1" and report["env"] == {}
    assert report["facts"]["count"] == 3
    assert "the transcript would not parse" in report["facts"]["events"][-1]["detail"]
    assert "watch: report recorder (failing) (session s1): sent r-1" in live.sh.log()


def test_a_session_whose_environment_turns_reports_off_is_never_reported(live):
    live.sh.start()
    live.record("s1", PROBE_TEST_BEHAVIOUR="fail", PROBE_TELEMETRY="off")
    assert wait_for(lambda: live.events("s1", "failing") >= 6, 15)
    assert _settled(live, 0.6) == []
    assert "recorder (failing) (session s1) not reported: the environment it happened in turns reports off" in live.sh.log()


@pytest.mark.skipif(WINDOWS, reason="Windows reports only a recorded crash (watch.WINDOWS: a logoff ends the service "
                    "with no stop record); test_on_windows_only_a_recorded_crash_is_reported_once pins that")
def test_a_sigkilled_service_is_reported_by_the_next_once_and_a_stop_on_purpose_is_none(live):
    sh = live.sh
    first = sh.start()
    os.kill(first["pid"], signal.SIGKILL)
    assert sh.wait_exit(first["pid"], 5)
    second = sh.start()
    assert second["pid"] != first["pid"]
    live.consenting_session()
    assert wait_for(live.reports, 15), sh.log()
    (report,) = live.reports()
    assert report["family"] == "service_crash" and report["reason"] == "unclean_exit" and report["sid"] is None
    assert report["facts"]["boot_known"] is True and report["facts"]["previous"]["version"]
    sh.call(Method.STOP)
    assert sh.wait_exit(second["pid"], 5)
    sh.start()
    assert [r["family"] for r in _settled(live)] == ["service_crash"]


def _lock_free() -> bool:
    """No service holds `service.lock` (the one that crashed has exited)."""
    fd = os.open(paths.lock_path(), os.O_RDWR | os.O_CREAT)
    try:
        if paths.try_lock(fd):
            paths.unlock(fd)
            return True
        return False
    finally:
        os.close(fd)


@pytest.mark.skipif(not WINDOWS, reason="Windows' rule (watch.WINDOWS); POSIX's: the SIGKILL test above")
def test_on_windows_only_a_recorded_crash_is_reported_once(live):
    """A logoff ends the service with no stop record, and the uptime boot id
    survives it: on Windows a missing stop record says nothing, and only
    `last-crash.json` (a service on its way out of an exception) is a crash.
    A real one here: a service that finds its pipe's name taken cannot serve,
    and exits on the exception."""
    import _winapi

    from probe.service import client, watch, winpipe

    sh = live.sh
    first = sh.start()
    live.consenting_session()  # kept in sessions.json: every later service restores it, and asks it
    os.kill(first["pid"], signal.SIGTERM)  # TerminateProcess: no stop record, no last-crash.json
    assert sh.wait_exit(first["pid"], 10) and sh.wait_spawners()
    second = sh.start()
    assert second["pid"] != first["pid"]
    assert _settled(live, 1.5) == [], "an exit that recorded no crash is none on Windows"
    assert "ended without stopping" not in sh.log()
    sh.call(Method.STOP)
    assert sh.wait_exit(second["pid"], 10) and sh.wait_spawners()
    crash = paths.service_dir() / watch.LAST_CRASH_NAME
    taken = winpipe.create_pipe(paths.pipe_name(), True)
    try:
        client._spawn(client.runtime_python())
        assert wait_for(crash.exists, 30), sh.log()
        assert wait_for(_lock_free, 15), sh.log()
    finally:
        _winapi.CloseHandle(taken)
    third = sh.start()
    assert wait_for(live.reports, 15), sh.log()
    (report,) = live.reports()
    assert report["family"] == "service_crash" and report["reason"] == "crashed" and report["sid"] is None
    assert report["facts"]["error"] and report["facts"]["traceback"], report["facts"]
    assert not crash.exists(), "reported: the record is taken"
    sh.call(Method.STOP)
    assert sh.wait_exit(third["pid"], 10) and sh.wait_spawners()
    paths.starts_path().unlink()  # a fourth start in a minute is `ensure`'s back-off, not this test's
    sh.start()
    assert [r["family"] for r in _settled(live)] == ["service_crash"]


@pytest.mark.skipif(WINDOWS, reason="the service supervises no daemon worker on Windows (WorkerHost.claim refuses there)")
def test_a_daemon_worker_that_gives_up_is_reported_once(live):
    sh = live.sh
    live.worker.plan(exits=[workers.EXIT_DO_NOT_RESPAWN])
    sessions = sh.home / ".local" / "state" / "probe" / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / "s1.state").write_text("daemon")
    sh.start()
    live.record("s1", mode="daemon", PROBE_TEST_BEHAVIOUR="worker")
    assert wait_for(live.reports, 15), sh.log()
    (report,) = _settled(live)
    assert report["family"] == "worker" and report["reason"] == "gave_up_exit_3"
    assert report["sid"] is None and report["facts"]["session"] == "s1"
    assert report["facts"]["source"] == "supervisor" and report["facts"]["last_exit"] == 3
    assert len(live.worker.starts("s1")) == 1, "a give-up is not respawned"


@pytest.mark.skipif(WINDOWS, reason="no hook host on Windows (hooks.host refuses there: a host forks each event)")
def test_a_hook_host_that_keeps_dying_is_reported_after_the_third(live, tmp_path):
    sh = live.sh
    root = tmp_path / "dying-plugin"
    (root / "hooks").mkdir(parents=True)
    (root / "hooks" / "zygote.py").write_text("import sys\nsys.exit(1)\n")
    (root / "hooks" / "dispatch.py").write_text("")
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "probe-research"}))
    sh.start()
    live.consenting_session()
    for n in range(3):
        assert sh.call(Method.HOOKS_HOST, {"root": str(root)})["started"] is True, sh.log()
        # `service.status` reaps it: a host that exited 1 on its own.
        assert wait_for(lambda: sh.call(Method.STATUS)["hook_hosts"] == [], 10)
        if n < 2:
            time.sleep(0.4)
            assert live.reports() == [], "fewer than three"
    assert wait_for(live.reports, 10), sh.log()
    (report,) = _settled(live)
    assert report["family"] == "hook_host" and report["reason"] == "host_exited" and report["sid"] is None
    assert report["facts"]["count"] == 3 and report["facts"]["events"][-1]["code"] == 1


@pytest.mark.skipif(WINDOWS, reason="hooks.run refuses on Windows (hookhosts.runnable: its routes run in the dispatcher there)")
def test_hooks_run_events_that_exit_2_are_never_a_failure(live, tmp_path):
    """A Stop message delivered, a PreToolUse veto: exit 2 is an answer, not a crash (Codex rev-3 #3)."""
    sh = live.sh
    root = tmp_path / "vetoing-plugin"
    (root / "hooks").mkdir(parents=True)
    for name in ("dispatch.py", "dispatch.sh", "zygote.py", "_service_paths.py"):
        shutil.copy2(HOOKS / name, root / "hooks" / name)
    veto = "/bin/bash -c 'cat >/dev/null; echo vetoed >&2; exit 2'"
    (root / "hooks" / "routes.json").write_text(json.dumps({"hooks": {"PreToolUse": [
        {"lane": "pre-tool", "matcher": "^Bash$", "hooks": [{"type": "command", "command": veto}]}]}}))
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "probe-research"}))
    sh.start()
    live.consenting_session()
    for _ in range(5):
        answer = sh.call(Method.HOOKS_RUN, {
            "plugin_root": str(root), "lane": "pre-tool", "env": {"HOME": str(sh.home), "PATH": os.environ["PATH"]},
            "cwd": str(tmp_path), "timeout_ms": 30_000,
            "payload": {"tool_name": "Bash", "tool_input": {"command": "ls"}, "session_id": "s-hooks"},
        })
        assert answer["exit_code"] == 2 and not answer["timed_out"], answer
    assert _settled(live) == []
    assert "hook_host" not in sh.log()


def test_a_rejected_release_is_reported_once_naming_the_version(live):
    sh = live.sh
    sh.start()
    live.consenting_session()
    (paths.service_dir() / "guard.json").write_text(json.dumps({
        "at": time.time(), "from": "0.296.0", "to": "0.297.0", "ok": False,
        "reason": "the new service did not answer within 105 s", "rollback": "done",
        "active": "0.296.0", "answering": "0.296.0",
    }))
    assert wait_for(live.reports, 10), sh.log()
    (report,) = _settled(live)
    assert report["family"] == "update_rejected" and report["reason"] == "switched_back"
    assert report["facts"]["rejected_version"] == "0.297.0" and report["facts"]["from"] == "0.296.0"


def test_nothing_is_reported_while_the_update_barrier_is_up(live):
    sh = live.sh
    sh.start()
    # The barrier an update raises (its owner: a live process, this test's).
    barrier.raise_barrier("test-token", pid=os.getpid())
    try:
        # The watch reads the barrier at its scan (never on a recorder's thread).
        time.sleep(0.6)
        live.record("s1", PROBE_TEST_BEHAVIOUR="fail")
        assert wait_for(lambda: live.events("s1", "failing") >= 5, 15)
        assert _settled(live, 0.6) == []
    finally:
        barrier.lower("test-token")
    # Lowered: what fails from here on is counted again.
    live.record("s2", PROBE_TEST_BEHAVIOUR="fail")
    assert wait_for(live.reports, 15), sh.log()
    assert [(r["family"], r["facts"].get("session")) for r in _settled(live, 0.4)] == [("recorder", "s2")]


# -- the real `report` read (PR 2a, on main) against a stand-in API ----------------------


class Api:
    """A local HTTP server standing in for `POST /v1/diagnostics/reports`."""

    REPORT_ID = "7f3c9a2e-1111-4222-8333-444455556666"

    def __init__(self) -> None:
        import threading
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

        self.posts: list = []
        api = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args) -> None:
                pass

            def do_POST(self) -> None:  # noqa: N802 -- http.server's name
                body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                api.posts.append({"path": self.path, "auth": self.headers.get("Authorization"),
                                  "body": json.loads(body or b"{}")})
                data = json.dumps({"id": api.REPORT_ID}).encode()
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()


def test_the_real_report_read_sends_what_the_watch_hands_it(service_home, monkeypatch, tmp_path):
    """No stand-in for the read: the service runs the real `python -I -m
    probe.core.run report` (runtime.json: this interpreter), which takes the
    watch's params, collects, and POSTs to a local server. The session's own
    environment names Probe's hosted service (the consent's backend: it
    outranks the CLI config's), while the CLI config, which the upload uses,
    names the local server: nothing leaves this machine."""
    import uuid

    from probe.sdk.config import save_context

    api = Api()
    try:
        monkeypatch.setenv("PROBE_SERVICE_REPORTS", "1")
        monkeypatch.setenv("PROBE_SERVICE_WATCH_S", "0.2")
        monkeypatch.setenv("PROBE_SERVICE_RECORDER_RETRY_S", "0.05")
        # Where the service (HOME only, a clean environment) reads the CLI config too.
        monkeypatch.setenv("XDG_CONFIG_HOME", str(service_home.home / ".config"))
        save_context({"base_url": api.url, "token": "probe_pat_" + "e2e0" * 8})
        agent, owner = spawn_agent()
        try:
            sh = service_home
            sh.start()
            sid = str(uuid.uuid4())
            root = _tap(tmp_path / "tap-real")
            answer = sh.call(Method.SESSION_RECORD, {
                "sid": sid, "harness": "claude_code", "mode": "inline", "owner": owner, "generation": 1,
                "state_dir": str(sh.home / ".local" / "state" / "probe"), "cwd": str(tmp_path),
                "transcript": str(tmp_path / f"{sid}.jsonl"), "transcript_dir": None, "tap_root": str(root),
                "tap_version": "0.10.0",
                "env": {"HOME": str(sh.home), "PROBE_TEST_BEHAVIOUR": "fail",
                        "PROBE_BASE_URL": "https://api.research.prbe.ai"},
            })
            assert answer["recording"] is True
            assert wait_for(lambda: api.posts, 90), sh.log()
            (post,) = api.posts
            body = post["body"]
            assert post["path"] == "/v1/diagnostics/reports" and post["auth"].startswith("Bearer probe_pat_")
            assert body["kind"] == "auto" and body["family"] == "recorder" and body["reason"] == "failing"
            assert body["session_ids"] == [sid]
            assert "the transcript would not parse" in json.dumps(body["report"])
            assert wait_for(lambda: f"(session {sid}): sent {Api.REPORT_ID}" in sh.log(), 10), sh.log()
        finally:
            kill_agent(agent)
    finally:
        api.close()
