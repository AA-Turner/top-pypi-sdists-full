"""The tap's recorder under both of its hosts, as real processes (plan D21).

One recorder codebase, two hosts: standalone `tap watch` (the hook's wrapper
starts it) and a thread of the Probe service (`session.record`). Every test
here runs once per host, and asserts the same outcome for both, so a behaviour
that differs between them fails a test:

    watch    `PROBE_TAP_HOSTED=0`: `tap start` spawns the wrapper and its `tap watch`
    service  `PROBE_TAP_HOSTED=1`: `tap start` asks a real Probe service in a
             throwaway HOME (`service_harness.service_home`) to record it

Both are driven the way an agent drives them: SessionStart's `tap start`
(after the owner record `tap owner` writes), transcript lines appended as a
session writes them, and SessionEnd's own hook (`hooks/session-end.sh --wait`).
Both upload to the live run's stub Probe API (`tests/live/live_run.py`
`StubState`, one stub for the 5 h run and this), which checks every batch
continues its stream; nothing is monkeypatched in the recorder.

`tests/test_durable_runtime.py` (in the tap's own suite) keeps the
fine-grained cases that need the loop's internals patched; its `hosted` variant
runs the loop on a thread in-process. This file is the end-to-end half: what
the server receives, when the session ends, after a crash, through an outage,
from a folder switched off, with a credential in the transcript.
"""

from __future__ import annotations

import contextlib
import importlib.util
import json
import os
import signal
import subprocess
import sys
import threading
import time
import uuid
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from probe.service import paths, procid
from probe.service.protocol import Method
from tests.service_harness import kill_agent, pid_running, service_home, spawn_agent, wait_for  # noqa: F401

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the service is POSIX-only until R3")

AGENT = Path(__file__).resolve().parents[1]
TAP_ROOT = AGENT / "plugins" / "probe-research-tap"
SESSION_END = TAP_ROOT / "hooks" / "session-end.sh"
WATCHER = "/tmp/probe-research-tap-watcher-"
LABEL = "t1"
#: Looks like a Probe API token: the tap's scrubber must take it out.
SECRET = "probe_pat_" + "0123456789abcdef" * 2


def _live_run():
    """The live run's harness module (its stub Probe API), loaded from its file."""
    name = "_live_run_stub"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).parent / "live" / "live_run.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module  # before exec: its dataclasses look themselves up there
        spec.loader.exec_module(module)
    return sys.modules[name]


live_run = _live_run()


class Stub(live_run.StubState):
    """The live run's stub, plus every POST body it was sent and an outage switch."""

    def __init__(self, root: Path) -> None:
        layout = live_run.Layout(root, root / "out")
        layout.make()
        super().__init__(layout, {})
        self.bodies: list[bytes] = []
        self.down = threading.Event()

    def accept(self, source: str, raw: bytes) -> tuple[int, dict]:
        with self.lock:
            self.bodies.append(raw)
        if self.down.is_set():
            return 503, {"detail": "the stub is down"}
        return super().accept(source, raw)

    def accepted(self, sid: str) -> list[dict]:
        batches = self.snapshot().get(sid, {}).get("batches", [])
        return sorted((b for b in batches if b["status"] == "accepted"), key=lambda b: b["batch_seq"])

    def lines(self, sid: str) -> list[int]:
        """The transcript lines the server took, in batch order, by their marker."""
        return [int(m.split(":")[1]) for b in self.accepted(sid) for m in b["markers"]]

    def finalized(self, sid: str) -> bool:
        accepted = self.accepted(sid)
        return bool(accepted) and accepted[-1]["finalize"]


@pytest.fixture
def stub(tmp_path):
    state = Stub(tmp_path / "stub")
    server = ThreadingHTTPServer(("127.0.0.1", 0), live_run.make_handler(state))
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, name="stub-api", daemon=True)
    thread.start()
    state.base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        yield state
    finally:
        server.shutdown()
        server.server_close()
        for handle in (state.requests_log, state.batches_log):
            handle.close()


def _watch_children(pid: int) -> list[int]:
    """`pid`'s `tap watch` children (never the wrapper's `sleep 5` between respawns)."""
    out = subprocess.run(["ps", "-A", "-ww", "-o", "pid=,ppid=,command="], capture_output=True, text=True,
                         timeout=30, check=False).stdout
    found = []
    for line in out.splitlines():
        parts = line.split(None, 2)
        if len(parts) == 3 and parts[1] == str(pid) and "-m tap watch" in parts[2]:
            found.append(int(parts[0]))
    return found


