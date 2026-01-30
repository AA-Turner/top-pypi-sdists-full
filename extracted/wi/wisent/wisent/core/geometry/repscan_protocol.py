"""
RepScan protocol: 4-step representation discovery and characterization.

1. Signal Test - does a learnable signal exist?
2. Geometry Test - is the representation linear or nonlinear?
3. Decomposition Test - is the concept fragmented into sub-concepts?
4. Intervention Selection - which steering method to use?
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import torch
import numpy as np


def _adaptive_gap_threshold(n_samples: int) -> float:
    """Adaptive geometry gap threshold based on sample size.

    With more samples, accuracy estimates are more stable, so we can
    require a smaller gap to declare nonlinearity meaningful.
    Based on: threshold = k / sqrt(n_samples) where k controls sensitivity.
    """
    # Using k=0.5 gives ~0.05 at n=100, ~0.025 at n=400
    threshold = 0.5 / np.sqrt(n_samples)
    return max(0.02, min(threshold, 0.1))


def _adaptive_min_silhouette(n_samples: int) -> float:
    """Adaptive silhouette threshold based on sample size.

    With more samples, silhouette scores are more reliable, so we can
    require higher scores to declare fragmentation.
    """
    # Scale from 0.05 at small n to 0.15 at large n
    base = 0.05 + 0.1 * min(1.0, n_samples / 500)
    return max(0.05, min(base, 0.2))


@dataclass
class SignalTestResult:
    """Result of signal existence test."""
    max_z_score: float
    min_p_value: float
    passed: bool
    permutation_metrics: Dict[str, Dict[str, float]]  # metric -> {real_score, null_mean, z_score, p_value}
    nonsense_metrics: Optional[Dict[str, Dict[str, float]]] = None  # metric -> {real_score, nonsense_score, z_score}


@dataclass
class GeometryTestResult:
    """Result of geometry (linear vs nonlinear) test."""
    linear_accuracy: float
    nonlinear_accuracy: float
    gap: float
    diagnosis: str  # "LINEAR" or "NONLINEAR"


@dataclass
class DecompositionTestResult:
    """Result of concept decomposition test."""
    n_concepts: int
    cluster_labels: List[int]
    silhouette_score: float
    is_fragmented: bool
    per_concept_sizes: Dict[int, int]


@dataclass
class InterventionResult:
    """Result of intervention method selection."""
    recommended_method: str
    confidence: float
    reasoning: List[str]
    method_scores: Dict[str, float]


def test_signal(
    pos: torch.Tensor, neg: torch.Tensor,
    metric_keys: List[str],
    model=None,
    tokenizer=None,
    layer: int = None,
    device: str = "cuda",
    p_threshold: float = 0.05,
) -> SignalTestResult:
    """Step 1: Test if a learnable signal exists relative to null.

    Runs two null tests:
    1. Permutation test - shuffles labels to test if labels carry information
    2. Nonsense baseline - compares against random token activations (if model/tokenizer provided)

    Signal passes if permutation p_value < p_threshold AND (if nonsense available)
    nonsense z_score > 2.0 for any metric.
    """
    from .signal_null_tests import compute_signal_vs_null, compute_signal_vs_nonsense, compute_aggregate_signal

    # Always run permutation test
    perm_metrics = compute_signal_vs_null(pos, neg, metric_keys)
    max_z, min_p, any_sig = compute_aggregate_signal(perm_metrics)

    # Run nonsense baseline if model/tokenizer provided
    nonsense_metrics = None
    if model is not None and tokenizer is not None:
        try:
            nonsense_metrics = compute_signal_vs_nonsense(
                pos, neg, model, tokenizer, metric_keys, layer=layer, device=device
            )
            # Combine: require both tests to pass
            nonsense_z, _, nonsense_sig = compute_aggregate_signal(nonsense_metrics)
            max_z = max(max_z, nonsense_z)
            # Signal passes if permutation significant AND nonsense significant
            passed = (min_p < p_threshold) and nonsense_sig
        except Exception:
            # If nonsense fails, fall back to permutation only
            passed = min_p < p_threshold
    else:
        passed = min_p < p_threshold

    return SignalTestResult(max_z, min_p, passed, perm_metrics, nonsense_metrics)


def test_geometry(
    pos: torch.Tensor, neg: torch.Tensor, gap_threshold: float = 0.05,
) -> GeometryTestResult:
    """Step 2: Test if geometry is linear or nonlinear."""
    from .geometry_metrics import compute_linear_nonlinear_gap
    linear, nonlinear = compute_linear_nonlinear_gap(pos, neg)
    gap = nonlinear - linear
    diagnosis = "NONLINEAR" if gap > gap_threshold else "LINEAR"
    return GeometryTestResult(linear, nonlinear, gap, diagnosis)


def test_decomposition(
    pos: torch.Tensor, neg: torch.Tensor, min_silhouette: float = 0.1,
) -> DecompositionTestResult:
    """Step 3: Test if concept is fragmented into sub-concepts."""
    from .decomposition_metrics import find_optimal_clustering
    diff = pos - neg
    n_concepts, labels, sil = find_optimal_clustering(diff)
    labels_np = np.array(labels)
    sizes = {int(k): int((labels_np == k).sum()) for k in range(n_concepts)}
    fragmented = n_concepts > 1 and sil >= min_silhouette
    return DecompositionTestResult(n_concepts, labels, sil, fragmented, sizes)


def select_intervention(
    signal: SignalTestResult,
    geometry: GeometryTestResult,
    decomposition: DecompositionTestResult,
) -> InterventionResult:
    """Step 4: Select optimal intervention method."""
    scores = {"CAA": 0.0, "Hyperplane": 0.0, "MLP": 0.0, "PRISM": 0.0, "TITAN": 0.0}
    reasoning = []

    if not signal.passed:
        return InterventionResult("NONE", 0.0, ["No signal (p > 0.05)"], scores)

    is_linear = geometry.diagnosis == "LINEAR"
    is_frag = decomposition.is_fragmented
    n = decomposition.n_concepts

    if is_linear and not is_frag:
        scores["CAA"], recommended, conf = 1.0, "CAA", 0.9
        reasoning.append("Linear + single concept → CAA")
    elif is_linear and is_frag:
        scores["PRISM"], recommended, conf = 1.0, "PRISM", 0.75
        reasoning.append(f"Linear + {n} concepts → PRISM")
    elif not is_linear and not is_frag:
        scores["Hyperplane"], recommended, conf = 1.0, "Hyperplane", 0.8
        reasoning.append("Nonlinear + single → Hyperplane")
    else:
        scores["TITAN"], recommended, conf = 1.0, "TITAN", 0.7
        reasoning.append(f"Nonlinear + {n} concepts → TITAN")

    # Boost confidence based on z-score (higher z = stronger signal)
    z_boost = min(0.1, signal.max_z_score * 0.02)
    conf = min(1.0, conf + z_boost)
    reasoning.append(f"Z-score: {signal.max_z_score:.2f}, p-value: {signal.min_p_value:.4f}, Gap: {geometry.gap:.3f}")

    return InterventionResult(recommended, conf, reasoning, scores)


def run_full_protocol(
    pos: torch.Tensor, neg: torch.Tensor,
    model=None,
    tokenizer=None,
    layer: int = None,
    device: str = "cuda",
    signal_keys: Optional[List[str]] = None,
    p_threshold: float = 0.05,
    gap_threshold: Optional[float] = None,
    min_silhouette: Optional[float] = None,
) -> Dict[str, Any]:
    """Run complete 4-step RepScan protocol.

    Signal test runs both permutation null and nonsense baseline (if model/tokenizer provided).
    Geometry and decomposition thresholds are adaptive by default.
    """
    if signal_keys is None:
        signal_keys = ["knn_accuracy", "knn_pca_accuracy", "mlp_probe_accuracy"]

    # Derive adaptive thresholds from data dimensions
    n_samples = len(pos)
    if gap_threshold is None:
        gap_threshold = _adaptive_gap_threshold(n_samples)
    if min_silhouette is None:
        min_silhouette = _adaptive_min_silhouette(n_samples)

    sig = test_signal(pos, neg, signal_keys, model, tokenizer, layer, device, p_threshold)
    geo = test_geometry(pos, neg, gap_threshold)
    dec = test_decomposition(pos, neg, min_silhouette)
    inter = select_intervention(sig, geo, dec)

    return {
        "protocol_config": {
            "n_samples": n_samples,
            "p_threshold": p_threshold,
            "gap_threshold": gap_threshold,
            "min_silhouette": min_silhouette,
        },
        "signal_test": {
            "max_z_score": sig.max_z_score,
            "min_p_value": sig.min_p_value,
            "passed": sig.passed,
            "permutation_metrics": sig.permutation_metrics,
            "nonsense_metrics": sig.nonsense_metrics,
        },
        "geometry_test": {
            "linear_accuracy": geo.linear_accuracy,
            "nonlinear_accuracy": geo.nonlinear_accuracy,
            "gap": geo.gap, "gap_threshold": gap_threshold,
            "diagnosis": geo.diagnosis,
        },
        "decomposition_test": {
            "n_concepts": dec.n_concepts, "silhouette_score": dec.silhouette_score,
            "min_silhouette": min_silhouette, "is_fragmented": dec.is_fragmented,
            "per_concept_sizes": dec.per_concept_sizes,
            "cluster_labels": dec.cluster_labels,
        },
        "intervention": {
            "recommended_method": inter.recommended_method,
            "confidence": inter.confidence,
            "reasoning": inter.reasoning,
            "method_scores": inter.method_scores,
        },
    }


# Aliases for backwards compatibility
run_repscan_protocol = run_full_protocol


@dataclass
class RepScanProtocolConfig:
    """Configuration for RepScan protocol."""
    signal_keys: List[str] = None
    p_threshold: float = 0.05
    gap_threshold: Optional[float] = None
    min_silhouette: Optional[float] = None

    def __post_init__(self):
        if self.signal_keys is None:
            self.signal_keys = ["knn_accuracy", "knn_pca_accuracy", "mlp_probe_accuracy"]
