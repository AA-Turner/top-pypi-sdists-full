"""List projects and mark the one this invocation acts on."""

from __future__ import annotations

from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class ProjectListCommand(EndpointCommand):
    """Show what every project owns, with the selected project named even before it exists."""

    def __init__(self) -> None:
        """Declare the project collection and the switch that reads its archived side."""
        super().__init__(
            "list",
            "/api/v1/projects",
            [
                click.Option(
                    ["--archived"],
                    is_flag=True,
                    flag_value="true",
                    default=None,
                    help="List the archived projects instead of the active ones.",
                )
            ],
            "List active projects and what each owns. `selected` marks the project that commands act on.",
        )

    def _write_response(self, client: ManagementClient, query: dict[str, object]) -> None:
        """Flag the selected row and repeat its name beside the table."""
        selected = ContextAccessor.current().selection().name
        items: list[JsonValue] = []
        for raw in JsonDocument.expect_list(client.get(self._path, query)["items"]):
            item = JsonDocument.expect_dict(raw)
            items.append({**item, "selected": item["name"] == selected})
        ResultWriter().write_dict({"items": items, "selected": selected})
