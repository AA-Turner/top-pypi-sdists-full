from __future__ import annotations

"""TriStar handshake using φ-field correction and vector logging."""

from typing import Optional, Dict

from ..core.phi_math import phi_wavefunction, phase_alignment_potential
from ..core.rev_eng import Rev_Eng

def handshake(
    local_phi: float, remote_phi: float, rev: Optional[Rev_Eng] = None
) -> Dict[str, float]:
    """Return resonance metrics and optionally log via ``Rev_Eng``."""
    wave_local = phi_wavefunction(local_phi)
    wave_remote = phi_wavefunction(remote_phi)
    delta = remote_phi - local_phi
    potential = phase_alignment_potential(delta)
    resonance = wave_local * wave_remote
    metrics = {
        "delta": delta,
        "potential": potential,
        "resonance": resonance,
    }
    if rev:
        rev.log_event(
            "TRISTAR_HANDSHAKE",
            delta=delta,
            potential=potential,
            resonance=resonance,
        )
    return metrics
