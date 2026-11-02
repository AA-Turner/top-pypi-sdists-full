"""Governed analytics and operational inspection client."""

from __future__ import annotations

from collections.abc import Mapping

from labqoat._generated.analytics_query import AnalyticsQuery
from labqoat.base_client import BaseClient
from labqoat.json_document import JsonValue


class AnalyticsClient(BaseClient):
    """Governed queries and samples."""

    def submit_query(self, payload: Mapping[str, JsonValue]) -> AnalyticsQuery:
        """Submit a governed query."""
        response = self.send_json("POST", "/api/v1/analytics-queries", payload)
        return self.decode(response, "/api/v1/analytics-queries", AnalyticsQuery.from_dict)

    def get_query(self, ref: str) -> AnalyticsQuery:
        """Read a retained query."""
        path = f"/api/v1/analytics-queries/item?ref={BaseClient.encode_ref(ref)}"
        return self.decode(self.send("GET", path), path, AnalyticsQuery.from_dict)

    def sample(self, payload: Mapping[str, JsonValue]) -> AnalyticsQuery:
        """Submit a bounded sample as a query."""
        return self.submit_query(payload)
