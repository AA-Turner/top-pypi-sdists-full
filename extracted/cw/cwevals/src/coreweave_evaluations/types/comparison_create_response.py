# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["ComparisonCreateResponse"]


class ComparisonCreateResponse(BaseModel):
    commit_id: int

    comparison_ids: List[str]

    publish_operation_id: str
