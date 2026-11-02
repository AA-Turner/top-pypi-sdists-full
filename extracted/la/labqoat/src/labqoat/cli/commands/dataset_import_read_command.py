"""Read durable import progress or resume event-backed waiting."""

from contextlib import closing

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.cli.observation_deadline import ObservationDeadline


class DatasetImportReadCommand(StrictCommand):
    """Inspect a previously accepted import after disconnecting the original CLI."""

    def __init__(self) -> None:
        """Accept the durable ID returned by import admission."""
        super().__init__(
            "get",
            help="Read an import or wait for its published revision.",
            params=[
                click.Argument(["import_id"]),
                click.Option(["--wait"], is_flag=True),
                ObservationDeadline.option(),
            ],
        )

    def invoke(self, ctx: click.Context) -> object:
        """Read authoritative state with the active profile's API credentials."""
        try:
            with (
                closing(ContextAccessor.current().datasets()) as client,
                ObservationDeadline.current(str(ctx.params["import_id"])).watching(),
            ):
                identity = ctx.params["import_id"]
                result = (
                    client.wait_import(identity).to_dict()
                    if ctx.params["wait"]
                    else client.get_import(identity).to_dict()
                )
            ResultWriter().write_dict(result)
        except Exception as error:
            ErrorReporter.report(error)
        return None
