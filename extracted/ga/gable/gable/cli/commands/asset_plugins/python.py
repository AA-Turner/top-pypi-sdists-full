import functools
import json
import re
from typing import Callable, List, Mapping, TypedDict, cast

import click

from gable.api.client import GableAPIClient
from gable.cli.commands.asset_plugins.baseclass import (
    AssetPluginAbstract,
    ExtractedAsset,
)
from gable.cli.helpers.data_asset import EventAsset
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.npm import prepare_npm_environment, run_sca_python
from gable.cli.helpers.repo_interactions import get_git_repo_info
from gable.cli.options import PYTHON_EVENT_NAME_KEY_REGEX
from gable.openapi import SourceType, StructuredDataAssetResourceName


class PythonConfig(TypedDict):
    """Configuration for Python asset plugin"""

    project_root: click.Path
    emitter_file_path: str
    emitter_function: str
    emitter_payload_parameter: str
    event_name_key: str
    exclude: str | None


class PythonAssetPlugin(AssetPluginAbstract):
    def source_type(self) -> SourceType:
        return SourceType.python

    def click_options_decorator(self) -> Callable:
        def decorator(func):

            @click.option(
                "--project-root",
                help="The directory location of the Python project that will be analyzed.",
                type=click.Path(exists=True),
                required=True,
            )
            @click.option(
                "--emitter-file-path",
                help="Relative path from the root of the project to the file that contains the emitter function",
                type=str,
                required=True,
            )
            @click.option(
                "--emitter-function",
                help="Name of the emitter function",
                type=str,
                required=True,
            )
            @click.option(
                "--emitter-payload-parameter",
                help="Name of the parameter representing the event payload",
                type=str,
                required=True,
            )
            @click.option(
                "--event-name-key",
                help="Name of the event property that contains the event name",
                type=str,
                required=True,
            )
            @click.option(
                "--exclude",
                help="Comma delimited list of filenames or patterns to exclude from the analysis",
                type=str,
                required=False,
            )
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def click_options_keys(self) -> set[str]:
        return set(PythonConfig.__annotations__.keys())

    def pre_validation(self, config: Mapping) -> None:
        if not re.match(PYTHON_EVENT_NAME_KEY_REGEX, config["event_name_key"]):
            raise click.BadParameter(
                "Invalid event name key. Must be a valid must be valid event name access path."
            )

    def extract_assets(
        self, client: GableAPIClient, config: Mapping
    ) -> List[ExtractedAsset]:
        """Extract assets from the source."""
        prepare_npm_environment(client)

        typed_config = PythonConfig(**config)
        sca_results = run_sca_python(
            project_root=str(typed_config["project_root"]),
            emitter_file_path=typed_config["emitter_file_path"],
            emitter_function=typed_config["emitter_function"],
            emitter_payload_parameter=typed_config["emitter_payload_parameter"],
            event_name_key=typed_config["event_name_key"],
            exclude_paths=typed_config["exclude"],
        )
        sca_results_dict = cast(
            dict[str, list[tuple[str, EventAsset, None]]], json.loads(sca_results)
        )
        # Assume only one key in the outer dict for now. The key is the emitter file path and function name
        _, sca_result_list = list(sca_results_dict.items())[0]
        # Filter out any undefined events, or events that are a string, which will happen
        # when the SCA returns "Unknown" for the event type
        sca_result_list = cast(
            list[EventAsset],
            [x for x in sca_result_list if x is not None and not isinstance(x, str)],
        )
        project_repo = get_git_repo_info(
            str(typed_config["project_root"]) + "/" + typed_config["emitter_file_path"]
        )
        source_name = project_repo["gitSSHRepo"]

        if not sca_result_list:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} No data assets found to register! You can use the --debug or --trace flags for more details.",
            )

        extracted_assets: list[ExtractedAsset] = []
        for schema_content in sca_result_list:
            data_asset_name = (
                f"{schema_content['eventNamespace']}.{schema_content['eventName']}"
            )
            extracted_fields = []
            for field in schema_content["properties"].items():
                field_name, field_type = field
                extracted_fields.append(
                    ExtractedAsset.safe_parse_field(
                        {
                            "name": field_name,
                            "type": field_type,
                        }
                    )
                )
            extracted_assets.append(
                ExtractedAsset(
                    darn=StructuredDataAssetResourceName(
                        source_type=self.source_type(),
                        data_source=source_name,
                        path=data_asset_name,
                    ),
                    dataProfileMapping=None,
                    fields=extracted_fields,
                )
            )
        return extracted_assets

    def checked_when_registered(self) -> bool:
        return False
