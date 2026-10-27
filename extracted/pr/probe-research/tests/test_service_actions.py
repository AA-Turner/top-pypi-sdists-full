"""Actions over the service socket (plan X5, X2, A5): real service, real child processes.

`action.run` answers an `action_id` before any work and journals everything;
`action.status` / `action.events` answer from the journal, also after the
service restarted; a `client_request_id` never runs twice; one mutating action
at a time; `action.cancel` only while the child waits for a browser approval;
the child gets the request's context and never the launcher's credentials; an
action in progress keeps the service alive. The `probe.core.run` children are
played by `service_fakes.FakeCore` (the real ones: `test_core_run.py`).
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest

from probe.service import client, paths
from probe.service.protocol import ErrorCode, Method
from tests.service_fakes import FakeCore, events_until
from tests.service_harness import pid_running, service_home as service_home, wait_for

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")

STEP = {"event": "step", "name": "sign_in", "status": "done", "message": "signed in", "agent": None}
PROMPT = {
    "event": "device_prompt",
    "verification_uri": "https://example.invalid/device",
    "verification_uri_complete": "https://example.invalid/device?code=ABCD",
    "user_code": "ABCD",
    "expires_in": 600,
}


@pytest.fixture
def core(service_home):
    return FakeCore(service_home.home)


def _run(conn, action="configure", params=None, crid="req-1", **extra):
    body = {"action": action, "params": {"agents": ["claude"]} if params is None else params,
            "client_request_id": crid, **extra}
    return conn.call(Method.ACTION_RUN, body)


def _wait_done(conn, action_id, timeout=10.0) -> dict:
    status = wait_for(lambda: (s := conn.call(Method.ACTION_STATUS, {"action_id": action_id}))["state"] == "done" and s,
                      timeout)
    assert status, conn.call(Method.ACTION_STATUS, {"action_id": action_id})
    return status


def test_run_answers_an_id_then_streams_and_journals_the_events(service_home, core):
    core.plan("configure", steps=[{"event": STEP}])
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": ["action.event", "action.done"]})
        answer = _run(conn, params={"agents": ["claude"], "capture": False})
        action_id = answer["action_id"]
        assert set(answer) == {"action_id"} and action_id.startswith("act_")
        seen = events_until(conn, lambda e: e["topic"] == "action.done", 10.0)
        status = _wait_done(conn, action_id)
        replay = conn.call(Method.ACTION_EVENTS, {"action_id": action_id, "since": 0})
        later = conn.call(Method.ACTION_EVENTS, {"action_id": action_id, "since": 1})
    streamed = [e for e in seen if e["topic"] == "action.event"]
    assert [e["seq"] for e in streamed] == [1, 2]
    assert [e["event"]["event"] for e in streamed] == ["step", "done"]
    assert all(e["action_id"] == action_id for e in seen)
    assert seen[-1]["done"]["ok"] is True
    assert status["action"] == "configure" and status["done"]["exit_code"] == 0
    assert status["cancelled"] is False
    assert isinstance(status["started_at"], float) and status["ended_at"] >= status["started_at"]
    assert [e["seq"] for e in replay["events"]] == [1, 2] and replay["done"] is True
    assert [e["seq"] for e in later["events"]] == [2]
    (call,) = core.calls("configure")
    assert json.loads(call["stdin"]) == {"agents": ["claude"], "capture": False}
    assert call["flags"] == ["-I"]
    assert os.path.realpath(call["cwd"]) == os.path.realpath(service_home.home)  # macOS: /tmp is /private/tmp
    journal = paths.actions_dir() / f"{action_id}.jsonl"
    assert journal.stat().st_mode & 0o777 == 0o600
    kinds = [json.loads(line)["type"] for line in journal.read_text().splitlines()]
    assert kinds == ["accepted", "child", "event", "event", "ended"]


def test_a_client_request_id_runs_once(service_home, core):
    core.plan("recorder", steps=[{"event": STEP}])
    service_home.start()
    with service_home.connect() as conn:
        first = _run(conn, "recorder", {"who_records": "daemon"}, crid="same")["action_id"]
        _wait_done(conn, first)
        again = _run(conn, "recorder", {"who_records": "daemon"}, crid="same")
    assert again == {"action_id": first, "existing": True}
    assert len(core.calls("recorder")) == 1


def test_reinstall_flag_reaches_the_core_child_without_setup_defaults(service_home, core):
    core.plan("configure")
    service_home.start()
    params = {"agents": ["claude"], "reinstall": True}
    with service_home.connect() as conn:
        action = _run(conn, params=params)["action_id"]
        assert _wait_done(conn, action)["done"]["complete"] is True
    (call,) = core.calls("configure")
    assert json.loads(call["stdin"]) == params


def test_one_mutating_action_at_a_time(service_home, core):
    gate = service_home.home / "release"
    core.plan("logout", steps=[{"event": STEP}, {"wait": str(gate)}])
    service_home.start()
    with service_home.connect() as conn:
        holder = _run(conn, "logout", {}, crid="a")["action_id"]
        wait_for(lambda: core.calls("logout"), 5.0)
        with pytest.raises(client.ServiceError) as raised:
            _run(conn, "session_default", {"state": "read"}, crid="b")
        assert raised.value.code == ErrorCode.BUSY == -32010
        assert raised.value.data == {"holder": {"kind": "action", "action_id": holder, "action": "logout"}}
        assert conn.call(Method.STATUS)["actions"]["running"]["action_id"] == holder
        gate.touch()
        _wait_done(conn, holder)
        second = _run(conn, "session_default", {"state": "read"}, crid="b")["action_id"]
        _wait_done(conn, second)
    (later,) = core.calls("session_default")
    assert later["at"] > core.calls("logout")[0]["at"]


#: An action child that hangs; with `done`, one that writes its own `done` as
#: SIGTERM stops it, as `probe.core.events`' handler does.
_HANG = """
import json, os, signal, sys, time
open(sys.argv[1], "w").write(str(os.getpid()))
if sys.argv[2] == "done":
    def stopped(*_):
        print(json.dumps({"v": 1, "event": "done", "ok": False, "complete": False, "exit_code": 143, "steps": []}),
              flush=True)
        sys.exit(143)
    signal.signal(signal.SIGTERM, stopped)
