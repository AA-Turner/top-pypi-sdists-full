"""
Cyclic-manifold steering demo, matching the Sauers/Goodfire reference structure.

Synthesizes 7 concept centroids on a circle in 32-D activation space (with
noise around each), projects to 3D, then overlays two paths:
 - a curved path along the fitted manifold (around the ring)
 - a straight Euclidean line between the start and a far cluster (off-manifold)

Saves PNG to ../zwiad_3d_outputs/zwiad_cyclic_steering.png.
"""
from __future__ import annotations

import sys
import types as _types
import importlib.util as _ilu
from pathlib import Path

import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent
sys.path.insert(0, str(_REPO))


def _stub(name: str):
    m = _types.ModuleType(name)
    sys.modules[name] = m
    return m


for n in ("wisent", "wisent.core", "wisent.core.utils", "wisent.core.utils.config_tools",
          "wisent.core.utils.visualization", "wisent.core.utils.visualization.geometry",
          "wisent.core.utils.visualization.geometry.internals",
          "wisent.core.utils.visualization.geometry.internals.shapes_3d"):
    _stub(n)
_c = sys.modules["wisent.core.utils.config_tools.constants"] = _types.ModuleType("wisent.core.utils.config_tools.constants")
_c.VIZ_N_COMPONENTS_3D = 3; _c.DEFAULT_RANDOM_SEED = 42; _c.NORM_EPS = 1e-9


def _load(qualname: str, p: Path):
    spec = _ilu.spec_from_file_location(qualname, p)
    mod = _ilu.module_from_spec(spec)
    sys.modules[qualname] = mod
    spec.loader.exec_module(mod)
    return mod


_root = _REPO / "wisent/core/utils/visualization/geometry/internals/shapes_3d"
_disp = _load("wisent.core.utils.visualization.geometry.internals.shapes_3d.dispatch", _root / "dispatch.py")
compute_pca_3d = _disp.compute_pca_3d


_SEED = 17
_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_N_PER = 80
_DIM = 32
_OUTDIR = _HERE.parent / "zwiad_3d_outputs"
_OUTDIR.mkdir(parents=True, exist_ok=True)


def synthesize_ring():
    """7 concept clusters whose centroids lie on a circle in 32-D."""
    rng = np.random.RandomState(_SEED)
    a = rng.randn(_DIM); a /= np.linalg.norm(a)
    b = rng.randn(_DIM); b -= b @ a * a; b /= np.linalg.norm(b)
    k = len(_DAYS)
    angles = np.linspace(0.0, 2.0 * np.pi, k, endpoint=False)
    radius = 5.0
    centroids = np.stack([radius * (np.cos(t) * a + np.sin(t) * b) for t in angles])
    acts, labels = [], []
    for i, c in enumerate(centroids):
        acts.append(c + rng.randn(_N_PER, _DIM) * 0.55)
        labels.extend([i] * _N_PER)
    return np.concatenate(acts, axis=0), np.array(labels), centroids, angles, (a, b)


def main():
    acts, labels, centroids_hd, angles, (a, b) = synthesize_ring()
    pos = torch.from_numpy(acts.astype(np.float32))
    neg = torch.from_numpy(acts.astype(np.float32))
    pts_3d, _, evr = compute_pca_3d(pos, neg)
    from sklearn.decomposition import PCA
    pca = PCA(n_components=3, random_state=42).fit(np.concatenate([acts, acts], axis=0))
    centroids_3d = pca.transform(centroids_hd)

    curved_hd = []
    for t in np.linspace(0.0, 3.0, 80):
        u = 2.0 * np.pi * t / 7.0
        curved_hd.append(5.0 * (np.cos(u) * a + np.sin(u) * b))
    curved_hd = np.array(curved_hd)
    curved_3d = pca.transform(curved_hd)

    start, end = centroids_hd[0], centroids_hd[3]
    straight_hd = np.array([(1.0 - t) * start + t * end for t in np.linspace(0.0, 1.0, 80)])
    straight_3d = pca.transform(straight_hd)

    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")
    cmap = plt.cm.viridis(np.linspace(0.0, 1.0, len(_DAYS)))
    for i, day in enumerate(_DAYS):
        mask = labels == i
        ax.scatter(pts_3d[mask, 0], pts_3d[mask, 1], pts_3d[mask, 2],
                   c=[cmap[i]], s=14, alpha=0.55, label=day)
        c3 = centroids_3d[i]
        ax.scatter([c3[0]], [c3[1]], [c3[2]], color=cmap[i], s=180, marker="X",
                   edgecolor="black", linewidths=1.5)
        ax.text(c3[0], c3[1], c3[2] + 0.5, day, fontsize=10, fontweight="bold")

    ax.plot(curved_3d[:, 0], curved_3d[:, 1], curved_3d[:, 2],
            color="black", lw=3.0, label="manifold steering (along ring)")
    ax.plot(straight_3d[:, 0], straight_3d[:, 1], straight_3d[:, 2],
            color="red", lw=3.0, linestyle="--", label="linear steering (cuts across)")
    ax.scatter([curved_3d[-1, 0]], [curved_3d[-1, 1]], [curved_3d[-1, 2]],
               color="black", s=160, marker="o")
    ax.scatter([straight_3d[-1, 0]], [straight_3d[-1, 1]], [straight_3d[-1, 2]],
               color="red", s=160, marker="o")

    ax.set_title("Cyclic concept manifold (days-of-the-week) — manifold vs linear steering\n"
                 "(activation space, 7 clusters in a ring)")
    ax.set_xlabel(f"PC1 ({evr[0]:.2f})"); ax.set_ylabel(f"PC2 ({evr[1]:.2f})")
    ax.set_zlabel(f"PC3 ({evr[2]:.2f})")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
    out = _OUTDIR / "zwiad_cyclic_steering.png"
    plt.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print(f"wrote {out}")
    print(f"evr={[round(x,3) for x in evr.tolist()]}")
    print(f"n_concepts={len(_DAYS)}  n_per_cluster={_N_PER}  ambient_dim={_DIM}")
    print(f"curved_path_length_3d={float(np.linalg.norm(np.diff(curved_3d, axis=0), axis=1).sum()):.3f}")
    print(f"straight_path_length_3d={float(np.linalg.norm(np.diff(straight_3d, axis=0), axis=1).sum()):.3f}")


if __name__ == "__main__":
    main()
