"""Phi-field correction equations.

© 2025 Samuel Edward Howells. All rights reserved.
- Open for non-commercial academic and research use.
- Commercial use, redistribution, or integration into proprietary models requires written permission from the author.
- For inquiries, contact via the project page.
"""

from __future__ import annotations

import math

def phi_wavefunction(
    phi: float, phi_vacuum: float = 0.0, lam: float = 1.0
) -> float:
    """Return ψ(φ) = exp((φ - φ_vacuum) / λ)."""
    return math.exp((phi - phi_vacuum) / lam)

def phase_alignment_potential(
    phi: float, phi_vacuum: float = 0.0, lam: float = 1.0
) -> float:
    """Return g(φ) = 2 * exp((φ - φ_vacuum) / λ)."""
    return 2.0 * phi_wavefunction(phi, phi_vacuum, lam)

def corrected_energy(
    n: int, phi: float, phi_vacuum: float = 0.0, lam: float = 1.0
) -> float:
    """Return E_n = -g(φ) / n²."""
    g_val = phase_alignment_potential(phi, phi_vacuum, lam)
    return -g_val / float(n * n)

def orbital_radius(
    n: int, phi: float, phi_vacuum: float = 0.0, lam: float = 1.0
) -> float:
    """Return r_n ≈ n² / g(φ)."""
    g_val = phase_alignment_potential(phi, phi_vacuum, lam)
    return (n * n) / g_val

__all__ = [
    "phi_wavefunction",
    "phase_alignment_potential",
    "corrected_energy",
    "orbital_radius",
]
