"""The service supervises each recorded session's daemon worker itself (plan Q3).

Unit half (a fake Popen and clock): the tap supervisor's rules, by exit code
-- respawn at once after 0, later after EXIT_RESPAWN_LATER and
EXIT_RETRY_LIBS, a doubling wait after a crash, none after EXIT_DO_NOT_RESPAWN
or 2 until the switch moves, at most RESPAWNS_PER_MINUTE -- plus what only
this one does: no start while the updater holds starts or another live worker
holds the session lock (whose holder is asked to hand over), one owner per
session, SIGTERM at release.

Service half (a real service, a stand-in tap that hands its worker over, and
`FakeWorker` as the worker): spawn and `service.status`, crash backoff,
give-up exits, session end, no second worker while one holds the lock, an
older tap keeping its own, and the updater's hand-over.
"""

from __future__ import annotations

import fcntl
import json
import os
import signal
import sys
import time
from pathlib import Path

import pytest

from probe.service import workers
from probe.service.protocol import Method, WorkerState
from tests.service_fakes import FakeCore, FakeWorker
from tests.service_harness import kill_agent, ps_passes, service_home, spawn_agent, wait_for  # noqa: F401

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the service is POSIX-only")

SID = "11111111-2222-3333-4444-555555555555"
#: The real tap supervisor's SDK socket can fall back to a shared /tmp path:
#: a session id no other test uses.
CROSS_SID = "q3q3q3q3-2222-3333-4444-555555555555"


# -- the rules, unit --------------------------------------------------------------


class Clock:
    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


class Switch:
    def __init__(self, state: str | None = "daemon") -> None:
        self.state = state

    def __call__(self) -> tuple:
        return self.state, self.state == "daemon"


def _popen(exits: list, spawned: list):
    """A Popen whose n-th child exits with exits[n] (None: keeps running)."""

    class FakePopen:
        def __init__(self, argv, **kw):
            spawned.append({"argv": argv, **kw})
            self.pid = 4000 + len(spawned)
            self.returncode = exits[len(spawned) - 1] if len(spawned) <= len(exits) else None
            self.signals: list = []

        def poll(self):
            return self.returncode

        def send_signal(self, sig):
            self.signals.append(sig)

    return FakePopen


def _spec(tmp_path: Path, switch=None, **over) -> dict:
    spec = {
        "sid": SID, "transcript": str(tmp_path / "t.jsonl"), "cwd": str(tmp_path), "source": "claude_code",
        "daemon_dir": str(tmp_path / "state" / "probe" / "daemon"),
        "env": {"HOME": str(tmp_path), "PROBE_TEST_MARK": "m"}, "switch": switch or Switch(),
    }
    spec.update(over)
    return spec


@pytest.fixture
def rig(tmp_path, monkeypatch):
    """A supervisor with a fake Popen, clock and interpreter; nothing held."""
    spawned: list = []
    clock = Clock()
    exits: list = []
    monkeypatch.setattr(workers.subprocess, "Popen", ps_passes(_popen(exits, spawned)))
    monkeypatch.setattr(workers, "cli_python", lambda: "/cli/python")
    monkeypatch.setattr(workers, "held_for_update", lambda: False)
    switch = Switch()
    sup = workers.Supervisor(workers.parse_spec(_spec(tmp_path, switch)), owner=None, clock=clock)

    class Rig:
        def poll(self):
            """One look, and the launch it may start, to its end (its own thread)."""
            self.sup.poll()
            launch = self.sup._launch
            if launch is not None and launch.thread is not None:
                launch.thread.join(5)
                assert not launch.thread.is_alive(), "a launch did not finish"

    r = Rig()
    r.sup, r.spawned, r.clock, r.exits, r.switch, r.monkeypatch = sup, spawned, clock, exits, switch, monkeypatch
    return r


def test_it_starts_the_worker_from_the_cli_interpreter_with_the_session_s_environment(rig, tmp_path):
    rig.exits[:] = [None]
    rig.poll()
    (spawn,) = rig.spawned
    assert spawn["argv"] == ["/cli/python", "-I", "-c", workers.ENTRY, "daemon", "worker", "--session-id", SID,
                             "--transcript", str(tmp_path / "t.jsonl"), "--cwd", str(tmp_path), "--source",
                             "claude_code"]
    assert spawn["env"]["PROBE_TEST_MARK"] == "m" and spawn["env"]["HOME"] == str(tmp_path)
    assert all(spawn["env"][k] == "1" for k in workers.SUPERVISOR_ENV)
    identity = json.loads(spawn["env"][workers.SUPERVISOR_PID_ENV])
    assert identity == {"pid": os.getpid(), "start": workers.procid.start_time(os.getpid()), "sid": SID}
    assert spawn["env"][workers.ENTER_CWD_ENV] == "1"
    assert spawn["start_new_session"] is True
    assert spawn["cwd"] == str(tmp_path / "state" / "probe" / "daemon"), "its own state folder, never the project's"
    assert (tmp_path / "state" / "probe" / "daemon" / f"{SID}.log").exists()
    assert rig.sup.state == WorkerState.RUNNING and rig.sup.public(rig.clock.now)["pid"] == 4001
    rig.poll()
    assert len(rig.spawned) == 1, "one worker while it runs"


def test_a_worker_is_told_to_enter_its_folder_without_an_identity_too(rig):
    """No start time to name this service by: the worker gets its pid alone,
    and still moves into its session's folder."""
    rig.monkeypatch.setattr(workers.procid, "start_time", lambda pid: None)
    rig.monkeypatch.setattr(workers, "_own_start", {})
    rig.exits[:] = [None]
    rig.poll()
    (spawn,) = rig.spawned
    assert json.loads(spawn["env"][workers.SUPERVISOR_PID_ENV]) == {"pid": os.getpid(), "start": None, "sid": SID}
    assert spawn["env"][workers.ENTER_CWD_ENV] == "1"


