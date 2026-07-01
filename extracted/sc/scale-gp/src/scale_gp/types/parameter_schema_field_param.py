# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ParameterSchemaFieldParam"]


class ParameterSchemaFieldParam(TypedDict, total=False):
    description: Required[str]

    name: Required[str]

    required: Required[bool]

    type: Required[Literal["str", "int", "float", "bool"]]
