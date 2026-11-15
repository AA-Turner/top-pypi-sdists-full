"""Closing a browser waits, and the wait is not the event loop's.

The close of a browser waits for its processes to exit, ends the survivors of its tree and removes its profile: seconds of
waiting, which is how Playwright's own `close()` behaves too (it returns once the processes are gone). What was wrong is WHO
waited. With four browsers in one Python process py-spy put about a fifth of the main thread in the wait for the exit
(`psutil.wait_procs`) and the removal of the profile (`rmtree`) when one of them closed, all on the event loop that serves the other
three, plus a scan of every process of the machine, its environment read, to find the tree to end.

Now:

* the tree of a launch is known from the launch, never searched for: its job on Windows, its engine's descendants on POSIX
  (`process.EngineTree`); `find_processes` and `reap_session` of a token a launch registered read nothing of the machine;
* the close has a form an event loop can await (`Browser.aclose`, `Connection.aclose`, `SessionFiles.aremove`), which runs the same
  close in a thread of its own: the contract (it returns when the processes are gone and the profile is removed) is the same, only
  the thread that waits is not the loop's.

The tests stand a Python process in for the engine (what is measured is the teardown, not the browser): it answers the Juggler
pipe, has two children of its own and, when its pipe closes, ends them, starts a straggler (as the pingsender is, which outlives
the browser) and exits. They run in a client program of their own, as the spawn tests of this suite do: the real spawn of the
platform (`_spawn_windows`, `_spawn_posix`), the real `instance.launch` and `Browser`, on Linux and on Windows.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
import time

import pytest

from invisible_core import process as P

WINDOWS = sys.platform == "win32"

#: What stands for the engine. It answers every command on the Juggler pipe (fds 3 and 4 on POSIX, the handles named by
#: PW_PIPE_READ/PW_PIPE_WRITE on Windows), starts two children, and says so. When the pipe closes it ends its children, starts a
#: straggler that runs for a while longer (the pingsender) and says its pid, and 0.4 s after that, in the last milliseconds
#: before it exits, starts one more child that would run for two minutes (`{late}` is its sleep, 0 for none). That one is born
#: after any listing a close could have made while the engine was alive: only a tree that holds it by construction ends it.
_ENGINE = textwrap.dedent("""
    import json, os, subprocess, sys, time
    if os.name == "nt":
        import msvcrt
        r = msvcrt.open_osfhandle(int(os.environ["PW_PIPE_READ"]), os.O_RDONLY)
        w = msvcrt.open_osfhandle(int(os.environ["PW_PIPE_WRITE"]), 0)
    else:
        r, w = 3, 4
    SLEEP = [sys.executable, "-c", "import time; time.sleep({straggle})"]
    kids = [subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"]) for _ in range(2)]
    print("PIDS", os.getpid(), *[k.pid for k in kids], flush=True)
    print("Juggler listening to the pipe", flush=True)
    buffer = b""
    while True:
        data = os.read(r, 65536)
        if not data:
            break
        buffer += data
        while b"\\0" in buffer:
            raw, buffer = buffer.split(b"\\0", 1)
            if raw:
                message = json.loads(raw)
                os.write(w, json.dumps({{"id": message["id"], "result": {{}}}}).encode() + b"\\0")
    for k in kids:
        k.kill()
    sender = subprocess.Popen(SLEEP)
    print("PIDS", sender.pid, flush=True)
    time.sleep(0.4)
    if {late}:
        late = subprocess.Popen([sys.executable, "-c", "import time; time.sleep({late})"])
        print("PIDS", late.pid, flush=True)
        os._exit(0)
""")

#: The client: two browsers made by the real `instance.launch` (only the executable is the stand-in), one closed while a sentinel
#: task on the loop measures how long the loop stays still, then the other. Prints one JSON line.
_CLIENT = textwrap.dedent("""
    import asyncio, json, os, sys, threading, time, traceback
    import psutil
    from invisible_core.juggler import connection, instance
    from invisible_core.process import SessionToken, find_processes

    ENGINE = {engine!r}
    real = {{"nt": connection._spawn_windows, "posix": connection._spawn_posix}}
    spawn = real["nt" if os.name == "nt" else "posix"]

    def stand_in(executable, argv, env):
        return spawn(sys.executable, ["-c", ENGINE], env)

    connection._spawn_windows = connection._spawn_posix = stand_in
    # What a straggler is let to finish is 10 s in the product; here it is short, and the one that never finishes is ended after it.
    from invisible_core.juggler import _profile
    SUBREAPER = sys.argv[2:] == ["subreaper"]
    if SUBREAPER:
        # A client that is the init of its orphans and does not reap them: the PID 1 of a container without one. What the engine
        # leaves behind becomes this process's child and, when it ends, a zombie nobody collects. The grace stays the product's.
        import ctypes
        assert ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) == 0      # PR_SET_CHILD_SUBREAPER
    else:
        _profile.SENDER_GRACE = 1.0

    def launch():
        token = SessionToken.mint()
        return token, instance.launch("engine", prefs={{"a": True}}, env=token.stamp(dict(os.environ)),
                                      ready_timeout=60)

    def pids_of(browser):
        out = []
        for line in browser.conn.output.tail(200):
            if line.startswith("PIDS"):
                out += [int(x) for x in line.split()[1:]]
        return out

    def alive(pids):
        return [p for p in pids if psutil.pid_exists(p) and psutil.Process(p).status() != psutil.STATUS_ZOMBIE]

    async def close(browser):
        if sys.argv[1] == "inline":
            browser.close()           # the control: the same close, made on the loop itself
        else:
            await browser.aclose()

    async def main():
        (ta, a), (tb, b) = launch(), launch()
        time.sleep(0.5)
        pa, pb = pids_of(a), pids_of(b)
        scans = []
        real_iter, real_environ = psutil.process_iter, psutil.Process.environ
        psutil.process_iter = lambda *x, **k: (scans.append("process_iter"), real_iter(*x, **k))[1]
        psutil.Process.environ = lambda self: (scans.append("environ"), real_environ(self))[1]

        stop, gaps = asyncio.Event(), []
        beat, holes, over = [time.monotonic()], [], threading.Event()
        main_id = threading.get_ident()

        async def sentinel():
            last = time.monotonic()
            while not stop.is_set():
                await asyncio.sleep(0.005)
                now = time.monotonic()
                gaps.append(now - last)
                last = beat[0] = now

        def stacks():
            frames = sys._current_frames()
            names = {{t.ident: t.name for t in threading.enumerate()}}
            return {{
                "main": "".join(traceback.format_stack(frames[main_id])[-6:]),
                "others": {{names.get(i, str(i)): "".join(traceback.format_stack(f)[-3:])
                           for i, f in frames.items() if i != main_id and i != threading.get_ident()}}}}

        def idle(frame):
            # True when the main thread is waiting in the event loop's selector: it is not running anything of anybody's.
            for _ in range(3):
                if frame is None:
                    return False
                code = frame.f_code
                if code.co_name in ("_poll", "select") and code.co_filename.endswith(("windows_events.py", "selectors.py")):
                    return True
                frame = frame.f_back
            return False

        held = [0.0]

        def watcher():
            # A loop that wakes late has two very different causes. The machine did not schedule it (a loaded host: an idle
            # loop with nothing in it is 140 ms late now and then, measured), and then the main thread is idle in the
            # selector; or something holds it, and then the main thread is INSIDE that something. `held` is the lateness of
            # the second kind only, which is what a close on the loop is. Each 30 ms of lateness takes a look at every
            # thread, so a failure names where they were instead of a number.
            looked = 0
            while not over.is_set():
                time.sleep(0.003)
                late = time.monotonic() - beat[0]
                level = int(late / 0.03)
                if late > 0.03 and not idle(sys._current_frames().get(main_id)):
                    held[0] = max(held[0], late)
                if level > looked:
                    holes.append({{"late_ms": round(late * 1000), **stacks()}})
                looked = level

        # What the loop's own thread runs while the close is awaited: every blocking step a close makes, by the thread that made it.
        import shutil
        on_the_loop, real = [], {{}}

        def watched(owner, name):
            real[(owner, name)] = original = getattr(owner, name)

            def call(*x, **k):
                if threading.get_ident() == main_id and not over.is_set():
                    on_the_loop.append(name)
                return original(*x, **k)
            setattr(owner, name, call)

        watched(time, "sleep")
        watched(os, "close")
        watched(shutil, "rmtree")
        watched(psutil, "wait_procs")

        threading.Thread(target=watcher, daemon=True, name="the-watcher").start()
        watch = asyncio.create_task(sentinel())
        await asyncio.sleep(0.1)
        files_a = (a._files.profile, a._files.tmp)
        leader = None if os.name == "nt" else (os.getpgid(pa[0]) == pa[0] != os.getpgrp())
        started = time.monotonic()
        await close(a)
        took = time.monotonic() - started
        stop.set()
        await watch
        over.set()
        for (owner, name), original in real.items():
            setattr(owner, name, original)
        psutil.process_iter, psutil.Process.environ = real_iter, real_environ
        time.sleep(0.2)
        pa = pids_of(a)                       # the straggler's pid is printed while it closes
        report = {{
            "gap": max(gaps), "took": took, "scans": scans, "leader": leader, "holes": holes[:4], "held": held[0], "on_the_loop": on_the_loop,
            "a_pids": len(pa), "a_alive": alive(pa),
            "a_dirs": [d for d in files_a if os.path.exists(d)],
            "zombies": [p for p in pa if psutil.pid_exists(p) and psutil.Process(p).status() == psutil.STATUS_ZOMBIE],
            "b_pids": len(pb), "b_alive": alive(pb),
            "b_dirs": [d for d in (b._files.profile, b._files.tmp) if os.path.exists(d)],
        }}
        await close(b)
        pb = pids_of(b)
        report["b_closed_alive"] = alive(pb)
        report["b_closed_dirs"] = [d for d in (b._files.profile, b._files.tmp) if os.path.exists(d)]
        report["token_a_listed"] = len(find_processes(ta))
        print("REPORT", json.dumps(report), flush=True)

    asyncio.run(main())
