"""What the person's own programs are doing on a Cloud Computer (idle evidence).

The platform's stack (the worker, Chrome, Xvfb, the stream, the window manager,
taskbar, audio) is excluded by process name: its CPU is not the person working.
Browser activity is counted by the control plane from browser commands and
input, never here. Everything else — a shell job, a compiler, a terminal the
person types in — is reported as cumulative CPU ticks so two readings show
whether anything ran in between.

CPU alone misses work that waits on the network (a download, an upload, a
build fetching packages: review D7, 2026-10-18), so the reading also carries
the I/O those programs did (``/proc/<pid>/io``), the machine's network bytes
(``/proc/net/dev``), each as a rate since the previous reading, and the agent
shell work still running (processes under the agent daemon, agent calls in
flight). The control plane never moves a build while any of it is non-zero.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

#: Process names (``/proc/<pid>/comm``, max 15 chars) of the platform's own
#: always-busy stack. Generic names (python, bash, sh) are NOT here: a person's
#: script is often exactly that. The worker itself is excluded by pid instead,
#: and an idle shell or entrypoint script uses no CPU, so it never reads as
#: activity (growth between readings is what counts).
PLATFORM_PROCESSES = frozenset(
    {
        "Xvfb",
        "chrome",
        "chrome_crashpad",
        "chrome_crashpad_handler",
        "chromium",
        "nacl_helper",
        "selkies-gstreame",
        "selkies",
        "gst-plugin-scan",
        "openbox",
        "tint2",
        # The desktop icons/wallpaper (redraws whenever the screen changes),
        # the container's init, and the entrypoint's user switch — measured
        # ticking on an idle live machine 2026-10-17.
        "pcmanfm",
        "init",
        "runuser",
        "pulseaudio",
        "dbus-daemon",
        "dbus-launch",
        "tini",
        "dumb-init",
        "turnserver",
        "amazon-ssm-agen",
        "ssm-agent-worke",
        "ssm-session-wor",
        "xdotool",
        "scrot",
        "at-spi-bus-laun",
        "at-spi2-registr",
        "Thread<00>",
    }
)


def _read(path: Path) -> str | None:
    try:
        return path.read_text()
    except OSError:
        return None


def read_input_idle_ms(display: str | None = None) -> int | None:
    """Milliseconds since the last keyboard/mouse input on the desktop's X
    server (MIT-SCREEN-SAVER, ``libXss`` — a Chrome dependency, so present on
    every image). The stream injects input through X, so this is the person
    typing or clicking. None when there is no X server to ask."""
    import ctypes

    try:
        xlib = ctypes.cdll.LoadLibrary("libX11.so.6")
        xss = ctypes.cdll.LoadLibrary("libXss.so.1")
    except OSError:
        return None

    class _Info(ctypes.Structure):
        _fields_ = [
            ("window", ctypes.c_ulong),
            ("state", ctypes.c_int),
            ("kind", ctypes.c_int),
            ("til_or_since", ctypes.c_ulong),
            ("idle", ctypes.c_ulong),
            ("event_mask", ctypes.c_ulong),
        ]

    xlib.XOpenDisplay.restype = ctypes.c_void_p
    xlib.XOpenDisplay.argtypes = [ctypes.c_char_p]
    xlib.XDefaultRootWindow.restype = ctypes.c_ulong
    xlib.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
    xlib.XCloseDisplay.argtypes = [ctypes.c_void_p]
    xlib.XFree.argtypes = [ctypes.c_void_p]
    xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(_Info)
    xss.XScreenSaverQueryInfo.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(_Info)]
    if display is None:
        # The desktop's own X server: its socket names the display number.
        sockets = sorted(Path("/tmp/.X11-unix").glob("X*"))
        if not sockets:
            return None
        display = f":{sockets[0].name[1:]}"
    name = display
    dpy = xlib.XOpenDisplay(name.encode())
    if not dpy:
        return None
    try:
        info = xss.XScreenSaverAllocInfo()
        if not info:
            return None
        try:
            if not xss.XScreenSaverQueryInfo(dpy, xlib.XDefaultRootWindow(dpy), info):
                return None
            return int(info.contents.idle)
        finally:
            xlib.XFree(info)
    finally:
        xlib.XCloseDisplay(dpy)


class InFlight:
    """Agent calls running right now through the machine's ``/agent`` door."""

    def __init__(self) -> None:
        self.count = 0

    def __enter__(self) -> InFlight:
        self.count += 1
        return self

    def __exit__(self, *_: object) -> None:
        self.count -= 1


