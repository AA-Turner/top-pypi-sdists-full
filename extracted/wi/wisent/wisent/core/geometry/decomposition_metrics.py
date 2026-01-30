"""Decomposition metrics for RepScan Step 3: Decomposition Test."""

from typing import List, Tuple
import torch
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def _adaptive_max_k(n_samples: int) -> int:
    """Adaptive max clusters: sqrt(n/2) clamped to [2, 15]."""
    max_k = int(np.sqrt(n_samples / 2))
    return max(2, min(max_k, 15))


def _adaptive_min_cluster_size(n_samples: int) -> int:
    """Adaptive min samples per cluster: max(5, n/20)."""
    return max(5, n_samples // 20)


def find_optimal_clustering(
    diff_vectors: torch.Tensor,
) -> Tuple[int, List[int], float]:
    """
    Find optimal number of clusters with adaptive parameters.

    Uses silhouette score to determine optimal k.
    All parameters derived from data size.

    Returns:
        Tuple of (n_concepts, cluster_labels, best_silhouette)
    """
    diff_np = diff_vectors.cpu().numpy() if isinstance(diff_vectors, torch.Tensor) else diff_vectors

    n_samples, n_features = diff_np.shape
    max_k = _adaptive_max_k(n_samples)
    min_cluster_size = _adaptive_min_cluster_size(n_samples)

    # Adjust max_k based on min_cluster_size constraint
    max_k = min(max_k, n_samples // min_cluster_size)

    if max_k < 2:
        return 1, [0] * n_samples, 0.0

    # Adaptive n_init based on sample size (more samples = fewer inits needed)
    n_init = max(3, min(10, 1000 // n_samples + 1))

    best_k = 1
    best_silhouette = -1.0
    best_labels = [0] * n_samples

    for k in range(2, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=n_init)
        labels = kmeans.fit_predict(diff_np)

        # Check if any cluster is too small
        cluster_sizes = np.bincount(labels)
        if cluster_sizes.min() < min_cluster_size:
            continue

        sil = silhouette_score(diff_np, labels)
        if sil > best_silhouette:
            best_silhouette = sil
            best_k = k
            best_labels = labels.tolist()

    return best_k, best_labels, float(best_silhouette)
