"""Hints, printed beside a launch, about where the project stands against its budget."""

import threading
from typing import ClassVar

import click

from labqoat.cli.commands.project.budget_lines import BudgetLines
from labqoat.client import Client
from labqoat.errors.api_error import ApiError


class BudgetAdvice:
    """Remind whoever launches work of the budget; a launch never fails or waits because of it."""

    PATIENCE_SECONDS: ClassVar[float] = 1.0

    @staticmethod
    def announce(client: Client, project: str) -> threading.Thread:
        """Read the budget while the launch goes on and write its hints to stderr as soon as they arrive."""
        reading = threading.Thread(target=BudgetAdvice.hints, args=(client, project), daemon=True)
        reading.start()
        return reading

    @staticmethod
    def finish(reading: threading.Thread) -> None:
        """Give a reading still on its way a moment before the launch closes the client it uses."""
        reading.join(BudgetAdvice.PATIENCE_SECONDS)

    @staticmethod
    def hints(client: Client, project: str) -> None:
        """Write the budget's hints to stderr so machine-readable stdout stays a single receipt."""
        try:
            budget = client.projects.budget(project)
        except ApiError:
            return
        for line in BudgetLines.hints(budget):
            click.echo(f"hint {line}", err=True)
