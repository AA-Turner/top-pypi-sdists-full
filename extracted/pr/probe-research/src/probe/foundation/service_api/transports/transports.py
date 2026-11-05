"""The one registry that picks how this process reaches the Probe service: the socket, else (fenced) the drop folder."""

from __future__ import annotations

from ..service_api import TIMEOUT_S
from ..vocabularies import Client
from .drop import DROP_TIMEOUT_S, DropTransport
from .socket import SocketTransport
from .transport import Channel, FencedError, Transport

#: The transport this process settled on: None until a connect succeeded or was fenced.
_picked: Transport | None = None


def get_transport() -> Transport | None:
    """The transport this process picked, or None before its first decisive connect."""
    return _picked


def connect(timeout: float = TIMEOUT_S, *, client: str = Client.CLI, client_version: str = "unknown") -> Channel:
    """A channel to the service: the socket first; the drop folder once a sandbox refused the
    socket (`FencedError`), for the rest of this process. OSError when no service answers."""
    global _picked
    if _picked is not None:
        return _picked.connect(timeout, client=client, client_version=client_version)
    try:
        channel = SocketTransport().connect(timeout, client=client, client_version=client_version)
    except FencedError:
        _picked = DropTransport()
        return _picked.connect(max(timeout, DROP_TIMEOUT_S), client=client, client_version=client_version)
    _picked = SocketTransport()
    return channel
