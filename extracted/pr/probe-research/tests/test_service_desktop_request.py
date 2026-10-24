"""The desktop app's management requests through the Probe service (plan Q6).

    desktop.request   `probe desktop request --json`'s request in, its v1
                      envelope out, answered by a `probe.core.run desktop`
                      child: the same code (`probe.cli.desktop.respond`), so
                      the app switches by changing transport only
    session.list      each session's delivery receipts (D29) from the
                      recorder's journal, and the same per agent
    socket            where the service listens, without the machine key

Real service processes in a throwaway HOME (`service_harness`); `FakeCore`
plays the child where the test is about the service around it, and the real
`probe.core.run desktop` answers where parity is the point. The deadlines,
the turn limits and the oversized answers are `Management`'s own, tested in
process against real child processes.
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import time

import pytest

from probe.service import children, client, management, paths, receipts
from probe.service.protocol import ErrorCode, Method, Mode, RefusedReason, RpcError
from probe.tap_core.session_journal import Journal
from tests.service_fakes import FakeCore
from tests.service_harness import service_home, wait_for  # noqa: F401 -- a fixture
from tests.test_transcript_protocol3 import CUSTOMER, DoorWire, _drain, _session, _start, _user

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the service is POSIX-only (plan S8)")

ENVELOPE = {"v": 1, "ok": True, "data": {"jobs": [], "total": 0}}


@pytest.fixture
def core(service_home):
    return FakeCore(service_home.home)


def _ask(conn, request: dict, **params) -> dict:
    return conn.call(Method.DESKTOP_REQUEST, {"request": request, **params})


# -- desktop.request ----------------------------------------------------------------


def test_the_answer_is_the_cli_envelope_and_the_child_reads_the_request(service_home, core):
    core.plan("desktop", stdout=ENVELOPE)
    service_home.start()
    request = {"op": "jobs", "cursor": "abc"}
    with service_home.connect(who="app") as conn:
        assert _ask(conn, request, context={"CLAUDE_CONFIG_DIR": "/elsewhere"}) == ENVELOPE
        assert _ask(conn, {"op": "resume_job", "id": "j-1"}, origin="desktop") == ENVELOPE
    read, change = core.calls("desktop")
    assert json.loads(read["stdin"]) == request and read["flags"] == ["-I"]
    assert read["env"]["CLAUDE_CONFIG_DIR"] == "/elsewhere"
    # The child reports `os.getcwd()`, the real path: /tmp is /private/tmp on macOS.
    assert read["cwd"] == os.path.realpath(service_home.home)
    # Only an explicit `origin: desktop` says a person asked (the CLI's telemetry).
    assert (read["env"]["PROBE_DESKTOP_HUMAN"], change["env"]["PROBE_DESKTOP_HUMAN"]) == ("0", "1")
    # An op that runs the agents' CLIs (a backfill worker) gets the login
    # shell's PATH, merged as an action child's is (D14); a read needs none.
    login_bin = str(service_home.home / ".local" / "bin")
    assert login_bin in change["env"]["PATH"].split(":")
    assert login_bin not in (read["env"]["PATH"] or "").split(":")


def test_a_refusal_from_the_cli_is_its_envelope_unchanged(service_home, core):
    refused = {"v": 1, "ok": False, "error": "Unknown desktop operation."}
    core.plan("desktop", stdout=refused, exit=1)
    service_home.start()
    with service_home.connect(who="app") as conn:
        assert _ask(conn, {"op": "shell"}) == refused


def test_an_ok_envelope_from_a_child_that_failed_reads_as_not_completed(service_home, core):
    """The app's own rule (`wizard.rs`: exit != 0 with an ok answer)."""
    core.plan("desktop", stdout=ENVELOPE, exit=3)
    service_home.start()
    with service_home.connect(who="app") as conn:
        assert _ask(conn, {"op": "jobs"}) == {"v": 1, "ok": False, "error": management.NOT_COMPLETED}


def test_a_child_with_no_envelope_is_refused_so_the_app_can_ask_the_cli(service_home, core):
    core.plan("desktop", stdout={"not": "an envelope"}, exit=1)
    service_home.start()
    with service_home.connect(who="app") as conn:
        with pytest.raises(client.ServiceError) as raised:
            _ask(conn, {"op": "jobs"})
    assert raised.value.code == ErrorCode.REFUSED
    assert raised.value.data == {"reason": RefusedReason.NO_ANSWER, "exit_code": 1}


