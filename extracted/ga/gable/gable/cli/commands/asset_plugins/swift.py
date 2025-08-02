import functools
import importlib
import os
import subprocess
import sys
import traceback
from typing import Any, Callable, List, Mapping, TypedDict

import click
from gable.api.client import GableAPIClient
from gable.cli.commands.asset_plugins.baseclass import (
    AssetPluginAbstract,
    ExtractedAsset,
)
from gable.cli.helpers.data_asset import get_git_repo, get_relative_project_path
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.npm import (
    get_sca_prime_results,
    prepare_npm_environment,
    run_sca_npx_help,
    start_sca_prime,
)
from gable.openapi import SourceType, StructuredDataAssetResourceName
from loguru import logger

SwiftConfig = TypedDict(
    "SwiftConfig",
    {
        "project_root": click.Path,
        "annotation": str,
        "debug": click.Option,
    },
)


class SwiftAssetPlugin(AssetPluginAbstract):
    def source_type(self) -> SourceType:
        return SourceType.swift

    def click_options_decorator(self) -> Callable:
        def decorator(func):
            @click.option(
                "--project-root",
                help="The directory location of the Swift project that will be analyzed.",
                type=click.Path(exists=True),
                required=True,
            )
            @click.option(
                "--annotation",
                help="Annotation name that will be used for asset detection, can include multiple entries e.g. --annotation <a> --annotation <b>",
                type=str,
                multiple=True,
                required=False,
            )
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def click_options_keys(self) -> set[str]:
        return set(SwiftConfig.__annotations__.keys())

    def pre_validation(self, config: Mapping) -> None:
        typed_config = SwiftConfig(**config)
        if not typed_config["project_root"]:
            raise click.MissingParameter(
                f"{EMOJI.RED_X.value} Missing required options for Swift project registration. --project-root is required. You can use the --help option for more details.",
                param_type="option",
            )

    def extract_assets(
        self, client: GableAPIClient, config: Mapping
    ) -> List[ExtractedAsset]:
        try:
            typed_config = SwiftConfig(**config)
            project_root = config["project_root"]

            annotations = []
            if "annotation" in config:
                annotations = config["annotation"]

            prepare_npm_environment(client)
            run_sca_npx_help(client.endpoint)
            semgrep_bin_path = self.install_semgrep()

            sca_prime_future = start_sca_prime(
                client=client,
                project_root=project_root,
                annotations=annotations,
                sca_debug=("debug" in config),
                semgrep_bin_path=semgrep_bin_path,
            )

            results, locations = get_sca_prime_results(
                sca_prime_future,
                client,
                project_root,
                post_metrics=False,
            )

            self.log_asset_location_results(locations)

            git_ssh_repo = get_git_repo(str(typed_config["project_root"]))
            _, relative_project_root = get_relative_project_path(
                str(typed_config["project_root"])
            )
            data_source = f"git@{git_ssh_repo}:{relative_project_root}"
            assets = [
                ExtractedAsset(
                    darn=StructuredDataAssetResourceName(
                        source_type=SourceType.swift,
                        data_source=data_source,
                        path=event_name,
                    ),
                    fields=[
                        field
                        for field in map(
                            ExtractedAsset.safe_parse_field, event_schema["fields"]
                        )
                        if field is not None
                    ],
                    dataProfileMapping=None,
                )
                for event_name, event_schema in {**results}.items()
            ]
            return assets

        except Exception as e:
            traceback.print_exc()
            raise click.ClickException(
                f"{EMOJI.RED_X.value} FAILURE: {e}",
            )

    def checked_when_registered(self) -> bool:
        return False

    def log_asset_location_results(self, results: dict[str, tuple[Any, Any]]) -> None:
        for name, info in results.items():
            self.log_finding(name, info)  # name, (recap, source_location)

    def log_finding(self, asset_name: str, asset_info: tuple[Any, Any]) -> None:
        try:
            asset_type = asset_info[0]["type"]
            asset_fields = asset_info[0]["fields"]
            source_location = asset_info[1]

            log_message = "Detected asset: \n" + asset_type + " " + asset_name + " {\n"
            for field in asset_fields:
                log_message += f"  {field['name']}: {field['type']}"
                if field["type"] == "union":
                    log_message += (
                        "[" + ", ".join([x["type"] for x in field["types"]]) + "]"
                    )
                elif field["type"] == "list":
                    log_message += f"[{field['values']['type']}]"
                elif field["type"] == "map":
                    log_message += (
                        f"[{field['keys']['type']}: {field['values']['type']}]"
                    )
                log_message += "\n"
            log_message += "}\n"
            location = (
                source_location["file_path"]
                + ":"
                + str(source_location["start"]["line"])
            )
            log_message += f"Location: {location}\n"
            logger.debug(log_message)

        except KeyError as e:
            logger.warning(
                f"{EMOJI.RED_X.value} Malformed findings data for asset: {asset_name} - {e}"
            )
            # try to show as much as possible, even if there are some failures

        except Exception as e:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Failed to render asset: {asset_name} - {e}",
            )

    def install_semgrep(self) -> str:
        return "".join(self._pip_install("semgrep", "1.90.0"))

    def _pip_install(self, package, exact_version, import_name=None) -> str:
        """
        Install a package using pip if it's not already installed
        """
        try:
            bin_path = os.path.join(
                importlib.import_module(import_name or package).__path__[0],
                "bin",
                "semgrep-core",
            )
            return bin_path
        except ImportError:
            try:
                subprocess.run(
                    [
                        # sys.executable is the path to the current python interpreter so we know
                        # we're installing the package in the same environment
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        f"{package}=={exact_version}",
                        "-qqq",
                    ],
                    check=True,
                )
                bin_path = os.path.join(
                    importlib.import_module(import_name or package).__path__[0],
                    "bin",
                    "semgrep-core",
                )
                return bin_path

            except Exception as e:
                raise click.ClickException(
                    f"Error installing {package}: {e}",
                )
