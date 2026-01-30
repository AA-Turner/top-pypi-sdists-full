"""
Main geometry runner that orchestrates all geometry analysis.

This module provides the main entry points for running geometry
analysis on activation representations.
"""

import os
os.environ["NUMBA_NUM_THREADS"] = "1"

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

import torch
import numpy as np

from .probe_metrics import (
    compute_signal_strength,
    compute_linear_probe_accuracy,
    compute_mlp_probe_accuracy,
    compute_knn_accuracy,
    compute_knn_pca_accuracy,
)
from .distribution_metrics import (
    compute_mmd_rbf,
    compute_density_ratio,
    compute_fisher_per_dimension,
)
from .intrinsic_dim import (
    compute_local_intrinsic_dims,
    compute_diff_intrinsic_dim,
)
from .direction_metrics import (
    compute_direction_stability,
    compute_multi_direction_accuracy,
    compute_pairwise_diff_consistency,
)
from .steerability import (
    compute_steerability_metrics,
    compute_linearity_score,
    compute_final_steering_prescription,
)
from .steering_recommendation import (
    compute_steering_recommendation,
)
from .icd import compute_icd
from .concept_analysis import (
    detect_multiple_concepts,
    compute_concept_coherence,
)
from .signal_analysis import (
    compute_signal_to_noise,
    compute_bootstrap_signal_estimate,
)
from .activation_structure import (
    compute_two_cloud_relationship,
    compute_relative_position,
    compute_cluster_structure,
)
from .representation_metrics import (
    compute_magnitude_metrics,
    compute_sparsity_metrics,
    compute_pair_quality_metrics,
    compute_manifold_metrics,
    compute_noise_baseline_comparison,
)
from .nonsense_baseline import (
    analyze_with_nonsense_baseline,
)
from .transformer_analysis import (
    compare_components_for_benchmark,
)
from .visualizations import (
    plot_pca_projection,
    plot_diff_vectors,
    plot_alignment_distribution,
    plot_eigenvalue_spectrum,
    plot_tsne_projection,
    plot_umap_projection,
    plot_pacmap_projection,
    plot_norm_distribution,
    plot_pairwise_distances,
    create_summary_figure,
    render_matplotlib_figure,
)