def test_the_updater_finds_the_worker_by_its_command_line():
    """`updater._is_worker` reads the command line for `daemon worker <sid>`:
    the D7 hand-over asks only workers it recognizes."""
    argv = workers.Supervisor(workers.parse_spec(_spec(Path("/tmp"))), owner=None)._argv("/cli/python")
    assert "daemon" in argv and "worker" in argv and SID in " ".join(argv)


def test_no_worker_while_the_switch_does_not_want_one(rig):
    rig.switch.state = "off"
    rig.poll()
    assert rig.spawned == [] and rig.sup.state == WorkerState.IDLE


def test_a_crashing_worker_is_started_again_after_a_doubling_wait(rig):
    rig.exits[:] = [workers.EXIT_CRASHED, 1, 0, None]
    rig.poll()  # spawn 1
    rig.poll()  # it crashed: wait
    assert len(rig.spawned) == 1 and rig.sup.crashes == 1 and rig.sup.state == WorkerState.BACKOFF
    rig.clock.now += workers.CRASH_BACKOFF_S + 1
    rig.poll()  # spawn 2
    rig.poll()  # crashed again (a plain traceback exit): the wait doubles
    rig.clock.now += workers.CRASH_BACKOFF_S + 1
    rig.poll()
    assert len(rig.spawned) == 2 and rig.sup.crashes == 2
    rig.clock.now += workers.CRASH_BACKOFF_S
    rig.poll()  # spawn 3, which exits 0: again at once, the count reset
    rig.poll()
    assert len(rig.spawned) == 4 and rig.sup.crashes == 0 and rig.sup.gave_up_in is None


def test_a_worker_stopped_by_a_full_disk_waits_like_a_crash_and_is_never_a_crash_loop(rig):
    """new-workspace 2026-10-24: a full disk is the machine's, not a worker bug."""
    reports: list = []
    rig.sup.incident = lambda *args, **kwargs: reports.append(args)
    rig.exits[:] = [workers.EXIT_DISK_FULL] * workers.REPORT_CRASHES + [None]
    for n in range(workers.REPORT_CRASHES):
        rig.poll()  # spawn
        rig.poll()  # it stopped: wait
        assert rig.sup.crashes == n + 1 and rig.sup.state == WorkerState.BACKOFF
        rig.clock.now += workers.CRASH_BACKOFF_S * 2 ** n + 1
    assert len(rig.spawned) == workers.REPORT_CRASHES and reports == []


@pytest.mark.parametrize("code", [workers.EXIT_DO_NOT_RESPAWN, workers.EXIT_NO_COMMAND])
def test_a_worker_that_says_respawning_cannot_help_waits_for_the_switch_to_move(rig, code):
    rig.exits[:] = [code, None]
    for _ in range(4):
        rig.poll()
        rig.clock.now += 120
    assert len(rig.spawned) == 1 and rig.sup.gave_up_in == "daemon" and rig.sup.state == WorkerState.GAVE_UP
    rig.switch.state = "off"
    rig.poll()
    rig.switch.state = "daemon"
    rig.poll()
    assert len(rig.spawned) == 2


def test_a_worker_that_left_over_the_switch_starts_again_later_never_given_up(rig):
    rig.exits[:] = [workers.EXIT_RESPAWN_LATER, None]
    rig.poll()
    rig.poll()
    assert rig.sup.gave_up_in is None and rig.sup.crashes == 0 and len(rig.spawned) == 1
    rig.clock.now += workers.RESPAWN_LATER_S + 1
    rig.poll()
    assert len(rig.spawned) == 2


def test_a_worker_without_its_libraries_is_tried_again_later(rig):
    rig.exits[:] = [workers.EXIT_RETRY_LIBS, None]
    rig.poll()
    rig.poll()
    rig.clock.now += workers.LIBS_RETRY_S - 1
    rig.poll()
    assert len(rig.spawned) == 1 and rig.sup.gave_up_in is None
    rig.clock.now += 2
    rig.poll()
    assert len(rig.spawned) == 2


def test_at_most_five_starts_a_minute(rig):
    rig.exits[:] = [0] * 10
    for _ in range(10):
        rig.poll()
    assert len(rig.spawned) == workers.RESPAWNS_PER_MINUTE and rig.sup.state == WorkerState.BACKOFF
    rig.clock.now += 61
    rig.poll()
    assert len(rig.spawned) == workers.RESPAWNS_PER_MINUTE + 1


def test_no_interpreter_is_a_give_up_until_the_switch_moves(rig):
    rig.monkeypatch.setattr(workers, "cli_python", lambda: None)
    rig.poll()
    rig.poll()
    assert rig.spawned == [] and rig.sup.gave_up_in == "daemon"


def test_nothing_starts_while_the_updater_holds_worker_starts(rig):
    rig.monkeypatch.setattr(workers, "held_for_update", lambda: True)
    rig.poll()
    assert rig.spawned == [] and rig.sup.state == WorkerState.HELD_FOR_UPDATE
    rig.monkeypatch.setattr(workers, "held_for_update", lambda: False)
    rig.exits[:] = [None]
    rig.poll()
    assert len(rig.spawned) == 1, "and the next one starts once it lets go"


def _hold(lock: Path):
    lock.parent.mkdir(parents=True, exist_ok=True)
    handle = open(lock, "a")  # noqa: SIM115 -- the caller closes it
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    return handle


def test_no_second_worker_while_another_holds_the_session_lock_and_it_is_asked_to_hand_over(rig):
    """The hazard: a waiting worker waits for a holder that never hands over,
    and a supervisor that lost track of its child added one per respawn (the
    Windows harness: ~100). Here none starts until the holder lets go, and the
    holder is asked to hand over meanwhile (its marker kept fresh)."""
    held = _hold(rig.sup.lock)
    try:
        for _ in range(10):
            rig.poll()
            rig.clock.now += workers.HANDOVER_TOUCH_S
        assert rig.spawned == [] and rig.sup.state == WorkerState.WAITING_FOR_LOCK
        assert time.time() - rig.sup.handover.stat().st_mtime < 10
    finally:
        held.close()
    rig.exits[:] = [None]
    rig.poll()
    assert len(rig.spawned) == 1


