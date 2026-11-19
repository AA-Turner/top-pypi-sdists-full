# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A connection's send window, kept through the pauses between a robot's uploads.

    from sequence_ai.network import window

    transport = httpx.HTTPTransport(socket_options=window.socket_options())    # BBR and TCP keepalive, where available
    window.keep(sock)                                                          # or BBR on your own socket

    warm = window.Warm(ping=connection.ping)      # where there is no BBR: a ping while the connection is idle
    warm.used()                                   # each time you send on it
    warm.close()

    window.check()                                # warns once: what this machine does after a pause, how to change it

── a robot's uploads through the pauses between them: BBR ──
On Linux a connection that has sent nothing for longer than its retransmission timeout (at least its RTT plus 200 ms)
restarts its congestion window before it sends again, halved for each such timeout it was idle, down to 10 packets
(net.ipv4.tcp_slow_start_after_idle, on by default; tcp_output.c tcp_cwnd_restart). So a robot sending a request every
0.53 s with 24 KB of frames (19 packets) uploaded each request in two round trips instead of one. BBR on the
connection's own socket, where the robot allows it, keeps the window through the pauses: BBR has its own cong_control,
so the idle restart and the application-limited decay are both skipped (include/net/tcp.h
tcp_slow_start_after_idle_check, tcp_output.c tcp_cwnd_validate). Measured on kernels 7.0 and 6.8, a request every 0.53
s, an RTT of about 21 ms: 40 of 40 requests took one more round trip without it (21.5 ms); with BBR 0.5 to 3.0 ms, and
40 of 40 in one round trip.

── a connection kept warm while the robot runs: Warm ──
After every `every_s` in which the robot sent nothing, a ping is sent on its connection, for `for_s` after its last
send: a large observation after a pause is then uploaded like one sent right after another. What it keeps: the machine's
Wi-Fi radio awake (asleep, the responses to an upload's first round trips wait at the access point for its next beacon);
a connection never idle past a retransmission timeout while its far end answers the pings (past one, Linux restarts its
window, RFC 5681 4.1); and a dead connection detected by the ping's deadline before the robot's next send uses it. What
it cannot keep: Linux shrinks a window the pings do not fill (RFC 2861, tcp_output.c tcp_cwnd_validate); BBR or
tcp_slow_start_after_idle=0 keeps that one. Each ping waits for its pong, so a server that answers none while it works
leaves the robot silent until it does: with openpi's own server, during inference, Linux halved the window once before
most uploads (openpi.py has the measurement). macOS keeps its window for three minutes of idle time regardless.
Measured: at an RTT of 226 ms, 162 KB uploads 3 s apart on one pinged connection took 303.6 ms to arrive without the
pings and under 1 ms with them; from 85 ms away, 2.36 MB after a 2 s pause took a median 504 ms without, 421 ms with a
ping every 100 ms, and 396 ms sent immediately: three of each, too few to be sure of the last.

── a connection that died between uses: TCP keepalive ──
The machine probes the far end once the connection has been idle, then at an interval, and drops it after a few probes
go unanswered: a home or office router that silently dropped its record of the connection is detected before the next
send uses it, and the probes keep the router's mapping fresh.

Standard library only. Each socket option is tried on a separate socket first: an HTTP client sets its socket options as
it connects, and one it cannot set fails the connect.
"""
from __future__ import annotations

import socket
import threading
import time
from typing import Callable, Optional

from ._warn import warn

# the socket option that names a connection's congestion control (Linux; absent elsewhere)
_TCP_CONGESTION = getattr(socket, "TCP_CONGESTION", None)
# The setting by which Linux restarts a connection's window after a pause (1, the default) or keeps it (0).
_SLOW_START_AFTER_IDLE = "/proc/sys/net/ipv4/tcp_slow_start_after_idle"
# An upload this large after a pause takes several round trips on a machine that restarts a connection's window
# after a pause: above this size, such a machine gets one warning with how to keep its window (check).
BIG_UPLOAD = 256 * 1024
# warned once per process: a machine that restarts a connection's window after a pause (check)
_WARNED = threading.Event()
_LOCK = threading.Lock()


def bbr_options() -> Optional[list]:
    """The socket option that makes a connection use BBR, when this machine allows a socket to set it; else None. Tried
    on a separate socket first: an HTTP client sets its socket options as it connects, and one it cannot set fails the
    connect. An unprivileged process may set BBR whenever its kernel has the tcp_bbr module loaded (BBR is not
    restricted to net.ipv4.tcp_allowed_congestion_control); Ubuntu does not load it by default, and the attempt fails
    with ENOENT. A machine whose `socket` module has no TCP_CONGESTION (not Linux) has nothing to try."""
    if _TCP_CONGESTION is None:
        return None
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.setsockopt(socket.IPPROTO_TCP, _TCP_CONGESTION, b"bbr")
    except OSError:
        return None
    return [(socket.IPPROTO_TCP, _TCP_CONGESTION, b"bbr")]


def keepalive_options(idle_s: int = 20, every_s: int = 5, probes: int = 3) -> list:
    """The socket options that enable TCP keepalive: SO_KEEPALIVE, and its idle time, interval and count where this
    machine defines them (TCP_KEEPIDLE on Linux and Windows, TCP_KEEPALIVE on macOS). Each is tried on a separate socket
    first, as bbr_options does: one this machine rejects is left out and the rest are kept; none at all where
    SO_KEEPALIVE itself is rejected."""
    idle = getattr(socket, "TCP_KEEPIDLE", None) or getattr(socket, "TCP_KEEPALIVE", None)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            kept = [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)]
            for name, value in ((idle, idle_s), (getattr(socket, "TCP_KEEPINTVL", None), every_s),
                                (getattr(socket, "TCP_KEEPCNT", None), probes)):
                if name is None:
                    continue
                try:
                    probe.setsockopt(socket.IPPROTO_TCP, name, value)
                except OSError:
                    continue
                kept.append((socket.IPPROTO_TCP, name, value))
    except OSError:
        return []
    return kept


def socket_options() -> list:
    """Every option this machine accepts (BBR where available, and TCP keepalive) as (level, name, value) tuples, which
    is what an HTTP client's transport takes as its `socket_options` (httpx.HTTPTransport, httpcore's pools)."""
    return [*(bbr_options() or []), *keepalive_options()]


def keep(sock: socket.socket) -> bool:
    """Set BBR on `sock`, the caller's own socket: whether the socket accepted it."""
    if _TCP_CONGESTION is None:
        return False
    try:
        sock.setsockopt(socket.IPPROTO_TCP, _TCP_CONGESTION, b"bbr")
    except OSError:
        return False
    return True


