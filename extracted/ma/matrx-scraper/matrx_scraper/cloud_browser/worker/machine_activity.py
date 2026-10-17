"""What the person's own programs are doing on a Cloud Computer (idle evidence).

The platform's stack (the worker, Chrome, Xvfb, the stream, the window manager,
taskbar, audio) is excluded by process name: its CPU is not the person working.
Browser activity is counted by the control plane from browser commands and
input, never here. Everything else — a shell job, a compiler, a terminal the
person types in — is reported as cumulative CPU ticks so two readings show
whether anything ran in between.
"""

from __future__ import annotations

import os
from pathlib import Path

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


def read_machine_activity(proc_root: str = "/proc") -> dict[str, object]:
    root = Path(proc_root)
    if not root.is_dir():
        return {"available": False, "reason": "no /proc on this host"}
    own = {os.getpid(), os.getppid()}
    ticks = 0
    running = 0
    names: set[str] = set()
    for entry in root.iterdir():
        if not entry.name.isdigit() or int(entry.name) in own:
            continue
        stat = _read(entry / "stat")
        if not stat or ")" not in stat:
            continue
        # comm is inside the LAST parentheses; fields after it are space-separated.
        comm = stat[stat.index("(") + 1 : stat.rindex(")")]
        if comm in PLATFORM_PROCESSES:
            continue
        fields = stat[stat.rindex(")") + 2 :].split()
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
    return {
        "available": True,
        "foreign_cpu_ticks": ticks,
        "foreign_running": running,
        "foreign_processes": sorted(names)[:50],
        "input_idle_ms": read_input_idle_ms(),
    }