time.sleep(120)
"""


def _in_process_actions(tmp_path, monkeypatch):
    from probe.service import actions, loginenv

    for name, sub in (("HOME", "home"), ("XDG_STATE_HOME", "state"), ("XDG_CONFIG_HOME", "config"),
                      ("CLAUDE_CONFIG_DIR", "claude"), ("CODEX_HOME", "codex"), ("PI_CODING_AGENT_DIR", "pi")):
        monkeypatch.setenv(name, str(tmp_path / sub))
    monkeypatch.setenv(actions.ACTION_TIMEOUT_ENV, "1")
    monkeypatch.setenv(actions.ACTION_STOP_GRACE_ENV, "5")

    async def no_login_shell(**_kw):
        return {}

    monkeypatch.setattr(loginenv, "child_env", no_login_shell)
    (tmp_path / "home").mkdir()
    return actions


@pytest.mark.parametrize("child", ["hangs", "done"])
def test_an_action_past_its_time_limit_is_stopped_and_fails(tmp_path, monkeypatch, child):
    """An action child that never returned held the one mutating slot -- and
    every update, which defers on a running action -- for good (plan C1). Past
    its limit its process group is stopped, the action fails saying why (also
    when the child writes its own `done` as it stops), and the slot is free for
    the next one. In process: a service `ensure` starts gets no test override
    (`client.ENV_ALLOWLIST`)."""
    import asyncio

    from probe.service import children

    actions = _in_process_actions(tmp_path, monkeypatch)
    pidfile = tmp_path / "child.pid"
    monkeypatch.setattr(children, "core_argv", lambda _action: [sys.executable, "-c", _HANG, str(pidfile), child])

    async def run_one():
        manager = actions.ActionManager(emit=lambda *_a: None, changed=lambda: None, holder=lambda: None)
        action_id = manager.run({"action": "logout", "params": {}, "client_request_id": "a"}, {})["action_id"]
        record = manager.records[action_id]
        while record.state != "done":
            await asyncio.sleep(0.05)
        return record, manager.busy_holder()

    record, holder = asyncio.run(asyncio.wait_for(run_one(), 30.0))
    status = record.public()
    assert (status["done"]["ok"], status["done"]["exit_code"], holder) == (False, 143, None)
    assert status["error"]["message"] == "the action ran past 1 s and was stopped (SIGTERM)"
    assert not pid_running(int(pidfile.read_text()))


def test_a_child_an_earlier_service_left_running_gets_the_time_limit_too(tmp_path, monkeypatch):
    """A service stopped under its action leaves the child running; the next
    one watches it to the end and holds the slot meanwhile. Past the same
    limit, counted from the action's acceptance, that child is stopped too."""
    import asyncio

    from probe.service import paths, procid

    actions = _in_process_actions(tmp_path, monkeypatch)
    child = subprocess.Popen([sys.executable, "-c", _HANG, str(tmp_path / "child.pid"), "hangs"],
                             start_new_session=True)
    action_id = "act_" + "0" * 16
    try:
        paths.private_dir(paths.actions_dir())
        lines = [
            {"type": "accepted", "v": 1, "action_id": action_id, "action": "logout", "params": {},
             "client_request_id": "a", "accepted_at": time.time() - 5, "service_pid": 1},
            {"type": "child", "pid": child.pid, "start_time": procid.start_time(child.pid), "at": time.time() - 5},
        ]
        (paths.actions_dir() / f"{action_id}.jsonl").write_text("".join(json.dumps(line) + "\n" for line in lines))

        async def recover():
            manager = actions.ActionManager(emit=lambda *_a: None, changed=lambda: None, holder=lambda: None)
            manager.load(lambda *_a: None)  # the service's pid watcher: this test waits itself
            record = manager.records[action_id]
            assert record.orphan and manager.busy_holder() is not None
            while record.state != "done":
                await asyncio.sleep(0.05)
            return record.public(), manager.busy_holder()

        status, holder = asyncio.run(asyncio.wait_for(recover(), 30.0))
        assert child.wait(timeout=10) is not None
    finally:
        child.kill()
        child.wait(timeout=10)
    assert (status["error"]["message"], holder) == ("the action ran past 1 s and was stopped", None)


