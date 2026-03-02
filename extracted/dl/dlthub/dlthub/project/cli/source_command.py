import argparse
import importlib

from dlt._workspace.cli import SupportsCliCommand, echo as fmt, DEFAULT_VERIFIED_SOURCES_REPO
from dlt._workspace.cli._init_command import (
    _list_core_sources,
    _list_verified_sources,
)

from dlthub.common.cli import add_project_opts
from dlthub.project.project_context import ProjectRunContext
from dlthub.project.cli.write_state import ProjectWriteState
from dlthub.project.cli.helpers import (
    project_from_args_with_cli_output,
    add_source,
    get_available_source_templates,
)
from dlthub.project.cli.formatters import print_entity_list


class SourceCommand(SupportsCliCommand):
    command = "source"
    help_string = "Manage dlthub project sources"
    description = """
Commands to manage sources for project.
Run without arguments to list all sources in current project.
"""

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser

        add_project_opts(parser)

        parser.add_argument("source_name", help="Name of the source to add.", nargs="?")

        subparsers = parser.add_subparsers(title="Available subcommands", dest="source_command")

        subparsers.add_parser(
            "check",
            help="(temporary feature) Checks if the source is importable, only works for "
            + "sources within the sources folder.",
            description="(temporary feature) Checks if the source is importable, only works for "
            + "sources within the sources folder.",
        )

        subparsers.add_parser(
            "list",
            help="List all sources in the project.",
            description="""
List all sources in the project context.
""",
        )

        subparsers.add_parser(
            "list-available",
            help="List all source types that can be added to the project.",
            description="List all source types that can be added to the project.",
        )

        add_parser = subparsers.add_parser(
            "add",
            help="Add a new source to the project.",
            description="""
Add a new source to the project context.

* If source type is not specified, the source type will be the same as the source name.
* If a give source_type is not found, a default source template will be used.
""",
        )
        add_parser.add_argument(
            "source_type",
            help="Type of the source to add. If not specified, "
            "the source type will be the same as the source name.",
            nargs="?",
        )
        add_parser.add_argument(
            "--location",
            default=DEFAULT_VERIFIED_SOURCES_REPO,
            help="Advanced. Uses a specific url or local path to verified sources repository.",
        )
        add_parser.add_argument(
            "--branch",
            default=None,
            help=(
                "Advanced. Uses specific branch of the verified sources repository to fetch the"
                " template."
            ),
        )
        add_parser.add_argument(
            "--eject-source",
            default=False,
            action="store_true",
            help=(
                "Ejects the source code of the core source like sql_database or rest_api so they"
                " will be editable by you."
            ),
        )
        add_parser.add_argument(
            "--add-pipeline-script",
            action="store_true",
            help="Create an example pipeline script for the source.",
        )

    def execute(self, args: argparse.Namespace) -> None:
        if args.source_command == "list-available":
            list_available_sources()
            return

        project_run_context = project_from_args_with_cli_output(args)

        if args.source_command == "add":
            add_project_source(
                project_run_context,
                args.source_name,
                args.source_type,
                args.location,
                args.branch,
                args.eject_source,
                args.add_pipeline_script,
            )
        elif args.source_command == "list":
            print_entity_list(
                "source",
                [
                    f"{name}: {config.get('type')}"
                    for name, config in project_run_context.project.sources.items()
                ],
            )
        elif args.source_command == "check":
            check_project_source(project_run_context, args.source_name)
        else:
            self.parser.print_usage()


def add_project_source(
    project_run_context: ProjectRunContext,
    source_name: str,
    source_type: str,
    location: str = DEFAULT_VERIFIED_SOURCES_REPO,
    branch: str = None,
    eject_source: bool = True,
    add_pipeline_script: bool = False,
) -> None:
    fmt.echo("Will add a new source to your dlthub project.")
    if not fmt.confirm("Do you want to proceed?", default=True):
        exit(0)
    project_state = ProjectWriteState.from_run_context(project_run_context)
    with fmt.always_choose(always_choose_default=True, always_choose_value="Y"):
        add_source(
            project_state,
            source_name,
            source_type,
            location=location,
            branch=branch,
            eject_source=eject_source,
            add_example_pipeline_script=add_pipeline_script,
        )
    project_state.commit()
    fmt.echo("Done.")


def check_project_source(project_run_context: ProjectRunContext, source_name: str) -> None:
    fmt.echo(f"Checking if source {source_name} is importable...")
    source_type = project_run_context.project.sources.get(source_name, {}).get("type")
    if not source_type:
        fmt.error(f"Source {source_name} is not found in the project or has no type defined.")
        exit(1)

    # split source_type
    source_type_parts = source_type.split(".")
    if len(source_type_parts) <= 2:
        fmt.error(
            f"Source type {source_type} is not valid. Must be a valid "
            + "python module path in the sources module."
        )
        exit(1)

    source_module_path = ".".join(source_type_parts[:-1])
    importlib.import_module(source_module_path)

    fmt.note(f"Source file at {source_module_path} could be imported successfully.")


def list_available_sources() -> None:
    fmt.echo("Available core source types for adding to a project:")
    for source_name, source_config in _list_core_sources().items():
        fmt.echo(f" * {source_name}: {source_config.doc}")
    fmt.echo("")
    fmt.echo("Available verified source types for adding to a project:")
    for source_name, source_config in _list_verified_sources(
        repo_location=DEFAULT_VERIFIED_SOURCES_REPO
    ).items():
        fmt.echo(f" * {source_name}: {source_config.doc}")
    fmt.echo("")
    fmt.echo("Available source templates for adding to a project:")
    for template_name, description in get_available_source_templates().items():
        fmt.echo(f" * {template_name}: {description}")
    fmt.note(
        "To add a source or source template to your project, use the "
        + "`dlt source <source_type> add` command."
    )
