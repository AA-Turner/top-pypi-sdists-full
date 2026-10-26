"""Probe off means the session is not captured (the owner's decision, 2026-10-24).

A real Probe service in a throwaway HOME, the real tap package it loads
(`plugins/probe-research-tap`, unchanged: the tap every running session
already has), and a stub of the ingest routes over real HTTP
(`capture_stub.IngestStub`). Each test writes transcript lines, moves the
session's switch the way the CLI does (its `.state` file, then
`session.recording`, which `probe session state` asks right after), and reads
what reached the server: no line written while the switch read `off` ever
does, and every line written after it moved back does.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pytest

from probe.service.protocol import Method
from tests.capture_stub import IngestStub
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401

pytestmark = [
    pytest.mark.skipif(os.name != "posix", reason="the service records sessions on POSIX here"),
    pytest.mark.heavy,
]

TAP_ROOT = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap"
TAP_VERSION = next(
    line.split('"')[1] for line in (TAP_ROOT / "tap" / "__init__.py").read_text().splitlines()
    if line.startswith("__version__")
)
STAMP = "2026-10-24T12:00:00.000Z"


# -- each harness's transcript ------------------------------------------------------


@dataclass(frozen=True)
class Harness:
    id: str
    token_env: str
    #: (session id, cwd) -> the transcript's header record, or None.
    header: Callable[[str, str], dict] | None
    #: (session id, text) -> one researcher prompt.
    line: Callable[[str, str], dict]

    def transcript(self, home: Path, sid: str) -> Path:
        if self.id == "codex":
            return home / "codex-sessions" / "2026" / "10" / "24" / f"rollout-2026-10-24T12-00-00-{sid}.jsonl"
        if self.id == "kimi_code":
            return home / ".kimi-code" / "sessions" / "work" / f"session_{sid}" / "agents" / "main" / "wire.jsonl"
        return home / f"{sid}.jsonl"

    def start(self, home: Path, sid: str) -> Path:
        path = self.transcript(home, sid)
        path.parent.mkdir(parents=True, exist_ok=True)
        if self.id == "kimi_code":
            (path.parents[2] / "state.json").write_text(json.dumps({"id": f"session_{sid}", "cwd": str(home)}))
        path.write_text(json.dumps(self.header(sid, str(home))) + "\n" if self.header else "")
        return path

    def params(self, home: Path, sid: str, owner: dict, stub: IngestStub, **env) -> dict:
        path = self.transcript(home, sid)
        return {
            "sid": sid, "harness": self.id, "mode": "inline", "owner": owner, "generation": int(time.time() * 1000),
            "state_dir": str(_state_dir(home)), "cwd": str(home),
            "transcript": None if self.id == "codex" else str(path),
            "transcript_dir": str(home / "codex-sessions") if self.id == "codex" else None,
            "tap_root": str(TAP_ROOT), "tap_version": TAP_VERSION, "env": _env(home, stub, self, **env),
        }


HARNESSES = {
    "claude_code": Harness(
        "claude_code", "PROBE_INGEST_TOKEN", None,
        lambda sid, text: {"type": "user", "sessionId": sid, "uuid": str(uuid.uuid4()), "timestamp": STAMP,
                           "message": {"role": "user", "content": text}},
    ),
    "codex": Harness(
        "codex", "PRBE_CODEX_TAP_TOKEN",
        lambda sid, cwd: {"timestamp": STAMP, "type": "session_meta", "payload": {"id": sid, "cwd": cwd}},
        lambda sid, text: {"timestamp": STAMP, "type": "response_item",
                           "payload": {"type": "message", "role": "user",
                                       "content": [{"type": "input_text", "text": text}]}},
    ),
    "pi": Harness(
        "pi", "PROBE_PI_TAP_TOKEN",
        lambda sid, cwd: {"type": "session", "version": 3, "id": sid, "timestamp": STAMP, "cwd": cwd},
        lambda sid, text: {"type": "message", "id": uuid.uuid4().hex[:8], "parentId": None, "timestamp": STAMP,
                           "message": {"role": "user", "content": [{"type": "text", "text": text}],
                                       "timestamp": 1792929600000}},
    ),
    "kimi_code": Harness(
        "kimi_code", "PROBE_KIMI_TAP_TOKEN",
        lambda sid, cwd: {"type": "metadata", "protocol_version": "1", "created_at": STAMP},
        lambda sid, text: {"type": "context.append_message", "agentId": "main", "time": 1,
                           "message": {"role": "user", "content": [{"type": "text", "text": text}], "toolCalls": [],
                                       "origin": {"kind": "user"}}},
    ),
}
CLAUDE = HARNESSES["claude_code"]


# -- fixtures ----------------------------------------------------------------------


@pytest.fixture
def stub():
    server = IngestStub().start()
    yield server
    server.stop()


@pytest.fixture
def agent():
    proc, owner = spawn_agent()
    yield proc, owner
    kill_agent(proc)


def _new_sid() -> str:
    return str(uuid.uuid4())


def _watchers(home: Path) -> Path:
    """The tap's watcher files of these tests (`PROBE_TAP_WATCHER_DIR`, read on
    every OS from tap 0.10.19): inside the test's own HOME, never the shared
    `/tmp`, so nothing is left there by a service that stops after the test."""
    folder = home / "tap-watchers"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


@pytest.fixture
def sid():
    return _new_sid()


@pytest.fixture
def other_sid():
    return _new_sid()


def _env(home: Path, stub: IngestStub, harness: Harness = CLAUDE, **extra) -> dict:
    return {
        "HOME": str(home), "PATH": os.environ.get("PATH", "/usr/bin:/bin"), "PROBE_BASE_URL": stub.base_url,
        "PROBE_TAP_WATCHER_DIR": str(_watchers(home)),
        harness.token_env: "synthetic", "PROBE_TAP_SOURCE": harness.id,
        "PROBE_RESEARCH_TAP_ACTIVE_INTERVAL_SECONDS": "1", "PROBE_RESEARCH_TAP_IDLE_INTERVAL_SECONDS": "1",
        **extra,
    }


def _state_dir(home: Path) -> Path:
    return home / ".local" / "state" / "probe"


def _switch(home: Path, sid: str, state: str) -> None:
    """What `session_marker.set_session_state` writes."""
    folder = _state_dir(home) / "sessions"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{sid}.state").write_text(state + "\n", encoding="utf-8")


def _machine_default(home: Path, state: str) -> None:
    """`probe session default <state>`: the machine's default for new sessions."""
    path = home / ".config" / "probe" / "config.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"defaults": {"session_state": state}}), encoding="utf-8")


