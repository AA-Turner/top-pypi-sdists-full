"""Daemon v2 worker, the long-running half: the lease, one worker per session,
crash loops, the session-end deadline, what a bite shows, the folder check, the
inbox, and the device counter doctor reads.

Same seams as test_daemon_worker.py: the model is Pydantic AI's FunctionModel,
`probe` commands never reach a server, and the chat log is a real file.
"""

from __future__ import annotations

import asyncio
import dataclasses
import fcntl
import json
import os
import signal
import threading
import time
import types
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")

from pydantic_ai.exceptions import ModelHTTPError  # noqa: E402
from pydantic_ai.messages import ModelResponse, ToolCallPart  # noqa: E402
from pydantic_ai.models.function import AgentInfo, FunctionModel  # noqa: E402

from probe.daemon import approvals as appr  # noqa: E402
from probe.daemon import bite as bite_mod  # noqa: E402
from probe.daemon import folders, lease, tools  # noqa: E402
from probe.daemon import store as store_mod  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from probe.daemon.events import Event, Kind  # noqa: E402
from probe.sdk.session_marker import WIZARD_HINT  # noqa: E402

SID = "11111111-2222-3333-4444-555555555555"
RUN = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """No real config (so no real key), no MCP: nothing leaves the box."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    _set_state("daemon")


class Replay:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    async def run(self, argv, op_id):
        self.calls.append(list(argv))
        return 0, json.dumps({"ok": True})

    def deletion_facts(self, kind, target):
        return {"id": target, "name": target, "what": kind, "others": {}, "count": 0, "updated_at": "t"}


def _set_state(state: str) -> None:
    (lease.sessions_dir() / f"{SID}.state").write_text(state)


def _line(obj: dict) -> str:
    return json.dumps(obj) + "\n"


def _transcript(tmp_path: Path) -> tuple[Path, Path]:
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True, exist_ok=True)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line({"type": "permission-mode", "permissionMode": "default"})
        + _line({"type": "user", "message": {"content": "sweep C for an SVM on digits"}, "cwd": str(work)})
        + _line({"type": "assistant", "message": {"content": [{"type": "text", "text": "SVM C=10: 0.9889."}]}})
        + _line({"type": "system", "subtype": "turn_duration", "durationMs": 5})
    )
    return transcript, work


def _scripted(commands: list[str], note: str = "note"):
    calls = {"n": 0}

    def fn(messages, info: AgentInfo) -> ModelResponse:
        i = calls["n"]
        calls["n"] += 1
        if i < len(commands):
            return ModelResponse(parts=[ToolCallPart("shell", {"command": commands[i], "why": "test"})])
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"summary": note})])

    return FunctionModel(fn), calls


def _raising(exc: Exception):
    calls = {"n": 0}

    def fn(messages, info):
        calls["n"] += 1
        raise exc

    return FunctionModel(fn), calls


def _worker(tmp_path: Path, *, model=None, replay=None, clock=time.time, source="claude_code"):
    transcript, work = _transcript(tmp_path)
    return worker_mod.Worker(worker_mod.Session(SID, transcript, work, source, home=tmp_path / "home"),
                             clock=clock, replay=replay, model=model)


def _lease() -> dict:
    return json.loads(lease.lease_path(SID).read_text())


def _errors(tmp_path: Path) -> str:
    path = tmp_path / "state" / "probe" / "daemon-errors.log"
    return path.read_text() if path.exists() else ""


# ---------------------------------------------------------------------------
# A1: the lease is renewed only while recording works.
# ---------------------------------------------------------------------------


def test_the_poll_never_renews_a_lease_released_for_a_refused_key(tmp_path):
    model, _ = _raising(ModelHTTPError(401, "default"))
    w = _worker(tmp_path, model=model)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert _lease()["reason"] == lease.REASON_UNAUTHORIZED
    for _ in range(3):
        assert asyncio.run(w.tick()) is None
    assert _lease()["reason"] == lease.REASON_UNAUTHORIZED, "the poll undid the release"


def test_no_renewal_when_the_switch_is_not_daemon_or_another_daemon_holds_the_lease(tmp_path):
    w = _worker(tmp_path)
    assert w._renew() and _lease()["pid"] == os.getpid()
    _set_state("full")
    lease.release(SID, lease.REASON_STOPPED)
    assert w._renew() is False and _lease()["reason"] == lease.REASON_STOPPED
    _set_state("daemon")
    other = {"v": 1, "writer": "daemon", "pid": os.getpid() + 1, "expires_at": time.time() + 200,
             "renewed_at": time.time(), "reason": None}
    lease.lease_path(SID).write_text(json.dumps(other))
    assert w._renew() is False and _lease()["pid"] == os.getpid() + 1


def test_a_tool_call_never_takes_the_lease_from_another_daemon(tmp_path, monkeypatch):
    ran = []

    async def run_probe(deps, argv, op_id):
        ran.append(argv)
        return tools.ProbeResult(0, "{}")

    monkeypatch.setattr(tools, "run_probe_process", run_probe)
    model, _ = _scripted([f"probe run tag {RUN} svm"])
    w = _worker(tmp_path, model=model)
    w.read_new()
    other = {"v": 1, "writer": "daemon", "pid": os.getpid() + 1, "expires_at": time.time() + 200,
             "renewed_at": time.time(), "reason": None}
    lease.lease_path(SID).write_text(json.dumps(other))
    assert asyncio.run(w.run_bite("turn end")) is False
    assert ran == [], "the write ran on a lease this process does not hold"
    assert _lease()["pid"] == os.getpid() + 1
    # Its writes were refused, so its range stays queued for when the lease is ours.
    assert w.store.pending() and w.store.recent_bites(1)[0]["outcome"] == "lease lost"
    assert w.next_attempt_at > w.clock(), "retried at once: a model call every poll"


def test_a_released_lease_comes_back_when_the_model_answers_again(tmp_path, monkeypatch):
    ran = []

    async def run_probe(deps, argv, op_id):
        ran.append(argv)
        return tools.ProbeResult(0, "{}")

    monkeypatch.setattr(tools, "run_probe_process", run_probe)
    model, _ = _scripted([f"probe run tag {RUN} svm"])
    w = _worker(tmp_path, model=model)
    w.read_new()
    w._release(lease.REASON_UNAUTHORIZED)
    assert asyncio.run(w.run_bite("turn end")) is True
    assert ran == [["run", "tag", RUN, "svm"]]
    assert w.released_reason is None and _lease()["reason"] is None and _lease()["pid"] == os.getpid()
    assert w.store.pending() == []


@pytest.mark.parametrize("refused_by", ["the model (401)", "Probe, still refusing", "Probe, accepting again"])
def test_a_key_probe_refused_comes_back_only_once_a_probe_auth_check_passes(tmp_path, monkeypatch, refused_by):
    """R3-5: the model's route can take a key Probe's other routes refuse. After
    PROBE refused it, a model answering never takes the lease back: only a Probe
    auth check that passes (`probe_api.whoami`), and no model call before it. A
    key the MODEL refused comes back as before, when a model round answers."""
    import httpx

    from probe.daemon import probe_api

    async def refused(deps, argv, op_id):
        # What `tools.run_probe_process` does when the CLI reports a 401.
        deps.key_refused = True
        deps.stopped = "Probe refused the daemon's key"
        return tools.ProbeResult(1, "", "error: 401 Unauthorized")

    monkeypatch.setattr(tools, "run_probe_process", refused)
    asked = []

    async def whoami(env):
        asked.append(env)
        if refused_by == "Probe, still refusing":
            req = httpx.Request("GET", "https://probe.test/v1/me")
            raise httpx.HTTPStatusError("401 Unauthorized", request=req, response=httpx.Response(401, request=req))
        return {"user_id": "u1"}

    monkeypatch.setattr(probe_api, "whoami", whoami)
    if refused_by == "the model (401)":
        model, _ = _raising(ModelHTTPError(401, "default"))
    else:
        model, _ = _scripted([f"probe run tag {RUN} svm"])
    w = _worker(tmp_path, model=model)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert _lease()["reason"] == lease.REASON_UNAUTHORIZED and w.released_reason == lease.REASON_UNAUTHORIZED
    # The retry, 30 minutes on: the model's route takes the key and it answers.
    w._model, calls = _scripted([])
    w.next_attempt_at = 0.0
    done = asyncio.run(w.run_bite("turn end"))
    if refused_by == "Probe, still refusing":
        assert _lease()["reason"] == lease.REASON_UNAUTHORIZED and w.released_reason == lease.REASON_UNAUTHORIZED, \
            "a model answer took back a lease Probe still refuses the key for"
        assert done is False and calls["n"] == 0, "a model call while Probe refuses the key"
        assert w.next_attempt_at == pytest.approx(w.clock() + worker_mod.UNAUTHORIZED_RETRY_S, abs=5)
        assert len(asked) == 1
        return
    assert done is True and calls["n"] == 1
    assert w.released_reason is None and _lease()["reason"] is None and _lease()["pid"] == os.getpid()
    assert len(asked) == (0 if refused_by == "the model (401)" else 1)


def test_a_bites_tools_get_an_op_seed_the_retry_of_the_same_events_repeats(tmp_path, monkeypatch):
    """R3-7, the worker's half: a bite's Deps carry `op_seed` =
    `<session>:<its first event>`, so the same command in a retried bite over the
    same events sends the same Idempotency-Key. Set only when `tools.Deps` has the
    field: a Deps without it still builds."""
    w0 = _worker(tmp_path)
    plain = w0.deps(None, op_seed=f"{SID}:1")
    assert getattr(plain, "op_seed", f"{SID}:1") == f"{SID}:1"

    @dataclasses.dataclass
    class SeededDeps(tools.Deps):
        op_seed: str | None = None

    monkeypatch.setattr(tools, "Deps", SeededDeps)
    seeds = []

    async def run_probe(deps, argv, op_id):
        seeds.append(deps.op_seed)
        return tools.ProbeResult(0, "{}")

    monkeypatch.setattr(tools, "run_probe_process", run_probe)
    rounds = {"n": 0}

    def fn(messages, info: AgentInfo) -> ModelResponse:
        rounds["n"] += 1
        if rounds["n"] in (1, 3):  # each bite's first round: the same command
            return ModelResponse(parts=[ToolCallPart("shell", {"command": f"probe run tag {RUN} svm", "why": "t"})])
        if rounds["n"] == 2:
            raise RuntimeError("the provider dropped the first bite")
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"summary": "note"})])

    w = _worker(tmp_path, model=FunctionModel(fn))
    w.read_new()
    first = w.store.pending()[0].seq
    assert asyncio.run(w.run_bite("turn end")) is False
    assert asyncio.run(w.run_bite("turn end")) is True
    assert seeds == [f"{SID}:{first}", f"{SID}:{first}"]
    assert w.deps(None).op_seed is None, "a held action's Deps (no bite) carry no seed"


@pytest.mark.parametrize("error", ["connection", "timeout", "503", "not an outage"])
def test_model_outages_release_the_lease_after_two_in_a_row(tmp_path, error):
    from pydantic_ai.exceptions import ModelAPIError

    exc = {"connection": ModelAPIError("default", "Connection error."),
           "timeout": ModelAPIError("default", "Request timed out."),
           "503": ModelHTTPError(503, "default"),
           "not an outage": RuntimeError("the model returned something odd")}[error]
    model, calls = _raising(exc)
    w = _worker(tmp_path, model=model)
    w.read_new()
    assert w._renew()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert _lease()["reason"] is None, "one failure is not an outage"
    assert asyncio.run(w.run_bite("turn end")) is False and calls["n"] == 2
    if error == "not an outage":
        assert _lease()["reason"] is None and w.released_reason is None
        return
    assert _lease()["reason"] == lease.REASON_GATEWAY and w.released_reason == lease.REASON_GATEWAY
    assert "failed 2 times in a row" in _errors(tmp_path)
    assert w.store.pending(), "nothing is dropped"
    # The model answers again: the lease comes back.
    w._model, _ = _scripted([])
    assert asyncio.run(w.run_bite("turn end")) is True
    assert w.released_reason is None and _lease()["reason"] is None and w.gateway_failures == 0


@pytest.mark.parametrize("then", ["the model answers", "the model fails"])
def test_probe_refusing_the_daemons_key_releases_the_lease_and_waits(tmp_path, monkeypatch, then):
    ran = []

    async def run_probe(deps, argv, op_id):
        # What `tools.run_probe_process` does when the CLI reports a 401 / 403.
        ran.append(list(argv))
        deps.key_refused = True
        deps.stopped = "Probe refused the daemon's key"
        return tools.ProbeResult(1, "", "error: 401 Unauthorized")

    monkeypatch.setattr(tools, "run_probe_process", run_probe)
    rounds = {"n": 0}

    def fn(messages, info: AgentInfo) -> ModelResponse:
        rounds["n"] += 1
        if rounds["n"] == 1:
            return ModelResponse(parts=[ToolCallPart("shell", {"command": f"probe run tag {RUN} svm", "why": "t"})])
        if then == "the model fails":
            raise RuntimeError("provider down")
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"summary": "note"})])

    w = _worker(tmp_path, model=FunctionModel(fn))
    w.read_new()
    queued = [ev.seq for ev in w.store.pending()]
    assert asyncio.run(w.run_bite("turn end")) is False
    assert ran == [["run", "tag", RUN, "svm"]]
    assert _lease()["reason"] == lease.REASON_UNAUTHORIZED and w.released_reason == lease.REASON_UNAUTHORIZED
    assert w.next_attempt_at == pytest.approx(w.clock() + worker_mod.UNAUTHORIZED_RETRY_S, abs=5)
    assert w.failures == 0, "a refused key is not a failure that moves events to the back"
    assert [ev.seq for ev in w.store.pending()] == queued, "the range stays queued"
    assert WIZARD_HINT in _errors(tmp_path)


def test_no_model_call_while_the_switch_cannot_be_read_and_the_worker_leaves_after_a_minute(tmp_path):
    now = [1000.0]
    model, calls = _scripted([])
    w = _worker(tmp_path, model=model, clock=lambda: now[0])
    assert w._renew()
    (lease.sessions_dir() / f"{SID}.state").unlink()
    assert asyncio.run(w.tick()) is None
    assert calls["n"] == 0, "a model call while the switch cannot be read"
    assert w.due() == "turn end", "the bite is still due: it just does not start"
    now[0] += worker_mod.SWITCH_UNREADABLE_EXIT_S / 2
    assert asyncio.run(w.tick()) is None and calls["n"] == 0
    # Readable again for a moment: the minute starts over.
    _set_state("daemon")
    assert asyncio.run(w.tick()) is None and calls["n"] == 1
    (lease.sessions_dir() / f"{SID}.state").unlink()
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": "more"}}))
        handle.write(_line({"type": "system", "subtype": "turn_duration", "durationMs": 5}))
    assert asyncio.run(w.tick()) is None
    now[0] += worker_mod.SWITCH_UNREADABLE_EXIT_S - 1
    assert asyncio.run(w.tick()) is None and calls["n"] == 1
    now[0] += 2
    assert asyncio.run(w.tick()) == worker_mod.EXIT_RESPAWN_LATER, "not a give-up: the switch decides (T11)"
    assert calls["n"] == 1 and _lease()["reason"] == lease.REASON_ERROR
    assert "could not be read" in _errors(tmp_path)


def test_no_model_call_while_another_process_holds_a_live_lease(tmp_path):
    model, calls = _scripted([])
    w = _worker(tmp_path, model=model)
    other = {"v": 1, "writer": "daemon", "pid": os.getpid() + 1, "expires_at": time.time() + 200,
             "renewed_at": time.time(), "reason": None}
    lease.lease_path(SID).write_text(json.dumps(other))
    assert asyncio.run(w.tick()) is None
    assert calls["n"] == 0, "a model call on a lease another process holds (a killed predecessor's)"
    assert _lease()["pid"] == os.getpid() + 1
    # Once it lapses, this worker takes the lease and records.
    other["expires_at"] = time.time() - 1
    lease.lease_path(SID).write_text(json.dumps(other))
    assert asyncio.run(w.tick()) is None and calls["n"] == 1
    assert _lease()["pid"] == os.getpid() and w.store.recent_bites(1)[0]["outcome"] == "done"


def test_a_release_this_worker_made_still_lets_the_model_answer(tmp_path):
    model, calls = _scripted([])
    w = _worker(tmp_path, model=model)
    assert w._renew()
    w._release(lease.REASON_GATEWAY)
    assert asyncio.run(w.tick()) is None and calls["n"] == 1, "the model round is how the lease comes back"
    assert w.released_reason is None and _lease()["reason"] is None


# ---------------------------------------------------------------------------
# A3: one worker per session.
# ---------------------------------------------------------------------------


def _hold_lock() -> object:
    path = worker_mod.lock_path(SID)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a")
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    return handle


def _run_main(argv: list[str]) -> int:
    handlers = {s: signal.getsignal(s) for s in (signal.SIGTERM, signal.SIGINT)}
    try:
        return worker_mod.main(argv)
    finally:
        for s, h in handlers.items():
            signal.signal(s, h)


def _argv(tmp_path: Path) -> list[str]:
    transcript, work = _transcript(tmp_path)
    return ["--session-id", SID, "--transcript", str(transcript), "--cwd", str(work)]


def test_a_second_worker_waits_for_the_first_and_leaves_if_the_switch_moves(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_DAEMON_KEY", "k-test")
    held = _hold_lock()
    try:
        _set_state("full")
        assert _run_main(_argv(tmp_path)) == worker_mod.EXIT_RESPAWN_LATER
        assert not store_mod.store_path(SID).exists(), "it opened the store while another worker held it"
    finally:
        held.close()


def test_the_session_lock_is_taken_once_the_first_worker_lets_go(tmp_path):
    held = _hold_lock()
    threading.Timer(0.3, held.close).start()
    started = time.monotonic()
    got = worker_mod.session_lock(SID, poll_s=0.05)
    try:
        assert not isinstance(got, int) and time.monotonic() - started >= 0.25
    finally:
        got.close()
    again = _hold_lock()
    try:
        assert worker_mod.session_lock(SID, should_stop=lambda: True, poll_s=0.01) == 0
    finally:
        again.close()


def test_an_orphaned_worker_finishes_and_takes_no_new_input(tmp_path, monkeypatch):
    model, calls = _scripted([])
    w = _worker(tmp_path, model=model, replay=Replay())
    monkeypatch.setattr(worker_mod.os, "getppid", lambda: w.parent_pid + 1)
    assert asyncio.run(w.tick()) is None  # the last look reads what is on disk, then one bite
    assert w.stopping and w.finish_by is not None and calls["n"] == 1
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": "written after capture went away"}}))
    assert asyncio.run(w.tick()) == 0
    assert w.store.search("capture went away") == []
    assert _lease()["reason"] == lease.REASON_STOPPED


# ---------------------------------------------------------------------------
# A4: nothing crash-loops.
# ---------------------------------------------------------------------------


def test_an_answer_that_cannot_be_acted_on_waits_instead_of_crashing(tmp_path, monkeypatch):
    now = [1000.0]
    w = _worker(tmp_path, replay=Replay(), clock=lambda: now[0])
    facts = {"id": "r9", "name": "r9", "what": "run", "others": {"alice|runs": 2}, "count": 2, "updated_at": "t"}
    req = w.board.hold(policy="delete.others_data", session_id=SID, facts=facts, bypass=False,
                       held={"kind": "probe", "argv": ["run", "delete", "r9"], "op_id": "op1", "cwd": "."})
    w.board.answer(req.id, req.question.yes_label, channel="test")
    tries = []

    async def unreachable(deps, parsed):
        tries.append(1)
        raise OSError("Probe is unreachable")

    monkeypatch.setattr(tools, "deletion_facts", unreachable)
    asyncio.run(w.settle_answers())
    assert w.board.get(req.id).state == appr.WAITING
    notices = [e for e in w.store.pending() if e.kind == Kind.META]
    assert len(notices) == 1 and req.id in notices[0].text and "Nothing ran" in notices[0].text
    asyncio.run(w.settle_answers())
    assert len(tries) == 1, "retried inside its back-off"
    now[0] += worker_mod.SETTLE_RETRY_S + 1
    asyncio.run(w.settle_answers())
    assert len(tries) == 2 and len([e for e in w.store.pending() if e.kind == Kind.META]) == 1
    monkeypatch.setattr(tools, "deletion_facts", lambda deps, parsed: _facts(facts))
    now[0] += 10 * worker_mod.SETTLE_RETRY_S
    asyncio.run(w.settle_answers())
    assert w.board.get(req.id).state == appr.APPROVED and w.replay.calls == [["run", "delete", "r9"]]


async def _facts(facts):
    return facts


def _held_override(w, argv: list[str]):
    import shlex

    facts = {"command": "probe " + shlex.join(argv), "blocked_because": "a check", "flagged": None, "masked": None,
             "reason": "a false alarm"}
    held = {"kind": "probe", "argv": argv, "op_id": "op-held", "cwd": str(w.session.cwd), "override": "root_option"}
    req = w.board.hold(policy="check.override", session_id=SID, facts=facts, held=held, bypass=False)
    w.board.answer(req.id, req.question.yes_label, channel="test")
    return req


def test_a_yes_marked_running_is_never_run_twice_even_when_running_it_fails(tmp_path, monkeypatch):
    now = [1000.0]
    w = _worker(tmp_path, clock=lambda: now[0])
    assert w._renew()
    req = _held_override(w, ["run", "tag", RUN, "svm"])
    seen = []

    async def run_probe(deps, argv, op_id):
        # The command went out, then something broke before the worker could log it.
        seen.append(w.board.get(req.id).outcome)
        raise ConnectionResetError("the connection dropped after the write")

    monkeypatch.setattr(tools, "_run_probe", run_probe)
    asyncio.run(w.settle_answers())
    assert seen == ["yes: running"], "not marked before it ran"
    done = w.board.get(req.id)
    assert done.state == appr.APPROVED and done.outcome.startswith("yes: failed while running")
    notices = [e.text for e in w.store.pending() if e.kind == Kind.META]
    assert len(notices) == 1 and req.id in notices[0] and "may have run in part" in notices[0]
    assert "Nothing ran" not in notices[0]
    for _ in range(3):
        now[0] += 10 * worker_mod.BACKOFF_CAP_S
        asyncio.run(w.settle_answers())
    assert seen == ["yes: running"], "run a second time"


def test_a_yes_probe_refuses_the_key_for_releases_the_lease(tmp_path, monkeypatch):
    w = _worker(tmp_path)
    assert w._renew()
    req = _held_override(w, ["run", "tag", RUN, "svm"])

    async def run_probe(deps, argv, op_id):
        deps.key_refused = True
        deps.stopped = "Probe refused the daemon's key"
        return 1, "error: 401 Unauthorized", "error: 401 Unauthorized"

    monkeypatch.setattr(tools, "_run_probe", run_probe)
    asyncio.run(w.settle_answers())
    assert w.board.get(req.id).outcome == "yes: Probe refused the daemon's key"
    assert _lease()["reason"] == lease.REASON_UNAUTHORIZED and w.released_reason == lease.REASON_UNAUTHORIZED
    notices = [e.text for e in w.store.pending() if e.kind == Kind.META]
    assert len(notices) == 1 and "didn't run" in notices[0]


def test_a_yes_cancelled_mid_run_stays_marked_running_and_is_not_run_again(tmp_path, monkeypatch):
    w = _worker(tmp_path)
    assert w._renew()
    req = _held_override(w, ["run", "tag", RUN, "svm"])
    seen = []

    async def run_probe(deps, argv, op_id):
        seen.append(argv)
        raise asyncio.CancelledError()

    monkeypatch.setattr(tools, "_run_probe", run_probe)
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(w.settle_answers())
    assert w.board.get(req.id).outcome == "yes: running"
    fresh = _worker(tmp_path)  # a worker started after the one that was stopped
    assert fresh._renew()
    asyncio.run(fresh.settle_answers())
    assert len(seen) == 1


def test_a_yes_left_running_by_a_worker_that_stopped_is_reported_interrupted_never_run(tmp_path, monkeypatch):
    """R3-8: a crash between marking a yes `yes: running` and running it. The
    session's next worker reports it interrupted (it may not have run) with a
    notice, and never runs it; another session's running yes is not its own."""
    ran = []

    async def run_probe(deps, argv, op_id):
        ran.append(argv)
        return 0, "{}", ""

    monkeypatch.setattr(tools, "_run_probe", run_probe)
    w = _worker(tmp_path)
    req = _held_override(w, ["run", "tag", RUN, "svm"])
    w.board.resolve(req, state=appr.APPROVED, outcome=worker_mod.HELD_RUNNING, channel="test")  # then the crash
    theirs = w.board.hold(policy=req.policy, session_id="another-session", facts=req.facts, held=req.held,
                          bypass=False)
    w.board.resolve(theirs, state=appr.APPROVED, outcome=worker_mod.HELD_RUNNING, channel="test")
    fresh = _worker(tmp_path)  # the stopped worker's successor
    done = fresh.board.get(req.id)
    assert done.state == appr.APPROVED and done.outcome == worker_mod.HELD_INTERRUPTED
    notices = [e.text for e in fresh.store.pending() if e.kind == Kind.META]
    assert len(notices) == 1 and req.id in notices[0] and "may not have run" in notices[0]
    assert fresh.board.get(theirs.id).outcome == worker_mod.HELD_RUNNING, "another session's yes was touched"
    assert fresh._renew()
    asyncio.run(fresh.settle_answers())
    _worker(tmp_path)  # and the next start again
    assert len([e for e in fresh.store.pending() if e.kind == Kind.META]) == 1, "reported twice"
    assert ran == [], "an interrupted yes ran"