def compute_geometry_metrics(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
    n_folds: int = 5,
    model=None,
    tokenizer=None,
    layer: Optional[int] = None,
    device: str = "cuda",
    pos_activations_by_component: Optional[Dict[str, torch.Tensor]] = None,
    neg_activations_by_component: Optional[Dict[str, torch.Tensor]] = None,
    generate_visualizations: bool = False,
) -> Dict[str, Any]:
    """
    Compute comprehensive geometry metrics for activations.

    Args:
        pos_activations: [N, hidden_dim] positive class activations
        neg_activations: [N, hidden_dim] negative class activations
        n_folds: Number of CV folds
        model: Optional model for nonsense baseline generation
        tokenizer: Optional tokenizer for nonsense baseline generation
        layer: Optional layer index for nonsense baseline
        device: Device for model inference
        pos_activations_by_component: Optional dict mapping component name -> pos activations
        neg_activations_by_component: Optional dict mapping component name -> neg activations
        generate_visualizations: Whether to generate and include visualization figures

    Returns:
        Dict with all computed metrics
    """
    metrics = {}
    
    # Basic probe metrics
    metrics["signal_strength"] = compute_signal_strength(pos_activations, neg_activations, n_folds)
    metrics["linear_probe_accuracy"] = compute_linear_probe_accuracy(pos_activations, neg_activations, n_folds)
    metrics["mlp_probe_accuracy"] = compute_mlp_probe_accuracy(pos_activations, neg_activations, n_folds=n_folds)
    
    # ICD
    icd_result = compute_icd(pos_activations, neg_activations)
    metrics.update({f"icd_{k}": v for k, v in icd_result.items()})
    
    # Direction metrics
    stability = compute_direction_stability(pos_activations, neg_activations)
    metrics.update({f"direction_{k}": v for k, v in stability.items()})
    
    consistency = compute_pairwise_diff_consistency(pos_activations, neg_activations)
    metrics.update({f"consistency_{k}": v for k, v in consistency.items()})
    
    # Steerability
    steerability = compute_steerability_metrics(pos_activations, neg_activations)
    metrics.update({f"steer_{k}": v for k, v in steerability.items()})
    
    # Concept analysis
    metrics["concept_coherence"] = compute_concept_coherence(pos_activations, neg_activations)
    concept_detection = detect_multiple_concepts(pos_activations, neg_activations)
    metrics["n_concepts"] = concept_detection.get("n_concepts", 1)
    metrics["best_silhouette"] = concept_detection.get("best_silhouette", 0)

    # Magnitude metrics
    magnitude = compute_magnitude_metrics(pos_activations, neg_activations)
    metrics.update({f"magnitude_{k}": v for k, v in magnitude.items()})

    # Pair quality metrics
    pair_quality = compute_pair_quality_metrics(pos_activations, neg_activations)
    if "error" not in pair_quality:
        metrics["pair_alignment_mean"] = pair_quality.get("alignment_mean")
        metrics["pair_alignment_std"] = pair_quality.get("alignment_std")
        metrics["pair_outlier_fraction"] = pair_quality.get("outlier_fraction")
        metrics["pair_high_quality_fraction"] = pair_quality.get("high_quality_fraction")

    # Two-cloud relationship
    relationship = compute_two_cloud_relationship(pos_activations, neg_activations)
    if "error" not in relationship:
        metrics["cloud_centroid_distance"] = relationship.get("centroid_distance")
        metrics["cloud_separation_ratio"] = relationship.get("separation_ratio")
        metrics["cloud_pos_overlap"] = relationship.get("pos_overlap_fraction")
        metrics["cloud_neg_overlap"] = relationship.get("neg_overlap_fraction")
        metrics["cloud_pc1_alignment"] = relationship.get("pc1_alignment")

    # Relative position (translation analysis)
    rel_position = compute_relative_position(pos_activations, neg_activations)
    metrics["shift_explains_fraction"] = rel_position.get("shift_explains_fraction")
    metrics["translation_consistency"] = rel_position.get("translation_consistency")

    # All metrics are always computed
    # Distribution metrics
    metrics["mmd_rbf"] = compute_mmd_rbf(pos_activations, neg_activations)
    metrics["density_ratio"] = compute_density_ratio(pos_activations, neg_activations)
    
    fisher = compute_fisher_per_dimension(pos_activations, neg_activations)
    metrics.update({f"fisher_{k}": v for k, v in fisher.items()})
    
    # Intrinsic dim
    dim_pos, dim_neg, dim_ratio = compute_local_intrinsic_dims(pos_activations, neg_activations)
    metrics["intrinsic_dim_pos"] = dim_pos
    metrics["intrinsic_dim_neg"] = dim_neg
    metrics["intrinsic_dim_ratio"] = dim_ratio
    
    # Multi-direction
    multi_dir = compute_multi_direction_accuracy(pos_activations, neg_activations)
    metrics["multi_dir_saturation_k"] = multi_dir.get("saturation_k", 1)
    metrics["multi_dir_gain"] = multi_dir.get("gain_from_multi", 0.0)
    
    # k-NN
    metrics["knn_accuracy"] = compute_knn_accuracy(pos_activations, neg_activations)
    metrics["knn_pca_accuracy"] = compute_knn_pca_accuracy(pos_activations, neg_activations)
    
    # Signal to noise
    metrics["signal_to_noise"] = compute_signal_to_noise(pos_activations, neg_activations)

    # Sparsity metrics
    sparsity = compute_sparsity_metrics(pos_activations, neg_activations)
    metrics["sparsity_neurons_for_50pct"] = sparsity.get("neurons_for_50pct")
    metrics["sparsity_neurons_for_90pct"] = sparsity.get("neurons_for_90pct")
    metrics["sparsity_diff_gini"] = sparsity.get("diff_gini")
    metrics["sparsity_top_10_contribution"] = sparsity.get("top_10_contribution_fraction")

    # Manifold metrics (curvature, linearity)
    manifold = compute_manifold_metrics(pos_activations, neg_activations)
    metrics["manifold_variance_pc1"] = manifold.get("variance_pc1")
    metrics["manifold_dims_for_90pct"] = manifold.get("dims_for_90pct_variance")
    metrics["manifold_participation_ratio"] = manifold.get("participation_ratio")
    metrics["manifold_local_linearity"] = manifold.get("local_linearity_mean")
    metrics["manifold_curvature"] = manifold.get("curvature_proxy")

    # Cluster structure
    pos_clusters = compute_cluster_structure(pos_activations)
    neg_clusters = compute_cluster_structure(neg_activations)
    if "error" not in pos_clusters:
        metrics["pos_best_k_clusters"] = pos_clusters.get("best_k")
        metrics["pos_best_silhouette"] = pos_clusters.get("best_silhouette")
    if "error" not in neg_clusters:
        metrics["neg_best_k_clusters"] = neg_clusters.get("best_k")
        metrics["neg_best_silhouette"] = neg_clusters.get("best_silhouette")

    # Noise baseline comparison
    noise_comparison = compute_noise_baseline_comparison(pos_activations, neg_activations)
    if "error" not in noise_comparison:
        vs_noise = noise_comparison.get("vs_noise", {})
        metrics["noise_alignment_above_baseline"] = vs_noise.get("alignment_mean")
        metrics["noise_linear_probe_above_baseline"] = vs_noise.get("linear_probe")
        stds_above = noise_comparison.get("stds_above_noise", {})
        metrics["noise_alignment_z_score"] = stds_above.get("alignment_mean")
        metrics["noise_linear_z_score"] = stds_above.get("linear_probe")

    # Nonsense baseline (requires model/tokenizer)
    if model is not None and tokenizer is not None:
        nonsense_result = analyze_with_nonsense_baseline(
            pos_activations, neg_activations,
            model=model, tokenizer=tokenizer,
            layer=layer, device=device,
        )
        if "error" not in nonsense_result:
            metrics["nonsense_baseline"] = nonsense_result
            if nonsense_result.get("z_scores"):
                metrics["nonsense_linear_z"] = nonsense_result["z_scores"].get("linear_probe_z")
                metrics["nonsense_signal_z"] = nonsense_result["z_scores"].get("signal_strength_z")
            metrics["is_real_signal"] = nonsense_result.get("is_real_signal", False)

    # Transformer component analysis (requires per-component activations)
    if pos_activations_by_component is not None and neg_activations_by_component is not None:
        component_result = compare_components_for_benchmark(
            model, tokenizer,
            pos_activations_by_component,
            neg_activations_by_component,
        )
        metrics["component_analysis"] = component_result
        if "best_component" in component_result:
            metrics["best_component"] = component_result["best_component"]

    # Visualizations
    if generate_visualizations:
        visualizations = {}

        # PCA projection
        try:
            pca_data = plot_pca_projection(pos_activations, neg_activations)
            visualizations["pca_projection"] = render_matplotlib_figure(pca_data)
        except Exception:
            pass

        # t-SNE projection
        try:
            tsne_data = plot_tsne_projection(pos_activations, neg_activations)
            if "error" not in tsne_data:
                visualizations["tsne_projection"] = render_matplotlib_figure(tsne_data)
        except Exception:
            pass

        # UMAP projection
        try:
            umap_data = plot_umap_projection(pos_activations, neg_activations)
            if "error" not in umap_data:
                visualizations["umap_projection"] = render_matplotlib_figure(umap_data)
        except Exception:
            pass

        # PaCMAP projection
        try:
            pacmap_data = plot_pacmap_projection(pos_activations, neg_activations)
            if "error" not in pacmap_data:
                visualizations["pacmap_projection"] = render_matplotlib_figure(pacmap_data)
        except Exception:
            pass

        # Diff vectors
        try:
            diff_data = plot_diff_vectors(pos_activations, neg_activations)
            visualizations["diff_vectors"] = render_matplotlib_figure(diff_data)
        except Exception:
            pass

        # Alignment distribution
        try:
            align_data = plot_alignment_distribution(pos_activations, neg_activations)
            visualizations["alignment_distribution"] = render_matplotlib_figure(align_data)
        except Exception:
            pass

        # Eigenvalue spectrum
        try:
            eigen_data = plot_eigenvalue_spectrum(pos_activations, neg_activations)
            visualizations["eigenvalue_spectrum"] = render_matplotlib_figure(eigen_data)
        except Exception:
            pass

        # Norm distribution
        try:
            norm_data = plot_norm_distribution(pos_activations, neg_activations)
            visualizations["norm_distribution"] = render_matplotlib_figure(norm_data)
        except Exception:
            pass

        # Pairwise distances
        try:
            dist_data = plot_pairwise_distances(pos_activations, neg_activations)
            visualizations["pairwise_distances"] = render_matplotlib_figure(dist_data)
        except Exception:
            pass

        # Summary figure (returns base64 directly)
        try:
            visualizations["summary"] = create_summary_figure(pos_activations, neg_activations, metrics)
        except Exception:
            pass

        if visualizations:
            metrics["visualizations"] = visualizations

    # Generate recommendation
    recommendation = compute_steering_recommendation(metrics)
    metrics["recommended_method"] = recommendation.get("recommended_method", "CAA")
    metrics["recommendation_confidence"] = recommendation.get("confidence", 0.5)
    metrics["recommendation_reasoning"] = recommendation.get("reasoning", [])
    metrics["method_scores"] = recommendation.get("method_scores", {})

    return metrics


