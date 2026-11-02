"""Pins what BackgroundHost answers, books and logs for drain / watch_box over fake children.

One scripted run; the expected record sits in background_host_golden.json beside it.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

from probe.service.jobs.background import background as mod

GOLDEN = Path(__file__).with_name("background_host_golden.json")


class FakePopen:
    """A child that exits when told to: poll/wait/kill/terminate and nothing else."""

    pids = 1000

    def __init__(self) -> None:
        FakePopen.pids += 1
        self.pid = FakePopen.pids
        self.code = None
        self.exited = threading.Event()
        self.termed = False

    def poll(self):
        return self.code

    def wait(self, timeout=None):
        if not self.exited.wait(timeout if timeout is not None else 5) and timeout is not None:
            raise subprocess.TimeoutExpired("fake", timeout)
        return self.code if self.code is not None else 0

    def kill(self) -> None:
        self.code = -9
        self.exited.set()

    def terminate(self) -> None:
        self.termed = True

    def exit_with(self, code: int) -> None:
        self.code = code
        self.exited.set()


def _wait_until_ended(host, count: int) -> None:
    deadline = time.monotonic() + 2.0
    while host.ended < count and time.monotonic() < deadline:
        time.sleep(0.01)
    assert host.ended == count


def _run_script(tmp: Path, monkeypatch) -> list:
    out: list = []
    spawned: list = []
    held = {"on": False}
    fail_spawn = {"on": False}

    def spawn(argv, env, *, cwd, log_path):
        if fail_spawn["on"]:
            raise OSError("no fork")
        popen = FakePopen()
        spawned.append((argv, sorted(env.items()), cwd, log_path))
        return popen

    monkeypatch.setattr(mod, "_is_lease_held", lambda path: held["on"])
    monkeypatch.setattr(mod.BackgroundHost, "_spawn", staticmethod(spawn))

    def host(**kw):
        logs: list = []
        return mod.BackgroundHost(log=logs.append, **kw), logs

    def books(h):
        return {
            "children": sorted(h._children), "live": len(h._live), "starting": sorted(h._starting),
            "failing": sorted(h._failing), "started": h.started, "ended": h.ended, "stopped": h.stopped,
        }

    def rec(name, answer, h, logs):
        out.append({"case": name, "answer": answer, "books": books(h), "logs": [x.split(" (pid")[0] for x in logs]})

    def age(h, seconds=10):
        for c in h._live.values():
            c.started -= seconds

    q = tmp / "q"
    q.mkdir(mode=0o700)
    q2 = tmp / "q2"
    q2.mkdir(mode=0o700)
    req = {"dir": str(q), "python": sys.executable, "env": {"A": "1"}, "cwd": None}

    h, logs = host()
    rec("unusable_python", h.drain({**req, "python": "/nonexistent/python"}), h, logs)
    h, logs = host()
    h.close()
    rec("closed", h.drain(req), h, logs)
    h, logs = host()
    rec("unusable_dir", h.drain({**req, "dir": "/nonexistent"}), h, logs)
    h, logs = host()
    held["on"] = True
    rec("lease_held", h.drain(req), h, logs)
    held["on"] = False
    h, logs = host()
    rec("started", h.drain(req), h, logs)
    rec("young_running", h.drain(req), h, logs)
    argv, env, cwd, log_path = spawned[-1]
    out.append({
        "case": "spawned", "argv": argv[1:], "env": env, "cwd_is_dir": cwd == os.path.realpath(q),
        "log": os.path.basename(log_path),
    })
    age(h)
    rec("second_child", h.drain(req), h, logs)
    age(h)
    rec("per_key_busy", h.drain(req), h, logs)

    h, logs = host(max_drains=1)
    rec("kind_first", h.drain(req), h, logs)
    rec("kind_busy", h.drain({**req, "dir": str(q2)}), h, logs)

    h, logs = host()
    incidents: list = []
    h.incident = lambda *a, **k: incidents.append([a[1], a[3]["kind"], a[3]["code"]])
    rec("pre_fail", h.drain(req), h, logs)
    next(iter(h._live.values())).popen.exit_with(1)
    _wait_until_ended(h, 1)
    rec("after_fail", h.drain(req), h, logs)
    out.append({"case": "incidents", "v": incidents})

    h, logs = host()
    h.drain(req)
    next(iter(h._live.values())).popen.exit_with(3)
    _wait_until_ended(h, 1)
    rec("clean3_then", h.drain(req), h, logs)

    fail_spawn["on"] = True
    h, logs = host()
    rec("spawn_fails", h.drain(req), h, logs)
    fail_spawn["on"] = False

    h, logs = host()
    real_start = threading.Thread.start

    def start(self):
        if self.name.startswith("probe-background-"):
            raise RuntimeError("no thread")
        return real_start(self)

    monkeypatch.setattr(threading.Thread, "start", start)
    rec("thread_fails", h.drain(req), h, logs)
    monkeypatch.setattr(threading.Thread, "start", real_start)

    h, logs = host()
    h.drain(req)
    age(h, mod.STALL_S + 1)
    rec("stall_look1", h.drain(req), h, logs)
    for c in h._live.values():
        if c.free_since is not None:
            c.free_since -= mod.STALL_CONFIRM_S + 1
        c.started -= mod.STALL_S + 1
    rec("stall_look2", h.drain(req), h, logs)
    out.append({"case": "termed", "v": sorted(c.popen.termed for c in h._live.values())})

    h, logs = host()
    box = tmp / "box"
    box.mkdir()
    rec("box", h.watch_box({"python": sys.executable, "env": {"PROBE_BOX_DIR": str(box)}, "cwd": None}), h, logs)
    out.append({"case": "box_argv", "v": spawned[-1][0][1:]})

    h, logs = host()
    h.drain(req)
    for c in h._live.values():
        c.started -= 10
        c.free_since = 5.0
    held["on"] = True
    rec("held_clears", h.drain(req), h, logs)
    held["on"] = False
    out.append({"case": "free_since", "v": [c.free_since for c in h._live.values()]})
    return out


def test_background_host_start_drain_watch_box_match_golden(tmp_path, monkeypatch) -> None:
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    work = tmp_path / "work"
    work.mkdir()
    got = _run_script(work, monkeypatch)
    text = json.dumps(got, sort_keys=True, default=str).replace(str(work), "<tmp>")
    assert json.loads(text) == json.loads(json.dumps(json.loads(GOLDEN.read_text()), sort_keys=True))
