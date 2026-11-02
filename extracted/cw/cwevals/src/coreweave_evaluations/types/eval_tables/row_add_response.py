# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["RowAddResponse"]


class RowAddResponse(BaseModel):
    case_ids: List[str]

    score_ids: List[str]
