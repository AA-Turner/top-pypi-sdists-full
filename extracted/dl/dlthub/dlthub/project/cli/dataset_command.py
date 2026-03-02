import argparse


import dlt
from dlt.common.utils import uniq_id
from dlt._workspace.cli import SupportsCliCommand, echo as fmt
from dlt._workspace.cli._pipeline_command import pipeline_command

from dlthub.common.cli import add_project_opts
from dlthub.destinations.dataset import WritableDataset

from dlthub.project.entity_factory import EntityFactory
from dlthub.project.project_context import ProjectRunContext
from dlthub.project.cli.helpers import project_from_args_with_cli_output
from dlthub.project.cli.formatters import print_entity_list


class DatasetCommand(SupportsCliCommand):
    # TODO: move to OSS at least partially
    command = "dataset"
    help_string = "Manage dlthub project datasets"
    description = """
Commands to manage datasets for project.
Run without arguments to list all datasets in current project.
"""

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        # add opts to switch project / profile
        add_project_opts(parser)

        parser.add_argument("dataset_name", metavar="dataset-name", help="Dataset name", nargs="?")
        parser.add_argument("--destination", help="Destination name, if many allowed", default=None)
        parser.add_argument(
            "--schema",
            help="Limits to schema with name for multi-schema datasets",
            default=None,
        )

        subparsers = parser.add_subparsers(
            title="Available subcommands", dest="operation", required=False
        )

        subparsers.add_parser("list", help="List Datasets")
        subparsers.add_parser("info", help="Dataset info")
        subparsers.add_parser("drop", help="Drops the dataset and all data in it")

        subparsers.add_parser("show", help="Shows the content of dataset in Streamlit")
        subparsers.add_parser(
            "row-counts", help="Display the row counts of all tables in the dataset"
        )

        # peak into a table
        head_parser = subparsers.add_parser(
            "head", help="Display the first x rows of a table, defaults to 5"
        )
        head_parser.add_argument("table_name", help="Table name")
        head_parser.add_argument("--limit", type=int, default=5, help="Number of rows to display")

        # subparsers.add_parser("schemas", help="Lists all schemas in dataset")
        # subparsers.add_parser("schema", help="Reads, syncs or drops schema in a dataset")
        # subparsers.add_parser("tables", help="Lists all tables in dataset in selected schemas")
        # subparsers.add_parser("table", help="Reads, writes a table in a dataset")
        # subparsers.add_parser(
        #     "pipelines", help="Lists all pipelines known to be writing to dataset"
        # )
        # subparsers.add_parser("read", help="Reads a table from dataset and saves to parquet/json")
        # subparsers.add_parser("write", help="Writes to a table from file")

    def execute(self, args: argparse.Namespace) -> None:
        run_context = project_from_args_with_cli_output(args)
        entities = EntityFactory(run_context.project)

        # TODO: also find ad hoc datasets ie. present in pipelines
        all_datasets = list(entities.project_config.datasets.keys())

        # TODO: list implicit datasets
        if args.operation == "list":
            print_entity_list(
                "dataset",
                all_datasets,
                note=(
                    "NOTE: You can also run dataset commands on datasets "
                    + "implicitly defined in pipelines."
                ),
            )
            return

        if not args.dataset_name:
            self.parser.print_usage()
            return

        # TODO: move . notation to entity manager
        dataset_name = all_datasets[0] if args.dataset_name == "." else args.dataset_name
        # dataset does not reach to destination when created
        dataset = entities.get_dataset(
            dataset_name, destination_name=args.destination, schema=args.schema
        )

        if args.operation == "drop":
            drop_dataset(dataset, dataset_name)

        elif args.operation == "info":
            show_dataset_info(run_context, dataset, dataset_name)

        elif args.operation == "show":
            show_dataset(dataset, dataset_name)

        elif args.operation == "row-counts":
            show_dataset_row_counts(dataset, dataset_name)

        elif args.operation == "head":
            show_dataset_head(dataset, args.table_name, args.limit)

        else:
            self.parser.print_usage()


def drop_dataset(dataset: WritableDataset, dataset_name: str) -> None:
    dataset_location = (
        f"{dataset._destination.destination_name}"
        + f"[{str(dataset._destination.configuration(None, accept_partial=True))}]"
    )
    fmt.echo("Do you want to drop the dataset %s" % fmt.bold(dataset_name), nl=False)
    fmt.echo(" on destination %s?" % fmt.bold(dataset_location))
    fmt.secho("All data in the dataset will be irreversibly deleted!", bold=True)
    if fmt.confirm("Proceed?") is True:
        with dataset.destination_client as client:
            if not client.is_storage_initialized():
                fmt.warning("Storage not initialized. Dataset does not yet exist.")
            else:
                client.drop_storage()
                fmt.echo("Dropped")


def show_dataset_info(
    run_context: ProjectRunContext, dataset: WritableDataset, dataset_name: str
) -> None:
    fmt.echo("Dataset %s" % fmt.bold(dataset_name), nl=False)
    fmt.echo(" is available on the following destinations:")
    factory = EntityFactory(run_context.project)
    available_destinations = factory._resolve_dataset_destinations(dataset_name)
    fmt.echo("- " + "\n- ".join(available_destinations))
    fmt.echo("Connecting to destination: %s" % fmt.bold(dataset._destination.destination_name))
    if dataset.schema.is_new:
        fmt.echo("No tables found for contract: %s " % fmt.bold(dataset.schema.name))
        fmt.warning("Dataset is not yet created or new contract is being added.")
    else:
        fmt.echo("Found contract: %s " % fmt.bold(dataset.schema.name), nl=False)
        fmt.echo(" with %s tables." % fmt.bold(str(len(dataset.schema.data_table_names()))))
        fmt.echo("- " + "\n- ".join(dataset.schema.data_table_names()))


def show_dataset(dataset: WritableDataset, dataset_name: str) -> None:
    pipeline_name = f"{dataset_name}_pipeline_{uniq_id(4)}"
    pipeline = dlt.pipeline(
        pipeline_name, destination=dataset._destination, dataset_name=dataset_name
    )
    try:
        pipeline._inject_schema(dataset.schema)
        pipeline_command("show", pipeline.pipeline_name, pipeline.pipelines_dir, 0)
    finally:
        pipeline._wipe_working_folder()


def show_dataset_row_counts(dataset: WritableDataset, dataset_name: str) -> None:
    fmt.echo("Loading row counts for dataset %s." % fmt.bold(dataset_name))
    fmt.echo("Depending on your destination type and table size, this may take a while...")
    fmt.echo(dataset.row_counts(dlt_tables=True).df())


def show_dataset_head(dataset: WritableDataset, table_name: str, limit: int) -> None:
    fmt.echo("Loading first %s rows of table %s." % (limit, table_name))
    fmt.echo(dataset[table_name].head(limit=limit).df())
