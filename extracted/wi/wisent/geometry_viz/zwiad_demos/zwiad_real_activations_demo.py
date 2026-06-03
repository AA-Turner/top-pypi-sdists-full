"""
Run the Zwiad 3D shape renderers on REAL activations (no synthetic data).

Source: HuggingFace wisent-ai/activations
  meta-llama__Llama-3.2-1B-Instruct / truthfulqa_mc1 / chat_last / layer_12.safetensors
  -> pos_activations (500, 2048), neg_activations (500, 2048)

Outputs PNGs to ../zwiad_3d_outputs/ prefixed real_truthfulqa_mc1_layer12_.
"""
from __future__ import annotations

import sys
import types as _types
import importlib.util as _ilu
from pathlib import Path

import numpy as np
import torch
from safetensors import safe_open
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
_c.VIZ_N_COMPONENTS_3D = 3
_c.DEFAULT_RANDOM_SEED = 42
_c.NORM_EPS = 1e-9


def _load(qualname: str, p: Path):
    spec = _ilu.spec_from_file_location(qualname, p)
    mod = _ilu.module_from_spec(spec)
    sys.modules[qualname] = mod
    spec.loader.exec_module(mod)
    return mod


_root = _REPO / "wisent/core/utils/visualization/geometry/internals/shapes_3d"
_load("wisent.core.utils.visualization.geometry.internals.shapes_3d.dispatch", _root / "dispatch.py")
_rend = _load("wisent.core.utils.visualization.geometry.internals.shapes_3d.renderers", _root / "renderers.py")
_disp = sys.modules["wisent.core.utils.visualization.geometry.internals.shapes_3d.dispatch"]
render_shape = _disp.render_shape

_OUTDIR = _HERE.parent / "zwiad_3d_outputs"
_BLOB = _OUTDIR / "llama1b_truthfulqa_mc1_chat_last_layer12.safetensors"


def _render_png(data: dict, path: Path) -> None:
    fig = plt.figure(figsize=(8.0, 7.0))
    ax = fig.add_subplot(111, projection="3d")
    pos = data["pos_3d"]
    neg = data["neg_3d"]
    ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], c="#d62728", s=10, alpha=0.5, label="pos (truthful)")
    ax.scatter(neg[:, 0], neg[:, 1], neg[:, 2], c="#1f77b4", s=10, alpha=0.5, label="neg (false)")
    s = data["shape"]
    if s == "linear" and "axis_endpoints" in data:
        ep = data["axis_endpoints"]
        ax.plot(ep[:, 0], ep[:, 1], ep[:, 2], color="black", lw=2.5, label="separating axis")
    elif s == "cone" and "cone_lines" in data:
        for seg in data["cone_lines"]:
            ax.plot(seg[:, 0], seg[:, 1], seg[:, 2], color="black", lw=0.4, alpha=0.4)
    elif s == "bimodal":
        cp, cn = data["centroid_pos"], data["centroid_neg"]
        ax.scatter([cp[0], cn[0]], [cp[1], cn[1]], [cp[2], cn[2]],
                   c="black", s=90, marker="X", label="centroids")
    elif s == "cluster":
        for k, c in enumerate(data["cluster_centroids"]):
            ax.scatter([c[0]], [c[1]], [c[2]], s=110, marker="X",
                       edgecolor="black", linewidths=1.0)
    elif s == "manifold":
        for seg in data["edges"][:600]:
            ax.plot(seg[:, 0], seg[:, 1], seg[:, 2], color="black", lw=0.2, alpha=0.35)
    elif s == "sphere":
        surf = data["sphere_surface"]
        ax.plot_wireframe(surf[:, :, 0], surf[:, :, 1], surf[:, :, 2],
                          color="black", lw=0.3, alpha=0.4, rcount=10, ccount=14)
    ax.set_title(data.get("title", s))
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); ax.set_zlabel("PC3")
    ax.legend(loc="upper left", fontsize=8)
    plt.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main():
    if not _BLOB.exists():
        raise FileNotFoundError(f"missing real activation blob: {_BLOB}")
    with safe_open(str(_BLOB), framework="np") as f:
        pos_np = f.get_tensor("pos_activations")
        neg_np = f.get_tensor("neg_activations")
    pos = torch.from_numpy(pos_np)
    neg = torch.from_numpy(neg_np)

    # Substantiate the data is genuinely contrastive (not identical tensors).
    pm = pos_np.mean(axis=0)
    nm = neg_np.mean(axis=0)
    cos = float(pm @ nm / (np.linalg.norm(pm) * np.linalg.norm(nm) + 1e-9))
    print(f"loaded REAL activations: pos{tuple(pos.shape)} neg{tuple(neg.shape)}")
    print(f"pos_mean·neg_mean cosine = {cos:.4f}  (|pos_mean|={np.linalg.norm(pm):.3f} |neg_mean|={np.linalg.norm(nm):.3f})")
    print(f"||pos_mean - neg_mean|| = {np.linalg.norm(pm - nm):.4f}")

    for shape in ["linear", "cone", "bimodal", "cluster", "manifold", "sphere"]:
        data = render_shape(shape, pos, neg,
                            title=f"{shape} — REAL Llama-3.2-1B truthfulqa_mc1 L12 (n=500)")
        out = _OUTDIR / f"real_truthfulqa_mc1_layer12_{shape}.png"
        _render_png(data, out)
        evr = [round(x, 3) for x in data["explained_variance_ratio"].tolist()]
        print(f"wrote {out.name}  shape={data['shape']}  evr={evr}")


if __name__ == "__main__":
    main()
