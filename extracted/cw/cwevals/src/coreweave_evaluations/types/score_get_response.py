# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ScoreGetResponse", "Target"]


class Target(BaseModel):
    id: str
    """ID of the published case, comparison, or trajectory selected by kind."""

    kind: Literal["case", "comparison", "trajectory"]
    """Kind of resource being scored."""


class ScoreGetResponse(BaseModel):
    attributes: Dict[str, object]

    commit_id: int

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    scope_ref: str

    score_id: str

    scorer_id: str

    scorer_version_id: str

    target: Target

    value: object

    value_type: Literal["null", "boolean", "integer", "number", "string", "json"]
