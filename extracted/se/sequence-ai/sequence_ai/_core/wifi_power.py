"""
Wi-Fi power saving on the link a robot acts over: said once a process, with how to turn it off. Linux alone, read only.

In one sentence: the first connection to a worker starts the check, on a thread of its own so no connection waits on it
→ the interface of the machine's default route (/proc/net/route, the lowest metric of them) → Wi-Fi when
/sys/class/net/<it>/wireless is there → its power saving as `iw dev <it> get power_save` says it, else as `iwconfig
<it>` says its Power Management → on: said once a process, with the command that turns it off and the setting that
keeps it off. Nothing on the machine is changed, and what cannot be read says nothing.

WHY: with power saving on, a Wi-Fi card dozes between its access point's beacons, and what comes for it waits until it
wakes - an act's answer among it. A robot on Wi-Fi alone keeps its link awake by turning power saving off.

"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import threading
from typing import Callable, Optional

from .warn import warn

_ROUTE = "/proc/net/route"
_NET = "/sys/class/net"

_SBIN = ("/usr/sbin", "/sbin", "/usr/bin", "/bin")

_READS = ((("iw", "dev", "{iface}", "get", "power_save"), re.compile(r"Power save:\s*(on|off)", re.I)),
          (("iwconfig", "{iface}"), re.compile(r"Power Management:\s*(on|off)", re.I)))

_STARTED = threading.Event()
_LOCK = threading.Lock()


def words(iface: str) -> str:
    """What is said of `iface` with its power saving on."""
    return (f"Wi-Fi power saving is on for {iface}, so its card can hold this robot's packets back while it dozes; "
            f"`sudo iw dev {iface} set power_save off` turns it off until the next reboot, and `wifi.powersave = 2` "
            "under [connection] in a file in /etc/NetworkManager/conf.d/ keeps it off")


def default_iface(route: str = _ROUTE) -> Optional[str]:
    """The interface of the machine's default route, the lowest metric of them; None where it has none, or it cannot
    be read (not Linux)."""
    try:
        with open(route) as f:
            rows = [line.split() for line in f.read().splitlines()[1:]]
    except OSError:
        return None
    best: Optional[tuple] = None
    for row in rows:

        if len(row) < 8 or row[1] != "00000000" or row[7] != "00000000":
            continue
        try:
            up, metric = int(row[3], 16) & 1, int(row[6])
        except ValueError:
            continue
        if up and (best is None or metric < best[0]):
            best = (metric, row[0])
    return best[1] if best else None


def _tool(name: str) -> Optional[str]:
    return shutil.which(name) or next((os.path.join(d, name) for d in _SBIN if os.access(os.path.join(d, name),
                                                                                         os.X_OK)), None)


def power_save_on(iface: str, *, net: str = _NET, run: Callable[..., subprocess.CompletedProcess] = subprocess.run,
                  tool: Callable[[str], Optional[str]] = _tool) -> Optional[bool]:
    """Whether Wi-Fi power saving is on for `iface`: None when it is no Wi-Fi interface, or neither tool is there to say
    or says it."""
    if not os.path.isdir(os.path.join(net, iface, "wireless")):
        return None
    for command, said in _READS:
        path = tool(command[0])
        if path is None:
            continue
        try:
            out = run([path, *(part.format(iface=iface) for part in command[1:])], capture_output=True, text=True,
                      timeout=2.0, check=False).stdout
        except (OSError, subprocess.SubprocessError):
            continue
        found = said.search(out or "")
        if found:
            return found.group(1).lower() == "on"
    return None


def check(route: str = _ROUTE, **kw) -> Optional[str]:
    """The Wi-Fi interface of the machine's default route when its power saving is on, said; else None."""
    iface = default_iface(route)
    if iface is None or not power_save_on(iface, **kw):
        return None
    warn(words(iface))
    return iface


def check_once(*, linux: bool = sys.platform.startswith("linux")) -> Optional[threading.Thread]:
    """The check, once a process, on a thread of its own (see the module); the thread, or None where nothing started."""
    if not linux or _STARTED.is_set():
        return None
    with _LOCK:
        if _STARTED.is_set():
            return None
        _STARTED.set()
    thread = threading.Thread(target=_check_quietly, daemon=True, name="seq-wifi-power")
    thread.start()
    return thread


def _check_quietly() -> None:
    try:
        check()
    except Exception:
        pass
