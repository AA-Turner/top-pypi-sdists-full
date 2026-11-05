"""The one interface every way of reaching the Probe service implements: `Transport.connect(timeout) -> Channel`, `Channel.call`.

Two transports (service-only plan Q1 = A): the socket, and the drop folder for a fenced caller whose
sandbox refuses the socket. `transports.connect` picks one once (`transports.py`).
"""

from __future__ import annotations

import errno
from abc import ABC, abstractmethod
from collections.abc import Sequence

#: `socket()` or `connect()` failing with one of these means a sandbox refused the socket.
FENCED_ERRNOS = frozenset({errno.EPERM, errno.EACCES})
#: What a fenced caller is told when its call needs its terminal (fds): the drop folder carries none.
INTERACTIVE_NEEDS_TERMINAL = "interactive commands need an unfenced terminal"


class FencedError(PermissionError):
    """The socket is closed to this process (a sandbox refused it): the drop folder reaches the service."""


class FdsUnsupportedError(Exception):
    """A call passed file descriptors over a transport that carries none (the drop folder)."""


class Channel(ABC):
    """One conversation with the service: `call` sends a request and returns its result."""

    #: The service's `service.hello` answer, once one came ({} before).
    hello: dict

    @abstractmethod
    def call(self, method: str, parameters: dict | None = None, fds: Sequence[int] = ()) -> dict:
        """The method's result; `ServiceError` for an error answer, OSError when none came."""

    @abstractmethod
    def close(self) -> None: ...

    def __enter__(self) -> Channel:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


class Transport(ABC):
    """A way to reach this machine's service."""

    @abstractmethod
    def connect(self, timeout: float, *, client: str, client_version: str) -> Channel:
        """A channel, or OSError (`FencedError` when a sandbox refused it)."""
