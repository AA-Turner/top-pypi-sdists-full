"""
Additional representation metrics for describing activation geometry.

These metrics provide detailed descriptions of representation structure
without making recommendations or using arbitrary thresholds.
"""

import torch
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from scipy import stats


def compute_magnitude_metrics(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
) -> Dict[str, Any]:
    """
    Compute magnitude and scale metrics.

    Describes:
    - Actual norms of activations
    - How steering vector norm compares to activation norms
    - Distribution of norms
    """
    pos = pos_activations.float().cpu().numpy()
    neg = neg_activations.float().cpu().numpy()

    n = min(len(pos), len(neg))
    pos, neg = pos[:n], neg[:n]

    # Activation norms
    pos_norms = np.linalg.norm(pos, axis=1)
    neg_norms = np.linalg.norm(neg, axis=1)
    all_norms = np.concatenate([pos_norms, neg_norms])

    # Diff vectors
    diffs = pos - neg
    diff_norms = np.linalg.norm(diffs, axis=1)

    # Mean diff (steering vector)
    mean_diff = diffs.mean(axis=0)
    steering_norm = np.linalg.norm(mean_diff)

    return {
        # Activation norms
        "pos_norm_mean": float(pos_norms.mean()),
        "pos_norm_std": float(pos_norms.std()),
        "neg_norm_mean": float(neg_norms.mean()),
        "neg_norm_std": float(neg_norms.std()),
        "all_norm_mean": float(all_norms.mean()),
        "all_norm_std": float(all_norms.std()),

        # Diff norms
        "diff_norm_mean": float(diff_norms.mean()),
        "diff_norm_std": float(diff_norms.std()),
        "diff_norm_min": float(diff_norms.min()),
        "diff_norm_max": float(diff_norms.max()),

        # Steering vector
        "steering_vector_norm": float(steering_norm),
        "steering_to_activation_ratio": float(steering_norm / (all_norms.mean() + 1e-8)),
        "steering_to_diff_ratio": float(steering_norm / (diff_norms.mean() + 1e-8)),
    }


def compute_sparsity_metrics(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
    threshold_fraction: float = 0.01,
) -> Dict[str, Any]:
    """
    Compute sparsity and neuron activation patterns.

    Describes:
    - How sparse are the activations
    - Which neurons are most active
    - How concentrated is the signal
    """
    pos = pos_activations.float().cpu().numpy()
    neg = neg_activations.float().cpu().numpy()

    n = min(len(pos), len(neg))
    pos, neg = pos[:n], neg[:n]
    diffs = pos - neg

    hidden_dim = pos.shape[1]

    # Absolute activation analysis
    pos_abs = np.abs(pos)
    neg_abs = np.abs(neg)
    diff_abs = np.abs(diffs)

    # Threshold for "active" neuron (fraction of max)
    pos_threshold = pos_abs.max() * threshold_fraction
    neg_threshold = neg_abs.max() * threshold_fraction
    diff_threshold = diff_abs.max() * threshold_fraction

    # Sparsity: fraction of neurons below threshold
    pos_sparsity = (pos_abs < pos_threshold).mean()
    neg_sparsity = (neg_abs < neg_threshold).mean()
    diff_sparsity = (diff_abs < diff_threshold).mean()

    # Gini coefficient (measure of inequality/concentration)
    def gini(x):
        x = np.abs(x).flatten()
        x = np.sort(x)
        n = len(x)
        cumsum = np.cumsum(x)
        return (2 * np.sum((np.arange(1, n+1) * x)) - (n + 1) * cumsum[-1]) / (n * cumsum[-1] + 1e-8)

    # Per-neuron contribution to steering direction
    mean_diff = diffs.mean(axis=0)
    neuron_contributions = np.abs(mean_diff)
    sorted_contributions = np.sort(neuron_contributions)[::-1]
    cumsum_contributions = np.cumsum(sorted_contributions) / (sorted_contributions.sum() + 1e-8)

    # How many neurons needed for X% of signal
    neurons_for_50 = int(np.searchsorted(cumsum_contributions, 0.5) + 1)
    neurons_for_90 = int(np.searchsorted(cumsum_contributions, 0.9) + 1)
    neurons_for_99 = int(np.searchsorted(cumsum_contributions, 0.99) + 1)

    # Top neuron indices (most important for steering)
    top_neuron_indices = np.argsort(neuron_contributions)[::-1][:20].tolist()
    top_neuron_contributions = neuron_contributions[top_neuron_indices].tolist()

    return {
        # Sparsity
        "pos_sparsity": float(pos_sparsity),
        "neg_sparsity": float(neg_sparsity),
        "diff_sparsity": float(diff_sparsity),

        # Concentration (Gini)
        "pos_gini": float(gini(pos.mean(axis=0))),
        "neg_gini": float(gini(neg.mean(axis=0))),
        "diff_gini": float(gini(mean_diff)),

        # Neurons needed for signal
        "neurons_for_50pct": neurons_for_50,
        "neurons_for_90pct": neurons_for_90,
        "neurons_for_99pct": neurons_for_99,
        "neurons_for_50pct_fraction": neurons_for_50 / hidden_dim,
        "neurons_for_90pct_fraction": neurons_for_90 / hidden_dim,

        # Top neurons
        "top_20_neuron_indices": top_neuron_indices,
        "top_20_neuron_contributions": top_neuron_contributions,
        "top_10_contribution_fraction": float(sorted_contributions[:10].sum() / (sorted_contributions.sum() + 1e-8)),
    }


