"""
Demo: render every Zwiad geometry shape in 3D using the new shapes_3d renderers.

Synthesizes pos/neg activations with each known geometric shape, dispatches
via render_shape(), then plots the returned dict with matplotlib Axes3D.

Run: python geometry_viz/zwiad_3d_shape_demo.py
Outputs PNGs to geometry_viz/zwiad_3d_outputs/.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (registers 3d projection)

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent
sys.path.insert(0, str(_REPO))

# Bypass wisent/__init__.py (which eagerly loads transformers/datasets/lm_eval).
# The shapes_3d module only needs three constants — inject a minimal stub
# package tree so its `from wisent.core.utils.config_tools.constants import …`
# resolves without dragging in the rest of wisent.
import types as _types
import importlib.util as _ilu


def _stub(name: str) -> _types.ModuleType:
    m = _types.ModuleType(name)
    sys.modules[name] = m
    return m


_stub("wisent")
_stub("wisent.core")
_stub("wisent.core.utils")
_stub("wisent.core.utils.config_tools")
_const = _stub("wisent.core.utils.config_tools.constants")
_const.VIZ_N_COMPONENTS_3D = 3
_const.DEFAULT_RANDOM_SEED = 42
_const.NORM_EPS = 1e-9
_stub("wisent.core.utils.visualization")
_stub("wisent.core.utils.visualization.geometry")
_stub("wisent.core.utils.visualization.geometry.internals")
_stub("wisent.core.utils.visualization.geometry.internals.shapes_3d")


def _load_module(qualname: str, file_path: Path):
    spec = _ilu.spec_from_file_location(qualname, file_path)
    mod = _ilu.module_from_spec(spec)
    sys.modules[qualname] = mod
    spec.loader.exec_module(mod)
    return mod


_shapes_root = _REPO / "wisent" / "core" / "utils" / "visualization" / "geometry" / "internals" / "shapes_3d"
_dispatch = _load_module("wisent.core.utils.visualization.geometry.internals.shapes_3d.dispatch", _shapes_root / "dispatch.py")
_renderers = _load_module("wisent.core.utils.visualization.geometry.internals.shapes_3d.renderers", _shapes_root / "renderers.py")
render_shape = _dispatch.render_shape


_SEED = 17
_N = 300
_OUTDIR = _HERE / "zwiad_3d_outputs"
_OUTDIR.mkdir(parents=True, exist_ok=True)


def _synthesize(shape: str, dim: int = 32):
    """Return (pos, neg) tensors with the geometry indicated by shape."""
    rng = np.random.RandomState(_SEED)
    if shape == "linear":
        d = rng.randn(dim); d /= np.linalg.norm(d)
        pos = rng.randn(_N, dim) * 0.4 + d * 2.5
        neg = rng.randn(_N, dim) * 0.4 - d * 2.5
    elif shape == "cone":
        axis = rng.randn(dim); axis /= np.linalg.norm(axis)
        deviations = rng.randn(_N, dim) * 0.5
        pos = axis * (1.0 + np.abs(rng.randn(_N, 1)) * 3.0) + deviations
        neg = -axis * (1.0 + np.abs(rng.randn(_N, 1)) * 3.0) + rng.randn(_N, dim) * 0.5
    elif shape == "orthogonal":
        a = rng.randn(dim); a /= np.linalg.norm(a)
        b = rng.randn(dim); b -= b @ a * a; b /= np.linalg.norm(b)
        pos = (rng.randn(_N, 1) * a + rng.randn(_N, 1) * b) * 2.0 + rng.randn(_N, dim) * 0.3
        neg = (rng.randn(_N, 1) * a + rng.randn(_N, 1) * b) * 2.0 + rng.randn(_N, dim) * 0.3
    elif shape == "bimodal":
        c1 = rng.randn(dim) * 3.0; c2 = -c1
        pos = c1 + rng.randn(_N, dim) * 0.5
        neg = c2 + rng.randn(_N, dim) * 0.5
    elif shape == "cluster":
        k = 5
        centroids = rng.randn(k, dim) * 4.0
        labels = rng.randint(0, k, size=_N)
        pos = centroids[labels] + rng.randn(_N, dim) * 0.4
        neg = pos + rng.randn(_N, dim) * 0.6
    elif shape == "manifold":
        t = np.linspace(0.0, 4.0 * np.pi, _N)
        curve = np.stack([np.cos(t) * (1.0 + 0.3 * t), np.sin(t) * (1.0 + 0.3 * t), 0.2 * t], axis=1)
        emb = np.zeros((_N, dim))
        emb[:, :3] = curve
        emb += rng.randn(_N, dim) * 0.15
        pos = emb
        neg = emb + rng.randn(_N, dim) * 0.2
    elif shape == "sparse":
        pos = rng.randn(_N, dim) * 0.3
        outlier_idx = rng.choice(_N, size=_N // 10, replace=False)
        pos[outlier_idx] += rng.randn(len(outlier_idx), dim) * 5.0
        neg = rng.randn(_N, dim) * 0.3
        outlier_idx2 = rng.choice(_N, size=_N // 10, replace=False)
        neg[outlier_idx2] += rng.randn(len(outlier_idx2), dim) * 5.0
    elif shape == "sphere":
        v = rng.randn(_N, dim)
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        pos = v * 3.0 + rng.randn(_N, dim) * 0.1
        v2 = rng.randn(_N, dim)
        v2 /= np.linalg.norm(v2, axis=1, keepdims=True)
        neg = v2 * 3.0 + rng.randn(_N, dim) * 0.1
    else:
        raise ValueError(f"unknown shape: {shape}")
    return torch.from_numpy(pos.astype(np.float32)), torch.from_numpy(neg.astype(np.float32))


def _render_to_png(data: dict, path: Path) -> None:
    """Render a render_shape() result dict to a PNG via matplotlib Axes3D."""
    fig = plt.figure(figsize=(7.5, 7.0))
    ax = fig.add_subplot(111, projection="3d")
    pos = data["pos_3d"]; neg = data["neg_3d"]
    ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], c="#d62728", s=8, alpha=0.55, label="pos")
    ax.scatter(neg[:, 0], neg[:, 1], neg[:, 2], c="#1f77b4", s=8, alpha=0.55, label="neg")

    s = data["shape"]
    if s == "linear":
        ep = data["axis_endpoints"]
        ax.plot(ep[:, 0], ep[:, 1], ep[:, 2], color="black", lw=2.5, label="separating axis")
    elif s == "cone":
        lines = data["cone_lines"]
        for seg in lines:
            ax.plot(seg[:, 0], seg[:, 1], seg[:, 2], color="black", lw=0.4, alpha=0.45)
        apex = data["cone_apex"]
        ax.scatter([apex[0]], [apex[1]], [apex[2]], c="black", s=40, marker="^", label=f"apex ({data['cone_half_angle_deg']:.1f}°)")
    elif s == "orthogonal":
        axes = data["axes"]
        for axis_pair in axes:
            ax.plot(axis_pair[:, 0], axis_pair[:, 1], axis_pair[:, 2], color="black", lw=2.0)
        ax.plot([], [], [], color="black", lw=2.0, label="PC1/PC2")
    elif s == "bimodal":
        cp = data["centroid_pos"]; cn = data["centroid_neg"]
        ax.scatter([cp[0], cn[0]], [cp[1], cn[1]], [cp[2], cn[2]], c="black", s=80, marker="X", label="centroids")
        # render the separating plane as a small quad
        p = data["separating_plane_point"]; n = data["separating_plane_normal"]
        # find two vectors orthogonal to n
        helper = np.array([1.0, 0.0, 0.0]) if abs(n[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
        u = np.cross(n, helper); u /= np.linalg.norm(u) + 1e-9
        v = np.cross(n, u)
        span = float(np.linalg.norm(cp - cn))
        corners = [p + a * u + b * v for a in (-span, span) for b in (-span, span)]
        corners = np.array([corners[0], corners[1], corners[3], corners[2]])
        ax.plot_trisurf(corners[:, 0], corners[:, 1], corners[:, 2], color="grey", alpha=0.2)
    elif s == "cluster":
        labels = data["cluster_labels"]
        cents = data["cluster_centroids"]
        # color-recolor diff_3d points by cluster id
        cmap = plt.cm.tab10
        for k, c in enumerate(cents):
            ax.scatter([c[0]], [c[1]], [c[2]], color=cmap(k % 10), s=120, marker="X",
                       edgecolor="black", linewidths=1.2, label=f"cluster {k}")
    elif s == "manifold":
        edges = data["edges"]
        for seg in edges:
            ax.plot(seg[:, 0], seg[:, 1], seg[:, 2], color="black", lw=0.25, alpha=0.4)
        ax.plot([], [], [], color="black", lw=0.7, label=f"kNN graph (k={data['n_neighbors']})")
    elif s == "sparse":
        # density already encoded; redo the scatter weighted by density
        ax.cla()
        density = data["density"]
        all_pts = np.concatenate([pos, neg], axis=0)
        ax.scatter(all_pts[:, 0], all_pts[:, 1], all_pts[:, 2], c=density, cmap="viridis", s=20)
    elif s == "sphere":
        surf = data["sphere_surface"]
        ax.plot_wireframe(surf[:, :, 0], surf[:, :, 1], surf[:, :, 2],
                          color="black", lw=0.4, alpha=0.45, rcount=12, ccount=18)
        ax.set_title(f"{data['title']} — r={data['sphere_radius']:.2f} ± {data['sphere_radius_std']:.2f}")

    ax.set_title(data.get("title", s))
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); ax.set_zlabel("PC3")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.85)
    plt.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main():
    shapes = ["linear", "cone", "orthogonal", "bimodal", "cluster", "manifold", "sparse", "sphere"]
    for s in shapes:
        pos, neg = _synthesize(s)
        data = render_shape(s, pos, neg, title=f"{s} (synthetic)")
        out = _OUTDIR / f"zwiad_3d_{s}.png"
        _render_to_png(data, out)
        extras = {}
        if s == "cone":
            extras["half_angle_deg"] = round(data["cone_half_angle_deg"], 3)
        if s == "cluster":
            extras["n_clusters"] = data["n_clusters"]
        if s == "sphere":
            extras["radius"] = round(data["sphere_radius"], 3)
            extras["radius_std"] = round(data["sphere_radius_std"], 3)
        if s == "bimodal":
            extras["plane_normal_norm"] = round(float((data["separating_plane_normal"] ** 2).sum() ** 0.5), 3)
        if s == "manifold":
            extras["n_edges"] = data["edges"].shape[0]
        print(f"wrote {out}  shape={data['shape']}  n_pos={data['pos_3d'].shape[0]}  n_neg={data['neg_3d'].shape[0]}  evr={[round(x,3) for x in data['explained_variance_ratio'].tolist()]}  extras={extras}")


if __name__ == "__main__":
    main()
