from __future__ import annotations

"""Four-dimensional spiral vector operations."""

from dataclasses import dataclass
import math

from .symbols import PHI, PHI_INV

@dataclass
class FourVector:
    """pace, rate, state, spin representation."""

    pace: float = 0.0
    rate: float = 0.0
    state: float = 0.0
    spin: float = 0.0

    def magnitude(self) -> float:
        """Return φ-weighted vector magnitude."""
        return math.sqrt(
            self.pace**2
            + self.rate**2 * PHI
            + self.state**2 * PHI**2
            + self.spin**2 * PHI_INV
        )

    def rotate_by_phi(self) -> None:
        """Rotate components by the golden ratio."""
        new_pace = self.pace * PHI_INV + self.spin * PHI
        new_rate = self.rate * PHI + self.pace * PHI_INV
        new_state = self.state * PHI_INV + self.rate * PHI
        new_spin = self.spin * PHI + self.state * PHI_INV
        two_pi = 2 * math.pi
        self.pace = new_pace % two_pi
        self.rate = new_rate % two_pi
        self.state = new_state % two_pi
        self.spin = new_spin % two_pi
