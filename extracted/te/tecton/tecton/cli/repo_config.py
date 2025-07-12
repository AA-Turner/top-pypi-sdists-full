import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Tuple

import click
import yaml
from colorama import Fore

from tecton import version
from tecton._internals.tecton_pydantic import pydantic_v1
from tecton.cli import printer
from tecton.cli.command import TectonCommandCategory
from tecton.cli.command import TectonGroup
from tecton.framework import repo_config as repo_config_module
from tecton_core import repo_file_handler


logger = logging.getLogger(__name__)

DEFAULT_REPO_CONFIG_NAME = "repo.yaml"

# Templated starter repo config string. Simpler than bundling as a data asset.
_STARTER_REPO_CONFIG = """# This is the Tecton repo config. It's used to configure how Tecton builds and applies your
# feature definitions during `tecton plan/apply/test`.
#
# By default, the Tecton CLI will use the Repo Config specified at <TECTON_REPO_ROOT>/repo.yaml, but you
# can specify another file by using `tecton plan --config my_config.yaml`.

# The `defaults` keyword specifies default parameter values for Tecton objects defined in your Feature Repository.
# For example, you can set a default `tecton_materialization_runtime` for all Batch Feature Views.
# Defaults can be overridden on a per-object basis in your Python feature definitions.
# See Tecton's documentation for details on which Tecton objects are currently supported by the `defaults` keyword.

defaults:
  batch_feature_view:
    tecton_materialization_runtime: {current_version}
    environment: {environment}  # For Rift-based Batch Feature Views
  stream_feature_view:
    tecton_materialization_runtime: {current_version}
    environment: {environment}  # For Rift-based Stream Feature Views
  feature_table:
    tecton_materialization_runtime: {current_version}

# Below is an example of other defaults that can be set using the `defaults` keyword.
# defaults:
#   batch_feature_view:
#     tecton_materialization_runtime: {current_version}
#     online_store:
#       kind: RedisConfig
#     offline_store:
#       kind: OfflineStoreConfig
#       staging_table_format:
#         kind: ParquetConfig
#     batch_compute:
#       kind: DatabricksClusterConfig
#       instance_type: m5.xlarge
#       number_of_workers: 2
#       extra_pip_dependencies:
#         - haversine==2.8.0
#   stream_feature_view:
#     tecton_materialization_runtime: {current_version}
#     stream_compute:
#       kind: DatabricksClusterConfig
#       instance_availability: on_demand
#       instance_type: m5.2xlarge
#       number_of_workers: 4
#     offline_store:
#       kind: OfflineStoreConfig
#       staging_table_format:
#         kind: ParquetConfig
#     aggregation_leading_edge:
#       kind: AggregationLeadingEdge
#   feature_table:
#     tecton_materialization_runtime: {current_version}
#     batch_compute:
#       kind: DatabricksClusterConfig
#       instance_type: m5.xlarge
#       number_of_workers: 2
#     online_store:
#       kind: RedisConfig
#   feature_service:
#     realtime_environment: tecton-python-extended:0.4
#     transform_server_group: default_transform_server_group
#     feature_server_group: default_feature_server_group
#   stream_source:
#     push_config:
#       transform_server_group: default_transform_server_group
#       ingest_server_group: default_ingest_server_group
"""


@click.command("repo-config", cls=TectonGroup, command_category=TectonCommandCategory.WORKSPACE)
def repo_config_group():
    """Create, inspect, or debug the repo configuration."""


@repo_config_group.command("show")
@click.argument(
    "config", required=False, default=None, type=click.Path(exists=True, dir_okay=False, path_type=Path, readable=True)
)
def show(config: Optional[Path]):
    """Print out the parsed repo config at CONFIG path. Defaults to the repo.yaml at the repo root."""
    if config is None:
        config = get_default_repo_config_path()

    printer.safe_print(f"Loading and printing repo config at path: {config}")
    load_repo_config(config)
    loaded_config = repo_config_module.get_repo_config()

    # TODO(jake): This prints out formatted JSON, which is decent. Using a library like "rich" or a custom function
    # to print out the model would be better.
    printer.safe_print(loaded_config.json(exclude_unset=True, indent=4, by_alias=True))


@repo_config_group.command("init")
@click.argument("config", required=False, default=None, type=click.Path(exists=False, path_type=Path, readable=True))
def init(config: Optional[Path]):
    """Write out a starter repo config to the provided CONFIG path. Default path is REPO_ROOT/repo.yaml."""
    if config is None:
        config = get_default_repo_config_path()

    if config.exists():
        printer.safe_print(Fore.RED + f"A file already exists at {config}. Aborting." + Fore.RESET)
        sys.exit(1)

    create_starter_repo_config(config_path=config)
    printer.safe_print(
        f"Starter repo config written to {config}.\n\n💡 We recommend tracking this file in git.", file=sys.stderr
    )