def compute_pair_quality_metrics(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
) -> Dict[str, Any]:
    """
    Compute per-pair quality metrics.

    Describes:
    - Which pairs are consistent with the mean direction
    - Which pairs are outliers
    - Distribution of pair qualities
    """
    pos = pos_activations.float().cpu().numpy()
    neg = neg_activations.float().cpu().numpy()

    n = min(len(pos), len(neg))
    pos, neg = pos[:n], neg[:n]
    diffs = pos - neg

    # Mean direction
    mean_diff = diffs.mean(axis=0)
    mean_diff_norm = np.linalg.norm(mean_diff)

    if mean_diff_norm < 1e-8:
        return {"error": "mean_diff_norm too small"}

    mean_diff_normalized = mean_diff / mean_diff_norm

    # Per-pair alignment with mean direction
    diff_norms = np.linalg.norm(diffs, axis=1)
    valid_mask = diff_norms > 1e-8

    alignments = np.zeros(n)
    alignments[valid_mask] = (diffs[valid_mask] / diff_norms[valid_mask, np.newaxis]) @ mean_diff_normalized

    # Per-pair contribution to mean (how much this pair "agrees")
    contributions = diffs @ mean_diff_normalized

    # Identify outliers (pairs that point opposite direction)
    outlier_mask = alignments < 0
    outlier_indices = np.where(outlier_mask)[0].tolist()

    # Identify high-quality pairs (high alignment, reasonable norm)
    high_quality_mask = (alignments > 0.5) & (diff_norms > np.percentile(diff_norms, 25))
    high_quality_indices = np.where(high_quality_mask)[0].tolist()

    # Leave-one-out stability: how much does direction change without each pair
    loo_angles = []
    for i in range(min(n, 100)):  # Limit to 100 for speed
        mask = np.ones(n, dtype=bool)
        mask[i] = False
        loo_mean = diffs[mask].mean(axis=0)
        loo_norm = np.linalg.norm(loo_mean)
        if loo_norm > 1e-8:
            loo_normalized = loo_mean / loo_norm
            angle = np.arccos(np.clip(np.dot(mean_diff_normalized, loo_normalized), -1, 1))
            loo_angles.append(np.degrees(angle))

    loo_angles = np.array(loo_angles)

    return {
        # Alignment distribution
        "alignment_mean": float(alignments.mean()),
        "alignment_std": float(alignments.std()),
        "alignment_min": float(alignments.min()),
        "alignment_max": float(alignments.max()),
        "alignment_median": float(np.median(alignments)),

        # Percentiles
        "alignment_p10": float(np.percentile(alignments, 10)),
        "alignment_p25": float(np.percentile(alignments, 25)),
        "alignment_p75": float(np.percentile(alignments, 75)),
        "alignment_p90": float(np.percentile(alignments, 90)),

        # Outliers
        "n_outliers": int(outlier_mask.sum()),
        "outlier_fraction": float(outlier_mask.mean()),
        "outlier_indices": outlier_indices[:20],  # First 20

        # High quality
        "n_high_quality": int(high_quality_mask.sum()),
        "high_quality_fraction": float(high_quality_mask.mean()),
        "high_quality_indices": high_quality_indices[:20],

        # Leave-one-out stability
        "loo_angle_mean": float(loo_angles.mean()) if len(loo_angles) > 0 else None,
        "loo_angle_std": float(loo_angles.std()) if len(loo_angles) > 0 else None,
        "loo_angle_max": float(loo_angles.max()) if len(loo_angles) > 0 else None,

        # Per-pair alignments (for detailed analysis)
        "per_pair_alignments": alignments.tolist(),
    }


