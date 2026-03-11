from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from galileo_core.schemas.shared.filtered_collection import EnumFilter, MapFilter, StringFilter
from galileo_core.schemas.shared.multimodal import ContentModality

OPERATOR_LABELS = {
    "eq": "is",
    "ne": "is not",
    "contains": "contains",
    "one_of": "is one of",
    "not_in": "is not in",
    "gt": "is greater than",
    "gte": "is greater than or equal to",
    "lt": "is less than",
    "lte": "is less than or equal to",
    "between": "is between",
}


class PrintableBaseModel(BaseModel):
    def __str__(self) -> str:
        model_dict = self.model_dump(mode="json")
        string = ""
        if "name" in model_dict:
            string += f"{model_dict['name'].replace('_', ' ').title()} "
        if "key" in model_dict:
            string += f'"{model_dict["key"]}" '
        if "operator" in model_dict:
            string += f"{OPERATOR_LABELS.get(model_dict['operator'], model_dict['operator'])} "
        if "value" in model_dict:
            if isinstance(model_dict["value"], list):
                string += ", ".join([f'"{val}"' for val in model_dict["value"]])
            else:
                string += f'"{model_dict["value"]}"'
        return string


class ScorerJobFilterNames(str, Enum):
    node_name = "node_name"
    metadata = "metadata"
    modality = "modality"


class NodeNameFilter(StringFilter, PrintableBaseModel):
    """
    Filters on node names in scorer jobs.
    """

    name: Literal[ScorerJobFilterNames.node_name] = ScorerJobFilterNames.node_name


class MetadataFilter(MapFilter, PrintableBaseModel):
    """
    Filters on metadata key-value pairs in scorer jobs.
    """

    name: Literal[ScorerJobFilterNames.metadata] = ScorerJobFilterNames.metadata


class ModalityFilter(EnumFilter[ContentModality], PrintableBaseModel):
    """
    Filters on content modalities in scorer jobs.
    Matches if at least one of the specified modalities is present.
    """

    name: Literal[ScorerJobFilterNames.modality] = ScorerJobFilterNames.modality


ScorerJobFilter = Annotated[
    Union[NodeNameFilter, MetadataFilter, ModalityFilter],
    Field(discriminator="name"),
]
