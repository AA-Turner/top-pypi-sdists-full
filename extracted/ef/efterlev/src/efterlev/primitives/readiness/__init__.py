"""Readiness scoring — single deterministic signal of "how close am I?".

ISVs running their first FedRAMP 20x can produce all the artifacts
Efterlev emits and still not know whether they're ready to engage a
3PAO. The Gap Agent says "23 not_implemented"; the POA&M lists them
out; but there's no single signal of overall position. `efterlev
readiness` is that signal.

Pure deterministic: reads the provenance store + the FRMR catalog +
manifests directory. No LLM call. Same calculation regardless of
when it's run (modulo workspace state changes).
"""

from __future__ import annotations

from efterlev.primitives.readiness.gate import (
    ALL_ITEMS,
    GateItem,
    KsiGateResult,
    Rfc0017GateReport,
    compute_rfc_0017_gate,
)
from efterlev.primitives.readiness.score import (
    ReadinessReport,
    ReadinessScore,
    TopBlocker,
    compute_readiness,
    load_latest_claim_statuses,
)

__all__ = [
    "ALL_ITEMS",
    "GateItem",
    "KsiGateResult",
    "ReadinessReport",
    "ReadinessScore",
    "Rfc0017GateReport",
    "TopBlocker",
    "compute_readiness",
    "compute_rfc_0017_gate",
    "load_latest_claim_statuses",
]
