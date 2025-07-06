from __future__ import annotations

"""Superposition of voxel states."""

from .voxel import MeshVoxel


def superpose(*voxels: MeshVoxel) -> MeshVoxel:
    """Return average of all voxels."""
    if not voxels:
        return MeshVoxel(0, 0, 0, 0)
    n = len(voxels)
    return MeshVoxel(
        sum(v.pace for v in voxels) / n,
        sum(v.rate for v in voxels) / n,
        sum(v.state for v in voxels) / n,
        sum(v.spin for v in voxels) / n,
    )

__all__ = ["superpose"]
