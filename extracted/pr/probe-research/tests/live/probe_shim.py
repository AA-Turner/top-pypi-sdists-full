#!/usr/bin/env python3
"""`probe` on the live run's PATH: times every call, then runs the real CLI.

Installed as `<run>/bin/probe` ahead of `~/.local/bin` (where `uv tool install`
puts the real one), so every `probe` a hook, the tap, a stand-in session's
Bash tool or the driver runs goes through here. Each call appends one line to
`~/.live-run/probe-calls.jsonl`:

    {"argv", "start", "end", "duration_s", "exit", "barrier_at_start", "ppid"}

`barrier_at_start`: the Probe service's update barrier existed when the call
began, so the call had to wait for the update (at most
`probe.service.barrier.WAIT_S`): this machine's
(`~/.local/state/probe/service/<machine key>/update.barrier`, where today's
service raises it) or the one a service from before the machine key raises
(`service/update.barrier`), both from the checkout's copy of
`probe.service.paths` (the tap's `tap/service/paths.py`).

`probe daemon worker` is exec'd in place (its start is logged, nothing else):
the worker's lock, signals and parent are then exactly the real ones. On
Windows, which has no exec, the shim runs it as a child and waits for it.

Stdlib only; HOME decides every path (the service's update child has a clean env).
"""

from __future__ import annotations

import contextlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
TAP_ROOT = HERE.parents[1] / "plugins" / "probe-research-tap"


def _home() -> Path:
    return Path(os.environ.get("HOME") or os.path.expanduser("~"))


def _barriers() -> list[Path]:
    """Where the service raises its update barrier: the service's own path
    helpers (machine-keyed, and the legacy folder), else both by their layout."""
    try:
        if str(TAP_ROOT) not in sys.path:
            sys.path.insert(0, str(TAP_ROOT))
        from tap.service import paths

        return [paths.barrier_path(), paths.legacy_barrier_path()]
    except Exception:  # noqa: BLE001 -- a checkout without the tap's copy: its layout
        service = _home() / ".local" / "state" / "probe" / "service"
        return [*sorted(service.glob("*/update.barrier")), service / "update.barrier"]


def _real_probe() -> str:
    name = "probe.exe" if os.name == "nt" else "probe"
    return str(_home() / ".local" / "bin" / name)


def _log(record: dict) -> None:
    path = _home() / ".live-run" / "probe-calls.jsonl"
    with contextlib.suppress(OSError):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")


def standin_worker(args: list[str]) -> int:
    """`--daemon-session standin`: a daemon worker that only does what the
    service's quiet check and the tap's supervisor see -- it holds
    `<state>/probe/daemon/<sid>.lock` (flock) for its life, and exits 0 on
    SIGTERM or when its parent (the tap) is gone."""
    import fcntl

    sid = args[args.index("--session-id") + 1] if "--session-id" in args else "unknown"
    state = Path(os.environ.get("XDG_STATE_HOME") or (_home() / ".local" / "state"))
    lock = state / "probe" / "daemon" / f"{sid}.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    stop = {"now": False}

    def on_term(_signum, _frame):
        stop["now"] = True

    signal.signal(signal.SIGTERM, on_term)
    signal.signal(signal.SIGINT, on_term)
    parent = os.getppid()
    with lock.open("a") as handle:
        while not stop["now"]:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                time.sleep(1)
        while not stop["now"] and os.getppid() == parent:
            time.sleep(1)
    return 0


def main() -> int:
    argv = sys.argv[1:]
    real = _real_probe()
    barrier = any(path.exists() for path in _barriers())
    start = time.time()
    base = {"argv": argv[:6], "start": start, "barrier_at_start": barrier, "ppid": os.getppid(),
            "session": os.environ.get("CLAUDE_CODE_SESSION_ID", "")}
    if argv[:2] == ["daemon", "worker"]:
        if (_home() / ".live-run" / "standin-worker").exists():
            _log({**base, "standin_worker": True})
            return standin_worker(argv[2:])
        _log({**base, "exec": True})
        if os.name == "nt":
            # Windows has no exec: os.execv starts a new process and this one
            # exits 0 at once, so the tap's supervisor saw its worker exit and
            # started another (5 a minute), each waiting for the session lock:
            # ~100 leaked workers in 20 min, and a runner out of memory. Wait.
            return subprocess.call([real, *argv])
        os.execv(real, [real, *argv])
    try:
        child = subprocess.Popen([real, *argv])
    except OSError as exc:
        _log({**base, "end": time.time(), "duration_s": 0.0, "exit": 127, "error": str(exc)})
        print(f"probe (live-run shim): cannot run {real}: {exc}", file=sys.stderr)
        return 127

    def forward(signum, _frame):
        with contextlib.suppress(OSError):
            child.send_signal(signum)

    for name in ("SIGTERM", "SIGINT", "SIGHUP"):
        if hasattr(signal, name):
            with contextlib.suppress(OSError, ValueError):
                signal.signal(getattr(signal, name), forward)
    code = child.wait()
    end = time.time()
    _log({**base, "end": end, "duration_s": round(end - start, 3), "exit": code})
    return 128 - code if code < 0 else code


if __name__ == "__main__":
    sys.exit(main())