@pytest.mark.parametrize("via, left_s", [("settle", 1.5), ("tick", 1.5), ("tick", -1.0)])
def test_a_yes_on_an_aged_lease_runs_on_a_renewed_one_and_completes(tmp_path, via, left_s):
    """R3-9: the lease was last renewed about 238s ago (1.5s left of its 240s),
    or has just lapsed. The poll renews it before it settles answers, and the
    worker again right before it runs a yes, so the command completes instead of
    being stopped by the lease watch seconds in (or waiting a poll)."""
    model, _ = _scripted([])
    w = _worker(tmp_path, model=model)
    cwd = str(w.session.cwd)
    command = "sleep 3; echo finished"
    facts = {"command": command, "cwd": cwd, "why_asking": "isn't on the safe list", "reason": "a test"}
    held = {"kind": "shell", "command": command, "cwd": cwd, "op_id": "op-aged"}
    req = w.board.hold(policy="shell.unsafe_command", session_id=SID, facts=facts, held=held, bypass=False)
    w.board.answer(req.id, req.question.yes_label, channel="test")
    assert lease.renew(SID, now=time.time() - (lease.LEASE_TTL_SECONDS - left_s))
    asyncio.run(w.tick() if via == "tick" else w.settle_answers())
    assert w.board.get(req.id).outcome == "yes: ran", w.board.get(req.id).outcome
    row = w.store.db.execute("SELECT status, exit_code, output FROM writes WHERE head = 'shell'").fetchone()
    assert (row["status"], row["exit_code"]) == ("ran", 0) and "finished" in row["output"]


