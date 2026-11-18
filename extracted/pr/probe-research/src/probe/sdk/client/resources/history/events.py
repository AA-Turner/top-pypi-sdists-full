"""`client.events`: the team's append-only event log (run created, renamed, files, lineage...), read newest
first, forward from a saved cursor for an incremental sync, or as the live poll (twins: app/projects/events,
app/live)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from .....generated.models import EventOut, LivePoll

if TYPE_CHECKING:
    from ....delivery.transport.transport import Page
    from ...client import Client

#: `after=` for a forward sync's first page: from the team's oldest event.
FEED_START = "start"


class EventFeed:
    """The events after a cursor, oldest first, until caught up. Iterate it for `EventOut`s; `cursor` is where
    to resume next time (it moves once a page is fully yielded). The server holds back events younger than 30 s,
    so a sync resumed from `cursor` misses none."""

    def __init__(self, client: Client, after: str, *, limit: int | None = None) -> None:
        self._client = client
        self.cursor = after
        self._limit = limit

    def __iter__(self) -> Iterator[EventOut]:
        while True:
            page = self._client.events.list_after(self.cursor, limit=self._limit)
            for row in page.items:
                yield EventOut.model_validate(row)
            moved = bool(page.next_cursor) and page.next_cursor != self.cursor
            if moved:
                self.cursor = page.next_cursor
            if not page.items or not moved:
                return


class EventsReadClient:
    """Read the team's event log. Read-only: the server writes events (run created/updated, spans, gc...)."""

    def __init__(self, client: Client):
        self.client = client

    def list(self, **filters: Any) -> Page:
        """GET /v1/events: one page, newest first (`cursor` pages back)."""
        return self.client.transport.get_page("/v1/events", params=filters or None)

    def list_after(self, after: str = FEED_START, *, limit: int | None = None) -> Page:
        """GET /v1/events?after=: one page oldest first; its `next_cursor` is always set, to resume from."""
        filters: dict[str, Any] = {"after": after}
        if limit is not None:
            filters["limit"] = limit
        return self.client.transport.get_page("/v1/events", params=filters)

    def iter(self, after: str = FEED_START, *, limit: int | None = None) -> EventFeed:
        """Every event after `after` (a saved `EventFeed.cursor`, or `start`), oldest first, page by page."""
        return EventFeed(self.client, after, limit=limit)

    def list_for_run(self, run_id: str) -> list[dict]:
        """GET /v1/runs/{id}/events."""
        return self.client.transport.get(f"/v1/runs/{run_id}/events")

    for_run = list_for_run  # the name before api-access T4, kept for scripts written against it

    def poll_live(
        self,
        *,
        run: str | None = None,
        experiment: str | None = None,
        project: str | None = None,
        kinds: str | None = None,
        since: int | None = None,
        wait: float | None = None,
        limit: int | None = None,
    ) -> LivePoll:
        """GET /v1/live/events/poll: the live events after seq `since`, waiting up to `wait` s for one. A script
        that wants a stream uses `probe.events.stream` instead."""
        filters = {
            key: value
            for key, value in {
                "run": run, "experiment": experiment, "project": project, "kinds": kinds, "since": since,
                "wait": wait, "limit": limit,
            }.items()
            if value is not None
        }
        return LivePoll.model_validate(self.client.transport.get("/v1/live/events/poll", params=filters or None))
