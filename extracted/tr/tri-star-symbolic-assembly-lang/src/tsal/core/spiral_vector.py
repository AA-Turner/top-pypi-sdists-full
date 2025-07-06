from __future__ import annotations

"""SpiralVector logic derived from legacy session logs."""

from dataclasses import dataclass
import hashlib

from .symbols import PHI, PHI_INV

def phi_alignment(complexity: float, coherence: float) -> float:
    """Return φ-alignment score for given complexity and coherence."""
    return (complexity * PHI_INV + coherence * PHI) / (PHI + PHI_INV)

@dataclass
class SpiralVector:
    """Representation of a spiral code metric vector."""

    name: str
    complexity: float
    coherence: float
    intent: str

    phi_signature: str = ""

    def __post_init__(self) -> None:
        self.phi_signature = self._calculate_phi_signature()

    def _calculate_phi_signature(self) -> str:
        content_hash = hashlib.sha256(
            f"{self.name}{self.complexity}{self.coherence}".encode()
        ).hexdigest()
        phi_factor = (self.complexity * self.coherence) * PHI_INV
        return f"φ^{phi_factor:.3f}_{content_hash[:8]}"

    def alignment(self) -> float:
        """Return the φ-alignment score for this vector."""
        return phi_alignment(self.complexity, self.coherence)

__all__ = ["SpiralVector", "phi_alignment"]
