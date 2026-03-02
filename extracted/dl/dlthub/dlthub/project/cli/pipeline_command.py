from typing import List

import argparse

import dlt

from dlt._workspace.cli import echo as fmt, DEFAULT_VERIFIED_SOURCES_REPO
from dlt._workspace.cli.commands import PipelineCommand


from dlthub.common.cli import add_project_opts, get_existing_subparser
from dlthub.project.pipeline_manager import PipelineManager
from dlthub.project.project_context import ProjectRunContext
from dlthub.project.cli.helpers import (
    project_from_args_with_cli_output,
    init_pipeline,
    add_pipeline,
    ensure_unique_names,
)
from dlthub.project.cli.write_state import ProjectWriteState
from dlthub.project.cli.formatters import print_entity_list


class ProjectPipelineCommand(PipelineCommand):
    description = """
The `dlt pipeline` command provides a set of commands to inspect the pipeline working directory,
tables, and data in the destination and check for problems encountered during data loading.

Run without arguments to list all pipelines in the current project.
    """

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        # add opts to switch project / profile
        add_project_opts(parser)
        super().configure_parser(parser)

        subparsers = get_existing_subparser(parser)

        # NOTE: the pipeline parser interface should be changed to
        # dlt pipeline run <pipeline_name> in the core lib

        subparsers.add_parser(
            "list",
            help="List all pipelines in the project.",
            description="List all pipelines in the project.",
        )

        add_parser = subparsers.add_parser(
            "add",
            help="Add a new pipeline to the current project",
            description="""
Adds a new pipeline to the current project. Will not create any sources
or destinations, you can reference other entities by name.
""",
        )

        add_parser.add_argument("source_name", help="Name of the source to add")
        add_parser.add_argument("destination_name", help="Name of the destination to add")
        add_parser.add_argument("--dataset-name", help="Name of the dataset to add", default=None)

        run_parser = subparsers.add_parser("run", help="Run a pipeline")
        run_parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Limits the number of extracted pages for all resources. See source.add_limit.",
        )
        run_parser.add_argument(
            "--resources",
            type=lambda s: [item.strip() for item in s.split(",")],
            help="Comma-separated list of resource names.",
        )

        init_parser = subparsers.add_parser(
            "init",
            help="Initialize a pipeline in the current working directory",
            description="""
Initializes a pipeline from a new source to a new destination,
registering all entities in the project.

Example:
dlt pipeline my_pokepipeline init pokemon duckdb --dataset-name my_pokeset
""",
        )
        init_parser.add_argument(
            "source_name", help="Name of the source to add", nargs="?", default=None
        )
        init_parser.add_argument(
            "destination_name", help="Name of the destination to add", nargs="?", default=None
        )
        init_parser.add_argument("--dataset-name", help="Name of the dataset to add", default=None)
        init_parser.add_argument(
            "--location",
            default=DEFAULT_VERIFIED_SOURCES_REPO,
            help="Advanced. Uses a specific url or local path to verified sources repository.",
        )
        init_parser.add_argument(
            "--branch",
            default=None,
            help=(
                "Advanced. Uses specific branch of the verified sources repository to fetch the"
                " template."
            ),
        )
        init_parser.add_argument(
            "--eject_source",
            default=False,
            action="store_true",
            help=(
                "Ejects the source code of the core sources (e.g. sql_database) so they will be "
                "editable by you."
            ),
        )
        init_parser.add_argument(
            "--add-pipeline-script",
            action="store_true",
            help="Create an example pipeline script from source to destination.",
        )

    def execute(self, args: argparse.Namespace) -> None:
        if args.operation in ("add", "run", "init"):
            run_context = project_from_args_with_cli_output(args)
            # must have project context
            if args.operation == "add":
                add_project_pipeline(
                    run_context,
                    args.pipeline_name,
                    args.source_name,
                    args.destination_name,
                    args.dataset_name,
                )
            elif args.operation == "run":
                run_pipeline(run_context, args.pipeline_name, args.limit, args.resources)
            elif args.operation == "init":
                init_project_pipeline(
                    run_context,
                    args.source_name,
                    args.destination_name,
                    args.pipeline_name,
                    args.dataset_name,
                    args.location,
                    args.branch,
                    args.eject_source,
                    args.add_pipeline_script,
                )

        # optional project context
        elif args.list_pipelines or args.operation == "list":
            run_context = project_from_args_with_cli_output(args, allow_no_project=True)
            if args.operation == "list" or args.list_pipelines:
                # NOTE: by default list pipelines in project if no operation is specified
                # we could change this in the core
                if run_context:
                    list_pipelines(run_context)
                else:
                    try:
                        super().execute(args)
                    except Exception:
                        fmt.echo(
                            "No pipeline dirs found in %s" % dlt.current.run_context().data_dir
                        )
        # no project context required
        else:
            # execute regular pipeline command without project context
            super().execute(args)


