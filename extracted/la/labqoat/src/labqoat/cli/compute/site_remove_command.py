"""``compute sites remove`` deletes an existing-machine site once its hosts are unenrolled."""

from __future__ import annotations

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.strict_command import StrictCommand


class SiteRemoveCommand(StrictCommand):
    """Confirm, then remove a site and its offering policy."""

    def __init__(self) -> None:
        """Declare the site selector and noninteractive confirmation."""
        params: list[click.Parameter] = [click.Argument(["site_id"], type=str, required=True), ParameterFactory.yes()]
        super().__init__("remove", params=params, help="Remove an existing-machine site with no enrolled hosts.")

    def invoke(self, ctx: click.Context) -> object:
        """Confirm unless --yes, remove the site and report the outcome on stderr."""
        site = str(ctx.params["site_id"])
        if not ctx.params["yes"]:
            click.confirm(f"Remove site {site}?", abort=True)
        client = ContextAccessor.current().compute()
        try:
            client.remove_site(site)
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        click.echo(f"Site {site} was removed.", err=True)
        return None
