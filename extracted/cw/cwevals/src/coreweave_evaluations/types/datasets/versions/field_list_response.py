# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["FieldListResponse", "Field"]


class Field(BaseModel):
    dataset_field_id: int

    name: str

    source: Literal["input", "output"]

    value_type: Literal["boolean", "integer", "number", "string", "json"]


class FieldListResponse(BaseModel):
    fields: List[Field]
