"""
Steering method recommendation based on RepScan metrics.

Scores all 7 registered steering methods using the full set of computed
geometry metrics (~90 signals). The method scores are additive: each
metric check awards or penalizes relevant methods, and the highest
scorer wins. Confidence is derived from the margin between top two.
"""

import numpy as np
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class SteeringThresholds:
    """Configurable thresholds for steering recommendations."""
    linear_probe_high: float = 0.85
    linear_probe_low: float = 0.65
    nonlinearity_gap_significant: float = 0.05
    icd_high: float = 0.7
    icd_low: float = 0.3
    stability_high: float = 0.8
    stability_low: float = 0.5
    multi_concept_silhouette: float = 0.3
    alignment_high: float = 0.3
    alignment_low: float = 0.1
    variance_concentrated: float = 0.15
    effective_dims_low: float = 20
    multi_dir_gain_high: float = 0.05


def _get_metric(metrics: Dict[str, Any], keys: List[str]) -> Optional[float]:
    """Get metric value trying multiple possible keys."""
    for key in keys:
        if key in metrics and metrics[key] is not None:
            return float(metrics[key])
    return None


_LEARNED_CONFIG_PATH = "~/.wisent/learned_recommendation_config.json"


def compute_steering_recommendation(
    metrics: Dict[str, Any],
    thresholds: Optional[SteeringThresholds] = None,
) -> Dict[str, Any]:
    """Compute steering method recommendation from RepScan metrics.

    Scores all 7 methods: CAA, Hyperplane, MLP, PRISM, PULSE, TITAN, Concept Flow.
    If a learned config exists at ~/.wisent/learned_recommendation_config.json,
    delegates to compute_configurable_recommendation automatically.
    """
    from pathlib import Path
    learned = Path(_LEARNED_CONFIG_PATH).expanduser()
    if learned.exists():
        from .recommendation.config import RecommendationConfig
        from .recommendation.configurable import (
            compute_configurable_recommendation)
        cfg = RecommendationConfig.load(learned)
        return compute_configurable_recommendation(metrics, cfg)
    if thresholds is None:
        thresholds = SteeringThresholds()

    # Extract metrics
    linear_acc = _get_metric(metrics, ["linear_probe_accuracy", "linear_probe"])
    mlp_acc = _get_metric(metrics, ["mlp_probe_accuracy", "mlp_probe"])
    icd = _get_metric(metrics, ["icd_icd", "icd"])
    stability = _get_metric(metrics, ["direction_stability_score", "direction_stability"])
    alignment = _get_metric(metrics, ["steer_diff_mean_alignment", "diff_mean_alignment"])
    n_concepts = _get_metric(metrics, ["n_concepts"])
    coherence = _get_metric(metrics, ["concept_coherence"])
    consistency = _get_metric(metrics, ["consistency_consistency_score", "consistency_mean"])
    silhouette = _get_metric(metrics, ["best_silhouette"])
    variance_pc1 = _get_metric(metrics, ["manifold_variance_pc1"])
    dims_for_90 = _get_metric(metrics, ["manifold_dims_for_90pct"])
    multi_dir_gain = _get_metric(metrics, ["multi_dir_gain"])
    effective_dims = _get_metric(metrics, ["steer_effective_steering_dims"])
    icd_top5 = _get_metric(metrics, ["icd_top5_variance"])

    nonlinearity_gap = None
    if mlp_acc is not None and linear_acc is not None:
        nonlinearity_gap = mlp_acc - linear_acc

    raw_signals = {
        "linear_acc": linear_acc, "mlp_acc": mlp_acc,
        "nonlinearity_gap": nonlinearity_gap, "icd": icd,
        "stability": stability, "alignment": alignment,
        "n_concepts": n_concepts, "coherence": coherence,
        "consistency": consistency, "silhouette": silhouette,
        "variance_pc1": variance_pc1, "dims_for_90": dims_for_90,
        "multi_dir_gain": multi_dir_gain, "effective_dims": effective_dims,
    }

    scores = {
        "CAA": 0.0, "Hyperplane": 0.0, "MLP": 0.0, "PRISM": 0.0,
        "PULSE": 0.0, "TITAN": 0.0, "Concept Flow": 0.0,
    }
    reasoning = []

    # 1. Steering viability
    steering_viable = True
    if icd is not None and icd < thresholds.icd_low:
        reasoning.append(f"Low ICD ({icd:.3f}) suggests weak steering signal")
        steering_viable = False
    if alignment is not None and alignment < thresholds.alignment_low:
        reasoning.append(f"Low alignment ({alignment:.3f}) suggests inconsistent direction")

    # 2. Linear vs Nonlinear
    if linear_acc is not None:
        if linear_acc >= thresholds.linear_probe_high:
            reasoning.append(f"High linear accuracy ({linear_acc:.3f}) favors linear methods")
            scores["CAA"] += 2.0
            scores["Hyperplane"] += 2.0
            scores["Concept Flow"] += 1.0
        elif linear_acc < thresholds.linear_probe_low:
            reasoning.append(f"Low linear accuracy ({linear_acc:.3f}) suggests nonlinear structure")
            scores["MLP"] += 1.0
            scores["PULSE"] += 1.0
            scores["TITAN"] += 1.0
            scores["Concept Flow"] += 0.5

    if nonlinearity_gap is not None and nonlinearity_gap > thresholds.nonlinearity_gap_significant:
        reasoning.append(f"Nonlinearity gap ({nonlinearity_gap:.3f}) suggests MLP captures more")
        scores["MLP"] += 1.5
        scores["PULSE"] += 0.5
        scores["TITAN"] += 0.5
        scores["Concept Flow"] += 1.0

    # 3. Multiple concepts
    if n_concepts is not None and n_concepts > 1:
        if silhouette is not None and silhouette > thresholds.multi_concept_silhouette:
            reasoning.append(f"Multiple concepts (k={n_concepts}, sil={silhouette:.3f})")
            scores["PRISM"] += 2.0
            scores["TITAN"] += 1.0
            scores["Concept Flow"] += 1.5
            scores["CAA"] -= 1.0
            scores["Hyperplane"] -= 0.5

    # 4. Direction stability
    if stability is not None:
        if stability >= thresholds.stability_high:
            reasoning.append(f"High stability ({stability:.3f}) supports simple methods")
            scores["CAA"] += 1.0
            scores["Hyperplane"] += 0.5
            scores["Concept Flow"] += 0.5
        elif stability < thresholds.stability_low:
            reasoning.append(f"Low stability ({stability:.3f}) needs robust methods")
            scores["TITAN"] += 1.0
            scores["PULSE"] += 0.5
            scores["Concept Flow"] += 1.0
            scores["CAA"] -= 0.5

    # 5. ICD strength
    if icd is not None:
        if icd >= thresholds.icd_high:
            reasoning.append(f"High ICD ({icd:.3f}) indicates strong steering potential")
            scores["CAA"] += 1.0
            scores["Hyperplane"] += 0.5
            scores["Concept Flow"] += 0.5
        elif icd < thresholds.icd_low:
            scores["TITAN"] += 0.5
            scores["PULSE"] += 0.5

    # 6. Coherence
    if coherence is not None:
        if coherence > 0.8:
            reasoning.append(f"High coherence ({coherence:.3f}) supports single-direction")
            scores["CAA"] += 0.5
        elif coherence < 0.5:
            reasoning.append(f"Low coherence ({coherence:.3f}) suggests fragmented concept")
            scores["PRISM"] += 0.5
            scores["TITAN"] += 0.5
            scores["Concept Flow"] += 0.5

    # 7. Concept Flow specific: subspace structure
    if variance_pc1 is not None and variance_pc1 >= thresholds.variance_concentrated:
        reasoning.append(f"Concentrated variance (PC1={variance_pc1:.3f}) favors subspace methods")
        scores["Concept Flow"] += 1.0
    if icd_top5 is not None and icd_top5 >= 0.4:
        scores["Concept Flow"] += 0.5
    if multi_dir_gain is not None and multi_dir_gain >= thresholds.multi_dir_gain_high:
        reasoning.append(f"Multi-direction gain ({multi_dir_gain:.3f}) favors flow/multi-dir")
        scores["Concept Flow"] += 1.0
        scores["PRISM"] += 0.5
    if effective_dims is not None and effective_dims <= thresholds.effective_dims_low:
        scores["Concept Flow"] += 0.5

    # Normalize scores to be non-negative
    min_score = min(scores.values())
    if min_score < 0:
        scores = {k: v - min_score for k, v in scores.items()}

    best_method = max(scores, key=scores.get)
    best_score = scores[best_method]

    sorted_scores = sorted(scores.values(), reverse=True)
    if len(sorted_scores) > 1 and sorted_scores[0] > 0:
        margin = (sorted_scores[0] - sorted_scores[1]) / sorted_scores[0]
        confidence = min(0.5 + margin * 0.5, 1.0)
    else:
        confidence = 0.5

    if not steering_viable:
        confidence *= 0.5
        reasoning.append("Warning: steering may not be effective for this concept")

    if not reasoning:
        reasoning.append("Insufficient metrics for detailed analysis")
        best_method = "CAA"
        confidence = 0.3

    return {
        "recommended_method": best_method,
        "confidence": float(confidence),
        "reasoning": reasoning,
        "method_scores": scores,
        "raw_signals": raw_signals,
    }