@pytest.mark.parametrize("params", [
    {}, {"request": "jobs"}, {"request": {}}, {"request": {"op": 7}}, {"request": {"op": "x" * 65}},
    {"request": {"op": "jobs"}, "origin": "terminal"},
    {"request": {"op": "jobs"}, "context": {"PROBE_TOKEN": "secret"}},
])
def test_a_request_that_is_not_one_is_invalid_params_and_runs_nothing(service_home, core, params):
    core.plan("desktop", stdout=ENVELOPE)
    service_home.start()
    with service_home.connect(who="app") as conn:
        with pytest.raises(client.ServiceError) as raised:
            conn.call(Method.DESKTOP_REQUEST, params)
    assert raised.value.code == ErrorCode.INVALID_PARAMS
    assert core.calls("desktop") == []


def _register_me(conn, sid: str, mode: str) -> None:
    owner = client.owner_of(os.getpid())
    assert owner, "cannot read this process's start time"
    conn.call(Method.SESSION_REGISTER, {"sid": sid, "harness": "claude_code", "mode": mode, "owner": owner,
                                        "generation": 1})


@pytest.mark.parametrize("request_", [{"op": "start_backfill", "previewId": "0" * 32}, {"op": "jobs"}],
                         ids=["change", "read"])
def test_nothing_is_asked_from_inside_a_daemon_recorded_session(service_home, core, monkeypatch, request_):
    """As `action.run` (D9), and as the CLI, which refuses `probe desktop` in
    such a session: an agent's own shell neither approves a backfill nor
    reads around `probe ask`. An inline session's shell may."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    core.plan("desktop", stdout=ENVELOPE)
    service_home.start()
    with service_home.connect() as conn:
        _register_me(conn, "s-recorded", Mode.DAEMON)
        with pytest.raises(client.ServiceError) as raised:
            _ask(conn, request_)
        assert raised.value.code == ErrorCode.REFUSED
        assert raised.value.data == {"reason": RefusedReason.DAEMON_SESSION, "sid": "s-recorded"}
        assert core.calls("desktop") == []
        conn.call(Method.SESSION_END, {"sid": "s-recorded", "generation": 1})
        _register_me(conn, "s-inline", Mode.INLINE)
        assert _ask(conn, request_) == ENVELOPE


AGENT_SESSION = "0b6f2c1e-5a8d-4d9e-9f3a-2c7b1e4d6a90"


def _daemon_session(service_home, monkeypatch) -> None:
    """What the lean plugin leaves for a session the daemon records: its
    profile and its state, where the service's child looks (the default state
    folder under this HOME). No registration with the service at all."""
    from probe.sdk import session_marker

    monkeypatch.setenv("XDG_STATE_HOME", str(service_home.home / ".local" / "state"))
    session_marker.mark_session_profile(AGENT_SESSION, session_marker.RECORDER_DAEMON)
    session_marker.set_session_state(AGENT_SESSION, session_marker.STATE_DAEMON)
    monkeypatch.delenv("XDG_STATE_HOME")
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)


def _cli_refusal(service_home) -> str:
    """What `probe desktop request --json` says in that session: its own gate."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("XDG_")}
    done = subprocess.run(
        [sys.executable, "-m", "probe.cli", "desktop", "request", "--json"], input='{"op": "jobs"}',
        capture_output=True, text=True, timeout=60,
        env={**env, "HOME": str(service_home.home), "CLAUDE_CODE_SESSION_ID": AGENT_SESSION},
    )
    assert done.returncode == 3 and "probe desktop" in done.stderr, (done.returncode, done.stderr)
    return done.stderr.strip()


