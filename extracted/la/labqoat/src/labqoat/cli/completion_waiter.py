"""Shared event-driven waiting for durable asynchronous operations."""

from __future__ import annotations

from typing import TYPE_CHECKING
from contextlib import closing

from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class CompletionWaiter:
    """Drain a completion stream and fetch the authoritative final document once."""

    @staticmethod
    def wait(
        client: ManagementClient,
        submitted: JsonDocument,
        pending: frozenset[str],
        path: str,
        kind: str,
    ) -> JsonDocument:
        """Require a matching completion event before resolving a pending operation."""
        identifier = JsonDocument.expect_scalar(submitted.get("id"), str)
        status = JsonDocument.expect_scalar(submitted.get("status"), str)
        if status not in pending:
            return submitted
        completed = False
        with closing(client.stream(f"{path}/stream", {"ref": identifier})) as events:
            for event in events:
                resource = event.get("resource")
                resource_id = resource.get("id") if isinstance(resource, dict) else event.get("id")
                if event.get("type") == f"{kind}.complete" and resource_id == identifier:
                    completed = True
        if not completed:
            raise ApiError(f"{kind} {identifier} stream closed before completion")
        current = client.get(path, {"ref": identifier})
        if current.get("status") in pending:
            raise ApiError(f"{kind} {identifier} remained pending after completion")
        return current
