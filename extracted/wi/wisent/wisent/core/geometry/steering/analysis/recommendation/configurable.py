"""Configurable recommendation scoring function.

Mirrors compute_steering_recommendation but reads every literal from a
RecommendationConfig instance.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from .config import RecommendationConfig, METHODS


def _get(metrics: Dict[str, Any], keys: List[str]) -> Optional[float]:
    for key in keys:
        if key in metrics and metrics[key] is not None:
            return float(metrics[key])
    return None


def compute_configurable_recommendation(
    metrics: Dict[str, Any],
    cfg: RecommendationConfig,
) -> Dict[str, Any]:
    """Score all 7 methods using configurable thresholds and weights."""
    t = cfg.thresholds
    w = cfg.weights

    linear_acc = _get(metrics, ["linear_probe_accuracy", "linear_probe"])
    mlp_acc = _get(metrics, ["mlp_probe_accuracy", "mlp_probe"])
    icd = _get(metrics, ["icd_icd", "icd"])
    stability = _get(metrics, [
        "direction_stability_score", "direction_stability"])
    alignment = _get(metrics, [
        "steer_diff_mean_alignment", "diff_mean_alignment"])
    n_concepts = _get(metrics, ["n_concepts"])
    coherence = _get(metrics, ["concept_coherence"])
    silhouette = _get(metrics, ["best_silhouette"])
    variance_pc1 = _get(metrics, ["manifold_variance_pc1"])
    icd_top5 = _get(metrics, ["icd_top5_variance"])
    multi_dir_gain = _get(metrics, ["multi_dir_gain"])
    effective_dims = _get(metrics, ["steer_effective_steering_dims"])

    nonlinearity_gap = None
    if mlp_acc is not None and linear_acc is not None:
        nonlinearity_gap = mlp_acc - linear_acc

    raw_signals = {
        "linear_acc": linear_acc, "mlp_acc": mlp_acc,
        "nonlinearity_gap": nonlinearity_gap, "icd": icd,
        "stability": stability, "alignment": alignment,
        "n_concepts": n_concepts, "coherence": coherence,
        "silhouette": silhouette, "variance_pc1": variance_pc1,
        "multi_dir_gain": multi_dir_gain,
        "effective_dims": effective_dims,
    }

    scores: Dict[str, float] = {m: 0.0 for m in METHODS}
    reasoning: List[str] = []

    # 1. Viability
    steering_viable = True
    if icd is not None and icd < t.icd_low:
        reasoning.append(
            f"Low ICD ({icd:.3f}) suggests weak steering signal")
        steering_viable = False
    if alignment is not None and alignment < t.alignment_low:
        reasoning.append(
            f"Low alignment ({alignment:.3f}) suggests inconsistent "
            "direction")

    # 2. Linear vs Nonlinear
    if linear_acc is not None:
        if linear_acc >= t.linear_probe_high:
            reasoning.append(
                f"High linear accuracy ({linear_acc:.3f})")
            scores["CAA"] += w.linear_high_caa
            scores["Hyperplane"] += w.linear_high_hyperplane
            scores["Concept Flow"] += w.linear_high_cf
        elif linear_acc < t.linear_probe_low:
            reasoning.append(
                f"Low linear accuracy ({linear_acc:.3f})")
            scores["MLP"] += w.linear_low_mlp
            scores["PULSE"] += w.linear_low_pulse
            scores["TITAN"] += w.linear_low_titan
            scores["Concept Flow"] += w.linear_low_cf
    if (nonlinearity_gap is not None
            and nonlinearity_gap > t.nonlinearity_gap_significant):
        reasoning.append(
            f"Nonlinearity gap ({nonlinearity_gap:.3f})")
        scores["MLP"] += w.nonlin_gap_mlp
        scores["PULSE"] += w.nonlin_gap_pulse
        scores["TITAN"] += w.nonlin_gap_titan
        scores["Concept Flow"] += w.nonlin_gap_cf

    # 3. Multiple concepts
    if n_concepts is not None and n_concepts > 1:
        if (silhouette is not None
                and silhouette > t.multi_concept_silhouette):
            reasoning.append(
                f"Multi concepts (k={n_concepts}, "
                f"sil={silhouette:.3f})")
            scores["PRISM"] += w.multi_concept_prism
            scores["TITAN"] += w.multi_concept_titan
            scores["Concept Flow"] += w.multi_concept_cf
            scores["CAA"] += w.multi_concept_caa
            scores["Hyperplane"] += w.multi_concept_hyperplane

    # 4. Direction stability
    if stability is not None:
        if stability >= t.stability_high:
            reasoning.append(f"High stability ({stability:.3f})")
            scores["CAA"] += w.stab_high_caa
            scores["Hyperplane"] += w.stab_high_hyperplane
            scores["Concept Flow"] += w.stab_high_cf
        elif stability < t.stability_low:
            reasoning.append(f"Low stability ({stability:.3f})")
            scores["TITAN"] += w.stab_low_titan
            scores["PULSE"] += w.stab_low_pulse
            scores["Concept Flow"] += w.stab_low_cf
            scores["CAA"] += w.stab_low_caa

    # 5. ICD strength
    if icd is not None:
        if icd >= t.icd_high:
            reasoning.append(f"High ICD ({icd:.3f})")
            scores["CAA"] += w.icd_high_caa
            scores["Hyperplane"] += w.icd_high_hyperplane
            scores["Concept Flow"] += w.icd_high_cf
        elif icd < t.icd_low:
            scores["TITAN"] += w.icd_low_titan
            scores["PULSE"] += w.icd_low_pulse

    # 6. Coherence
    if coherence is not None:
        if coherence > t.coherence_high:
            reasoning.append(f"High coherence ({coherence:.3f})")
            scores["CAA"] += w.coh_high_caa
        elif coherence < t.coherence_low:
            reasoning.append(f"Low coherence ({coherence:.3f})")
            scores["PRISM"] += w.coh_low_prism
            scores["TITAN"] += w.coh_low_titan
            scores["Concept Flow"] += w.coh_low_cf

    # 7. Concept Flow specifics
    if (variance_pc1 is not None
            and variance_pc1 >= t.variance_concentrated):
        reasoning.append(f"Concentrated variance ({variance_pc1:.3f})")
        scores["Concept Flow"] += w.var_pc1_cf
    if icd_top5 is not None and icd_top5 >= t.icd_top5_threshold:
        scores["Concept Flow"] += w.icd_top5_cf
    if (multi_dir_gain is not None
            and multi_dir_gain >= t.multi_dir_gain_high):
        reasoning.append(f"Multi-dir gain ({multi_dir_gain:.3f})")
        scores["Concept Flow"] += w.mdir_gain_cf
        scores["PRISM"] += w.mdir_gain_prism
    if (effective_dims is not None
            and effective_dims <= t.effective_dims_low):
        scores["Concept Flow"] += w.eff_dims_cf

    # Normalize and pick
    min_score = min(scores.values())
    if min_score < 0:
        scores = {k: v - min_score for k, v in scores.items()}
    best_method = max(scores, key=scores.get)
    sorted_scores = sorted(scores.values(), reverse=True)
    if len(sorted_scores) > 1 and sorted_scores[0] > 0:
        margin = ((sorted_scores[0] - sorted_scores[1])
                  / sorted_scores[0])
        confidence = min(w.confidence_base + margin * 0.5, 1.0)
    else:
        confidence = w.confidence_base
    if not steering_viable:
        confidence *= w.not_viable_scale
        reasoning.append(
            "Warning: steering may not be effective")
    if not reasoning:
        reasoning.append("Insufficient metrics")
        best_method = "CAA"
        confidence = 0.3
    return {
        "recommended_method": best_method,
        "confidence": float(confidence),
        "reasoning": reasoning,
        "method_scores": scores,
        "raw_signals": raw_signals,
    }