class Host:
    """One session recorded by one host, started and ended as an agent does."""

    def __init__(self, kind: str, service_home, stub: Stub, agent_pid: int) -> None:
        self.kind = kind
        self.service = service_home
        self.stub = stub
        self.agent_pid = agent_pid
        self.sid = str(uuid.uuid4())
        home = service_home.home
        self.cwd = home / "work"
        self.cwd.mkdir()
        self.transcript = self.cwd / f"{self.sid}.jsonl"
        self.transcript.write_text("")
        self.plugin_dir = home / "tap-state"
        self.written = 0
        bin_dir = home / "bin"
        bin_dir.mkdir()
        # The hooks run `python3`: this interpreter, whatever the machine's is.
        python3 = bin_dir / "python3"
        python3.write_text(f'#!/bin/sh\nexec "{sys.executable}" "$@"\n')
        python3.chmod(0o755)
        self.env = {
            **os.environ,
            "PATH": f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '/usr/bin:/bin')}",
            "PYTHONPATH": str(TAP_ROOT),
            "PROBE_TAP_HOSTED": "1" if kind == "service" else "0",
            "PROBE_BASE_URL": stub.base_url,
            "PROBE_INGEST_TOKEN": "synthetic-ingest-token",
            "PROBE_RESEARCH_TAP_PLUGIN_DIR": str(self.plugin_dir),
            "PROBE_TRANSCRIPT_STATE_DIR": str(home / "transcripts-v2"),
            # A tick a second (the default is 60 s active, 300 s idle).
            "PROBE_RESEARCH_TAP_INTERVAL_SECONDS": "1",
            # Discovery's roots: empty folders of this HOME, never a real one.
            "PROBE_RESEARCH_TAP_PROJECTS_DIR": str(home / "projects"),
            "PRBE_CODEX_SESSIONS_DIR": str(home / "codex-sessions"),
            "PROBE_KIMI_SESSIONS_DIR": str(home / "kimi-sessions"),
            # SessionEnd's full wait (15 s), as a container sets it.
            "CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS": "16000",
        }
        for name in ("PROBE_TAP_SOURCE", "CLAUDE_PLUGIN_ROOT", "PLUGIN_ROOT"):
            self.env.pop(name, None)

    # -- the session's agent ---------------------------------------------------------

    def write(self, count: int, *, text: str = "turn") -> None:
        with self.transcript.open("a", encoding="utf-8") as handle:
            for _ in range(count):
                handle.write(json.dumps({
                    "type": "user", "sessionId": self.sid, "cwd": str(self.cwd), "uuid": str(uuid.uuid4()),
                    "message": {"role": "user", "content": f"{text} LIVE-RUN-MARK {LABEL} L{self.written:06d}"},
                }) + "\n")
                self.written += 1

    def start(self) -> None:
        """SessionStart: `tap owner`'s record of the agent process, then `tap start`."""
        owner = Path(f"{WATCHER}{self.sid}.owner")
        owner.write_text(json.dumps({"pid": self.agent_pid, "start": procid.start_time(self.agent_pid),
                                     "name": "claude"}))
        done = subprocess.run(
            [sys.executable, "-m", "tap", "start", "--session-id", self.sid, "--cwd", str(self.cwd),
             "--transcript", str(self.transcript), "--plugin-root", str(TAP_ROOT)],
            env=self.env, cwd=str(self.cwd), capture_output=True, text=True, timeout=30, check=False,
        )
        assert done.returncode == 0, f"tap start: {done.returncode} {done.stderr}"
        assert wait_for(self.recording, 10), f"{self.kind}: nothing records the session ({self.facts()})"

    def end(self) -> None:
        """SessionEnd: the tap's own hook, waiting for the last pass."""
        payload = json.dumps({"session_id": self.sid, "hook_event_name": "SessionEnd", "reason": "other"})
        done = subprocess.run(["bash", str(SESSION_END), "--wait"], input=payload, env=self.env, cwd=str(self.cwd),
                              capture_output=True, text=True, timeout=40, check=False)
        assert done.returncode == 0, done.stderr

    # -- which host records it ---------------------------------------------------------

    def wrapper_pid(self) -> int | None:
        with contextlib.suppress(OSError, ValueError):
            return int(Path(f"{WATCHER}{self.sid}.pid").read_text().strip())
        return None

    def watch_pid(self) -> int | None:
        """The wrapper's `tap watch` child."""
        wrapper = self.wrapper_pid()
        children = _watch_children(wrapper) if wrapper and pid_running(wrapper) else []
        return children[0] if children else None

    def hosted_pid(self) -> int | None:
        with contextlib.suppress(OSError, ValueError):
            return int(Path(f"{WATCHER}{self.sid}.hosted").read_text().strip())
        return None

    def recording(self) -> bool:
        if self.kind == "watch":
            return self.watch_pid() is not None and self.hosted_pid() is None
        try:
            return self.service.call(Method.SESSION_RECORDING, {"sid": self.sid}) == {"recording": True}
        except OSError:
            return False

    def gone(self) -> bool:
        """No recorder of this session runs on this host any more."""
        if self.kind == "watch":
            wrapper = self.wrapper_pid()
            return not (wrapper and pid_running(wrapper)) and self.watch_pid() is None
        return not self.recording()

    def crash(self) -> None:
        """The host dies under the session (SIGKILL): the tap watch process, or the service."""
        if self.kind == "watch":
            pid = self.watch_pid()
        else:
            pid = self.hosted_pid()
            assert pid and pid == self.service.status()["pid"], "the marker names the running service"
        assert pid, self.facts()
        os.kill(pid, signal.SIGKILL)
        assert wait_for(lambda: not pid_running(pid), 5)

    def recover(self) -> None:
        """What brings the host back: the wrapper respawns `tap watch` by itself
        (5 s later); a service is started again by the next caller, and resumes
        the sessions it recorded from their saved progress."""
        if self.kind == "service":
            self.service.start()
        assert wait_for(self.recording, 20), f"{self.kind}: not recording again ({self.facts()})"

    def facts(self) -> str:
        log = self.plugin_dir / "logs" / f"{self.sid}.log"
        try:
            tail = log.read_text(encoding="utf-8")[-3000:]
        except OSError:
            tail = "(no tap log)"
        return (f"wrapper {self.wrapper_pid()}, hosted {self.hosted_pid()}; tap log:\n{tail}\n"
                f"service log:\n{self.service.log()[-2000:]}")

    def cleanup(self) -> None:
        Path(f"{WATCHER}{self.sid}.shutdown").touch()
        wrapper = self.wrapper_pid()
        if wrapper and pid_running(wrapper):
            with contextlib.suppress(OSError):
                os.killpg(wrapper, signal.SIGTERM)
            if not wait_for(lambda: not pid_running(wrapper), 5):
                with contextlib.suppress(OSError):
                    os.killpg(wrapper, signal.SIGKILL)
        for suffix in ("pid", "shutdown", "owner", "hosted", "version", "stopping"):
            with contextlib.suppress(OSError):
                Path(f"{WATCHER}{self.sid}.{suffix}").unlink()


