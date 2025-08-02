import functools
import importlib.util
import os
import subprocess
from typing import Any, Callable, List, Mapping, TypedDict, Union

import click
from gable.api.client import GableAPIClient
from gable.cli.commands.asset_plugins.baseclass import (
    AssetPluginAbstract,
    ExtractedAsset,
)
from gable.cli.helpers.data_asset import get_git_repo, get_relative_project_path
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.npm import (
    get_installed_package_dir,
    get_sca_cmd,
    get_sca_prime_results,
    prepare_npm_environment,
    should_use_local_sca,
    start_sca_prime,
)
from gable.cli.helpers.util import split_list_str
from gable.openapi import SourceType, StructuredDataAssetResourceName
from loguru import logger

from gable.cli.local import get_local_kotlin_script

KotlinConfig = TypedDict(
    "KotlinConfig",
    {
        "project_root": str,
        "jar_path": str,
        "event_annotations": str,
        "property_annotations": str,
    },
)


class KotlinAssetPlugin(AssetPluginAbstract):
    def source_type(self) -> SourceType:
        return SourceType.kotlin

    def click_options_decorator(self) -> Callable:
        def decorator(func):

            @click.option(
                "--project-root",
                help="The root of the Kotlin project.",
                type=click.Path(exists=True, file_okay=False, dir_okay=True),
                required=True,
            )
            @click.option(
                "--jar-path",
                help="Path to the compile .jar file.",
                type=click.Path(exists=True, file_okay=True, dir_okay=False),
                required=True,
            )
            @click.option(
                "--event-annotations",
                help="Comma delimited list of annotation classes, including namespace, used to annotate events. Example: com.example.EventAnnotation",
                type=str,
                required=True,
            )
            @click.option(
                "--property-annotations",
                help="Comma delimited list of annotation classes, including namespace, used to annotate properties of events. Example: com.example.PropertyAnnotation",
                type=str,
                required=True,
            )
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def click_options_keys(self) -> set[str]:
        return set(KotlinConfig.__annotations__.keys())

    def pre_validation(self, config: Mapping) -> None:

        typed_config = KotlinConfig(**config)
        event_annotations = split_list_str(typed_config["event_annotations"], ";")
        property_annotations = split_list_str(typed_config["property_annotations"], ";")
        if len(event_annotations) == 0:
            raise click.MissingParameter(
                f"{EMOJI.RED_X.value} At least one event annotation is required.",
                param_type="option",
            )
        if len(property_annotations) == 0:
            raise click.MissingParameter(
                f"{EMOJI.RED_X.value} At least one property annotation is required.",
                param_type="option",
            )

    def extract_assets(
        self, client: GableAPIClient, config: Mapping
    ) -> List[ExtractedAsset]:
        """Extract assets from the source."""
        typed_config = KotlinConfig(**config)

        prepare_npm_environment(client)
        sca_prime_results_future = start_sca_prime(
            client, typed_config["project_root"], []
        )
        sca_results_dict = self._run_sca_kotlin(
            str(typed_config["jar_path"]),
            typed_config["event_annotations"],
            typed_config["property_annotations"],
            client.endpoint,
        )
        if sca_results_dict == {}:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} No data assets found to register! You can use the --debug or --trace flags for more details.",
            )

        # Run Gable Code in shadow-mode
        sca_prime_results, _ = get_sca_prime_results(
            sca_prime_results_future, client, typed_config["project_root"], True
        )

        git_ssh_repo = get_git_repo(str(typed_config["project_root"]))
        _, relative_project_root = get_relative_project_path(
            str(typed_config["project_root"])
        )
        data_source = f"git@{git_ssh_repo}:{relative_project_root}"
        assets = [
            ExtractedAsset(
                darn=StructuredDataAssetResourceName(
                    source_type=SourceType.kotlin,
                    data_source=data_source,
                    path=event_name,
                ),
                fields=[
                    field
                    for field in map(
                        ExtractedAsset.safe_parse_field, event_schema["fields"]
                    )
                    if field
                ],
                dataProfileMapping=None,
            )
            for event_name, event_schema in {
                **sca_results_dict,
                **sca_prime_results,
            }.items()
        ]
        return assets

    def checked_when_registered(self) -> bool:
        return False

    def _run_sca_kotlin(
        self,
        jar_path: str,
        event_annotations: str,
        property_annotations: str,
        api_endpoint: Union[str, None] = None,
    ) -> dict[str, dict[str, Any]]:
        try:

            # Run the npx command to install the package
            subprocess.run(
                get_sca_cmd(api_endpoint, ["--help"]),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            # Dynamically import the Kotlin SCA script
            kotlin_script = self._get_kotlin_sca_script_path(api_endpoint)
            k_spec = importlib.util.spec_from_file_location(
                # We have to give the module a unique name even though we never use the
                # module by name.
                "gable_kotlin",
                kotlin_script,
            )
            if k_spec is None or k_spec.loader is None:
                raise Exception("Error importing Kotlin SCA script.")
            k_module = importlib.util.module_from_spec(k_spec)
            k_spec.loader.exec_module(k_module)

            return k_module.detect_events(
                jar_path,
                event_annotations,
                property_annotations,
            )
        except Exception as e:
            logger.opt(exception=e).debug("Error running Gable SCA")
            raise click.ClickException(
                f"Error running Gable SCA, enable --debug or --trace logging for more details: {str(e)}"
            ) from e

    def _get_kotlin_sca_script_path(self, gable_api_endpoint: Union[str, None]) -> str:
        """Returns the path to the Kotlin SCA script"""
        if should_use_local_sca(gable_api_endpoint):
            local_kotlin_script = get_local_kotlin_script()
            logger.trace(f"Using local Kotlin SCA script: {local_kotlin_script}")
            return local_kotlin_script
        return os.path.join(get_installed_package_dir(), "dist/kotlin.py")
