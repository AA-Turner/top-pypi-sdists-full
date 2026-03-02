import argparse

from dlt._workspace.cli import SupportsCliCommand, echo as fmt

from dlthub.common.cli import add_project_opts

from dlthub.project.cli.helpers import project_from_args_with_cli_output
from dlthub.project.cli.write_state import ProjectWriteState

from ..project_context import (
    ProjectRunContext,
)

from .helpers import add_destination, get_available_destinations
from .formatters import print_entity_list


class DestinationCommand(SupportsCliCommand):
    command = "destination"
    help_string = "Manage project destinations"
    description = """
Commands to manage destinations for project.
Run without arguments to list all destinations in current project.
"""

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        add_project_opts(parser)

        parser.add_argument("destination_name", help="Name of the destination", nargs="?")

        subparsers = parser.add_subparsers(
            title="Available subcommands", dest="destination_command", required=False
        )

        subparsers.add_parser(
            "list",
            help="List all destinations in the project.",
            description="List all destinations in the project.",
        )

        subparsers.add_parser(
            "list-available",
            help="List all destination types that can be added to the project.",
            description="List all destination types that can be added to the project.",
        )

        # add a new destination
        add_parser = subparsers.add_parser(
            "add",
            help="Add a new destination to the project",
            description="Add a new destination to the project",
        )
        add_parser.add_argument(
            "destination_type",
            help="Will default to the destination name if not specified.",
            nargs="?",
        )
        add_parser.add_argument(
            "--dataset-name",
            help=(
                "Name of the dataset to add in the datasets section. "
                + "Will add no dataset if not specified."
            ),
            default=None,
        )

    def execute(self, args: argparse.Namespace) -> None:
        if args.destination_command == "list-available":
            list_available_destinations()
            return

        project_run_context = project_from_args_with_cli_output(args)

        if args.destination_command == "list":
            print_entity_list(
                "destination",
                [
                    f"{name}: {config.get('type')}"
                    for name, config in project_run_context.project.destinations.items()
                ],
            )
        elif args.destination_command == "add":
            add_project_destination(
                project_run_context, args.destination_name, args.destination_type, args.dataset_name
            )
        else:
            self.parser.print_usage()


def add_project_destination(
    project_run_context: ProjectRunContext,
    destination_name: str,
    destination_type: str,
    dataset_name: str,
) -> None:
    destination_type = destination_type or destination_name
    fmt.echo(
        f"Will add destination {destination_name} to the project with type {destination_type}."
    )
    if not fmt.confirm("Do you want to proceed?", default=True):
        exit(0)
    state = ProjectWriteState.from_run_context(project_run_context)
    add_destination(state, destination_name, destination_type, dataset_name)
    state.commit()
    fmt.echo(f"Destination {destination_name} added.")


def list_available_destinations() -> None:
    fmt.echo("Available destination types for adding to a project:")
    for destination in get_available_destinations():
        fmt.echo(f" * {destination}")
    fmt.note(
        "To add a destination to your project, use the "
        + "`dlt destination <destination_type> add` command."
    )