def _held_shell(w, command: str = "make summary"):
    cwd = str(w.session.cwd)
    facts = {"command": command, "cwd": cwd, "why_asking": "isn't on the safe list", "reason": "a test"}
    held = {"kind": "shell", "command": command, "cwd": cwd, "op_id": "op-shell"}
    req = w.board.hold(policy="shell.unsafe_command", session_id=SID, facts=facts, held=held, bypass=False)
    w.board.answer(req.id, req.question.yes_label, channel="test")
    return req


@pytest.mark.parametrize("how", ["shell stopped", "shell timed out", "probe stopped"])
def test_a_yes_stopped_mid_run_is_resolved_stopped_not_ran(tmp_path, monkeypatch, how):
    """R3-12: a held command stopped while it ran (the switch moved, the lease
    was lost, its time ran out) is `yes: stopped (<why>)`, and the notice says it
    may have run in part -- never `yes: ran`."""
    from probe.daemon import shell as shell_mod

    moved = "the researcher moved the switch to `full`, so the daemon no longer records it"

    async def run(command, *, cwd, watch=None, **_):
        if how == "shell stopped":
            return shell_mod.ShellResult(None, "half of it", False, False, stopped=moved)
        return shell_mod.ShellResult(None, "half of it", False, True)

    async def run_probe(deps, argv, op_id):
        deps.stopped = moved
        return None, f"stopped while it ran ({moved}); it may have written part of its work", ""

    monkeypatch.setattr(shell_mod, "run", run)
    monkeypatch.setattr(tools, "_run_probe", run_probe)
    w = _worker(tmp_path)
    assert w._renew()
    req = _held_override(w, ["run", "tag", RUN, "svm"]) if how == "probe stopped" else _held_shell(w)
    asyncio.run(w.settle_answers())
    done = w.board.get(req.id)
    why = "it did not finish in time" if how == "shell timed out" else moved
    assert done.state == appr.APPROVED and done.outcome == f"yes: stopped ({why})", done.outcome
    notices = [e.text for e in w.store.pending() if e.kind == Kind.META]
    assert len(notices) == 1 and "stopped while it ran" in notices[0] and "may have run in part" in notices[0]