""")


def _run_client(tmp_path, engine, how, *more):
    script = tmp_path / "client.py"
    script.write_text(_CLIENT.format(engine=engine), encoding="utf-8")
    done = subprocess.run([sys.executable, str(script), how, *more], capture_output=True, text=True, timeout=180)
    lines = [x for x in done.stdout.splitlines() if x.startswith("REPORT ")]
    assert done.returncode == 0 and lines, (
        "the client failed (%s):\n%s\n%s" % (done.returncode, done.stdout[-2000:], done.stderr[-4000:]))
    return json.loads(lines[-1][len("REPORT "):])


def _holes(report):
    """What the client saw while its loop was late: the main thread's stack and the other threads' tops."""
    out = []
    for hole in report.get("holes") or []:
        out.append("--- the loop was %d ms late. MAIN THREAD:\n%s" % (hole["late_ms"], hole["main"]))
        for name, stack in hole["others"].items():
            out.append("--- thread %s:\n%s" % (name, stack))
    return "\n".join(out) or "(no look was taken: the lateness was gone before a look, or the whole process was not scheduled)"


@pytest.fixture(scope="module")
def report(tmp_path_factory):
    """One run of the client: its numbers are asserted one claim at a time below."""
    return _run_client(tmp_path_factory.mktemp("teardown"), _ENGINE.format(straggle=2, late=120), "aclose")


@pytest.fixture(scope="module")
def subreaped(tmp_path_factory):
    """One run of the client as the parent of its orphans that never reaps them: the straggler lives 1 s."""
    return _run_client(tmp_path_factory.mktemp("subreaper"), _ENGINE.format(straggle=1, late=0), "aclose", "subreaper")


@pytest.fixture(scope="module")
def control(tmp_path_factory):
    """The same run with the close made inline on the loop."""
    return _run_client(tmp_path_factory.mktemp("control"), _ENGINE.format(straggle=2, late=0), "inline")


pytestmark = pytest.mark.integration


@pytest.mark.wall_clock
def test_the_instrument_sees_a_loop_that_is_held(control):
    """The control: closed inline, the loop stands still for the whole close. Without this, a sentinel that could not see a held
    loop would pass the test below for nothing."""
    assert control["gap"] > 0.5 * control["took"] > 0.15, (
        "the sentinel did not notice a close made on the loop itself: gap %.0f ms of a close of %.0f ms"
        % (control["gap"] * 1000, control["took"] * 1000))
    assert control["held"] > 0.5 * control["took"], (
        "the watcher did not tell a held loop from a starved one: held %.0f ms of a close of %.0f ms"
        % (control["held"] * 1000, control["took"] * 1000))
    assert control["on_the_loop"], "no blocking step of the close was seen on the loop's thread, closing it there"


@pytest.mark.wall_clock
def test_the_loop_is_not_held_while_a_browser_closes(report):
    """The loop stood still for the whole of the close, seconds, when a client made it on the loop. A sentinel task asks to wake every
    5 ms and the watcher thread writes down how late it was, and where the main thread was: waiting in the selector (the machine did
    not run it: on a loaded host an idle loop is 140 ms late now and then, so that is not the close's doing and is not counted), or
    inside something (held). Nothing may hold it for 50 ms."""
    assert report["took"] > 0.3, "the close finished before the engine could have exited: nothing was waited for"
    assert report["held"] < 0.05, (
        "the loop was held for %.0f ms while a browser closed (the close took %.0f ms; the longest wake was %.0f ms late). "
        "Where the threads were while it was late:\n%s"
        % (report["held"] * 1000, report["took"] * 1000, report["gap"] * 1000, _holes(report)))


def test_no_blocking_step_of_the_close_runs_on_the_loop_s_thread(report):
    """The cause, asked directly and without the clock: `time.sleep`, `os.close`, `rmtree` and `psutil.wait_procs` are what a close
    does while it waits and removes, and none of them may be called by the thread that runs the loop. Red on a close made inline."""
    assert report["on_the_loop"] == [], "the loop's own thread made these calls while it awaited the close: %s" % report["on_the_loop"]


def test_closing_a_browser_reads_no_process_of_the_machine_and_no_environment(report):
    """Red on the token search: `find_processes` asks `psutil.process_iter` for every process and reads the environment of each."""
    assert report["scans"] == [], "the close scanned the machine: %d calls (%s)" % (
        len(report["scans"]), sorted(set(report["scans"])))


def test_after_close_no_process_of_the_tree_is_alive_and_the_profile_is_gone(report):
    """The contract of `close()` does not change: it returns when the processes have exited. The straggler (the pingsender: it
    outlives the browser and is the process that kept a profile from being removed) and a child born in the last milliseconds of
    the engine, which outlives it for good, are in the tree of the launch: a tree LISTED while the engine was alive (every 0.1 s, say)
    cannot hold the second; one the launch is born as the leader of (a process group, a job) does."""
    assert report["a_pids"] == 5, "the engine, its two children, the straggler and the last child were not all counted: %r" % report
    assert report["a_alive"] == [], "processes of the closed browser are alive: %s" % report["a_alive"]
    assert report["a_dirs"] == [], "the closed browser left its directories: %s" % report["a_dirs"]
    assert report["token_a_listed"] == 0, "the session's token still lists processes after the close"


def test_closing_one_browser_does_not_touch_the_other(report):
    """Two browsers in one process: the first one's close ends its own tree and nothing of the second's, and then the second closes
    the same way."""
    assert report["b_pids"] == 3
    assert len(report["b_alive"]) == 3, "closing the first browser ended a process of the second: %r" % report
    assert report["b_dirs"] != [] and len(report["b_dirs"]) == 2, "the second browser's directories went with the first's"
    assert report["b_closed_alive"] == [], "the second browser's tree is not gone after its own close: %s" % report["b_closed_alive"]
    assert report["b_closed_dirs"] == []


# ── the pieces, without a launch ────────────────────────────────────────────

class _NoSearch:
    """`psutil` that records a search of the machine and answers nothing, for the calls that must not make one."""

    def __init__(self, monkeypatch):
        import psutil

        self.calls = []
        monkeypatch.setattr(psutil, "process_iter",
                            lambda *a, **k: (self.calls.append("process_iter"), iter(()))[1])
        monkeypatch.setattr(psutil.Process, "environ",
                            lambda proc: (self.calls.append("environ"), {})[1])


@pytest.mark.unit
def test_a_registered_token_is_listed_and_ended_from_its_tree_not_searched(monkeypatch):
    import psutil

    searched = _NoSearch(monkeypatch)
    token = P.SessionToken.mint()
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        tree = P.EngineTree(child.pid)
        P.register_tree(token, tree)
        assert [p.pid for p in P.find_processes(token)] == [child.pid]
        assert P.reap_session(token, timeout=5) == 1
        child.wait(timeout=10)
        assert P.find_processes(token) == []
        assert not psutil.pid_exists(child.pid) or child.poll() is not None
        assert searched.calls == [], "a registered token was searched for: %s" % searched.calls
    finally:
        if child.poll() is None:
            child.kill()
            child.wait()


@pytest.mark.unit
def test_a_token_no_launch_registered_is_still_searched_for(monkeypatch):
    """What `find_processes` is still for: a tree that was not launched by this core (the search reads the token from each environment)."""
    seen = []
    import psutil

    monkeypatch.setattr(psutil, "process_iter", lambda *a, **k: (seen.append(1), iter(()))[1])
    assert P.find_processes(P.SessionToken.mint()) == []
    assert seen == [1]


_GRANDCHILD = ("import subprocess, sys, time; "
               "k = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)']); "
               "print(k.pid, flush=True); time.sleep(60)")


@pytest.mark.unit
def test_the_tree_of_an_engine_is_its_descendants_listed_in_one_pass():
    import psutil

    engine = subprocess.Popen([sys.executable, "-c", _GRANDCHILD], stdout=subprocess.PIPE, text=True)
    try:
        grandchild = int(engine.stdout.readline())
        tree = P.EngineTree(engine.pid)
        assert {p.pid for p in tree.members()} == {engine.pid, grandchild}
        tree.remember()
        engine.kill()
        engine.wait()
        # The engine is gone and its child is reparented: it is still the tree's, because it was listed while its parent lived.
        assert {p.pid for p in tree.members()} == {grandchild}
        assert tree.end(timeout=5) == 1
        assert tree.members() == []
        assert not psutil.pid_exists(grandchild) or not psutil.Process(grandchild).is_running()
    finally:
        engine.kill()


@pytest.mark.unit
def test_an_engine_that_has_been_reaped_does_not_name_a_process_that_reuses_its_pid():
    """The tree holds process objects with their creation time, so a pid the system reused is not the one that was listed."""
    engine = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    tree = P.EngineTree(engine.pid)
    engine.kill()
    engine.wait()
    assert tree.members() == []


@pytest.mark.unit
@pytest.mark.skipif(not WINDOWS, reason="the job object is Windows")
def test_a_job_lists_and_ends_its_own_tree_and_only_it():
    """`EngineJob.pids` lists what is in the job by its own account (the job of another launch holds its own), `terminate` ends all of it."""
    import ctypes
    from ctypes import wintypes

    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    k.AssignProcessToJobObject.restype = wintypes.BOOL
    a, b = P.EngineJob.create(), P.EngineJob.create()
    procs = []
    try:
        for job in (a, b):
            proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], creationflags=0x4)
            procs.append(proc)
            assert k.AssignProcessToJobObject(job.handle, int(proc._handle))
            import psutil
            psutil.Process(proc.pid).resume()
        assert a.pids() == [procs[0].pid] and b.pids() == [procs[1].pid]
        a.terminate()
        assert a.wait_empty(time.monotonic() + 10) is True
        assert procs[0].wait(timeout=10) is not None
        assert procs[1].poll() is None, "ending one job ended the other's process"
        assert b.pids() == [procs[1].pid]
    finally:
        for job in (a, b):
            job.close()
        for proc in procs:
            if proc.poll() is None:
                proc.kill()
                proc.wait()


@pytest.mark.skipif(WINDOWS, reason="process groups are POSIX")
def test_the_engine_is_born_the_leader_of_a_process_group_of_its_own(report):
    """The tree is the group: the engine's pid is its group's, and not the client's (Playwright's launcher: `detached: true`)."""
    assert report["leader"] is True


@pytest.mark.unit
@pytest.mark.skipif(WINDOWS, reason="process groups are POSIX")
def test_a_group_is_waited_for_and_ended_whole_with_nothing_listed(monkeypatch):
    """The leader exits and leaves a child behind: the group still holds it (`killpg(pgid, 0)`), and `end` ends it, listing
    and scanning nothing."""
    searched = _NoSearch(monkeypatch)
    leader = subprocess.Popen(
        [sys.executable, "-c",
         "import subprocess, sys; "
         "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)']); print('up', flush=True)"],
        process_group=0, stdout=subprocess.PIPE, text=True)
    try:
        assert leader.stdout.readline().strip() == "up"
        leader.wait(timeout=10)
        tree = P.EngineTree(leader.pid, group=True, poll=leader.poll)
        assert tree._group_alive(), "the child the leader left behind is not in its group"
        assert tree.end(timeout=5) == 1
        assert not tree._group_alive()
        assert searched.calls == [], "ending a group read the machine: %s" % searched.calls
    finally:
        try:
            os.killpg(leader.pid, 9)
        except OSError:
            pass


@pytest.mark.unit
@pytest.mark.skipif(WINDOWS, reason="process groups are POSIX")
def test_a_group_that_has_been_seen_empty_is_never_signalled_again(monkeypatch):
    """Its number may belong to an unrelated process group by then."""
    leader = subprocess.Popen([sys.executable, "-c", "pass"], process_group=0)
    leader.wait(timeout=10)
    tree = P.EngineTree(leader.pid, group=True, poll=leader.poll)
    assert tree.end(timeout=1) == 0 and tree._gone
    sent = []
    monkeypatch.setattr(os, "killpg", lambda *a: sent.append(a))
    assert tree.end(timeout=1) == 0
    assert sent == [], "a group that was empty was signalled: %s" % sent


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="a client that is its orphans' init, and /proc: Linux")
def test_a_group_of_zombies_is_empty_so_a_close_does_not_wait_for_nobody(subreaped):
    """Red when the group is waited for with `killpg(pgid, 0)` alone, which answers for a zombie too: in a container whose PID 1 is
    the user's script, the straggler that outlived the engine stays a zombie nobody reaps, the group looks alive, and every close
    waited the 10 s a straggler is given and then the 5 s of the SIGTERM. The client here is the init of its orphans and reaps none."""
    assert subreaped["zombies"], "the setup is not the one under test: nothing was left a zombie: %r" % subreaped
    assert subreaped["took"] < 1 + 2, (
        "the close waited %.1f s for a group of zombies (the straggler lives 1 s)" % subreaped["took"])
    assert subreaped["held"] < 0.05, "the loop was held for %.0f ms:\n%s" % (subreaped["held"] * 1000, _holes(subreaped))
    assert subreaped["a_dirs"] == [], "the closed browser left its directories: %s" % subreaped["a_dirs"]