def _write(harness: Harness, transcript: Path, sid: str, *texts: str) -> None:
    with transcript.open("a", encoding="utf-8") as handle:
        for text in texts:
            handle.write(json.dumps(harness.line(sid, text)) + "\n")


def _sent(stub: IngestStub, sid: str, text: str, timeout: float = 20.0) -> bool:
    return bool(wait_for(lambda: text in stub.sent_text(sid), timeout, 0.1))


def _covers(stub: IngestStub, sid: str, transcript: Path, timeout: float = 20.0) -> bool:
    """The server's cursor reached the transcript's end: every byte is accounted
    for (sent, or skipped as nothing), so no recorder can ever send it again."""
    size = transcript.stat().st_size
    return bool(wait_for(lambda: (stub.stream(sid) or {}).get("source_byte_end") == size, timeout, 0.1))


def _hosted_marker(home: Path, harness: Harness, sid: str) -> str | None:
    prefix = "prbe-codex-tap" if harness.id == "codex" else "probe-research-tap"
    try:
        return (_watchers(home) / f"{prefix}-watcher-{sid}.hosted").read_text().strip()
    except OSError:
        return None


def _owner_file(home: Path, sid: str, owner: dict) -> None:
    """What SessionStart's `tap owner` writes: the agent that owns the session."""
    (_watchers(home) / f"probe-research-tap-watcher-{sid}.owner").write_text(
        json.dumps({"pid": owner["pid"], "start": owner["start_time"], "name": "claude"}))


# -- the switch moved mid-session ------------------------------------------------------


@pytest.mark.parametrize("harness", list(HARNESSES.values()), ids=list(HARNESSES))
def test_lines_written_while_off_are_never_sent_and_capture_resumes_from_the_flip(
    service_home, stub, agent, sid, harness
):
    _proc, owner = agent
    home = service_home.home
    transcript = harness.start(home, sid)
    _switch(home, sid, "full")
    _write(harness, transcript, sid, "on-before-1", "on-before-2")
    service_home.start()
    answer = service_home.call(Method.SESSION_RECORD, harness.params(home, sid, owner, stub))
    assert answer["recording"] is True and "off" not in answer
    assert _sent(stub, sid, "on-before-2"), service_home.log()

    _switch(home, sid, "off")
    looked = service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(harness, transcript, sid, "SECRET-while-off-1", "SECRET-while-off-2")
    time.sleep(4)  # four of the tap's 1 s passes
    assert "SECRET" not in stub.sent_text(sid)
    assert looked == {"recording": True, "off": True}
    row = next(r for r in service_home.call(Method.STATUS)["recorders"] if r["sid"] == sid)
    assert row["off"] is True

    _switch(home, sid, "full")
    assert service_home.call(Method.SESSION_RECORDING, {"sid": sid}) == {"recording": True}
    _write(harness, transcript, sid, "on-after-1", "on-after-2")
    assert _sent(stub, sid, "on-after-2"), service_home.log()
    assert _covers(stub, sid, transcript), (stub.stream(sid), transcript.stat().st_size)
    sent = stub.sent_text(sid)
    assert "SECRET" not in sent
    assert all(text in sent for text in ("on-before-1", "on-before-2", "on-after-1", "on-after-2"))

    # Its end: finalized, and still nothing of what was written while off.
    finished = service_home.call(Method.SESSION_FINISH, {"sid": sid, "wait": 15})
    assert finished["finished"] is True
    assert (stub.stream(sid) or {}).get("finalized") is True
    assert "SECRET" not in stub.sent_text(sid)


def test_off_from_the_machine_default_sends_nothing_until_switched_on(service_home, stub, agent, sid):
    """A session nobody switched, on a machine whose default is `off`: nothing
    of it reaches the server, not even a question about it, until the switch
    moves to on; from then on it is captured from that moment."""
    _proc, owner = agent
    home = service_home.home
    _machine_default(home, "off")
    transcript = CLAUDE.start(home, sid)
    _write(CLAUDE, transcript, sid, "SECRET-from-the-start-1", "SECRET-from-the-start-2")
    status = service_home.start()
    answer = service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    _write(CLAUDE, transcript, sid, "SECRET-from-the-start-3")
    time.sleep(4)
    assert stub.asked_about(sid) == []
    # Taken (no `tap watch` starts for it), held: this service's pid while it
    # runs, as for any session it takes.
    assert answer["recording"] is True and answer["off"] is True and answer["pid"] == status["pid"]

    _switch(home, sid, "full")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "on-after-1")
    assert _sent(stub, sid, "on-after-1"), service_home.log()
    assert _covers(stub, sid, transcript)
    assert "SECRET" not in stub.sent_text(sid)


def test_a_session_that_ends_while_off_is_finalized_without_its_off_lines(service_home, stub, agent, sid):
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-1")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1", "SECRET-2")
    time.sleep(2)

    finished = service_home.call(Method.SESSION_FINISH, {"sid": sid, "wait": 15})
    assert finished["finished"] is True
    stream = stub.stream(sid) or {}
    assert stream.get("finalized") is True
    assert stream.get("source_byte_end") == transcript.stat().st_size
    assert "SECRET" not in stub.sent_text(sid)


def test_an_off_session_that_never_sent_anything_ends_sending_nothing(service_home, stub, agent, sid):
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "off")
    _write(CLAUDE, transcript, sid, "SECRET-1")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    finished = service_home.call(Method.SESSION_FINISH, {"sid": sid, "wait": 15})
    assert finished["finished"] is True
    assert stub.asked_about(sid) == []


def test_the_off_stretch_survives_a_service_restart(service_home, stub, agent, sid):
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-1")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    service_home.call(Method.STOP)
    assert service_home.wait_exit(first["pid"], 10)
    # No service may run for it while it is off: its own agent stands in the marker.
    assert _hosted_marker(home, CLAUDE, sid) == str(owner["pid"])
    _write(CLAUDE, transcript, sid, "SECRET-2")

    service_home.start()
    assert wait_for(lambda: any(r["sid"] == sid and r["off"] for r in service_home.call(Method.STATUS)["recorders"]), 10)
    _write(CLAUDE, transcript, sid, "SECRET-3")
    _switch(home, sid, "full")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "on-2")
    assert _sent(stub, sid, "on-2"), service_home.log()
    assert _covers(stub, sid, transcript)
    assert "SECRET" not in stub.sent_text(sid)