def test_cancel_is_refused_while_writing_and_interrupts_an_approval_wait(service_home, core):
    writing, approved = service_home.home / "written", service_home.home / "approved"
    core.plan("configure", steps=[{"event": STEP}, {"wait": str(writing)}, {"event": PROMPT, "interruptible": True},
                                  {"wait": str(approved), "interruptible": True}])
    service_home.start()
    with service_home.connect() as conn:
        action_id = _run(conn)["action_id"]
        wait_for(lambda: len(conn.call(Method.ACTION_EVENTS, {"action_id": action_id, "since": 0})["events"]) == 1, 5.0)
        with pytest.raises(client.ServiceError) as raised:
            conn.call(Method.ACTION_CANCEL, {"action_id": action_id})
        assert raised.value.code == ErrorCode.REFUSED and raised.value.data == {"reason": "writing"}
        writing.touch()
        wait_for(lambda: conn.call(Method.ACTION_EVENTS, {"action_id": action_id, "since": 1})["events"], 5.0)
        assert conn.call(Method.ACTION_CANCEL, {"action_id": action_id}) == {}
        status = _wait_done(conn, action_id)
        with pytest.raises(client.ServiceError) as again:
            conn.call(Method.ACTION_CANCEL, {"action_id": action_id})
    assert status["done"]["exit_code"] == 130 and status["error"]["code"] == "interrupted"
    assert status["cancelled"] is True
    assert again.value.data == {"reason": "finished"}


def test_an_action_whose_acceptance_cannot_be_journaled_never_runs(service_home, monkeypatch):
    """`{action_id}` promises an outcome a restart can still answer (X5): an
    `accepted` line that did not reach the disk refuses the action instead."""
    import errno

    from probe.service import actions

    manager = actions.ActionManager(emit=lambda *_: None, changed=lambda: None, holder=lambda: None)

    class FullDisk:  # `os` for the actions module alone, whose writes fail
        def __getattr__(self, name):
            return getattr(os, name)

        @staticmethod
        def write(fd, data):
            raise OSError(errno.ENOSPC, "No space left on device")

    monkeypatch.setattr(actions, "os", FullDisk())
    with pytest.raises(actions.RpcError) as raised:
        manager.run({"action": "logout", "params": {}, "client_request_id": "c"}, {})
    assert raised.value.data == {"reason": "internal"}
    assert manager.running is None and manager.records == {}
    assert list(paths.actions_dir().glob("*.jsonl")) == []


def test_the_journal_answers_after_a_restart(service_home, core):
    core.plan("uninstall", steps=[{"event": STEP}])
    first = service_home.start()
    with service_home.connect() as conn:
        action_id = _run(conn, "uninstall", {}, crid="keep")["action_id"]
        before = _wait_done(conn, action_id)
        events = conn.call(Method.ACTION_EVENTS, {"action_id": action_id, "since": 0})
        conn.call(Method.STOP)
    assert service_home.wait_exit(first["pid"], 5.0)
    second = service_home.start()
    assert second["pid"] != first["pid"]
    with service_home.connect() as conn:
        assert conn.call(Method.ACTION_STATUS, {"action_id": action_id}) == before
        assert conn.call(Method.ACTION_EVENTS, {"action_id": action_id, "since": 0}) == events
        assert _run(conn, "uninstall", {}, crid="keep") == {"action_id": action_id, "existing": True}
    assert len(core.calls("uninstall")) == 1


