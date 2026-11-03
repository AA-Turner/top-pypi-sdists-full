"""Failed events («eventos fallidos»): the port of the dead letter of the events EventBridge refused.

Write only, no cache (ADR-002 of api-chatty: events go out as they do today, an outbox comes later). Collection
`failed_events`. A record is a plain dict that the publisher builds (`events/events_manager.py` in api-chatty):
`event` (whatever `Event.model_dump_json()` answers: JSON text for most classes, a dict for the ones that override it), `eventbridge_source`, `error_code`, `error_message`, `retry_count` and `timestamp`
(UTC). Nothing in api-chatty reads it back but the health board (`company/analytics/health/`), which queries the
collection directly.
"""
from __future__ import annotations

from typing import Any, Dict, List, Protocol


class FailedEventSink(Protocol):
    async def insert_many(self, records: List[Dict[str, Any]]) -> List[Any]:
        """Stores every record, in order, and returns the ids it stored. Mongo adds `_id` to each record in place, as
        the driver does."""
        ...