def test_a_failure_reporting_a_yes_that_ran_never_says_nothing_ran(tmp_path, monkeypatch):
    """R3-12: once the held action ran, a failure recording its outcome is
    logged -- never the pre-run "Nothing ran" notice, never a retry, never a
    second run."""
    ran = []

    async def run_probe(deps, argv, op_id):
        ran.append(argv)
        return 0, "{}", ""

    monkeypatch.setattr(tools, "_run_probe", run_probe)
    w = _worker(tmp_path)
    assert w._renew()
    req = _held_override(w, ["run", "tag", RUN, "svm"])
    real = w.board.resolve

    def resolve(r, *, state, outcome, channel=None):
        if outcome == "yes: ran":
            raise OSError("No space left on device")
        real(r, state=state, outcome=outcome, channel=channel)

    monkeypatch.setattr(w.board, "resolve", resolve)
    asyncio.run(w.settle_answers())
    assert ran == [["run", "tag", RUN, "svm"]]
    notices = [e.text for e in w.store.pending() if e.kind == Kind.META]
    assert not any("Nothing ran" in n for n in notices), notices
    assert req.id not in w.settle_retry
    asyncio.run(w.settle_answers())
    assert len(ran) == 1, "run a second time"


def test_the_device_counter_never_loses_an_update_between_sessions():
    errors = []

    def add():
        try:
            for _ in range(25):
                store_mod.add_device_tokens(1)
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=add) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert errors == [] and store_mod.device_tokens_today() == 200
    data = json.loads(store_mod.device_path().read_text())
    assert data["day"] == time.strftime("%Y-%m-%d", time.gmtime())
    assert not list(store_mod.device_path().parent.glob("*.tmp"))


def test_a_counter_that_cannot_be_written_never_replays_a_finished_bite(tmp_path, monkeypatch):
    def broken(n):
        raise FileNotFoundError("device.tmp")

    monkeypatch.setattr(worker_mod, "add_device_tokens", broken)
    model, _ = _scripted([])
    w = _worker(tmp_path, model=model, replay=Replay())
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert w.store.pending() == [] and w.store.recent_bites(1)[0]["outcome"] == "done"


def test_a_line_that_cannot_be_read_or_stored_is_skipped_and_the_cursor_moves_on(tmp_path, monkeypatch):
    w = _worker(tmp_path, replay=Replay())
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": "BOOM-PARSE"}}))
        handle.write(_line({"type": "user", "message": {"content": "BOOM-STORE"}}))
        handle.write(_line({"type": "user", "message": {"content": "the line after"}}))
    real_parse, real_add = w.adapter.parse_line, w.store.add

    def parse(obj, **kw):
        if "BOOM-PARSE" in json.dumps(obj):
            raise KeyError("an unexpected shape")
        return real_parse(obj, **kw)

    def add(events, **kw):
        if any("BOOM-STORE" in (e.text or "") for e in events):
            raise ValueError("not storable")
        return real_add(events, **kw)

    monkeypatch.setattr(w.adapter, "parse_line", parse)
    monkeypatch.setattr(w.store, "add", add)
    assert w.read_new() > 0
    assert w.store.search("line after") and not w.store.search("BOOM")
    assert w.store.cursor("main")[1] == w.session.transcript.stat().st_size


def _meta(w) -> list[str]:
    return [e.text for e in w.store.events_between(1) if e.kind == Kind.META]


def test_a_line_longer_than_a_chunk_is_read_whole_and_one_over_the_cap_is_skipped_loudly(tmp_path, monkeypatch):
    monkeypatch.setattr(worker_mod, "READ_CHUNK_BYTES", 1000)
    monkeypatch.setattr(worker_mod, "MAX_LINE_BYTES", 5000)
    w = _worker(tmp_path, replay=Replay())
    for _ in range(3):
        w.read_new()
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": "bigmarker " + "x" * 3000}}))
        handle.write(_line({"type": "user", "message": {"content": "hugemarker " + "y" * 8000}}))
        handle.write(_line({"type": "user", "message": {"content": "aftermarker"}}))
    for _ in range(10):
        w.read_new()
    assert w.store.search("bigmarker"), "a line between one chunk and the cap was dropped"
    assert not w.store.search("hugemarker") and w.store.search("aftermarker")
    skipped = [t for t in _meta(w) if "was skipped" in t]
    assert len(skipped) == 1 and "5,000 bytes" in skipped[0]
    assert w.store.cursor("main")[1] == w.session.transcript.stat().st_size
    # One still being written when read: skipped to the end, then past its newline, noticed once.
    with w.session.transcript.open("a") as handle:
        handle.write('{"type": "user", "message": {"content": "partialmarker ' + "z" * 6000)
    for _ in range(3):
        w.read_new()
    with w.session.transcript.open("a") as handle:
        handle.write("z" * 2000 + '"}}\n' + _line({"type": "user", "message": {"content": "resumedmarker"}}))
    for _ in range(3):
        w.read_new()
    assert w.store.search("resumedmarker") and not w.store.search("partialmarker")
    assert len([t for t in _meta(w) if "was skipped" in t]) == 2


def test_shutdown_reads_what_is_on_disk_to_its_end_not_one_chunk(tmp_path, monkeypatch):
    monkeypatch.setattr(worker_mod, "READ_CHUNK_BYTES", 300)
    model, _ = _scripted([])
    w = _worker(tmp_path, model=model, replay=Replay())
    with w.session.transcript.open("a") as handle:
        for i in range(40):
            handle.write(_line({"type": "user", "message": {"content": f"backlogmarker{i}"}}))
    _inbox([{"event": "run_start", "run_id": f"inboxrun{i}"} for i in range(20)])
    size = w.session.transcript.stat().st_size
    w.stopping = True
    asyncio.run(w.tick())
    assert w.store.cursor("main")[1] == size and w.store.search("backlogmarker39")
    assert w.store.cursor("sdk")[1] == worker_mod.inbox_path(SID).stat().st_size
    assert len([e for e in w.store.events_between(1) if e.kind == Kind.RUN_EVENT]) == 20
    # Written after shutdown began: not taken on.
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": "latemarker"}}))
    asyncio.run(w.tick())
    assert not w.store.search("latemarker")


