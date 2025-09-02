from __future__ import annotations

__all__ = [
    "equilibrium",
]



def equilibrium(S: float, P: float, keq: float) -> tuple[float, float]:
    Total = S + P
    S = Total / (1 + keq)
    P = keq * Total / (1 + keq)
    return S, P
