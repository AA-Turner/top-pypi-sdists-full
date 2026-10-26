"""The daemon host: every session's daemon worker in one child process of the service.

Plan `~/plans/daemon-in-service/PLAN.md` (H1-H15, S1-S6, P1). These start REAL
hosts (`probe.daemon.host`, through the service's `daemonhost.DaemonHost`) and
real workers in them, on sessions whose model endpoint is a closed local port:
nothing reaches the network, and a worker with an empty queue does no model call.
"""

from __future__ import annotations

import json
import os
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import textwrap
import time
import uuid
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")

from probe.daemon import host as host_mod  # noqa: E402
from probe.daemon import proxy as proxy_mod  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from probe.service import daemonhost  # noqa: E402
from probe.service import updater as updater_mod  # noqa: E402
from probe.service import workers as workers_mod  # noqa: E402

# Real hosts and real workers, several seconds each: nightly (`heavy`), and wherever
# the daemon extra is installed (`importorskip` above).
pytestmark = [pytest.mark.skipif(os.name != "posix", reason="the daemon host is POSIX only"), pytest.mark.heavy]


def _wait(predicate, timeout: float = 60.0, step: float = 0.1):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        value = predicate()
        if value:
            return value
        time.sleep(step)
    raise AssertionError(f"timed out after {timeout:.0f} s")


class Session:
    """A recorded session's files: its switch, an empty transcript, its folders."""

    def __init__(self, base: Path, name: str, state_word: str = "daemon") -> None:
        self.sid = f"{name}-{uuid.uuid4()}"
        self.home = base / "home"
        self.state = self.home / ".local" / "state"
        self.sessions = self.state / "probe" / "sessions"
        self.daemon_dir = self.state / "probe" / "daemon"
        self.sessions.mkdir(parents=True, exist_ok=True)
        self.project = base / f"project-{name}"
        self.project.mkdir(parents=True, exist_ok=True)
        self.transcript = self.project / "t.jsonl"
        self.transcript.write_text("")
        self.switch(state_word)

    def switch(self, word: str) -> None:
        (self.sessions / f"{self.sid}.state").write_text(word)

    @property
    def env(self) -> dict:
        return {"HOME": str(self.home), "XDG_STATE_HOME": str(self.state), "PATH": os.environ.get("PATH", ""),
                "PROBE_BASE_URL": "http://127.0.0.1:9", "PROBE_DAEMON_KEY": f"key-{self.sid[:6]}",
                **workers_mod.SUPERVISOR_ENV}

    def spec(self) -> dict:
        return {"sid": self.sid, "transcript": str(self.transcript), "cwd": str(self.project), "source": "claude_code",
                "daemon_dir": str(self.daemon_dir), "env": self.env}

    def lease(self) -> dict | None:
        try:
            return json.loads((self.sessions / f"{self.sid}.writer").read_text())
        except (OSError, ValueError):
            return None


@pytest.fixture
def manager(tmp_path):
    logs: list[str] = []
    incidents: list[tuple] = []
    host = daemonhost.DaemonHost(log=logs.append, incident=lambda *a, **k: incidents.append(a),
                                 python=lambda: sys.executable)
    host.logs, host.incidents = logs, incidents
    yield host
    with host._lock:
        procs = ([host._current] if host._current else []) + list(host._retired)
    for proc in procs:
        host._kill(proc)


def test_two_sessions_run_in_one_host_each_with_its_own_lease_and_logs(manager, tmp_path):
    a, b = Session(tmp_path, "a"), Session(tmp_path, "b")
    run_a, run_b = manager.start(a.spec()), manager.start(b.spec())
    assert run_a.pid == run_b.pid == manager._current.pid  # one process
    leases = _wait(lambda: (a.lease(), b.lease()) if a.lease() and b.lease() else None)
    assert {leases[0]["pid"], leases[1]["pid"]} == {run_a.pid}
    assert leases[0]["owner"] and leases[1]["owner"] and leases[0]["owner"] != leases[1]["owner"]
    beat = _wait(lambda: manager._current.beat.get("runs") and len(manager._current.beat["runs"]) == 2
                 and manager._current.beat)
    assert {row["sid"] for row in beat["runs"]} == {a.sid, b.sid}
    for session in (a, b):
        session.switch("off")  # the worker leaves, as a worker process does
    assert _wait(lambda: run_a.poll() is not None and run_b.poll() is not None)
    assert (run_a.poll(), run_b.poll()) == (0, 0)
    # Each session's log is its own: no record of the other's in it.
    for mine, other in ((a, b), (b, a)):
        worker_log = mine.daemon_dir / "sessions" / mine.sid / "worker.log"
        assert worker_log.exists()
        assert other.sid not in worker_log.read_text()
    assert manager.runs() == 0