def test_a_crash_is_logged_releases_the_lease_and_exits_for_a_backoff(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_DAEMON_KEY", "k-test")

    async def boom(self):
        raise RuntimeError("a bug in the loop")

    monkeypatch.setattr(worker_mod.Worker, "loop", boom)
    assert _run_main(_argv(tmp_path)) == worker_mod.EXIT_CRASHED
    assert "the daemon crashed (RuntimeError: a bug in the loop)" in _errors(tmp_path)
    assert _lease()["reason"] == lease.REASON_ERROR


# ---------------------------------------------------------------------------
# A5: the session-end deadline.
# ---------------------------------------------------------------------------


def test_no_bite_starts_after_the_session_end_deadline(tmp_path):
    now = [1000.0]
    model, calls = _raising(RuntimeError("provider down"))
    w = _worker(tmp_path, model=model, replay=Replay(), clock=lambda: now[0])
    w.stopping = True
    assert asyncio.run(w.tick()) is None and calls["n"] == 1  # one bite, failed: it waits to retry
    now[0] = w.finish_by + 1
    assert asyncio.run(w.tick()) == 0
    assert calls["n"] == 1, "a bite was dispatched past the deadline"
    assert "ended with" in _errors(tmp_path) and w.store.pending()


def test_a_bite_is_bounded_by_what_is_left_of_the_deadline(tmp_path):
    async def slow(messages, info):
        await asyncio.sleep(10)

    w = _worker(tmp_path, model=FunctionModel(slow), replay=Replay())
    w.read_new()
    w.stopping, w.finish_by = True, time.time() + 0.2
    started = time.monotonic()
    assert asyncio.run(w.run_bite("session end")) is False
    assert time.monotonic() - started < 5
    bite = w.store.recent_bites(1)[0]
    assert bite["outcome"] == "stopped: session end" and w.store.pending()


def test_sigterm_starts_the_finish_budget_at_the_signal_and_cancels_a_live_run_at_it(tmp_path, monkeypatch):
    """The deadline counts from the signal, not from the next round boundary: a
    model call still going when it passes is cancelled."""
    monkeypatch.setenv("PROBE_DAEMON_KEY", "k-test")
    monkeypatch.setattr(worker_mod, "FINISH_CAP_S", 0.5)
    seen: dict = {}

    async def slow(messages, info):
        seen["signal"] = time.time()
        os.kill(os.getpid(), signal.SIGTERM)  # the session ends while the model is thinking
        await asyncio.sleep(5)

    async def one_bite(self):
        self._model, self.replay = FunctionModel(slow), Replay()
        self.read_new()
        started = time.monotonic()
        seen["done"] = await self.run_bite("turn end")
        seen["took"] = time.monotonic() - started
        seen["finish_by"] = self.finish_by
        seen["outcome"] = self.store.recent_bites(1)[0]["outcome"]
        seen["pending"] = len(self.store.pending())
        return 0

    monkeypatch.setattr(worker_mod.Worker, "loop", one_bite)
    assert _run_main(_argv(tmp_path)) == 0
    assert seen["done"] is False and seen["took"] < 3, "the run went on past the deadline"
    assert seen["finish_by"] == pytest.approx(seen["signal"] + 0.5, abs=0.2), "the budget starts at the signal"
    assert seen["outcome"] == "stopped: session end" and seen["pending"] > 0


# ---------------------------------------------------------------------------
# E4: one long turn never blows the context; failed bites still count.
# ---------------------------------------------------------------------------


def _long_turn(st: store_mod.Store, n: int, *, chars: int = 3000) -> None:
    events = [Event(kind=Kind.PROMPT, stream="main", offset=1, text="THE PROMPT: run the whole sweep")]
    events += [Event(kind=Kind.AGENT_TEXT, stream="main", offset=10 + i, text=f"step {i} " + "x" * chars)
               for i in range(n)]
    st.add(events)


def test_a_long_current_turn_keeps_its_start_and_end_and_cuts_the_middle(tmp_path):
    st = store_mod.Store(tmp_path / "s.sqlite")
    _long_turn(st, 300)
    st.mark_covered(st.open_bite("test", None, None), st.pending()[-1].seq)
    st.add([Event(kind=Kind.AGENT_TEXT, stream="main", offset=100_000 + i, text=f"NEW-{i} result")
            for i in range(3)])
    built = bite_mod.build(st, trigger="age", context_line="", pending_lines=[], recent_writes=[])
    assert len(built.prompt) < bite_mod.TURN_SHOWN_TOKENS * bite_mod.CHARS_PER_TOKEN + 20_000
    assert "THE PROMPT: run the whole sweep" in built.prompt
    assert "earlier events of turn 1 not shown" in built.prompt and "session op=open turn=1" in built.prompt
    assert all(f"NEW-{i} result" in built.prompt for i in range(3))
    assert "step 299 " in built.prompt, "the end nearest the new events is kept"
    assert built.prompt.index("not shown") < built.prompt.index("new since your last bite")


def test_one_bite_covers_about_new_shown_tokens_and_leaves_the_rest_queued(tmp_path):
    st = store_mod.Store(tmp_path / "s.sqlite")
    _long_turn(st, 200)
    first, last = bite_mod.cover(st)
    covered = st.events_between(first, last)
    assert len(covered) < 201
    assert sum(bite_mod.shown_chars(e) for e in covered) <= (bite_mod.NEW_SHOWN_TOKENS * bite_mod.CHARS_PER_TOKEN)


def test_a_failed_bite_counts_what_it_spent(tmp_path):
    state = {"n": 0}

    def fn(messages, info):
        state["n"] += 1
        if state["n"] == 1:
            return ModelResponse(parts=[ToolCallPart("shell", {"command": "ls", "why": "look"})])
        raise RuntimeError("provider dropped the connection")

    w = _worker(tmp_path, model=FunctionModel(fn), replay=Replay())
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    bite = w.store.recent_bites(1)[0]
    assert bite["outcome"] == "failed" and bite["input_tokens"] > 0
    assert store_mod.device_tokens_today() == bite["input_tokens"] + bite["output_tokens"]


# ---------------------------------------------------------------------------
# E5 / E6 / G5: the folder check.
# ---------------------------------------------------------------------------


def test_working_folders_are_anywhere_but_home_above_it_system_trees_and_hidden(tmp_path):
    home = tmp_path / "home"
    (home / "proj" / ".hidden").mkdir(parents=True)
    outside = tmp_path / "elsewhere" / "proj"
    (outside / ".git").mkdir(parents=True)
    for system in ("/etc", "/tmp", "/usr", "/", "/var", "/proc"):
        assert not folders._ok_folder(Path(system), home, outside), system
    for system in ("/etc/ssl", "/usr/lib", "/usr/local/bin", "/var/log", "/proc/self", "/sys/kernel"):
        if Path(system).is_dir():
            assert not folders._ok_folder(Path(system), home, outside), system
    assert not folders._ok_folder(home, home) and not folders._ok_folder(tmp_path, home), "home and above"
    assert folders._ok_folder(home / "proj", home)
    assert not folders._ok_folder(home / "proj" / ".hidden", home)
    assert folders._ok_folder(outside, home, outside)
    assert not folders._ok_folder(outside / ".git", home, outside)
    # A session started in a system folder does not make the system folder its tree.
    assert not folders._ok_folder(Path("/etc/ssl"), home, Path("/etc"))
    # A data disk, a /workspace, a scratch folder under /tmp: kept (E5 was too narrow).
    for data in ("/data/ckpts", "/mnt/nvme/proj", "/workspace", "/workspace/run1", "/tmp/sweep", "/opt/proj"):
        assert not folders._system_tree(Path(data)), data
    for system in ("/etc/ssl", "/usr/lib", "/lib64/x", "/libx32", "/var/www", "/proc/1", "/root/x", "/boot/efi",
                   "/run/user", "/snap/core", "/sbin/x", "/dev/shm", "/private/var/folders"):
        assert folders._system_tree(Path(system)), system
    if not folders._system_tree(outside.resolve()):  # (a macOS temp folder is under /private/var)
        assert folders._ok_folder(outside, home), "outside $HOME and the session's tree, not a system tree"
        assert not folders._ok_folder(outside / ".git", home)


def test_working_folders_keep_a_folder_outside_home_the_session_worked_in(tmp_path):
    home = tmp_path / "home"
    work = home / "work"
    work.mkdir(parents=True)
    data = tmp_path / "data" / "ckpts"
    data.mkdir(parents=True)
    if folders._system_tree(data.resolve()):
        pytest.skip("this machine's temp folder is inside a system tree")
    st = store_mod.Store(tmp_path / "s.sqlite")
    st.add([Event(kind=Kind.TOOL_CALL, stream="main", offset=1, tool="Bash",
                  tool_input={"command": f"cd {data} && python train.py"}),
            Event(kind=Kind.TOOL_CALL, stream="main", offset=2, tool="Bash",
                  tool_input={"command": "cd /etc && cat hosts > /tmp/hosts.txt"})])
    found = folders.working_folders(st, work, home)
    assert found == [work.resolve(), data.resolve()]


def test_working_folders_keep_the_session_folder_and_the_most_recent(tmp_path):
    home = tmp_path / "home"
    work = home / "work"
    work.mkdir(parents=True)
    st = store_mod.Store(tmp_path / "s.sqlite")
    events = []
    for i in range(12):
        (home / f"d{i}").mkdir()
        events.append(Event(kind=Kind.TOOL_CALL, stream="main", offset=i + 1, tool="Bash",
                            tool_input={"command": f"cd {home / f'd{i}'} && ls"}))
    st.add(events)
    found = folders.working_folders(st, work, home)
    assert len(found) == folders.MAX_WORKING_FOLDERS
    assert found[0] == work.resolve() and found[1] == (home / "d11").resolve()
    assert (home / "d0").resolve() not in found


def test_the_check_caps_files_and_stored_text(tmp_path, monkeypatch):
    home = tmp_path / "home"
    work = home / "work"
    work.mkdir(parents=True)
    st = store_mod.Store(tmp_path / "s.sqlite")
    for i in range(20):
        (work / f"f{i:02}.txt").write_text("y" * 80)
    monkeypatch.setattr(folders, "MAX_FILES_PER_CHECK", 5)
    monkeypatch.setattr(folders, "MAX_TEXT_STORED", 200)
    folders.check(st, work, home, emit=False)
    rows = list(st.db.execute("SELECT path, text FROM files"))
    assert len(rows) == 5
    assert sum(1 for r in rows if r["text"]) == 2 and st.stored_text_bytes() <= 200


def test_a_credential_shaped_file_is_reported_without_its_content(tmp_path):
    home = tmp_path / "home"
    work = home / "work"
    work.mkdir(parents=True)
    st = store_mod.Store(tmp_path / "s.sqlite")
    asyncio.run(folders.baseline(st, work, home))
    (work / "service.key").write_text("TOPSECRETVALUE\n")
    (work / "notes.md").write_text("plain notes\n")
    assert folders.check(st, work, home) == 2
    texts = {e.text.split(" ")[2]: e.text for e in st.pending()}
    key = texts[str(work / "service.key")]
    assert "credential-shaped" in key and "TOPSECRETVALUE" not in key
    assert "plain notes" in texts[str(work / "notes.md")]
    assert st.file_row(str(work / "service.key"))["text"] is None


def test_the_folder_check_never_follows_a_symlink(tmp_path):
    home = tmp_path / "home"
    work = home / "work"
    work.mkdir(parents=True)
    secret = tmp_path / "outside" / "creds.txt"
    secret.parent.mkdir()
    secret.write_text("TOPSECRET-VALUE\n")
    st = store_mod.Store(tmp_path / "s.sqlite")
    asyncio.run(folders.baseline(st, work, home))
    (work / "link.txt").symlink_to(secret)
    (work / "linked-dir").symlink_to(secret.parent, target_is_directory=True)
    (work / "notes.md").write_text("plain notes\n")
    assert folders.check(st, work, home) == 1
    texts = [e.text for e in st.pending()]
    assert not any("TOPSECRET" in t or "link" in t for t in texts), texts
    assert st.file_row(str(work / "link.txt")) is None and "plain notes" in texts[0]


def test_the_folder_check_never_blocks_on_a_fifo(tmp_path):
    home = tmp_path / "home"
    work = home / "work"
    work.mkdir(parents=True)
    st = store_mod.Store(tmp_path / "s.sqlite")
    asyncio.run(folders.baseline(st, work, home))
    os.mkfifo(work / "pipe")
    (work / "notes.md").write_text("plain notes\n")
    folders_, known, is_secret, room = folders._prepare(st, work, home, None)
    found = []
    thread = threading.Thread(target=lambda: found.append(folders.scan(folders_, known, is_secret=is_secret,
                                                                          text_room=room)), daemon=True)
    thread.start()
    thread.join(10)
    assert not thread.is_alive(), "the check blocked opening a FIFO"
    assert [s.path for s in found[0]] == [str(work / "notes.md")]


def test_the_stored_text_total_is_kept_not_summed_on_every_check(tmp_path):
    st = store_mod.Store(tmp_path / "s.sqlite")
    st.set_file("/w/a", 1, 1.0, "x" * 100)
    st.set_file("/w/b", 1, 1.0, "y" * 50)
    st.set_file("/w/a", 1, 2.0, "z" * 10)
    st.set_file("/w/c", 1, 1.0, None)
    statements: list[str] = []
    st.db.set_trace_callback(statements.append)
    assert st.stored_text_bytes() == 60
    assert not any("sum(" in q.lower() for q in statements), statements
    st.db.set_trace_callback(None)
    # A store written before the total existed sums once.
    st.db.execute("DELETE FROM meta WHERE key = 'files_text_chars'")
    assert st.stored_text_bytes() == 60 and st.meta("files_text_chars") == "60"


def test_the_folder_check_runs_off_the_loop_and_at_most_every_30s(tmp_path, monkeypatch):
    now = [1000.0]
    threads = []
    real_scan = folders.scan

    def scan(*a, **kw):
        threads.append(threading.current_thread() is threading.main_thread())
        return real_scan(*a, **kw)

    monkeypatch.setattr(folders, "scan", scan)
    model, _ = _scripted([])
    w = _worker(tmp_path, model=model, replay=Replay(), clock=lambda: now[0])
    for _ in range(3):
        with w.session.transcript.open("a") as handle:
            handle.write(_line({"type": "user", "message": {"content": f"prompt at {now[0]}"}}))
            handle.write(_line({"type": "system", "subtype": "turn_duration", "durationMs": 5}))
        asyncio.run(w.tick())
        now[0] += 10
    assert threads == [False], "one check, in a worker thread"
    now[0] += folders_check_s()
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "system", "subtype": "turn_duration", "durationMs": 5}))
    asyncio.run(w.tick())
    assert threads == [False, False]


