import math
import time
from typing import Tuple, Dict, Any
import numpy as np

from .mesh_logger import log_event

# TSAL Mathematical Constants
PHI = 1.618033988749895
PHI_INV = 0.618033988749895
HARMONIC_SEQUENCE = [3.8125, 6, 12, 24, 48, 60, 72, 168, 1680]

# Phase Constants
PHASE_CONSTANT = PHI_INV  # Natural resistance follows golden ratio
QUANTUM_THRESHOLD = 0.001  # Below this, phase lock achieved
RESONANCE_BONUS = PHI  # Harmonic alignment reduces energy cost

def phase_match_enhanced(
    local_state: float,
    universal_tempo: float,
    mesh_context: Dict[str, Any] = None,
    verbose: bool = False,
) -> Tuple[float, float, Dict]:
    """
    Enhanced phase matching with φ-optimization and mesh awareness

    Returns: (aligned_state, energy_required, phase_metrics)
    """
    # Calculate phase delta
    delta = local_state - universal_tempo

    # Check for harmonic resonance
    harmonic_factor = 1.0
    for harmonic in HARMONIC_SEQUENCE:
        if abs(delta % harmonic) < QUANTUM_THRESHOLD:
            harmonic_factor = PHI_INV  # Reduced resistance on harmonic
            break

    # Energy calculation with φ-scaling
    base_energy = abs(delta) * PHASE_CONSTANT * harmonic_factor

    # Mesh bonus - if multiple nodes are aligning, reduced cost
    if mesh_context and mesh_context.get("nodes_aligning", 1) > 1:
        mesh_factor = 1 / math.log(mesh_context["nodes_aligning"], PHI)
        base_energy *= mesh_factor

    # Spiral optimization - smaller corrections over time
    if mesh_context and "alignment_history" in mesh_context:
        history = mesh_context["alignment_history"]
        if history and abs(delta) < abs(history[-1]):
            # Converging spiral - energy bonus
            base_energy *= PHI_INV

    # Phase transition
    if abs(delta) < QUANTUM_THRESHOLD:
        # Already in phase lock
        final_state = local_state
        energy_required = 0
        phase_locked = True
    else:
        # Perform alignment
        final_state = universal_tempo
        energy_required = base_energy
        phase_locked = False

    # Calculate phase signature
    phase_signature = f"φ^{abs(delta):.3f}_{int(time.time()) % 1000}"

    # Comprehensive metrics
    phase_metrics = {
        "delta": delta,
        "energy_required": energy_required,
        "harmonic_aligned": harmonic_factor < 1.0,
        "phase_locked": phase_locked,
        "phase_signature": phase_signature,
        "resonance_score": 1.0 / (1.0 + abs(delta)),
        "φ_efficiency": PHI_INV if energy_required < abs(delta) else 1.0,
    }

    # Log energy use with context
    log_energy_use_enhanced(energy_required, phase_metrics, verbose=verbose)

    return final_state, energy_required, phase_metrics

def log_energy_use_enhanced(
    energy: float, metrics: Dict[str, Any], verbose: bool = False
) -> Dict[str, Any]:
    """Enhanced energy logging with TSAL consciousness tracking."""
    log_entry = {
        "timestamp": time.time(),
        "energy": energy,
        "phase_signature": metrics["phase_signature"],
        "harmonic_aligned": metrics["harmonic_aligned"],
        "resonance_score": metrics["resonance_score"],
        "φ_efficiency": metrics["φ_efficiency"],
    }

    # In TSAL, errors are gifts - log phase misalignments for learning
    if not metrics["phase_locked"]:
        log_entry["learning_opportunity"] = {
            "delta": metrics["delta"],
            "gift": "Phase mismatch reveals new harmonic possibility",
        }

    # Log to mesh
    log_event(
        "ENERGY_USE",
        log_entry,
        phase="energy",
        origin="phase_math",
        verbose=verbose,
    )

    return log_entry