def test_an_off_session_never_keeps_the_service_alive(service_home, stub, agent, sid, monkeypatch):
    """Probe off starts nothing and keeps nothing running: the service a tap's
    `tap record` started for an off session goes idle and exits while that
    session's agent still runs, and nothing asks it again every minute (live
    test, bug F: refused `owner_gone` and asked again every 60 s)."""
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "1")
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "off")
    _write(CLAUDE, transcript, sid, "SECRET-1")
    status = service_home.start()
    answer = service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert answer["recording"] is True and answer["off"] is True
    listed = {s["sid"]: s for s in service_home.call(Method.SESSION_LIST, {"receipts": False})["sessions"]}
    assert listed[sid]["mode"] == "off" and listed[sid]["agent_live"] is True
    assert service_home.wait_exit(status["pid"], 15), service_home.log()
    assert agent[0].poll() is None  # its agent still runs
    assert "owner_gone" not in service_home.log()
    assert stub.asked_about(sid) == []


# -- other recorders of this service ----------------------------------------------------


def test_another_sessions_recorder_never_sends_an_off_sessions_lines(service_home, stub, agent, sid, other_sid):
    """Every recorder drains every session of its journal (the tap's shared
    drain) and adopts transcripts it has a log for and no row (its gap sweep):
    neither ever touches a session that is off."""
    _proc, owner = agent
    home = service_home.home
    projects = home / ".claude" / "projects" / "work"
    projects.mkdir(parents=True)
    # B: recorded here, on and then off.
    b_path = projects / f"{sid}.jsonl"
    _switch(home, sid, "full")
    _write(CLAUDE, b_path, sid, "b-on-1")
    # C: off from its start, recorded by nobody, with a tap log (the gap sweep's proof it was ours).
    c_path = projects / f"{other_sid}.jsonl"
    _switch(home, other_sid, "off")
    _write(CLAUDE, c_path, other_sid, "SECRET-c-1")
    logs = home / ".claude" / "plugins" / "probe-research-tap" / "logs"
    logs.mkdir(parents=True)
    (logs / f"{other_sid}.log").write_text("tap: session started\n")
    service_home.start()
    b = CLAUDE.params(home, sid, owner, stub)
    b["transcript"] = str(b_path)
    service_home.call(Method.SESSION_RECORD, b)
    assert _sent(stub, sid, "b-on-1")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, b_path, sid, "SECRET-b-1")
    # A: on throughout, recorded here: its passes drain B and sweep for gaps.
    a_sid = _new_sid()
    a_path = projects / f"{a_sid}.jsonl"
    _switch(home, a_sid, "full")
    _write(CLAUDE, a_path, a_sid, "a-on-1")
    a = CLAUDE.params(home, a_sid, owner, stub)
    a["transcript"] = str(a_path)
    service_home.call(Method.SESSION_RECORD, a)
    assert _sent(stub, a_sid, "a-on-1")
    for i in range(12):  # past RECONCILE_EVERY_TICKS of A's 1 s passes
        _write(CLAUDE, a_path, a_sid, f"a-on-{i + 2}")
        _write(CLAUDE, b_path, sid, f"SECRET-b-{i + 2}")
        time.sleep(1)
    assert _sent(stub, a_sid, "a-on-13")
    assert "SECRET" not in stub.sent_text(sid)
    assert stub.asked_about(other_sid) == []


# -- an older tap against this service --------------------------------------------------


def _tap_env(home: Path, stub: IngestStub, **extra) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("PROBE_", "PRBE_", "XDG_"))}
    env.update(_env(home, stub), PYTHONPATH=str(TAP_ROOT), PROBE_TAP_HOSTED="1")
    env.update(extra)  # a test's own say wins (PROBE_TAP_HOSTED="0" included)
    return env


def test_an_old_tap_record_of_an_off_session_starts_no_tap_watch(service_home, stub, agent, sid):
    """`tap record` (SessionStart's, from the tap every running session has):
    taken, so the hook starts no `tap watch`. The `.hosted` marker names this
    service while it runs (a `tap watch` racing it reads the session as
    recorded by the service, and leaves it); once the service goes idle it
    names the session's own agent, which the UserPromptSubmit hook's fast path
    reads as alive (no service start, no `tap watch`, every prompt)."""
    proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "off")
    _write(CLAUDE, transcript, sid, "SECRET-1")
    status = service_home.start()
    _owner_file(home, sid, owner)
    done = subprocess.run(
        [sys.executable, "-m", "tap", "record", "--session-id", sid, "--cwd", str(home),
         "--transcript", str(transcript), "--plugin-root", str(TAP_ROOT)],
        env=_tap_env(home, stub), capture_output=True, text=True, timeout=30,
    )
    assert done.returncode == 0, (done.stdout, done.stderr, service_home.log())
    assert _hosted_marker(home, CLAUDE, sid) == str(status["pid"])
    time.sleep(3)
    assert stub.asked_about(sid) == []
    service_home.call(Method.STOP)
    assert service_home.wait_exit(status["pid"], 10)
    assert _hosted_marker(home, CLAUDE, sid) == str(owner["pid"])


