"""Bounded transport recovery for cursor-addressed run-tree console evidence."""

from collections.abc import Generator
from time import sleep
from typing import TYPE_CHECKING
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from labqoat.errors.api_error import ApiError
from labqoat.errors.transport_error import TransportError
from labqoat.json_document import JsonDocument
from labqoat.reconnect_budget import ReconnectBudget
from labqoat.sse_client import SseClient

if TYPE_CHECKING:
    from labqoat.base_client import BaseClient


class RunLogStream:
    """Close every interrupted response and resume only from the last delivered evidence cursor."""

    def __init__(self, client: "BaseClient", target: str) -> None:
        """Keep the original filter scope unchanged across every reconnect."""
        self.client = client
        self.target = target
        self.cursor: str | None = None
        self.complete = False

    def entries(self) -> Generator[JsonDocument]:
        """Recover transient network failures without converting service errors into success.

        A watch may outlive any number of connections: only eight reconnects in a row after connections that
        ended at once with nothing new are treated as the service being unavailable.
        """
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
            if self.complete:
                return
            if budget.exhausted(progressed=self.cursor != seen):
                raise TransportError(f"Log stream reconnect limit exceeded; last cursor: {self.cursor or 'start'}.")
            sleep(budget.delay())

    def follow(self) -> Generator[JsonDocument]:
        """Persist a cursor before yielding so early caller disconnect always closes cleanly."""
        with self.client.stream_response("GET", self.resumed(), event_stream=True) as response:
            documents = SseClient.parse_stream(response.iter_bytes())
            for document in documents:
                kind = document.get("type")
                if kind in ("parse_error", "run.logs.error"):
                    raise ApiError(str(document.get("detail", "Malformed or rejected run log stream.")))
                cursor = document.get("cursor")
                if isinstance(cursor, str):
                    self.cursor = cursor
                self.complete = kind == "run.logs.complete"
                yield document
                if self.complete:
                    # Reading the service's end of stream returns the connection for the result requests.
                    next(documents, None)
                    return

    def resumed(self) -> str:
        """Replace only the replay position, preserving selectors and encoded child keys."""
        if self.cursor is None:
            return self.target
        parts = urlsplit(self.target)
        params = dict(parse_qsl(parts.query))
        params["cursor"] = self.cursor
        return urlunsplit(parts._replace(query=urlencode(params)))