def test_a_daemon_session_the_service_never_registered_is_refused_by_the_child(service_home, monkeypatch):
    """Codex P1: the session's saved policy, not its registration, decides. Its
    id named in the context reaches the child, which refuses exactly what the
    CLI refuses there, before any account or network is touched."""
    _daemon_session(service_home, monkeypatch)
    refusal = _cli_refusal(service_home)
    service_home.start()
    with service_home.connect(who="app") as conn:
        conn.sock.settimeout(60)
        answer = _ask(conn, {"op": "onboarding_complete", "userId": "u-1", "customerId": "c-1"},
                      context={"CLAUDE_CODE_SESSION_ID": AGENT_SESSION})
    assert answer == {"v": 1, "ok": False, "error": refusal}


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="a peer's environment is read on Linux only")
def test_a_caller_whose_environment_names_an_unregistered_daemon_session_is_refused(service_home, monkeypatch):
    """No registration and no context: the caller's own environment names the
    session, and the service hands that identity to the child."""
    _daemon_session(service_home, monkeypatch)
    refusal = _cli_refusal(service_home)
    service_home.start()
    script = (
        "import json, sys\n"
        "from probe.service import client\n"
        "conn = client.Connection.open(60)\n"
        "conn.hello('app', '0')\n"
        "print(json.dumps(conn.call('desktop.request', {'request': {'op': 'jobs'}})))\n"
    )
    done = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=90,
                          env={**os.environ, "CLAUDE_CODE_SESSION_ID": AGENT_SESSION})
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout) == {"v": 1, "ok": False, "error": refusal}


PI_SESSION = "7d1c2b3a-4e5f-4a6b-8c7d-9e0f1a2b3c4d"
CLAUDE_SESSION = "11111111-2222-4333-8444-555555555555"


def _mark_daemon(service_home, monkeypatch, sid: str) -> None:
    from probe.sdk import session_marker

    monkeypatch.setenv("XDG_STATE_HOME", str(service_home.home / ".local" / "state"))
    session_marker.mark_session_profile(sid, session_marker.RECORDER_DAEMON)
    session_marker.set_session_state(sid, session_marker.STATE_DAEMON)
    monkeypatch.delenv("XDG_STATE_HOME")


def _expected_refusal(service_home, monkeypatch, env: dict) -> str:
    """The CLI's own refusal for `probe desktop request` in that environment."""
    from probe.cli import write_gate

    monkeypatch.setenv("XDG_STATE_HOME", str(service_home.home / ".local" / "state"))
    message = write_gate.refusal(["desktop", "request", "--json"], directed=False, env=env)
    monkeypatch.delenv("XDG_STATE_HOME")
    assert message and "probe desktop" in message
    return message


_ASK_FROM_ENV = (
    "import json, sys\n"
    "from probe.service import client\n"
    "conn = client.Connection.open(60)\n"
    "conn.hello('app', '0')\n"
    "print(json.dumps(conn.call('desktop.request', {'request': {'op': 'jobs'}})))\n"
)


def _caller_env(**names: str) -> dict:
    """This process's environment without any coding agent's session or marker."""
    from probe.harness import get_registry

    agent_vars = {v for h in get_registry().all() for v in (*h.detect_env, h.session_env) if v}
    return {**{k: v for k, v in os.environ.items() if k not in agent_vars}, **names}


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="a peer's environment is read on Linux only")
def test_pi_inside_claude_code_is_refused_by_pis_own_daemon_session(service_home, monkeypatch):
    """Codex P1: pi inherits CLAUDE_CODE_SESSION_ID from the Claude Code it was
    started in; its own PI_SESSION_ID (marked by PI_CODING_AGENT) is the session
    that asks, and the daemon records it. The CLI's precedence picks pi's."""
    _mark_daemon(service_home, monkeypatch, PI_SESSION)
    env = {"CLAUDE_CODE_SESSION_ID": CLAUDE_SESSION, "PI_CODING_AGENT": "true", "PI_SESSION_ID": PI_SESSION}
    refusal = _expected_refusal(service_home, monkeypatch, env)
    service_home.start()
    done = subprocess.run([sys.executable, "-c", _ASK_FROM_ENV], capture_output=True, text=True, timeout=90,
                          env=_caller_env(**env))
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout) == {"v": 1, "ok": False, "error": refusal}


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="the walk reads /proc here (ps elsewhere)")
def test_an_unregistered_kimi_caller_is_found_by_its_harness_process_marker(service_home, monkeypatch):
    """Codex P1: Kimi Code puts no session id in its shells; its hook records
    "harness process P runs session S", and the CLI recovers it by walking up to
    P. The service walks up from the CALLER (its peer), not from itself."""
    from probe.sdk import session_marker

    kimi = "2c3d4e5f-6a7b-4c8d-9e0f-1a2b3c4d5e6f"
    _mark_daemon(service_home, monkeypatch, kimi)
    monkeypatch.setenv("XDG_STATE_HOME", str(service_home.home / ".local" / "state"))
    _parent, start, _title = session_marker._proc_linux(os.getpid())  # noqa: SLF001 -- the caller's parent: us
    record = session_marker._process_record_path(os.getpid(), start)  # noqa: SLF001
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(json.dumps({"harness": "kimi_code", "session_id": kimi, "updated_at": time.time()}))
    monkeypatch.delenv("XDG_STATE_HOME")
    refusal = _expected_refusal(service_home, monkeypatch, {"PROBE_KIMI_SESSION_ID": kimi})
    service_home.start()
    done = subprocess.run([sys.executable, "-c", _ASK_FROM_ENV], capture_output=True, text=True, timeout=90,
                          env=_caller_env())
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout) == {"v": 1, "ok": False, "error": refusal}