def folders_check_s() -> float:
    return worker_mod.FOLDER_CHECK_S


def test_old_files_of_dead_sessions_are_swept_at_start(tmp_path):
    base = store_mod.state_dir()
    base.mkdir(parents=True, exist_ok=True)
    old = time.time() - 40 * 86400
    for sid in ("dead", "live", "recent"):
        for suffix in (".sqlite", ".inbox.jsonl", ".log"):
            (base / f"{sid}{suffix}").write_text("x")
            if sid != "recent":
                os.utime(base / f"{sid}{suffix}", (old, old))
    (base / "device.json").write_text("{}")
    os.utime(base / "device.json", (old, old))
    live = (base / "live.lock").open("a")
    fcntl.flock(live.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    try:
        assert worker_mod.sweep_stale(SID) == 3
    finally:
        live.close()
    left = sorted(p.name for p in base.iterdir() if not p.name.endswith(".lock"))
    assert left == ["device.json", "live.inbox.jsonl", "live.log", "live.sqlite",
                    "recent.inbox.jsonl", "recent.log", "recent.sqlite"]


# ---------------------------------------------------------------------------
# E7 / E8 / E9: per-bite aggregates, the inbox, "Not recorded yet".
# ---------------------------------------------------------------------------


def test_a_bite_aggregates_the_events_table_once_and_through_an_index(tmp_path, monkeypatch):
    st = store_mod.Store(tmp_path / "s.sqlite")
    _long_turn(st, 5, chars=10)
    seen = []
    real = st.shown_turn_sizes
    monkeypatch.setattr(st, "shown_turn_sizes", lambda: seen.append(1) or real())
    assert bite_mod.build(st, trigger="age", context_line="", pending_lines=[], recent_writes=[]) is not None
    assert seen == [1]
    plan = " ".join(str(tuple(r)) for r in st.db.execute(
        "EXPLAIN QUERY PLAN SELECT turn, min(seq), sum(chars) FROM events GROUP BY turn"))
    assert "COVERING INDEX events_sizes" in plan


def _inbox(msgs: list[dict], mode: str = "w") -> None:
    path = worker_mod.inbox_path(SID)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open(mode) as handle:
        handle.write("".join(json.dumps(m) + "\n" for m in msgs))


def test_an_inbox_rewritten_shorter_is_read_again_from_the_start(tmp_path):
    w = _worker(tmp_path, replay=Replay())
    _inbox([{"event": "run_start", "run_id": f"r{i}", "description": "x" * 50} for i in range(3)])
    w.read_new()
    _inbox([{"event": "run_start", "run_id": "after-rotation"}])
    w.read_new()
    runs = [e.text for e in w.store.events_between(1) if e.kind == Kind.RUN_EVENT]
    assert len(runs) == 4 and "after-rotation" in runs[-1]


def test_the_inbox_is_read_a_chunk_at_a_time(tmp_path, monkeypatch):
    monkeypatch.setattr(worker_mod, "READ_CHUNK_BYTES", 120)
    w = _worker(tmp_path, replay=Replay())
    _inbox([{"event": "run_start", "run_id": f"run-{i}"} for i in range(10)])
    size = worker_mod.inbox_path(SID).stat().st_size
    w.read_new()
    assert 0 < w.store.cursor("sdk")[1] <= 120
    for _ in range(20):
        w.read_new()
    assert w.store.cursor("sdk")[1] == size
    assert len([e for e in w.store.events_between(1) if e.kind == Kind.RUN_EVENT]) == 10


def test_notices_never_collide_when_the_clock_repeats(tmp_path, monkeypatch):
    monkeypatch.setattr(time, "time_ns", lambda: 42)
    monkeypatch.setattr(time, "time", lambda: 42.0)
    w = _worker(tmp_path, replay=Replay())
    w._notice("the researcher said no to question a1b")
    w._notice("the researcher said no to question c2d")
    texts = [e.text for e in w.store.pending() if e.kind == Kind.META]
    assert texts == ["the researcher said no to question a1b", "the researcher said no to question c2d"]


def test_not_recorded_yet_drops_failures_a_later_write_superseded(tmp_path):
    now = [1000.0]
    w = _worker(tmp_path, replay=Replay(), clock=lambda: now[0])
    st = w.store
    bite = st.open_bite("t", None, None)
    st.log_write(bite=bite, op_id="1", argv=["probe", "run", "tag", "R1", "svm"], head="run tag", status="failed",
                 reason="timeout")
    st.log_write(bite=bite, op_id="2", argv=["probe", "run", "tag", "R2", "svm"], head="run tag", status="failed",
                 reason="timeout")
    st.log_write(bite=bite, op_id="3", argv=["probe", "run", "tag", "R1", "svm"], head="run tag", status="ran")
    lines = [line for line in w.pending_lines() if line.startswith("failed")]
    assert len(lines) == 1 and "R2" in lines[0]
    # Failures older than the last FAILURES_SHOWN_BITES bites are no longer listed.
    for _ in range(worker_mod.FAILURES_SHOWN_BITES - 1):
        now[0] += 60
        st.open_bite("later", None, None)
    assert [line for line in w.pending_lines() if line.startswith("failed")]
    now[0] += 60
    st.open_bite("later", None, None)
    assert not [line for line in w.pending_lines() if line.startswith("failed")]


# ---------------------------------------------------------------------------
# E11 / G4 / G6 / the model's timeout.
# ---------------------------------------------------------------------------


def test_provisioning_fetches_only_the_half_that_is_missing(monkeypatch):
    """R12: the key is approved only when missing (a second approval mints a
    second key for nothing), and the libraries install only when missing, with
    no approval -- the key-held, libraries-missing machine is the one whose
    switch to the daemon failed on "missing packages"."""
    import importlib

    from probe.cli import companion, daemon_cli
    from probe.cli import setup as wizard

    main = importlib.import_module("probe.cli.main")
    approvals, installs = [], []
    key = {"held": False}

    def approve(base, open_browser=True):
        approvals.append(base)
        key["held"] = True
        return ["key approved"]

    monkeypatch.setattr(main, "_authorize_companion", approve)
    monkeypatch.setattr(wizard, "companion_token_held", lambda: key["held"])
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: None)
    monkeypatch.setattr(daemon_cli, "daemon_install", lambda: installs.append(1))
    said = []
    assert companion.provision_daemon("https://x", say=said.append) == ["key approved"] == said
    assert (approvals, installs) == (["https://x"], [1]), "nothing held: both halves"

    assert companion.provision_daemon("https://x") == []
    assert (approvals, installs) == (["https://x"], [1, 1]), "key held: libraries only, no approval"

    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: "2.51")
    companion.provision_daemon("https://x")
    assert (approvals, installs) == (["https://x"], [1, 1]), "both held: nothing"

    key["held"] = False
    monkeypatch.setattr(main, "_authorize_companion", lambda base, open_browser=True: ["declined"])
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: None)
    assert companion.provision_daemon("https://x") == ["declined"]
    assert installs == [1, 1], "no key: no install either"


