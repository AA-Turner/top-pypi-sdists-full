# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ColumnCreateResponse", "DatasetField", "Scorer"]


class DatasetField(BaseModel):
    name: str

    source: Literal["input", "output"]

    value_type: Literal["null", "boolean", "integer", "number", "string", "json"]
    """json may represent an extension-backed field or an ordinary JSON field."""

    extension_schema_version: Optional[int] = None
    """Extension schema version, omitted for ordinary fields."""

    extension_type: Optional[Literal["wandb-image", "wandb-audio", "wandb-video"]] = None
    """Extension schema type, omitted for ordinary fields."""


class Scorer(BaseModel):
    name: str

    scorer_id: str

    scorer_version_id: str

    value_type: Literal["boolean", "integer", "number", "string"]


class ColumnCreateResponse(BaseModel):
    dataset_fields: List[DatasetField]

    scorers: List[Scorer]
