"""Deterministic memory publication keys and bounded retries for lost responses."""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Mapping
from typing import TYPE_CHECKING

from labqoat.errors.api_error import ApiError
from labqoat.errors.transport_error import TransportError
from labqoat.json_document import JsonDocument

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class MemoryWrites:
    """Retry exactly the same authored payload; conflicts always reach the caller."""

    @staticmethod
    def key(path: str, query: Mapping[str, object], payload: JsonDocument) -> str:
        """Derive a durable key from scope, operation and canonical authored content."""
        body = json.dumps([path, dict(query), payload], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return "memory:" + hashlib.sha256(body.encode("utf-8")).hexdigest()

    @staticmethod
    def send(client: ManagementClient, path: str, query: Mapping[str, object], payload: JsonDocument) -> JsonDocument:
        """Retry transport failures and temporary service errors at most twice."""
        for attempt in range(2):
            try:
                return client.post(path, query, payload)
            except ApiError as error:
                if not MemoryWrites.retryable(error):
                    raise
                time.sleep(0.2 * (2**attempt))
        return client.post(path, query, payload)

    @staticmethod
    def retryable(error: ApiError) -> bool:
        """Limit automatic retries to failures compatible with permanent key replay."""
        return isinstance(error, TransportError) or error.status in (429, 502, 503, 504)
