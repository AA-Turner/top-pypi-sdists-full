# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["TrajectoryGetResponse"]


class TrajectoryGetResponse(BaseModel):
    commit_id: int

    dataset_id: str

    depth: int
    """0 for a top-level trajectory, otherwise one more than its parent's."""

    name: str

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    parent_trajectory_id: Optional[str] = None
    """Null for a top-level trajectory."""

    root_case_id: str

    scope_ref: str

    trajectory_id: str
