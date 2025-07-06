from __future__ import annotations

"""Simple voxel gradient operations."""

from .voxel import MeshVoxel


def voxel_gradient(a: MeshVoxel, b: MeshVoxel) -> MeshVoxel:
    """Return gradient ``b - a`` component-wise."""
    return MeshVoxel(
        b.pace - a.pace,
        b.rate - a.rate,
        b.state - a.state,
        b.spin - a.spin,
    )

__all__ = ["voxel_gradient"]
