# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["ScoreCreateResponse"]


class ScoreCreateResponse(BaseModel):
    commit_id: int

    publish_operation_id: str

    score_ids: List[str]
