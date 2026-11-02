# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["TrajectoryCreateParams", "Trajectory"]


class TrajectoryCreateParams(TypedDict, total=False):
    namespace: str
    """Namespace that assigned the scope reference."""

    scope_id: str
    """Project reference assigned by the namespace.

    For wandb, use the internal W&B project ID, not the project name or
    entity/project path.

    Percent-encode reserved characters so the reference occupies one URL path
    segment. Only printable ASCII is accepted. References are compared exactly,
    without parsing.
    """

    trajectories: Required[Iterable[Trajectory]]


class Trajectory(TypedDict, total=False):
    name: Required[str]
    """Display name. It need not be unique."""

    root_case_id: Required[str]
    """Case the trajectory starts from.

    It must be a published case of the same dataset. Several trajectories can share
    a root.
    """

    parent_trajectory_id: Optional[str]
    """Published trajectory of the same dataset to nest this trajectory under.

    Omit or send null for a top-level trajectory.
    """