def test_a_run_whose_owner_leaves_finishes_and_the_host_then_exits(tmp_path):
    folder = tmp_path / "h"
    sock_path = Path(tempfile.mkdtemp(prefix="pdh", dir="/tmp")) / "h.sock"  # a private folder, as the host requires
    env = {"HOME": str(tmp_path / "home"), "PATH": os.environ.get("PATH", "")}
    proc = subprocess.Popen([sys.executable, "-I", "-c", host_mod.ENTRY, host_mod.ARGV_MARK, "--folder", str(folder),
                             "--socket", str(sock_path)], env=env, start_new_session=True,
                            stdout=subprocess.DEVNULL, stderr=open(tmp_path / "host.log", "ab"))
    try:
        _wait(sock_path.exists, 30)
        assert stat.S_IMODE(sock_path.stat().st_mode) == 0o600
        s = Session(tmp_path, "s")
        sock = socket.socket(socket.AF_UNIX)
        sock.connect(str(sock_path))
        f = sock.makefile("rwb")
        f.write(b'{"op":"hello","role":"proxy"}\n')
        f.flush()
        assert json.loads(f.readline())["pid"] == proc.pid
        f.write((json.dumps({"op": "start", "run": "r1", **s.spec()}) + "\n").encode())
        f.flush()
        assert json.loads(f.readline())["op"] == "started"
        _wait(s.lease, 60)
        f.close()
        sock.close()  # its owner is gone: an empty queue is finished at once
        assert proc.wait(timeout=60) == 0
        assert s.lease()["reason"] == "stopped"
        assert not sock_path.exists()  # the host removed its own socket
    finally:
        if proc.poll() is None:
            proc.kill()


def test_a_crash_in_one_run_is_that_sessions_crash_and_the_other_starts_again(manager, tmp_path):
    a, b = Session(tmp_path, "crasher"), Session(tmp_path, "bystander")
    patch_dir = tmp_path / "patch"
    patch_dir.mkdir()
    (patch_dir / "crashpatch.py").write_text(textwrap.dedent(f"""
        import asyncio, ctypes
        from probe.daemon import worker
        _loop = worker.Worker.loop
        async def loop(self):
            if self.session.session_id == {a.sid!r}:
                await asyncio.sleep(1.5)
                ctypes.string_at(0)  # a native crash on this run's thread
            return await _loop(self)
        worker.Worker.loop = loop
    """))
    wrapper = tmp_path / "python"
    wrapper.write_text(textwrap.dedent(f"""\
        #!/bin/bash
        shift 3  # -I -c <entry>: replaced by the same entry with the patch first
        exec {sys.executable} -c 'import sys; sys.path.insert(0, "{patch_dir}"); import crashpatch; \\
        from probe.daemon.host import main; sys.exit(main(sys.argv[1:]))' "$@"
    """))
    wrapper.chmod(0o755)
    manager._python = lambda: str(wrapper)
    run_a, run_b = manager.start(a.spec()), manager.start(b.spec())
    assert _wait(lambda: run_a.poll() is not None and run_b.poll() is not None, 90)
    assert run_a.poll() == worker_mod.EXIT_CRASHED  # its Supervisor backs off
    assert run_b.poll() == 0  # started again at once, its conversation resumed from disk
    assert any("crash was in session " + a.sid in line for line in manager.logs)


def test_replacing_the_host_hands_its_live_runs_over(manager, tmp_path):
    s = Session(tmp_path, "s")
    run = manager.start(s.spec())
    _wait(s.lease)
    old_pid = run.pid
    manager.replace("a test")
    marker = s.daemon_dir / f"{daemonhost._safe_sid(s.sid)}.handover"
    assert marker.stat().st_mtime > time.time() + 60  # its ask stays fresh while it finishes its round
    assert _wait(lambda: run.poll() is not None) and run.poll() == 0
    assert s.lease()["reason"] == "handover"
    again = manager.start(s.spec())  # its Supervisor starts it again: in a new host
    assert again.pid != old_pid
    s.switch("off")
    assert _wait(lambda: again.poll() is not None) and again.poll() == 0


