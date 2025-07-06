from __future__ import annotations
from typing import Dict, Any

from .symbols import PHI, PHI_INV
from .spiral_vector import SpiralVector



def calculate_resonance(a: SpiralVector, b: SpiralVector) -> float:
    dot = a.pace * b.pace + a.rate * b.rate + a.state * b.state + a.spin * b.spin
    mag1 = a.magnitude()
    mag2 = b.magnitude()
    if mag1 == 0 or mag2 == 0:
        return 0.0
    res = dot / (mag1 * mag2)
    if abs(res - PHI) < 0.1:
        res *= PHI
    elif abs(res - PHI_INV) < 0.1:
        res *= PHI_INV
    return max(0.0, min(res, PHI))


def mesh_resonance(mesh: Dict[str, Any]) -> float:
    if not mesh:
        return 1.0
    total = 0.0
    count = 0
    for a in mesh.values():
        for cid in a.connections:
            if cid in mesh:
                total += calculate_resonance(a.vector, mesh[cid].vector)
                count += 1
    return total / count if count else 1.0