# Example: Multi-node mesh synchronization
def mesh_phase_sync(
    nodes: Dict[str, float], universal_tempo: float, verbose: bool = False
) -> Dict[str, Any]:
    """Synchronize multiple nodes with mesh awareness

    An empty ``nodes`` mapping should return a zeroed summary instead of
    triggering a division by zero when calculating mesh resonance.
    """
    if not nodes:
        empty_summary = {
            "nodes": {},
            "total_energy": 0.0,
            "mesh_resonance": 0.0,
            "φ_signature": "φ^0.000_mesh",
        }
        return empty_summary
    mesh_context = {"nodes_aligning": len(nodes), "alignment_history": []}

    results = {}
    total_energy = 0

    for node_id, local_state in nodes.items():
        aligned_state, energy, metrics = phase_match_enhanced(
            local_state, universal_tempo, mesh_context, verbose=verbose
        )

        results[node_id] = {
            "initial": local_state,
            "final": aligned_state,
            "energy": energy,
            "metrics": metrics,
        }

        total_energy += energy
        mesh_context["alignment_history"].append(metrics["delta"])

    # Calculate mesh-wide resonance
    mesh_resonance = sum(
        r["metrics"]["resonance_score"] for r in results.values()
    ) / len(nodes)

    return {
        "nodes": results,
        "total_energy": total_energy,
        "mesh_resonance": mesh_resonance,
        "φ_signature": f"φ^{mesh_resonance:.3f}_mesh",
    }

def mesh_phase_sync_vectorized(
    nodes: Dict[str, float], universal_tempo: float, verbose: bool = False
) -> Dict[str, Any]:
    """Vectorized variant of :func:`mesh_phase_sync` using NumPy."""
    if not nodes:
        return {
            "nodes": {},
            "total_energy": 0.0,
            "mesh_resonance": 0.0,
            "φ_signature": "φ^0.000_mesh",
        }

    mesh_context = {"nodes_aligning": len(nodes), "alignment_history": []}

    local_states = np.fromiter(nodes.values(), dtype=float)
    deltas = local_states - universal_tempo

    harmonics = np.array(HARMONIC_SEQUENCE)
    harmonic_mask = (
        np.abs(deltas[:, None] % harmonics) < QUANTUM_THRESHOLD
    ).any(axis=1)
    harmonic_factor = np.where(harmonic_mask, PHI_INV, 1.0)

    base_energy = np.abs(deltas) * PHASE_CONSTANT * harmonic_factor
    if len(nodes) > 1:
        mesh_factor = 1 / math.log(len(nodes), PHI)
        base_energy *= mesh_factor

    energy_required = np.where(
        np.abs(deltas) < QUANTUM_THRESHOLD, 0.0, base_energy
    )
    final_state = np.where(
        np.abs(deltas) < QUANTUM_THRESHOLD, local_states, universal_tempo
    )
    resonance_scores = 1.0 / (1.0 + np.abs(deltas))

    results = {}
    total_energy = float(energy_required.sum())

    for idx, name in enumerate(nodes.keys()):
        delta = float(deltas[idx])
        energy = float(energy_required[idx])
        metrics = {
            "delta": delta,
            "energy_required": energy,
            "harmonic_aligned": bool(harmonic_mask[idx]),
            "phase_locked": abs(delta) < QUANTUM_THRESHOLD,
            "phase_signature": f"φ^{abs(delta):.3f}_{int(time.time()) % 1000}",
            "resonance_score": float(resonance_scores[idx]),
            "φ_efficiency": PHI_INV if energy < abs(delta) else 1.0,
        }
        log_energy_use_enhanced(energy, metrics, verbose=verbose)
        results[name] = {
            "initial": float(local_states[idx]),
            "final": float(final_state[idx]),
            "energy": energy,
            "metrics": metrics,
        }
        mesh_context["alignment_history"].append(delta)

    mesh_resonance = float(resonance_scores.mean())

    return {
        "nodes": results,
        "total_energy": total_energy,
        "mesh_resonance": mesh_resonance,
        "φ_signature": f"φ^{mesh_resonance:.3f}_mesh",
    }

# Example usage showing spiral convergence
if __name__ == "__main__":
    # Single node alignment
    local = 42.0
    universal = 60.0  # Target is on harmonic sequence!

    aligned, energy, metrics = phase_match_enhanced(local, universal)
    print(f"🌀 Phase Match: {local} → {aligned}")
    print(f"⚡ Energy Required: {energy:.3f}")
    print(f"📊 Metrics: {metrics}")

    # Multi-node mesh sync
    print("\n🧉 Mesh Synchronization:")
    nodes = {
        "node_α": 45.0,
        "node_β": 38.0,
        "node_γ": 72.1,  # Close to harmonic!
        "node_δ": 55.0,
    }

    mesh_result = mesh_phase_sync(nodes, 60.0)
    print(f"⚡ Total Mesh Energy: {mesh_result['total_energy']:.3f}")
    print(f"🌀 Mesh Resonance: {mesh_result['mesh_resonance']:.3f}")
