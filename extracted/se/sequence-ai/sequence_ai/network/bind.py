# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A connection that leaves by one network interface: each socket it opens is bound to the interface before it connects,
so its packets go out that way whatever this machine's default route - how a robot's stream goes over each of its
uplinks (a Starlink terminal's and a cellular modem's, say), and how each line is let into a GPU's allow list.

    import sequence_ai
    policy = sequence_ai.connect("http://your-gpu:8000", lines=["eth0", "wwan0"])   # a stream by each

    from sequence_ai.network import bind
    transport = bind.transport(httpx, "wwan0")       # an httpx transport whose connections leave by the modem alone

In one sentence: an interface's name → the socket option that binds a socket to it, for the socket's address family
(Linux: SO_BINDTODEVICE, by name; macOS: IP_BOUND_IF or IPV6_BOUND_IF, by index) → set on each socket the connection
opens, before connect(), its other options after it, as httpcore sets them → an httpx transport whose connection pool
opens its sockets that way.

WHY before connect(): a TCP connection's route is chosen when it connects, and httpcore sets its socket_options after
socket.create_connection, when the first packet has left by the default route (httpcore 1.0.9
SyncBackend.connect_tcp). So the binding is done here, in a network backend of the connection's own.
WHY no root: Linux lets any user bind a socket not yet bound to an interface since 5.7 (its commit c427bfec18f2, "net:
core: enable SO_BINDTODEVICE for non-root users"); macOS asks nothing for IP_BOUND_IF.

Needs httpx and httpcore, which sequence-ai installs; Linux 5.7 or later, or macOS.
"""
from __future__ import annotations

import socket
import sys
from typing import Any, Iterable, Optional

# macOS's: Python names neither (<netinet/in.h>: IP_BOUND_IF 25, <netinet6/in6.h>: IPV6_BOUND_IF 125)
IP_BOUND_IF = getattr(socket, "IP_BOUND_IF", 25)
IPV6_BOUND_IF = getattr(socket, "IPV6_BOUND_IF", 125)


def options(interface: str, family: int, platform: Optional[str] = None) -> list:
    """The socket options that bind a socket of address `family` to `interface`, on `platform` (this one's by
    default). OSError where the system has no way to, or no interface by that name (macOS reads its index)."""
    platform = platform or sys.platform
    if platform.startswith("linux"):
        return [(socket.SOL_SOCKET, getattr(socket, "SO_BINDTODEVICE", 25), interface.encode())]
    if platform == "darwin":
        index = socket.if_nametoindex(interface)
        if family == socket.AF_INET6:
            return [(socket.IPPROTO_IPV6, IPV6_BOUND_IF, index)]
        return [(socket.IPPROTO_IP, IP_BOUND_IF, index)]
    raise OSError(f"a connection is bound to an interface ({interface}) on Linux or macOS, and this is {platform}")


def check(interface: str) -> None:
    """OSError, naming this machine's interfaces, where it has no interface by that name."""
    try:
        socket.if_nametoindex(interface)
    except OSError:
        names = ", ".join(name for _, name in socket.if_nameindex())
        raise OSError(f"no network interface {interface!r} on this machine: it has {names}") from None


def _backend(interface: str) -> Any:
    import httpcore
    from httpcore._backends.sync import SyncStream

    class Bound(httpcore.SyncBackend):
        """httpcore's backend, but each TCP socket is bound to `interface` before it connects."""

        def __init__(self) -> None:
            self.interface = interface

        def connect_tcp(self, host: str, port: int, timeout: Optional[float] = None,
                        local_address: Optional[str] = None,
                        socket_options: Optional[Iterable[tuple]] = None) -> Any:
            failed: list = []
            for family, kind, proto, _, address in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM):
                sock = socket.socket(family, kind, proto)
                try:
                    for option in options(interface, family):
                        sock.setsockopt(*option)
                    if local_address is not None:
                        sock.bind((local_address, 0))
                    sock.settimeout(timeout)
                    sock.connect(address)
                    for option in socket_options or ():
                        sock.setsockopt(*option)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    return SyncStream(sock)
                except OSError as error:
                    sock.close()
                    failed.append(error)
            last = failed[-1] if failed else OSError(f"no address for {host}")
            kind = httpcore.ConnectTimeout if isinstance(last, socket.timeout) else httpcore.ConnectError
            raise kind(f"{last} (connecting to {host}:{port} by {interface})") from last

    return Bound()


def transport(httpx: Any, interface: str, **options_: Any) -> Any:
    """An httpx transport, made with `options_` (httpx.HTTPTransport's), whose connections leave by `interface`.
    OSError where this machine has no such interface."""
    check(interface)
    made = httpx.HTTPTransport(**options_)
    # httpx 0.28's transport keeps its httpcore pool as _pool, and the pool opens each connection with its
    # _network_backend (tests/network/test_bind.py fails if either name changes)
    made._pool._network_backend = _backend(interface)
    return made
