# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["TrajectoryListResponse", "Trajectory"]


class Trajectory(BaseModel):
    commit_id: int

    dataset_id: str

    depth: int
    """0 for a top-level trajectory, otherwise one more than its parent's."""

    name: str

    parent_trajectory_id: Optional[str] = None
    """Null for a top-level trajectory."""

    root_case_id: str

    trajectory_id: str


class TrajectoryListResponse(BaseModel):
    trajectories: List[Trajectory]

    next_cursor: Optional[str] = None