def test_an_action_lost_with_the_service_reads_as_stopped(service_home, core):
    gate = service_home.home / "never"
    core.plan("configure", steps=[{"event": STEP}, {"wait": str(gate)}])
    first = service_home.start()
    with service_home.connect() as conn:
        action_id = _run(conn)["action_id"]
        wait_for(lambda: conn.call(Method.ACTION_EVENTS, {"action_id": action_id, "since": 0})["events"], 5.0)
    (call,) = core.calls("configure")
    os.kill(first["pid"], signal.SIGKILL)
    os.kill(call["pid"], signal.SIGKILL)
    assert service_home.wait_exit(first["pid"], 5.0) and service_home.wait_exit(call["pid"], 5.0)
    service_home.start()
    with service_home.connect() as conn:
        status = conn.call(Method.ACTION_STATUS, {"action_id": action_id})
        events = conn.call(Method.ACTION_EVENTS, {"action_id": action_id, "since": 0})
        assert conn.call(Method.STATUS)["actions"]["running"] is None
    assert status["state"] == "done"
    assert status["done"] == {"v": 1, "event": "done", "ok": False, "complete": False, "exit_code": None, "steps": []}
    assert status["error"] == {"v": 1, "event": "error", "code": "interrupted", "message": "service stopped"}
    assert [e["event"]["event"] for e in events["events"]] == ["step", "error", "done"]


def test_a_child_that_outlived_its_service_still_holds_the_slot(service_home, core):
    gate = service_home.home / "finish"
    core.plan("configure", steps=[{"wait": str(gate)}])
    first = service_home.start()
    with service_home.connect() as conn:
        action_id = _run(conn)["action_id"]
        wait_for(lambda: conn.call(Method.ACTION_STATUS, {"action_id": action_id})["state"] == "running", 5.0)
    # `running` is journaled as the child starts, before it is far enough along to log.
    assert wait_for(lambda: core.calls("configure"), 5.0)
    os.kill(first["pid"], signal.SIGKILL)
    assert service_home.wait_exit(first["pid"], 5.0)
    (call,) = core.calls("configure")
    assert pid_running(call["pid"])
    service_home.start()
    with service_home.connect() as conn:
        assert conn.call(Method.ACTION_STATUS, {"action_id": action_id})["state"] == "running"
        with pytest.raises(client.ServiceError) as raised:
            _run(conn, crid="other")
        assert raised.value.code == ErrorCode.BUSY
        gate.touch()  # the child goes on, finds its stdout gone, and exits
        status = _wait_done(conn, action_id)
    assert status["done"]["ok"] is False and status["error"]["message"] == "service stopped"


def test_a_service_stopped_by_a_signal_leaves_its_action_running(service_home, core):
    """A clean stop (SIGTERM, or a restart for a new CLI) must not kill a
    running action: from Python 3.13 an asyncio subprocess transport SIGKILLs
    its still-running child as the service's objects are freed (the CLI's uv
    tool env runs 3.14). The next service finds the child and waits for it."""
    gate = service_home.home / "finish"
    core.plan("configure", steps=[{"wait": str(gate)}])
    first = service_home.start()
    with service_home.connect() as conn:
        action_id = _run(conn)["action_id"]
        wait_for(lambda: conn.call(Method.ACTION_STATUS, {"action_id": action_id})["state"] == "running", 5.0)
    assert wait_for(lambda: core.calls("configure"), 5.0)
    (call,) = core.calls("configure")
    os.kill(first["pid"], signal.SIGTERM)
    assert service_home.wait_exit(first["pid"], 5.0), service_home.log()
    time.sleep(0.5)
    try:
        assert pid_running(call["pid"]), "the service's exit killed its action child"
        service_home.start()
        with service_home.connect() as conn:
            assert conn.call(Method.ACTION_STATUS, {"action_id": action_id})["state"] == "running"
    finally:
        gate.touch()
    assert wait_for(lambda: not pid_running(call["pid"]), 10.0)


def test_the_child_gets_the_request_context_and_no_launcher_credentials(service_home, core, monkeypatch):
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_launcher_secret")
    monkeypatch.setenv("PROBE_CONFIG_PATH", "/launcher/config.json")
    core.plan("session_default", steps=[])
    app_config = _signed_in(service_home.home / "app" / "config.json", "https://probe.example.test")
    service_home.start()
    with service_home.connect() as conn:
        context = {"PROBE_CONFIG_PATH": str(app_config), "CLAUDE_CONFIG_DIR": "/app/claude"}
        action_id = _run(conn, "session_default", {"state": "off"}, context=context,
                         base_url="https://probe.example.test")["action_id"]
        _wait_done(conn, action_id)
        with pytest.raises(client.ServiceError) as raised:
            _run(conn, "session_default", {"state": "off"}, crid="r2", context={"PROBE_TOKEN": "x"})
        assert raised.value.code == ErrorCode.INVALID_PARAMS
    (call,) = core.calls("session_default")
    assert call["env"]["PROBE_CONFIG_PATH"] == str(app_config)
    assert call["env"]["CLAUDE_CONFIG_DIR"] == "/app/claude"
    assert call["env"]["PROBE_BASE_URL"] == "https://probe.example.test"
    assert call["env"]["PROBE_TOKEN"] is None
    journal = (paths.actions_dir() / f"{action_id}.jsonl").read_text()
    assert "/app/claude" not in journal  # a context value can carry a password: never journaled