def test_a_released_supervisor_withdraws_the_ask_it_kept_fresh(rig):
    """Its session ended while it waited: the holder must finish its own
    queue, not hand it to a successor that never comes."""
    held = _hold(rig.sup.lock)
    try:
        rig.poll()
        assert rig.sup.handover.exists()
        assert rig.sup.terminate() is None
        assert not rig.sup.handover.exists()
    finally:
        held.close()


def test_nothing_starts_once_the_service_stops(rig):
    rig.sup.may_start = lambda: False
    rig.poll()
    assert rig.spawned == []


def test_an_ask_dated_ahead_by_a_stopping_service_is_left_ahead(rig):
    held = _hold(rig.sup.lock)
    try:
        rig.sup.handover.touch()
        ahead = time.time() + 180
        os.utime(rig.sup.handover, (ahead, ahead))
        rig.poll()
        assert rig.sup.handover.stat().st_mtime == pytest.approx(ahead, abs=1)
    finally:
        held.close()


def test_a_released_session_s_worker_is_asked_to_stop_and_reaped(tmp_path, monkeypatch):
    monkeypatch.setenv(workers.POLL_ENV, "0.02")
    spawned: list = []
    monkeypatch.setattr(workers.subprocess, "Popen", ps_passes(_popen([None], spawned)))
    monkeypatch.setattr(workers, "cli_python", lambda: "/cli/python")
    monkeypatch.setattr(workers, "held_for_update", lambda: False)
    host = workers.WorkerHost(log=lambda m: None)
    link = host.link(SID)
    assert link.supervise(_spec(tmp_path)) is True
    assert wait_for(lambda: len(spawned) == 1, 5)
    (row,) = host.public()
    assert row["state"] == WorkerState.RUNNING and row["pid"] == 4001
    link.release()
    assert wait_for(lambda: host.public() and host.public()[0]["state"] == WorkerState.DRAINING, 5)
    child = host._draining[0][1]
    assert child.signals == [signal.SIGTERM]
    child.returncode = 0
    assert wait_for(lambda: host.public() == [], 5), "reaped once it exits"
    assert len(spawned) == 1, "an ended session's worker is never started again"
    host.close()


def test_a_hung_project_folder_stalls_no_other_session(tmp_path, monkeypatch):
    """Codex R1 on #3309: `_spawn` looked at the project folder (`isdir`, then
    Popen's chdir) on the one supervising thread, so a hung network mount in one
    session's folder stopped every other session's starts, restarts and stops.
    The project is the worker's `--cwd`; nothing on this thread touches it."""
    monkeypatch.setenv(workers.POLL_ENV, "0.02")
    monkeypatch.setattr(workers, "cli_python", lambda: "/cli/python")
    monkeypatch.setattr(workers, "held_for_update", lambda: False)
    hung = str(tmp_path / "hung-mount" / "project")
    release = __import__("threading").Event()
    spawned: list = []
    real_isdir = os.path.isdir

    def isdir(path):
        if str(path).startswith(hung):
            release.wait(30)  # a stat on a dead NFS server
        return real_isdir(path)

    class Popen:
        def __init__(self, argv, **kw):
            if str(kw.get("cwd", "")).startswith(hung):
                release.wait(30)  # the chdir into it, in the child, blocks the parent's exec wait
            spawned.append(argv[argv.index("--session-id") + 1])
            self.pid, self.returncode = 5000 + len(spawned), None

        def poll(self):
            return None

        def send_signal(self, sig):
            pass

    monkeypatch.setattr(workers.os.path, "isdir", isdir)
    monkeypatch.setattr(workers.subprocess, "Popen", ps_passes(Popen))
    host = workers.WorkerHost(log=lambda m: None)
    try:
        assert host.link("hung").supervise(_spec(tmp_path, sid="hung", cwd=hung))
        assert host.link("fine").supervise(_spec(tmp_path, sid="fine"))
        assert wait_for(lambda: "fine" in spawned, 3), "one session's dead mount stalled another's start"
        assert wait_for(lambda: "hung" in spawned, 3), "and its own worker starts too: it is the worker's to enter"
    finally:
        release.set()
        host.close()


def test_a_start_time_it_could_not_read_is_read_again_later(monkeypatch):
    """Codex R2 on #3309: one failed read of this service's start time (a `ps`
    timing out on macOS) was cached for the life of the service, so no worker
    ever got its supervisor's identity. It is read again, with a growing wait."""
    reads: list = []
    answers = iter([None, None, "4711"])
    clock = Clock()
    monkeypatch.setattr(workers.procid, "start_time", lambda pid: reads.append(pid) or next(answers))
    monkeypatch.setattr(workers.time, "monotonic", clock)
    monkeypatch.setattr(workers, "_own_start", {})

    def start():
        return json.loads(workers.supervisor_value(SID))["start"]

    assert start() is None
    assert start() is None and len(reads) == 1, "not read again at once"
    clock.now += 600
    assert start() is None and len(reads) == 2
    clock.now += 600
    assert start() == "4711"
    clock.now += 600
    assert start() == "4711" and len(reads) == 3, "once read, kept"


