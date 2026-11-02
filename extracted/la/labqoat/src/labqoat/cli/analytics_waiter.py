"""Event-driven waiting for durable governed analytics completion."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from labqoat.cli.completion_waiter import CompletionWaiter
from labqoat.json_document import JsonDocument

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class AnalyticsWaiter:
    """Resolve an accepted analytics intent to its authoritative terminal row."""

    _PENDING: ClassVar[frozenset[str]] = frozenset({"accepted", "running"})
    _TERMINAL: ClassVar[frozenset[str]] = frozenset({"succeeded", "failed"})

    @staticmethod
    def wait(
        client: ManagementClient,
        submitted: JsonDocument,
    ) -> JsonDocument:
        """Wait by durable query ID until execution succeeds or fails."""
        current = CompletionWaiter.wait(
            client, submitted, AnalyticsWaiter._PENDING, "/api/v1/analytics-queries/item", "analytics"
        )
        query_id = JsonDocument.expect_scalar(current.get("id"), str)
        status = AnalyticsWaiter._status(current)

        if status not in AnalyticsWaiter._TERMINAL:
            raise ValueError(f"analytics query {query_id} returned unknown status {status!r}")
        return current

    @staticmethod
    def _status(document: JsonDocument) -> str:
        """Read the required lifecycle state."""
        return JsonDocument.expect_scalar(document.get("status"), str)