def test_a_running_change_keeps_the_service_and_its_hold_across_a_restart(tmp_path, monkeypatch):
    """Codex P2: a change past its deadline still runs. Its service never idles
    out under it, and a replacement service (an update's restart, a crash)
    recovers its process from disk: Update stays `busy` until it exits."""
    from probe.service import server

    marker = tmp_path / "finished"
    _child_script(monkeypatch, tmp_path, f"import sys, time\nsys.stdin.read()\ntime.sleep(2.0)\n"
                                         f"open({str(marker)!r}, 'w').write('done')\n")
    monkeypatch.setattr(management, "CHANGE_S", 0.4)
    _server, first = _in_process_service(tmp_path, monkeypatch)

    async def answered_late():
        with pytest.raises(RpcError):
            await first.management.request({"op": "cancel_job", "id": "j"}, {}, human=True)
        await asyncio.sleep(0.3)  # its identity reaches the disk
        return first.holds()

    assert asyncio.run(answered_late()) is True, "a running change must keep its service alive"
    _server, second = _in_process_service(tmp_path, monkeypatch)
    calls = []
    monkeypatch.setattr(second, "reevaluate", lambda: calls.append("reevaluate"))

    async def replacement():
        watcher = server.PidWatcher(asyncio.get_running_loop())
        second.management.load(watcher.watch)
        held = (second.mutating_holder(), second.holds())
        while not marker.exists():
            await asyncio.sleep(0.05)
        for _ in range(100):
            if second.management.running == 0:
                break
            await asyncio.sleep(0.05)
        watcher.close()
        return held, second.mutating_holder()

    held, after = asyncio.run(replacement())
    assert held == ({"kind": "desktop", "changes": 1}, True)
    assert after is None and calls, "its exit is seen, and the service looks again at what holds it"


def test_session_list_reads_the_journal_the_services_own_recorder_published(tmp_path, monkeypatch):
    """No /proc/locks (macOS) and no lock probe: a session the service records
    itself is read from the journal its recorder published."""
    import threading
    from types import SimpleNamespace

    from probe.service import receipts as receipts_mod
    from probe.service.recorders import Recording
    from tests.test_service_receipts import _recorded

    monkeypatch.setenv("HOME", str(tmp_path))
    sid, _path, journal, _door, _root = _recorded(tmp_path)
    folder = journal.directory
    journal.close()  # nothing holds a lock: only the publication says where it records
    monkeypatch.setattr(receipts_mod, "journal_roots", lambda envs=(): [folder.parent])
    monkeypatch.setattr(receipts_mod, "_linux_flocks", lambda: None)
    server, service = _in_process_service(tmp_path, monkeypatch)
    service.registry.register(sid, "claude_code", Mode.INLINE, None, 1)
    alive = threading.Thread(target=threading.Event().wait, args=(5,), daemon=True)
    alive.start()
    service.recorders.recordings[sid] = Recording(sid, {"sid": sid}, SimpleNamespace(claimed=str(folder)),
                                                  thread=alive)
    listing = asyncio.run(service._list(server.Connection(None, peer_pid=os.getpid()), {}))  # noqa: SLF001
    (row,) = listing["sessions"]
    assert row["receipts"]["last_line"] == 6
    assert row["receipts"]["scope"]["customer"] == "synthetic"


