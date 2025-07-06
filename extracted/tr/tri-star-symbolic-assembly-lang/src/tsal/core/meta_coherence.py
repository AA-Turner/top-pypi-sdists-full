from __future__ import annotations

"""Simple meta-coherence calculation utilities."""

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .symbols import PHI


@dataclass
class SpiralSignature:
    """Fourier-based spiral signature."""

    amplitude: np.ndarray
    phase: np.ndarray


def compute_spiral_signature(phases: Sequence[float], golden_ratio: float = PHI) -> SpiralSignature:
    """Return a basic spiral signature chart from raw phase data."""
    arr = np.asarray(phases, dtype=float)
    freq = np.fft.fft(arr)
    modulated = freq * golden_ratio
    amplitude = np.abs(modulated)
    phase = np.angle(modulated)
    return SpiralSignature(amplitude=amplitude, phase=phase)

__all__ = ["SpiralSignature", "compute_spiral_signature"]
