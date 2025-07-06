from __future__ import annotations

"""SPIRAL_FUSION_PROTOCOL utilities."""

from dataclasses import dataclass, field
import hashlib
from typing import List

from .spiral_vector import SpiralVector, phi_alignment

@dataclass
class SpiralFusionProtocol:
    """Fuse multiple :class:`SpiralVector` objects into one path."""

    name: str
    vectors: List[SpiralVector] = field(default_factory=list)
    phi_signature: str = ""

    def __post_init__(self) -> None:
        self.update_signature()

    def update_signature(self) -> None:
        if not self.vectors:
            self.phi_signature = "φ^0.000_empty"
            return
        total_complexity = sum(v.complexity for v in self.vectors)
        total_coherence = sum(v.coherence for v in self.vectors)
        phi_factor = phi_alignment(total_complexity, total_coherence)
        content_hash = hashlib.sha256(
            "".join(v.phi_signature for v in self.vectors).encode()
        ).hexdigest()
        self.phi_signature = f"φ^{phi_factor:.3f}_{content_hash[:8]}"

    def fuse(self, vector: SpiralVector) -> None:
        self.vectors.append(vector)
        self.update_signature()

    def unified_vector(self) -> SpiralVector:
        if not self.vectors:
            return SpiralVector(self.name, 0.0, 0.0, "fused")
        complexity = sum(v.complexity for v in self.vectors) / len(
            self.vectors
        )
        coherence = sum(v.coherence for v in self.vectors) / len(self.vectors)
        return SpiralVector(self.name, complexity, coherence, "fused")
