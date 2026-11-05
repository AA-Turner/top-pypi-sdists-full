"""How a client reaches this machine's Probe service: one `connect` that picks a transport once (service-only plan Q1 = A).

    connect(timeout)  the socket; when a sandbox refuses it (EPERM/EACCES), the drop folder,
                      and every later connect of this process goes there too
    Channel.call(method, parameters, fds=())  one request, its result

The service watches the drop folder and answers each request through the same dispatch as the
socket (`probe.service.server.connections.drop_door`); the OS starts it for either (D19).
"""

from __future__ import annotations

from .drop import DROP_TIMEOUT_S, DropChannel, DropTransport
from .socket import SocketChannel, SocketTransport
from .transports import connect, get_transport
from .transport import (
    FENCED_ERRNOS,
    INTERACTIVE_NEEDS_TERMINAL,
    Channel,
    FdsUnsupportedError,
    FencedError,
    Transport,
)

__all__ = [
    "DROP_TIMEOUT_S", "FENCED_ERRNOS", "INTERACTIVE_NEEDS_TERMINAL", "Channel", "DropChannel", "DropTransport",
    "FdsUnsupportedError", "FencedError", "SocketChannel", "SocketTransport", "Transport", "connect", "get_transport",
]
