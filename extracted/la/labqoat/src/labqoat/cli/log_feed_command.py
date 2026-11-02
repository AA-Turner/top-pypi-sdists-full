"""Finite JSON pages and server-sent operational log entries."""

from __future__ import annotations

from collections.abc import Sequence
from contextlib import closing
from typing import TYPE_CHECKING

import click

from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.console.console_options import ConsoleOptions
from labqoat.cli.console.run_console import RunConsole
from labqoat.cli.console.console_entry import ConsoleEntry
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class LogFeedCommand(EndpointCommand):
    """Reuse strict endpoint reads while optionally following a single stream."""

    def __init__(
        self,
        path: str,
        params: Sequence[click.Parameter],
        help_text: str,
        reference_name: str,
    ) -> None:
        """Add the shared log-following flag to an operational endpoint."""
        controls = self.controls()
        super().__init__("logs", path, [*params, ParameterFactory.follow(), *controls], help_text, reference_name)

    @staticmethod
    def controls() -> list[click.Parameter]:
        """Operational feeds share presentation controls without run-tree selectors."""
        selected = [
            p
            for p in ConsoleOptions.parameters("info")
            if p.name in ("level", "source", "build_output", "timestamps", "json")
        ]
        for parameter in selected:
            if parameter.name == "build_output":
                parameter.default = "full"
        return selected

    def _write_response(self, client: ManagementClient, query: dict[str, object]) -> None:
        """Render one page or raw entry JSONL from the companion SSE endpoint."""
        options = ConsoleOptions.current(query)
        for parameter in self.controls():
            query.pop(str(parameter.name), None)
        console = RunConsole(options, records=True)
        try:
            if query.pop("follow"):
                self.follow(client, query, console)
            else:
                self.page(client.get(self._path, query), console)
            console.flush()
        finally:
            console.close()

    def page(self, page: JsonDocument, console: RunConsole) -> None:
        """Render a finite machine page or its readable log entries."""
        if console.options.json:
            ResultWriter().write_dict(self.filtered(page, console))
        else:
            for item in JsonDocument.expect_list(page["items"]):
                self.render(JsonDocument.expect_dict(item), console)

    def follow(self, client: ManagementClient, query: dict[str, object], console: RunConsole) -> None:
        """Render each incoming log immediately and preserve remote stream failures."""
        with closing(client.stream_events(f"{self._path}/stream", query)) as events:
            for event in events:
                if event.get("event") == "log.entry":
                    self.render(JsonDocument.expect_dict(event.get("data")), console)
                elif event.get("event") == "log.error":
                    data = JsonDocument.expect_dict(event.get("data"))
                    raise ApiError(str(data.get("detail") or data.get("message") or "Log stream failed."))

    def render(self, entry: JsonDocument, console: RunConsole) -> None:
        """Supply the known build source while retaining attributed worker evidence."""
        effective = self.attributed(entry)
        if not console.visible(ConsoleEntry(effective)):
            return
        if console.options.json:
            ResultWriter(pretty=False).write_dict(entry)
            return
        console.accept(effective)

    def attributed(self, entry: JsonDocument) -> JsonDocument:
        """Identify build records and logical owners of shared machine output."""
        if self._path.startswith("/api/v1/builds/"):
            return JsonDocument(entry, stream="build")
        source = entry.get("source")
        owner = source.get("run_id", "") if isinstance(source, dict) else ""
        return JsonDocument(entry, run_path=entry.get("run_path") or entry.get("run_id") or owner)

    def filtered(self, page: JsonDocument, console: RunConsole) -> JsonDocument:
        """Keep page cursors while applying the same visibility rules as followed records."""
        items = [JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(page["items"])]
        return JsonDocument(
            page, items=[item for item in items if console.visible(ConsoleEntry(self.attributed(item)))]
        )