def test_a_running_change_holds_off_any_action_until_its_child_exits(tmp_path, monkeypatch):
    """Codex P2: a person's Update (`action.run update`) must not replace the
    CLI's env under a management change, also one past its deadline (another
    state folder means another wizard lock: the lock alone does not cover it)."""
    marker = tmp_path / "finished"
    _child_script(monkeypatch, tmp_path, f"import sys, time\nsys.stdin.read()\ntime.sleep(1.0)\n"
                                         f"open({str(marker)!r}, 'w').write('done')\n")
    monkeypatch.setattr(management, "CHANGE_S", 0.4)
    _server, service = _in_process_service(tmp_path, monkeypatch)
    update = {"action": "update", "params": {}, "client_request_id": "after-change"}

    async def scenario():
        with pytest.raises(RpcError):  # timed out, left running
            await service.management.request({"op": "start_backfill", "previewId": "0" * 32}, {}, human=True)
        with pytest.raises(RpcError) as busy:
            service.actions.run(update, {})
        while not marker.exists():
            await asyncio.sleep(0.05)
        await asyncio.sleep(0.3)  # the exit reaches the loop
        return busy.value, service.mutating_holder()

    busy, after = asyncio.run(scenario())
    assert busy.code == ErrorCode.BUSY and busy.data["holder"] == {"kind": "desktop", "changes": 1}
    assert after is None


def test_every_cli_op_is_a_read_or_a_change_and_an_unknown_one_is_a_change():
    """`protocol.DesktopOp` is `probe desktop request`'s op list; an op added to
    the CLI and not here fails here, and meanwhile counts as a change (never
    killed mid-write)."""
    from probe.cli import desktop
    from probe.service.protocol import DESKTOP_READS, DesktopOp

    ops = {v for k, v in vars(DesktopOp).items() if k.isupper()}
    assert ops == set(desktop.FIELDS)
    assert DESKTOP_READS < ops
    assert desktop.LOCKED < ops and not desktop.LOCKED & DESKTOP_READS
    assert management.is_change("a_new_op") and management.deadline("a_new_op") == management.CHANGE_S


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="no_new_privs is Linux's")
def test_a_caller_in_a_sandbox_is_refused(service_home, core):
    """The child reads this user's credentials with the context the caller chose."""
    from tests.test_service_cli_on_service import _SANDBOXED

    core.plan("desktop", stdout=ENVELOPE)
    service_home.start()
    done = subprocess.run(
        [sys.executable, "-c", _SANDBOXED, Method.DESKTOP_REQUEST, json.dumps({"request": {"op": "jobs"}})],
        capture_output=True, text=True, timeout=30, env=os.environ.copy(),
    )
    assert json.loads(done.stdout) == {"code": -32012, "data": {"reason": "sandboxed"}}, done.stderr
    assert core.calls("desktop") == []


def test_a_request_being_answered_holds_the_service(service_home, core, monkeypatch):
    """A window-less caller (a CLI) gets its answer even past the grace."""
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "0.3")
    core.plan("desktop", stdout=ENVELOPE, before=[{"sleep": 1.5}])
    started = service_home.start()
    with service_home.connect() as conn:
        conn.sock.settimeout(30)
        assert _ask(conn, {"op": "jobs"}) == ENVELOPE
    assert service_home.status()["pid"] == started["pid"]


def test_the_real_child_answers_byte_for_byte_what_probe_desktop_request_prints(service_home):
    """No stand-in: `runtime.json` names this interpreter, so the service's
    child is the real `probe.core.run desktop`."""
    service_home.start()
    # What the app imports for its children (IMPORTED_ENV): the CLI below runs
    # with this process's environment, the service's child with its own plus this.
    context = {name: os.environ[name] for name in ("PROBE_TELEMETRY", "PROBE_CONFIG_PATH", "XDG_CONFIG_HOME",
                                                   "XDG_STATE_HOME") if name in os.environ}
    for request in ({"op": "shell"}, {"op": "jobs", "extra": 1}, {"op": "analytics_policy"}):
        with service_home.connect(who="app") as conn:
            conn.sock.settimeout(60)
            answer = _ask(conn, request, context=context)
        cli = subprocess.run(
            [sys.executable, "-m", "probe.cli", "desktop", "request", "--json"], input=json.dumps(request),
            capture_output=True, text=True, timeout=60, env={**os.environ, "PROBE_DESKTOP_HUMAN": "0"},
        )
        assert answer == json.loads(cli.stdout), cli.stderr
        assert answer["v"] == 1


# -- Management: deadlines, turns, sizes (in process, real children) -----------------


def _child_script(monkeypatch, tmp_path, code: str) -> None:
    script = tmp_path / "child.py"
    script.write_text(code)
    monkeypatch.setattr(children, "core_argv", lambda action: [sys.executable, "-I", str(script)])
    monkeypatch.setattr(management.loginenv, "child_env", _login({"PATH": os.environ.get("PATH", "")}))
    monkeypatch.setattr(management, "MIN_RUN_S", 0.1)  # the tests' deadlines are short


