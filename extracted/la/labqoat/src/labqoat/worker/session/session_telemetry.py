"""Small telemetry windows ride the supervisor's persistent session instead of a new upload connection."""

import json
from collections.abc import Callable
from dataclasses import dataclass

from labqoat.json_document import JsonDocument
from labqoat.worker.session.local_session_client import LocalSessionClient
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass(frozen=True)
class SessionTelemetry:
    """Deliver bounded evidence through delegated local IPC only after the service negotiated support."""

    local: LocalSessionClient
    negotiated: Callable[[], bool]
    limit: int = 262_144

    def accepts(self, frames: list[bytes]) -> bool:
        """Leave large replay windows on the streaming upload so they never delay lifecycle commands."""
        return self.negotiated() and sum(map(len, frames)) <= self.limit

    def deliver(self, frames: list[bytes]) -> None:
        """Require a durable receipt for every frame; an interrupted window is replayed unchanged."""
        for frame in frames:
            message = JsonDocument.expect_dict(json.loads(frame[4:]))
            if self.local.request("telemetry", message) != {"status": "ok"}:
                raise WorkerApiError("Worker telemetry acknowledgement is invalid", 502)