def test_the_service_holds_an_off_sessions_claim_so_a_watcher_hands_it_over(service_home, stub, agent, sid):
    """A `tap watch` of an off session (an older tap's code, which records what
    it records until it hands over: here, what was there when it started)
    offers its session to the service. Before this the service registered it
    `off`, answered `owner_gone` and asked again a minute later while the
    watcher recorded on (live test, bug F). Now the service takes it and holds
    its claim, so the watcher lets go, sees the service's recorder hold it
    (`service.status` `recording`), and exits 12 without a last pass; nothing
    written from then on is sent."""
    proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "off")
    _write(CLAUDE, transcript, sid, "before-the-watcher-1")
    service_home.start()
    _owner_file(home, sid, owner)
    watcher = subprocess.Popen(
        [sys.executable, "-m", "tap", "watch", "--session-id", sid, "--cwd", str(home), "--transcript",
         str(transcript), "--plugin-root", str(TAP_ROOT)],
        env=_tap_env(home, stub, PROBE_TAP_HANDBACK_S="2"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        code = watcher.wait(timeout=60)
        assert code == 12, service_home.log()
        assert any(r["sid"] == sid and r["off"] for r in service_home.call(Method.STATUS)["recorders"])
        _write(CLAUDE, transcript, sid, "SECRET-after-hand-over")
        time.sleep(3)
        assert "SECRET" not in stub.sent_text(sid)
        assert "owner_gone" not in service_home.log()
    finally:
        if watcher.poll() is None:
            watcher.kill()
            watcher.wait(timeout=10)


# -- the CLI that moves the switch -------------------------------------------------------


def test_switching_on_after_the_service_went_idle_captures_from_the_flip(service_home, stub, agent, sid, monkeypatch):
    """A held session lets its service go idle. `probe session state on` (the
    CLI's `capture_switched`) starts it again and has it look at once, so the
    session is captured from the move, never the stretch before it; `off`
    never starts it."""
    from probe.cli import service_calls

    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "1")
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-1")
    _switch(home, sid, "off")
    assert service_calls.capture_switched(sid, off=True) is True
    _write(CLAUDE, transcript, sid, "SECRET-1")
    assert service_home.wait_exit(first["pid"], 15), service_home.log()
    _write(CLAUDE, transcript, sid, "SECRET-2")
    assert service_calls.capture_switched(sid, off=True) is None
    assert service_home.service_processes() == []

    _switch(home, sid, "full")
    assert service_calls.capture_switched(sid, off=False) is True
    _write(CLAUDE, transcript, sid, "on-2")
    assert _sent(stub, sid, "on-2"), service_home.log()
    assert _covers(stub, sid, transcript)
    assert "SECRET" not in stub.sent_text(sid)


def test_read_only_is_unchanged_its_transcript_still_uploads(service_home, stub, agent, sid):
    """`read` is out of this decision's scope and unchanged: the tap uploads a
    read-only session's transcript as it always did (the `probe` skill's "records
    nothing" is about Probe's writes, not the transcript). Pinned so that a
    change to it is a decision, not an accident."""
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "read-only")
    _write(CLAUDE, transcript, sid, "read-only-1")
    service_home.start()
    answer = service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert answer["recording"] is True and "off" not in answer
    assert _sent(stub, sid, "read-only-1"), service_home.log()



# -- the review's findings: durable gaps, the server down at the end, the settle race ---------


@pytest.fixture
def stub3():
    server = IngestStub(protocol=3).start()
    yield server
    server.stop()


def test_protocol_3_skips_the_off_stretch_as_nothing_too(service_home, stub3, agent, sid):
    """On protocol 3 (fragments, the door's `ready` stream) the off stretch is
    covered by a batch with no fragment for it, and finalized after."""
    stub = stub3
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-before")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-before"), service_home.log()
    assert stub.stream(sid)["protocol_version"] == 3
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    _switch(home, sid, "full")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "on-after")
    assert _sent(stub, sid, "on-after"), service_home.log()
    assert _covers(stub, sid, transcript)
    assert service_home.call(Method.SESSION_FINISH, {"sid": sid, "wait": 15})["finished"] is True
    assert stub.stream(sid)["finalized"] is True
    assert "SECRET" not in stub.sent_text(sid)


def _gap_file(home: Path, sid: str) -> Path:
    return _state_dir(home) / "sessions" / f"{sid}.gaps"


def test_a_session_that_never_sent_anything_keeps_its_gaps_for_a_later_capture(service_home, stub, agent, sid):
    """Off from its first line, ended, nothing sent: its gap file stays. Picked
    up again later with its switch reading on (its `.state` pruned, or the
    default changed), it is captured from where it was resumed, never from its
    first line."""
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "off")
    _write(CLAUDE, transcript, sid, "SECRET-1", "SECRET-2")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert service_home.call(Method.SESSION_FINISH, {"sid": sid, "wait": 15})["finished"] is True
    assert stub.asked_about(sid) == []
    assert json.loads(_gap_file(home, sid).read_text())["gaps"] == [[0, None]]

    (_state_dir(home) / "sessions" / f"{sid}.state").unlink()  # pruned: it reads as the default, on
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    _write(CLAUDE, transcript, sid, "on-after-the-resume")
    assert _sent(stub, sid, "on-after-the-resume"), service_home.log()
    assert _covers(stub, sid, transcript)
    assert "SECRET" not in stub.sent_text(sid)


def _record_other(service_home, stub, home: Path, owner: dict, *texts: str) -> tuple[str, Path]:
    """Session A, on throughout, recorded here: its passes drain every session
    of the journal and sweep for gaps."""
    a_sid = _new_sid()
    a_path = CLAUDE.start(home, a_sid)
    _switch(home, a_sid, "full")
    _write(CLAUDE, a_path, a_sid, *texts)
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, a_sid, owner, stub))
    return a_sid, a_path


def test_gaps_outlive_a_lost_recorders_json_and_a_pruned_state(service_home, stub, agent, sid):
    """B held off; its service gone, `recorders.json` lost and its `.state`
    pruned: another session's recorder in the next service still sends none
    of what B wrote while off (its gap file)."""
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "b-on")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "b-on")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    service_home.call(Method.STOP)
    assert service_home.wait_exit(first["pid"], 10)
    (service_home.service_dir / "recorders.json").unlink()
    (_state_dir(home) / "sessions" / f"{sid}.state").unlink()
    _write(CLAUDE, transcript, sid, "SECRET-2")

    service_home.start()
    a_sid, a_path = _record_other(service_home, stub, home, owner, "a-on-1")
    assert _sent(stub, a_sid, "a-on-1"), service_home.log()
    for i in range(12):  # past RECONCILE_EVERY_TICKS of A's 1 s passes
        _write(CLAUDE, a_path, a_sid, f"a-on-{i + 2}")
        time.sleep(1)
    assert _sent(stub, a_sid, "a-on-13")
    assert "SECRET" not in stub.sent_text(sid)


def test_a_session_that_ends_while_off_with_the_server_down_is_finished_later(service_home, stub, agent, sid,
                                                                               monkeypatch):
    """Ended while off, the server refusing every batch: never given up. Its
    service goes idle with it saved; no other session's recorder sends its off
    stretch meanwhile; the next service finishes it once the server is back,
    without the stretch."""
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "1")
    proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-1")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    stub.refusing = True
    kill_agent(proc)  # its agent ends: the session ends while off
    assert service_home.wait_exit(first["pid"], 40), service_home.log()
    saved = json.loads((service_home.service_dir / "recorders.json").read_text())
    assert [s["sid"] for s in saved["sessions"]] == [sid]
    assert saved["sessions"][0].get("capture_deferred") is True
    assert json.loads(_gap_file(home, sid).read_text())["gaps"]

    # The server still down: the next service resumes it deferred, so it does
    # not keep itself up for three finishing tries (at least 6 s) again.
    second = service_home.start()
    assert service_home.wait_exit(second["pid"], 3.5), service_home.log()
    saved = json.loads((service_home.service_dir / "recorders.json").read_text())
    assert [s["sid"] for s in saved["sessions"]] == [sid]

    stub.refusing = False
    service_home.start()
    assert wait_for(lambda: (stub.stream(sid) or {}).get("finalized") is True, 30), service_home.log()
    assert stub.stream(sid)["source_byte_end"] == transcript.stat().st_size
    assert "SECRET" not in stub.sent_text(sid)
    assert wait_for(lambda: not _gap_file(home, sid).exists(), 10)