def create_starter_repo_config(config_path: Path):
    """Create a starter repo config to config_path."""
    sdk_version = version.get_version()

    # TODO (TEC-19058): hard-coded pending a process that publishes the environments at the same time as the SDK
    environment = "tecton-core-1.2.0" if sdk_version != "99.99.99" else ""
    formatted_start_repo_config = _STARTER_REPO_CONFIG.format(current_version=sdk_version, environment=environment)

    with open(config_path, "w") as file:
        file.write(formatted_start_repo_config)


def get_default_repo_config_path() -> Path:
    repo_file_handler.ensure_prepare_repo()
    repo_root = repo_file_handler.repo_root()
    return Path(repo_root) / DEFAULT_REPO_CONFIG_NAME


def load_repo_config(repo_config_path: Path) -> None:
    """Load the repo config from the yaml file at repo_config_path."""
    if not repo_config_path.exists():
        printer.safe_print(
            Fore.RED
            + f"A repo config is required for this command and not found at {repo_config_path}. Run `tecton repo-config init` to create a starter config."
            + Fore.RESET
        )
        sys.exit(1)

    # Existence of the repo config path should already be validated by this point.
    with open(repo_config_path, "r") as file:
        try:
            repo_config_dict = yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            printer.safe_print(
                Fore.RED
                + f"Failed to parse the Tecton repo config at {repo_config_path}. Likely invalid YAML."
                + f"\nError details:\n{e}"
                + Fore.RESET
            )
            sys.exit(1)

    try:
        config = repo_config_module.RepoConfig(**repo_config_dict)
    except pydantic_v1.ValidationError as e:
        printer.safe_print(
            Fore.RED + f"Invalid Tecton repo config at {repo_config_path}.\n\n" + "Error details:" + Fore.RESET
        )

        for error_details in e.errors():
            pretty_details = _PrettyPydanticErrorDetails.from_pydantic_details(error_details)
            # Include the problem value at the error path. Note that in Pydantic V2, the error includes the input value,
            # so we can remove this logic when moving to Pydantic V2.
            input_value = _get_nested_value(repo_config_dict, pretty_details.raw_path)
            printer.safe_print(
                Fore.RED
                + f"  {pretty_details.message}\n"
                + f"    Path: '{pretty_details.path}'\n"
                + f"    Value: {input_value} ({type(input_value)})"
                + Fore.RESET
            )

        logger.debug(f"Raw repo config error: {e}.")
        sys.exit(1)

    repo_config_module.set_repo_config(config)
    logger.debug(f"Successfully loaded repo config: {config}")


@dataclass
class _PrettyPydanticErrorDetails:
    """Used to improve Pydantic repo config error rendering."""

    raw_path: Tuple[str, ...]
    raw_message: str
    value: Any
    error_type: str

    @classmethod
    def from_pydantic_details(cls, details: Mapping) -> "_PrettyPydanticErrorDetails":
        return cls(
            raw_path=details.get("loc", ()),
            raw_message=details.get("msg", "Unknown error."),
            value=details.get("input"),
            error_type=details.get("type", "unknown_error"),
        )

    @property
    def path(self) -> Optional[str]:
        return ".".join(self.raw_path)

    @property
    def field_name(self) -> str:
        if len(self.raw_path) == 0:
            msg = "Invalid path provided for exception."
            raise ValueError(msg)
        return self.raw_path[-1]

    @property
    def message(self) -> str:
        pretty_error_msgs = {
            "value_error.extra": f"Unexpected field name '{self.field_name}' found at path",
            "value_error.discriminated_union.missing_discriminator": f"Missing 'kind' field at '{self.path}'. Kind is needed to discrimate Union types, e.g. 'kind: ParquetConfig'",
        }
        return pretty_error_msgs.get(self.error_type, self.raw_message)


def _get_nested_value(dct: dict, raw_path: Tuple[str, ...]) -> Any:
    """Safely traverse a nested dictionary using a tuple of keys. Return the value at path."""
    current = dct
    for key in raw_path:
        if not isinstance(current, dict):
            # Not at a leaf in the path, but the current value is not a dictionary. This is unexpected, but return
            # None to be safe.
            logger.warning(f"Expected value at nested path {raw_path} but did not find one.")
            return None

        is_discriminator_key = "kind" in current and current["kind"] == key
        if is_discriminator_key:
            # For some reason Pydantic V1 includes Union discriminators in the path, e.g. DatabricksClusterConfig in
            # 'defaults.batch_feature_view.batch_compute.DatabricksClusterConfig.number_of_workers'. Skip these path
            # entries.
            continue

        if key not in current:
            return None

        current = current[key]

    return current