def compute_cross_layer_consistency(
    activations_by_layer: Dict[int, Tuple[torch.Tensor, torch.Tensor]],
) -> Dict[str, Any]:
    """
    Compute consistency of steering direction across layers.

    Describes:
    - Do different layers have similar steering directions?
    - Which layers agree/disagree?
    - Is there a consistent "concept" across layers?
    """
    layers = sorted(activations_by_layer.keys())

    if len(layers) < 2:
        return {"error": "need at least 2 layers"}

    # Compute steering direction for each layer
    directions = {}
    for layer in layers:
        pos, neg = activations_by_layer[layer]
        pos = pos.float().cpu().numpy()
        neg = neg.float().cpu().numpy()
        n = min(len(pos), len(neg))

        mean_diff = (pos[:n] - neg[:n]).mean(axis=0)
        norm = np.linalg.norm(mean_diff)

        if norm > 1e-8:
            directions[layer] = mean_diff / norm
        else:
            directions[layer] = None

    # Compute pairwise cosine similarities between layers
    layer_pairs = []
    similarities = []

    for i, l1 in enumerate(layers):
        for l2 in layers[i+1:]:
            if directions[l1] is not None and directions[l2] is not None:
                # Project to common dimension if needed
                d1, d2 = directions[l1], directions[l2]
                if len(d1) == len(d2):
                    sim = float(np.dot(d1, d2))
                    layer_pairs.append((l1, l2))
                    similarities.append(sim)

    similarities = np.array(similarities)

    # Find most/least consistent layer pairs
    if len(similarities) > 0:
        most_similar_idx = np.argmax(similarities)
        least_similar_idx = np.argmin(similarities)

        # Per-layer consistency (average similarity with other layers)
        per_layer_consistency = {}
        for layer in layers:
            if directions[layer] is not None:
                layer_sims = []
                for other in layers:
                    if other != layer and directions[other] is not None:
                        d1, d2 = directions[layer], directions[other]
                        if len(d1) == len(d2):
                            layer_sims.append(np.dot(d1, d2))
                if layer_sims:
                    per_layer_consistency[layer] = float(np.mean(layer_sims))
    else:
        most_similar_idx = None
        least_similar_idx = None
        per_layer_consistency = {}

    return {
        "n_layers": len(layers),
        "layers": layers,

        # Overall consistency
        "mean_cross_layer_similarity": float(similarities.mean()) if len(similarities) > 0 else None,
        "std_cross_layer_similarity": float(similarities.std()) if len(similarities) > 0 else None,
        "min_cross_layer_similarity": float(similarities.min()) if len(similarities) > 0 else None,
        "max_cross_layer_similarity": float(similarities.max()) if len(similarities) > 0 else None,

        # Most/least similar pairs
        "most_similar_pair": layer_pairs[most_similar_idx] if most_similar_idx is not None else None,
        "most_similar_value": float(similarities[most_similar_idx]) if most_similar_idx is not None else None,
        "least_similar_pair": layer_pairs[least_similar_idx] if least_similar_idx is not None else None,
        "least_similar_value": float(similarities[least_similar_idx]) if least_similar_idx is not None else None,

        # Per-layer
        "per_layer_consistency": per_layer_consistency,

        # All pairwise similarities
        "pairwise_similarities": {f"{p[0]}-{p[1]}": float(s) for p, s in zip(layer_pairs, similarities)},
    }


