"""Operational inspection client."""

from __future__ import annotations

from labqoat.base_client import BaseClient
from labqoat.json_document import JsonDocument


class OperationsClient(BaseClient):
    """Events, worker history, and capabilities."""

    def events(self, limit: int = 20) -> JsonDocument:
        """Read operation events."""
        return JsonDocument.expect_dict(self.send("GET", f"/api/v1/operation-events?limit={limit}").json())

    def worker_history(self, limit: int = 20) -> JsonDocument:
        """Read worker history."""
        return JsonDocument.expect_dict(self.send("GET", f"/api/v1/worker-history?limit={limit}").json())

    def capabilities(self) -> JsonDocument:
        """Read capabilities."""
        return JsonDocument.expect_dict(self.send("GET", "/api/v1/capabilities").json())

    def status(self) -> JsonDocument:
        """Read protected status."""
        return JsonDocument.expect_dict(self.send("GET", "/api/v1/status").json())