def list_pipelines(run_context: ProjectRunContext) -> None:
    print_entity_list(
        "pipeline",
        [
            f"{name}: {config.get('source')} to {config.get('destination')}"
            for name, config in run_context.project.pipelines.items()
        ],
    )


def init_project_pipeline(
    run_context: ProjectRunContext,
    source_name: str,
    destination_name: str,
    pipeline_name: str,
    dataset_name: str = None,
    location: str = None,
    branch: str = None,
    eject: bool = False,
    add_pipeline_script: bool = False,
) -> None:
    """
    Imports source-files for source, write example script how to move data from source to
    destination, creates creates secrets and configs, register all entities (source, destination,
    dataset, pipeline in the dlt.yml
    """
    state = ProjectWriteState.from_run_context(run_context)
    ensure_unique_names(state, source_name, destination_name, pipeline_name, dataset_name)
    fmt.echo(
        "Will add a complete pipeline with source, destination, dataset to your dlthub project."
    )
    if not fmt.confirm("Do you want to proceed?", default=True):
        exit(0)
    added_source, added_destination, _, added_dataset = init_pipeline(
        state,
        source_name,
        destination_name,
        pipeline_name,
        dataset_name,
        location,
        branch,
        eject,
        add_pipeline_script,
    )
    state.commit()
    fmt.echo(
        f"Pipeline `{pipeline_name} from {added_source} to {added_destination} with dataset "
        f"{added_dataset} added."
    )
    fmt.echo(f"To run the pipeline, use the command: `dlt pipeline {pipeline_name} run`")


def add_project_pipeline(
    run_context: ProjectRunContext,
    pipeline_name: str,
    source_name: str,
    destination_name: str,
    dataset_name: str = None,
) -> None:
    # TODO: we could autocreate source and destination if not present and a certain flag
    # is set, not sure..
    fmt.echo("Will add a new pipeline to your dlthub project.")
    if source_name not in run_context.project.sources.keys():
        fmt.warning(
            "Source %s does not exist in project, your pipeline will "
            "reference a non-existing source." % source_name
        )
    if destination_name not in run_context.project.destinations.keys():
        fmt.warning(
            "Destination %s does not exist in project, your pipeline will "
            "reference a non-existing destination." % destination_name
        )
    if not fmt.confirm("Do you want to proceed?", default=True):
        exit(0)
    state = ProjectWriteState.from_run_context(run_context)
    add_pipeline(state, pipeline_name, source_name, destination_name, dataset_name)
    state.commit()
    fmt.echo(f"Pipeline {pipeline_name} added.")


def run_pipeline(
    run_context: ProjectRunContext, pipeline_name: str, limit: int, resources: List[str]
) -> None:
    # TODO: display pre-run info: does the pipeline exist? does it have pending data
    # (we skip extract otherwise)
    # are we changing destination or dataset? do we drop any data if so ask for permission.
    # TODO: now we support explicit config so ad hoc pipelines can be run
    #   we just need to take source_ref, destination ref and dataset name and pass it

    pipeline_manager = PipelineManager(run_context.project)
    load_info = pipeline_manager.run_pipeline(pipeline_name, limit=limit, resources=resources)
    fmt.echo(load_info)