def compute_manifold_metrics(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
    n_neighbors: int = 10,
) -> Dict[str, Any]:
    """
    Compute manifold and curvature metrics.

    Describes:
    - Is the separation surface flat or curved?
    - Local vs global structure
    - Intrinsic dimensionality estimates
    """
    pos = pos_activations.float().cpu().numpy()
    neg = neg_activations.float().cpu().numpy()

    n = min(len(pos), len(neg))
    pos, neg = pos[:n], neg[:n]
    diffs = pos - neg

    # PCA on diffs
    from sklearn.decomposition import PCA

    n_components = min(50, n - 1, diffs.shape[1])
    pca = PCA(n_components=n_components)
    diffs_pca = pca.fit_transform(diffs)

    explained_variance = pca.explained_variance_ratio_
    cumsum_variance = np.cumsum(explained_variance)

    # Intrinsic dim estimates
    dims_for_50 = int(np.searchsorted(cumsum_variance, 0.5) + 1)
    dims_for_90 = int(np.searchsorted(cumsum_variance, 0.9) + 1)
    dims_for_99 = int(np.searchsorted(cumsum_variance, 0.99) + 1)

    # Participation ratio (effective dimensionality)
    participation_ratio = (explained_variance.sum() ** 2) / (np.sum(explained_variance ** 2) + 1e-8)

    # Local linearity: how well does local PCA match global PCA
    local_linearities = []
    for i in range(min(n, 50)):
        # Find k nearest neighbors
        distances = np.linalg.norm(diffs - diffs[i], axis=1)
        neighbor_idx = np.argsort(distances)[1:n_neighbors+1]

        if len(neighbor_idx) >= 3:
            local_diffs = diffs[neighbor_idx]
            local_mean = local_diffs.mean(axis=0)
            local_norm = np.linalg.norm(local_mean)

            global_mean = diffs.mean(axis=0)
            global_norm = np.linalg.norm(global_mean)

            if local_norm > 1e-8 and global_norm > 1e-8:
                local_dir = local_mean / local_norm
                global_dir = global_mean / global_norm
                local_linearities.append(np.abs(np.dot(local_dir, global_dir)))

    local_linearities = np.array(local_linearities)

    # Curvature proxy: variance of local directions
    curvature_proxy = 1 - local_linearities.mean() if len(local_linearities) > 0 else None

    return {
        # PCA variance
        "variance_pc1": float(explained_variance[0]) if len(explained_variance) > 0 else None,
        "variance_pc2": float(explained_variance[1]) if len(explained_variance) > 1 else None,
        "variance_pc3": float(explained_variance[2]) if len(explained_variance) > 2 else None,
        "variance_top5": float(cumsum_variance[4]) if len(cumsum_variance) > 4 else None,
        "variance_top10": float(cumsum_variance[9]) if len(cumsum_variance) > 9 else None,

        # Dimensionality
        "dims_for_50pct_variance": dims_for_50,
        "dims_for_90pct_variance": dims_for_90,
        "dims_for_99pct_variance": dims_for_99,
        "participation_ratio": float(participation_ratio),

        # Curvature/linearity
        "local_linearity_mean": float(local_linearities.mean()) if len(local_linearities) > 0 else None,
        "local_linearity_std": float(local_linearities.std()) if len(local_linearities) > 0 else None,
        "local_linearity_min": float(local_linearities.min()) if len(local_linearities) > 0 else None,
        "curvature_proxy": float(curvature_proxy) if curvature_proxy is not None else None,

        # Full explained variance (for plotting)
        "explained_variance_ratio": explained_variance.tolist(),
    }


def compute_token_position_metrics(
    pos_activations_by_position: Dict[int, torch.Tensor],
    neg_activations_by_position: Dict[int, torch.Tensor],
) -> Dict[str, Any]:
    """
    Compute token position dependence metrics.

    Describes:
    - Is the signal at all positions or just certain ones?
    - How does signal strength vary by position?

    Args:
        pos_activations_by_position: Dict mapping position -> activations
        neg_activations_by_position: Dict mapping position -> activations
    """
    positions = sorted(set(pos_activations_by_position.keys()) & set(neg_activations_by_position.keys()))

    if len(positions) < 2:
        return {"error": "need at least 2 positions"}

    # Compute signal strength at each position
    from sklearn.linear_model import LogisticRegression

    position_metrics = {}
    directions = {}

    for pos_idx in positions:
        pos = pos_activations_by_position[pos_idx].float().cpu().numpy()
        neg = neg_activations_by_position[pos_idx].float().cpu().numpy()
        n = min(len(pos), len(neg))

        if n < 5:
            continue

        # Linear probe accuracy
        X = np.vstack([pos[:n], neg[:n]])
        y = np.array([1] * n + [0] * n)

        try:
            clf = LogisticRegression(max_iter=500, random_state=42)
            clf.fit(X, y)
            accuracy = clf.score(X, y)
        except:
            accuracy = 0.5

        # Steering direction
        mean_diff = (pos[:n] - neg[:n]).mean(axis=0)
        norm = np.linalg.norm(mean_diff)

        position_metrics[pos_idx] = {
            "linear_accuracy": float(accuracy),
            "steering_norm": float(norm),
        }

        if norm > 1e-8:
            directions[pos_idx] = mean_diff / norm

    # Cross-position consistency
    position_list = list(directions.keys())
    if len(position_list) >= 2:
        cross_pos_sims = []
        for i, p1 in enumerate(position_list):
            for p2 in position_list[i+1:]:
                if len(directions[p1]) == len(directions[p2]):
                    cross_pos_sims.append(np.dot(directions[p1], directions[p2]))
        cross_pos_sims = np.array(cross_pos_sims)
    else:
        cross_pos_sims = np.array([])

    # Find best position
    if position_metrics:
        best_position = max(position_metrics.keys(), key=lambda p: position_metrics[p]["linear_accuracy"])
    else:
        best_position = None

    return {
        "n_positions": len(positions),
        "positions": positions,
        "per_position_metrics": position_metrics,

        # Cross-position consistency
        "cross_position_similarity_mean": float(cross_pos_sims.mean()) if len(cross_pos_sims) > 0 else None,
        "cross_position_similarity_std": float(cross_pos_sims.std()) if len(cross_pos_sims) > 0 else None,

        # Best position
        "best_position": best_position,
        "best_position_accuracy": position_metrics[best_position]["linear_accuracy"] if best_position else None,
    }