def test_an_update_action_is_a_person_s_unless_it_says_otherwise(service_home, core):
    core.plan("update", steps=[])
    service_home.start()
    with service_home.connect() as conn:
        _wait_done(conn, _run(conn, "update", {}, crid="u")["action_id"])
        _wait_done(conn, _run(conn, "update", {}, crid="u2", trigger="session_start")["action_id"])
        with pytest.raises(client.ServiceError) as raised:
            _run(conn, "logout", {}, crid="u3", trigger="manual")
        assert raised.value.code == ErrorCode.INVALID_PARAMS
    assert [c["env"]["PROBE_AUTOUPDATE_TRIGGER"] for c in core.calls("update")] == ["manual", "session_start"]


def test_only_explicit_desktop_actions_pass_human_provenance_and_privacy_context(service_home, core):
    core.plan("update", steps=[])
    _signed_in(service_home.home / ".config" / "probe" / "config.json", "https://private.example")
    service_home.start()
    with service_home.connect() as conn:
        _wait_done(conn, _run(conn, "update", {}, crid="desktop", origin="desktop",
            context={"PROBE_TELEMETRY":"off","PROBE_BASE_URL":"https://private.example"})["action_id"])
        _wait_done(conn, _run(conn, "update", {}, crid="robot", trigger="session_start")["action_id"])
        with pytest.raises(client.ServiceError) as error:
            _run(conn, "update", {}, crid="bad-origin", origin="anything")
        assert error.value.code == ErrorCode.INVALID_PARAMS
    desktop, robot = core.calls("update")
    assert desktop["env"]["PROBE_DESKTOP_HUMAN"] == "1"
    assert desktop["env"]["PROBE_TELEMETRY"] == "off"
    assert desktop["env"]["PROBE_BASE_URL"] == "https://private.example"
    assert robot["env"]["PROBE_DESKTOP_HUMAN"] == "0"


def _signed_in(path: Path, *base_urls: str) -> Path:
    """A CLI config (v2) whose contexts name `base_urls`."""
    path.parent.mkdir(parents=True, exist_ok=True)
    contexts = {f"c{i}": {"base_url": url, "token": "probe_pat_x"} for i, url in enumerate(base_urls)}
    path.write_text(json.dumps({"version": 2, "current_context": "c0", "contexts": contexts}))
    return path


@pytest.mark.parametrize(
    ("where", "url", "allowed"),
    [
        ("base_url", "https://self.example/", True),  # the current context's, a trailing slash aside
        ("context", "https://self.example", True),
        ("base_url", "https://other.example", False),  # another context's: its token is not the one sent
        ("base_url", "https://api.research.prbe.ai", False),  # the hosted API, while signed in elsewhere
        ("base_url", "https://elsewhere.example", False),  # https, but never signed in to
        ("context", "https://elsewhere.example", False),
        ("base_url", "http://self.example", False),  # never plain http
        ("context", "http://self.example", False),
    ],
)
def test_a_child_runs_only_with_an_endpoint_the_config_knows(service_home, core, where, url, allowed):
    """The current context's stored token follows PROBE_BASE_URL (plan D10)."""
    core.plan("logout", steps=[])
    _signed_in(service_home.home / ".config" / "probe" / "config.json", "https://self.example", "https://other.example")
    service_home.start()
    extra = {"base_url": url} if where == "base_url" else {"context": {"PROBE_BASE_URL": url}}
    with service_home.connect() as conn:
        if allowed:
            _wait_done(conn, _run(conn, "logout", {}, **extra)["action_id"])
        else:
            with pytest.raises(client.ServiceError) as raised:
                _run(conn, "logout", {}, **extra)
            assert raised.value.code == ErrorCode.INVALID_PARAMS
    assert len(core.calls("logout")) == (1 if allowed else 0)


def test_the_hosted_api_is_known_without_a_config(service_home, core):
    core.plan("logout", steps=[])
    service_home.start()
    with service_home.connect() as conn:
        _wait_done(conn, _run(conn, "logout", {}, base_url="https://api.research.prbe.ai")["action_id"])
    assert len(core.calls("logout")) == 1


