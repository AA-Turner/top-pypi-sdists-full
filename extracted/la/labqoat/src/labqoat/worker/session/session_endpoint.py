"""Verified WebSocket configuration captured from an already validated worker API."""

from collections.abc import Mapping
from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit

from labqoat.worker.session.session_connection import SessionConnection


@dataclass(frozen=True)
class SessionEndpoint:
    """Disable ambient proxies, compression and redirects for scoped control traffic."""

    url: str
    headers: Mapping[str, str]

    def connect(self) -> SessionConnection:
        """Use standard certificate verification, bounded buffers and protocol keepalives."""
        parsed = urlsplit(self.url)
        scheme = "wss" if parsed.scheme == "https" else "ws"
        path = parsed.path.rstrip("/") + "/api/v1/worker/session"
        uri = urlunsplit((scheme, parsed.netloc, path, "", ""))
        return SessionConnection(
            uri,
            additional_headers=self.headers,
            proxy=None,
            compression=None,
            open_timeout=10,
            close_timeout=5,
            ping_interval=20,
            ping_timeout=20,
            max_size=16_777_216,
            max_queue=16,
        )
