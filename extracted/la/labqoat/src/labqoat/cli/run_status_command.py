"""``lab run status``: where a run stands, without its arguments, resources or identities."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, ClassVar

import click

from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class RunStatusCommand(EndpointCommand):
    """Read the run and keep its state, timing, failure and parent."""

    FIELDS: ClassVar[tuple[str, ...]] = (
        "id",
        "name",
        "status",
        "state",
        "terminal",
        "failure_detail",
        "inserted_at",
        "started_at",
        "ended_at",
        "owner_run_id",
        "child_operation_key",
    )

    def __init__(self, reference: Sequence[click.Parameter]) -> None:
        """Bind the run reference."""
        super().__init__(
            "status",
            "/api/v1/runs/{ref}",
            reference,
            "Show a run's state, timing, failure and parent; lab run get has its arguments and resources.",
            "run_ref",
        )

    def _write_response(self, client: ManagementClient, query: dict[str, object]) -> None:
        """Render the fields that say where the run stands, with the newest value of each metric it logs."""
        document = client.get(self._path, query)
        status: dict[str, JsonValue] = {key: document[key] for key in self.FIELDS if key in document}
        latest = client.get(f"{self._path}/metrics", {**query, "latest": "true"})
        metrics = {
            str(item["name"]): f"{item['value']:.6g} @ step {item['step']}"
            for item in map(JsonDocument.expect_dict, JsonDocument.expect_list(latest.get("items", [])))
            if isinstance(item.get("value"), (int, float))
        }
        if metrics:
            status["metrics"] = dict(metrics)
        ResultWriter().write_dict(status)