def test_the_mcp_is_offered_only_beside_the_api_the_key_belongs_to(monkeypatch):
    from probe.daemon import agent

    monkeypatch.delenv("PROBE_MCP_URL", raising=False)
    assert agent.mcp_url("https://api.research.prbe.ai") == agent.STOCK_MCP_URL
    assert agent.mcp_url("https://probe.internal.example") is None
    monkeypatch.setenv("PROBE_MCP_URL", "https://mcp.internal.example/mcp")
    assert agent.mcp_url("https://probe.internal.example") == "https://mcp.internal.example/mcp"


@pytest.mark.parametrize("switch", ["daemon", "full"])
def test_every_tool_call_is_gated_by_the_lease_mcp_reads_included(tmp_path, switch):
    from pydantic_ai.messages import ToolReturnPart
    from pydantic_ai.toolsets import FunctionToolset

    from probe.daemon import agent as agent_mod

    reads = []

    def browse(query: str) -> str:
        """A stand-in for the Probe MCP's read tools: a toolset the daemon did not write."""
        reads.append(query)
        return "the team's projects"

    answers = []

    def fn(messages, info: AgentInfo) -> ModelResponse:
        returns = [p for m in messages for p in getattr(m, "parts", []) if isinstance(p, ToolReturnPart)]
        if not returns:
            return ModelResponse(parts=[ToolCallPart("browse", {"query": "projects"})])
        answers.append(str(returns[-1].content))
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"summary": "note"})])

    w = _worker(tmp_path, replay=None)
    assert w._renew()
    deps = w.deps(None)
    _set_state(switch)
    agent = agent_mod.build_agent("instructions", model=FunctionModel(fn))
    result = asyncio.run(agent.run("go", deps=deps, toolsets=[FunctionToolset([browse])]))
    assert result.output.summary == "note", "the bite can still end"
    if switch == "daemon":
        assert reads == ["projects"] and answers == ["the team's projects"] and deps.stopped is None
    else:
        assert reads == [], "a read ran after the switch moved"
        assert answers and answers[0].startswith(tools.NO_LEASE) and "full" in deps.stopped


def test_the_session_tools_answer_through_the_agent_not_a_thread_error(tmp_path):
    """`session` through the real agent tool path: as plain `def` tools Pydantic
    AI ran the session reads in a worker thread, the store's SQLite connection
    refused it, and every call answered "tool error (ProgrammingError)"
    (0.186.0, 0.186.1)."""
    from pydantic_ai.messages import ToolReturnPart

    answers = []

    def fn(messages, info: AgentInfo) -> ModelResponse:
        returns = [p for m in messages for p in getattr(m, "parts", []) if isinstance(p, ToolReturnPart)]
        if not returns:
            return ModelResponse(parts=[ToolCallPart("session", {"op": "outline"}),
                                        ToolCallPart("session", {"op": "search", "query": "SVM"})])
        answers.extend(str(p.content) for p in returns)
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"summary": "note"})])

    w = _worker(tmp_path, model=FunctionModel(fn), replay=Replay())
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert len(answers) == 2 and not any("tool error" in a for a in answers), answers
    assert any("turn 1 ·" in a for a in answers) and any("SVM C=10: 0.9889." in a for a in answers)


def test_doctor_reads_the_daemons_device_counter(tmp_path):
    from probe.cli import companion, doctor

    store_mod.add_device_tokens(1234)
    assert companion.tokens_today() == 1234
    assert "1,234 (UTC day)" in "\n".join(doctor._daemon_rows())


def test_companion_log_reads_a_v2_sessions_logbook(tmp_path, monkeypatch, capsys):
    from probe.cli import companion

    w = _worker(tmp_path, replay=Replay())
    w.store.log_write(bite=None, op_id="1", argv=["probe", "run", "tag", RUN, "svm"], head="run tag", status="ran")
    monkeypatch.setattr(companion, "_session", lambda s: SID)
    companion.log_cmd(session=SID, status=None)
    out = json.loads(capsys.readouterr().out)
    assert out["writes"][0]["command"] == f"probe run tag {RUN} svm" and out["writes"][0]["status"] == "ran"


def test_the_model_client_outlasts_the_servers_deadline_and_names_its_lane():
    """A daemon model call may take 30 minutes: the client's timeout sits above the
    server's (1,830 s), so the layer that fails is the one that reports. Each lane
    sends its header and its own model name."""
    from probe.daemon import model

    ep = model.Endpoint("https://api.example.test", "k")
    built = model.build(ep)
    assert model.DEFAULT_TIMEOUT_S == 1900.0
    assert built.settings["timeout"] == model.DEFAULT_TIMEOUT_S
    assert built.client.timeout == model.DEFAULT_TIMEOUT_S and built.client.max_retries == model.MAX_RETRIES
    assert str(built.client.base_url).startswith("https://api.example.test/v1/companion")
    assert built.client.default_headers[model.LANE_HEADER] == model.LANE_WRITE
    assert built.model_name == "default"
    reader = model.build(ep, model.LANE_READ)
    assert reader.client.default_headers[model.LANE_HEADER] == model.LANE_READ
    assert reader.model_name == "reader"


def test_the_lease_is_renewed_while_a_model_call_runs():
    """The lease lives 240 s and a call may take 30 min: keep_lease renews a lease
    this process holds while the run is in progress (compaction's summary call
    included), and never one it released."""
    from probe.daemon.agent import keep_lease

    deps = types.SimpleNamespace(session_id=SID, replay=None)

    async def slow(_request):
        await asyncio.sleep(0.35)
        return "answer"

    def renewed_at() -> float:
        return json.loads(lease.lease_path(SID).read_text())["renewed_at"]

    assert lease.renew(SID, now=time.time() - 100)
    before = renewed_at()
    async def run():
        async with keep_lease(deps, every_s=0.1):
            return await slow(None)

    got = asyncio.run(run())
    assert got == "answer"
    assert renewed_at() > before + 50
    assert lease.may_write(SID) is None

    lease.release(SID, lease.REASON_BUDGET)
    released = renewed_at()
    asyncio.run(run())
    assert renewed_at() == released
    assert json.loads(lease.lease_path(SID).read_text())["reason"] == lease.REASON_BUDGET


