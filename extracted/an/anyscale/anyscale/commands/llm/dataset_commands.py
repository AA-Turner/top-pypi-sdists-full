import os
from typing import Optional

import click
from dateutil import tz
from rich import print as rprint
import tabulate

import anyscale
from anyscale.commands import command_examples
from anyscale.commands.util import AnyscaleCommand


@click.group("dataset", help="Dataset files stored on your Anyscale cloud.")
def dataset_cli():
    pass


@dataset_cli.command(
    name="get",
    short_help="Retrieves metadata about a dataset.",
    cls=AnyscaleCommand,
    is_alpha=True,
    example=command_examples.LLM_DATASET_GET_EXAMPLE,
)
@click.argument(
    "name", required=True,
)
@click.option(
    "--version",
    "-v",
    required=False,
    type=int,
    help="Version of the dataset. "
    "If a negative integer is provided, the dataset returned is this many versions back of the latest version. "
    "Default: Latest version.",
)
@click.option(
    "--project",
    required=False,
    help="Name of the Anyscale project that the dataset belongs to. "
    "If not provided, all projects will be searched.",
)
def get_dataset(
    name: str, version: Optional[int], project: Optional[str],
):
    """
    Retrieves metadata about a dataset.

    NAME = Name of the dataset

    Example usage:

        anyscale llm dataset get my_first_dataset

    Retrieve the second latest version of the dataset:

        anyscale llm dataset get my_first_dataset -v -1
    """
    dataset = anyscale.llm.dataset.get(name, version, project)
    rprint(dataset)


@dataset_cli.command(
    name="upload",
    short_help="Upload a dataset to your Anyscale cloud.",
    cls=AnyscaleCommand,
    is_alpha=True,
    example=command_examples.LLM_DATASET_UPLOAD_EXAMPLE,
)
@click.argument("dataset_file", required=True)
@click.option(
    "--name",
    "-n",
    required=True,
    help="Name of a new dataset, or an existing dataset, to upload a new version of.",
)
@click.option(
    "--description", required=False, help="Description of the dataset version.",
)
@click.option(
    "--cloud",
    required=False,
    help="Name of the Anyscale cloud to upload a new dataset to. "
    "If not provided, the default cloud will be used.",
)
@click.option(
    "--project",
    required=False,
    help="Name of the Anyscale project to upload a new dataset to. "
    "If not provided, the default project of the cloud will be used.",
)
def upload_dataset(
    dataset_file: str,
    name: str,
    description: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
):
    """
    Uploads a dataset, or a new version of a dataset, to your Anyscale cloud.

    DATASET_FILE = Path to the dataset file to upload

    Example usage:

        anyscale llm dataset upload path/to/my_dataset.jsonl -n my_first_dataset

        anyscale llm dataset upload my_dataset.jsonl -n second_dataset.jsonl

        anyscale llm dataset upload my_dataset2.jsonl -n second_dataset.jsonl --description 'added 3 lines'

    \b
    NOTE:
    If you are uploading a new version, have run this from within an Anyscale workspace,
    and neither `--cloud` nor `--project` is provided, the cloud and project of the workspace will be used.
    """
    dataset = anyscale.llm.dataset.upload(
        dataset_file, name, description=description, cloud=cloud, project=project,
    )
    rprint(dataset)


@dataset_cli.command(
    name="download",
    short_help="Download a dataset.",
    cls=AnyscaleCommand,
    is_alpha=True,
    example=command_examples.LLM_DATASET_DOWNLOAD_EXAMPLE,
)
@click.argument(
    "name", required=True,
)
@click.option(
    "--version",
    "-v",
    required=False,
    type=int,
    help="Version of the dataset to download. "
    "If a negative integer is provided, the dataset returned is this many versions back of the latest version. "
    "Default: Latest version.",
)
@click.option(
    "--project",
    required=False,
    help="Name of the Anyscale project to download the dataset from. "
    "If not provided, all projects will be searched.",
)
@click.option(
    "--output",
    "-o",
    required=False,
    help="Path to save the downloaded dataset to."
    "If not provided, the dataset contents will be printed to the terminal.",
)
def download_dataset(
    name: str, version: Optional[int], project: Optional[str], output: Optional[str],
):
    """
    Downloads a dataset from your Anyscale cloud.

    NAME = Name of the dataset to download

    Prints the dataset contents to the terminal by default.

    Example usage:

        anyscale llm dataset download my_first_dataset.jsonl

    Save the dataset to a file:

        anyscale llm dataset download my_dataset.jsonl -o ~/Downloads/my_dataset.jsonl

    Retrieve the second latest version of the dataset:

        anyscale llm dataset download my_dataset.jsonl -v -1
    """
    if output:
        output = os.path.expanduser(output)
        if os.path.exists(output):
            raise click.ClickException(f"File already exists at '{output}'")
    downloaded_contents = anyscale.llm.dataset.download(name, version, project)
    if output:
        # Create the parent directory if it doesn't exist
        parent_dir = os.path.dirname(output)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(output, "wb") as output_file:
            output_file.write(downloaded_contents)
        rprint(f"Dataset '{name}' downloaded to '{output}'")
        return
    print(downloaded_contents.decode())


@dataset_cli.command(
    name="list",
    short_help="List datasets.",
    cls=AnyscaleCommand,
    is_alpha=True,
    example=command_examples.LLM_DATASET_LIST_EXAMPLE,
)
@click.option(
    "--limit",
    "-l",
    required=False,
    default=10,
    type=int,
    help="Maximum number of datasets to return. Default: 10.",
)
@click.option(
    "--after",
    required=False,
    help="ID of the dataset to start the listing from. If provided, the list will start from the dataset after this ID.",
)
@click.option(
    "--name-contains",
    "-n",
    required=False,
    help="Filter datasets by name. If provided, only datasets with name containing this string will be returned.",
)
@click.option(
    "--cloud",
    required=False,
    help="Name of the Anyscale cloud to search in. If not provided, all clouds will be searched.",
)
@click.option(
    "--project",
    required=False,
    help="Name of the Anyscale project to search in. If not provided, all projects will be searched.",
)
def list_datasets(
    limit: int,
    after: Optional[str],
    name_contains: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
):
    """
    Lists datasets.

    Example usage:

        anyscale llm dataset list

    List datasets in a specific project:

        anyscale llm dataset list --project my_project
    """
    datasets = anyscale.llm.dataset.list(
        limit=limit,
        after=after,
        name_contains=name_contains,
        cloud=cloud,
        project=project,
    )
    table = tabulate.tabulate(
        [
            (
                d.id,
                d.name,
                d.description,
                d.created_at.astimezone(tz=tz.tzlocal()).strftime("%m/%d/%Y %I:%M %p"),
                d.num_versions,
            )
            for d in datasets
        ],
        headers=["ID", "Name", "Description", "Created At", "Num Versions"],
    )
    rprint(table)