def test_a_hung_interpreter_stat_never_holds_up_another_session_s_stop(tmp_path, monkeypatch):
    """Codex R2 on #3309: the interpreter lookup (runtime.json, then a stat of
    the python it names -- which `probe service start` allows to be a project
    venv's, on a mount that can hang) ran on the one supervising thread, and
    another session's release got no SIGTERM until the stat came back. The real
    lookup runs here, against a stat that blocks."""
    from probe.service import client

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv(workers.POLL_ENV, "0.02")
    monkeypatch.setattr(workers, "held_for_update", lambda: False)
    real_python = str(tmp_path / "bin" / "python")
    Path(real_python).parent.mkdir(parents=True)
    Path(real_python).write_text("")
    os.chmod(real_python, 0o755)
    hung = str(tmp_path / "hung-mount" / "venv" / "bin" / "python")
    release = __import__("threading").Event()
    real_isfile = os.path.isfile

    def isfile(path):
        if str(path) == hung:
            release.wait(30)  # a stat on a dead NFS server
        return real_isfile(path)

    spawned: list = []
    monkeypatch.setattr(workers.subprocess, "Popen", ps_passes(_popen([None, None], spawned)))
    monkeypatch.setattr(os.path, "isfile", isfile)
    host = workers.WorkerHost(log=lambda m: None)
    try:
        client.write_runtime(real_python, "test")
        first = host.link("first")
        assert first.supervise(_spec(tmp_path, sid="first"))
        assert wait_for(lambda: len(spawned) == 1, 5), "the first session's worker starts"
        client.write_runtime(hung, "test")  # the next lookup hangs on its stat
        assert host.link("second").supervise(_spec(tmp_path, sid="second"))
        time.sleep(0.2)  # the second session's start is under way, stuck in the stat
        first.release()
        assert wait_for(lambda: host._draining and host._draining[0][1].signals == [signal.SIGTERM], 3), \
            "a hung interpreter stat held up another session's SIGTERM"
    finally:
        release.set()
        host.close()


def _blocking_popen(gate, spawned):
    """A Popen whose exec blocks until `gate` opens (a hung mount), then a child
    that keeps running and records the signals it gets."""

    class FakePopen:
        def __init__(self, argv, **kw):
            gate.wait(30)
            spawned.append(self)
            self.pid, self.returncode, self.signals = 6000 + len(spawned), None, []

        def poll(self):
            return self.returncode

        def send_signal(self, sig):
            self.signals.append(sig)

    return FakePopen


def test_a_worker_started_while_the_service_stops_is_stopped_not_kept(tmp_path, monkeypatch):
    """Codex R3 on #3309: a launch blocked in its exec when the service stopped
    published its child anyway (`running`, no SIGTERM, not drained): a worker
    of a dying service that missed the hand-over ask. Stopping cancels every
    launch under way; a child it still yields is asked to stop and drained.
    Mutation caught: dropping the cancelled check where the child is published."""
    gate = __import__("threading").Event()
    spawned: list = []
    monkeypatch.setenv(workers.POLL_ENV, "0.02")
    monkeypatch.setattr(workers, "cli_python", lambda: "/cli/python")
    monkeypatch.setattr(workers, "held_for_update", lambda: False)
    monkeypatch.setattr(workers.subprocess, "Popen", ps_passes(_blocking_popen(gate, spawned)))
    host = workers.WorkerHost(log=lambda m: None)
    try:
        assert host.link(SID).supervise(_spec(tmp_path))
        assert wait_for(lambda: host.public() and host.public()[0]["state"] == WorkerState.STARTING, 5)
        time.sleep(0.1)  # in its exec
        host.close()
        gate.set()
        assert wait_for(lambda: spawned, 5)
        (child,) = spawned
        assert wait_for(lambda: child.signals == [signal.SIGTERM], 5), "a worker the stopping service started was kept"
        assert host._sessions[SID].child is None and host._sessions[SID].state != WorkerState.RUNNING
        assert any(c is child for _, c in host._draining), "and reaped as it drains"
    finally:
        gate.set()
        host.close()


def test_its_pid_goes_to_the_worker_even_without_its_start_time(monkeypatch):
    """Codex R3 on #3309: with its start time unreadable the service sent no
    identity at all, and the worker went by `getppid()` alone (init's, after
    a quick exit). The pid always goes; the start time when it is known.
    Mutation caught: leaving the identity out when the start time is missing."""
    clock = Clock()
    monkeypatch.setattr(workers.procid, "start_time", lambda pid: None)
    monkeypatch.setattr(workers.time, "monotonic", clock)
    monkeypatch.setattr(workers, "_own_start", {})
    value = workers.supervisor_value(SID)
    assert value is not None and json.loads(value) == {"pid": os.getpid(), "start": None, "sid": SID}


def test_one_launch_per_session_across_releases_and_new_recordings(tmp_path, monkeypatch):
    """Codex R3 on #3309: each release and new recording of a session whose
    launch hung (a blocked interpreter stat) started another launch thread: 8
    cycles, 8 threads. One launch per session at a time, kept across releases
    and recordings, until it is done. Mutation caught: dropping the per-session
    launch reservation (a fresh supervisor launches at once)."""
    import threading

    from probe.service import client

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv(workers.POLL_ENV, "0.02")
    monkeypatch.setattr(workers, "held_for_update", lambda: False)
    hung = str(tmp_path / "hung-mount" / "venv" / "bin" / "python")
    release = threading.Event()
    real_isfile = os.path.isfile

    def isfile(path):
        if str(path) == hung:
            release.wait(30)  # a stat on a dead NFS server
        return real_isfile(path)

    spawned: list = []
    monkeypatch.setattr(workers.subprocess, "Popen", ps_passes(_popen([None] * 10, spawned)))
    monkeypatch.setattr(os.path, "isfile", isfile)
    client.write_runtime(hung, "test")
    host = workers.WorkerHost(log=lambda m: None)

    def launches() -> int:
        return sum(1 for t in threading.enumerate() if t.name == f"worker-launch-{SID[:12]}" and t.is_alive())

    try:
        for _ in range(8):
            link = host.link(SID)
            assert link.supervise(_spec(tmp_path))
            time.sleep(0.1)  # its poll would start a launch
            link.release()
            time.sleep(0.05)
        assert launches() == 1, f"{launches()} launch threads for one session"
    finally:
        release.set()
        host.close()