def test_a_retry_while_the_action_runs_gets_the_same_action(service_home, core):
    """A client that lost its connection asks again while its action runs: the
    same action, not `busy` for its own work (the dedupe comes first)."""
    gate = service_home.home / "release"
    core.plan("logout", steps=[{"wait": str(gate)}])
    service_home.start()
    with service_home.connect() as conn:
        first = _run(conn, "logout", {}, crid="same")["action_id"]
        assert wait_for(lambda: core.calls("logout"), 5.0)
        again = _run(conn, "logout", {}, crid="same")
        gate.touch()
        _wait_done(conn, first)
    assert again == {"action_id": first, "existing": True}
    assert len(core.calls("logout")) == 1


def test_an_exit_130_without_a_cancel_is_not_a_cancel(service_home, core):
    core.plan("logout", steps=[{"exit": 130}])
    service_home.start()
    with service_home.connect() as conn:
        status = _wait_done(conn, _run(conn, "logout", {}, crid="a")["action_id"])
    assert status["done"]["exit_code"] == 130 and status["cancelled"] is False


def test_a_cancel_that_misses_the_approval_wait_is_not_a_cancel(service_home, core):
    """The child ignores SIGINT outside its approval wait (`probe.core.events`):
    a cancel sent as the wait ends must not read as cancelled."""
    approved = service_home.home / "approved"
    core.plan("configure", steps=[{"event": PROMPT}, {"wait": str(approved)}])  # not interruptible
    service_home.start()
    with service_home.connect() as conn:
        action_id = _run(conn)["action_id"]
        wait_for(lambda: conn.call(Method.ACTION_EVENTS, {"action_id": action_id, "since": 0})["events"], 5.0)
        assert conn.call(Method.ACTION_CANCEL, {"action_id": action_id}) == {}
        approved.touch()
        status = _wait_done(conn, action_id)
    assert status["done"]["ok"] is True and status["cancelled"] is False


def test_an_action_in_progress_keeps_the_service_alive(service_home, core, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "1")
    gate = service_home.home / "release"
    core.plan("logout", steps=[{"wait": str(gate)}])
    status = service_home.start()
    with service_home.connect() as conn:
        _run(conn, "logout", {})
        with pytest.raises(client.ServiceError) as refused:
            conn.call(Method.STOP)
        assert refused.value.data == {"reason": "action_running"}
    time.sleep(2.0)  # twice the grace, with no session and no app window
    assert pid_running(status["pid"])
    gate.touch()
    assert service_home.wait_exit(status["pid"], 5.0), service_home.log()
    assert "stopping (idle)" in service_home.log()


@pytest.mark.parametrize(
    "params",
    [
        {"action": "status", "params": {}, "client_request_id": "x"},  # a read, not an action
        {"action": "nope", "params": {}, "client_request_id": "x"},
        {"action": "configure", "params": {"agents": []}, "client_request_id": "x"},
        {"action": "configure", "params": {"agents": ["claude"], "capture": "no"}, "client_request_id": "x"},
        {"action": "logout", "params": {"extra": 1}, "client_request_id": "x"},
        {"action": "logout", "params": {}},  # no client_request_id
        {"action": "logout", "params": {}, "client_request_id": "x", "base_url": "ftp://x"},
    ],
)
def test_run_checks_its_request(service_home, core, params):
    service_home.start()
    with service_home.connect() as conn:
        with pytest.raises(client.ServiceError) as raised:
            conn.call(Method.ACTION_RUN, params)
    assert raised.value.code == ErrorCode.INVALID_PARAMS
    assert core.calls() == []


def test_unknown_actions_are_not_found(service_home, core):
    service_home.start()
    with service_home.connect() as conn:
        for method in (Method.ACTION_STATUS, Method.ACTION_EVENTS, Method.ACTION_CANCEL):
            with pytest.raises(client.ServiceError) as raised:
                conn.call(method, {"action_id": "act_0123456789abcdef", "since": 0})
            assert raised.value.code == ErrorCode.NOT_FOUND
        with pytest.raises(client.ServiceError) as bad:
            conn.call(Method.ACTION_STATUS, {"action_id": "../../etc/passwd"})
        assert bad.value.code == ErrorCode.INVALID_PARAMS


