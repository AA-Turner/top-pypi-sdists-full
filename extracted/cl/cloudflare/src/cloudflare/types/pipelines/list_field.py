# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._models import BaseModel

__all__ = ["ListField"]


class ListField(BaseModel):
    items: "SourceField"


from .source_field import SourceField