def test_a_slow_start_time_read_holds_up_no_other_launch(monkeypatch):
    """Codex R3 on #3309: the read of this service's start time (a `ps` on
    macOS) ran under the lock every launch takes, so one blocked read held
    every other session in `starting`. The read is reserved under the lock and
    made outside it; the others go on without the start time meanwhile.
    Mutation caught: holding the lock across the read."""
    import threading

    gate = threading.Event()
    entered = threading.Event()

    def start_time(pid):
        entered.set()
        gate.wait(30)
        return "4711"

    monkeypatch.setattr(workers.procid, "start_time", start_time)
    monkeypatch.setattr(workers, "_own_start", {})
    first = threading.Thread(target=workers.supervisor_value, args=("first",), daemon=True)
    first.start()
    try:
        assert entered.wait(5)
        got = {}
        second = threading.Thread(target=lambda: got.setdefault("v", workers.supervisor_value("second")), daemon=True)
        second.start()
        second.join(2)
        assert "v" in got, "a slow start-time read held up another session's launch"
    finally:
        gate.set()
        first.join(5)


def test_a_failed_start_time_read_is_retried_at_5_10_20_up_to_300_s(monkeypatch):
    """The retry schedule itself, read off when the reads happen: 5 s, doubling,
    capped at 300 s. Mutations caught: a constant wait, an uncapped one, no doubling."""
    reads: list = []
    clock = Clock()
    monkeypatch.setattr(workers.procid, "start_time", lambda pid: reads.append(clock.now) and None)
    monkeypatch.setattr(workers.time, "monotonic", clock)
    monkeypatch.setattr(workers, "_own_start", {})
    start = clock.now
    while clock.now < start + 1300:
        workers.supervisor_value(SID)
        clock.now += 1.0
    gaps = [round(b - a) for a, b in zip(reads, reads[1:])]
    assert gaps[:8] == [5, 10, 20, 40, 80, 160, 300, 300], gaps


def test_one_owner_per_session_and_a_stale_release_changes_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(workers, "POLL_S", 3600.0)
    host = workers.WorkerHost(log=lambda m: None)
    first, second = host.link(SID), host.link(SID)
    assert first.supervise(_spec(tmp_path)) and second.supervise(_spec(tmp_path))
    assert len(host._sessions) == 1 and host._sessions[SID].owner is second
    first.release()  # the older recording ending: the session goes on with the newer
    assert host.supervised(SID)
    second.release()
    assert not host.supervised(SID)
    host.close()


def test_a_spec_it_cannot_use_leaves_the_worker_to_the_tap(tmp_path):
    host = workers.WorkerHost(log=lambda m: None)
    link = host.link(SID)
    assert link.supervise(_spec(tmp_path, cwd="relative")) is False
    assert link.supervise(_spec(tmp_path, switch="not callable")) is False
    assert link.supervise(_spec(tmp_path, sid="another")) is False
    assert link.supervise(_spec(tmp_path, env={"A": "x\0y"})) is False
    assert not host.supervised(SID)
    host.close()


def test_a_session_that_ends_as_the_service_stops_still_has_its_worker_stopped(tmp_path, monkeypatch):
    spawned: list = []
    monkeypatch.setenv(workers.POLL_ENV, "0.02")
    monkeypatch.setattr(workers.subprocess, "Popen", ps_passes(_popen([None], spawned)))
    monkeypatch.setattr(workers, "cli_python", lambda: "/cli/python")
    monkeypatch.setattr(workers, "held_for_update", lambda: False)
    host = workers.WorkerHost(log=lambda m: None)
    link = host.link(SID)
    link.supervise(_spec(tmp_path))
    assert wait_for(lambda: len(spawned) == 1, 5)
    child = host._sessions[SID].child
    host.close()
    assert child.signals == [], "a stopping service leaves its workers to hand over"
    link.release()
    assert wait_for(lambda: child.signals == [signal.SIGTERM], 5), "the host's thread still stops ended sessions' workers"


def test_a_stopping_service_starts_nothing_but_keeps_the_tap_from_starting_one(tmp_path, monkeypatch):
    spawned: list = []
    monkeypatch.setattr(workers.subprocess, "Popen", ps_passes(_popen([], spawned)))
    host = workers.WorkerHost(log=lambda m: None)
    host.close()
    assert host.link(SID).supervise(_spec(tmp_path)) is True
    time.sleep(0.1)
    assert spawned == [] and host.public() == []


def test_the_exit_codes_and_rules_are_the_worker_s_and_the_tap_supervisor_s(tap_sup):
    from probe.daemon import worker

    assert (workers.EXIT_DO_NOT_RESPAWN, workers.EXIT_CRASHED, workers.EXIT_RESPAWN_LATER, workers.EXIT_RETRY_LIBS,
            workers.EXIT_DISK_FULL) \
        == (worker.EXIT_DO_NOT_RESPAWN, worker.EXIT_CRASHED, worker.EXIT_RESPAWN_LATER, worker.EXIT_RETRY_LIBS,
            worker.EXIT_DISK_FULL)
    # A tap's supervisor knows no EXIT_DISK_FULL: it waits on it as on any crash.
    assert workers.EXIT_DISK_FULL not in (tap_sup.EXIT_CRASHED, tap_sup.EXIT_RESPAWN_LATER, tap_sup.EXIT_RETRY_LIBS,
                                          0, 2, 3)
    assert workers.SUPERVISOR_PID_ENV == worker.SUPERVISOR_PID_ENV
    assert workers.ENTER_CWD_ENV == worker.ENTER_CWD_ENV
    assert set(workers.SUPERVISOR_ENV) == {
        worker.SUPERVISOR_FOLLOWS_INLINE_ENV, worker.SUPERVISOR_READ_ONLY_INLINE_ENV,
        worker.SUPERVISOR_RETRIES_LIBS_ENV,
    }
    assert (workers.RESPAWNS_PER_MINUTE, workers.RESPAWN_LATER_S, workers.LIBS_RETRY_S, workers.CRASH_BACKOFF_S,
            workers.CRASH_BACKOFF_CAP_S) == (
        tap_sup.RESPAWNS_PER_MINUTE, tap_sup.RESPAWN_LATER_SECONDS, tap_sup.LIBS_RETRY_SECONDS,
        tap_sup.CRASH_BACKOFF_SECONDS, tap_sup.CRASH_BACKOFF_CAP_SECONDS)
    assert workers.safe_sid("a/b c") == Path(worker.store_path("a/b c").name).stem
    assert workers.POLL_ENV in __import__("probe.service.client", fromlist=["x"]).ENV_ALLOWLIST
    assert workers.BACKOFF_ENV in __import__("probe.service.client", fromlist=["x"]).ENV_ALLOWLIST