def test_a_yes_shell_command_stops_when_the_switch_moves_while_it_runs(tmp_path):
    """A held shell command run on a yes is watched like a tool's: the researcher
    moving the switch while it runs stops its process group (G-8, worker side)."""
    w = _worker(tmp_path)
    assert w._renew()
    cwd = str(w.session.cwd)
    facts = {"command": "sleep 30", "cwd": cwd, "why_asking": "isn't on the safe list", "reason": "a test"}
    held = {"kind": "shell", "command": "sleep 30", "cwd": cwd, "op_id": "op-shell"}
    req = w.board.hold(policy="shell.unsafe_command", session_id=SID, facts=facts, held=held, bypass=False)
    w.board.answer(req.id, req.question.yes_label, channel="test")

    async def go():
        async def flip():
            await asyncio.sleep(1.0)
            _set_state("full")

        flipper = asyncio.create_task(flip())
        started = time.monotonic()
        await w.settle_answers()
        await flipper
        return time.monotonic() - started

    elapsed = asyncio.run(go())
    assert elapsed < 10, f"the command ran on for {elapsed:.0f}s after the switch moved"
    row = w.store.db.execute("SELECT status FROM writes WHERE head = 'shell'").fetchone()
    assert row is not None and row["status"].startswith("stopped"), row and row["status"]
    assert w.board.get(req.id).outcome.startswith("yes: stopped ("), w.board.get(req.id).outcome


def test_the_model_connection_keeps_itself_alive_and_is_shared():
    """A 30-minute non-streaming call is silent until its answer: TCP keepalive
    keeps a NAT between this machine and Probe from dropping it. One HTTP client
    serves both lanes and every turn (no client per turn left open)."""
    import socket

    from probe.daemon import model

    opts = model.keepalive_socket_options()
    assert (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) in opts
    assert any(value == model.KEEPALIVE_IDLE_S for _, _, value in opts[1:2]) or len(opts) == 1
    ep = model.Endpoint("https://api.example.test", "k")
    reader, writer = model.build(ep, model.LANE_READ), model.build(ep)
    assert reader.client._client is writer.client._client


# ---------------------------------------------------------------------------
# `read only (daemon)` (Richard 2026-09-29): the reader keeps reading, the writer
# records nothing -- not while the switch reads it, not once it is back on.
# ---------------------------------------------------------------------------


def _daemon_profile() -> None:
    (lease.sessions_dir() / f"{SID}.profile").write_text("daemon")


def _bites_by_text(w) -> dict[str, object]:
    return {row["text"]: row["bite"] for row in w.store.db.execute("SELECT text, bite FROM events")}


def test_read_only_keeps_the_worker_for_its_reader_and_records_none_of_it(tmp_path):
    _daemon_profile()
    model, _ = _scripted([])
    w = _worker(tmp_path, model=model)
    w.reader = object()  # the reader's task runs beside tick() (`loop`)
    assert w._renew() and lease.held(SID)
    w.read_new()  # what arrived while on (daemon): still the writer's

    _set_state("read-only")
    assert asyncio.run(w.tick()) is None, "the worker stays for its reader"
    assert _lease()["reason"] == lease.REASON_STOPPED, "the writer let go of the lease"
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": "now try C=100"}, "cwd": str(w.session.cwd)}))
    assert asyncio.run(w.tick()) is None
    texts = _bites_by_text(w)
    assert texts["now try C=100"] == store_mod.UNRECORDED_BITE, "the reader's alone: no bite covers it"
    assert texts["sweep C for an SVM on digits"] is None, "what arrived while on stays pending"

    _set_state("daemon")
    assert asyncio.run(w.tick()) is None
    assert lease.held(SID), "back on: the lease comes back"
    texts = _bites_by_text(w)
    assert texts["now try C=100"] == store_mod.UNRECORDED_BITE, "still never recorded"
    assert any("read only from turn" in (text or "") for text in texts), "the writer is told once"


def test_the_writer_never_sees_read_only_events_even_beside_pending_ones(tmp_path):
    """Review of #2172: a bite cut short by the switch leaves turn T pending; the
    span after `/probe on` then runs across the read-only rows. None of them may
    reach the writer -- not the next bite, not the conversation's next message,
    not its session tool."""
    _daemon_profile()
    w = _worker(tmp_path)
    w.reader = object()
    w.read_new()  # turn T, still pending (its bite was stopped by the switch)
    _set_state("read-only")
    asyncio.run(w.tick())
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": "SECRET said during read only"},
                            "cwd": str(w.session.cwd)}))
        handle.write(_line({"type": "assistant", "message": {"content": [{"type": "text", "text": "SECRET reply"}]}}))
    asyncio.run(w.tick())
    _set_state("daemon")
    asyncio.run(w._end_read_only())  # what tick() does first once the switch is back on

    built = bite_mod.build(w.store, trigger="age", context_line="", pending_lines=[], recent_writes=[])
    assert built is not None and "SECRET" not in built.prompt
    assert "sweep C for an SVM on digits" in built.prompt, "turn T is still the writer's"
    assert "read only from turn" in built.prompt
    nxt = bite_mod.build_next(w.store, trigger="age", instructions="x")
    assert nxt is not None and "SECRET" not in nxt.prompt
    assert "SECRET" not in tools._outline(w.store, recorded=True)
    assert not w.store.search("SECRET", recorded=True)
    assert w.store.search("SECRET"), "the reader still finds it"


def test_read_only_without_a_reader_still_marks_what_arrives(tmp_path):
    _daemon_profile()
    _set_state("read-only")
    w = _worker(tmp_path)
    assert asyncio.run(w.tick()) is None, "the worker stays, so nothing read later is recorded"
    assert _bites_by_text(w)["sweep C for an SVM on digits"] == store_mod.UNRECORDED_BITE


def test_a_worker_started_after_a_crash_knows_read_only_began(tmp_path):
    _daemon_profile()
    w = _worker(tmp_path)
    w.reader = object()
    _set_state("read-only")
    asyncio.run(w.tick())
    turn = w.read_only_turn
    again = _worker(tmp_path)
    assert (again.read_only_from, again.read_only_turn) == (w.read_only_from, turn)
    _set_state("daemon")
    asyncio.run(again._end_read_only())
    assert again.store.fact(worker_mod.READ_ONLY_FROM) is None


def test_read_only_in_the_agent_profile_still_ends_the_worker(tmp_path):
    w = _worker(tmp_path)
    w.reader = object()
    _set_state("read-only")
    assert asyncio.run(w.tick()) == 0
    assert _lease()["reason"] == lease.REASON_STOPPED


def test_a_folder_only_read_only_touched_is_not_the_writers(tmp_path):
    _daemon_profile()
    w = _worker(tmp_path)
    w.reader = object()
    _set_state("read-only")
    asyncio.run(w.tick())
    secret = w.session.cwd.parent / "secret"
    secret.mkdir()
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "assistant", "cwd": str(w.session.cwd), "message": {"content": [
            {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": f"cd {secret} && python train.py"}}]}}))
    asyncio.run(w.tick())
    assert secret.resolve() not in folders.working_folders(w.store, w.session.cwd, w.session.home)


def test_the_folder_snapshot_moves_on_silently_in_read_only(tmp_path, monkeypatch):
    _daemon_profile()
    w = _worker(tmp_path)
    w.reader = object()
    seen = []

    async def check(workdirs, *, emit=True, force=False):
        seen.append((emit, force))

    monkeypatch.setattr(w, "_check_folders", check)
    _set_state("read-only")
    asyncio.run(w.tick())
    assert seen == [(False, False)], "read only: the snapshot moves on, nothing is announced"
    _set_state("daemon")
    asyncio.run(w._end_read_only())
    assert seen[-1] == (False, True), "and once more, forced, before the first bite back"


def test_what_read_only_left_unread_is_marked_by_its_stamps(tmp_path):
    """No worker ran while the switch read `read only (daemon)` (a crash backoff):
    the next one marks, by stamp, what was written before the switch moved back."""
    _daemon_profile()
    w = _worker(tmp_path)
    w.reader = object()
    _set_state("read-only")
    asyncio.run(w.tick())  # read only began here
    with w.session.transcript.open("a") as handle:  # written while nobody read
        handle.write(_line({"type": "user", "timestamp": "2026-09-29T05:00:00.000Z",
                            "message": {"content": "SECRET while read only"}, "cwd": str(w.session.cwd)}))
    _set_state("daemon")
    state = lease.sessions_dir() / f"{SID}.state"
    moved_back = time.mktime(time.strptime("2026-09-29 06:00:00", "%Y-%m-%d %H:%M:%S")) - time.timezone
    os.utime(state, (moved_back, moved_back))
    with w.session.transcript.open("a") as handle:  # written after the switch moved back
        handle.write(_line({"type": "user", "timestamp": "2026-09-29T07:00:00.000Z",
                            "message": {"content": "back on"}, "cwd": str(w.session.cwd)}))
    written = w.session.transcript.read_text()
    later = _worker(tmp_path)  # a fresh worker, same store (the helper rewrites the chat log)
    later.reader = object()
    later.session.transcript.write_text(written)
    asyncio.run(later._end_read_only())
    texts = _bites_by_text(later)
    assert texts["SECRET while read only"] == store_mod.UNRECORDED_BITE
    assert texts["back on"] is None, "after the switch moved back: the writer's"
