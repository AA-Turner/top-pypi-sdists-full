from __future__ import annotations

"""Shadow memory for voxel states."""

from dataclasses import dataclass, field
from typing import Dict, Optional

from .voxel import MeshVoxel

@dataclass
class ShadowMemory:
    """Track voxel state copies for taint analysis."""

    storage: Dict[str, MeshVoxel] = field(default_factory=dict)

    def read(self, name: str) -> Optional[MeshVoxel]:
        return self.storage.get(name)

    def write(self, name: str, voxel: MeshVoxel) -> None:
        self.storage[name] = MeshVoxel(voxel.pace, voxel.rate, voxel.state, voxel.spin)

__all__ = ["ShadowMemory"]
