"""Readable run watching with a silent outcome-only mode."""

from collections.abc import Sequence
from contextlib import closing

import sys

import click

from labqoat.cli.console.console_options import ConsoleOptions
from labqoat.cli.console.run_banner import RunBanner
from labqoat.cli.console.run_console import RunConsole
from labqoat.cli.output.output_style import OutputStyle
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.observation_deadline import ObservationDeadline
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.strict_command import StrictCommand


class RunWatchCommand(StrictCommand):
    """Observe logs until completion without taking cancellation ownership."""

    def __init__(self, params: Sequence[click.Parameter], expected_kind: str | None = None) -> None:
        """Expose consistent presentation controls alongside a local observation timeout."""
        super().__init__(
            "watch",
            params=[
                *params,
                *ConsoleOptions.parameters(),
                click.Option(["--silent"], is_flag=True),
                click.Option(["--cursor"], help="Resume from an opaque log stream cursor."),
                ObservationDeadline.option(),
            ],
            help="Watch run progress and logs; --silent prints only the final outcome.",
        )
        self._expected_kind = expected_kind

    def invoke(self, ctx: click.Context) -> object:
        """Read the authoritative final state after draining retained output."""
        options = ConsoleOptions.current(ctx.params)
        reference = str(ctx.params["run_ref"])
        link = f"{ContextAccessor.current().profile.base_url.rstrip('/')}/runs/{reference}"
        console = RunConsole(options, observing=True, link=link)
        if not (options.json or options.silent):
            for line in RunBanner.lines(OutputStyle.current(sys.stderr), reference, "", link):
                click.echo(line, err=True)
        client = ContextAccessor.current().management()
        query: dict[str, object] = {"ref": ctx.params["run_ref"], "expected_kind": self._expected_kind}
        selection = ConsoleOptions.selection(ctx.params)
        try:
            with (
                ObservationDeadline.current(str(query["ref"])).watching(),
                closing(
                    client.stream(
                        "/api/v1/runs/{ref}/logs",
                        {
                            **query,
                            **selection,
                            "follow": "true",
                            "include_metrics": "true",
                            "cursor": ctx.params["cursor"],
                        },
                    )
                ) as entries,
            ):
                for entry in entries:
                    console.accept(entry)
                result = client.get("/api/v1/runs/{ref}", query)
                code = console.finish(result)
            ctx.exit(code)
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            console.close()
            client.close()
