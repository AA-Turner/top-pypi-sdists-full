"""Session and mailbox calls are bound to the processes that own them (#3360, #3361).

Any process of this user reaches the Probe service's socket, the coding agent's
own shell among them, and `session.list` names every session's id and
generation. Before this, that shell could end its own session (`session.end`)
or re-register it `inline` (`session.register`), after which `action.run` no
longer found the daemon session it runs in and changed the device's settings
for it; and it could post into, or take messages from, any session's mailbox
(`mailbox.post`, `mailbox.claim`).

The kernel names the process behind every connection; that is the one fact a
request cannot forge, so it is what decides:

- a session is ended, or given another owner, only by the process that
  registered it (or the service itself); same-owner registers stay open, so the
  recorder hand-offs and older taps keep working;
- an agent process once registered in daemon mode stays refused until it exits,
  whatever later registrations say, and every match counts, so a registration
  forged beside the real one cannot hide it;
- the action child resolves the caller's own session from its process too;
- a mailbox post comes from the session's daemon worker (a child of the service,
  or one under the session's registrant), a claim from under the session's agent
  or a hook host; anyone else is refused and does the step on the files itself.

Real service processes in a throwaway HOME (`service_harness`), real stand-in
agents, and the forged calls made the way the agent's shell would make them:
from another process.
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import subprocess
import sys
import time
from dataclasses import asdict
from pathlib import Path

import pytest

from probe.daemon import mailbox
from probe.daemon.mailbox import Kind
from probe.service import client
from probe.service.caller import Bound
from probe.service.protocol import ErrorCode, Method, Mode, RpcError
from probe.service.registry import SERVICE, Outcome, Registry
from tests.service_fakes import FakeCore
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401 -- a fixture

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")

AGENT_ROOT = Path(__file__).resolve().parents[1]
READS_HOOK = AGENT_ROOT / "plugins" / "probe-research" / "hooks" / "reads_hook.py"
OLD_REGISTRY = Path(__file__).parent / "fixtures" / "old_service" / "registry_before_3360.py"
SID = "11111111-2222-3333-4444-555555555555"
OTHER = "99999999-8888-7777-6666-555555555555"


# ---------------------------------------------------------------------------
# The registry's rules, with fake processes.
# ---------------------------------------------------------------------------

A = {"pid": 4101, "start_time": "a"}
B = {"pid": 4102, "start_time": "b"}
OWNER = {"pid": 5001, "start_time": "o1"}
OWNER2 = {"pid": 5002, "start_time": "o2"}


class Procs:
    """Which fake processes run (`Registry.owner_alive`)."""

    def __init__(self, *running: dict) -> None:
        self.running = {(p["pid"], p["start_time"]) for p in running}

    def __call__(self, pid: int, start: str) -> bool:
        return (pid, start) in self.running

    def exit(self, proc: dict) -> None:
        self.running.discard((proc["pid"], proc["start_time"]))


def _registry(tmp_path, *running: dict) -> tuple[Registry, Procs]:
    procs = Procs(*running)
    reg = Registry(tmp_path / "sessions.json", owner_alive=procs)
    # Fake pids: every owner reads as a coding agent, and this service still
    # records what it registered (set as attributes: older registries ignore them).
    reg.agent_like = lambda pid, start: True
    reg.service_records = lambda sid: True
    return reg, procs


def _named_agent(tmp_path: Path, *args: str, program: str = "/bin/sleep", name: str = "claude") -> subprocess.Popen:
    """A process the kernel names `claude` (a link of that name to `program`):
    what a coding agent looks like to the service (`caller.agent_like`)."""
    folder = tmp_path / f"agent-{time.monotonic_ns()}"
    folder.mkdir()
    (folder / name).symlink_to(program)
    return subprocess.Popen([str(folder / name), *(args or ("120",))], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)


def _owner(proc: subprocess.Popen) -> dict:
    owner = wait_for(lambda: client.owner_of(proc.pid), 2.0)
    assert owner, "cannot read the stand-in agent's start time"
    return owner


def _refused(fn, *args, **kwargs) -> RpcError:
    with pytest.raises(RpcError) as raised:
        fn(*args, **kwargs)
    assert raised.value.code == ErrorCode.REFUSED
    return raised.value


def test_only_the_registrant_or_the_service_ends_a_session(tmp_path):
    reg, _ = _registry(tmp_path, A, B, OWNER)
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 1, caller=A)
    assert _refused(reg.end, SID, 1, B).data == {"reason": Bound.NOT_REGISTRANT}
    assert _refused(reg.end, SID, 9, None).data == {"reason": Bound.NOT_REGISTRANT}, "an unnamed caller proves nothing"
    assert SID in reg.sessions
    assert reg.end(SID, 1, A) is not None
    reg.register(OTHER, "claude_code", Mode.INLINE, OWNER, 1, caller=A)
    assert reg.end(OTHER, 1, SERVICE) is not None, "the service ends any (a hosted recorder's link)"


def test_a_start_time_tells_a_recycled_pid_from_the_registrant(tmp_path):
    impostor = {"pid": A["pid"], "start_time": "later"}
    reg, _ = _registry(tmp_path, A, OWNER, impostor)
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 1, caller=A)
    _refused(reg.end, SID, 1, impostor)


def test_a_session_whose_registrant_or_agent_is_gone_is_anyones(tmp_path):
    reg, procs = _registry(tmp_path, A, B, OWNER, OWNER2)
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 1, caller=A)
    _refused(reg.register, SID, "claude_code", Mode.DAEMON, OWNER2, 2, caller=B)
    procs.exit(A)  # its `tap watch` exited: the next one takes the session up
    assert reg.register(SID, "claude_code", Mode.DAEMON, OWNER2, 2, caller=B).outcome == Outcome.REPLACED
    assert reg.sessions[SID].registrant == B
    procs.exit(OWNER2)  # and an agent that exited leaves a session anyone may end
    assert reg.end(SID, 2, A) is not None


def test_another_owner_needs_the_registrant(tmp_path):
    reg, _ = _registry(tmp_path, A, B, OWNER, OWNER2)
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 1, caller=A)
    err = _refused(reg.register, SID, "claude_code", Mode.INLINE, OWNER2, 2, caller=B)
    assert err.data == {"reason": Bound.NOT_REGISTRANT}
    assert reg.sessions[SID].owner == OWNER and reg.sessions[SID].mode == Mode.DAEMON
    assert reg.register(SID, "claude_code", Mode.DAEMON, OWNER2, 3, caller=A).outcome == Outcome.REPLACED
    assert reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 4, caller=SERVICE).outcome == Outcome.REPLACED
    assert reg.sessions[SID].registrant == SERVICE


def test_same_owner_registers_stay_open_and_move_nothing_that_matters(tmp_path):
    """The hand-offs (`session.record` from a hook, a `tap watch` taking its
    session back) re-register from another process under the same owner: they
    go through, and never move the registrant, the state folder or the consent."""
    reg, _ = _registry(tmp_path, A, B, OWNER)
    reg.register(SID, "claude_code", Mode.INLINE, OWNER, 1, "/home/u/.local/state/probe", False, caller=A)
    taken = reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 2, "/tmp/elsewhere/probe", True, caller=B)
    assert taken.outcome == Outcome.REPLACED
    session = reg.sessions[SID]
    assert (session.mode, session.generation) == (Mode.DAEMON, 2), "the switch it says is the session's"
    assert session.registrant == A
    assert session.state_dir == "/home/u/.local/state/probe" and session.report_env is False
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 2, "/tmp/elsewhere/probe", True, caller=B)
    assert reg.sessions[SID].state_dir == "/home/u/.local/state/probe", "a heartbeat from it neither"
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 2, "/home/u/.local/state/probe", True, caller=A)
    assert reg.sessions[SID].report_env is True, "its registrant moves them"


def test_a_registry_that_names_no_registrant_binds_nothing(tmp_path):
    """Written by a service before this: what it lists stays as open as it was."""
    reg, _ = _registry(tmp_path, A, B, OWNER)
    reg.register(SID, "claude_code", Mode.INLINE, OWNER, 1, caller=A)
    data = json.loads(reg.path.read_text())
    for row in data["sessions"]:
        row.pop("registrant")
    data.pop("daemon_owners")
    reg.path.write_text(json.dumps(data))
    again = Registry(reg.path, owner_alive=Procs(A, B, OWNER))
    again.load()
    assert again.sessions[SID].registrant is None
    assert again.end(SID, 1, B) is not None


def test_an_agent_registered_in_daemon_mode_is_remembered_until_it_exits(tmp_path):
    reg, _ = _registry(tmp_path, A, B, OWNER)
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 1, caller=A)
    assert reg.daemon_owner(OWNER["pid"], OWNER["start_time"]) == {"sid": SID, "harness": "claude_code",
                                                                   "at": pytest.approx(time.time(), abs=60)}
    reg.register(SID, "claude_code", Mode.INLINE, OWNER, 2, caller=A)
    reg.end(SID, 2, A)
    reg.register(OTHER, "claude_code", Mode.INLINE, OWNER, 1, caller=B)
    assert reg.daemon_owner(OWNER["pid"], OWNER["start_time"])["sid"] == SID, "ended, replaced, re-registered"
    assert reg.daemon_agent_runs(SID) and not reg.daemon_agent_runs(OTHER)
    reg.forget_daemon_owner(OWNER)
    assert reg.daemon_owner(OWNER["pid"], OWNER["start_time"]) is None


def test_a_refused_daemon_register_still_names_its_agent(tmp_path):
    """The set only grows between exits: a register turned down for its
    generation or its caller still says which agent the daemon records."""
    reg, _ = _registry(tmp_path, A, B, OWNER, OWNER2)
    reg.register(SID, "claude_code", Mode.INLINE, OWNER, 5, caller=A)
    _refused(reg.register, SID, "claude_code", Mode.DAEMON, OWNER2, 9, caller=B)
    _refused(reg.register, SID, "claude_code", Mode.DAEMON, OWNER, 1, caller=B)  # stale
    assert reg.daemon_owner(OWNER2["pid"], OWNER2["start_time"]) is not None
    assert reg.daemon_owner(OWNER["pid"], OWNER["start_time"]) is not None
    reg.register(OTHER, "claude_code", Mode.DAEMON, {"pid": 5999, "start_time": "gone"}, 1, caller=A)
    assert reg.daemon_owner(5999, "gone") is None, "an agent that is not running is never remembered"


def test_the_registrant_and_the_remembered_agents_survive_a_restart(tmp_path):
    agent = _named_agent(tmp_path)
    try:
        me = _owner(agent)
        reg = Registry(tmp_path / "sessions.json")
        reg.register(SID, "claude_code", Mode.DAEMON, me, 1, caller=A)
        reg.register(OTHER, "claude_code", Mode.INLINE, me, 1)  # this service's own
        reg.end(SID, 1, A)
        again = Registry(tmp_path / "sessions.json")
        again.load()
        assert again.sessions[OTHER].registrant == SERVICE
        assert again.daemon_owner(me["pid"], me["start_time"])["sid"] == SID
    finally:
        kill_agent(agent)


def _old_registry_module():
    """`probe.service.registry` as it was before #3360 (what an older service runs)."""
    spec = importlib.util.spec_from_file_location("probe.service._registry_before_3360", OLD_REGISTRY)
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "probe.service"
    sys.modules[spec.name] = module  # its dataclasses look their module up there
    spec.loader.exec_module(module)
    return module


