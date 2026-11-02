"""The project command group: select, create, inspect, reorganize, archive and rank a piece of work."""

from __future__ import annotations

import click

from labqoat.cli.commands.project.project_archive_command import ProjectArchiveCommand
from labqoat.cli.commands.project.project_budget_set_command import ProjectBudgetSetCommand
from labqoat.cli.commands.project.project_budget_show_command import ProjectBudgetShowCommand
from labqoat.cli.commands.project.project_budget_watch_command import ProjectBudgetWatchCommand
from labqoat.cli.commands.project.project_current_command import ProjectCurrentCommand
from labqoat.cli.commands.project.project_delete_command import ProjectDeleteCommand
from labqoat.cli.commands.project.project_list_command import ProjectListCommand
from labqoat.cli.commands.project.project_move_command import ProjectMoveCommand
from labqoat.cli.commands.project.project_put_command import ProjectPutCommand
from labqoat.cli.commands.project.project_show_command import ProjectShowCommand
from labqoat.cli.core_command_catalog import CoreCommandCatalog
from labqoat.cli.memory_mutation_command import MemoryMutationCommand


class ProjectCommandCatalog:
    """Assemble the commands for the container that owns runs, datasets, dashboards and one memory."""

    @staticmethod
    def group() -> click.Group:
        """Build the complete project group without network or file access."""
        group = CoreCommandCatalog.group(
            "project",
            "Select and organize the project that owns the work. A project groups runs, datasets, dashboards and "
            "one memory under a name. Start with `project init NAME`; --project, LABQOAT_PROJECT or "
            "[tool.labqoat] project in pyproject.toml select it afterwards.",
        )
        group.add_command(ProjectPutCommand("init", pin=True))
        group.add_command(ProjectPutCommand("create", pin=False))
        group.add_command(ProjectCurrentCommand())
        group.add_command(ProjectListCommand())
        group.add_command(ProjectShowCommand())
        group.add_command(ProjectMoveCommand())
        group.add_command(ProjectArchiveCommand("archive", archived=True))
        group.add_command(ProjectArchiveCommand("unarchive", archived=False))
        group.add_command(ProjectDeleteCommand())
        group.add_command(ProjectCommandCatalog.objectives())
        group.add_command(ProjectCommandCatalog.budget())
        return group

    @staticmethod
    def budget() -> click.Group:
        """Optional money and time budgets that advise whoever works in the selected project."""
        group = CoreCommandCatalog.group(
            "budget",
            "State and follow the selected project's money and time budgets. A budget gives hints to spend more "
            "or less; it blocks nothing.",
        )
        group.add_command(ProjectBudgetShowCommand())
        group.add_command(ProjectBudgetSetCommand("set", stated=True))
        group.add_command(ProjectBudgetSetCommand("clear", stated=False))
        group.add_command(ProjectBudgetWatchCommand())
        return group

    @staticmethod
    def objectives() -> click.Group:
        """Ranking objectives that turn result properties into the selected project's derived frontier."""
        group = CoreCommandCatalog.group("objective", "Declare the metrics that rank the selected project's results.")
        metric = click.Option(["--metric"], required=True, help="Result properties.metric to rank.")
        group.add_command(
            MemoryMutationCommand(
                "set",
                "objective-set",
                [
                    metric,
                    click.Option(["--direction"], type=click.Choice(["max", "min"]), required=True),
                    click.Option(
                        ["--require"],
                        multiple=True,
                        help="KEY=VALUE that properties.setup must contain to rank; repeatable.",
                    ),
                ],
                "Add or replace one objective; other objectives are kept.",
                default_agent="lead",
            )
        )
        group.add_command(
            MemoryMutationCommand("remove", "objective-remove", [metric], "Remove one objective.", default_agent="lead")
        )
        return group
