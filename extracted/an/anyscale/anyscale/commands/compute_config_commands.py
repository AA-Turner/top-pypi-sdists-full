from io import StringIO
from typing import IO, Optional, Tuple

import click
import yaml

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.util import AnyscaleCommand, LegacyAnyscaleCommand
from anyscale.compute_config import ComputeConfig
from anyscale.controllers.compute_config_controller import ComputeConfigController
from anyscale.util import validate_non_negative_arg


logger = BlockLogger()


def _validate_name_and_id_args(
    *, positional_name: Optional[str], flag_name: Optional[str], id_flag: Optional[str]
) -> Tuple[Optional[str], Optional[str]]:
    """Handles validation and deduplication for the name & ID options.

    The positional name is deprecated and will be removed in the near future.

    Returns (name, ID) -- exactly one of them will be populated.
    """
    if flag_name and positional_name:
        raise click.ClickException(
            "Both -n/--name and [COMPUTE_CONFIG_NAME] were provided. "
            "Use -n/--name only (the positional argument is deprecated)."
        )
    elif positional_name:
        logger.warning(
            "The [COMPUTE_CONFIG_NAME] positional argument is deprecated. "
            "Use the -n/--name flag instead."
        )
        name = positional_name
    elif flag_name:
        name = flag_name
    else:
        name = None

    if name and id_flag:
        raise click.ClickException("Only one of name or ID can be provided.")

    if not name and not id_flag:
        raise click.ClickException(
            "Either -n/--name or --id/--compute-config-id must be provided."
        )

    return name, id_flag


@click.group(
    "compute-config", help="Manage compute configurations.",
)
def compute_config_cli() -> None:
    pass


@compute_config_cli.command(
    name="create",
    help=(
        "Create a new version of a compute config from a YAML file.\n\n"
        "(1) To use the **new schema** defined at "
        "https://docs.anyscale.com/reference/compute-config-api#computeconfig, "
        "use the -f/--config-file flag:\n\n"
        "`anyscale compute-config create -f new_schema_config.yaml`\n\n"
        "(2) To use the **old schema** defined at "
        "https://docs.anyscale.com/reference/compute-config-api/#createclustercomputeconfig-legacy, "
        "use the positional argument:\n\n"
        "`anyscale compute-config create old_schema_config.yaml`\n\n"
    ),
    cls=AnyscaleCommand,
    example=command_examples.COMPUTE_CONFIG_CREATE_EXAMPLE,
)
@click.argument("compute-config-file", type=click.File("rb"), required=False)
@click.option(
    "-n",
    "--name",
    help="Name for the created compute config. This should *not* include a version tag. If a name is not provided, an anonymous compute config is generated. Anonymous compute configs are not accessible in the UI and can only be referenced by their ID.",
    required=False,
    default=None,
    type=str,
)
@click.option(
    "-f",
    "--config-file",
    required=False,
    default=None,
    type=str,
    help="Path to a YAML config file defining the compute config. Schema: https://docs.anyscale.com/reference/compute-config-api#computeconfig.",
)
def create_compute_config(
    compute_config_file: Optional[IO[bytes]],
    config_file: Optional[str],
    name: Optional[str],
):
    if compute_config_file and config_file:
        raise click.ClickException(
            "Only one of the --config-file flag or [COMPUTE_CONFIG_FILE] argument can be provided."
        )

    if compute_config_file is not None:
        ComputeConfigController().create(compute_config_file, name)
    elif config_file is not None:
        config = ComputeConfig.from_yaml(config_file)
        anyscale.compute_config.create(config, name=name)
    else:
        raise click.ClickException(
            "Either the --config-file flag or [COMPUTE_CONFIG_FILE] argument must be provided."
        )


@compute_config_cli.command(
    name="archive",
    help=("Archive all versions of a specified compute config.\n\n"),
    cls=AnyscaleCommand,
    example=command_examples.COMPUTE_CONFIG_ARCHIVE_EXAMPLE,
)
@click.argument("compute-config-name", type=str, required=False)
@click.option(
    "-n",
    "--name",
    help="Name of the compute config to archive.",
    required=False,
    type=str,
)
@click.option(
    "--compute-config-id",
    "--id",
    help="ID of the compute config to archive. Alternative to name.",
    required=False,
    type=str,
)
def archive_compute_config(
    compute_config_name: Optional[str],
    name: Optional[str],
    compute_config_id: Optional[str],
) -> None:
    name, cc_id = _validate_name_and_id_args(
        positional_name=compute_config_name, flag_name=name, id_flag=compute_config_id
    )
    anyscale.compute_config.archive(name=name, _id=cc_id)


@compute_config_cli.command(
    name="list",
    help=(
        "List information about compute configs.\n\n"
        "By default, only compute configs created by the current user are returned."
    ),
    cls=LegacyAnyscaleCommand,
    is_limited_support=True,
)
@click.option(
    "-n",
    "--name",
    required=False,
    default=None,
    help="List information about the compute config with this name.",
)
@click.option(
    "--compute-config-id",
    "--id",
    required=False,
    default=None,
    help="List information about the compute config with this id.",
)
@click.option(
    "--include-shared",
    is_flag=True,
    default=False,
    help="Include all compute configs you have access to.",
)
@click.option(
    "--max-items",
    required=False,
    default=20,
    type=int,
    help="Max items to show in list.",
    callback=validate_non_negative_arg,
)
def list(  # noqa: A001
    name: Optional[str],
    compute_config_id: Optional[str],
    include_shared: bool,
    max_items: int,
):
    ComputeConfigController().list(
        cluster_compute_name=name,
        cluster_compute_id=compute_config_id,
        include_shared=include_shared,
        max_items=max_items,
    )


@compute_config_cli.command(
    name="get",
    help=(
        "Get the details of a compute config.\n\n"
        "The name can contain an optional version, e.g., 'name:version'. "
        "If no version is provided, the latest one will be returned.\n\n"
    ),
    cls=AnyscaleCommand,
    example=command_examples.COMPUTE_CONFIG_GET_EXAMPLE,
)
@click.argument("compute-config-name", required=False)
@click.option(
    "-n", "--name", required=False, default=None, help="Name of the compute config.",
)
@click.option(
    "--compute-config-id",
    "--id",
    required=False,
    default=None,
    help="ID of the compute config. Alternative to name.",
    hidden=True,
)
@click.option(
    "--include-archived", is_flag=True, help="Include archived compute configurations.",
)
@click.option(
    "--old-format",
    is_flag=True,
    default=False,
    help="Output the config in the old format: https://docs.anyscale.com/reference/python-sdk/models#createclustercomputeconfig.",
)
def get_compute_config(
    name: Optional[str],
    compute_config_name: Optional[str],
    compute_config_id: Optional[str],
    include_archived: bool,
    old_format: bool,
):
    name, cc_id = _validate_name_and_id_args(
        positional_name=compute_config_name, flag_name=name, id_flag=compute_config_id
    )
    if old_format:
        ComputeConfigController().get(
            cluster_compute_name=name,
            cluster_compute_id=cc_id,
            include_archived=include_archived,
        )
    else:
        config: ComputeConfig = anyscale.compute_config.get(
            name=name, _id=cc_id, include_archived=include_archived,
        )
        stream = StringIO()
        yaml.dump(config.to_dict(), stream, sort_keys=False)
        print(stream.getvalue(), end="")
