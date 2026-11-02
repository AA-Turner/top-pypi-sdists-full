"""A dashboard's leader and frontier changes followed across any number of connections."""

from __future__ import annotations

from collections.abc import Generator
from time import sleep
from typing import TYPE_CHECKING
from urllib.parse import urlencode

from labqoat._generated.dashboard_change import DashboardChange
from labqoat._generated.dashboard_change_page import DashboardChangePage
from labqoat.errors.api_error import ApiError
from labqoat.errors.transport_error import TransportError
from labqoat.json_document import JsonDocument
from labqoat.reconnect_budget import ReconnectBudget
from labqoat.sse_client import SseClient

if TYPE_CHECKING:
    from labqoat.base_client import BaseClient


class DashboardChangeStream:
    """Start after the newest recorded change and resume every reconnect after the last one delivered."""

    def __init__(self, client: BaseClient, ref: str, panel: str | None = None, cursor: str | None = None) -> None:
        """Keep the dashboard, the optional panel and an explicit starting position."""
        self.client = client
        self.ref = ref
        self.panel = panel
        self.cursor = cursor

    def changes(self) -> Generator[DashboardChange]:
        """Yield changes as they are recorded, reconnecting while the service stays reachable.

        A watch has no end of its own: only eight reconnects in a row after connections that ended at once
        with nothing new are treated as the service being unavailable.
        """
        if self.cursor is None:
            self.cursor = self.newest()
        budget = ReconnectBudget(8)
        while True:
            seen = self.cursor
            budget.opened()
            try:
                yield from self.follow()
            except TransportError:
                pass
            except ApiError as error:
                if error.status not in (502, 503, 504):
                    raise
            if budget.exhausted(progressed=self.cursor != seen):
                raise TransportError(f"Dashboard change stream reconnect limit exceeded; last cursor: {self.cursor}.")
            sleep(budget.delay())

    def newest(self) -> str:
        """Read where the change log ends now, so a reconnect cannot skip what is recorded meanwhile."""
        path = self.target("/api/v1/dashboards/item/changes", {"limit": "1"})
        page = self.client.decode(self.client.send("GET", path), path, DashboardChangePage.from_dict)
        return page.items[0].cursor if page.items else f"dashboard-{self.ref}-0"

    def follow(self) -> Generator[DashboardChange]:
        """Record each change's position before yielding it, so an early close resumes after it."""
        path = self.target("/api/v1/dashboards/item/changes/stream", {"cursor": self.cursor, "wait_ms": "5000"})
        with self.client.stream_response("GET", path, event_stream=True) as response:
            for event in SseClient.parse_events(response.iter_bytes()):
                change = DashboardChange.from_dict(JsonDocument.expect_dict(event["data"]))
                self.cursor = change.cursor
                yield change

    def target(self, path: str, query: dict[str, str | None]) -> str:
        """Address one dashboard, narrowed to the chosen panel when there is one."""
        selected = {"ref": self.ref, "panel": self.panel, **query}
        return f"{path}?{urlencode({name: value for name, value in selected.items() if value is not None})}"
