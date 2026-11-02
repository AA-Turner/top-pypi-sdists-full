"""Assignment-authenticated HTTP boundary for workflow workers."""

from __future__ import annotations

import base64
import http.client
import os
from dataclasses import replace
from typing import TYPE_CHECKING

from labqoat.json_document import JsonValue
from labqoat.stage_timer import StageTimer
from labqoat.worker.scoped_api import ScopedApi
from labqoat.net.transport_trust import TransportTrust
from labqoat.worker.session.local_session_client import LocalSessionClient
from labqoat.worker.session.session_telemetry import SessionTelemetry
from labqoat.worker.worker_lease import WorkerLease
from labqoat.worker.worker_telemetry_buffer import WorkerTelemetryBuffer
from labqoat.worker.worker_telemetry_stream import WorkerTelemetryStream

if TYPE_CHECKING:
    from labqoat.service.service_endpoint import ServiceEndpoint
    from labqoat.worker.session.session_endpoint import SessionEndpoint


class WorkerApi(ScopedApi):
    """Authorize worker-only routes without receiving management credentials."""

    capabilities: frozenset[str] = frozenset()
    attempt_id: str | None = None

    def __init__(
        self,
        base_url: str,
        credential_id: str,
        secret: str,
        timeout_seconds: float = 180.0,
        timing: StageTimer | None = None,
        session_socket: str | None = None,
    ) -> None:
        """Bind explicit credentials without logging them or following redirects."""
        headers = {
            "X-Labqoat-Worker-Authorization": "Basic "
            + base64.b64encode(f"{credential_id}:{secret}".encode()).decode(),
        }
        local = LocalSessionClient(session_socket, credential_id, secret, timeout_seconds) if session_socket else None
        super().__init__(base_url, headers, "/api/v1/worker/", timeout_seconds, timing, local)
        session = None if local is None else SessionTelemetry(local, self._session_telemetry)
        self._telemetry = WorkerTelemetryStream(
            self._telemetry_connection,
            self._url.path.rstrip("/") + "/api/v1/worker/assignments/telemetry",
            headers,
            session,
        )
        self._telemetry_buffer = WorkerTelemetryBuffer(self._telemetry)

    def telemetry(self, kind: str, entries: list[JsonValue]) -> None:
        """Durably acknowledge buffered evidence before this immediate telemetry push."""
        self._telemetry_buffer.send(kind, entries)

    def buffer_telemetry(self, kind: str, entries: list[JsonValue]) -> None:
        """Batch evidence for up to one second; flush_telemetry is the durable acknowledgement barrier."""
        self._telemetry_buffer.add(kind, entries)

    def flush_telemetry(self) -> None:
        """Wait for durable acknowledgement of all streamed telemetry."""
        self._telemetry_buffer.flush()

    def close(self) -> None:
        """Flush telemetry before the worker emits its authoritative result."""
        try:
            self._telemetry_buffer.close()
        finally:
            super().close()

    def lease(self) -> WorkerLease:
        """Renew with separate bounded connections, independent of uploads and long SSE waits."""
        local = None if self._local is None else replace(self._local, timeout=10)
        api = ScopedApi(self._url.geturl(), self._headers, self._prefix, timeout_seconds=10.0, local=local)
        return WorkerLease(api)

    def session_endpoint(self) -> SessionEndpoint:
        """Delegate the validated origin to one physical supervisor's persistent transport."""
        from labqoat.worker.session.session_endpoint import SessionEndpoint

        return SessionEndpoint(self._url.geturl(), self._headers)

    def service_endpoint(self, name: str) -> ServiceEndpoint:
        """Name one service of the run's project on the validated origin, under the run's own credentials."""
        from labqoat.service.service_endpoint import ServiceEndpoint

        return ServiceEndpoint(self._url.geturl(), self._headers, name)

    def fit_api(self) -> ScopedApi:
        """Bound fit reporting I/O independently of uploads; physical expiry never waits for this transport."""
        return ScopedApi(self._url.geturl(), self._headers, self._prefix, timeout_seconds=5.0)

    def _session_telemetry(self) -> bool:
        """Older services keep every telemetry window on the streaming upload."""
        return "delegated_telemetry" in self.capabilities

    def _telemetry_connection(self) -> http.client.HTTPConnection:
        """Keep telemetry recovery bounded independently of long-running asset request timeouts."""
        url = self._url
        return TransportTrust.connection(url.scheme, str(url.hostname), url.port, timeout=min(self._timeout, 10.0))

    @classmethod
    def from_environment(cls, timing: StageTimer | None = None) -> WorkerApi:
        """Read only the assignment credentials explicitly injected by the platform."""
        return cls(
            os.environ["LABQOAT_API_URL"],
            os.environ["LABQOAT_CREDENTIAL_ID"],
            os.environ["LABQOAT_WORKER_SECRET"],
            timing=timing,
            session_socket=os.environ.get("LABQOAT_SESSION_SOCKET"),
        )