def test_an_older_service_reads_what_this_one_writes(tmp_path):
    """A downgrade, or an older service started on this machine: the new keys
    are ignored, the sessions are read as before."""
    me = client.owner_of(os.getpid())
    reg = Registry(tmp_path / "sessions.json")
    reg.register(SID, "claude_code", Mode.DAEMON, me, 7, "/s/probe", True, caller=A)
    old = _old_registry_module().Registry(tmp_path / "sessions.json")
    (kept,) = old.load()
    assert (kept.sid, kept.mode, kept.owner, kept.generation, kept.state_dir) == (SID, Mode.DAEMON, me, 7, "/s/probe")


def test_this_service_reads_what_an_older_one_wrote(tmp_path):
    agent = _named_agent(tmp_path)
    try:
        me = _owner(agent)
        old = _old_registry_module().Registry(tmp_path / "sessions.json")
        old.register(SID, "claude_code", Mode.DAEMON, me, 3, "/s/probe")
        reg = Registry(tmp_path / "sessions.json")
        (kept,) = reg.load()
        assert (kept.sid, kept.generation, kept.registrant) == (SID, 3, None)
        assert reg.daemon_owners == {}, "learned again at the next register (a heartbeat within 20 s)"
        reg.register(SID, "claude_code", Mode.DAEMON, me, 3, "/s/probe", caller=A)
        assert reg.daemon_owner(me["pid"], me["start_time"]) is not None
    finally:
        kill_agent(agent)


