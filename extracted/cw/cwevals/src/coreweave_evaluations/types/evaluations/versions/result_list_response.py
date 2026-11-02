# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["ResultListResponse", "Target", "TargetScore", "TargetTarget"]


class TargetScore(BaseModel):
    commit_id: int

    score_id: str

    scorer_id: str

    scorer_version_id: str

    value: object

    value_type: Literal["null", "boolean", "integer", "number", "string", "json"]


class TargetTarget(BaseModel):
    id: str
    """ID of the published case, comparison, or trajectory selected by kind."""

    kind: Literal["case", "comparison", "trajectory"]
    """Kind of resource being scored."""


class Target(BaseModel):
    scores: List[TargetScore]

    target: TargetTarget


class ResultListResponse(BaseModel):
    published_commit_id: int

    targets: List[Target]

    next_cursor: Optional[str] = None
