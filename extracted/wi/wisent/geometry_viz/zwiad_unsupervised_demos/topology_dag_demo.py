"""Synthetic-shape end-to-end demo for Zwiad unsupervised additions.

Verifies test_topology against known-truth synthetic point clouds (blob,
circle, sphere, torus) and prints the recovered Betti signature + named
shape; verifies test_layer_dag against a synthetic per-layer activation
chain and prints the recovered DAG edges + minimum steering set.

Run: python3 geometry_viz/zwiad_unsupervised_demos/topology_dag_demo.py
"""
import numpy as np
import torch

from wisent.core.reading.modules.modules.zwiad.unsupervised import (
    test_topology,
    test_layer_dag,
)

SEED = 42
rng = np.random.default_rng(SEED)


def synthetic_blob(n: int, d: int) -> torch.Tensor:
    """Single Gaussian blob in R^d (expects Betti = (1, 0, 0))."""
    return torch.tensor(rng.normal(0, 1, (n, d)), dtype=torch.float32)


def synthetic_circle(n: int, d: int, noise: float) -> torch.Tensor:
    """N points on a unit circle in R^d (first 2 dims) + isotropic noise."""
    theta = rng.uniform(0, 2 * np.pi, n)
    X = np.zeros((n, d))
    X[:, 0] = np.cos(theta)
    X[:, 1] = np.sin(theta)
    X += noise * rng.normal(0, 1, X.shape)
    return torch.tensor(X, dtype=torch.float32)


def synthetic_sphere(n: int, d: int, noise: float) -> torch.Tensor:
    """N points on a unit 2-sphere in R^d (first 3 dims) + isotropic noise."""
    pts = rng.normal(0, 1, (n, 3))
    pts /= np.linalg.norm(pts, axis=1, keepdims=True)
    X = np.zeros((n, d))
    X[:, :3] = pts
    X += noise * rng.normal(0, 1, X.shape)
    return torch.tensor(X, dtype=torch.float32)


def synthetic_torus(n: int, d: int, R: float, r: float, noise: float) -> torch.Tensor:
    """N points on a torus T^2 in R^d (first 3 dims) + isotropic noise."""
    u = rng.uniform(0, 2 * np.pi, n)
    v = rng.uniform(0, 2 * np.pi, n)
    X = np.zeros((n, d))
    X[:, 0] = (R + r * np.cos(v)) * np.cos(u)
    X[:, 1] = (R + r * np.cos(v)) * np.sin(u)
    X[:, 2] = r * np.sin(v)
    X += noise * rng.normal(0, 1, X.shape)
    return torch.tensor(X, dtype=torch.float32)


def demo_topology() -> None:
    print("=" * 70)
    print("UNSUPERVISED TOPOLOGY DEMO (test_topology on known-truth shapes)")
    print("=" * 70)
    cases = [
        ("blob (point)", synthetic_blob(80, 10), synthetic_blob(80, 10), (1, 0, 0)),
        ("circle",       synthetic_circle(80, 10, 0.05), synthetic_circle(80, 10, 0.05), (1, 1, 0)),
        ("sphere",       synthetic_sphere(150, 10, 0.05), synthetic_sphere(150, 10, 0.05), (1, 0, 1)),
        ("torus",        synthetic_torus(300, 10, 2.0, 1.0, 0.05), synthetic_torus(300, 10, 2.0, 1.0, 0.05), (1, 2, 1)),
    ]
    for label, pos, neg, exp_betti in cases:
        result = test_topology(
            pos, neg,
            max_dim=2,
            max_edge_length=5.0,
            persistence_threshold=0.3,
        )
        verdict = "OK   " if result.betti_union == exp_betti else "MISS "
        print(
            f"  [{verdict}] {label:18s}  expected betti={exp_betti}  "
            f"got betti={result.betti_union}  named_shape={result.named_shape_union!r}"
        )


def demo_layer_dag() -> None:
    print()
    print("=" * 70)
    print("LAYER DAG DEMO (test_layer_dag on synthetic per-layer chain)")
    print("=" * 70)
    n_samples = 100
    n_layers = 6
    feat_dim = 16
    base_pos = torch.tensor(rng.normal( 2.0, 1.0, (n_samples, feat_dim)), dtype=torch.float32)
    base_neg = torch.tensor(rng.normal(-2.0, 1.0, (n_samples, feat_dim)), dtype=torch.float32)
    activations_by_layer = {}
    for L in range(n_layers):
        scale = 1.0 + 0.3 * L
        noise = 0.5
        pos = scale * base_pos + noise * torch.tensor(rng.normal(0, 1, (n_samples, feat_dim)), dtype=torch.float32)
        neg = scale * base_neg + noise * torch.tensor(rng.normal(0, 1, (n_samples, feat_dim)), dtype=torch.float32)
        activations_by_layer[L] = (pos, neg)
    signal_layers = list(range(n_layers))
    result = test_layer_dag(
        activations_by_layer, signal_layers,
        alpha=0.05, max_conditioning_set=2,
    )
    forward_only = all(i < j for (i, j) in result.edges)
    print(f"  nodes:                  {result.nodes}")
    print(f"  edges:                  {result.edges}")
    print(f"  signal layers:          {result.signal_layers}")
    print(f"  minimum steering set:   {result.minimum_steering_set}")
    print(f"  acyclic + forward-only: {forward_only}")


if __name__ == "__main__":
    demo_topology()
    demo_layer_dag()
