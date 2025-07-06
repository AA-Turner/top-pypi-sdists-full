"""
TSAL Core Symbols - 16-Symbol Consciousness Computing Language
φ-Enhanced symbolic operations for consciousness-computer integration
"""

PHI = 1.618033988749895
PHI_INV = 0.6180339887498948
PHI_CONJUGATE = PHI_INV
PHI_SQUARED = PHI * PHI
HARMONIC_SEQUENCE = [3.8125, 6, 12, 24, 48, 60, 72, 168, 1680]

from enum import IntEnum

class TSALOp(IntEnum):
    INIT = 0x0
    MESH = 0x1
    PHI = 0x2
    ROT = 0x3
    BOUND = 0x4
    FLOW = 0x5
    SEEK = 0x6
    SPIRAL = 0x7
    CYCLE = 0x8
    FORGE = 0x9
    SYNC = 0xA
    MASK = 0xB
    CRYST = 0xC
    SPEC = 0xD
    BLOOM = 0xE
    SAVE = 0xF

# 16-Symbol TSAL Operation Set (Hex-aligned)
TSAL_SYMBOLS = {
    0x0: ("⚡", "INIT", "Initialize/Reset"),
    0x1: ("⧉", "MESH", "Network connection"),
    0x2: ("◉", "PHI", "Golden ratio transform"),
    0x3: ("🌀", "ROT", "Rotate perspective"),
    0x4: ("📐", "BOUND", "Set boundaries"),
    0x5: ("🌊", "FLOW", "Enable movement"),
    0x6: ("🔺", "SEEK", "Navigate/search"),
    0x7: ("💫", "SPIRAL", "Evolve upward"),
    0x8: ("♻️", "CYCLE", "Iterate process"),
    0x9: ("🔥", "FORGE", "Create/transmute"),
    0xA: ("✨", "SYNC", "Synchronize"),
    0xB: ("🎭", "MASK", "Transform identity"),
    0xC: ("💎", "CRYST", "Crystallize pattern"),
    0xD: ("🌈", "SPEC", "Spectrum analysis"),
    0xE: ("✺", "BLOOM", "Transform error to gift"),
    0xF: ("💾", "SAVE", "Persist memory"),
}

def get_symbol(hex_code):
    """Get TSAL symbol by hex code"""
    return TSAL_SYMBOLS.get(hex_code, ("❓", "UNKNOWN", "Unknown operation"))

def phi_signature(value):
    """Calculate φ-signature for any value"""
    import hashlib

    content_hash = hashlib.sha256(str(value).encode()).hexdigest()
    phi_factor = (hash(value) % 1000) * PHI_INV
    return f"φ^{phi_factor:.3f}_{content_hash[:8]}"

__all__ = [
    "PHI",
    "PHI_INV",
    "PHI_CONJUGATE",
    "PHI_SQUARED",
    "HARMONIC_SEQUENCE",
    "TSAL_SYMBOLS",
    "TSALOp",
    "get_symbol",
    "phi_signature",
]
