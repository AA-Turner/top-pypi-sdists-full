"""Repeat the selected project's budget on an interval for an agent that works alongside it."""

from __future__ import annotations

import time

import click

from labqoat.cli.commands.project.budget_lines import BudgetLines
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.observation_deadline import ObservationDeadline
from labqoat.cli.strict_command import StrictCommand


class ProjectBudgetWatchCommand(StrictCommand):
    """Write the budget now and again every interval until interrupted or the timeout passes."""

    def __init__(self) -> None:
        """Declare the interval and the optional local timeout."""
        every = click.Option(
            ["--every"],
            type=str,
            default="15m",
            show_default=True,
            callback=ProjectBudgetWatchCommand.interval,
            help="Time between reports, such as 5m or 1h; at least one minute.",
        )
        super().__init__(
            "watch",
            params=[every, ObservationDeadline.option()],
            help="Report the selected project's budget and hints now and on an interval. Run it in the background "
            "while working and follow the latest hint. --json writes one document per report.",
        )

    @staticmethod
    def interval(_ctx: click.Context, _param: click.Parameter, value: str) -> float:
        """Parse the interval and keep it slow enough to be a reminder, not a poll."""
        seconds = ObservationDeadline.parse(value)
        if seconds is None or seconds < 60:
            raise click.BadParameter("Expected at least one minute, such as 5m or 1h.")
        return seconds

    def invoke(self, ctx: click.Context) -> object:
        """Report until the observer leaves; the budget itself is unaffected."""
        context = ContextAccessor.current()
        name = context.project_name()
        with context.client() as client, ObservationDeadline.current().watching():
            while True:
                BudgetLines.write(client.projects.budget(name))
                time.sleep(float(ctx.params["every"]))