def compute_per_layer_recommendation(
    per_layer_metrics: Dict[int, Dict[str, Any]],
    thresholds: Optional[SteeringThresholds] = None,
) -> Dict[str, Any]:
    """Compute recommendations for each layer and identify best layer."""
    if not per_layer_metrics:
        return {"error": "no layer metrics provided"}
    per_layer = {}
    layer_scores = {}
    for layer, metrics in per_layer_metrics.items():
        rec = compute_steering_recommendation(metrics, thresholds)
        per_layer[layer] = rec
        icd = rec["raw_signals"].get("icd")
        stability = rec["raw_signals"].get("stability")
        alignment = rec["raw_signals"].get("alignment")
        score = 0.0
        if icd is not None:
            score += icd * 2.0
        if stability is not None:
            score += stability
        if alignment is not None:
            score += alignment
        layer_scores[layer] = score
    best_layer = max(layer_scores, key=layer_scores.get)
    return {
        "per_layer": per_layer, "layer_scores": layer_scores,
        "best_layer": best_layer, "best_layer_recommendation": per_layer[best_layer],
    }


def get_method_description(method: str) -> str:
    """Get description of a steering method."""
    from wisent.core.steering_methods.registry import SteeringMethodRegistry
    name = method.lower().replace(" ", "_")
    if SteeringMethodRegistry.validate_method(name):
        return SteeringMethodRegistry.get(name).description
    return "Unknown method"


def get_method_requirements(method: str) -> Dict[str, Any]:
    """Get requirements/assumptions for a steering method."""
    from wisent.core.steering_methods.registry import SteeringMethodRegistry
    name = method.lower().replace(" ", "_")
    if not SteeringMethodRegistry.validate_method(name):
        return {}
    defn = SteeringMethodRegistry.get(name)
    return {
        "min_pairs": defn.optimization_config.get("min_pairs", 10),
        "default_strength": defn.default_strength,
        "strength_range": defn.strength_range,
        "parameters": [p.name for p in defn.parameters],
    }
