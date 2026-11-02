# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["TrajectoryCreateResponse"]


class TrajectoryCreateResponse(BaseModel):
    commit_id: int

    publish_operation_id: str

    trajectory_ids: List[str]