def _login(env: dict, calls: list | None = None):
    async def child_env(*, vars: bool) -> dict:
        if calls is not None:
            calls.append(vars)
        return dict(env)

    return child_env


def test_a_read_past_its_deadline_is_killed(monkeypatch, tmp_path):
    pidfile = tmp_path / "pid"
    _child_script(monkeypatch, tmp_path, f"import os, time\nopen({str(pidfile)!r}, 'w').write(str(os.getpid()))\n"
                                         "time.sleep(30)\n")
    monkeypatch.setattr(management, "READ_S", 0.6)
    with pytest.raises(RpcError) as raised:
        asyncio.run(management.Management().request({"op": "jobs"}, {}, human=False))
    assert raised.value.data == {"reason": RefusedReason.TIMED_OUT, "killed": True, "deadline_s": 0.6}
    pid = int(pidfile.read_text())
    assert wait_for(lambda: not _running(pid), 5.0), "the read was left running"


def test_a_change_past_its_deadline_is_left_to_finish(monkeypatch, tmp_path):
    marker = tmp_path / "finished"
    _child_script(monkeypatch, tmp_path, f"import sys, time\nsys.stdin.read()\ntime.sleep(1.0)\n"
                                         f"open({str(marker)!r}, 'w').write('done')\n"
                                         "print('{\"v\": 1, \"ok\": true, \"data\": null}')\n")
    monkeypatch.setattr(management, "CHANGE_S", 0.6)
    with pytest.raises(RpcError) as raised:
        asyncio.run(management.Management().request({"op": "cancel_job", "id": "j"}, {}, human=True))
    assert raised.value.data["reason"] == RefusedReason.TIMED_OUT and raised.value.data["killed"] is False
    assert wait_for(marker.exists, 10.0), "a change must never be stopped mid-write"


def test_requests_past_the_turn_limit_are_refused_before_anything_runs(monkeypatch, tmp_path):
    _child_script(monkeypatch, tmp_path, "import sys, time\nsys.stdin.read()\ntime.sleep(0.8)\n"
                                         "print('{\"v\": 1, \"ok\": true, \"data\": 1}')\n")
    monkeypatch.setattr(management, "MAX_RUNNING", 1)
    monkeypatch.setattr(management, "MAX_WAITING", 1)

    async def scenario():
        answers = management.Management()
        results = await asyncio.gather(
            *(answers.request({"op": "jobs"}, {}, human=False) for _ in range(3)), return_exceptions=True
        )
        return answers, results

    answers, results = asyncio.run(scenario())
    refused = [r for r in results if isinstance(r, RpcError)]
    assert [r.data["reason"] for r in refused] == [RefusedReason.TOO_MANY]
    assert [r for r in results if isinstance(r, dict)] == [{"v": 1, "ok": True, "data": 1}] * 2
    assert answers.children == 2 and answers.admitted == 0


def test_an_answer_over_one_line_sends_the_app_to_the_cli(monkeypatch, tmp_path):
    _child_script(monkeypatch, tmp_path, "import json, sys\nsys.stdin.read()\n"
                                         "print(json.dumps({'v': 1, 'ok': True, 'data': 'x' * 5000}))\n")
    monkeypatch.setattr(management, "MAX_ANSWER_BYTES", 1000)
    with pytest.raises(RpcError) as raised:
        asyncio.run(management.Management().request({"op": "discover_sessions"}, {}, human=False))
    assert raised.value.data == {"reason": RefusedReason.NO_ANSWER, "too_large": True, "exit_code": 0}


def test_an_answer_the_wire_cannot_carry_sends_the_app_to_the_cli(monkeypatch, tmp_path):
    """A lone surrogate (a file name that is not UTF-8) cannot go out as UTF-8."""
    _child_script(monkeypatch, tmp_path, "import sys\nsys.stdin.read()\n"
                                         "print('{\"v\": 1, \"ok\": true, \"data\": \"\\\\udcff\"}')\n")
    with pytest.raises(RpcError) as raised:
        asyncio.run(management.Management().request({"op": "discover_sessions"}, {}, human=False))
    assert raised.value.data == {"reason": RefusedReason.NO_ANSWER, "exit_code": 0}


