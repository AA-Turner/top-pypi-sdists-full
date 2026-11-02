"""``compute hosts remove`` unenrolls a connected machine without stopping it."""

from __future__ import annotations

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.strict_command import StrictCommand


class HostRemoveCommand(StrictCommand):
    """Confirm, unenroll and explain that only Labqoat-owned containers are cleaned up."""

    NOTICE = (
        "Host {host} was unenrolled. The machine keeps running; Labqoat stops scheduling there and cleans up "
        "only the containers it owns."
    )

    def __init__(self) -> None:
        """Declare the host selector and noninteractive confirmation."""
        params: list[click.Parameter] = [click.Argument(["host_id"], type=str, required=True), ParameterFactory.yes()]
        super().__init__("remove", params=params, help="Unenroll a connected host; the machine keeps running.")

    def invoke(self, ctx: click.Context) -> object:
        """Confirm unless --yes, then unenroll and print the cleanup notice on stderr."""
        host = str(ctx.params["host_id"])
        if not ctx.params["yes"]:
            click.confirm(f"Unenroll host {host}? The machine keeps running.", abort=True)
        client = ContextAccessor.current().compute()
        try:
            ResultWriter().write_dict(client.unenroll_host(host))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        click.echo(self.NOTICE.format(host=host), err=True)
        return None
