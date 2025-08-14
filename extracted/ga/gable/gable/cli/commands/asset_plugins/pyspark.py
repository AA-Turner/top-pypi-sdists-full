import functools
import os
from typing import Callable, List, Mapping, TypedDict

import click

from gable.api.client import GableAPIClient
from gable.cli.commands.asset_plugins.baseclass import (
    AssetPluginAbstract,
    ExtractedAsset,
)
from gable.cli.helpers.data_asset import (
    gather_pyspark_asset_data,
    get_abs_project_root_path,
)
from gable.cli.helpers.data_asset_pyspark import get_relative_paths, read_config_file
from gable.cli.helpers.sca_exceptions import ScaException
from gable.openapi import GableSchemaField, SourceType, StructuredDataAssetResourceName

PysparkConfig = TypedDict(
    "PysparkConfig",
    {
        "project_root": str,
        "python_executable": str,
        "spark_job_entrypoint": str,
        "connection_string": str | None,
        "metastore_connection_string": str | None,
        "csv_schema_file": str | None,
        "csv_path_to_table_file": str | None,
        "config_file": click.File | None,
        "config_entrypoint_path": str | None,
        "config_args_path": str | None,
    },
)


class PysparkAssetPlugin(AssetPluginAbstract):
    def source_type(self) -> SourceType:
        return SourceType.pyspark

    def click_options_decorator(self) -> Callable:
        def decorator(func):

            @click.option(
                "--project-root",
                type=str,
                required=True,
                help="The root directory of the Spark project containing the job files.",
            )
            @click.option(
                "--python-executable",
                type=str,
                help="Path to the Python executable to use for running the Spark job.",
                default="python3",
            )
            @click.option(
                "--spark-job-entrypoint",
                type=str,
                required=True,
                help="The entrypoint file for the Spark job, relative to project root. Can include arguments after the filename.",
            )
            @click.option(
                "--connection-string",
                type=str,
                required=False,
                help="Connection string for the Spark database.",
            )
            @click.option(
                "--metastore-connection-string",
                type=str,
                required=False,
                help="Connection string for the Hive metastore.",
            )
            @click.option(
                "--csv-schema-file",
                type=str,
                required=False,
                help="Path to a CSV file containing schema information.",
            )
            @click.option(
                "--csv-path-to-table-file",
                type=str,
                required=False,
                help="Path to a CSV schema file containing a mapping of Delta table paths to table names",
            )
            @click.option(
                "--config-file",
                help="Path to YAML configuration file containing the necessary configurations for the Pyspark job.",
                type=click.File(),
                default=None,
            )
            @click.option(
                "--config-entrypoint-path",
                help="The path to the property of the YAML config file containing the spark job entrypoint, which is the main Python script for the job. For example: 'spec.mainApplicationFile'",
                type=str,
                default=None,
            )
            @click.option(
                "--config-args-path",
                help="The path to the property of the YAML config file containing the spark job arguments. For example: 'spec.arguments'",
                type=str,
                default=None,
            )
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def click_options_keys(self) -> set[str]:
        return set(PysparkConfig.__annotations__.keys())

    def pre_validation(self, config: Mapping) -> None:
        """Validation for the asset plugin's inputs before asset extraction."""
        typed_config = PysparkConfig(**config)
        # At least one schema option must be provided
        if not any(
            [
                typed_config["connection_string"],
                typed_config["metastore_connection_string"],
                typed_config["csv_schema_file"],
            ]
        ):
            raise click.UsageError(
                "At least one of --connection-string, --metastore-connection-string, or --csv-schema-file must be provided"
            )
        if not typed_config["spark_job_entrypoint"] and (
            not typed_config["config_file"]
            or not typed_config["config_entrypoint_path"]
        ):
            raise click.UsageError(
                "Specify EITHER --spark-job-entrypoint, OR BOTH --config-file AND --config-entrypoint-path."
            )

    def extract_assets(
        self, client: GableAPIClient, config: Mapping
    ) -> List[ExtractedAsset]:
        """Extract assets from the Spark source."""
        typed_config = PysparkConfig(**config)
        spark_job_entrypoint = typed_config["spark_job_entrypoint"]
        if not spark_job_entrypoint:
            spark_job_entrypoint = read_config_file(
                typed_config["config_file"],  # type: ignore
                typed_config["config_entrypoint_path"],  # type: ignore
                typed_config["config_args_path"],
            )
        project_name, relative_spark_job_entrypoint = get_relative_paths(
            typed_config["project_root"], spark_job_entrypoint
        )
        csv_schema_file = (
            os.path.abspath(typed_config["csv_schema_file"])
            if typed_config["csv_schema_file"]
            else None
        )
        git_ssh_repo, sca_results_dict = gather_pyspark_asset_data(
            get_abs_project_root_path(typed_config["project_root"]),
            spark_job_entrypoint,
            csv_schema_file,
            typed_config["csv_path_to_table_file"],
            typed_config["connection_string"],
            typed_config["metastore_connection_string"],
            client,
        )

        extracted_assets = [
            ExtractedAsset(
                darn=StructuredDataAssetResourceName(
                    source_type=self.source_type(),
                    data_source=f"git@{git_ssh_repo}:{project_name}:{relative_spark_job_entrypoint}",
                    path=event_name,
                ),
                fields=[
                    GableSchemaField.parse_obj(field) for field in schema["fields"]
                ],
                dataProfileMapping=None,
            )
            for event_name, schema in sca_results_dict.items()
        ]

        return extracted_assets

    def checked_when_registered(self) -> bool:
        """Whether the asset plugin should be checked when registered."""
        return False