@pytest.fixture
def agent():
    proc, owner = spawn_agent()
    yield proc
    kill_agent(proc)


@pytest.fixture(params=["watch", "service"])
def host(request, service_home, stub, agent):
    h = Host(request.param, service_home, stub, agent.pid)
    try:
        yield h
    finally:
        h.cleanup()


def _delivered(host: Host, count: int, timeout: float = 20) -> None:
    assert wait_for(lambda: len(host.stub.lines(host.sid)) >= count, timeout), (
        f"{host.kind}: the server has lines {host.stub.lines(host.sid)}, {count} written ({host.facts()})"
    )


def _exactly_once(host: Host) -> None:
    assert host.stub.lines(host.sid) == list(range(host.written)), "every line once, in order"
    assert host.stub.violations == [], host.stub.violations


# -- the tests ----------------------------------------------------------------------------


def test_every_line_reaches_the_server_once_in_order_and_the_end_finalizes(host):
    host.write(3)
    host.start()
    _delivered(host, 3)
    host.write(2)  # the live tail
    _delivered(host, 5)
    assert not host.stub.finalized(host.sid), "a live session is not finalized"
    host.end()
    assert wait_for(lambda: host.stub.finalized(host.sid), 5), host.facts()
    _exactly_once(host)
    assert wait_for(host.gone, 10), f"{host.kind}: the recorder outlived its session ({host.facts()})"


def test_a_host_killed_mid_session_loses_no_line_and_sends_none_twice(host):
    host.write(3)
    host.start()
    _delivered(host, 3)
    host.crash()
    host.write(3)  # written while nothing records
    host.recover()
    _delivered(host, 6, timeout=30)
    host.write(1)
    _delivered(host, 7)
    host.end()
    assert wait_for(lambda: host.stub.finalized(host.sid), 5), host.facts()
    _exactly_once(host)