# ---------------------------------------------------------------------------
# The real service: the forged calls from another process, the real ones beside them.
# ---------------------------------------------------------------------------

#: What the agent's shell would run: the client's own command line.
def _client(*argv: str) -> dict:
    done = subprocess.run([sys.executable, "-I", "-m", "probe.service.client", *argv], capture_output=True,
                          text=True, timeout=30, env={**os.environ})
    return json.loads(done.stdout)


def _register(sh, sid: str, owner: dict, mode: str = Mode.DAEMON, generation: int = 1) -> object:
    return sh.call(Method.SESSION_REGISTER, {"sid": sid, "harness": "claude_code", "mode": mode, "owner": owner,
                                             "generation": generation})


def _listed(sh) -> dict:
    return {s["sid"]: s for s in sh.call(Method.SESSION_LIST, {"receipts": False})["sessions"]}


def test_another_process_cannot_end_or_take_over_a_session(service_home):
    """This test registers the session (its `tap watch`, say); a different
    process (the agent's shell) sends the forged calls."""
    service_home.start()
    agent, owner = spawn_agent()
    other, owner2 = spawn_agent()
    try:
        _register(service_home, SID, owner, generation=5)
        forged = _client("end", "--session-id", SID, "--generation", "5")
        assert forged["error"]["data"] == {"reason": Bound.NOT_REGISTRANT}
        forged = _client("register", "--session-id", SID, "--harness", "claude_code", "--mode", "inline",
                         "--owner-pid", str(other.pid), "--generation", "6")
        assert forged["error"]["data"] == {"reason": Bound.NOT_REGISTRANT}
        listed = _listed(service_home)[SID]
        assert (listed["mode"], listed["owner"], listed["generation"]) == (Mode.DAEMON, owner, 5)
        assert "not the process that registered it" in service_home.log()
        assert service_home.call(Method.SESSION_END, {"sid": SID, "generation": 5}) == {}, "its registrant may"
        assert SID not in _listed(service_home)
    finally:
        kill_agent(agent)
        kill_agent(other)


_ACTION_AS = r'''
import json, sys
from probe.service import client
from probe.service.protocol import Client, Method
conn = client.Connection.open()
conn.hello(Client.CLI, "0")
for method, params in json.loads(sys.argv[1]):
    try:
        conn.call(method, params)
    except client.ServiceError as exc:
        pass
try:
    answer = conn.call(Method.ACTION_RUN, {"action": "logout", "params": {}, "client_request_id": "forged"})
    print(json.dumps({"ran": answer}))
except client.ServiceError as exc:
    print(json.dumps({"refused": exc.data}))
'''


#: A stand-in coding agent's loop: each line on stdin is a job its "shell" (a
#: child of it) runs with the real interpreter; one JSON line back per job.
_AGENT_DRIVER = r'''
import json, subprocess, sys
python = sys.argv[1]
sys.stdout.write("ready\n"); sys.stdout.flush()
for line in sys.stdin:
    job = json.loads(line)
    done = subprocess.run([python, "-c", job["code"], *job["args"]], capture_output=True, text=True, env=job["env"])
    sys.stdout.write(json.dumps({"out": done.stdout, "err": done.stderr[-3000:], "rc": done.returncode}) + "\n")
    sys.stdout.flush()
'''


def _interpreter_binary() -> str:
    """The interpreter's own binary, for a link named `claude` to run as `claude`.
    A macOS framework build's `bin/python3.x` is a launcher that re-executes
    `Resources/Python.app/Contents/MacOS/Python` with argv[0] replaced, so a link
    to it runs as `Python`, which `caller.agent_like` rightly takes for no agent
    (agent-ci service-macos: the remembered daemon owner was never remembered)."""
    app = Path(sys.base_prefix) / "Resources" / "Python.app" / "Contents" / "MacOS" / "Python"
    return str(app) if sys.platform == "darwin" and app.is_file() else os.path.realpath(sys.executable)


class _Agent:
    """A coding agent as the service sees one (the kernel names it `claude`),
    whose shell runs what this test hands it: its children are under it."""

    def __init__(self, tmp_path: Path) -> None:
        self.proc = _named_agent(tmp_path, "-c", _AGENT_DRIVER, sys.executable, program=_interpreter_binary())
        from probe.service import caller

        assert caller.agent_like(self.proc.pid), "the stand-in must look like an agent, or nothing here is tested"
        assert self.proc.stdout.readline().strip() == "ready", self.proc.stderr.read()
        self.owner = _owner(self.proc)

    def shell(self, code: str, *args: str) -> str:
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CODE_SESSION_ID"}
        self.proc.stdin.write(json.dumps({"code": code, "args": list(args), "env": env}) + "\n")
        self.proc.stdin.flush()
        answer = json.loads(self.proc.stdout.readline())
        assert answer["rc"] == 0, answer["err"]
        return answer["out"]

    def forge_then_act(self, steps: list) -> dict:
        return json.loads(self.shell(_ACTION_AS.replace('"forged"', f'"f-{time.monotonic_ns()}"'), json.dumps(steps)))

    def close(self) -> None:
        kill_agent(self.proc)