def test_recovering_an_action_at_start_does_not_end_discovery_early(service_home, core, monkeypatch):
    """An unfinished journal is closed while the service starts; that must not
    start the idle grace before the discovery window (X6) is even set."""
    monkeypatch.setenv("PROBE_SERVICE_DISCOVERY_S", "3")
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "0.5")
    paths.private_dir(paths.actions_dir())
    action_id = "act_00000000000000aa"
    accepted = {"type": "accepted", "v": 1, "action_id": action_id, "action": "logout", "params": {},
                "client_request_id": "old", "accepted_at": time.time() - 60, "service_pid": 1}
    (paths.actions_dir() / f"{action_id}.jsonl").write_text(json.dumps(accepted) + "\n")
    status = service_home.start()
    time.sleep(1.5)  # three graces, half the discovery window
    assert pid_running(status["pid"]), service_home.log()
    with service_home.connect() as conn:
        assert conn.call(Method.ACTION_STATUS, {"action_id": action_id})["error"]["message"] == "service stopped"


def test_the_context_names_every_harness_s_session_and_home_variables():
    """A request from inside an agent's session must be able to say so (its
    session-id variable, read from the registry), and a client with its own
    agent homes must reach them: every harness's `session_env` and `home.env`."""
    from probe.harness import get_registry
    from probe.service.protocol import CONTEXT_ENV
    from probe.service.server import session_env_names

    sessions = {h.session_env for h in get_registry().all() if h.session_env}
    registry = json.loads((Path(__file__).resolve().parent.parent / "src" / "probe" / "harness" / "harnesses.json").read_text())
    homes = {h["home"]["env"] for h in registry["harnesses"] if isinstance(h.get("home"), dict) and h["home"].get("env")}
    assert sessions and sessions == session_env_names()
    assert homes and homes <= CONTEXT_ENV, sorted(homes - CONTEXT_ENV)


def test_an_agent_s_session_reaches_the_child_and_its_refusal_holds(service_home, monkeypatch):
    """Real `probe.core.run` children: inside a session the Probe daemon records,
    `session_default` is refused (exit 2) when the request names the session,
    exactly as `probe session default` is; the service does not route around it."""
    from probe.sdk import session_marker

    session = "0b6f2c1e-5a8d-4d9e-9f3a-2c7b1e4d6a90"
    monkeypatch.setenv("XDG_STATE_HOME", str(service_home.home / ".local" / "state"))
    session_marker.mark_session_profile(session, session_marker.RECORDER_DAEMON)
    monkeypatch.delenv("XDG_STATE_HOME")
    service_home.start()
    with service_home.connect() as conn:
        conn.sock.settimeout(60)
        refused = _wait_done(conn, _run(conn, "session_default", {"state": "off"}, crid="in-session",
                                        context={"CLAUDE_CODE_SESSION_ID": session})["action_id"], 60.0)
        applied = _wait_done(conn, _run(conn, "session_default", {"state": "off"}, crid="app")["action_id"], 60.0)
    assert refused["done"]["exit_code"] == 2 and refused["done"]["ok"] is False
    assert applied["done"]["exit_code"] == 0, applied


# -- who is calling (plan D9) ---------------------------------------------------


def _register_me(conn, sid: str, mode: str) -> None:
    """Register a session whose agent is THIS process: every connection this
    test opens comes from inside it."""
    owner = client.owner_of(os.getpid())
    assert owner, "cannot read this process's start time"
    conn.call(
        Method.SESSION_REGISTER,
        {"sid": sid, "harness": "claude_code", "mode": mode, "owner": owner, "generation": 1},
    )


