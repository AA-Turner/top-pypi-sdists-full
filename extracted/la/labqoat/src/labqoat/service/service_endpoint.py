"""Where the control plane carries one named service, from the worker API a run already trusts."""

from collections.abc import Mapping
from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit

from labqoat.worker.session.session_connection import SessionConnection


@dataclass(frozen=True)
class ServiceEndpoint:
    """The tunnel a serving worker opens and the address its project's workers call, under one name."""

    api_url: str
    headers: Mapping[str, str]
    name: str

    def call_url(self) -> str:
        """Return the base address callers append the service's own paths to."""
        return self.api_url.rstrip("/") + f"/api/v1/worker/services/{self.name}/http"

    def connect(self) -> SessionConnection:
        """Open the tunnel with verified certificates, no proxy, no redirects and protocol keepalives."""
        parsed = urlsplit(self.api_url)
        scheme = "wss" if parsed.scheme == "https" else "ws"
        path = parsed.path.rstrip("/") + f"/api/v1/worker/services/{self.name}/tunnel"
        return SessionConnection(
            urlunsplit((scheme, parsed.netloc, path, "", "")),
            additional_headers=self.headers,
            proxy=None,
            compression=None,
            open_timeout=10,
            close_timeout=1,
            ping_interval=20,
            ping_timeout=20,
            max_size=1_048_576,
            max_queue=64,
        )