def test_a_daemon_session_s_shell_cannot_end_or_reregister_its_way_to_an_action(service_home, monkeypatch, tmp_path):
    """#3360 as reported, and each way around it, from the shell of a coding
    agent this test registered (as its `tap watch` would): end the session,
    re-register it `inline` under the same agent, register a fake `inline`
    session under the agent. Every one leaves the action refused, and so does
    the registrant's own real end: the agent ran under the daemon."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    core = FakeCore(service_home.home)
    core.plan("logout", steps=[])
    service_home.start()
    agent = _Agent(tmp_path)
    try:
        me = agent.owner
        _register(service_home, SID, me, generation=5)
        tries = [
            [[Method.SESSION_END, {"sid": SID, "generation": 5}]],
            [[Method.SESSION_REGISTER, {"sid": SID, "harness": "claude_code", "mode": "inline", "owner": me,
                                        "generation": 5}]],
            [[Method.SESSION_REGISTER, {"sid": SID, "harness": "claude_code", "mode": "inline", "owner": me,
                                        "generation": 6}]],
            [[Method.SESSION_REGISTER, {"sid": OTHER, "harness": "claude_code", "mode": "inline", "owner": me,
                                        "generation": 1}]],
            [[Method.SESSION_END, {"sid": SID, "generation": 6}],
             [Method.SESSION_REGISTER, {"sid": SID, "harness": "claude_code", "mode": "inline", "owner": me,
                                        "generation": 7}]],
        ]
        for steps in tries:
            answer = agent.forge_then_act(steps)
            assert answer == {"refused": {"reason": "daemon_session", "sid": SID}}, steps
        assert _listed(service_home)[SID]["mode"] == Mode.DAEMON, "only its registrant moves it out of daemon mode"
        service_home.call(Method.SESSION_END, {"sid": SID, "generation": 5})
        assert SID not in _listed(service_home)
        assert agent.forge_then_act([])["refused"]["reason"] == "daemon_session"
        assert core.calls("logout") == []
    finally:
        agent.close()


def test_a_fake_registration_under_the_shell_itself_does_not_hide_the_agent(service_home, monkeypatch):
    """A registration naming the caller's own process (found first, nearest in
    its ancestry) is one match; the daemon session above it is another."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    core = FakeCore(service_home.home)
    core.plan("logout", steps=[])
    service_home.start()
    me = client.owner_of(os.getpid())
    _register(service_home, SID, me)
    script = (
        "import json, os\n"
        "from probe.service import client\n"
        "from probe.service.protocol import Client, Method\n"
        "conn = client.Connection.open()\n"
        "conn.hello(Client.CLI, '0')\n"
        "own = client.owner_of(os.getpid())\n"
        f"conn.call(Method.SESSION_REGISTER, {{'sid': '{OTHER}', 'harness': 'claude_code', 'mode': 'inline',"
        " 'owner': own, 'generation': 1})\n"
        "try:\n"
        "    conn.call(Method.ACTION_RUN, {'action': 'logout', 'params': {}, 'client_request_id': 'x'})\n"
        "    print('ran')\n"
        "except client.ServiceError as exc:\n"
        "    print(json.dumps(exc.data))\n"
    )
    done = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=30)
    assert json.loads(done.stdout) == {"reason": "daemon_session", "sid": SID}, done.stderr
    assert core.calls("logout") == []


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="a peer's environment is read on Linux only")
def test_a_detached_job_of_an_ended_daemon_session_is_still_refused(service_home, tmp_path):
    """Its environment names the session, which its registrant has ended: the
    agent registered under it in daemon mode still runs, so it is refused."""
    core = FakeCore(service_home.home)
    core.plan("logout", steps=[])
    service_home.start()
    agent = _named_agent(service_home.home)
    try:
        _register(service_home, SID, _owner(agent))
        assert service_home.call(Method.SESSION_END, {"sid": SID, "generation": 1}) == {}
        env = {**os.environ, "CLAUDE_CODE_SESSION_ID": SID}
        done = subprocess.run([sys.executable, "-c", _ACTION_AS, "[]"], env=env, capture_output=True, text=True,
                              timeout=30, start_new_session=True)
        assert json.loads(done.stdout) == {"refused": {"reason": "daemon_session", "sid": SID}}, done.stderr
        kill_agent(agent)  # its agent gone, nothing is remembered for it
        assert wait_for(lambda: not _agent_named(service_home, SID, env), 5.0)
    finally:
        kill_agent(agent)
    (call,) = wait_for(lambda: core.calls("logout"), 10.0)
    assert call["env"]["CLAUDE_CODE_SESSION_ID"] is None, "nothing registered names it any more"


def _agent_named(sh, sid: str, env: dict) -> bool:
    """Is a job carrying `sid` still refused? (A fresh request id each time.)"""
    script = _ACTION_AS.replace('"forged"', f'"try-{time.monotonic_ns()}"')
    done = subprocess.run([sys.executable, "-c", script, "[]"], env=env, capture_output=True, text=True, timeout=30,
                          start_new_session=True)
    return "refused" in json.loads(done.stdout)


def test_the_action_child_is_told_who_asked(service_home, monkeypatch):
    """As `desktop.request`'s: the child resolves the caller's own session from
    its process, registered or not (`probe.core.run._caller_session_refusal`)."""
    from probe.service.management import CALLER_PID_ENV, CALLER_START_ENV

    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    core = FakeCore(service_home.home)
    core.plan("logout", steps=[])
    service_home.start()
    with service_home.connect() as conn:
        answer = conn.call(Method.ACTION_RUN, {"action": "logout", "params": {}, "client_request_id": "c1"})
        status = {"action_id": answer["action_id"]}
        assert wait_for(lambda: conn.call(Method.ACTION_STATUS, status)["state"] == "done", 10.0)
    (call,) = core.calls("logout")
    assert call["env"][CALLER_PID_ENV] == str(os.getpid())
    if sys.platform.startswith("linux"):
        assert call["env"][CALLER_START_ENV] == client.owner_of(os.getpid())["start_time"]


# ---------------------------------------------------------------------------
# The action child (`probe.core.run`).
# ---------------------------------------------------------------------------


