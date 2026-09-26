# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["StructFieldParam"]


class StructFieldParam(TypedDict, total=False):
    fields: Required[Iterable["SourceFieldParam"]]

    name: Optional[str]


from .source_field_param import SourceFieldParam