def test_switching_off_again_while_a_settle_runs_sends_nothing_written_meanwhile(service_home, stub, agent, sid):
    """Off, on (its settle starts, the server slow), off again before the
    settle ends: what is written after the second move is never sent."""
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-1")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    # Its loop has left and its recorder holds it (`last` says so).
    assert wait_for(lambda: any(r["sid"] == sid and r["last"] == "off"
                                for r in service_home.call(Method.STATUS)["recorders"]), 10)
    stub.delay_s = 3.0
    _switch(home, sid, "full")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    time.sleep(1.0)  # its settle's batch is in flight now
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-2-written-while-off-again")
    time.sleep(6)
    stub.delay_s = 0.0
    time.sleep(3)
    assert "SECRET" not in stub.sent_text(sid)
    _switch(home, sid, "full")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "on-2")
    assert _sent(stub, sid, "on-2"), service_home.log()
    assert _covers(stub, sid, transcript)
    assert "SECRET" not in stub.sent_text(sid)


def test_the_keeper_never_restarts_the_service_for_a_session_that_is_off(service_home, stub, agent, sid, monkeypatch):
    """The OS keeper starts the service while a session it recorded has its
    agent running. Not for one held because Probe is off (no restart every
    minute, no false `service_down`); once its switch reads on, it does, so
    the session is recorded again within a minute even if nothing told the
    service."""
    from probe.service import keeper

    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "1")
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "off")
    _write(CLAUDE, transcript, sid, "SECRET-1")
    status = service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert service_home.wait_exit(status["pid"], 15), service_home.log()
    assert keeper.needed() is False
    _switch(home, sid, "full")
    assert keeper.needed() is True


def _saved_sids(service_home) -> list[str]:
    try:
        saved = json.loads((service_home.service_dir / "recorders.json").read_text())
    except (OSError, ValueError):
        return []
    return [s["sid"] for s in saved.get("sessions") or []]


def _rows(service_home, sid: str) -> list[dict]:
    return [r for r in (service_home.call(Method.STATUS) or {}).get("recorders") or [] if r["sid"] == sid]


def test_a_resume_after_ending_off_with_the_server_down_is_recorded_by_the_new_recorder_alone(
        service_home, stub, agent, sid, monkeypatch):
    """Ended while off and not finished (the server down), then resumed (pi
    `--continue`, a Codex resume): the old recorder, retrying, never closes its
    stale gap over what the resumed session writes, never finalizes the live
    session, never lifts the gaps the new one still has to settle."""
    monkeypatch.setenv("PROBE_SERVICE_RECORDER_RETRY_S", "0.5")
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-1")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    stub.refusing = True
    service_home.call(Method.SESSION_FINISH, {"sid": sid, "wait": 0})
    assert wait_for(lambda: any(r["last"] == "ended off: not finished yet" for r in _rows(service_home, sid)), 30), \
        service_home.log()

    _switch(home, sid, "full")
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))  # the resume
    _write(CLAUDE, transcript, sid, "on-after-resume-1")
    time.sleep(3)  # the ended recorder's retries (from 0.5 s) come round meanwhile
    assert json.loads(_gap_file(home, sid).read_text())["gaps"][0][1] < transcript.stat().st_size
    stub.refusing = False
    assert _sent(stub, sid, "on-after-resume-1"), service_home.log()
    # The resumed session records on: the ended recorder neither republishes
    # its stale gap (which would hold every drain off it) nor finalizes it.
    for i in range(2, 6):
        _write(CLAUDE, transcript, sid, f"on-after-resume-{i}")
        time.sleep(1.5)
    assert _sent(stub, sid, "on-after-resume-5", timeout=20), service_home.log()
    assert _covers(stub, sid, transcript)
    assert stub.stream(sid)["finalized"] is False
    assert len(_rows(service_home, sid)) == 1
    assert "SECRET" not in stub.sent_text(sid)
    assert service_home.call(Method.SESSION_FINISH, {"sid": sid, "wait": 15})["finished"] is True
    assert stub.stream(sid)["finalized"] is True
    assert "SECRET" not in stub.sent_text(sid)


def test_a_session_ending_off_that_the_server_refuses_for_good_is_dropped_with_its_gaps_kept(
        service_home, stub, agent, sid):
    """A 403 (a login revoked, a team removed): no later service retries it
    for ever, keeping itself up; its gap file stays, so nothing of the
    stretch is ever sent by anything that captures it later."""
    proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-1")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    stub.refusal_code, stub.refusing = 403, True
    kill_agent(proc)
    assert wait_for(lambda: not _rows(service_home, sid) and sid not in _saved_sids(service_home), 20), \
        service_home.log()
    assert "refused it" in service_home.log()
    assert json.loads(_gap_file(home, sid).read_text())["gaps"]
    assert "SECRET" not in stub.sent_text(sid)


def test_a_session_refused_for_good_while_the_service_stops_is_dropped_all_the_same(service_home, stub, agent, sid):
    """Its agent gone while it is off, its last settle in flight when the
    service is told to stop; the gateway refuses it (403): the stopping
    service does not save it for the next one to retry for ever."""
    proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-1")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    assert wait_for(lambda: any(r["last"] == "off" for r in _rows(service_home, sid)), 10)

    def posts() -> int:
        with stub.lock:
            return sum(1 for method, path in stub.requests
                       if method == "POST" and path.count("/") == 4)  # a batch: /ingest/v1/sessions/<route>

    before = posts()
    stub.delay_s, stub.refusal_code, stub.refusing = 3.0, 403, True
    kill_agent(proc)
    assert wait_for(lambda: posts() > before, 15), service_home.log()  # its last settle's batch is in flight
    service_home.call(Method.STOP)
    assert service_home.wait_exit(first["pid"], 15), service_home.log()
    assert "refused it" in service_home.log()
    assert sid not in _saved_sids(service_home)
    assert json.loads(_gap_file(home, sid).read_text())["gaps"]
    assert "SECRET" not in stub.sent_text(sid)


