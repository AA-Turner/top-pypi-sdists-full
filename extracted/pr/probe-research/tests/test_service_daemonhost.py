"""The service's side of the daemon host, without starting one (plan
daemon-in-service): what must never wait on a host starting, and how a hosted
run is stopped for an update -- never by signalling the host, which runs every
session's worker."""

from __future__ import annotations

import asyncio
import json
import os
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe.daemon import runctx
from probe.service import daemonhost
from probe.service import updater as updater_mod
from probe.service import workers as workers_mod

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the daemon host is POSIX only")


def _fake_proc(pid: int = 4242):
    return SimpleNamespace(pid=pid, dead=False, retired_at=None, popen=SimpleNamespace(poll=lambda: None),
                           live_runs=lambda: [], last_beat=time.monotonic(), rss_mb=None)


def test_a_host_starting_never_holds_up_the_status_read():
    """`service.status` reads `public()` on the service's loop: a host start (up to
    START_TIMEOUT_S) under the same lock made the update guard's status call fail
    and the update roll back (live test, 2026-10-25)."""
    host = daemonhost.DaemonHost(log=lambda line: None)
    entered, release, spawns = threading.Event(), threading.Event(), []

    def slow_spawn():
        spawns.append(1)
        entered.set()
        release.wait(10)
        return _fake_proc()

    host._spawn = slow_spawn
    got: list = []
    first = threading.Thread(target=lambda: got.append(host._ensure()))
    first.start()
    assert entered.wait(5)
    second = threading.Thread(target=lambda: got.append(host._ensure()))  # a second run's start meanwhile
    second.start()
    started = time.monotonic()
    view = host.public()
    assert time.monotonic() - started < 1.0 and view["pid"] is None
    release.set()
    first.join(5)
    second.join(5)
    assert spawns == [1] and len(got) == 2 and got[0] is got[1]
    assert host.public()["pid"] == 4242


def test_a_failed_host_start_lets_the_next_caller_try():
    host = daemonhost.DaemonHost(log=lambda line: None)
    calls = []

    def spawn():
        calls.append(1)
        if len(calls) == 1:
            raise daemonhost.HostUnavailable("would not start")
        return _fake_proc()

    host._spawn = spawn
    with pytest.raises(daemonhost.HostUnavailable):
        host._ensure()
    assert host._ensure().pid == 4242 and len(calls) == 2


def _a_process_named(*words: str) -> subprocess.Popen:
    """A process whose command line carries `words`, readable before it returns:
    right after a vfork'd exec, `/proc/<pid>/cmdline` reads empty for a moment
    (124 of 300 spawns on 3.11, 2026-10-26), and a check that read it then took
    the host for a plain process (agent-ci 3.11 shard flake)."""
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)", *words],
                            stdin=subprocess.DEVNULL, env=dict(os.environ))
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            if words[0].encode() in Path(f"/proc/{proc.pid}/cmdline").read_bytes().split(b"\0"):
                break
        except OSError:
            break  # no /proc (macOS): `ps`, which reads it later, answers there
        time.sleep(0.01)
    return proc


def test_the_update_stops_a_hosted_run_through_the_host_never_by_signalling_it(tmp_path):
    """The D7 hand-over SIGTERMed each worker's pid, which for a hosted run is the
    host's: five sessions, five SIGTERMs to the one process running them all
    (live test, 2026-10-25: the host stopped beating and was killed with its runs)."""
    host = _a_process_named("daemon-host", "--folder", str(tmp_path))
    try:
        stopped: list[str] = []
        u = updater_mod.Updater(version="0.1.0", emit=lambda *a: None, changed=lambda: None, stop=lambda r: None,
                                action_running=lambda: False, discovering=lambda: False,
                                stop_hosted=lambda sid: stopped.append(sid) or True)
        sids = ["s1", "s2", "s3"]
        workers = [updater_mod.Worker(sid=sid, lock=tmp_path / f"{sid}.lock", pid=host.pid) for sid in sids]
        left = asyncio.run(u._stop_workers(workers))
        assert left == [] and stopped == sids
        time.sleep(0.2)
        assert host.poll() is None, "the host was signalled"
        assert all(w.handover.exists() is False for w in workers)  # withdrawn after the wait, as for a process
    finally:
        host.kill()
        host.wait()


def test_a_switch_back_never_signals_the_host(tmp_path, monkeypatch):
    host = _a_process_named("daemon-host", "--folder", str(tmp_path))
    try:
        worker = updater_mod.Worker(sid="s1", lock=tmp_path / "s1.lock", pid=host.pid)
        monkeypatch.setattr(updater_mod, "live_workers", lambda dirs: [worker])
        monkeypatch.setattr(updater_mod, "_parent_is_service", lambda pid: True)  # a live service's host
        assert updater_mod.hand_over_workers([tmp_path]) == 1
        time.sleep(0.2)
        assert host.poll() is None, "the host was signalled"
        assert worker.handover.stat().st_mtime > time.time()  # dated ahead: the run hands over on it
    finally:
        host.kill()
        host.wait()