def compute_direction_overlap_metrics(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
    other_directions: Dict[str, np.ndarray] = None,
) -> Dict[str, Any]:
    """
    Compute overlap with other known directions.

    Describes:
    - Does this concept's direction overlap with other concepts?
    - How unique is this direction?

    Args:
        other_directions: Dict mapping concept name -> unit direction vector
    """
    pos = pos_activations.float().cpu().numpy()
    neg = neg_activations.float().cpu().numpy()

    n = min(len(pos), len(neg))
    diffs = pos[:n] - neg[:n]
    mean_diff = diffs.mean(axis=0)
    norm = np.linalg.norm(mean_diff)

    if norm < 1e-8:
        return {"error": "steering direction norm too small"}

    direction = mean_diff / norm

    if not other_directions:
        return {
            "steering_direction_norm": float(norm),
            "other_directions_provided": False,
        }

    # Compute overlap with each other direction
    overlaps = {}
    for name, other_dir in other_directions.items():
        if len(other_dir) == len(direction):
            other_norm = np.linalg.norm(other_dir)
            if other_norm > 1e-8:
                other_normalized = other_dir / other_norm
                overlap = float(np.dot(direction, other_normalized))
                overlaps[name] = overlap

    # Find most overlapping
    if overlaps:
        most_overlapping = max(overlaps.keys(), key=lambda k: abs(overlaps[k]))
        least_overlapping = min(overlaps.keys(), key=lambda k: abs(overlaps[k]))
    else:
        most_overlapping = None
        least_overlapping = None

    return {
        "steering_direction_norm": float(norm),
        "other_directions_provided": True,
        "n_other_directions": len(other_directions),

        # Overlaps
        "overlaps": overlaps,
        "most_overlapping": most_overlapping,
        "most_overlapping_value": overlaps.get(most_overlapping) if most_overlapping else None,
        "least_overlapping": least_overlapping,
        "least_overlapping_value": overlaps.get(least_overlapping) if least_overlapping else None,

        # Summary stats
        "mean_absolute_overlap": float(np.mean([abs(v) for v in overlaps.values()])) if overlaps else None,
        "max_absolute_overlap": float(np.max([abs(v) for v in overlaps.values()])) if overlaps else None,
    }