def test_an_agent_killed_without_session_end_is_finalized_by_its_recorder(host, agent):
    host.write(2)
    host.start()
    _delivered(host, 2)
    kill_agent(agent)  # SIGKILL: no SessionEnd will come
    assert wait_for(lambda: host.stub.finalized(host.sid), 15), f"{host.kind}: never finalized ({host.facts()})"
    _exactly_once(host)
    assert wait_for(host.gone, 15), f"{host.kind}: the recorder outlived its agent ({host.facts()})"


def test_an_outage_keeps_every_line_and_sends_it_once_the_server_is_back(host):
    host.stub.down.set()
    host.write(3)
    host.start()
    assert wait_for(lambda: len(host.stub.bodies) >= 2, 15), "the recorder kept trying"
    assert host.stub.lines(host.sid) == []
    host.write(2)
    host.stub.down.clear()
    _delivered(host, 5)
    host.end()
    assert wait_for(lambda: host.stub.finalized(host.sid), 5), host.facts()
    _exactly_once(host)


def test_a_folder_switched_off_mid_session_ships_nothing_more(host):
    host.write(2)
    host.start()
    _delivered(host, 2)
    (host.plugin_dir / ".disabled_paths").write_text(f"{host.cwd}\n")
    time.sleep(3)  # three ticks: the recorder has seen the switch
    host.write(3)
    time.sleep(4)
    host.end()
    time.sleep(1)
    assert host.stub.lines(host.sid) == [0, 1], "nothing after the switch"
    assert not host.stub.finalized(host.sid)
    assert host.stub.violations == []


def test_a_credential_in_the_transcript_never_leaves_the_machine(host):
    host.write(1)
    host.write(1, text=f"here is my token {SECRET} keep it")
    host.start()
    _delivered(host, 2)
    host.end()
    assert wait_for(lambda: host.stub.finalized(host.sid), 5), host.facts()
    assert host.stub.bodies and not any(SECRET.encode() in body for body in host.stub.bodies)
    _exactly_once(host)


# -- the service's own: a restart on purpose -------------------------------------------------


def test_a_service_restart_pauses_the_real_recorder_and_the_next_resumes_it(service_home, stub, agent):
    """A service stop (an update, `probe service stop`) pauses each recorder:
    no FINALIZE, the session goes on. The next service resumes it from its saved
    progress, and lines written in between go once."""
    h = Host("service", service_home, stub, agent.pid)
    try:
        h.write(2)
        h.start()
        _delivered(h, 2)
        pid = service_home.status()["pid"]
        service_home.call(Method.STOP)
        assert service_home.wait_exit(pid, 10), "the service stopped"
        assert not stub.finalized(h.sid), "a restart is not the session's end"
        h.write(2)
        h.recover()
        assert service_home.status()["pid"] != pid
        _delivered(h, 4)
        h.end()
        assert wait_for(lambda: stub.finalized(h.sid), 5), h.facts()
        _exactly_once(h)
    finally:
        h.cleanup()


# -- the service's recorder row says who owns the recording ------------------------------------------


def _row(service_home, sid: str) -> dict | None:
    status = service_home.status() or {}
    return next((row for row in status.get("recorders") or [] if row.get("sid") == sid), None)


def test_the_services_recorder_row_says_it_records_the_session(service_home, stub, agent):
    h = Host("service", service_home, stub, agent.pid)
    try:
        h.write(2)
        h.start()
        _delivered(h, 2)
        assert wait_for(lambda: (_row(service_home, h.sid) or {}).get("recording") is True, 10), _row(
            service_home, h.sid)
        h.end()
    finally:
        h.cleanup()


def test_a_just_started_session_is_recorded_from_its_recorders_first_pass(service_home, stub, agent):
    """Live run 39936954062: a session's transcript has no line when its
    recorder starts, and the recorder took the session's claim only once a line
    proved the transcript's identity, a sync interval (60 s) later: `recording`
    read false for the first minute. The claim now comes on the first pass."""
    h = Host("service", service_home, stub, agent.pid)
    h.env["PROBE_RESEARCH_TAP_INTERVAL_SECONDS"] = "60"  # the real cadence
    try:
        h.start()  # nothing written yet
        assert wait_for(lambda: (_row(service_home, h.sid) or {}).get("recording") is True, 10), _row(
            service_home, h.sid)
        h.write(2)
        h.end()  # its last pass takes what was written
        assert wait_for(lambda: stub.finalized(h.sid), 10), h.facts()
        _exactly_once(h)
    finally:
        h.cleanup()


