import os
import re
from typing import Any, Optional, Tuple

import click
import yaml

from gable.cli.helpers.data_asset import get_abs_project_root_path
from gable.cli.helpers.repo_interactions import (
    get_git_repo_info,
    get_relative_file_path,
)


def get_spark_job_entrypoint_file(spark_job_entrypoint: str) -> str:
    """Remove any arguments that are passed into the entrypoint script (not our CLI args, args expected by the customer)
    Returns Just the PySpark script file path"""
    return re.split(r"\s+", spark_job_entrypoint)[0]


def get_relative_paths(project_root: str, spark_job_entrypoint: str) -> Tuple[str, str]:
    """Returns the name of the Python project, and the relative path to the PySpark script from the project root."""
    spark_job_entrypoint_no_args = os.path.join(
        project_root, get_spark_job_entrypoint_file(spark_job_entrypoint)
    )
    git_repo_info = get_git_repo_info(spark_job_entrypoint_no_args)
    relative_spark_job_entrypoint = get_relative_file_path(
        git_repo_info, spark_job_entrypoint_no_args
    )
    relative_project_root = get_relative_file_path(
        git_repo_info, get_abs_project_root_path(project_root)
    )
    project_name = os.path.basename(relative_project_root)
    return project_name, re.sub(
        r"^" + relative_project_root, "", relative_spark_job_entrypoint
    ).strip("/")


def get_nested_value(d: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        if key in d:
            d = d[key]
        else:
            return None
    return d


def read_config_file(
    config_file: click.File, config_entrypoint: str, config_args: Optional[str] = None
) -> str:
    try:
        config_file_yaml: dict[str, Any] = yaml.safe_load(config_file)  # type: ignore
        spark_job_entrypoint = get_nested_value(
            config_file_yaml, config_entrypoint.split(".")
        )
        spark_job_args = (
            get_nested_value(config_file_yaml, config_args.split("."))
            if config_args
            else None
        )

        return spark_job_entrypoint + (
            f' {" ".join(spark_job_args)}' if spark_job_args else ""
        )

    except yaml.scanner.ScannerError as exc:  # type: ignore
        # This should be a custom exception for user errors
        raise click.ClickException(f"Error parsing YAML file: {config_file}")