def compute_noise_baseline_comparison(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
    n_noise_samples: int = 5,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Compare actual metrics to what random noise would produce.

    Computes metrics on random Gaussian activations with same shape/norms
    and reports how actual data differs from noise baseline.

    This helps identify whether there's semantic content or just noise.
    """
    pos = pos_activations.float().cpu().numpy()
    neg = neg_activations.float().cpu().numpy()

    n = min(len(pos), len(neg))
    pos, neg = pos[:n], neg[:n]
    hidden_dim = pos.shape[1]

    # Compute actual metrics
    pos_norms = np.linalg.norm(pos, axis=1)
    neg_norms = np.linalg.norm(neg, axis=1)
    mean_norm = (pos_norms.mean() + neg_norms.mean()) / 2

    diffs = pos - neg
    mean_diff = diffs.mean(axis=0)
    mean_diff_norm = np.linalg.norm(mean_diff)

    # Actual metrics
    diff_norms = np.linalg.norm(diffs, axis=1)
    valid_mask = diff_norms > 1e-8
    if valid_mask.sum() < 2:
        return {"error": "not enough valid diffs"}

    diff_normalized = diffs[valid_mask] / diff_norms[valid_mask, np.newaxis]
    mean_diff_normalized = mean_diff / (mean_diff_norm + 1e-8)

    # Actual alignment
    actual_alignments = diff_normalized @ mean_diff_normalized
    actual_alignment_mean = float(actual_alignments.mean())

    # Actual variance concentration (PC1)
    from sklearn.decomposition import PCA
    n_components = min(50, n - 1, hidden_dim)
    if n_components < 1:
        return {"error": "not enough samples for PCA"}

    pca = PCA(n_components=n_components)
    pca.fit(diffs)
    actual_variance_pc1 = float(pca.explained_variance_ratio_[0])
    actual_cumsum = np.cumsum(pca.explained_variance_ratio_)
    actual_dims_for_90 = int(np.searchsorted(actual_cumsum, 0.9) + 1)

    # Actual linear probe
    from sklearn.linear_model import LogisticRegression
    X = np.vstack([pos, neg])
    y = np.array([1] * n + [0] * n)
    try:
        clf = LogisticRegression(max_iter=500, random_state=42)
        clf.fit(X, y)
        actual_linear_probe = float(clf.score(X, y))
    except:
        actual_linear_probe = 0.5

    # Actual steering/activation ratio
    actual_steering_ratio = mean_diff_norm / (mean_norm + 1e-8)

    # Generate noise baselines
    np.random.seed(seed)
    noise_metrics = {
        'alignment_mean': [],
        'variance_pc1': [],
        'dims_for_90': [],
        'linear_probe': [],
        'steering_ratio': [],
    }

    for i in range(n_noise_samples):
        # Random activations with same norm distribution
        noise_pos = np.random.randn(n, hidden_dim)
        noise_neg = np.random.randn(n, hidden_dim)

        # Scale to match actual norms
        noise_pos = noise_pos / np.linalg.norm(noise_pos, axis=1, keepdims=True) * pos_norms[:, np.newaxis]
        noise_neg = noise_neg / np.linalg.norm(noise_neg, axis=1, keepdims=True) * neg_norms[:, np.newaxis]

        # Noise diffs
        noise_diffs = noise_pos - noise_neg
        noise_mean_diff = noise_diffs.mean(axis=0)
        noise_mean_diff_norm = np.linalg.norm(noise_mean_diff)

        noise_diff_norms = np.linalg.norm(noise_diffs, axis=1)
        noise_valid = noise_diff_norms > 1e-8

        if noise_valid.sum() >= 2:
            noise_diff_normalized = noise_diffs[noise_valid] / noise_diff_norms[noise_valid, np.newaxis]
            noise_mean_normalized = noise_mean_diff / (noise_mean_diff_norm + 1e-8)
            noise_alignments = noise_diff_normalized @ noise_mean_normalized
            noise_metrics['alignment_mean'].append(float(noise_alignments.mean()))

        # Noise PCA
        try:
            noise_pca = PCA(n_components=n_components)
            noise_pca.fit(noise_diffs)
            noise_metrics['variance_pc1'].append(float(noise_pca.explained_variance_ratio_[0]))
            noise_cumsum = np.cumsum(noise_pca.explained_variance_ratio_)
            noise_metrics['dims_for_90'].append(int(np.searchsorted(noise_cumsum, 0.9) + 1))
        except:
            pass

        # Noise linear probe
        noise_X = np.vstack([noise_pos, noise_neg])
        try:
            noise_clf = LogisticRegression(max_iter=500, random_state=42+i)
            noise_clf.fit(noise_X, y)
            noise_metrics['linear_probe'].append(float(noise_clf.score(noise_X, y)))
        except:
            noise_metrics['linear_probe'].append(0.5)

        # Noise steering ratio
        noise_metrics['steering_ratio'].append(noise_mean_diff_norm / (mean_norm + 1e-8))

    # Compute noise baselines (mean of noise samples)
    noise_baseline = {k: float(np.mean(v)) if v else None for k, v in noise_metrics.items()}
    noise_std = {k: float(np.std(v)) if v else None for k, v in noise_metrics.items()}

    # Compute differences from noise
    alignment_vs_noise = actual_alignment_mean - noise_baseline['alignment_mean'] if noise_baseline['alignment_mean'] else None
    variance_vs_noise = actual_variance_pc1 - noise_baseline['variance_pc1'] if noise_baseline['variance_pc1'] else None
    dims_vs_noise = actual_dims_for_90 - noise_baseline['dims_for_90'] if noise_baseline['dims_for_90'] else None
    linear_vs_noise = actual_linear_probe - noise_baseline['linear_probe'] if noise_baseline['linear_probe'] else None
    steering_vs_noise = actual_steering_ratio - noise_baseline['steering_ratio'] if noise_baseline['steering_ratio'] else None

    return {
        # Actual values
        "actual": {
            "alignment_mean": actual_alignment_mean,
            "variance_pc1": actual_variance_pc1,
            "dims_for_90pct": actual_dims_for_90,
            "linear_probe": actual_linear_probe,
            "steering_ratio": actual_steering_ratio,
        },

        # Noise baseline (what random data looks like)
        "noise_baseline": {
            "alignment_mean": noise_baseline['alignment_mean'],
            "variance_pc1": noise_baseline['variance_pc1'],
            "dims_for_90pct": noise_baseline['dims_for_90'],
            "linear_probe": noise_baseline['linear_probe'],
            "steering_ratio": noise_baseline['steering_ratio'],
        },

        # Standard deviation of noise (for significance)
        "noise_std": {
            "alignment_mean": noise_std['alignment_mean'],
            "variance_pc1": noise_std['variance_pc1'],
            "dims_for_90pct": noise_std['dims_for_90'],
            "linear_probe": noise_std['linear_probe'],
            "steering_ratio": noise_std['steering_ratio'],
        },

        # Difference from noise (positive = more signal than noise)
        "vs_noise": {
            "alignment_mean": alignment_vs_noise,
            "variance_pc1": variance_vs_noise,
            "dims_for_90pct": dims_vs_noise,  # negative is better (more concentrated)
            "linear_probe": linear_vs_noise,
            "steering_ratio": steering_vs_noise,  # negative means pos/neg share structure
        },

        # How many noise stds above baseline (z-score like)
        "stds_above_noise": {
            "alignment_mean": alignment_vs_noise / (noise_std['alignment_mean'] + 1e-8) if noise_std['alignment_mean'] else None,
            "variance_pc1": variance_vs_noise / (noise_std['variance_pc1'] + 1e-8) if noise_std['variance_pc1'] else None,
            "linear_probe": linear_vs_noise / (noise_std['linear_probe'] + 1e-8) if noise_std['linear_probe'] else None,
        },

        # Metadata
        "n_pairs": n,
        "hidden_dim": hidden_dim,
        "n_noise_samples": n_noise_samples,
    }


def analyze_representation_geometry(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
) -> Dict[str, Any]:
    """
    Comprehensive geometric analysis of a representation.

    Analyzes the shape of the representation and returns raw metrics
    describing its geometry. Does NOT make recommendations.

    Returns metrics describing:
    - Linear separability (can a hyperplane separate pos/neg?)
    - Cone structure (do diff vectors point same direction?)
    - Intrinsic dimensionality (how many dims does concept use?)
    - Curvature (is the manifold flat or curved?)
    - Sparsity (is signal concentrated or distributed?)
    - Noise comparison (is this real signal?)

    The geometry determines which steering method is appropriate:
    - TIGHT CONE + FLAT + LINEAR → CAA
    - LINEAR but LOW ALIGNMENT → Hyperplane
    - MULTI-DIRECTIONAL → PRISM
    - CURVED/NONLINEAR → MLP-based
    - HIGH CURVATURE → TITAN/PULSE
    """
    from .probe_metrics import (
        compute_linear_probe_accuracy,
        compute_mlp_probe_accuracy,
        compute_knn_accuracy,
    )
    from .steerability import compute_steerability_metrics

    results = {}

    # 1. Linear separability
    linear_acc = compute_linear_probe_accuracy(pos_activations, neg_activations)
    mlp_acc = compute_mlp_probe_accuracy(pos_activations, neg_activations)
    knn_acc = compute_knn_accuracy(pos_activations, neg_activations)

    results["separability"] = {
        "linear_probe_accuracy": linear_acc,
        "mlp_probe_accuracy": mlp_acc,
        "knn_accuracy": knn_acc,
        "nonlinearity_gap": mlp_acc - linear_acc,
    }

    # 2. Cone structure (direction consistency)
    pair_quality = compute_pair_quality_metrics(pos_activations, neg_activations)
    steerability = compute_steerability_metrics(pos_activations, neg_activations)

    results["cone_structure"] = {
        "alignment_mean": pair_quality.get("alignment_mean"),
        "alignment_std": pair_quality.get("alignment_std"),
        "alignment_min": pair_quality.get("alignment_min"),
        "pct_positive_alignment": steerability.get("pct_positive_alignment"),
        "outlier_fraction": pair_quality.get("outlier_fraction"),
    }

    # 3. Intrinsic dimensionality
    manifold = compute_manifold_metrics(pos_activations, neg_activations)

    results["dimensionality"] = {
        "variance_pc1": manifold.get("variance_pc1"),
        "variance_top5": manifold.get("variance_top5"),
        "dims_for_50pct_variance": manifold.get("dims_for_50pct_variance"),
        "dims_for_90pct_variance": manifold.get("dims_for_90pct_variance"),
        "participation_ratio": manifold.get("participation_ratio"),
    }

    # 4. Curvature
    results["curvature"] = {
        "local_linearity_mean": manifold.get("local_linearity_mean"),
        "local_linearity_std": manifold.get("local_linearity_std"),
        "curvature_proxy": manifold.get("curvature_proxy"),
    }

    # 5. Sparsity
    sparsity = compute_sparsity_metrics(pos_activations, neg_activations)

    results["sparsity"] = {
        "neurons_for_50pct": sparsity.get("neurons_for_50pct"),
        "neurons_for_90pct": sparsity.get("neurons_for_90pct"),
        "neurons_for_50pct_fraction": sparsity.get("neurons_for_50pct_fraction"),
        "diff_gini": sparsity.get("diff_gini"),
        "top_10_contribution_fraction": sparsity.get("top_10_contribution_fraction"),
    }

    # 6. Magnitude
    magnitude = compute_magnitude_metrics(pos_activations, neg_activations)

    results["magnitude"] = {
        "activation_norm_mean": magnitude.get("all_norm_mean"),
        "diff_norm_mean": magnitude.get("diff_norm_mean"),
        "steering_vector_norm": magnitude.get("steering_vector_norm"),
        "steering_to_activation_ratio": magnitude.get("steering_to_activation_ratio"),
        "steering_to_diff_ratio": magnitude.get("steering_to_diff_ratio"),
    }

    # 7. Noise comparison
    noise = compute_noise_baseline_comparison(pos_activations, neg_activations)

    results["noise_comparison"] = {
        "actual_linear_probe": noise.get("actual", {}).get("linear_probe"),
        "noise_linear_probe": noise.get("noise_baseline", {}).get("linear_probe"),
        "actual_alignment": noise.get("actual", {}).get("alignment_mean"),
        "noise_alignment": noise.get("noise_baseline", {}).get("alignment_mean"),
        "alignment_vs_noise": noise.get("vs_noise", {}).get("alignment_mean"),
        "variance_vs_noise": noise.get("vs_noise", {}).get("variance_pc1"),
    }

    # Summary classification (no thresholds, just extracted key values)
    results["summary"] = {
        "is_linearly_separable": linear_acc,  # Higher = more linearly separable
        "is_tight_cone": pair_quality.get("alignment_mean"),  # Higher = tighter cone
        "is_flat": 1 - (manifold.get("curvature_proxy") or 0),  # Higher = flatter
        "is_low_dimensional": 1 / (manifold.get("dims_for_90pct_variance") or 1),  # Higher = lower dim
        "signal_above_noise": noise.get("vs_noise", {}).get("alignment_mean"),  # Higher = more signal
    }

    return results


def compute_all_representation_metrics(
    pos_activations: torch.Tensor,
    neg_activations: torch.Tensor,
    activations_by_layer: Dict[int, Tuple[torch.Tensor, torch.Tensor]] = None,
    pos_activations_by_position: Dict[int, torch.Tensor] = None,
    neg_activations_by_position: Dict[int, torch.Tensor] = None,
    other_directions: Dict[str, np.ndarray] = None,
    include_noise_baseline: bool = True,
) -> Dict[str, Any]:
    """
    Compute all representation metrics.

    This is the main entry point for comprehensive representation description.
    """
    results = {}

    # Always compute these
    results["magnitude"] = compute_magnitude_metrics(pos_activations, neg_activations)
    results["sparsity"] = compute_sparsity_metrics(pos_activations, neg_activations)
    results["pair_quality"] = compute_pair_quality_metrics(pos_activations, neg_activations)
    results["manifold"] = compute_manifold_metrics(pos_activations, neg_activations)

    # Noise baseline comparison (detect if data has semantic content vs noise)
    if include_noise_baseline:
        results["noise_comparison"] = compute_noise_baseline_comparison(pos_activations, neg_activations)

    # Optional: cross-layer consistency
    if activations_by_layer is not None:
        results["cross_layer"] = compute_cross_layer_consistency(activations_by_layer)

    # Optional: token position dependence
    if pos_activations_by_position is not None and neg_activations_by_position is not None:
        results["token_position"] = compute_token_position_metrics(
            pos_activations_by_position, neg_activations_by_position
        )

    # Optional: direction overlap
    results["direction_overlap"] = compute_direction_overlap_metrics(
        pos_activations, neg_activations, other_directions
    )

    return results
