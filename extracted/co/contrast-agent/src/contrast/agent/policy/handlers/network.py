# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import socket
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from contrast.agent.policy.handlers import EventDict

_INET_FAMILIES = frozenset(
    family
    for family in (getattr(socket, "AF_INET", None), getattr(socket, "AF_INET6", None))
    if family is not None
)

_EVENT_KEYS_BY_SOCKET_TYPE = {
    socket.SOCK_STREAM: "stream",
    socket.SOCK_DGRAM: "dgram",
}


def _socket_from_args(args: Mapping[str, object]) -> object:
    """
    Returns the socket that a socket method was called on.

    Some socket methods have signatures that inspect can parse (e.g. connect), so the
    socket is bound to `self`. Others don't (e.g. listen), and the socket is the first
    of the catch-all positional `args`.
    """
    if (sock := args.get("self")) is not None:
        return sock
    positional = args.get("args", ())
    return positional[0] if isinstance(positional, tuple) and positional else None


def shield_permissions_builder(
    event_dict: EventDict,
) -> Callable[[Mapping[str, object]], tuple[str, ...]]:
    """
    Builds a function that maps the arguments of a socket method call to the CVE shield
    permission (capability) it uses, depending on the socket's type.

    The event specifies the permission for each socket type it applies to, under the
    `stream` (TCP) and/or `dgram` (UDP) keys. Only internet sockets are considered,
    since other families (e.g. AF_UNIX) don't access the network.
    """
    permissions_by_type = {
        socket_type: (event_dict[key],)
        for socket_type, key in _EVENT_KEYS_BY_SOCKET_TYPE.items()
        if event_dict.get(key)
    }
    if not permissions_by_type:
        raise ValueError("Event must specify a 'stream' and/or 'dgram' permission.")

    def shield_permissions(args: Mapping[str, object]) -> tuple[str, ...]:
        sock = _socket_from_args(args)
        if not isinstance(sock, socket.socket) or sock.family not in _INET_FAMILIES:
            return ()
        return permissions_by_type.get(sock.type, ())

    return shield_permissions
