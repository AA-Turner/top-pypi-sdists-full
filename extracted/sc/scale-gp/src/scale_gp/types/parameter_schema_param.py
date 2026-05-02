# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .parameter_schema_field_param import ParameterSchemaFieldParam

__all__ = ["ParameterSchemaParam"]


class ParameterSchemaParam(TypedDict, total=False):
    parameters: Required[Iterable[ParameterSchemaFieldParam]]