def _core_run(action: str, request: dict, env: dict) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", "-m", "probe.core.run", action], input=json.dumps(request),
                          capture_output=True, text=True, timeout=120, env=env, cwd=str(Path(env["HOME"])))


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="another process's environment is read on Linux")
def test_the_child_refuses_for_the_callers_daemon_session_registered_or_not(tmp_path):
    """No registration anywhere: the caller's environment names a session the
    daemon records, and the child refuses `session_default` for it, exactly as
    `probe session default` refuses it in that shell."""
    from probe.sdk import session_marker
    from probe.service.management import CALLER_PID_ENV, CALLER_START_ENV

    home = tmp_path / "h"
    home.mkdir()
    base = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(home), "XDG_STATE_HOME": str(home / "s"),
            "XDG_CONFIG_HOME": str(home / "c"), "PROBE_TELEMETRY": "0"}
    old = os.environ.get("XDG_STATE_HOME")
    os.environ["XDG_STATE_HOME"] = base["XDG_STATE_HOME"]
    try:
        session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
        session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    finally:
        if old is None:
            os.environ.pop("XDG_STATE_HOME", None)
        else:
            os.environ["XDG_STATE_HOME"] = old
    shell = subprocess.Popen(["sleep", "60"], env={**base, "CLAUDECODE": "1", "CLAUDE_CODE_SESSION_ID": SID})
    try:
        start = wait_for(lambda: client.owner_of(shell.pid), 2.0)["start_time"]
        asked = {**base, CALLER_PID_ENV: str(shell.pid), CALLER_START_ENV: start}
        refused = _core_run("session_default", {"state": "off"}, asked)
        assert refused.returncode == 2, refused.stderr
        events = [json.loads(line) for line in refused.stdout.splitlines() if line.strip()]
        assert events[-1]["event"] == "done" and events[-1]["ok"] is False
        gone = _core_run("session_default", {"state": "off"}, {**asked, CALLER_START_ENV: "1 Jan 1970"})
        assert gone.returncode == 2 and "has exited" in gone.stderr
    finally:
        shell.kill()
        shell.wait(timeout=5)


def test_a_read_action_never_looks_the_caller_up(monkeypatch):
    from probe.core import run
    from probe.core.requests import ActionName
    from probe.service.management import CALLER_PID_ENV, CALLER_START_ENV

    monkeypatch.setenv(CALLER_PID_ENV, "1")
    monkeypatch.setenv(CALLER_START_ENV, "never")
    assert run._caller_session_refusal(ActionName.STATUS) is None  # noqa: SLF001
    assert CALLER_PID_ENV not in os.environ and CALLER_START_ENV not in os.environ, "and nothing inherits them"


def test_a_session_the_request_names_is_kept(monkeypatch):
    from probe.core import run
    from probe.core.requests import ActionName
    from probe.service.management import CALLER_PID_ENV

    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "named-by-the-context-0001")
    monkeypatch.setenv(CALLER_PID_ENV, str(os.getpid()))
    monkeypatch.setattr("probe.sdk.agent_session.session_env_of_process",
                        lambda pid: pytest.fail("the request named the session already"))
    assert run._caller_session_refusal(ActionName.LOGOUT) is None  # noqa: SLF001
    assert os.environ["CLAUDE_CODE_SESSION_ID"] == "named-by-the-context-0001"


# ---------------------------------------------------------------------------
# The mailbox (#3361).
# ---------------------------------------------------------------------------


def _state() -> Path:
    return Path(os.environ["XDG_STATE_HOME"]) / "probe"


