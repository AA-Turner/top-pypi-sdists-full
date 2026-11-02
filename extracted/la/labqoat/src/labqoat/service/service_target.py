"""The local HTTP server a worker serves to its project."""

import socket
from dataclasses import dataclass
from time import monotonic
from time import sleep as pause
from typing import ClassVar

from labqoat.net.async_http_client import AsyncHttpClient


@dataclass(frozen=True)
class ServiceTarget:
    """A server listening on a loopback port or on a unix socket inside the worker."""

    PROBE_SECONDS: ClassVar[float] = 0.2

    port: int | None = None
    unix_socket: str | None = None

    def __post_init__(self) -> None:
        """Require exactly one place to find the server."""
        if (self.port is None) == (self.unix_socket is None):
            raise ValueError("Serve either a port or a unix socket")

    def client(self) -> AsyncHttpClient:
        """Open a client that reaches only this server, follows nothing and waits as long as the server takes.

        It sends what a caller sent and nothing of its own: a default such as accepting compression would have
        the server answer a caller in an encoding the caller never asked for.
        """
        origin = "http://service" if self.port is None else f"http://127.0.0.1:{self.port}"
        return AsyncHttpClient(origin, timeout=None, connect_timeout=10.0, unix_socket=self.unix_socket)

    def wait(self, timeout: float, what: str) -> None:
        """Probe until the server accepts a connection, and fail once ``timeout`` seconds pass without one."""
        deadline = monotonic() + timeout
        while not self.listening():
            if monotonic() >= deadline:
                raise TimeoutError(f"Nothing listened for {what} within {timeout:g} s")
            pause(self.PROBE_SECONDS)

    def listening(self) -> bool:
        """Report whether the server accepts a connection right now."""
        family = socket.AF_INET if self.unix_socket is None else socket.AF_UNIX
        address = ("127.0.0.1", self.port) if self.unix_socket is None else self.unix_socket
        with socket.socket(family, socket.SOCK_STREAM) as probe:
            probe.settimeout(1.0)
            return probe.connect_ex(address) == 0
