"""Generated HTTP transport with HTTP Basic authentication."""

from __future__ import annotations

import base64
from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from threading import Lock
from _thread import LockType
from urllib.parse import urlsplit

from labqoat.net.client_identity import ClientIdentity
from labqoat.net.http_client import HttpClient
from labqoat.net.request import Handler
from labqoat.net.response import Response


@dataclass
class Transport:
    """Shared pooled HTTP transport. Owned by the schema emitter."""

    base_url: str
    username: str
    password: str
    timeout_seconds: float = 30.0
    handler: Handler | None = None
    _client: HttpClient | None = field(default=None, repr=False)
    _client_lock: LockType = field(default_factory=Lock, init=False, repr=False, compare=False)
    environment: str = "default"
    project: str | None = None
    agent: str | None = None
    group: str | None = None

    def __post_init__(self) -> None:
        """Validate the endpoint and credentials."""
        Transport.ensure_loopback(self.base_url)
        Transport.ensure_credentials(self.username, self.password)

    def request(
        self,
        method: str,
        path: str,
        content: bytes | Iterable[bytes] | None = None,
        content_type: str | None = None,
        content_length: int | None = None,
        idempotency_key: str | None = None,
        content_encoding: str | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send one authenticated request without redirects and read its whole answer."""
        fields = Transport.basic_headers(self.username, self.password)
        if content_type is not None:
            fields["content-type"] = content_type
        if content_length is not None:
            fields["content-length"] = str(content_length)
        if idempotency_key is not None:
            fields["idempotency-key"] = idempotency_key
        if content_encoding is not None:
            fields["content-encoding"] = content_encoding
        fields.update(headers or {})
        return self.open_client().request(method, path, content=content, headers=fields)

    @contextmanager
    def stream(
        self,
        method: str,
        path: str,
        content: bytes | Iterable[bytes] | None = None,
        content_type: str | None = None,
        event_stream: bool = False,
    ) -> Iterator[Response]:
        """Open one authenticated streaming request without redirects."""
        fields = Transport.basic_headers(self.username, self.password)
        if content_type is not None:
            fields["content-type"] = content_type
        timeout = None
        if event_stream:
            fields["accept"] = "text/event-stream"
            timeout = max(self.timeout_seconds, 45.0)
        with self.open_client().stream(method, path, content=content, headers=fields, timeout=timeout) as response:
            yield response

    def open_client(self) -> HttpClient:
        """Open or reuse one pooled HTTP client even when concurrent bulk calls start together."""
        with self._client_lock:
            if self._client is None:
                self._client = HttpClient(
                    self.base_url,
                    headers=self.default_headers(),
                    timeout=self.timeout_seconds,
                    handler=self.handler,
                    proxy=True,
                )
            return self._client

    def default_headers(self) -> dict[str, str]:
        """Name this SDK release, select environment, project and optional memory attribution, accept gzip."""
        headers = {
            **ClientIdentity.HEADERS,
            "accept-encoding": "gzip",
            "x-labqoat-environment": self.environment,
        }
        if self.project is not None:
            headers["x-labqoat-project"] = self.project
        if self.agent is not None:
            headers["x-labqoat-agent"] = self.agent
        if self.group is not None:
            headers["x-labqoat-group"] = self.group
        return headers

    def close(self) -> None:
        """Close the underlying HTTP client."""
        with self._client_lock:
            if self._client is not None:
                self._client.close()
                self._client = None

    def __enter__(self) -> Transport:
        """Open the client for a managed block."""
        self.open_client()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        """Close the client after a managed block."""
        self.close()

    @staticmethod
    def basic_headers(username: str, password: str) -> dict[str, str]:
        """Build the Authorization header value."""
        raw = f"{username}:{password}".encode()
        encoded = base64.b64encode(raw).decode("ascii")
        return {"authorization": f"Basic {encoded}"}

    @staticmethod
    def ensure_loopback(base_url: str) -> None:
        """Reject non-loopback plain HTTP destinations."""
        parts = urlsplit(base_url)
        if parts.scheme == "https":
            return
        if parts.scheme == "http" and parts.hostname in ("127.0.0.1", "localhost", "::1"):
            return
        msg = f"refusing non-loopback HTTP destination: {base_url}"
        raise ValueError(msg)

    @staticmethod
    def ensure_credentials(username: str, password: str) -> None:
        """Reject empty credentials before any request."""
        if not username or not password or ":" in username:
            msg = "username must be nonempty without a colon; password must be nonempty"
            raise ValueError(msg)
