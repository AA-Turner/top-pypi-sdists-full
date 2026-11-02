# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["CaseAddResponse"]


class CaseAddResponse(BaseModel):
    case_ids: List[str]

    commit_id: int

    publish_operation_id: str