def test_a_recorder_its_sessions_tap_watch_outran_says_it_records_nothing(service_home, stub, agent):
    """Codex R2 on 22154ffa0: the session's own `tap watch` holds the journal's
    claim, so the service's recorder for it returns at once and waits to try
    again: its thread is alive, yet `tap watch` records every line. The row
    says `recording: false`, and the lines still go once."""
    h = Host("watch", service_home, stub, agent.pid)
    try:
        h.write(2)
        h.start()
        _delivered(h, 2)
        env = {**h.env, "PROBE_TAP_HOSTED": "1"}
        done = subprocess.run(
            [sys.executable, "-m", "tap", "record", "--session-id", h.sid, "--cwd", str(h.cwd), "--transcript",
             str(h.transcript), "--plugin-root", str(TAP_ROOT)],
            env=env, cwd=str(h.cwd), capture_output=True, text=True, timeout=30, check=False)
        assert done.returncode == 0, done.stderr
        Path(f"{WATCHER}{h.sid}.hosted").unlink(missing_ok=True)  # the watch host's own view stays its own
        assert wait_for(lambda: (_row(service_home, h.sid) or {}).get("alive") is True, 10)
        time.sleep(3)  # its loop has met the claim and returned to its retry wait
        row = _row(service_home, h.sid)
        assert row and row["alive"] is True and row["recording"] is False, row
        h.write(2)
        _delivered(h, 4)
        # Its SessionEnd, as the hook sends it with the marker there: the
        # service's recorder finishes without ever taking the session over.
        assert service_home.call(Method.SESSION_FINISH, {"sid": h.sid, "wait": 10}) == {
            "recording": True, "finished": True}
        h.end()
        assert wait_for(lambda: h.stub.finalized(h.sid), 10), h.facts()
        _exactly_once(h)
    finally:
        h.cleanup()


# -- a session `tap watch` took at its start is handed to the service ---------------------------------


def test_a_session_tap_watch_took_at_its_start_is_handed_to_the_service(service_home, stub, agent, monkeypatch):
    """Live run 39933153434: sessions started at the instant an update landed
    got `tap watch` (the service could not be reached), and kept it for their
    whole life. Now the watcher asks the service once it is back, lets go of
    the journal's claim, and leaves once the service's recorder holds it: the
    wrapper ends with it, and every line still goes once, in order."""
    monkeypatch.setenv("PROBE_SERVICE_RECORDER_RETRY_S", "0.2")  # a taken claim is tried again in 0.6 s
    h = Host("service", service_home, stub, agent.pid)
    h.env["PROBE_TAP_HANDBACK_S"] = "1"
    runtime = paths.runtime_path()
    saved = runtime.read_text(encoding="utf-8")
    try:
        # SessionStart while no service can start (its interpreter is being replaced).
        runtime.write_text(json.dumps({"python": "/nonexistent/python3", "cli_version": "test"}), encoding="utf-8")
        h.write(3)
        Path(f"{WATCHER}{h.sid}.owner").write_text(json.dumps(
            {"pid": h.agent_pid, "start": procid.start_time(h.agent_pid), "name": "claude"}))
        done = subprocess.run(
            [sys.executable, "-m", "tap", "start", "--session-id", h.sid, "--cwd", str(h.cwd),
             "--transcript", str(h.transcript)],
            env=h.env, cwd=str(h.cwd), capture_output=True, text=True, timeout=30, check=False,
        )
        assert done.returncode == 0, done.stderr
        assert wait_for(lambda: h.watch_pid() is not None, 10), f"no tap watch fallback ({h.facts()})"
        _delivered(h, 3)
        wrapper = h.wrapper_pid()
        assert h.hosted_pid() is None

        runtime.write_text(saved, encoding="utf-8")  # the update is done: the service can start again
        status = service_home.start()
        assert wait_for(lambda: h.hosted_pid() == status["pid"] and h.wrapper_pid() is None, 30), h.facts()
        assert wait_for(lambda: not pid_running(wrapper), 10), "the wrapper ended with its tap watch"
        assert (_row(service_home, h.sid) or {}).get("recording") is True, _row(service_home, h.sid)
        assert not stub.finalized(h.sid), "a hand-over is not the session's end"

        h.write(2)  # recorded by the service now
        _delivered(h, 5)
        h.end()
        assert wait_for(lambda: stub.finalized(h.sid), 10), h.facts()
        _exactly_once(h)
        assert wait_for(h.gone, 10), h.facts()
    finally:
        if not runtime.is_file() or runtime.read_text(encoding="utf-8") != saved:
            runtime.write_text(saved, encoding="utf-8")
        h.cleanup()
