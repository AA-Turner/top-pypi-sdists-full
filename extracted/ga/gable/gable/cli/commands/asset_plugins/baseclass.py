from abc import ABC, abstractmethod
from typing import Any, Callable, List, Mapping, NamedTuple, Optional

from gable.api.client import GableAPIClient
from gable.openapi import (
    DataAssetFieldsToProfilesMapping,
    GableSchemaField,
    GableSchemaFieldUnknown,
    SourceType,
    StructuredDataAssetResourceName,
)


class ExtractedAsset(NamedTuple):
    darn: StructuredDataAssetResourceName
    fields: List[GableSchemaField]
    dataProfileMapping: Optional[DataAssetFieldsToProfilesMapping]

    @staticmethod
    def safe_parse_field(field: dict[str, Any]) -> Optional[GableSchemaField]:
        """Safely parse a field from a dictionary. If the field dictionary is not parseable but has a name,
        return an "unknown" type with the name. If it doesn't have a name, return None.
        """
        try:
            return GableSchemaField.parse_obj(field)
        except Exception as e:
            if "name" in field:
                # If the field has a name, we can at least return an unknown type with the name
                return GableSchemaField(
                    __root__=GableSchemaFieldUnknown(name=field["name"], type="unknown")
                )
        return None


class AssetPluginAbstract(ABC):
    @abstractmethod
    def source_type(self) -> SourceType:
        """Source type of the asset plugin"""

    @abstractmethod
    def click_options_decorator(self) -> Callable:
        """Decorator for click options for the asset plugin"""

    @abstractmethod
    def click_options_keys(self) -> set[str]:
        """Key names for the click options the asset plugin offers. This should be generated from a TypedDict that the plugin implementation uses
        to access the options. For example:
            return set(TypeScriptConfig.__annotations__.keys())
        """

    @abstractmethod
    def pre_validation(self, config: Mapping) -> None:
        """Validation for the asset plugin's inputs before asset extraction. This is intended
        for validity checks that cannot be done with click's validation and occurs after that validation.
        Should raise a click error like UsageError or MissingParameter.
        """

    @abstractmethod
    def extract_assets(
        self, client: GableAPIClient, config: Mapping
    ) -> List[ExtractedAsset]:
        """Extract assets from the source."""

    @abstractmethod
    def checked_when_registered(self) -> bool:
        pass