def test_a_turn_that_comes_too_late_or_during_an_update_runs_nothing(monkeypatch, tmp_path):
    _child_script(monkeypatch, tmp_path, "raise SystemExit('must not run')\n")
    answers = management.Management()
    monkeypatch.setattr(management, "MIN_RUN_S", 1000.0)
    with pytest.raises(RpcError) as late:
        asyncio.run(answers.request({"op": "jobs"}, {}, human=False))
    assert late.value.data["reason"] == RefusedReason.TOO_MANY
    monkeypatch.setattr(management, "MIN_RUN_S", 0.0)

    def updating():
        raise RpcError(ErrorCode.BUSY, "busy: an update is replacing the Probe CLI")

    with pytest.raises(RpcError) as busy:
        asyncio.run(answers.request({"op": "jobs"}, {}, human=False, may_start=updating))
    assert busy.value.code == ErrorCode.BUSY
    assert (answers.children, answers.running, answers.admitted) == (0, 0, 0)


def _in_process_service(tmp_path, monkeypatch):
    from probe.service import server, updater
    from probe.service.registry import Registry

    monkeypatch.setattr(updater, "_hosted_live", updater._hosted_live)  # noqa: SLF001 -- Service sets it
    return server, server.Service(registry=Registry(tmp_path / "sessions.json"))


def test_no_child_starts_while_an_update_replaces_the_cli(tmp_path, monkeypatch):
    """The cycle applying in place, or a person's Update action (which raises
    no barrier of its own): `busy`, and nothing ran."""
    from types import SimpleNamespace

    _child_script(monkeypatch, tmp_path, "raise SystemExit('must not run')\n")
    server, service = _in_process_service(tmp_path, monkeypatch)
    conn = server.Connection(None, peer_pid=os.getpid())
    ask = {"request": {"op": "jobs"}}
    service.updater.applying = True
    with pytest.raises(RpcError) as cycle:
        asyncio.run(service._desktop_request(conn, ask))  # noqa: SLF001
    assert cycle.value.code == ErrorCode.BUSY and cycle.value.data["holder"]["kind"] == "update"
    service.updater.applying = False
    service.actions.running = SimpleNamespace(action="update", action_id="act_0123456789abcdef")
    with pytest.raises(RpcError) as button:
        asyncio.run(service._desktop_request(conn, ask))  # noqa: SLF001
    assert button.value.code == ErrorCode.BUSY
    assert button.value.data["holder"] == {"kind": "action", "action_id": "act_0123456789abcdef", "action": "update"}
    assert service.management.children == 0


def test_an_update_that_starts_while_a_request_waits_for_its_turn_stops_it(tmp_path, monkeypatch):
    _child_script(monkeypatch, tmp_path, "import sys, time\nsys.stdin.read()\ntime.sleep(0.6)\n"
                                         "print('{\"v\": 1, \"ok\": true, \"data\": 1}')\n")
    monkeypatch.setattr(management, "MAX_RUNNING", 1)
    server, service = _in_process_service(tmp_path, monkeypatch)
    conn = server.Connection(None, peer_pid=os.getpid())

    async def scenario():
        first = asyncio.ensure_future(service._desktop_request(conn, {"request": {"op": "jobs"}}))  # noqa: SLF001
        while service.management.children == 0:
            await asyncio.sleep(0.01)
        second = asyncio.ensure_future(service._desktop_request(conn, {"request": {"op": "jobs"}}))  # noqa: SLF001
        await asyncio.sleep(0.1)  # waiting for the one turn
        service.updater.applying = True
        return await asyncio.gather(first, second, return_exceptions=True)

    first, second = asyncio.run(scenario())
    assert first == {"v": 1, "ok": True, "data": 1}
    assert isinstance(second, RpcError) and second.code == ErrorCode.BUSY
    assert service.management.children == 1


def test_a_change_holds_off_the_updater_until_its_child_exits(tmp_path, monkeypatch):
    """Even past its deadline: the change goes on, and so does the hold. A read
    holds nothing (it is killable and waits out the barrier itself)."""
    marker = tmp_path / "finished"
    _child_script(monkeypatch, tmp_path, f"import sys, time\nsys.stdin.read()\ntime.sleep(1.0)\n"
                                         f"open({str(marker)!r}, 'w').write('done')\n")
    monkeypatch.setattr(management, "CHANGE_S", 0.4)
    _server, service = _in_process_service(tmp_path, monkeypatch)

    async def scenario():
        with pytest.raises(RpcError):
            await service.management.request({"op": "cancel_job", "id": "j"}, {}, human=True)
        held = service.updater.action_running()
        while not marker.exists():
            await asyncio.sleep(0.05)
        await asyncio.sleep(0.3)  # the exit reaches the loop
        return held, service.updater.action_running()

    held, after = asyncio.run(scenario())
    assert (held, after) == (True, False)