def test_a_draining_run_moves_to_a_new_host_when_its_host_dies(manager, tmp_path):
    s = Session(tmp_path, "s")
    run = manager.start(s.spec())
    _wait(s.lease)
    run.draining, run.finish_by = True, time.time() + 600  # its session ended: finishing its queue
    first = manager._current
    os.killpg(first.pid, signal.SIGKILL)
    _wait(lambda: run._moved is not None, 60)
    assert run._moved.pid != first.pid
    assert run._moved.spec["draining"] is True and run._moved.spec["finish_by"] == run.finish_by
    _wait(lambda: run.poll() is not None)
    assert run.poll() == 0  # a draining run with an empty queue ends


def test_the_tools_a_dead_hosts_runs_left_are_ended(manager, tmp_path):
    from probe.service import procid

    child = subprocess.Popen(["sleep", "300"], start_new_session=True)
    try:
        folder = daemonhost.folder()
        folder.mkdir(parents=True, exist_ok=True)
        dead_host_pid = 999_999
        (folder / f"host-children-{dead_host_pid}.json").write_text(json.dumps(
            {"pid": dead_host_pid, "children": {str(child.pid): {"sid": "s", "start": procid.start_time(child.pid)}}}))

        class Dead:
            pid = dead_host_pid

        manager._end_children(Dead())
        assert child.wait(timeout=10) is not None
    finally:
        if child.poll() is None:
            child.kill()


def test_a_worker_process_the_service_starts_itself_is_never_sent_back_to_the_host():
    assert proxy_mod.eligible({})
    assert not proxy_mod.eligible({worker_mod.SUPERVISOR_PID_ENV: "{}"})
    assert not proxy_mod.eligible({worker_mod.ENTER_CWD_ENV: "1"})
    assert not proxy_mod.eligible({daemonhost.KILL_ENV: "off"})


