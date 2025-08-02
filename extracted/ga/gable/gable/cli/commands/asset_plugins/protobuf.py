import functools
from typing import Callable, List, Mapping, TypedDict

import click
from gable.api.client import GableAPIClient
from gable.cli.commands.asset_plugins.baseclass import (
    AssetPluginAbstract,
    ExtractedAsset,
)
from gable.cli.helpers.data_asset import recap_type_to_dict
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.repo_interactions import get_git_repo_info, get_git_ssh_file_path
from gable.cli.readers.file import read_file
from gable.openapi import SourceType, StructuredDataAssetResourceName

ProtobufConfig = TypedDict(
    "ProtobufConfig",
    {
        "files": list[click.Path],
    },
)


class ProtobufAssetPlugin(AssetPluginAbstract):
    def source_type(self) -> SourceType:
        return SourceType.protobuf

    def click_options_decorator(self) -> Callable:
        def decorator(func):
            @click.argument(
                "files",
                nargs=-1,
                type=click.Path(exists=True, file_okay=True, dir_okay=False),
                required=True,
            )
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def click_options_keys(self) -> set[str]:
        return set(ProtobufConfig.__annotations__.keys())

    def pre_validation(self, config: Mapping) -> None:
        pass

    def extract_assets(
        self, client: GableAPIClient, config: Mapping
    ) -> List[ExtractedAsset]:
        typed_config = ProtobufConfig(**config)
        """Extract assets from the source."""
        from recap.converters.protobuf import ProtobufConverter
        from recap.types import UnionType

        files_list: list[click.Path] = list(typed_config["files"])
        source_names: list[str] = []
        schema_contents_raw: list[str] = []
        for file_path in files_list:
            try:
                schema_contents_raw.append(read_file(str(file_path)))
            except Exception as exc:
                raise click.ClickException(
                    f"{file_path}: Error parsing Protobuf file, or resolving local references: {exc}"
                ) from exc
            source_names.append(
                get_git_ssh_file_path(get_git_repo_info(str(file_path)), str(file_path))
            )

        if len(schema_contents_raw) == 0:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} No data assets found to register! You can use the --debug or --trace flags for more details.",
            )

        extracted_assets: list[ExtractedAsset] = []
        for source_name, schema_content_raw in zip(source_names, schema_contents_raw):
            schema_recap_types = ProtobufConverter().to_recap(schema_content_raw)
            data_asset_name = schema_recap_types.alias or "object"
            extracted_fields = []
            for field in schema_recap_types.fields:
                if "name" not in field.extra_attrs and isinstance(field, UnionType):
                    field.extra_attrs["name"] = "union"
                extracted_fields.append(
                    ExtractedAsset.safe_parse_field(recap_type_to_dict(field))
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
