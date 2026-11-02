"""Where dict and queue requests go."""

from collections.abc import Mapping
from typing import Protocol

from labqoat.coordination.store_reply import StoreReply
from labqoat.json_document import JsonValue


class StoreChannel(Protocol):
    """The management API for people, the worker API for runs; paths start after the API's own prefix."""

    def send(
        self, method: str, path: str, document: Mapping[str, JsonValue] | None = None, wait: float = 0.0
    ) -> StoreReply:
        """Send one request the service may hold for up to ``wait`` seconds before it answers."""
        ...
