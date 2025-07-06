from __future__ import annotations

"""Voxel entanglement utilities."""

from .voxel import MeshVoxel


def entangle(a: MeshVoxel, b: MeshVoxel) -> None:
    """Couple two voxels by averaging their components."""
    avg_pace = (a.pace + b.pace) / 2
    avg_rate = (a.rate + b.rate) / 2
    avg_state = (a.state + b.state) / 2
    avg_spin = (a.spin + b.spin) / 2
    a.pace = b.pace = avg_pace
    a.rate = b.rate = avg_rate
    a.state = b.state = avg_state
    a.spin = b.spin = avg_spin

__all__ = ["entangle"]