def test_an_old_taps_worker_runs_in_the_host_and_exits_with_its_runs_code(manager, tmp_path):
    s = Session(tmp_path, "old-tap")
    address = manager.address()
    script = textwrap.dedent(f"""
        import sys
        from probe.daemon import proxy
        proxy._address = lambda: {address!r}
        code = proxy.main(sys.argv[1:])
        print("PROXY", code, flush=True)
        sys.exit(99 if code is None else code)
    """)
    env = {**s.env}
    proc = subprocess.Popen([sys.executable, "-c", script, "--session-id", s.sid, "--transcript", str(s.transcript),
                             "--cwd", str(s.project)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True)
    try:
        lease = _wait(s.lease, 60)
        assert lease["pid"] == address["pid"]  # the work is the host's, not this process's
        s.switch("off")
        out, err = proc.communicate(timeout=60)
        assert proc.returncode == 0, (out, err)
        assert "runs in the daemon host" in err
    finally:
        if proc.poll() is None:
            proc.kill()


def test_the_proxy_stops_its_run_on_sigterm(manager, tmp_path):
    s = Session(tmp_path, "old-tap")
    address = manager.address()
    script = textwrap.dedent(f"""
        import sys
        from probe.daemon import proxy
        proxy._address = lambda: {address!r}
        sys.exit(proxy.main(sys.argv[1:]))
    """)
    proc = subprocess.Popen([sys.executable, "-c", script, "--session-id", s.sid, "--transcript", str(s.transcript),
                             "--cwd", str(s.project)], env=s.env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        _wait(s.lease, 60)
        proc.send_signal(signal.SIGTERM)  # the old tap's stop(): finish the queue (empty here) and exit
        assert proc.wait(timeout=60) == 0
        assert s.lease()["reason"] == "stopped"
    finally:
        if proc.poll() is None:
            proc.kill()


def test_a_proxied_run_whose_host_dies_under_it_exits_crashed(manager, tmp_path):
    """The old tap backs the session off: a run that kills its host would else be
    started again at once and take every session down again (review of PR B)."""
    s = Session(tmp_path, "old-tap-crash")
    address = manager.address()
    script = textwrap.dedent(f"""
        import sys
        from probe.daemon import proxy
        proxy._address = lambda: {address!r}
        sys.exit(proxy.main(sys.argv[1:]))
    """)
    proc = subprocess.Popen([sys.executable, "-c", script, "--session-id", s.sid, "--transcript", str(s.transcript),
                             "--cwd", str(s.project)], env=s.env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        _wait(s.lease, 60)
        os.kill(address["pid"], signal.SIGKILL)  # the host dies with the run going
        assert proc.wait(timeout=60) == worker_mod.EXIT_CRASHED
    finally:
        if proc.poll() is None:
            proc.kill()


def test_the_service_supervises_a_hosted_run_like_a_worker_process(manager, tmp_path, monkeypatch):
    monkeypatch.setattr(workers_mod, "cli_python", lambda: sys.executable)
    s = Session(tmp_path, "s")
    host = workers_mod.WorkerHost(log=lambda m: None, daemon_host=manager)
    link = host.link(s.sid)
    switch = {"value": ("daemon", True)}
    assert link.supervise({**s.spec(), "switch": lambda: switch["value"]})
    _wait(lambda: any(r.get("host") and r["state"] == workers_mod.WorkerState.RUNNING for r in host.public()), 60)
    row = next(r for r in host.public() if r["sid"] == s.sid)
    assert row["pid"] == manager._current.pid
    assert host.host_runs() == 1
    link.release()  # its session ended: stopped, finishing its (empty) queue
    _wait(lambda: host.host_runs() == 0, 60)
    host.close()


def test_the_supervisor_starts_a_worker_process_when_the_host_is_unavailable(tmp_path, monkeypatch):
    class Broken:
        def available(self):
            return True

        def start(self, spec):
            raise daemonhost.HostUnavailable("broken for the test")

        def run_info(self, run):
            return {}

    started = []
    monkeypatch.setattr(workers_mod.subprocess, "Popen", lambda *a, **k: started.append(a) or _FakeChild())
    monkeypatch.setattr(workers_mod, "cli_python", lambda: sys.executable)
    s = Session(tmp_path, "s")
    spec = workers_mod.parse_spec({**s.spec(), "switch": lambda: ("daemon", True)})
    sup = workers_mod.Supervisor(spec, owner=None, host=Broken())
    sup._spawn(0.0)
    assert started and "worker" in started[0][0]  # `daemon worker`, its own process, as before
    assert sup.state == workers_mod.WorkerState.RUNNING


class _FakeChild:
    pid = 4242

    def poll(self):
        return None

    def send_signal(self, sig):
        pass


def test_the_updater_finds_a_hosted_run_by_its_hosts_command_line(manager, tmp_path):
    s = Session(tmp_path, "s")
    run = manager.start(s.spec())
    _wait(s.lease)
    assert updater_mod._is_worker(run.pid, s.sid)
    s.switch("off")
    _wait(lambda: run.poll() is not None)


def test_the_hosts_constants_are_the_services_and_the_workers():
    assert daemonhost.HOST_ENTRY == host_mod.ENTRY
    assert daemonhost.ARGV_MARK == host_mod.ARGV_MARK == updater_mod.DAEMON_HOST_MARK
    assert daemonhost.EXIT_CRASHED == worker_mod.EXIT_CRASHED
    assert proxy_mod.EXIT_CRASHED == worker_mod.EXIT_CRASHED
    assert daemonhost.FINISH_CAP_S == worker_mod.FINISH_CAP_S
    assert proxy_mod.SUPERVISOR_PID_ENV == worker_mod.SUPERVISOR_PID_ENV
    assert proxy_mod.ENTER_CWD_ENV == worker_mod.ENTER_CWD_ENV
    assert proxy_mod.KILL_ENV == daemonhost.KILL_ENV
    from probe.service import server

    assert proxy_mod.METHOD == server.DAEMON_HOST_METHOD


def test_the_host_is_off_with_its_switch(monkeypatch):
    monkeypatch.setenv(daemonhost.KILL_ENV, "off")
    assert not daemonhost.enabled()
    monkeypatch.delenv(daemonhost.KILL_ENV)
    assert daemonhost.enabled()
    daemonhost.folder().mkdir(parents=True, exist_ok=True)
    (daemonhost.folder() / daemonhost.OFF_FILE).write_text("")
    assert not daemonhost.enabled()


def _patched_python(tmp_path, body: str) -> Path:
    """A `python` for DaemonHost that runs the host with `body` patched in first."""
    patch_dir = tmp_path / "patch"
    patch_dir.mkdir(exist_ok=True)
    (patch_dir / "hostpatch.py").write_text(textwrap.dedent(body))
    wrapper = tmp_path / "python-patched"
    wrapper.write_text(textwrap.dedent(f"""\
        #!/bin/bash
        shift 3  # -I -c <entry>: replaced by the same entry with the patch first
        exec {sys.executable} -c 'import sys; sys.path.insert(0, "{patch_dir}"); import hostpatch; \\
        from probe.daemon.host import main; sys.exit(main(sys.argv[1:]))' "$@"
    """))
    wrapper.chmod(0o755)
    return wrapper


def test_a_run_that_raises_is_that_sessions_crash_and_the_others_keep_going(manager, tmp_path):
    a, b = Session(tmp_path, "raiser"), Session(tmp_path, "bystander")
    manager._python = lambda: str(_patched_python(tmp_path, f"""
        from probe.daemon import worker
        _tick = worker.Worker.tick
        async def tick(self):
            if self.session.session_id == {a.sid!r}:
                raise RuntimeError("a bug in this session's worker")
            return await _tick(self)
        worker.Worker.tick = tick
    """))
    run_a, run_b = manager.start(a.spec()), manager.start(b.spec())
    assert _wait(lambda: run_a.poll() is not None, 60) and run_a.poll() == worker_mod.EXIT_CRASHED
    assert a.lease()["reason"] == "error"  # it handed writing back, as a crashed worker process does
    first = (b.lease() or {}).get("renewed_at")
    _wait(lambda: (b.lease() or {}).get("renewed_at", 0) > (first or 0), 30)  # the other keeps renewing
    assert run_b.poll() is None and manager._current.popen.poll() is None
    b.switch("off")
    _wait(lambda: run_b.poll() is not None)


def test_a_run_that_hangs_stalls_only_itself(manager, tmp_path):
    a, b = Session(tmp_path, "hanger"), Session(tmp_path, "bystander")
    manager._python = lambda: str(_patched_python(tmp_path, f"""
        import time
        from probe.daemon import worker
        _tick = worker.Worker.tick
        async def tick(self):
            if self.session.session_id == {a.sid!r}:
                time.sleep(3600)  # a blocking call on its own thread: a hung mount, say
            return await _tick(self)
        worker.Worker.tick = tick
    """))
    hung, run_b = manager.start(a.spec()), manager.start(b.spec())
    _wait(lambda: b.lease(), 60)

    def stuck_beside_a_live_one():
        rows = {row["sid"]: row for row in (manager._current.beat or {}).get("runs") or []}
        if a.sid not in rows or b.sid not in rows:
            return None
        hung_age, live_age = rows[a.sid]["tick_age_s"], rows[b.sid]["tick_age_s"]
        return (hung_age is None or hung_age > 15) and live_age is not None and live_age < 5

    _wait(stuck_beside_a_live_one, 60)  # one run stuck in its poll, the other still polling
    b.switch("off")
    assert _wait(lambda: run_b.poll() is not None, 60) and run_b.poll() == 0
    assert hung.poll() is None  # still stuck: only the host's replacement or kill ends it


def _tick_age(manager, sid):
    rows = (manager._current.beat or {}).get("runs") or [] if manager._current is not None else []
    ages = [r.get("tick_age_s") or 0 for r in rows if r.get("sid") == sid]
    return max(ages) if ages else 0


def test_an_idle_hosted_run_wakes_when_its_files_change(manager, tmp_path):
    s = Session(tmp_path, "idle")
    spec = s.spec()
    # Idle after 1 s; without a poke it would next look in 120 s.
    spec["env"] = {**spec["env"], worker_mod.IDLE_AFTER_ENV: "1", worker_mod.IDLE_POLL_ENV: "120"}
    run = manager.start(spec)
    _wait(s.lease, 60)
    _wait(lambda: _tick_age(manager, s.sid) > 6, 60)  # idle for real: no look in 6 s (busy: one every 2 s)
    switched = time.monotonic()
    s.switch("off")  # the watcher sees the switch file change and pokes the run
    _wait(lambda: run.poll() is not None, 30)
    assert time.monotonic() - switched < 10


def test_an_idle_hosted_run_stops_at_once_when_asked(manager, tmp_path):
    """A stop (the session ended, an update's hand-over) wakes an idle run's wait:
    it never waits out IDLE_POLL_S (a worker process looks every 2 s)."""
    s = Session(tmp_path, "idle-stop")
    spec = s.spec()
    spec["env"] = {**spec["env"], worker_mod.IDLE_AFTER_ENV: "1", worker_mod.IDLE_POLL_ENV: "120"}
    run = manager.start(spec)
    _wait(s.lease, 60)
    time.sleep(6)  # idle now: waiting up to 120 s
    asked = time.monotonic()
    run.send_signal(signal.SIGTERM)
    _wait(lambda: run.poll() is not None, 60)
    assert time.monotonic() - asked < 15
