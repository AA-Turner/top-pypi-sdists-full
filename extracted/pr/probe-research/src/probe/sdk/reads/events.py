"""The backend's append-only ``events`` log (fold #10).

``EventsReadClient`` is READ-ONLY: events are emitted server-side (run created/
updated, spans, gc, ...). Exposed as ``client.events``.

``NoteClient`` (a research-note vocabulary encoded into ``kind="note"`` artifacts)
was removed: nothing server-side used its eight kinds beyond one list filter, and
durable claims already live in repo markdown. A text note needs no schema.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client.client import Client
    from ..delivery.transport.transport import Page


class EventsReadClient:
    """Read the backend append-only lifecycle+structure events log (fold #10).

    Read-only: events are emitted server-side (run created/updated, spans, gc, ...)."""

    def __init__(self, client: "Client"):
        self.client = client

    def list(self, **params: Any) -> "Page":
        """GET /v1/events (keyset paginated)."""
        return self.client.transport.get_page("/v1/events", params=params or None)

    def for_run(self, run_id: str) -> list[dict]:
        """GET /v1/runs/{id}/events."""
        return self.client.transport.get(f"/v1/runs/{run_id}/events")
