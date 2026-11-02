# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["VersionGetResponse", "Scorer"]


class Scorer(BaseModel):
    scorer_id: str

    version_id: str


class VersionGetResponse(BaseModel):
    dataset_id: str

    dataset_version_id: str

    evaluation_id: str

    evaluation_version_id: str

    last_commit_id: int
    """Last published write visible to this snapshot.

    Scores and reported metrics published later are excluded.
    """

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    primary_target_kind: Literal["case", "trajectory"]

    scope_ref: str

    scorers: List[Scorer]
    """
    Scorer versions selected for this snapshot, in the order used by result
    responses.
    """
