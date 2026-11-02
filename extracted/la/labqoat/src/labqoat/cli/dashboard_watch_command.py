"""Follow a dashboard's leader and frontier changes from the terminal."""

from __future__ import annotations

from contextlib import closing

import click

from labqoat._generated.dashboard_change import DashboardChange
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.dashboard_change_line import DashboardChangeLine
from labqoat.cli.observation_deadline import ObservationDeadline
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.json_writer import JsonWriter
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.strict_command import StrictCommand


class DashboardWatchCommand(StrictCommand):
    """Print each new leader and frontier move as it is recorded, until interrupted or timed out."""

    def __init__(self) -> None:
        """Select the dashboard, optionally some of its watched panels and a position to resume from."""
        super().__init__(
            "watch",
            params=[
                ParameterFactory.argument("dashboard_ref"),
                DashboardWatchCommand.panel_option(),
                click.Option(["--cursor"], help="Replay the changes recorded after this change's cursor first."),
                ObservationDeadline.option(),
            ],
            help="Follow new leaders and frontier moves; JSON modes print one change per line.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Stream changes in the invocation's output mode and always release the connection."""
        context = ContextAccessor.current()
        client = context.dashboards()
        reference = str(ctx.params["dashboard_ref"])
        try:
            with (
                ObservationDeadline.current(reference).watching(),
                closing(client.watch(reference, ctx.params["panel"], ctx.params["cursor"])) as changes,
            ):
                for change in changes:
                    DashboardWatchCommand.write(change, context.output_mode == "human")
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def panel_option() -> click.Option:
        """Narrow to watched panels; the service takes the chosen ids as one comma-separated value."""
        return click.Option(
            ["--panel"],
            multiple=True,
            callback=DashboardWatchCommand.chosen,
            help="Only this ranked table or frontier scatter; repeat for several.",
        )

    @staticmethod
    def chosen(_ctx: click.Context, _param: click.Parameter, value: tuple[str, ...]) -> str | None:
        """Join the repeated option, leaving every watched panel selected when it is absent."""
        return ",".join(value) or None

    @staticmethod
    def write(change: DashboardChange, human: bool) -> None:
        """Print a readable line for people and one compact JSON document per change for programs."""
        if human:
            click.echo(DashboardChangeLine.text(change))
        else:
            JsonWriter(pretty=False).write(change.to_dict())
