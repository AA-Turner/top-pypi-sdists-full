"""The socket transport: this machine's service socket (`service_api.Connection`), hello first, fds over SCM_RIGHTS."""

from __future__ import annotations

from collections.abc import Sequence

from ..service_api import TIMEOUT_S, Connection
from .transport import FENCED_ERRNOS, Channel, FencedError, Transport


class SocketChannel(Channel):
    """One socket connection after its hello."""

    def __init__(self, connection: Connection, hello: dict) -> None:
        self.connection = connection
        self.hello = hello

    def call(self, method: str, parameters: dict | None = None, fds: Sequence[int] = ()) -> dict:
        return self.connection.call(method, parameters, fds)

    def close(self) -> None:
        self.connection.close()


class SocketTransport(Transport):
    """Connect to the socket; `FencedError` when a sandbox refuses it (EPERM/EACCES at `socket()` or `connect()`)."""

    def connect(self, timeout: float = TIMEOUT_S, *, client: str, client_version: str) -> SocketChannel:
        try:
            connection = Connection.open(timeout)
        except PermissionError as exc:
            # A private-folder check raises PermissionError too, with no errno: never read as fenced.
            if exc.errno in FENCED_ERRNOS:
                raise FencedError(exc.errno, f"the service socket is closed to this process: {exc.strerror}") from exc
            raise
        try:
            return SocketChannel(connection, connection.hello(client, client_version))
        except BaseException:
            connection.close()
            raise