def test_a_session_finished_while_off_with_the_server_down_stays_saved_when_the_service_stops(
        service_home, stub, agent, sid, monkeypatch):
    """Its SessionEnd (`session.finish`), not its agent's exit: the service
    goes idle with it unfinished, and keeps it in `recorders.json` for the
    next service to finish."""
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "1")
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-1")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    stub.refusing = True
    service_home.call(Method.SESSION_FINISH, {"sid": sid, "wait": 0})
    assert service_home.wait_exit(first["pid"], 40), service_home.log()
    assert _saved_sids(service_home) == [sid]
    assert "SECRET" not in stub.sent_text(sid)


def test_a_held_off_session_resumed_by_a_new_service_names_that_service_in_its_marker(service_home, stub, agent, sid):
    """A stopping service writes the off session's agent into its `.hosted`
    marker; the next service that holds it writes itself back, so the hooks'
    readers that check the marker names a service read it as recorded."""
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "off")
    _write(CLAUDE, transcript, sid, "SECRET-1")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    service_home.call(Method.STOP)
    assert service_home.wait_exit(first["pid"], 10)
    assert _hosted_marker(home, CLAUDE, sid) == str(owner["pid"])
    second = service_home.start()
    assert wait_for(lambda: _hosted_marker(home, CLAUDE, sid) == str(second["pid"]), 10), service_home.log()
    assert stub.asked_about(sid) == []


def test_switching_off_during_a_settle_with_nothing_telling_the_service_sends_nothing_written_after(
        service_home, stub, agent, sid):
    """As the race above, but the second move is not told to the service (a
    machine default, Windows, a hook that did not run): its monitor sees it
    while the settle still runs, and opens the gap then."""
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-1")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    assert wait_for(lambda: any(r["last"] == "off" for r in _rows(service_home, sid)), 10)
    stub.delay_s = 4.0
    _switch(home, sid, "full")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    time.sleep(1.0)  # its settle's batch is in flight now
    _switch(home, sid, "off")  # nothing tells the service
    time.sleep(1.0)  # its monitor looks every 0.2 s
    _write(CLAUDE, transcript, sid, "SECRET-2-written-while-off-again")
    time.sleep(6)
    stub.delay_s = 0.0
    time.sleep(3)
    assert "SECRET" not in stub.sent_text(sid)
    _switch(home, sid, "full")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "on-2")
    assert _sent(stub, sid, "on-2"), service_home.log()
    assert _covers(stub, sid, transcript)
    assert "SECRET" not in stub.sent_text(sid)


# -- tap 0.10.19: every `tap watch` reads the switch and the gap file itself ----------------


def _watch(home: Path, stub: IngestStub, sid: str, transcript: Path, **env) -> subprocess.Popen:
    """`tap watch` of `sid` in its own process (the in-tree tap): what a
    sandboxed session, `PROBE_TAP_HOSTED=0`, a session no service could take,
    or a CLI on Python 3.10 records with."""
    return subprocess.Popen(
        [sys.executable, "-m", "tap", "watch", "--session-id", sid, "--cwd", str(home), "--transcript",
         str(transcript), "--plugin-root", str(TAP_ROOT)],
        env=_tap_env(home, stub, **{"PROBE_TAP_HOSTED": "0", **env}),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def _kill(watcher: subprocess.Popen) -> None:
    if watcher.poll() is None:
        watcher.kill()
        watcher.wait(timeout=10)


def _end(home: Path, sid: str) -> None:
    """The session's SessionEnd: its shutdown sentinel (the watch's last pass, then FINALIZE)."""
    (_watchers(home) / f"probe-research-tap-watcher-{sid}.shutdown").touch()


def _gaps(home: Path, sid: str) -> list | None:
    try:
        return json.loads(_gap_file(home, sid).read_text())["gaps"]
    except (OSError, ValueError, KeyError):
        return None


def _no_open_gap(home: Path, sid: str) -> bool:
    """Its stretch is closed: or already gone from its gap file (the watch
    drops a stretch once the server's cursor is past it)."""
    gaps = _gaps(home, sid)
    return gaps is None or gaps[-1][1] is not None


def _watch_log(home: Path, sid: str) -> str:
    return "\n".join(p.read_text(errors="replace")[-3000:] for p in home.rglob(f"logs/{sid}.log"))


@pytest.mark.parametrize("hosted", ["0", "1"], ids=["sandboxed-or-unhosted", "before-it-hands-over"])
def test_another_sessions_tap_watch_sends_none_of_an_off_sessions_stretch(service_home, stub, agent, sid, hosted):
    """Closed by tap 0.10.19 (#3370's review, finding 1): a `tap watch` of
    session A drains every session of the shared journal, B's included; it
    reads B's switch and gap file first, so none of what B wrote while off is
    sent, while A's own lines go."""
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "b-on")
    service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "b-on")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    a_sid = _new_sid()
    a_path = CLAUDE.start(home, a_sid)
    _switch(home, a_sid, "full")
    _write(CLAUDE, a_path, a_sid, "a-on")
    watcher = _watch(home, stub, a_sid, a_path, PROBE_TAP_HOSTED=hosted, PROBE_TAP_HANDBACK_S="600")
    try:
        assert _sent(stub, a_sid, "a-on"), _watch_log(home, a_sid)
        for i in range(3):
            _write(CLAUDE, transcript, sid, f"SECRET-{i + 2}")
            time.sleep(1)
        assert "SECRET" not in stub.sent_text(sid)
    finally:
        _kill(watcher)


def test_a_sessions_own_watch_sends_nothing_while_off_records_the_stretch_and_resumes_from_the_flip(
        service_home, stub, sid):
    """No Probe service at all (sandboxed, `PROBE_TAP_HOSTED=0`): the session's
    own `tap watch` sends nothing it wrote while off, records the stretch in
    its gap file, and captures from the flip back on, never the stretch."""
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-before-1")
    watcher = _watch(home, stub, sid, transcript)
    try:
        assert _sent(stub, sid, "on-before-1"), _watch_log(home, sid)
        _switch(home, sid, "off")
        _write(CLAUDE, transcript, sid, "SECRET-while-off-1", "SECRET-while-off-2")
        time.sleep(4)  # four of its 1 s passes
        assert "SECRET" not in stub.sent_text(sid)
        assert (_gaps(home, sid) or [[0, 0]])[-1][1] is None, _watch_log(home, sid)  # its stretch, recorded

        _switch(home, sid, "full")
        assert wait_for(lambda: _no_open_gap(home, sid), 10), _watch_log(home, sid)
        _write(CLAUDE, transcript, sid, "on-after-1")
        assert _sent(stub, sid, "on-after-1"), _watch_log(home, sid)
        assert _covers(stub, sid, transcript)
        _end(home, sid)
        assert watcher.wait(timeout=30) == 0
        assert (stub.stream(sid) or {}).get("finalized") is True
        assert "SECRET" not in stub.sent_text(sid)
    finally:
        _kill(watcher)


