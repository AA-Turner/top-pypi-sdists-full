"""Validate resource-bound Run stream envelopes before advancing any waiter's replay cursor."""

from labqoat._generated.run_stream_event import RunStreamEvent
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument


class RunEventCursor:
    """Keep ordinary and recovery waiters on identical scoped event identity checks."""

    @staticmethod
    def position(run_id: str, event: RunStreamEvent) -> str:
        """Reject cross-resource or inconsistent envelopes before recording their replay position."""
        try:
            resource = JsonDocument.expect_dict(event.data["resource"])
            cursor = JsonDocument.expect_scalar(event.data["cursor"], str)
            if resource != {"type": "run", "id": run_id} or not event.event.startswith("run."):
                raise ValueError("invalid resource or cursor")
            expected_id = RunEventCursor._event_id(run_id, event.event, cursor)
            if event.id != expected_id or event.data.get("id") != event.id or event.data.get("type") != event.event:
                raise ValueError("inconsistent event envelope")
            return cursor
        except (KeyError, TypeError, ValueError) as error:
            raise ApiError(f"Malformed Run event: {error}") from error

    @staticmethod
    def _event_id(run_id: str, event: str, cursor: str) -> str:
        """Validate scoped positions independently of the snapshot's synthetic SSE identity."""
        prefix = f"run-{run_id}-"
        position = cursor.removeprefix(prefix)
        terminal = event == "run.complete"
        valid_position = position == "complete" if terminal else position.isascii() and position.isdigit()
        if not cursor.startswith(prefix) or not valid_position:
            raise ValueError("invalid resource or cursor")
        return prefix + "snapshot" if event == "run.snapshot" else cursor
