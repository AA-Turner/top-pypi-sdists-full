# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
Wi-Fi power saving on the interface a robot sends its requests over: detected, and reported with how to disable it.
Read on Linux, read-only. On macOS, where it cannot be read, a robot whose requests go over Wi-Fi is told that it was
not checked (mac_wifi_iface, mac_words).

    from sequence_ai.network import wifi_power

    wifi_power.check()      # the interface whose power saving is on, after warning about it; None when there is none

In one sentence: the interface of the machine's default route (/proc/net/route, the one with the lowest metric) → it is
Wi-Fi when /sys/class/net/<it>/wireless exists → its power saving is read from `iw dev <it> get power_save`, else from
the Power Management field of `iwconfig <it>` → when it is on, a warning is issued with the command that disables it and
the setting that keeps it disabled. Nothing on the machine is changed, and when the state cannot be read nothing is
reported. check_once() runs the check once per process, on its own thread, so nothing waits for it.

WHY: with power saving on, a Wi-Fi adapter sleeps between its access point's beacons, and packets addressed to it, a
policy's response among them, wait at the access point until it wakes. A robot whose only link is Wi-Fi keeps the link
awake by disabling power saving.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import threading
from typing import Callable, Optional

from ._warn import warn

_ROUTE = "/proc/net/route"
_NET = "/sys/class/net"
# where the two tools are found when the robot's PATH omits the system directories (/usr/sbin is not on every user's)
_SBIN = ("/usr/sbin", "/sbin", "/usr/bin", "/bin")
# how each tool reports power saving: its command, then the pattern that matches on or off in its output
_READS = ((("iw", "dev", "{iface}", "get", "power_save"), re.compile(r"Power save:\s*(on|off)", re.I)),
          (("iwconfig", "{iface}"), re.compile(r"Power Management:\s*(on|off)", re.I)))
# the check starts once per process
_STARTED = threading.Event()
_LOCK = threading.Lock()


def words(iface: str) -> str:
    """The warning text for `iface` when its power saving is on."""
    return (f"Wi-Fi power saving is on for {iface}, so its adapter can delay this robot's packets while it sleeps; "
            f"`sudo iw dev {iface} set power_save off` disables it until the next reboot, and `wifi.powersave = 2` "
            "under [connection] in a file in /etc/NetworkManager/conf.d/ keeps it disabled")


def default_iface(route: str = _ROUTE) -> Optional[str]:
    """The interface of the machine's default route (the one with the lowest metric); None where there is none, or where
    the route table cannot be read (not Linux)."""
    try:
        with open(route) as f:
            rows = [line.split() for line in f.read().splitlines()[1:]]
    except OSError:
        return None
    best: Optional[tuple] = None
    for row in rows:
        # Iface Destination Gateway Flags RefCnt Use Metric Mask ...: a default route is up (flag 1), to 0.0.0.0/0
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
    """Whether Wi-Fi power saving is on for `iface`; None when it is not a Wi-Fi interface, or when neither tool is
    installed or reports the state."""
    if not os.path.isdir(os.path.join(net, iface, "wireless")):
        return None
    for command, pattern in _READS:
        path = tool(command[0])
        if path is None:
            continue
        try:
            out = run([path, *(part.format(iface=iface) for part in command[1:])], capture_output=True, text=True,
                      timeout=2.0, check=False).stdout
        except (OSError, subprocess.SubprocessError):
            continue
        found = pattern.search(out or "")
        if found:
            return found.group(1).lower() == "on"
    return None


def check(route: str = _ROUTE, **kw) -> Optional[str]:
    """Return the Wi-Fi interface of the machine's default route when its power saving is on, after issuing a warning
    about it; else None."""
    iface = default_iface(route)
    if iface is None or not power_save_on(iface, **kw):
        return None
    warn(words(iface))
    return iface


def mac_wifi_iface(run: Callable[..., subprocess.CompletedProcess] = subprocess.run) -> Optional[str]:
    """macOS: the Wi-Fi device (`networksetup -listallhardwareports`) when the default route goes over it (`route -n
    get default`); None when it does not, or when either cannot be read."""
    try:
        route = run(["/sbin/route", "-n", "get", "default"], capture_output=True, text=True, timeout=2.0,
                    check=False).stdout
        ports = run(["/usr/sbin/networksetup", "-listallhardwareports"], capture_output=True, text=True, timeout=2.0,
                    check=False).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    found = re.search(r"interface:\s*(\S+)", route or "")
    wifi = re.findall(r"Hardware Port:\s*(?:Wi-Fi|AirPort)\s*\n\s*Device:\s*(\S+)", ports or "")
    return found.group(1) if found and found.group(1) in wifi else None


def mac_words(iface: str) -> str:
    """What a robot on macOS is told when its requests go over Wi-Fi (`iface`)."""
    return (f"this robot's requests go over Wi-Fi ({iface}), and whether Wi-Fi saves power - which can hold its packets "
            "back - is read on Linux only, so it was not checked on this Mac; a wired connection takes the question "
            "away")


def check_once(*, linux: bool = sys.platform.startswith("linux"),
               darwin: bool = sys.platform == "darwin") -> Optional[threading.Thread]:
    """Run the check once per process, on its own thread (the module's docstring): on Linux, the warning when power
    saving is on; on macOS, the note that it was not checked, when the robot's requests go over Wi-Fi. Returns the
    thread, or None when nothing was started."""
    if not (linux or darwin) or _STARTED.is_set():
        return None
    with _LOCK:
        if _STARTED.is_set():
            return None
        _STARTED.set()
    thread = threading.Thread(target=_check_quietly if linux else _say_unchecked_quietly, daemon=True,
                              name="sequence-ai-wifi-power")
    thread.start()
    return thread


def _check_quietly() -> None:
    try:
        check()
    except Exception:  # noqa: BLE001 (a robot must not fail because of a hint)
        pass


def _say_unchecked_quietly() -> None:
    try:
        iface = mac_wifi_iface()
        if iface is not None:
            warn(mac_words(iface))
    except Exception:  # noqa: BLE001 (a robot must not fail because of a hint)
        pass
