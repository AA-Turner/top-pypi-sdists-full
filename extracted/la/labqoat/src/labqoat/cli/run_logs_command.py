"""Finite and followed run log feeds."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, ClassVar
from contextlib import closing

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.console.console_options import ConsoleOptions
from labqoat.cli.console.run_console import RunConsole
from labqoat.json_document import JsonDocument
from labqoat.cli.strict_command import StrictCommand
from labqoat.cli.output.json_writer import JsonWriter
from labqoat.cli.console.log_selection import LogSelection

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class RunLogsCommand(StrictCommand):
    """Select the bounded JSON page or terminal SSE log feed for one run."""

    path = "/api/v1/runs/{ref}/logs"

    def __init__(self, params: Sequence[click.Parameter], expected_kind: str | None = None) -> None:
        """Store the optional workload-kind constraint."""
        for parameter in params:
            if parameter.name == "limit":
                parameter.default = None
                parameter.type = click.IntRange(1, 200)
        super().__init__(
            "logs",
            params=[
                *params,
                *ConsoleOptions.parameters("info"),
                *LogSelection.parameters(),
                click.Option(["--grep"], help="Only lines containing TEXT, filtered on the server."),
            ],
            help="Read or follow build, lifecycle and execution logs: the newest 100 lines unless selected otherwise.",
        )
        self._expected_kind = expected_kind

    def invoke(self, ctx: click.Context) -> object:
        """Read or follow the run logs and render their native JSON shape."""
        query = self._query(ctx.params)
        console = RunConsole(ConsoleOptions.current(ctx.params), records=True)
        client = ContextAccessor.current().management()
        try:
            if ctx.params["follow"]:
                self._write_stream(client, query, console)
            else:
                printed = self.pages(client, query, console, bool(ctx.params["all"]))
                self.advise(printed, query)
            console.flush()
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            console.close()
            client.close()
        return None

    UNFILTERED: ClassVar[int] = 500

    @classmethod
    def advise(cls, printed: int, query: Mapping[str, object]) -> None:
        """After a long unfiltered history, point at the filters that run on the server."""
        if printed > cls.UNFILTERED and not any(query.get(key) for key in ("grep", "since", "until", "source")):
            click.echo(
                f"hint printed {printed} lines; --grep TEXT, --level warning or --since 10m filter on the server.",
                err=True,
            )

    def pages(self, client: ManagementClient, query: dict[str, object], console: RunConsole, all_pages: bool) -> int:
        """Walk complete history with bounded pages, or print one tail and its continuation; return the count."""
        printed = 0
        while True:
            page = client.get(self.path, query)
            for entry in JsonDocument.expect_list(page["items"]):
                console.accept(JsonDocument.expect_dict(entry))
                printed += 1
            cursor = page.get("next_cursor")
            if not all_pages or not cursor:
                break
            query = dict(query, cursor=cursor)
        if console.options.json:
            JsonWriter(pretty=False).write_dict(JsonDocument(next=cursor))
        return printed

    def _query(self, values: Mapping[str, object]) -> dict[str, object]:
        """Translate Click values into the run log query contract."""
        query = {
            name: value
            for name, value in values.items()
            if name in ("run_ref", "limit", "cursor") and value is not None
        }
        query["ref"] = query.pop("run_ref")
        query.update(ConsoleOptions.selection(values))
        query.update(LogSelection.query(values))
        if "metric" in str(values.get("source", "")).split(","):
            query["include_metrics"] = "true"
        query.update({key: values[key] for key in ("source", "level", "grep") if values.get(key)})
        # Pages and cursors count what the service returns, so build output this console would discard is
        # withheld there; otherwise a page from the start of a run is all hidden build lines and looks empty.
        builds = ConsoleOptions.current(values).delivered_builds()
        if builds is not None:
            query["build_output"] = builds
        if self._expected_kind is not None:
            query["expected_kind"] = self._expected_kind
        if values["follow"]:
            query.pop("limit", None)
            query["follow"] = "true"
        return query

    def _write_stream(self, client: ManagementClient, query: Mapping[str, object], console: RunConsole) -> None:
        """Render each validated stream document as one JSON line."""
        with closing(client.stream(self.path, query)) as entries:
            for document in entries:
                console.accept(document)