AGENT_CALLS = InFlight()

#: The previous reading's counters, so each reading reports a rate.
_last_sample: dict[str, float] = {}


def _rate(key: str, value: int | None, now: float, sample: dict[str, float]) -> float | None:
    """Bytes per second since the previous reading (None for the first one)."""
    if value is None:
        return None
    prev_t, prev_v = sample.get(f"{key}_t"), sample.get(key)
    sample[f"{key}_t"], sample[key] = now, float(value)
    if prev_t is None or prev_v is None or now <= prev_t or value < prev_v:
        return None
    return (value - prev_v) / (now - prev_t)


def read_net_bytes(proc_root: str = "/proc") -> int | None:
    """Received + sent bytes on every interface but loopback (None when unreadable)."""
    text = _read(Path(proc_root) / "net/dev")
    if text is None:
        return None
    total = 0
    for line in text.splitlines()[2:]:
        if ":" not in line:
            continue
        name, data = line.split(":", 1)
        cols = data.split()
        if name.strip() == "lo" or len(cols) < 9:
            continue
        try:
            total += int(cols[0]) + int(cols[8])
        except ValueError:
            continue
    return total


def _io_bytes(entry: Path) -> int | None:
    """``rchar + wchar`` of one process: every read and write, sockets included."""
    text = _read(entry / "io")
    if text is None:
        return None
    vals = dict(line.split(":", 1) for line in text.splitlines() if ":" in line)
    try:
        return int(vals.get("rchar", 0)) + int(vals.get("wchar", 0))
    except ValueError:
        return None


def read_machine_activity(
    proc_root: str = "/proc",
    *,
    agent_pid: int | None = None,
    work: dict[str, Any] | None = None,
    clock: Any = time.monotonic,
    sample: dict[str, float] | None = None,
) -> dict[str, object]:
    root = Path(proc_root)
    if not root.is_dir():
        return {"available": False, "reason": "no /proc on this host"}
    sample = _last_sample if sample is None else sample
    own = {os.getpid(), os.getppid()}
    ticks = 0
    running = 0
    io_total = 0
    io_known = False
    names: set[str] = set()
    parents: dict[int, int] = {}
    for entry in root.iterdir():
        if not entry.name.isdigit():
            continue
        stat = _read(entry / "stat")
        if not stat or ")" not in stat:
            continue
        # comm is inside the LAST parentheses; fields after it are space-separated.
        fields = stat[stat.rindex(")") + 2 :].split()
        if len(fields) >= 2 and fields[1].isdigit():
            parents[int(entry.name)] = int(fields[1])
        if int(entry.name) in own:
            continue
        comm = stat[stat.index("(") + 1 : stat.rindex(")")]
        if comm in PLATFORM_PROCESSES:
            continue
        if len(fields) < 13:
            continue
        state = fields[0]
        # utime + stime are fields 14 and 15 of /proc/<pid>/stat (index 11, 12 here).
        try:
            ticks += int(fields[11]) + int(fields[12])
        except ValueError:
            continue
        if state in {"R", "D"}:
            running += 1
        names.add(comm)
        io = _io_bytes(entry)
        if io is not None:
            io_total += io
            io_known = True
    agent_jobs = None
    if agent_pid is not None:
        # Every live process under the agent daemon: a running or backgrounded
        # agent shell command, an open agent terminal.
        agent_jobs = 0
        for pid in parents:
            parent, hops = parents.get(pid), 0
            while parent is not None and parent > 1 and hops < 64:
                if parent == agent_pid:
                    agent_jobs += 1
                    break
                parent, hops = parents.get(parent), hops + 1
    now = clock()
    return {
        "available": True,
        "foreign_cpu_ticks": ticks,
        "foreign_running": running,
        "foreign_processes": sorted(names)[:50],
        "input_idle_ms": read_input_idle_ms(),
        "foreign_io_bytes_per_second": _rate("io", io_total if io_known else None, now, sample),
        "net_bytes_per_second": _rate("net", read_net_bytes(proc_root), now, sample),
        "agent_calls_in_flight": AGENT_CALLS.count,
        "agent_jobs": agent_jobs,
        "cloud_files": work,
        #: The control plane moves a build only on a reading that carries these.
        "work_signals": 1,
    }