def test_a_watch_of_a_session_off_from_its_start_asks_nothing_until_switched_on(service_home, stub, sid):
    """Off from its first line: nothing of it reaches the server, not even a
    question about it (no claim, no receipts); its stretch is recorded from
    the first byte; once on, captured from the flip."""
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "off")
    _write(CLAUDE, transcript, sid, "SECRET-from-the-start-1")
    watcher = _watch(home, stub, sid, transcript)
    try:
        time.sleep(2)
        _write(CLAUDE, transcript, sid, "SECRET-from-the-start-2")
        time.sleep(3)
        assert stub.asked_about(sid) == []
        assert _gaps(home, sid) == [[0, None]], _watch_log(home, sid)
        _switch(home, sid, "full")
        assert wait_for(lambda: _no_open_gap(home, sid), 10), _watch_log(home, sid)
        _write(CLAUDE, transcript, sid, "on-after-1")
        assert _sent(stub, sid, "on-after-1"), _watch_log(home, sid)
        assert _covers(stub, sid, transcript)
        assert "SECRET" not in stub.sent_text(sid)
    finally:
        _kill(watcher)


def test_a_watch_of_a_session_that_ends_while_off_finalizes_it_without_the_stretch(service_home, stub, sid):
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    watcher = _watch(home, stub, sid, transcript)
    try:
        assert _sent(stub, sid, "on-1"), _watch_log(home, sid)
        _switch(home, sid, "off")
        _write(CLAUDE, transcript, sid, "SECRET-1", "SECRET-2")
        time.sleep(2)
        _end(home, sid)
        assert watcher.wait(timeout=30) == 0, _watch_log(home, sid)
        stream = stub.stream(sid) or {}
        assert stream.get("finalized") is True, _watch_log(home, sid)
        assert stream.get("source_byte_end") == transcript.stat().st_size
        assert "SECRET" not in stub.sent_text(sid)
    finally:
        _kill(watcher)


def test_a_watch_of_a_session_off_from_its_start_that_ends_sends_nothing(service_home, stub, sid):
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "off")
    _write(CLAUDE, transcript, sid, "SECRET-1")
    watcher = _watch(home, stub, sid, transcript)
    try:
        time.sleep(2)
        _end(home, sid)
        assert watcher.wait(timeout=30) == 0
        assert stub.asked_about(sid) == []
        assert _gaps(home, sid) == [[0, None]]  # kept: a later capture of it skips the stretch too
    finally:
        _kill(watcher)


def test_a_stretch_a_watch_recorded_is_never_sent_by_the_service_that_records_the_session_next(
        service_home, stub, agent, sid):
    """Whichever process records after the flip back on: the watch recorded
    the off stretch (and is gone without a last pass); the service that
    records the session next takes the stretch from its gap file."""
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    watcher = _watch(home, stub, sid, transcript)
    try:
        assert _sent(stub, sid, "on-1"), _watch_log(home, sid)
        _switch(home, sid, "off")
        _write(CLAUDE, transcript, sid, "SECRET-1")
        time.sleep(3)
    finally:
        _kill(watcher)
    assert "SECRET" not in stub.sent_text(sid)
    assert (_gaps(home, sid) or [[0, 0]])[-1][1] is None, _watch_log(home, sid)  # gone with its stretch recorded
    _write(CLAUDE, transcript, sid, "SECRET-2")
    _switch(home, sid, "full")  # nothing records it at this moment
    service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    _write(CLAUDE, transcript, sid, "on-after-1")
    assert _sent(stub, sid, "on-after-1"), service_home.log()
    assert _covers(stub, sid, transcript)
    assert "SECRET" not in stub.sent_text(sid)


def test_a_stretch_the_service_recorded_is_never_sent_by_a_watch_that_records_the_session_next(
        service_home, stub, agent, sid):
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-1")
    first = service_home.start()
    service_home.call(Method.SESSION_RECORD, CLAUDE.params(home, sid, owner, stub))
    assert _sent(stub, sid, "on-1")
    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-1")
    assert wait_for(lambda: (_gaps(home, sid) or [[0, 0]])[-1][1] is None, 10), service_home.log()
    service_home.call(Method.STOP)
    assert service_home.wait_exit(first["pid"], 10)
    _write(CLAUDE, transcript, sid, "SECRET-2")
    _switch(home, sid, "full")  # nothing records it at this moment: what it writes until one looks is skipped
    watcher = _watch(home, stub, sid, transcript)
    try:
        assert wait_for(lambda: _no_open_gap(home, sid), 10), _watch_log(home, sid)
        _write(CLAUDE, transcript, sid, "on-after-1")
        assert _sent(stub, sid, "on-after-1"), (_watch_log(home, sid), service_home.log())
        assert _covers(stub, sid, transcript)
        assert "SECRET" not in stub.sent_text(sid)
    finally:
        _kill(watcher)


def test_a_watch_of_a_session_off_before_it_claimed_it_hands_it_to_the_service(service_home, stub, agent, sid):
    """Off from its start, its own `tap watch` (the service was restarting at
    SessionStart) has no claim to hand over and staged nothing: the service
    takes the session held off, and the watch leaves (exit 12), having asked
    the server nothing about it."""
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "off")
    _write(CLAUDE, transcript, sid, "SECRET-1")
    service_home.start()
    _owner_file(home, sid, owner)
    watcher = _watch(home, stub, sid, transcript, PROBE_TAP_HOSTED="1", PROBE_TAP_HANDBACK_S="2")
    try:
        assert watcher.wait(timeout=60) == 12, (_watch_log(home, sid), service_home.log())
        assert any(r["sid"] == sid and r["off"] for r in service_home.call(Method.STATUS)["recorders"])
        assert _hosted_marker(home, CLAUDE, sid) == str(service_home.call(Method.STATUS)["pid"])
        _write(CLAUDE, transcript, sid, "SECRET-2")
        time.sleep(2)
        assert stub.asked_about(sid) == []
    finally:
        _kill(watcher)