def test_stopping_one_hosted_run_signals_that_run_only():
    sent: list = []
    run = SimpleNamespace(run_id="r1", returncode=None, request_stop=lambda: sent.append(("r1", signal.SIGTERM)))
    other = SimpleNamespace(run_id="r2", returncode=None, request_stop=lambda: sent.append(("r2", signal.SIGTERM)))
    process = SimpleNamespace(returncode=None, send_signal=lambda sig: sent.append(("process", sig)))
    wh = workers_mod.WorkerHost(log=lambda line: None)
    wh._sessions["s1"] = SimpleNamespace(child=run)
    wh._sessions["s2"] = SimpleNamespace(child=other)
    wh._sessions["s3"] = SimpleNamespace(child=process)  # a worker process: the updater signals it itself
    assert wh.stop_hosted("s1") is True and sent == [("r1", signal.SIGTERM)]
    assert wh.stop_hosted("s3") is False and wh.stop_hosted("nobody") is False


def test_the_hosts_stop_signal_never_waits_on_its_lock():
    """The host's SIGTERM handler runs on its control thread, which it may have
    interrupted inside the host's lock: it only asks, the control loop stops."""
    from probe.daemon import host as host_mod

    folder = Path(tempfile.mkdtemp(prefix="pdh", dir="/tmp"))
    host = host_mod.Host(folder, folder / "h.sock")
    host.bind()
    with host.lock:
        host.signalled()  # would block for good if it took the lock
    assert host._stop_asked and not host.stopping
    out: list = []
    serve = threading.Thread(target=lambda: out.append(host.serve()), daemon=True)
    serve.start()
    serve.join(10)
    assert out == [0] and host.stopping


# -- the service's decisions about a host, with fake hosts (review of PR B) -----------


def _proc(pid: int = 4242, *, runs: int = 0, beat_age: float = 0.0, retired_age: float | None = None):
    """A real `_Proc` over a socket pair (the far end stands in for the host)."""
    near, far = socket.socketpair()
    popen = SimpleNamespace(pid=pid, poll=lambda: None, kill=lambda: None, wait=lambda timeout=None: 0)
    proc = daemonhost._Proc(popen, near)
    proc.far = far
    proc.last_beat = time.monotonic() - beat_age
    if retired_age is not None:
        proc.retired_at = time.monotonic() - retired_age
    for i in range(runs):
        run = daemonhost.HostedRun(proc, f"r{i}", {"sid": f"s{i}", "daemon_dir": "/nowhere"})
        proc.runs[run.run_id] = run
    return proc


def _host(monkeypatch, tmp_path):
    seen: dict = {"killed": [], "incidents": [], "log": []}
    host = daemonhost.DaemonHost(log=seen["log"].append,
                                 incident=lambda family, reason, *a, **k: seen["incidents"].append(reason))
    monkeypatch.setattr(host, "_kill", seen["killed"].append)
    monkeypatch.setattr(host, "_later", lambda fn, *a, **k: fn(*a, **k))  # off the reader's thread, in order here
    monkeypatch.setattr(daemonhost, "folder", lambda: tmp_path)
    return host, seen


def test_a_send_to_a_host_that_stopped_reading_never_holds_up_a_status_read(monkeypatch):
    """A host that stops reading with a big message going out (a start carries the
    session's whole environment): the send gives up within SEND_TIMEOUT_S, a status
    read never waits behind it, and the next look kills the host."""
    monkeypatch.setattr(daemonhost, "SEND_TIMEOUT_S", 1.0)
    proc = _proc(runs=1)
    big = {"op": "start", "env": {"X": "y" * 4_000_000}}
    done: list = []
    # A daemon thread: a send that never gives up fails here, not by holding the
    # interpreter open past the summary until the job's timeout cancels it.
    sender = threading.Thread(target=lambda: done.append(proc.send(big)), daemon=True)
    sender.start()
    time.sleep(0.2)
    started = time.monotonic()
    assert len(proc.live_runs()) == 1 and time.monotonic() - started < 0.5
    sender.join(10)
    assert done == [False] and proc.stuck


def test_a_send_gives_up_where_the_kernel_ignores_dontwait(monkeypatch):
    """macOS's send() does not honour MSG_DONTWAIT (agent-ci service-macos: the
    send above never returned): the socket's own send timeout still bounds it."""
    monkeypatch.setattr(daemonhost, "SEND_TIMEOUT_S", 1.0)
    monkeypatch.setattr(daemonhost.socket, "MSG_DONTWAIT", 0)  # a blocking send, as there
    proc = _proc(runs=1)
    done: list = []
    sender = threading.Thread(target=lambda: done.append(proc.send({"env": "y" * 4_000_000})), daemon=True)
    started = time.monotonic()
    sender.start()
    sender.join(10)
    assert done == [False] and proc.stuck and time.monotonic() - started < 5