def test_an_action_from_inside_a_daemon_recorded_session_is_refused(service_home, core, monkeypatch):
    """The caller names no session (no context): its process ancestry does."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    core.plan("recorder", steps=[])
    service_home.start()
    with service_home.connect() as conn:
        _register_me(conn, "s-recorded", "daemon")
        with pytest.raises(client.ServiceError) as raised:
            _run(conn, "recorder", {"who_records": "agent"})
    assert raised.value.code == ErrorCode.REFUSED
    assert raised.value.data["reason"] == "daemon_session"
    assert core.calls("recorder") == []
    assert not list(paths.actions_dir().glob("*.jsonl")) if paths.actions_dir().exists() else True


def test_an_action_from_inside_an_inline_session_names_it_to_the_child(service_home, core, monkeypatch):
    """Not refused here, but the child learns the session it runs inside, so
    `probe.core.run` refuses what it refuses there (`probe session default`)."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    core.plan("session_default", steps=[])
    service_home.start()
    with service_home.connect() as conn:
        _register_me(conn, "s-inline", "inline")
        _wait_done(conn, _run(conn, "session_default", {"state": "off"})["action_id"])
    (call,) = core.calls("session_default")
    assert call["env"]["CLAUDE_CODE_SESSION_ID"] == "s-inline"


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="a peer's environment is read on Linux only")
def test_a_detached_job_that_kept_the_session_s_environment_is_refused(service_home, core):
    """nohup/setsid/tmux leave the agent's process tree, not its environment."""
    import subprocess

    core.plan("logout", steps=[])
    service_home.start()
    agent = subprocess.Popen(["sleep", "60"])
    try:
        owner = wait_for(lambda: client.owner_of(agent.pid), 2.0)
        with service_home.connect() as conn:
            conn.call(
                Method.SESSION_REGISTER,
                {"sid": "s-away", "harness": "claude_code", "mode": "daemon", "owner": owner, "generation": 1},
            )
        script = (
            "import json, sys\n"
            "from probe.service import client\n"
            "from probe.service.protocol import Client, Method\n"
            "conn = client.Connection.open()\n"
            "conn.hello(Client.CLI, '0')\n"
            "try:\n"
            "    conn.call(Method.ACTION_RUN, {'action': 'logout', 'params': {}, 'client_request_id': 'away'})\n"
            "    print('ran')\n"
            "except client.ServiceError as exc:\n"
            "    print(json.dumps(exc.data))\n"
        )
        env = {**os.environ, "CLAUDE_CODE_SESSION_ID": "s-away"}
        done = subprocess.run(
            [sys.executable, "-c", script], env=env, capture_output=True, text=True, timeout=30, start_new_session=True
        )
        assert done.returncode == 0, done.stderr
        assert json.loads(done.stdout)["reason"] == "daemon_session"
        assert core.calls("logout") == []
    finally:
        agent.kill()
        agent.wait(timeout=5)


def test_an_action_child_gets_the_login_shell_s_path(service_home, core, monkeypatch):
    """An agent installed with nvm or volta is on the login PATH only (D14)."""
    shell = service_home.home / "bin" / "fake-login-shell"
    shell.parent.mkdir(parents=True, exist_ok=True)
    shell.write_text('#!/bin/sh\nexport PATH=/opt/volta/bin:$PATH\nexport HTTPS_PROXY=http://p.example\nexec /bin/sh -c "$2"\n')
    shell.chmod(0o755)
    monkeypatch.setenv("SHELL", str(shell))
    core.plan("logout", steps=[])
    service_home.start()
    with service_home.connect() as conn:
        _wait_done(conn, _run(conn, "logout", {})["action_id"])
    (call,) = core.calls("logout")
    assert call["env"]["PATH"].split(":")[0] == "/opt/volta/bin"
    assert call["env"]["HTTPS_PROXY"] is None  # an action's settings are its request's context


@pytest.mark.parametrize("special", ["/dev/zero", "fifo"])
def test_a_config_path_that_is_not_a_file_never_hangs_the_service(service_home, core, tmp_path, special):
    """A request names the config the endpoint check reads (`context.PROBE_CONFIG_PATH`)."""
    if special == "fifo":
        special = str(tmp_path / "config.fifo")
        os.mkfifo(special)
    core.plan("logout", steps=[])
    service_home.start()
    with service_home.connect() as conn:
        started = time.monotonic()
        with pytest.raises(client.ServiceError) as raised:
            _run(conn, "logout", {}, context={"PROBE_CONFIG_PATH": special}, base_url="https://self.example")
        assert time.monotonic() - started < 2.0
        assert raised.value.code == ErrorCode.INVALID_PARAMS
        assert conn.call(Method.STATUS)["pid"]  # still serving


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="the kernel names a socket's opener on Linux and macOS; the test forks")
def test_a_connection_whose_opener_exited_changes_nothing(service_home, core):
    """A process connects, hands the connection to a child (which keeps the
    session's environment) and exits: who calls can no longer be checked."""
    core.plan("logout", steps=[])
    service_home.start()
    script = (
        "import json, os, sys, time\n"
        "from probe.service import client\n"
        "from probe.service.protocol import Client, Method\n"
        "conn = client.Connection.open()\n"
        "conn.hello(Client.CLI, '0')\n"
        "if os.fork():\n"
        "    os._exit(0)\n"
        "time.sleep(0.5)\n"
        "try:\n"
        "    conn.call(Method.ACTION_RUN, {'action': 'logout', 'params': {}, 'client_request_id': 'orphan'})\n"
        "    print('ran')\n"
        "except client.ServiceError as exc:\n"
        "    print(json.dumps(exc.data))\n"
        "sys.stdout.flush()\n"
    )
    out = tempfile.NamedTemporaryFile("w+", delete=False)
    import subprocess

    subprocess.run([sys.executable, "-c", script], stdout=out, timeout=30)
    assert wait_for(lambda: Path(out.name).read_text().strip(), 10.0)
    assert json.loads(Path(out.name).read_text())["reason"] == "caller_gone"
    assert core.calls("logout") == []