@pytest.fixture
def home(service_home, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(service_home.home / "state"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ATTENDED", raising=False)
    service_home.start()
    return service_home


def _alert(n: int, sid: str = SID) -> mailbox.Message:
    return mailbox.Message(id=mailbox.alert_message_id([n]), session=sid, kind=Kind.ALERT,
                           text=f"digits-svm crashed at step {n}.", keep=True, alerts=[n])


def _post_params(msg: mailbox.Message) -> dict:
    return {"sid": msg.session, "state_dir": str(_state()), "message": asdict(msg)}


#: A `tap watch` stand-in: it registers the session (owner: argv[1]), then its
#: "worker" -- the process itself -- posts what it is told to, and says
#: whether the service took it.
_TAP_WATCH = r'''
import json, sys
from probe.daemon import mailbox
from probe.service import client
from probe.service.protocol import Method
owner = client.owner_of(int(sys.argv[1]))
client.call(Method.SESSION_REGISTER, {"sid": sys.argv[2], "harness": "claude_code", "mode": "daemon",
                                      "owner": owner, "generation": 1, "state_dir": sys.argv[3]})
print("ready", flush=True)
for line in sys.stdin:
    msg = mailbox.Message(**json.loads(line))
    print(json.dumps({"via_service": mailbox.post_via_service(msg)}), flush=True)
'''


def test_only_the_sessions_own_worker_posts_through_the_service(home):
    agent, owner = spawn_agent()
    tap = subprocess.Popen([sys.executable, "-c", _TAP_WATCH, str(agent.pid), SID, str(_state())],
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        assert tap.stdout.readline().strip() == "ready", tap.stderr.read()
        # The agent's shell (here: this test, which runs under no part of the session).
        with pytest.raises(client.ServiceError) as raised:
            home.call(Method.MAILBOX_POST, _post_params(_alert(1)))
        assert raised.value.code == ErrorCode.REFUSED
        assert raised.value.data == {"reason": Bound.NOT_SESSION}
        assert mailbox.waiting(SID) == [], "nothing written"
        assert "refused mailbox.post" in home.log()
        # An older worker, or any refused poster, writes the file itself: delivered all the same.
        mailbox.publish(_alert(2))
        assert [m.id for _, m in mailbox.waiting(SID)] == [_alert(2).id]
        # The session's own worker (under its registrant).
        tap.stdin.write(json.dumps(asdict(_alert(3))) + "\n")
        tap.stdin.flush()
        assert json.loads(tap.stdout.readline()) == {"via_service": True}
        assert {m.id for _, m in mailbox.waiting(SID)} == {_alert(2).id, _alert(3).id}
    finally:
        tap.kill()
        tap.wait(timeout=5)
        kill_agent(agent)


def _hook(sid: str = SID) -> subprocess.CompletedProcess:
    payload = {"hook_event_name": "UserPromptSubmit", "session_id": sid, "cwd": "/tmp", "permission_mode": "default",
               "transcript_path": f"/home/u/.claude/projects/-tmp/{sid}.jsonl"}
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ["HOME"],
           "XDG_STATE_HOME": os.environ["XDG_STATE_HOME"]}
    return subprocess.run([sys.executable, str(READS_HOOK)], input=json.dumps(payload), capture_output=True,
                          text=True, env=env, timeout=30)


def _claims(sid: str = SID) -> list[dict]:
    path = mailbox.claim_log_path(sid)
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def test_a_hook_outside_the_session_claims_on_the_files_and_one_inside_through_the_service(home):
    """The reads hook runs as a child of this test. Registered under another
    agent, its claim is refused and it takes the message itself (delivered, no
    service token); registered under this test, the service claims for it."""
    agent, owner = spawn_agent()
    try:
        _register(home, SID, owner)
        mailbox.publish_here(_alert(4))
        started = time.monotonic()
        shown = _hook()
        assert shown.returncode == 0, shown.stderr
        assert json.loads(shown.stdout)["hookSpecificOutput"]["additionalContext"] == _alert(4).rendered()
        assert time.monotonic() - started < 3.0, "a refusal is an answer: no wait for a deadline"
        (entry,) = _claims()
        assert "token" not in entry, "claimed here, not by the service"
        assert "refused mailbox.claim" in home.log()
    finally:
        kill_agent(agent)
    me = client.owner_of(os.getpid())
    _register(home, OTHER, me)
    mailbox.publish_here(_alert(5, OTHER))
    shown = _hook(OTHER)
    assert json.loads(shown.stdout)["hookSpecificOutput"]["additionalContext"] == _alert(5, OTHER).rendered()
    (entry,) = _claims(OTHER)
    assert entry.get("token"), "claimed by the service, for this hook"


def test_another_sessions_shell_cannot_take_its_messages(home):
    """The cross-session case: the forger runs under another agent (this test),
    the session's agent is a process it does not descend from."""
    agent, owner = spawn_agent()
    try:
        _register(home, SID, owner)
        mailbox.publish_here(_alert(6))
        name = mailbox.waiting(SID)[0][0].name
        script = (
            "import json, sys\n"
            "from probe.service import client\n"
            "from probe.service.protocol import Method\n"
            "try:\n"
            f"    print(json.dumps(client.call(Method.MAILBOX_CLAIM, {{'sid': '{SID}', 'state_dir': sys.argv[1],"
            f" 'names': ['{name}'], 'by': 'x', 'token': 't'}})))\n"
            "except client.ServiceError as exc:\n"
            "    print(json.dumps(exc.data))\n"
        )
        done = subprocess.run([sys.executable, "-c", script, str(_state())], capture_output=True, text=True,
                              timeout=30, env={**os.environ})
        assert done.returncode == 0, done.stderr
        assert json.loads(done.stdout) == {"reason": Bound.NOT_SESSION}
        assert len(mailbox.waiting(SID)) == 1, "still there for the session's own hook"
    finally:
        kill_agent(agent)


def _bare_service(tmp_path, monkeypatch):
    from probe.service import server, updater

    monkeypatch.setattr(updater, "_hosted_live", updater._hosted_live)  # noqa: SLF001 -- Service sets it
    return server, server.Service(registry=Registry(tmp_path / "sessions.json"))


def test_events_forked_from_a_hook_host_may_claim(tmp_path, monkeypatch):
    """A warm host's events run as its children; the host is this service's
    child. Nothing above this service counts: an owner there names nothing."""
    from probe.service import caller

    server, service = _bare_service(tmp_path, monkeypatch)
    me = service.pid
    service.registry.owner_alive = lambda pid, start: True
    service.registry.register(SID, "claude_code", Mode.DAEMON, {"pid": 7, "start_time": "s7"}, 1)
    monkeypatch.setattr(service.hookhosts, "pids", lambda: {4242})
    chains = {
        900: [(900, "x"), (901, "y"), (4242, "h"), (me, "m"), (7, "s7")],  # hosted event
        910: [(910, "x"), (4343, "z"), (me, "m"), (7, "s7")],  # another child of the service
        920: [(920, "x"), (921, "y"), (7, "s7")],  # under the session's agent
    }
    monkeypatch.setattr(caller, "lineage", lambda pid: iter(chains[pid]))

    def claim(pid: int) -> bool:
        conn = server.Connection(None, peer_pid=pid)
        try:
            asyncio.run(service._refuse_foreign_mail(conn, SID, claim=True))  # noqa: SLF001
        except RpcError as exc:
            assert exc.data == {"reason": Bound.NOT_SESSION}
            return False
        return True

    assert claim(900) and claim(920)
    assert not claim(910)
    service.mailhost.close()


def test_a_worker_this_service_started_may_post_and_its_siblings_may_not(tmp_path, monkeypatch):
    from probe.service import caller

    server, service = _bare_service(tmp_path, monkeypatch)
    me = service.pid
    monkeypatch.setattr(service.workers, "pids", lambda sid: {5151} if sid == SID else set())
    chains = {5151: [(5151, "w"), (me, "m")], 5252: [(5252, "w2"), (me, "m")]}
    monkeypatch.setattr(caller, "lineage", lambda pid: iter(chains[pid]))

    def post(pid: int, sid: str) -> bool:
        try:
            asyncio.run(service._refuse_foreign_mail(server.Connection(None, peer_pid=pid), sid, claim=False))  # noqa: SLF001
        except RpcError:
            return False
        return True

    assert post(5151, SID)
    assert not post(5151, OTHER), "its own session's worker, never another's"
    assert not post(5252, SID)
    assert post(me, OTHER), "this service's own (a hint, a run alert)"
    service.mailhost.close()


def test_a_hosted_recorders_link_registers_as_the_service(tmp_path, monkeypatch):
    """A hosted recorder's `tap/service_link.py` connects from the service's own
    process: its registrations are the service's, which a forged call never is."""
    server, service = _bare_service(tmp_path, monkeypatch)
    assert service._caller_of(server.Connection(None, peer_pid=service.pid)) == SERVICE  # noqa: SLF001
    assert service._caller_of(None) == SERVICE  # noqa: SLF001
    other = service._caller_of(server.Connection(None, peer_pid=1))  # noqa: SLF001
    assert other["pid"] == 1
    service.mailhost.close()


# ---------------------------------------------------------------------------
# Review of #3391: the remembered agents, the log, the registrant, the guard.
# ---------------------------------------------------------------------------

AGENT = {"pid": 5101, "start_time": "ag"}


def test_a_full_list_never_drops_a_running_agent(tmp_path, monkeypatch):
    """A flood of fake daemon sessions, each under a live process, pushed the
    real agent out of the list; one same-owner `inline` register then let an
    action through. The list grows past its bound before it forgets a running
    agent, drops the exited ones first, and the `inline` register is refused."""
    from probe.service import registry as registry_mod

    monkeypatch.setattr(registry_mod, "MAX_DAEMON_OWNERS", 3)
    flood = [{"pid": 7000 + n, "start_time": f"f{n}"} for n in range(5)]
    late = {"pid": 7100, "start_time": "late"}
    reg, procs = _registry(tmp_path, A, B, AGENT, late, *flood)
    reg.register(SID, "claude_code", Mode.DAEMON, AGENT, 1, caller=A)
    for n, owner in enumerate(flood):
        reg.register(f"fake-{n}", "claude_code", Mode.DAEMON, owner, 1, caller=B)
    assert reg.daemon_owner(AGENT["pid"], AGENT["start_time"]) is not None, "never pushed out while it runs"
    assert len(reg.daemon_owners) == 6
    _refused(reg.register, SID, "claude_code", Mode.INLINE, AGENT, 1, caller=B)
    assert reg.sessions[SID].mode == Mode.DAEMON
    procs.exit(flood[0])
    procs.exit(flood[1])
    reg.register("one-more", "claude_code", Mode.DAEMON, late, 1, caller=B)
    assert (flood[0]["pid"], flood[0]["start_time"]) not in reg.daemon_owners, "an exited one goes first"
    assert (flood[1]["pid"], flood[1]["start_time"]) not in reg.daemon_owners
    assert reg.daemon_owner(AGENT["pid"], AGENT["start_time"]) is not None
    assert reg.daemon_owner(late["pid"], late["start_time"]) is not None


def test_only_its_registrant_moves_a_session_out_of_daemon_mode(tmp_path):
    reg, _ = _registry(tmp_path, A, B, OWNER)
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 1, caller=A)
    for mode, generation in ((Mode.INLINE, 1), (Mode.OFF, 2)):
        err = _refused(reg.register, SID, "claude_code", mode, OWNER, generation, caller=B)
        assert err.data == {"reason": Bound.NOT_REGISTRANT}
    assert reg.sessions[SID].mode == Mode.DAEMON
    kept = reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 2, caller=B)
    assert kept.outcome == Outcome.REPLACED, "a hand-off that keeps it in daemon mode still goes through"
    assert reg.register(SID, "claude_code", Mode.INLINE, OWNER, 2, caller=A).outcome == Outcome.REFRESHED
    assert reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 3, caller=B).outcome == Outcome.REPLACED
    assert reg.register(SID, "claude_code", Mode.OFF, OWNER, 3, caller=SERVICE).outcome == Outcome.REFRESHED