def congestion_of(sock: Optional[socket.socket]) -> Optional[str]:
    """The congestion control `sock`'s connection uses ("bbr", "cubic"), or None when that cannot be read (not Linux, no
    socket)."""
    try:
        if sock is None or _TCP_CONGESTION is None:
            return None
        return sock.getsockopt(socket.IPPROTO_TCP, _TCP_CONGESTION, 16).split(b"\0", 1)[0].decode() or None
    except (OSError, AttributeError, ValueError):
        return None


def restarts_after_idle() -> bool:
    """Whether this machine restarts a connection's send window after a pause: Linux with tcp_slow_start_after_idle 1
    (its default). False where it cannot be read (not Linux, or a container that hides it)."""
    try:
        with open(_SLOW_START_AFTER_IDLE) as f:
            return f.read().strip() == "1"
    except OSError:
        return False


def check(size: int = BIG_UPLOAD + 1) -> bool:
    """For an upload of `size` bytes on a machine that restarts a connection's send window after each pause and whose
    sockets cannot use BBR: warns once per process, with how to keep the window, since such an upload after a pause
    takes several round trips. Returns whether the warning was issued now. Nothing on the machine is changed."""
    if size <= BIG_UPLOAD or _WARNED.is_set() or bbr_options() is not None or not restarts_after_idle():
        return False
    with _LOCK:
        if _WARNED.is_set():
            return False
        _WARNED.set()
    warn(f"this machine restarts a connection's send window after each pause (net.ipv4.tcp_slow_start_after_idle "
         f"is 1), so an upload of {size / 1e6:.1f} MB sent after one takes several round trips. "
         "`sudo sysctl -w net.ipv4.tcp_slow_start_after_idle=0` keeps the window through pauses (a line in "
         "/etc/sysctl.d/ keeps it after a reboot), as does loading BBR (`sudo modprobe tcp_bbr`), which "
         "window.socket_options() then sets on your connections")
    return True


class Warm:
    """Keeps a connection warm while its robot runs (the module's docstring): after every `every_s` in which nothing was
    sent on it, within `for_s` of the last send, it calls `ping()` (the connection's own: a WebSocket ping or a small
    request), until close(). used() records that something was sent. A ping that raises stops the pings: its connection
    is dead, and the next send will find that.

    The thread starts at the first used(), so a connection that was never sent on is never pinged."""

    def __init__(self, ping: Callable[[], object], *, every_s: float = 0.1, for_s: float = 60.0,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._ping, self.every_s, self.for_s, self._clock = ping, every_s, for_s, clock
        self._used_at: Optional[float] = None
        self._sooner: Optional[float] = None           # when the next iteration comes, if sooner than its turn
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self.pings = 0

    def used(self) -> None:
        """Record that something was just sent on the connection: no ping is due for `every_s`, and it is kept warm for
        `for_s` more."""
        self._used_at = self._clock()
        if self._thread is None and not self._stop.is_set():
            with self._lock:
                if self._thread is None and not self._stop.is_set():
                    self._thread = threading.Thread(target=self._run, daemon=True, name="sequence-ai-keep-warm")
                    self._thread.start()

    def due(self) -> bool:
        """Whether a ping is due now: the connection was sent on, has been idle for `every_s`, and for no more than
        `for_s`."""
        if self._used_at is None:
            return False
        idle_s = self._clock() - self._used_at
        return self.every_s <= idle_s <= self.for_s

    def tick(self) -> bool:
        """One iteration: send a ping when one is due. Returns whether the pings continue. A `ping()` that returns False
        sent nothing (the connection was busy, or its ping yielded to a request: link.py) and is not counted."""
        if not self.due():
            return True
        try:
            sent = self._ping()
        except Exception:  # noqa: BLE001 (whatever the caller's connection raises: it is dead)
            return False
        if sent is not False:
            self.pings += 1
        return True

    def check_in(self, seconds: float) -> None:
        """Have the next iteration come `seconds` from now, if that is sooner than its turn: a ping left out for now
        (link.py's that yields to a request) is asked about again by the time it may no longer wait."""
        self._sooner = self._clock() + max(0.0, seconds)

    def _wait(self) -> float:
        """How long until the next iteration: `every_s`, or less where check_in() asked for one sooner."""
        sooner, self._sooner = self._sooner, None
        if sooner is None:
            return self.every_s
        return max(0.0, min(self.every_s, sooner - self._clock()))

    def _run(self) -> None:
        while not self._stop.wait(self._wait()):
            if not self.tick():
                return

    def close(self, wait_s: float = 2.0) -> None:
        """Stop the pings. A ping in flight is waited for, up to `wait_s`: the caller usually closes the connection
        next, and closing a connection while another thread is still making a request on it fails that request, or gives
        its descriptor to whatever opens next."""
        self._stop.set()
        thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(wait_s)
