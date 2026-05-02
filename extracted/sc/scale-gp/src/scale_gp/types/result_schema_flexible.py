# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .shared.flexible_chunk import FlexibleChunk
from .shared.chunk_extra_info_schema import ChunkExtraInfoSchema
from .shared.string_extra_info_schema import StringExtraInfoSchema
from .evaluation_datasets.flexible_message import FlexibleMessage

__all__ = [
    "ResultSchemaFlexible",
    "GenerationOutputAdditionalObjectGenerationOutputAdditionalObjectItem",
    "GenerationOutputAdditionalObjectGenerationOutputAdditionalObjectItemExternalFile",
    "GenerationOutputAdditionalObjectGenerationOutputAdditionalObjectItemInternalFile",
    "GenerationExtraInfo",
]


class GenerationOutputAdditionalObjectGenerationOutputAdditionalObjectItemExternalFile(BaseModel):
    file_type: Literal["image", "pdf"]

    uri: str


class GenerationOutputAdditionalObjectGenerationOutputAdditionalObjectItemInternalFile(BaseModel):
    file_id: str

    file_type: Literal["image", "pdf"]


GenerationOutputAdditionalObjectGenerationOutputAdditionalObjectItem: TypeAlias = Union[
    str,
    float,
    List[FlexibleChunk],
    List[FlexibleMessage],
    List[object],
    Dict[str, object],
    GenerationOutputAdditionalObjectGenerationOutputAdditionalObjectItemExternalFile,
    GenerationOutputAdditionalObjectGenerationOutputAdditionalObjectItemInternalFile,
]

GenerationExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class ResultSchemaFlexible(BaseModel):
    generation_output: Union[str, Dict[str, GenerationOutputAdditionalObjectGenerationOutputAdditionalObjectItem]]

    generation_extra_info: Optional[GenerationExtraInfo] = None