@pytest.fixture
def tap_sup(monkeypatch):
    """The tap plugin's supervisor module, off the plugin's own path; whatever
    `tap` another test left in `sys.modules` is set aside meanwhile."""
    for name in [m for m in list(sys.modules) if m == "tap" or m.startswith("tap.")]:
        monkeypatch.delitem(sys.modules, name)
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap"))
    from tap import companion_supervisor

    yield companion_supervisor
    for name in [m for m in list(sys.modules) if m == "tap" or m.startswith("tap.")]:
        sys.modules.pop(name, None)


def test_the_tap_s_supervisor_and_the_service_s_never_both_spawn(tmp_path, monkeypatch, tap_sup):
    """The real tap Supervisor on a recorder's thread, handed the service's
    real link: the service starts the one worker, the tap none -- and with no
    link (an older service) the tap starts it, as before."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv(workers.POLL_ENV, "0.02")
    monkeypatch.setattr(tap_sup, "probe_cli", lambda: "/usr/bin/probe")
    monkeypatch.setattr(workers, "cli_python", lambda: "/cli/python")
    monkeypatch.setattr(workers, "held_for_update", lambda: False)
    spawned: list = []
    # One `subprocess` module for both: who started a worker is in its argv.
    monkeypatch.setattr(workers.subprocess, "Popen", ps_passes(_popen([None, None], spawned)))

    def by(who: str) -> list:
        return [s for s in spawned if s["argv"][0] == who]

    state = tmp_path / "state" / "probe" / "sessions" / f"{CROSS_SID}.state"
    state.parent.mkdir(parents=True)
    state.write_text("daemon")
    host = workers.WorkerHost(log=lambda m: None)
    sup = tap_sup.Supervisor(
        session_id=CROSS_SID, transcript=tmp_path / "t.jsonl", cwd=tmp_path, service=host.link(CROSS_SID)
    )
    try:
        sup.poll()
        sup.claimed()
        for _ in range(5):
            sup.poll()
        assert wait_for(lambda: len(by("/cli/python")) == 1, 5)
        time.sleep(0.1)
        assert by("/usr/bin/probe") == [] and len(spawned) == 1
        assert spawned[0]["argv"][-1] == "claude_code"
    finally:
        sup.stop()
        host.close()
    older = tap_sup.Supervisor(session_id=CROSS_SID, transcript=tmp_path / "t.jsonl", cwd=tmp_path)
    older.poll()
    assert len(by("/usr/bin/probe")) == 1


# -- a real service ---------------------------------------------------------------

#: A tap whose recorder hands its session's worker over as `tap.companion_supervisor`
#: does (`PROBE_TEST_TAP=old`: one from before, which never does), reads the
#: switch from `<state>/probe/sessions/<sid>.state`, and releases the worker
#: when its session ends.
_HOSTED = '''
import json, os, threading, time
from dataclasses import dataclass, field

ENDED, PAUSED, STOPPED, FAILED = "ended", "paused", "stopped", "failed"


@dataclass
class Controls:
    stop: threading.Event = field(default_factory=threading.Event)
    pause: threading.Event = field(default_factory=threading.Event)
    workers: object = None


def record(session, controls):
    env = session["env"]
    state = os.path.join(env["HOME"], ".local", "state", "probe")
    sid = session["sid"]

    def switch():
        try:
            word = open(os.path.join(state, "sessions", sid + ".state")).read().strip() or None
        except OSError:
            word = None
        return word, word == "daemon"

    link = None if env.get("PROBE_TEST_TAP") == "old" else controls.workers
    taken = bool(link is not None and link.supervise({
        "sid": sid, "transcript": session["transcript"], "cwd": session["cwd"], "source": "claude_code",
        "daemon_dir": os.path.join(state, "daemon"), "env": env, "switch": switch}))
    with open(os.path.join(env["HOME"], "recorded.jsonl"), "a") as handle:
        handle.write(json.dumps({"sid": sid, "taken": taken, "link": controls.workers is not None}) + "\\n")
    while True:
        if controls.stop.wait(0.05):
            if taken:
                link.release()
            return ENDED, ""
        if controls.pause.is_set():
            return PAUSED, ""
'''


def _tap(root: Path) -> Path:
    tap = root / "tap"
    tap.mkdir(parents=True)
    (tap / "__init__.py").write_text('__version__ = "0.10.0"\n')
    (tap / "main.py").write_text("")
    (tap / "hosted.py").write_text(_HOSTED)
    return root


def _state(home: Path) -> Path:
    return home / ".local" / "state" / "probe"


def _switch(home: Path, sid: str, word: str) -> None:
    path = _state(home) / "sessions" / f"{sid}.state"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(word)


def _record(sh, sid: str, owner: dict, root: Path, tmp: Path, **env) -> dict:
    params = {
        "sid": sid, "harness": "claude_code", "mode": "daemon", "owner": owner, "generation": 1,
        "state_dir": str(_state(sh.home)), "cwd": str(tmp), "transcript": str(tmp / f"{sid}.jsonl"),
        "transcript_dir": None, "tap_root": str(root), "tap_version": "0.10.0",
        "env": {"HOME": str(sh.home), "PROBE_TEST_MARK": sid, **env},
    }
    return sh.call(Method.SESSION_RECORD, params)


def _rows(sh, sid: str) -> list[dict]:
    return [r for r in sh.call(Method.STATUS)["workers"] if r["sid"] == sid]


def _row(sh, sid: str) -> dict:
    rows = _rows(sh, sid)
    return rows[0] if rows else {}


@pytest.fixture
def live(service_home, monkeypatch, tmp_path):
    monkeypatch.setenv(workers.POLL_ENV, "0.05")
    monkeypatch.setenv(workers.BACKOFF_ENV, "0.4")
    FakeCore(service_home.home)
    fake = FakeWorker(service_home.home)
    agent, owner = spawn_agent()

    class Live:
        pass

    lv = Live()
    lv.sh, lv.fake, lv.owner, lv.root = service_home, fake, owner, _tap(tmp_path / "tap-a")
    try:
        yield lv
    finally:
        kill_agent(agent)
        for pid in fake.live_pids():
            with __import__("contextlib").suppress(OSError):
                os.kill(pid, signal.SIGKILL)


def test_the_service_starts_a_recorded_session_s_worker_and_shows_it(live, tmp_path):
    sh, fake = live.sh, live.fake
    _switch(sh.home, "s1", "daemon")
    status = sh.start()
    assert _record(sh, "s1", live.owner, live.root, tmp_path)["recording"] is True
    assert wait_for(lambda: fake.events("running", "s1"), 10), sh.log()
    (start,) = fake.starts("s1")
    assert start["argv"][:3] == ["daemon", "worker", "--session-id"] and "s1" in start["argv"]
    assert start["ppid"] == status["pid"], "the service is its parent"
    assert start["env"]["PROBE_TAP_FOLLOWS_INLINE"] == "1" and start["env"]["PROBE_TEST_MARK"] == "s1"
    assert start["env"]["PYTHONPATH"] is None
    assert start["argv"][start["argv"].index("--cwd") + 1] == str(tmp_path), "the project is its --cwd"
    # The child reports `os.getcwd()`, the real path: /tmp is /private/tmp on macOS.
    assert start["cwd"] == os.path.realpath(_state(sh.home) / "daemon")
    supervisor = json.loads(start["env"]["PROBE_DAEMON_SUPERVISOR"])
    assert supervisor["pid"] == status["pid"] and supervisor["sid"] == "s1" and supervisor["start"]
    assert wait_for(lambda: _row(sh, "s1").get("state") == WorkerState.RUNNING, 5)
    assert _row(sh, "s1")["pid"] == start["pid"] and _row(sh, "s1")["spawns"] == 1
    time.sleep(0.3)
    assert len(fake.starts("s1")) == 1


def test_a_crashing_worker_is_started_again_after_a_growing_wait_live(live, tmp_path):
    sh, fake = live.sh, live.fake
    fake.plan(exits=[workers.EXIT_CRASHED, workers.EXIT_CRASHED])
    _switch(sh.home, "s1", "daemon")
    sh.start()
    _record(sh, "s1", live.owner, live.root, tmp_path)
    assert wait_for(lambda: fake.events("running", "s1"), 15), sh.log()
    first, second, third = (s["at"] for s in fake.starts("s1"))
    assert second - first >= 0.35 and third - second >= 0.75, "0.4 s, then twice that"
    row = _row(sh, "s1")
    assert row["crashes"] == 2 and row["last_exit"] == workers.EXIT_CRASHED and row["state"] == WorkerState.RUNNING


def test_a_worker_with_no_key_is_not_started_again_until_the_switch_moves_live(live, tmp_path):
    sh, fake = live.sh, live.fake
    fake.plan(exits=[workers.EXIT_DO_NOT_RESPAWN])
    _switch(sh.home, "s1", "daemon")
    sh.start()
    _record(sh, "s1", live.owner, live.root, tmp_path)
    assert wait_for(lambda: _row(sh, "s1").get("state") == WorkerState.GAVE_UP, 10), sh.log()
    time.sleep(0.5)
    assert len(fake.starts("s1")) == 1 and _row(sh, "s1")["gave_up_in"] == "daemon"
    _switch(sh.home, "s1", "off")
    assert wait_for(lambda: _row(sh, "s1").get("state") == WorkerState.IDLE, 5)
    _switch(sh.home, "s1", "daemon")
    assert wait_for(lambda: fake.events("running", "s1"), 10)
    assert len(fake.starts("s1")) == 2


def test_the_session_s_end_stops_its_worker_and_starts_none(live, tmp_path):
    sh, fake = live.sh, live.fake
    _switch(sh.home, "s1", "daemon")
    sh.start()
    _record(sh, "s1", live.owner, live.root, tmp_path)
    assert wait_for(lambda: fake.events("running", "s1"), 10), sh.log()
    assert sh.call(Method.SESSION_FINISH, {"sid": "s1", "wait": 5})["finished"] is True
    assert wait_for(lambda: fake.events("sigterm", "s1"), 5), "SIGTERM at its session's end"
    assert fake.events("sigterm", "s1")[0]["handover"] is False, "an ended session's worker drains, never hands over"
    assert wait_for(lambda: _rows(sh, "s1") == [], 5)
    time.sleep(0.3)
    assert len(fake.starts("s1")) == 1


def test_no_worker_starts_while_another_holds_the_session_lock_live(live, tmp_path):
    """A `tap watch`'s worker, or the last service's still handing over, holds
    the lock: the service starts none (a second would only wait), keeps its
    hand-over ask fresh, and starts one the moment it lets go."""
    sh, fake = live.sh, live.fake
    _switch(sh.home, "s1", "daemon")
    held = _hold(_state(sh.home) / "daemon" / "s1.lock")
    try:
        sh.start()
        _record(sh, "s1", live.owner, live.root, tmp_path)
        assert wait_for(lambda: _row(sh, "s1").get("state") == WorkerState.WAITING_FOR_LOCK, 10), sh.log()
        time.sleep(0.5)
        assert fake.starts("s1") == []
        assert time.time() - (_state(sh.home) / "daemon" / "s1.handover").stat().st_mtime < 10
    finally:
        held.close()
    assert wait_for(lambda: fake.events("running", "s1"), 10)
    assert fake.events("lock_busy") == []


def test_an_older_tap_keeps_its_own_worker_and_the_service_starts_none(live, tmp_path):
    sh, fake = live.sh, live.fake
    _switch(sh.home, "s1", "daemon")
    sh.start()
    _record(sh, "s1", live.owner, live.root, tmp_path, PROBE_TEST_TAP="old")
    recorded = sh.home / "recorded.jsonl"
    # The recorder opens the file before it writes its line: wait for the line.
    assert wait_for(lambda: recorded.exists() and recorded.read_text().splitlines(), 5)
    seen = json.loads(recorded.read_text().splitlines()[0])
    assert seen == {"sid": "s1", "taken": False, "link": True}
    time.sleep(0.5)
    assert fake.starts() == [] and _rows(sh, "s1") == []


def test_the_updater_s_hand_over_holds_the_next_worker_until_the_update_is_done(live, tmp_path):
    """D7 with the service as the supervisor: the update asks the running
    worker to hand over (marker, SIGTERM), and the service starts no worker
    while starts are held or the barrier is up; then it starts the next one."""
    import probe
    from tests.service_fakes import enable_auto_update, events_until, last_checked

    sh, fake = live.sh, live.fake
    core = FakeCore(sh.home)
    core.plan("update", steps=[{"event": {"event": "step", "name": "persistent_install", "status": "done",
                                          "message": "CLI updated", "agent": None}}])
    core.plan("version", stdout={"cli_version": probe.__version__, "cli_latest": "999.0.0"})
    enable_auto_update(sh.home)
    last_checked(hours_ago=1)
    _switch(sh.home, "s1", "daemon")
    sh.start()
    _record(sh, "s1", live.owner, live.root, tmp_path)
    assert wait_for(lambda: fake.events("running", "s1"), 10), sh.log()
    with sh.connect() as conn:
        conn.call(Method.EVENTS_SUBSCRIBE, {"topics": ["update.done"]})
        assert conn.call(Method.UPDATE_CHECK_NOW, {"trigger": "cli"})["outcome"] == "started"
        (done,) = events_until(conn, lambda e: e["topic"] == "update.done", 30)
    assert done["deferred"] is None, sh.log()
    assert fake.events("sigterm", "s1")[0]["handover"] is True, "asked to hand over, not to drain"
    (update,) = core.calls("update")
    assert wait_for(lambda: len(fake.events("running", "s1")) == 2, 10), sh.log()
    second = fake.starts("s1")[1]
    assert not second["held"] and not second["barrier"], "never started under the update"
    assert second["at"] > update["at"]
    assert fake.events("lock_busy") == []


# -- the worker's side ---------------------------------------------------------------


def test_the_entry_it_spawns_reaches_the_worker_s_own_arguments():
    """`<python> -I -c ENTRY daemon worker ...` is `probe daemon worker ...`:
    the CLI, its update barrier, then the worker's own parser."""
    import subprocess

    done = subprocess.run([sys.executable, "-I", "-c", workers.ENTRY, "daemon", "worker", "--source", "codex"],
                          capture_output=True, text=True, timeout=120, check=False)
    # The worker's own parser saw `--source` and wants the rest: a usage exit,
    # which the supervisor reads as a CLI without the command (no respawn).
    assert done.returncode == workers.EXIT_NO_COMMAND, (done.stdout + done.stderr)[-2000:]
    assert "probe daemon worker" in done.stderr and "--session-id" in done.stderr