def test_no_cli_to_start_is_cli_unavailable(monkeypatch, tmp_path):
    monkeypatch.setattr(children, "core_argv", lambda action: [str(tmp_path / "no-such-python")])
    monkeypatch.setattr(management.loginenv, "child_env", _login({}))
    with pytest.raises(RpcError) as raised:
        asyncio.run(management.Management().request({"op": "jobs"}, {}, human=False))
    assert raised.value.data["reason"] == RefusedReason.CLI_UNAVAILABLE


def test_the_login_path_is_read_once_for_many_requests(monkeypatch, tmp_path):
    _child_script(monkeypatch, tmp_path, "import sys\nsys.stdin.read()\nprint('{\"v\": 1, \"ok\": true, \"data\": 0}')\n")
    calls: list = []
    monkeypatch.setattr(management.loginenv, "child_env", _login({"PATH": "/usr/bin"}, calls))

    async def scenario():
        answers = management.Management()
        await answers.request({"op": "profile"}, {}, human=False)
        assert calls == [], "a read that runs no agent CLI asks no login shell"
        for _ in range(3):
            await answers.request({"op": "resume_job", "id": "j"}, {}, human=True)

    asyncio.run(scenario())
    assert calls == [False], "PATH only, read once per LOGIN_TTL_S"


def _running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    try:
        with open(f"/proc/{pid}/stat") as handle:
            return handle.read().split()[2] != "Z"
    except OSError:
        return True


# -- session.list receipts (D29) ------------------------------------------------------


@pytest.mark.skipif(
    not receipts.PROC_LOCKS.exists(),
    reason="an inline session's journal is told from /proc/locks (Linux); elsewhere unknown by design",
)
def test_session_list_and_probe_status_carry_each_sessions_receipts(service_home):
    from probe.cli import service_calls

    door = DoorWire(offers=True)
    sid, path = _session(service_home.home, [_user("x", f"turn {i}", i) for i in range(6)])
    journal = Journal(door.base_url, CUSTOMER, door.source,
                      directory=service_home.home / ".probe" / "transcripts-v2")
    assert journal.claim_live(sid)  # its recorder runs
    _start(journal, door, sid, path)
    _drain(journal, door, sid)
    with path.open("ab") as handle:
        handle.write(json.dumps(_user(sid, "seven", 7)).encode() + b"\n")
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.SESSION_REGISTER, {"sid": sid, "harness": "claude_code", "mode": Mode.INLINE,
                                            "owner": None, "generation": 1})
        listing = conn.call(Method.SESSION_LIST)
    (row,) = listing["sessions"]
    found = row["receipts"]
    assert (found["last_line"], found["pending_lines"], found["pending_batch"]) == (6, 1, False)
    assert found["received_at"] and time.time() - found["received_at"] < 120
    (harness,) = listing["harnesses"]
    assert harness["harness"] == "claude_code"
    assert (harness["sessions"], harness["alive"], harness["pending_lines"]) == (1, 1, 1)
    assert harness["received_at"] == found["received_at"]
    view = service_calls.view(timeout=5)
    assert view["sessions"][0]["receipts"] == found
    assert view["harnesses"] == [harness]
    journal.close()


# -- where the service listens ----------------------------------------------------------


def test_socket_prints_every_place_a_client_needs(service_home, capsys):
    assert client.main(["socket"]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed == {
        "socket": str(paths.socket_path()), "legacy_socket": str(paths.legacy_socket_path()),
        "service_dir": str(paths.service_dir()), "root_dir": str(paths.root_dir()),
        "runtime": str(paths.runtime_path()), "machine_key": paths.machine_key(),
    }
    assert printed["service_dir"].endswith(printed["machine_key"])
    # The CLI's interpreter answers it with no `probe` command on PATH, and
    # starts no service by answering.
    done = subprocess.run([sys.executable, "-I", "-m", "probe.service.client", "socket"], capture_output=True,
                          text=True, timeout=30)
    assert json.loads(done.stdout) == printed
    assert service_home.service_processes() == []
