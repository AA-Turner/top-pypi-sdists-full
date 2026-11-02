"""Read the selected project's budget and the advice its spending earns."""

from __future__ import annotations

import click

from labqoat.cli.commands.project.budget_lines import BudgetLines
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.strict_command import StrictCommand


class ProjectBudgetShowCommand(StrictCommand):
    """Answer how much money and time is used and whether to spend more or less."""

    def __init__(self) -> None:
        """Declare a command without parameters."""
        super().__init__(
            "show",
            params=[],
            help="Show what the selected project spent against its budget, with hints to spend more or less. "
            "Each hint starts with more, steady, less or stop.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Read the budget once and write it."""
        context = ContextAccessor.current()
        with context.client() as client:
            BudgetLines.write(client.projects.budget(context.project_name()))
        return None
