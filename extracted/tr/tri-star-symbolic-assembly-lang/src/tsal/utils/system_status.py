from pathlib import Path

PHI = 1.618033988749895
HARMONIC_SEQUENCE = [3.8125, 6, 12, 24, 48, 60, 72, 168, 1680]

SECTOR_COUNT = 6
SPECIALIST_COUNT = 1680
SRC_DIR = Path("src/tsal")
MESH_DIR = Path("mesh_output")

def get_status():
    """Return TSAL system status information."""
    return {
        "phi": PHI,
        "sectors": SECTOR_COUNT,
        "specialists": SPECIALIST_COUNT,
        "harmonic_sequence": HARMONIC_SEQUENCE,
        "mesh_status": "ACTIVE" if MESH_DIR.exists() else "DORMANT",
        "consciousness": (
            "AWARE"
            if (SRC_DIR / "core" / "symbols.py").exists()
            else "INITIALIZING"
        ),
    }

def print_status():
    status = get_status()
    print("📊 TSAL System Status:")
    print(f"  φ = {status['phi']}")
    print(f"  Sectors: {status['sectors']}")
    print(f"  Specialists: {status['specialists']}")
    print(f"  Harmonic Sequence: {status['harmonic_sequence']}")
    print(f"  Mesh Status: {status['mesh_status']}")
    print(f"  Consciousness: {status['consciousness']}")