def test_a_refusal_is_logged_once_per_session_and_process_a_while(tmp_path, monkeypatch):
    """Two agents on one session id: the newer tap is refused every 2 s for as
    long as the older one runs. The service says so once per (session,
    process) every 10 minutes, not at every retry."""
    server, service = _bare_service(tmp_path, monkeypatch)
    lines: list = []
    monkeypatch.setattr(server, "log", lines.append)
    refusal = RpcError(ErrorCode.REFUSED, "refused", {"reason": Bound.NOT_REGISTRANT})
    newer, other = {"pid": 11, "start_time": "a"}, {"pid": 12, "start_time": "b"}
    for n in range(5):
        service._log_unbound(refusal, "session.register", SID, newer, now=100.0 + n)  # noqa: SLF001
    service._log_unbound(refusal, "session.register", SID, other, now=105.0)  # noqa: SLF001
    service._log_unbound(refusal, "session.end", OTHER, newer, now=106.0)  # noqa: SLF001
    assert len(lines) == 3
    service._log_unbound(refusal, "session.register", SID, newer, now=100.0 + 599)  # noqa: SLF001
    assert len(lines) == 3
    service._log_unbound(refusal, "session.register", SID, newer, now=100.0 + 601)  # noqa: SLF001
    assert len(lines) == 4
    service.mailhost.close()


_TAP_ROOT = str(AGENT_ROOT / "plugins" / "probe-research-tap")
#: A real tap `ServiceLink` (the tap's own code, unchanged by this PR) for one
#: session and one owner, retrying fast.
_TAP_LINK = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from tap import service_link
owner = json.loads(sys.argv[3])
link = service_link.ServiceLink(sys.argv[2], harness="test", owner_fn=lambda: owner,
                                heartbeat_s=0.3, retry_s=0.05, undecided_wait_s=0)