def test_poll_kills_a_stuck_or_silent_host_and_one_past_its_retired_cap(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    silent = _proc(1, runs=1, beat_age=daemonhost.HUNG_S + 1)
    quiet_idle = _proc(2, runs=0, beat_age=daemonhost.HUNG_S + 1)  # no run: nothing to hang
    stuck = _proc(3, runs=1)
    stuck.stuck = True
    overdue = _proc(4, retired_age=daemonhost.RETIRED_CAP_S + 1)
    host._current = silent
    host._retired = [quiet_idle, stuck, overdue]
    host.poll()
    assert seen["killed"] == [silent, stuck, overdue] and seen["incidents"].count("host_hung") == 2


def test_a_host_over_its_memory_budget_is_replaced_at_most_once_per_gap(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    proc = _proc(runs=2)
    host._current = proc
    replaced: list = []
    monkeypatch.setattr(host, "replace", lambda reason, **k: replaced.append(reason))
    monkeypatch.setattr(daemonhost, "_rss_mb", lambda pid: 10_000.0)
    host._on_message(proc, {"op": "beat"})
    proc.rss_at = 0.0  # look again at once
    host._replaced_at = time.monotonic()  # as the first replace stamps it
    host._on_message(proc, {"op": "beat"})
    assert len(replaced) == 1
    retired = _proc(5, runs=2, retired_age=1)
    host._on_message(retired, {"op": "beat"})  # only the current host is measured
    assert len(replaced) == 1


def test_a_stale_answer_replaces_only_the_host_that_gave_it(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    old, new = _proc(1, runs=1), _proc(2, runs=1)
    old.retired_at = time.monotonic()
    host._retired, host._current = [old], new
    host._on_message(old, {"op": "exited", "run": "r0", "code": 0, "reason": "stale"})
    assert new.retired_at is None and host._current is new
    assert "r0" not in old.runs  # an exited run leaves the host's map
    host._on_message(new, {"op": "exited", "run": "r0", "code": 0, "reason": "retiring"})
    assert new.retired_at is not None  # the current host takes no new run (signalled): a new one takes the next
    other = _proc(3, runs=1)
    host._current = other
    host._on_message(other, {"op": "exited", "run": "r0", "code": 0, "reason": "stale"})
    assert other.retired_at is not None and host._current is None


def test_the_second_unattributed_host_death_backs_every_run_off(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    monkeypatch.setattr(host, "_end_children", lambda proc: None)
    first = _proc(1, runs=1)
    first.popen.poll = lambda: -9
    host._died(first)
    assert first.runs["r0"].poll() == 0  # started again at once
    second = _proc(2, runs=1)
    second.popen.poll = lambda: -9
    host._died(second)
    assert second.runs["r0"].poll() == daemonhost.EXIT_CRASHED  # twice in the window: every run backs off


def test_a_crash_is_read_from_the_dead_hosts_own_files_and_they_go(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    monkeypatch.setattr(host, "_end_children", lambda proc: None)
    dead, beside = _proc(11, runs=2), _proc(12, runs=1)
    (tmp_path / "host-crash-11.log").write_bytes(b"Fatal Python error\nCurrent thread 0x00000000000000ab (most recent call first):\n")
    (tmp_path / "host-threads-11.json").write_text(json.dumps({"pid": 11, "threads": {hex(0xab): "s1"}}))
    (tmp_path / "host-threads-12.json").write_text(json.dumps({"pid": 12, "threads": {hex(0xab): "s0"}}))
    dead.popen.poll = lambda: -11
    host._died(dead)
    assert dead.runs["r1"].poll() == daemonhost.EXIT_CRASHED and dead.runs["r0"].poll() == 0
    assert not (tmp_path / "host-crash-11.log").exists() and not (tmp_path / "host-threads-11.json").exists()
    assert (tmp_path / "host-threads-12.json").exists()  # the other host's own


def test_a_draining_run_moves_only_after_the_others_have_ended(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    monkeypatch.setattr(host, "_end_children", lambda proc: None)
    proc = _proc(1, runs=2)
    proc.runs["r1"].draining, proc.runs["r1"].finish_by = True, time.time() + 600
    order: list = []
    monkeypatch.setattr(host, "_move_draining", lambda run: order.append(("move", proc.runs["r0"].poll())))
    proc.popen.poll = lambda: -9
    host._died(proc)
    assert order == [("move", 0)]


def test_an_old_taps_run_is_stopped_through_the_host_and_its_draining_read_from_the_beat(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    proc = _proc(1)
    host._current = proc
    proc.beat = {"runs": [{"run": "x", "sid": "old-tap", "draining": False},
                          {"run": "y", "sid": "ended", "draining": True}]}
    assert host.session_draining("old-tap") is False and host.session_draining("ended") is True
    assert host.session_draining("unknown") is None
    wh = workers_mod.WorkerHost(log=lambda line: None, daemon_host=host)
    assert wh.stop_hosted("old-tap") is True  # no Supervisor here: the host is asked by session
    assert json.loads(proc.far.recv(65536).decode().splitlines()[0]) == {"op": "stop", "sid": "old-tap"}


def test_the_update_counts_an_old_taps_hosted_run_as_live(tmp_path, monkeypatch):
    """An old tap's worker runs in the host now (the service's child): no recorder
    here, so the recorder rule alone would call it draining and defer every update
    for that session's life."""
    host = _a_process_named("daemon-host", "--folder", str(tmp_path))
    try:
        from probe.service import procid

        monkeypatch.setattr(procid, "proc", lambda pid: SimpleNamespace(ppid=os.getpid()))
        updater_mod.set_hosted(lambda sid: False, lambda sid: {"old-tap": False, "ended": True}.get(sid))
        assert updater_mod._session_ended(host.pid, "old-tap") is False
        assert updater_mod._session_ended(host.pid, "ended") is True
        assert updater_mod._session_ended(host.pid, "unknown") is True  # no beat word: the recorder's (none)
    finally:
        updater_mod.set_hosted(None)
        host.kill()
        host.wait()


# -- the host's own rules (review of PR B) ----------------------------------------


def _bare_host():
    from probe.daemon import host as host_mod

    folder = Path(tempfile.mkdtemp(prefix="pdh", dir="/tmp"))
    return host_mod, host_mod.Host(folder, folder / "h.sock")


class _FakeConn:
    def __init__(self, role, runs=()):
        self.role, self.runs, self.sent, self.closed = role, set(runs), [], False

    def send(self, obj):
        self.sent.append(obj)
        return True


def test_only_a_runs_owner_or_the_service_stops_it_and_a_proxy_sees_only_its_own():
    host_mod, host = _bare_host()
    asked: list = []
    owner, other, service = _FakeConn("proxy", {"r1"}), _FakeConn("proxy", {"r2"}), _FakeConn("service")
    for rid, sid, conn in (("r1", "s1", owner), ("r2", "s2", other)):
        host.runs[rid] = SimpleNamespace(run_id=rid, sid=sid, owner=conn, draining=False, worker=None, ticked_at=0,
                                         cpu_s=0.0, started_at=time.monotonic(),
                                         stopper=SimpleNamespace(request=lambda rid=rid: asked.append(rid)))
    host._handle(other, {"op": "stop", "run": "r1"})
    host._handle(other, {"op": "stop", "sid": "s1"})  # by session: the service's alone
    host._handle(other, {"op": "retire"})
    assert asked == [] and not host.retiring
    host._handle(owner, {"op": "stop", "run": "r1"})
    host._handle(service, {"op": "stop", "sid": "s2"})
    assert asked == ["r1", "r2"]
    host._handle(other, {"op": "status"})
    assert [r["run"] for r in other.sent[-1]["runs"]] == ["r2"]
    host._handle(service, {"op": "status"})
    assert sorted(r["run"] for r in service.sent[-1]["runs"]) == ["r1", "r2"]


def test_a_connection_a_send_failed_on_is_closed_and_its_runs_owner_is_gone():
    host_mod, host = _bare_host()
    near, far = socket.socketpair()
    far.close()
    woke: list = []
    conn = host_mod.Conn(sock=near, peer_pid=None, role="service", on_broken=lambda: woke.append(1))
    host.conns.add(conn)
    run = SimpleNamespace(run_id="r1", owner_gone=False)
    host.runs["r1"] = run
    conn.runs.add("r1")
    assert conn.send({"op": "beat", "x": "y" * 300_000}) is False and woke == [1]
    host.bind()
    serve = threading.Thread(target=host.serve, daemon=True)
    serve.start()
    deadline = time.monotonic() + 5
    while not run.owner_gone and time.monotonic() < deadline:
        time.sleep(0.05)
    host.runs.clear()
    host.signalled()  # no run left: the control loop stops
    serve.join(5)
    assert run.owner_gone and conn not in host.conns


def test_a_hosted_runs_session_log_is_private_and_never_followed_through_a_symlink(tmp_path, monkeypatch):
    from probe.daemon import host as host_mod

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    daemon_dir = tmp_path / "daemon"
    handlers = host_mod.run_handlers("s1", daemon_dir, "INFO")
    try:
        assert (daemon_dir / "s1.log").stat().st_mode & 0o777 == 0o600
    finally:
        for h in handlers:
            h.close()
    (daemon_dir / "s2.log").symlink_to(tmp_path / "elsewhere.log")
    handlers = host_mod.run_handlers("s2", daemon_dir, "INFO")
    try:
        assert not (tmp_path / "elsewhere.log").exists()  # not opened through the link
    finally:
        for h in handlers:
            h.close()


def test_the_hosts_state_files_are_whole_however_many_threads_write_them():
    host_mod, host = _bare_host()
    host.folder.mkdir(parents=True, exist_ok=True)

    def churn(n):
        for i in range(200):
            host.note_thread(f"s{n}")
            host.note_child(f"s{n}", os.getpid())
            host.forget_child(os.getpid())

    threads = [threading.Thread(target=churn, args=(n,)) for n in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(30)
    assert json.loads(host.threads_path.read_text())["pid"] == os.getpid()
    assert json.loads(host.children_path.read_text())["children"] == {}
    assert host.threads_path.name == f"host-threads-{os.getpid()}.json"


def test_the_host_socket_is_never_trusted_in_a_folder_others_can_write(tmp_path):
    """The /tmp fallback: a folder another local user made first (or a link to
    one) is never served in, and a listener there is never trusted."""
    shared = tmp_path / "shared"
    shared.mkdir()
    os.chmod(shared, 0o777)
    assert daemonhost.DaemonHost._connect(shared / "h.sock", 1) is None
    from probe.daemon import host as host_mod

    (tmp_path / "link").symlink_to(shared)
    with pytest.raises(OSError):
        host_mod.Host(tmp_path / "f", tmp_path / "link" / "h.sock").bind()


def _stale_spec(tmp_path, monkeypatch, cli_source="0" * 64):
    """A shipped spec older than the CLI, the copies kept under tmp_path, nothing tried yet."""
    import sys as _sys

    from probe.daemon import cli_spec

    cache = tmp_path / "cache"
    monkeypatch.setattr(cli_spec, "_cache_path", lambda sha: cache / f"{sha[:24]}.json")
    monkeypatch.setattr(cli_spec, "_TRIED", set())
    monkeypatch.delitem(_sys.modules, "probe.cli.main", raising=False)  # as in the daemon: the CLI not loaded
    spec = json.loads(cli_spec.SPEC_PATH.read_text())
    stale = tmp_path / "cli_spec.json"
    stale.write_text(json.dumps({**spec, "cli_source": cli_source}))
    return cli_spec, cache, stale, spec


def test_a_spec_made_from_another_cli_source_is_never_used(tmp_path, monkeypatch):
    cli_spec, cache, stale, spec = _stale_spec(tmp_path, monkeypatch)
    assert cli_spec.load(cli_spec.SPEC_PATH) is not None  # the shipped one matches this CLI
    monkeypatch.setattr(cli_spec, "_generate", lambda target: "none can be written")
    assert cli_spec.load(stale) is None  # the CLI's own tree is built instead: no command refused


def test_a_stale_spec_is_replaced_once_per_cli_by_one_a_child_writes(tmp_path, monkeypatch):
    """Any edit to the CLI's source makes the shipped spec older than it: the
    daemon then has one written for this CLI, once, by a short-lived child (the
    whole CLI is imported there, never in the daemon), and reads that after."""
    import sys as _sys

    cli_spec, cache, stale, spec = _stale_spec(tmp_path, monkeypatch)
    cache.mkdir()
    old = cache / "an-earlier-cli.json"
    old.write_text("{}")
    os.utime(old, (time.time() - cli_spec.CACHE_KEEP_S - 60,) * 2)
    recent = cache / "another-install.json"  # a second install sharing the folder: kept
    recent.write_text("{}")
    real, children = cli_spec._generate, []
    monkeypatch.setattr(cli_spec, "_generate", lambda target: children.append(target) or real(target))
    tree = cli_spec.load(stale)
    assert tree is not None and "run" in tree.commands and len(children) == 1
    assert json.loads(children[0].read_text())["cli_source"] == cli_spec.source_sha()
    assert "probe.cli.main" not in _sys.modules  # imported in the child only
    assert cli_spec.load(stale) is not None and len(children) == 1  # read from the copy: no second child
    assert not old.exists() and recent.exists()


def test_the_spec_writing_child_never_imports_what_the_cache_folder_or_a_session_holds(tmp_path, monkeypatch):
    """The cache folder is writable; a session's PYTHONPATH may name a research
    repo with a `probe` package of its own: neither is imported by the child."""
    cli_spec, cache, stale, spec = _stale_spec(tmp_path, monkeypatch)
    marker = tmp_path / "planted-ran"
    for folder in (cache / "probe", tmp_path / "repo" / "probe"):
        folder.mkdir(parents=True)
        (folder / "__init__.py").write_text(f"open({str(marker)!r}, 'w').write('ran')\n")
    from probe.daemon import runctx

    run = runctx.Run("s1", env={**os.environ, "PYTHONPATH": str(tmp_path / "repo")})
    environ = runctx.install()
    try:
        with runctx.enter(run):
            assert cli_spec.load(stale) is not None
    finally:
        runctx.uninstall()
    assert not marker.exists()


def test_a_child_that_writes_another_clis_spec_counts_as_none_and_deletes_nothing(tmp_path, monkeypatch):
    cli_spec, cache, stale, spec = _stale_spec(tmp_path, monkeypatch)
    cache.mkdir()
    keep = cache / ("f" * 24 + ".json")
    keep.write_text(json.dumps({**spec, "cli_source": "f" * 64}))
    os.utime(keep, (time.time() - cli_spec.CACHE_KEEP_S - 60,) * 2)
    monkeypatch.setattr(cli_spec, "_generate",
                        lambda target: target.write_text(json.dumps({**spec, "cli_source": "f" * 64})))
    assert cli_spec.load(stale) is None and keep.exists()


def test_one_failed_child_per_process_however_many_runs_ask(tmp_path, monkeypatch):
    cli_spec, cache, stale, spec = _stale_spec(tmp_path, monkeypatch)
    children: list = []
    monkeypatch.setattr(cli_spec, "_generate", lambda target: children.append(1) or time.sleep(0.2) or "failed")
    threads = [threading.Thread(target=cli_spec.load, args=(stale,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(10)
    assert children == [1]


def test_no_child_when_the_whole_cli_is_loaded_already(tmp_path, monkeypatch):
    import sys as _sys

    cli_spec, cache, stale, spec = _stale_spec(tmp_path, monkeypatch)
    monkeypatch.setitem(_sys.modules, "probe.cli.main", _sys.modules.get("probe.cli.main") or object())
    monkeypatch.setattr(cli_spec, "_generate", lambda target: pytest.fail("a child for a CLI already loaded"))
    assert cli_spec.load(stale) is None  # its own tree costs nothing there


# -- the second review of PR B: old taps' runs, silence, starts, retire ---------------


def test_a_start_with_no_answer_is_that_starts_fallback_never_the_hosts_kill(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    monkeypatch.setattr(daemonhost, "ACK_TIMEOUT_S", 0.2)
    proc = _proc(1)
    monkeypatch.setattr(host, "_ensure", lambda: proc)
    spec = {"sid": "s1", "transcript": "/t", "cwd": "/c", "source": "claude_code", "daemon_dir": "/d", "env": {}}
    with pytest.raises(daemonhost.HostUnavailable):
        host.start(spec)  # the Supervisor runs this session's worker as a process
    assert seen["killed"] == [] and proc.runs == {}
    with pytest.raises(daemonhost.HostUnavailable):
        host.start({**spec, "env": {"BIG": "x" * daemonhost.MAX_LINE}})  # never sent: the host would close on it


def test_an_invalid_answer_is_a_fallback_too(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    proc = _proc(1)
    monkeypatch.setattr(host, "_ensure", lambda: proc)

    def answer():
        line = proc.far.recv(65536).decode().splitlines()[0]
        rid = json.loads(line)["run"]
        host._on_message(proc, {"op": "exited", "run": rid, "code": 2, "reason": "invalid"})

    t = threading.Thread(target=answer)
    t.start()
    with pytest.raises(daemonhost.HostUnavailable):
        host.start({"sid": "s1", "transcript": "/t", "cwd": "/c", "source": "claude_code", "daemon_dir": "/d",
                    "env": {}})
    t.join(5)


def test_a_host_that_says_it_takes_no_new_run_is_replaced(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    proc = _proc(1, runs=1)
    host._current = proc
    host._on_message(proc, {"op": "beat", "retiring": True, "runs": []})
    assert proc.retired_at is not None and host._current is None
    assert json.loads(proc.far.recv(65536).decode().splitlines()[-1])["op"] == "retire"


def test_a_host_that_goes_silent_again_and_again_backs_every_run_off(monkeypatch, tmp_path):
    """Nobody can tell which run held the GIL (a run stuck mid-tick has a frozen CPU
    figure): a repeating hang backs every run off rather than restarting them all
    every HUNG_S for good. The service's own kill of a host that closed its
    connection is not counted."""
    host, seen = _host(monkeypatch, tmp_path)
    monkeypatch.setattr(host, "_end_children", lambda proc: None)
    codes = []
    for pid in (1, 2):
        proc = _proc(pid, runs=1, beat_age=daemonhost.HUNG_S + 1)
        host._current, host._retired = proc, []
        host.poll()
        host.poll()  # a second look (the other thread) never kills or reports it twice
        proc.popen.poll = lambda: -9
        host._died(proc)
        codes.append(proc.runs["r0"].poll())
    assert codes == [0, daemonhost.EXIT_CRASHED] and seen["incidents"].count("host_hung") == 2
    assert len(seen["killed"]) == 2
    host._unattributed = []
    closed = _proc(3, runs=1)
    closed.killed_by_service = True
    closed.popen.poll = lambda: -9
    host._died(closed)
    assert host._unattributed == []


def test_an_old_taps_runs_count_for_the_hung_kill_the_budget_and_the_services_stay(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    proc = _proc(1, runs=0, beat_age=daemonhost.HUNG_S + 1)
    proc.beat = {"runs": [{"run": "x", "sid": "old-tap", "draining": False}]}  # started through the proxy
    host._current = proc
    assert host.runs() == 1
    host.poll()
    assert seen["killed"] == [proc]


def test_the_reader_outlives_a_bad_message_and_a_closed_connection_means_a_dead_host(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    proc = _proc(1, runs=1)
    alive = {"v": True}
    proc.popen.poll = lambda: None if alive["v"] else -9
    proc.popen.wait = lambda timeout=None: (_ for _ in ()).throw(subprocess.TimeoutExpired("h", timeout))
    monkeypatch.setattr(host, "_kill", lambda p: (seen["killed"].append(p), alive.__setitem__("v", False)))
    monkeypatch.setattr(host, "_end_children", lambda p: None)
    monkeypatch.setattr(host, "_on_message", lambda p, m: (_ for _ in ()).throw(ValueError("a bug")))
    proc.far.sendall(b'{"op":"beat"}\n')
    proc.far.close()
    host._read(proc)
    assert seen["killed"] == [proc] and proc.dead and proc.runs["r0"].poll() is not None


def test_the_services_watchdog_looks_at_its_hosts_without_any_supervisor(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    monkeypatch.setattr(daemonhost, "WATCH_S", 0.05)
    polled: list = []
    monkeypatch.setattr(host, "poll", lambda: polled.append(1))
    host._current = _proc(1)
    # Held here too: the watchdog clears `host._watchdog` itself as it ends, which
    # it may do (WATCH_S later) before this thread reaches the join.
    watchdog = host._watchdog = threading.Thread(target=host._watch, daemon=True)
    watchdog.start()
    time.sleep(0.3)
    host._current = None
    watchdog.join(2)
    assert len(polled) >= 2 and host._watchdog is None


def test_a_stopping_service_starts_no_host(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    host.close()
    with pytest.raises(daemonhost.HostUnavailable):
        host._ensure()


def test_an_update_stops_a_hosted_run_without_calling_it_a_sessions_end():
    sent: list = []
    proc = SimpleNamespace(send=lambda obj: sent.append(obj) or True, pid=1)
    run = daemonhost.HostedRun(proc, "r1", {"sid": "s1"})
    wh = workers_mod.WorkerHost(log=lambda line: None)
    wh._sessions["s1"] = SimpleNamespace(child=run)
    assert wh.stop_hosted("s1") is True
    assert sent == [{"op": "stop", "run": "r1"}] and run.draining is False  # a host death moves no live run


def test_a_host_its_service_left_is_live_for_the_update_and_signalled_for_its_hand_over(tmp_path, monkeypatch):
    host = _a_process_named("daemon-host", "--folder", str(tmp_path))
    try:
        from probe.service import procid

        monkeypatch.setattr(procid, "proc", lambda pid: SimpleNamespace(ppid=1))  # its service is gone
        monkeypatch.setattr(daemonhost, "folder", lambda: tmp_path)
        (tmp_path / f"host-runs-{host.pid}.json").write_text(json.dumps(
            {"pid": host.pid, "runs": [{"sid": "old-tap", "draining": False}, {"sid": "ended", "draining": True}]}))
        assert updater_mod._session_ended(host.pid, "old-tap") is False  # live: handed over
        assert updater_mod._session_ended(host.pid, "ended") is True  # finishing its queue: never handed over
        assert updater_mod._session_ended(host.pid, "unknown") is True  # no word: never handed over
        monkeypatch.setattr(updater_mod, "_host_owned_here", lambda pid: False)
        u = updater_mod.Updater(version="0.1.0", emit=lambda *a: None, changed=lambda: None, stop=lambda r: None,
                                action_running=lambda: False, discovering=lambda: False,
                                stop_hosted=lambda sid: pytest.fail("not this service's host"))
        asyncio.run(u._stop_workers([updater_mod.Worker(sid="s1", lock=tmp_path / "s1.lock", pid=host.pid)]))
        assert host.wait(timeout=10) == -signal.SIGTERM  # its SIGTERM hands every run over
    finally:
        if host.poll() is None:
            host.kill()
            host.wait()


def test_a_switch_back_signals_a_host_its_service_left(tmp_path, monkeypatch):
    host = _a_process_named("daemon-host", "--folder", str(tmp_path))
    try:
        worker = updater_mod.Worker(sid="s1", lock=tmp_path / "s1.lock", pid=host.pid)
        monkeypatch.setattr(updater_mod, "live_workers", lambda dirs: [worker])
        monkeypatch.setattr(updater_mod, "_parent_is_service", lambda pid: False)
        assert updater_mod.hand_over_workers([tmp_path]) == 1
        assert host.wait(timeout=10) == -signal.SIGTERM
    finally:
        if host.poll() is None:
            host.kill()
            host.wait()


def test_a_retired_or_signalled_host_hands_every_live_run_over():
    host_mod, host = _bare_host()
    stopped: list = []
    for rid, draining in (("r1", False), ("r2", True)):
        host.runs[rid] = SimpleNamespace(run_id=rid, sid=f"s-{rid}", draining=draining, worker=None,
                                         daemon_dir=host.folder / "daemon",
                                         stopper=SimpleNamespace(request=lambda rid=rid: stopped.append(rid)))
    until = time.time() + 120
    host.retire(handover_until=until)
    assert sorted(stopped) == ["r1", "r2"]
    marker = host.folder / "daemon" / "s-r1.handover"
    deadline = time.monotonic() + 5  # dated on a thread of its own, never the control thread
    while not marker.exists() and time.monotonic() < deadline:
        time.sleep(0.02)
    assert marker.stat().st_mtime == pytest.approx(until, abs=1)
    assert not (host.folder / "daemon" / "s-r2.handover").exists()  # finishing an ended session's queue: no hand-over


def test_only_the_hosts_parent_is_its_service():
    host_mod, host = _bare_host()
    stranger = _FakeConn("")
    stranger.peer_pid = os.getpid() + 1
    host._handle(stranger, {"op": "hello", "role": "service"})
    assert stranger.role == "proxy" and not host.had_owner
    parent = _FakeConn("")
    parent.peer_pid = os.getppid()
    host._handle(parent, {"op": "hello", "role": "service"})
    assert parent.role == "service" and host.had_owner


def test_a_proxied_start_the_host_refuses_runs_the_worker_in_process(tmp_path, monkeypatch):
    from probe.daemon import proxy

    folder = Path(tempfile.mkdtemp(prefix="pdh", dir="/tmp"))
    os.chmod(folder, 0o700)
    path = folder / "h.sock"
    listener = socket.socket(socket.AF_UNIX)
    listener.bind(str(path))
    listener.listen(1)

    def serve():
        conn, _ = listener.accept()
        f = conn.makefile("rwb")
        f.readline()
        f.write(json.dumps({"op": "hello", "pid": os.getpid()}).encode() + b"\n")
        f.flush()
        start = json.loads(f.readline())
        f.write(json.dumps({"op": "exited", "run": start["run"], "code": 0, "reason": "retiring"}).encode() + b"\n")
        f.flush()
        f.close()
        conn.close()

    t = threading.Thread(target=serve, daemon=True)
    t.start()
    monkeypatch.setattr(proxy, "_address", lambda: {"socket": str(path), "pid": os.getpid()})
    monkeypatch.setattr(proxy, "eligible", lambda env=None: True)
    out = proxy.main(["--session-id", "s1", "--transcript", str(tmp_path / "t.jsonl"), "--cwd", str(tmp_path)])
    t.join(5)
    listener.close()
    assert out is None  # the old tap's worker runs in-process: never an exit code it would respawn or give up on


def test_the_copied_constants_match():
    from probe.daemon import host as host_mod
    from probe.daemon import proxy
    from probe.daemon import worker as worker_mod
    from probe.service import recorders

    assert daemonhost.MAX_LINE == host_mod.MAX_LINE
    assert daemonhost.HANDOVER_AHEAD_S == host_mod.HANDOVER_AHEAD_S == recorders.HANDOVER_AHEAD_S
    args = worker_mod._parse_args(["--session-id", "s", "--transcript", "t", "--cwd", "c"])
    assert proxy._default_source() == args.source


def test_a_change_to_the_clis_vocabulary_makes_the_spec_stale(tmp_path, monkeypatch):
    from probe.daemon import cli_spec

    before = cli_spec.source_sha()
    monkeypatch.setattr(cli_spec, "VOCABULARY", cli_spec.VOCABULARY[:-1])
    assert cli_spec.source_sha() != before


def test_the_host_keeps_its_runs_on_file_for_whoever_is_not_its_service():
    host_mod, host = _bare_host()
    host.folder.mkdir(parents=True, exist_ok=True)
    asked = SimpleNamespace(asked=True)
    host.runs["r1"] = SimpleNamespace(run_id="r1", sid="live", draining=False, worker=None, owner_gone=False,
                                      stopper=SimpleNamespace(asked=False), ticked_at=0, cpu_s=0.0,
                                      started_at=time.monotonic())
    host.runs["r2"] = SimpleNamespace(run_id="r2", sid="stopped", draining=False, worker=None, owner_gone=False,
                                      stopper=asked, ticked_at=0, cpu_s=0.0, started_at=time.monotonic())
    host.runs["r3"] = SimpleNamespace(run_id="r3", sid="orphan", draining=False, worker=None, owner_gone=True,
                                      stopper=SimpleNamespace(asked=False), ticked_at=0, cpu_s=0.0,
                                      started_at=time.monotonic())
    host._beat()  # no service connected: still on file
    data = json.loads(host.runs_path.read_text())
    assert {r["sid"]: r["draining"] for r in data["runs"]} == {"live": False, "stopped": True, "orphan": True}


def test_a_stop_by_session_reaches_a_run_too_new_for_any_beat(monkeypatch, tmp_path):
    host, seen = _host(monkeypatch, tmp_path)
    proc = _proc(1)
    host._current = proc
    assert host.stop_session("brand-new") is False  # not listed yet: not claimed as stopped
    assert json.loads(proc.far.recv(65536).decode().splitlines()[0]) == {"op": "stop", "sid": "brand-new"}


def test_a_runs_stuck_thread_never_keeps_its_run_from_ending():
    from probe.daemon import host as host_mod

    release = threading.Event()
    run = runctx.Run("s1")

    async def body():
        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, release.wait, 30)  # a thread stuck on a dead mount
        await asyncio.sleep(0.05)
        return 7

    started = time.monotonic()
    with runctx.enter(run):
        assert host_mod.run_loop(run, body()) == 7
    assert time.monotonic() - started < 5
    release.set()