def run_full_repscan(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
    layer: int,
    benchmark_name: str = "unknown",
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run full representation scan for a single layer.
    
    Args:
        pos_activations: Positive class activations
        neg_activations: Negative class activations
        layer: Layer number
        benchmark_name: Name of benchmark
        output_dir: Optional directory to save results
        
    Returns:
        Dict with all metrics and recommendations
    """
    start_time = time.time()
    
    metrics = compute_geometry_metrics(pos_activations, neg_activations)
    
    result = {
        "benchmark": benchmark_name,
        "layer": layer,
        "n_pos": len(pos_activations),
        "n_neg": len(neg_activations),
        "metrics": metrics,
        "runtime_seconds": time.time() - start_time,
    }
    
    if output_dir:
        output_path = Path(output_dir) / f"{benchmark_name}_layer{layer}_repscan.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
    
    return result


def run_full_repscan_with_layer_search(
    activations_by_layer: Dict[int, Tuple[torch.Tensor, torch.Tensor]],
    benchmark_name: str = "unknown",
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run repscan across multiple layers.

    Args:
        activations_by_layer: Dict mapping layer -> (pos, neg) activations
        benchmark_name: Name of benchmark
        output_dir: Optional directory to save results

    Returns:
        Dict with per-layer raw metrics. No recommendations or "best" layer selection.
    """
    results_by_layer = {}
    per_layer_metrics = {}

    for layer, (pos, neg) in activations_by_layer.items():
        result = run_full_repscan(pos, neg, layer, benchmark_name)
        results_by_layer[layer] = result
        per_layer_metrics[layer] = result["metrics"]

    # Extract raw metrics per layer
    prescription = compute_final_steering_prescription(per_layer_metrics)

    summary = {
        "benchmark": benchmark_name,
        "per_layer_metrics": prescription.get("per_layer", {}),
        "results_by_layer": results_by_layer,
    }

    if output_dir:
        output_path = Path(output_dir) / f"{benchmark_name}_layer_search.json"
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

    return summary


def run_full_repscan_with_steering_eval(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
    model,
    tokenizer,
    test_prompts: List[str],
    layer: int,
    benchmark_name: str = "unknown",
) -> Dict[str, Any]:
    """
    Run repscan and evaluate actual steering effectiveness.
    
    This combines geometry analysis with actual steering tests.
    """
    # Run geometry analysis
    metrics = compute_geometry_metrics(pos_activations, neg_activations)
    
    # Compute steering direction
    n = min(len(pos_activations), len(neg_activations))
    steering_direction = (pos_activations[:n] - neg_activations[:n]).mean(dim=0)
    
    result = {
        "benchmark": benchmark_name,
        "layer": layer,
        "metrics": metrics,
        "steering_direction_norm": float(torch.norm(steering_direction)),
        "n_test_prompts": len(test_prompts),
    }
    
    return result


def evaluate_steering_effectiveness(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
    model=None,
    tokenizer=None,
    test_pairs: List[Tuple[str, str]] = None,
) -> Dict[str, Any]:
    """
    Return raw metrics relevant to steering effectiveness.

    Does NOT predict effectiveness - just returns the raw metrics.
    """
    metrics = compute_geometry_metrics(pos_activations, neg_activations)

    return {
        "caa_probe_alignment": metrics.get("steer_caa_probe_alignment"),
        "diff_mean_alignment": metrics.get("steer_diff_mean_alignment"),
        "linear_accuracy": metrics.get("linear_probe_accuracy"),
        "icd": metrics.get("icd_icd"),
    }


def evaluate_activation_regions(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
) -> Dict[str, Any]:
    """
    Analyze different regions of activation space.
    
    Checks if pos/neg form distinct clusters or overlap.
    """
    try:
        from sklearn.mixture import GaussianMixture
        
        pos = pos_activations.float().cpu().numpy()
        neg = neg_activations.float().cpu().numpy()
        
        # Fit GMM to combined data
        X = np.vstack([pos, neg])
        gmm = GaussianMixture(n_components=2, random_state=42)
        gmm.fit(X)
        
        # Predict cluster assignments
        pos_clusters = gmm.predict(pos)
        neg_clusters = gmm.predict(neg)
        
        # Check separation
        pos_majority = int(np.median(pos_clusters))
        neg_majority = int(np.median(neg_clusters))
        
        separation = float((pos_clusters == pos_majority).mean() * (neg_clusters == neg_majority).mean())
        
        return {
            "gmm_separation": separation,
            "pos_cluster_purity": float((pos_clusters == pos_majority).mean()),
            "neg_cluster_purity": float((neg_clusters == neg_majority).mean()),
            "clusters_are_separated": pos_majority != neg_majority,
        }
    except Exception:
        return {
            "gmm_separation": 0.5,
            "pos_cluster_purity": 0.5,
            "neg_cluster_purity": 0.5,
            "clusters_are_separated": False,
        }
