"""``lab compute quotas``: the provider quotas behind each location, so quota and missing capacity read apart."""

from __future__ import annotations

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument, JsonValue


class QuotasCommand(StrictCommand):
    """One line per quota as acquisition last observed it: limit, use and what is left."""

    def __init__(self) -> None:
        """Declare the command; it takes no options."""
        super().__init__(
            "quotas",
            help=(
                "Show each location's provider quotas (on-demand and spot vCPUs per instance group, GPUs) with "
                "limit, use and what is free. A run waiting for provider quota waits on a group with nothing free."
            ),
        )

    def invoke(self, ctx: click.Context) -> object:
        """Read the locations once and list their quotas."""
        client = ContextAccessor.current().management()
        try:
            registry = client.get("/api/v1/locations", {})
            locations = [JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(registry["locations"])]
            rows: list[JsonValue] = [row for location in locations for row in QuotasCommand.rows(location)]
            ResultWriter().write_dict(JsonDocument(quotas=rows))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def rows(location: JsonDocument) -> list[JsonValue]:
        """The quotas of one location, smallest headroom first."""
        capacity = location.get("capacity")
        quotas = JsonDocument.expect_dict(capacity).get("quotas") if isinstance(capacity, dict) else None
        found = (
            [QuotasCommand.row(location, JsonDocument.expect_dict(item)) for item in quotas or []]
            if isinstance(quotas, list)
            else []
        )
        found.sort(key=QuotasCommand.free)
        return list(found)

    @staticmethod
    def free(row: dict[str, JsonValue]) -> int:
        """Sort key: what is left of a quota, unknown last."""
        free = row["free"]
        return free if isinstance(free, int) else 1 << 62

    @staticmethod
    def row(location: JsonDocument, quota: JsonDocument) -> dict[str, JsonValue]:
        """One quota in the words a placement message uses."""
        scope = JsonDocument.expect_dict(quota.get("scope", {}))
        limit, usage = quota.get("limit"), quota.get("usage")
        free = limit - usage if isinstance(limit, int) and isinstance(usage, int) else None
        metric = str(quota.get("metric", ""))
        return {
            "location": location.get("id"),
            "group": scope.get("group"),
            "kind": "spot" if "spot" in metric else "on-demand",
            "unit": quota.get("unit"),
            "limit": limit,
            "used": usage,
            "free": free,
            "current": quota.get("fresh"),
            "observed_at": quota.get("observed_at"),
            "error": quota.get("error"),
        }
