"""Where a sandbox host answers: beside its own worker, or through a service another run offers."""

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import ClassVar

from labqoat.net.async_http_client import AsyncHttpClient
from labqoat.net.client_identity import ClientIdentity
from labqoat.net.http_client import HttpClient
from labqoat.net.transport_trust import TransportTrust
from labqoat.sandbox.sandbox_unavailable_error import SandboxUnavailableError


@dataclass(frozen=True)
class SandboxRoute:
    """A sandbox host's private unix socket, or the address of a service that carries requests to one.

    A host's own worker reaches it over the socket the platform mounts. Anything else, another run or a
    machine outside the platform, reaches a host whose worker serves that socket under a name, at the
    service's address and with the headers that admit the caller.
    """

    SOCKET_VARIABLE: ClassVar[str] = "LABQOAT_SANDBOX_SOCKET"
    URL_VARIABLE: ClassVar[str] = "LABQOAT_SANDBOX_URL"
    AUTHORIZATION_VARIABLE: ClassVar[str] = "LABQOAT_SANDBOX_AUTHORIZATION"
    PROJECT_VARIABLE: ClassVar[str] = "LABQOAT_SANDBOX_PROJECT"

    origin: str
    socket_path: str | None = None
    headers: Mapping[str, str] = field(default_factory=dict, repr=False)

    @classmethod
    def local(cls, socket_path: str) -> "SandboxRoute":
        """Reach the host beside this worker; the socket never carries TLS and needs no credentials."""
        return cls("http://sandbox", socket_path)

    @classmethod
    def served(cls, url: str, headers: Mapping[str, str]) -> "SandboxRoute":
        """Reach a host through the service at ``url``, presenting ``headers`` to be let through."""
        return cls(url.rstrip("/"), None, dict(headers))

    @classmethod
    def from_environment(cls) -> "SandboxRoute":
        """Prefer the worker's own socket, then a served host named by address and credentials."""
        if socket_path := os.environ.get(cls.SOCKET_VARIABLE):
            return cls.local(socket_path)
        if url := os.environ.get(cls.URL_VARIABLE):
            named = {"Authorization": cls.AUTHORIZATION_VARIABLE, "X-Labqoat-Project": cls.PROJECT_VARIABLE}
            return cls.served(url, {name: os.environ[key] for name, key in named.items() if os.environ.get(key)})
        raise SandboxUnavailableError(
            f"{cls.SOCKET_VARIABLE} is not set: sandboxes are available to a sandbox host worker, "
            f"or through a served host named by {cls.URL_VARIABLE}"
        )

    def describe(self) -> str:
        """Name the host for messages without any credential."""
        return self.socket_path or self.origin

    def client(self, timeout: float) -> HttpClient:
        """A blocking client for the host: its socket, or verified TLS to the service."""
        named = ClientIdentity.HEADERS
        if self.socket_path is not None:
            return HttpClient(self.origin, headers=named, timeout=timeout, unix_socket=self.socket_path)
        return HttpClient(self.origin, headers=named, timeout=timeout, context=TransportTrust.context())

    def client_async(self, timeout: float) -> AsyncHttpClient:
        """An asynchronous client for the host: its socket, or verified TLS to the service."""
        named = ClientIdentity.HEADERS
        if self.socket_path is not None:
            return AsyncHttpClient(self.origin, headers=named, timeout=timeout, unix_socket=self.socket_path)
        return AsyncHttpClient(self.origin, headers=named, timeout=timeout, context=TransportTrust.context())