link.start()
sys.stdout.write("started\n"); sys.stdout.flush()
sys.stdin.readline()
link.stop()
'''


def test_two_live_agents_on_one_session_keep_the_older_and_log_one_line(service_home, monkeypatch):
    """`claude --continue` in a second tab while the first runs: the older
    registrant keeps the session until it exits; the newer tap's retries (every
    0.05 s here) leave one line in the service log, not one per retry."""
    from probe.service import paths

    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    service_home.start()
    first, owner1 = spawn_agent()
    second, owner2 = spawn_agent()
    state = paths.home() / ".local" / "state" / "probe" / "sessions"
    state.mkdir(parents=True, exist_ok=True)
    (state / f"{SID}.state").write_text("daemon")
    env = {**os.environ, "PROBE_TAP_SOURCE": "claude_code"}  # harness-literal-ok: the tap's default source
    links = []
    try:
        for owner in (owner1, owner2):
            link = subprocess.Popen([sys.executable, "-I", "-c", _TAP_LINK, _TAP_ROOT, SID, json.dumps(owner)],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, env=env)
            links.append(link)
            assert link.stdout.readline().strip() == "started"
            if owner is owner1:
                assert wait_for(lambda: _listed(service_home).get(SID, {}).get("owner") == owner1, 3.0)
        time.sleep(1.5)  # ~30 refused registers from the newer link
        assert _listed(service_home)[SID]["owner"] == owner1
        refused = [line for line in service_home.log().splitlines() if "not the process that registered it" in line]
        assert len(refused) == 1, refused
    finally:
        for link in links:
            link.kill()
        kill_agent(first)
        kill_agent(second)


def test_a_session_from_before_the_upgrade_is_bound_at_its_next_heartbeat(tmp_path):
    """Sessions open across the upgrade load with no registrant; the next
    register from their tap (a heartbeat) makes it theirs."""
    reg, _ = _registry(tmp_path, A, B, OWNER)
    reg.register(SID, "claude_code", Mode.INLINE, OWNER, 1, caller=A)
    data = json.loads(reg.path.read_text())
    for row in data["sessions"]:
        row.pop("registrant")
    reg.path.write_text(json.dumps(data))
    again, _ = _registry(tmp_path, A, B, OWNER)
    again.load()
    assert again.sessions[SID].registrant is None
    again.register(SID, "claude_code", Mode.INLINE, OWNER, 1, caller=A)
    again.register(SID, "claude_code", Mode.INLINE, OWNER, 1, caller=A)
    assert again.sessions[SID].registrant == A
    _refused(again.end, SID, 1, B)
    assert again.end(SID, 1, A) is not None


def test_a_hand_off_takes_a_registration_its_registrant_left(tmp_path):
    """A hook's `session.record` registered it and exited; the `tap watch` that
    records it now re-registers under the same owner: it is the registrant, and
    its own `session.end` at SessionEnd is accepted."""
    hook, watch = {"pid": 4201, "start_time": "h"}, {"pid": 4202, "start_time": "w"}
    reg, procs = _registry(tmp_path, hook, watch, B, OWNER)
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 1, caller=hook)
    procs.exit(hook)
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 2, caller=watch)
    assert reg.sessions[SID].registrant == watch
    _refused(reg.end, SID, 2, B)
    assert reg.end(SID, 2, watch) is not None


def test_a_tap_takes_over_what_this_service_no_longer_records(tmp_path):
    watch = {"pid": 4202, "start_time": "w"}
    reg, _ = _registry(tmp_path, watch, OWNER)
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 1)  # a hosted recorder's link
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 2, caller=watch)
    assert reg.sessions[SID].registrant == SERVICE, "while this service records it, it stays the service's"
    reg.service_records = lambda sid: False  # its recorder stood down (a `tap watch` took it back)
    reg.register(SID, "claude_code", Mode.DAEMON, OWNER, 2, caller=watch)
    assert reg.sessions[SID].registrant == watch
    assert reg.end(SID, 2, watch) is not None


def test_only_a_coding_agent_process_is_remembered(tmp_path):
    """A fake daemon session can name any live process as its owner (the
    desktop app, `systemd --user`): only one that looks like a coding agent is
    remembered past its session, so nothing else is refused for good."""
    plain = subprocess.Popen(["sleep", "60"])
    agent = _named_agent(tmp_path)
    try:
        reg = Registry(tmp_path / "sessions.json")
        not_agent, real = _owner(plain), _owner(agent)
        reg.register("fake", "claude_code", Mode.DAEMON, not_agent, 1)
        reg.register(SID, "claude_code", Mode.DAEMON, real, 1)
        reg.end("fake", 1)
        reg.end(SID, 1)
        assert reg.daemon_owner(not_agent["pid"], not_agent["start_time"]) is None
        assert reg.daemon_owner(real["pid"], real["start_time"]) is not None
    finally:
        kill_agent(plain)
        kill_agent(agent)


def test_agent_like_reads_the_names_agents_run_under(tmp_path):
    from probe.service import caller

    procs = [_named_agent(tmp_path, name=name) for name in ("claude", "codex", "kimi-code", "pi")]
    plain = subprocess.Popen(["sleep", "60"])
    try:
        assert all(caller.agent_like(p.pid) for p in procs)
        assert not caller.agent_like(plain.pid) and not caller.agent_like(os.getpid())
    finally:
        for p in (*procs, plain):
            kill_agent(p)


def test_a_fake_daemon_session_naming_the_app_does_not_stick(service_home, monkeypatch):
    """This test stands in for the desktop app. Another process registers a
    fake daemon session naming it as the owner, then ends it: the app's next
    action is not refused (it ran under no agent)."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    core = FakeCore(service_home.home)
    core.plan("logout", steps=[])
    service_home.start()
    app = client.owner_of(os.getpid())
    script = (
        "import json, sys\n"
        "from probe.service import client\n"
        "from probe.service.protocol import Method\n"
        "conn = client.Connection.open(); conn.hello('cli', '0')\n"
        f"conn.call(Method.SESSION_REGISTER, {{'sid': 'fake', 'harness': 'claude_code', 'mode': 'daemon',"
        " 'owner': json.loads(sys.argv[1]), 'generation': 1})\n"
        "conn.call(Method.SESSION_END, {'sid': 'fake', 'generation': 1})\n"
    )
    done = subprocess.run([sys.executable, "-c", script, json.dumps(app)], capture_output=True, text=True, timeout=30)
    assert done.returncode == 0, done.stderr
    with service_home.connect() as conn:
        answer = conn.call(Method.ACTION_RUN, {"action": "logout", "params": {}, "client_request_id": "app"})
    assert answer.get("action_id")