def test_a_worker_knows_its_supervisor_by_identity(monkeypatch):
    """By (pid, start time), not by `getppid()`: gone once that process is
    (exited, or its pid reused), alive while it runs even when the worker is
    not its direct child (an interpreter that forked under it)."""
    import subprocess

    from probe.daemon import worker as worker_mod
    from probe.service import procid

    me = (os.getpid(), procid.start_time(os.getpid()))
    monkeypatch.setenv(worker_mod.SUPERVISOR_PID_ENV, workers.supervisor_value(SID))
    assert worker_mod.supervisor_identity(SID) == me
    assert worker_mod.supervisor_identity("another-session") is None, "only for the session it names"
    assert worker_mod.parent_gone(me, os.getppid()) is False, "alive, though not this process's parent"
    gone = subprocess.Popen(["true"])
    gone.wait()
    assert worker_mod.parent_gone((gone.pid, "1"), os.getppid()) is True
    assert worker_mod.parent_gone((os.getpid(), "not-its-start"), os.getppid()) is True, "a reused pid"
    assert worker_mod.parent_gone(None, os.getppid()) is False and worker_mod.parent_gone(None, 1) is True
    monkeypatch.setenv(worker_mod.SUPERVISOR_PID_ENV, "junk")
    assert worker_mod.supervisor_identity(SID) is None



def test_a_waiting_worker_leaves_when_the_holder_never_lets_go(tmp_path, monkeypatch):
    """`worker.session_lock` waited forever for a holder that never stops (it
    hands over only after a model round). Bounded now: EXIT_RESPAWN_LATER, and
    its ask stays fresh for whoever asks next."""
    from probe.daemon import mailbox, lease
    from probe.daemon import worker as worker_mod

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setattr(lease, "worker_wanted", lambda sid, state=None: True)
    held = _hold(worker_mod.lock_path(SID))
    try:
        started = time.monotonic()
        assert worker_mod.session_lock(SID, poll_s=0.02, max_wait_s=0.2) == worker_mod.EXIT_RESPAWN_LATER
        assert 0.2 <= time.monotonic() - started < 5
        assert mailbox.handover_path(SID).exists()
    finally:
        held.close()
    assert worker_mod.LOCK_WAIT_S >= 60, "long enough for a holder's model round"
