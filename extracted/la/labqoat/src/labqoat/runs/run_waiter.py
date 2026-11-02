"""Event-backed Run waiting with scoped cursors, authoritative terminal reads and bounded transport recovery."""

from collections.abc import Iterator
from contextlib import closing
from time import sleep
from typing import TYPE_CHECKING

from labqoat._generated.run import Run
from labqoat._generated.run_stream_event import RunStreamEvent
from labqoat.errors.api_error import ApiError
from labqoat.errors.run_failed_error import RunFailedError
from labqoat.errors.transport_error import TransportError
from labqoat.reconnect_budget import ReconnectBudget
from labqoat.json_document import JsonDocument
from labqoat.runs.run_event_cursor import RunEventCursor

if TYPE_CHECKING:
    from labqoat.runs_client import RunsClient


class RunWaiter:
    """Read at entry and reconnect boundaries; ordinary progress comes only from the Run event stream."""

    _states = frozenset(
        {
            "pending",
            "preparing",
            "validating",
            "queued",
            "starting",
            "running",
            "finalizing",
            "cancelling",
            "completed",
            "completed_with_errors",
            "failed",
            "cancelled",
        }
    )

    def __init__(self, client: "RunsClient", run_id: str, expected_kind: str | None, max_reconnects: int) -> None:
        """Bind a finite reconnect budget and every observed frame to one immutable Run identity."""
        if max_reconnects < 0:
            raise ValueError("max_reconnects must be nonnegative")
        self._client = client
        self._id = run_id
        self._kind = expected_kind
        self._max_reconnects = max_reconnects
        self._cursor: str | None = None

    def run(self) -> Run:
        """Close interrupted streams before reading authoritative state, including after terminal frames."""
        budget = ReconnectBudget(self._max_reconnects)
        current: Run | None = None
        while True:
            seen = self._cursor
            budget.opened()
            try:
                current = self._observe(current)
                if self._terminal(current):
                    return current
            except TransportError:
                current = None
            except ApiError as error:
                if error.status not in (502, 503, 504):
                    raise
                current = None
            if budget.exhausted(progressed=self._cursor != seen):
                raise TransportError("Run event stream reconnect limit exceeded.")
            sleep(budget.delay())

    def _observe(self, current: Run | None) -> Run:
        """Use a known nonterminal snapshot until the event stream next closes or reports completion."""
        if current is None:
            current = self._read()
        if self._terminal(current):
            return current
        self._follow()
        current = self._read()
        if self._cursor == f"run-{self._id}-complete":
            self._cursor = None
        return current

    def _follow(self) -> None:
        """Retain only verified replay positions and promptly release terminal or interrupted HTTP responses."""
        try:
            with closing(self._client.events(self._id, cursor=self._cursor, expected_kind=self._kind)) as events:
                self._consume(events)
        except TransportError:
            return
        except ApiError as error:
            self._recover(error)

    def _consume(self, events: Iterator[RunStreamEvent]) -> None:
        """Advance through verified events until completion requires an authoritative read."""
        for event in events:
            self._cursor = RunEventCursor.position(self._id, event)
            if event.event == "run.complete":
                return
            if event.event == "run.snapshot" and self._snapshot_terminal(event):
                return

    def _recover(self, error: ApiError) -> None:
        """Reset rejected replay positions and retry only explicit transient upstream failures."""
        if error.status == 422 and self._cursor is not None:
            self._cursor = None
        elif error.status not in (502, 503, 504):
            raise error

    def _read(self) -> Run:
        """Keep unknown states and cross-resource responses from being mistaken for successful completion."""
        current = self._client.get(self._id, expected_kind=self._kind)
        if current.id != self._id or current.status not in self._states:
            raise ApiError("Malformed Run identity or status")
        return current

    @staticmethod
    def _terminal(run: Run) -> bool:
        """Only an authoritative successful terminal Run returns normally."""
        if run.status in ("failed", "cancelled", "completed_with_errors"):
            raise RunFailedError(run)
        return run.status == "completed"

    @staticmethod
    def _snapshot_terminal(event: RunStreamEvent) -> bool:
        """A terminal snapshot triggers an authoritative read rather than supplying the final resource."""
        try:
            data = JsonDocument.expect_dict(event.data.get("data"))
            status = JsonDocument.expect_scalar(data.get("status"), str)
            if status not in RunWaiter._states:
                raise ValueError("unknown snapshot status")
            return status in ("completed", "completed_with_errors", "failed", "cancelled")
        except (TypeError, ValueError) as error:
            raise ApiError(f"Malformed Run snapshot: {error}") from error
