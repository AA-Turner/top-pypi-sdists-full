"""State the selected project's whole budget, or remove it."""

from __future__ import annotations

import click

from labqoat._generated.project_budget_limits import ProjectBudgetLimits
from labqoat.cli.commands.project.budget_lines import BudgetLines
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.strict_command import StrictCommand


class ProjectBudgetSetCommand(StrictCommand):
    """Replace every limit at once so the stated budget is exactly what the command names."""

    def __init__(self, name: str, stated: bool) -> None:
        """Declare the optional limits and what is already used for ``set``; ``clear`` takes none."""
        positive = click.FloatRange(min=0, min_open=True)
        params: list[click.Parameter] = [
            click.Option(["--money"], type=positive, help="USD for the whole project."),
            click.Option(["--rate"], type=positive, help="USD per hour."),
            click.Option(["--hours"], type=positive, help="Wall-clock hours the project may take."),
            click.Option(["--spent"], type=click.FloatRange(min=0), help="USD already spent before this budget."),
            click.Option(["--elapsed"], type=click.FloatRange(min=0), help="Hours already gone before this budget."),
        ]
        summary = (
            "State the selected project's budget. Every limit is optional; one you omit is removed. Money and "
            "time count from the first time a budget is stated; --spent and --elapsed restart the count now with "
            "that much already used (0 for a fresh budget). Budgets give hints and block nothing."
            if stated
            else "Remove the selected project's budget."
        )
        super().__init__(name, params=params if stated else [], help=summary)
        self._stated = stated

    def invoke(self, ctx: click.Context) -> object:
        """Send the named limits, refusing a ``set`` that names none."""
        limits = ProjectBudgetLimits(
            spend=ctx.params.get("money"),
            spend_per_hour=ctx.params.get("rate"),
            hours=ctx.params.get("hours"),
            already_spent=ctx.params.get("spent"),
            already_hours=ctx.params.get("elapsed"),
        )
        if self._stated and (limits.spend, limits.spend_per_hour, limits.hours) == (None, None, None):
            raise click.UsageError("Give --money, --rate or --hours, or remove the budget with `project budget clear`.")
        context = ContextAccessor.current()
        with context.client() as client:
            BudgetLines.write(client.projects.put_budget(context.project_name(), limits))
        return None
