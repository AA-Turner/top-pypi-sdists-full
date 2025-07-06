from __future__ import annotations

"""Weighted merging of voxel states."""

from .voxel import MeshVoxel


def merge_voxels(a: MeshVoxel, b: MeshVoxel, weight: float = 0.5) -> MeshVoxel:
    """Return weighted merge of ``a`` and ``b``."""
    w2 = 1.0 - weight
    return MeshVoxel(
        a.pace * weight + b.pace * w2,
        a.rate * weight + b.rate * w2,
        a.state * weight + b.state * w2,
        a.spin * weight + b.spin * w2,
    )

__all__ = ["merge_voxels"]