def test_a_watch_whose_lock_file_cannot_be_opened_still_records_the_stretch_and_never_sends_it(
        service_home, stub, sid):
    """Review of #3387, reproduced with a real `tap watch`: the session's lock
    file could not be opened (here a folder stands there), so its stretch was
    never written, and the flip back on sent it. Locking that is unavailable
    writes without it."""
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-before-1")
    watcher = _watch(home, stub, sid, transcript)
    try:
        assert _sent(stub, sid, "on-before-1"), _watch_log(home, sid)
        (_state_dir(home) / "sessions" / f"{sid}.gaps.lock").mkdir()
        _switch(home, sid, "off")
        _write(CLAUDE, transcript, sid, "SECRET-while-off-1")
        time.sleep(4)
        assert "SECRET" not in stub.sent_text(sid)
        assert (_gaps(home, sid) or [[0, 0]])[-1][1] is None, _watch_log(home, sid)
        _switch(home, sid, "full")
        assert wait_for(lambda: _no_open_gap(home, sid), 10), _watch_log(home, sid)
        _write(CLAUDE, transcript, sid, "on-after-1")
        assert _sent(stub, sid, "on-after-1"), _watch_log(home, sid)
        assert _covers(stub, sid, transcript)
        assert "SECRET" not in stub.sent_text(sid)
    finally:
        _kill(watcher)


def test_a_watch_that_cannot_write_its_gap_file_at_all_skips_the_stretch_itself(service_home, stub, sid):
    """No gap-file write lands for the whole stretch (the sessions folder is
    read-only here): the watch keeps the stretch in memory, sends none of it
    after the flip back on, and captures from the flip."""
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    sessions = _state_dir(home) / "sessions"
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-before-1")
    watcher = _watch(home, stub, sid, transcript)
    try:
        assert _sent(stub, sid, "on-before-1"), _watch_log(home, sid)
        _switch(home, sid, "off")
        sessions.chmod(0o500)  # its `.state` still reads; nothing can be written beside it
        _write(CLAUDE, transcript, sid, "SECRET-while-off-1")
        time.sleep(4)
        assert "SECRET" not in stub.sent_text(sid)
        assert _gaps(home, sid) is None
        sessions.chmod(0o700)
        _switch(home, sid, "full")
        sessions.chmod(0o500)
        time.sleep(3)  # the watch sees it on (each second)
        _write(CLAUDE, transcript, sid, "on-after-1")
        assert _sent(stub, sid, "on-after-1"), _watch_log(home, sid)
        assert _covers(stub, sid, transcript)
        assert "SECRET" not in stub.sent_text(sid)
        assert "could not be written" in _watch_log(home, sid)
    finally:
        sessions.chmod(0o700)
        _kill(watcher)


def test_a_watch_between_long_passes_records_the_stretch_within_a_second_or_two(service_home, stub, sid):
    """Its passes are 30 s apart (an idle session): the switch is looked at
    each second between them, so the stretch starts where it was last seen on,
    not up to a pass later."""
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-before-1")
    watcher = _watch(home, stub, sid, transcript, PROBE_RESEARCH_TAP_ACTIVE_INTERVAL_SECONDS="30",
                     PROBE_RESEARCH_TAP_IDLE_INTERVAL_SECONDS="30")
    try:
        assert _sent(stub, sid, "on-before-1"), _watch_log(home, sid)
        time.sleep(2)  # into the sleep between its passes
        start = transcript.stat().st_size
        _switch(home, sid, "off")
        assert wait_for(lambda: _gaps(home, sid) is not None, 2.5), _watch_log(home, sid)
        assert _gaps(home, sid) == [[start, None]]
    finally:
        _kill(watcher)


# -- a tap from before its own gate, loaded by this service: the wraps ------------------------


def _released_tap(version: str, into: Path) -> Path | None:
    """The tap as released at `version` (the commit that set it), from this
    checkout's history; None in a shallow one."""
    init = "agent/plugins/probe-research-tap/tap/__init__.py"
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=TAP_ROOT, capture_output=True, text=True,
                             timeout=30, check=True).stdout.strip()
        # The commits that changed how often the line appears: the first set it.
        commits = subprocess.run(["git", "log", "--reverse", "--format=%H", f"-S__version__ = \"{version}\"",
                                  "--", init], cwd=top, capture_output=True, text=True, timeout=60,
                                 check=True).stdout.split()
        if not commits:
            return None
        commit = commits[0]
        archive = subprocess.run(["git", "archive", commit, "agent/plugins/probe-research-tap"], cwd=top,
                                 capture_output=True, timeout=60, check=True).stdout
        subprocess.run(["tar", "-x", "-C", str(into)], input=archive, check=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    root = into / "agent" / "plugins" / "probe-research-tap"
    return root if f'__version__ = "{version}"' in (root / "tap" / "__init__.py").read_text() else None


@pytest.fixture
def old_tap_sid(tmp_path):
    """A session of a tap before 0.10.19, which keeps its watcher files in
    `/tmp` on POSIX whatever the environment says: they go once the test's
    service has stopped (set up before `service_home`, so torn down after)."""
    value = _new_sid()
    yield value
    for path in Path("/tmp").glob(f"*-watcher-{value}.*"):
        path.unlink(missing_ok=True)


def test_a_tap_from_before_its_own_gate_is_still_gated_by_this_services_wraps(old_tap_sid, service_home, stub, agent,
                                                                              tmp_path):
    """Taps 0.10.0-0.10.18 read no switch: the service loading one wraps its
    drains, as #3370 shipped, and nothing written while off is sent."""
    root = _released_tap("0.10.18", tmp_path)
    if root is None:
        pytest.skip("no tap history here (a shallow checkout)")
    assert not (root / "tap" / "capture_gate.py").exists()
    sid = old_tap_sid
    _proc, owner = agent
    home = service_home.home
    transcript = CLAUDE.start(home, sid)
    _switch(home, sid, "full")
    _write(CLAUDE, transcript, sid, "on-before-1")
    service_home.start()
    params = CLAUDE.params(home, sid, owner, stub)
    params.update(tap_root=str(root), tap_version="0.10.18")
    service_home.call(Method.SESSION_RECORD, params)
    assert _sent(stub, sid, "on-before-1"), service_home.log()
    assert "recorder: tap 0.10.18 loaded" in service_home.log()

    _switch(home, sid, "off")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "SECRET-while-off-1")
    time.sleep(3)
    assert "SECRET" not in stub.sent_text(sid)
    _switch(home, sid, "full")
    service_home.call(Method.SESSION_RECORDING, {"sid": sid})
    _write(CLAUDE, transcript, sid, "on-after-1")
    assert _sent(stub, sid, "on-after-1"), service_home.log()
    assert _covers(stub, sid, transcript)
    assert "SECRET" not in stub.sent_text(sid)
