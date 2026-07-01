# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .parameter_schema_field import ParameterSchemaField

__all__ = ["ParameterSchema"]


class ParameterSchema(BaseModel):
    parameters: List[ParameterSchemaField]
