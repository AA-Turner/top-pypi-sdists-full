from __future__ import annotations

"""Non-Euclidean voxel math."""

from math import sqrt
from .voxel import MeshVoxel


def manifold_distance(a: MeshVoxel, b: MeshVoxel) -> float:
    """Return simple 4D distance between voxels."""
    return sqrt(
        (a.pace - b.pace) ** 2
        + (a.rate - b.rate) ** 2
        + (a.state - b.state) ** 2
        + (a.spin - b.spin) ** 2
    )

__all__ = ["manifold_distance"]
