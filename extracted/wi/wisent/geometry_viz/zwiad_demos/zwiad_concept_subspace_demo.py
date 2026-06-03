"""
REAL activations in the contrastive-difference concept subspace.

Uses the production discover_concept_subspace() (NURT) on real
Llama-3.2-1B truthfulqa_mc1 layer-12 activations and renders pos/neg
projected into the recovered concept basis (first 3 concept dims).

Output: ../zwiad_3d_outputs/real_concept_subspace_truthfulqa_mc1_l12.png
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


# Stub heavy parents so we can import the subspace module in isolation.
for n in ("wisent", "wisent.core", "wisent.core.utils",
          "wisent.core.utils.config_tools",
          "wisent.core.control", "wisent.core.control.steering_methods",
          "wisent.core.control.steering_methods.implementations",
          "wisent.core.control.steering_methods.implementations.methods",
          "wisent.core.control.steering_methods.implementations.methods.extended",
          "wisent.core.control.steering_methods.implementations.methods.extended.nurt"):
    _stub(n)
_c = sys.modules["wisent.core.utils.config_tools.constants"] = _types.ModuleType(
    "wisent.core.utils.config_tools.constants")
_c.LOG_EPS = 1e-9

_subspace = _ilu.spec_from_file_location(
    "wisent.core.control.steering_methods.implementations.methods.extended.nurt.subspace",
    _REPO / "wisent/core/control/steering_methods/implementations/methods/extended/nurt/subspace.py",
)
_sub_mod = _ilu.module_from_spec(_subspace)
sys.modules[_subspace.name] = _sub_mod
_subspace.loader.exec_module(_sub_mod)
discover_concept_subspace = _sub_mod.discover_concept_subspace
project_to_subspace = _sub_mod.project_to_subspace

_OUTDIR = _HERE.parent / "zwiad_3d_outputs"
_BLOB = _OUTDIR / "layers_l1b_tqa" / "layer_8.safetensors"  # measured-best layer


def main():
    with safe_open(str(_BLOB), framework="np") as f:
        pos = torch.from_numpy(f.get_tensor("pos_activations"))
        neg = torch.from_numpy(f.get_tensor("neg_activations"))
    print(f"REAL activations (L8, measured-best layer): pos{tuple(pos.shape)} neg{tuple(neg.shape)}")

    # Production NURT subspace discovery on D = pos - neg (auto k).
    Vh, S, k = discover_concept_subspace(
        pos, neg,
        variance_threshold=0.90,
        nurt_num_dims=0,        # 0 = auto-select from spectrum
        nurt_max_concept_dim=64,
        min_concept_dim=3,
    )
    S_np = S.cpu().numpy()
    total = float((S_np ** 2).sum())
    top3 = float((S_np[:3] ** 2).sum()) / total
    print(f"concept subspace: k={k}  Vh{tuple(Vh.shape)}")
    print(f"singular values[:8] = {[round(float(x),3) for x in S_np[:8]]}")
    print(f"top-3 concept-dim variance fraction = {top3:.3f}  "
          f"(vs raw-PCA top3 = 0.263 measured earlier)")

    pos_z = project_to_subspace(pos, Vh).cpu().numpy()
    neg_z = project_to_subspace(neg, Vh).cpu().numpy()

    # The actual structure is 1-dimensional: separable along the concept
    # direction (unit vector between class means), NOT a low-D manifold.
    direction = pos_z.mean(axis=0) - neg_z.mean(axis=0)
    direction = direction / (np.linalg.norm(direction) + 1e-9)
    p_proj = pos_z @ direction
    n_proj = neg_z @ direction
    pooled_sd = np.sqrt(0.5 * (p_proj.var() + n_proj.var()))
    cohen_d = float((p_proj.mean() - n_proj.mean()) / (pooled_sd + 1e-9))
    thr = 0.5 * (p_proj.mean() + n_proj.mean())
    acc = float(((p_proj > thr).sum() + (n_proj < thr).sum())
                / (len(p_proj) + len(n_proj)))

    # orthogonal residual top-PC (the dimension that does NOT separate)
    rp = pos_z - np.outer(p_proj, direction)
    rn = neg_z - np.outer(n_proj, direction)
    ra = np.concatenate([rp, rn])
    r_axis = np.linalg.svd(ra - ra.mean(0), full_matrices=False)[2][0]
    p_r, n_r = rp @ r_axis, rn @ r_axis

    fig, (axh, axs) = plt.subplots(1, 2, figsize=(14, 6))
    bins = np.linspace(min(p_proj.min(), n_proj.min()),
                       max(p_proj.max(), n_proj.max()), 45)
    axh.hist(n_proj, bins=bins, alpha=0.6, color="#1f77b4", label="neg (false)")
    axh.hist(p_proj, bins=bins, alpha=0.6, color="#d62728", label="pos (truthful)")
    axh.axvline(thr, color="black", ls="--", lw=1.5,
                label=f"threshold (acc={acc:.2f})")
    axh.set_xlabel("projection onto concept direction")
    axh.set_ylabel("count")
    axh.set_title(f"THE actual structure: 1D separation (Cohen d = {cohen_d:.2f})")
    axh.legend(fontsize=9)
    axs.scatter(n_r, n_proj, c="#1f77b4", s=12, alpha=0.5, label="neg (false)")
    axs.scatter(p_r, p_proj, c="#d62728", s=12, alpha=0.5, label="pos (truthful)")
    axs.axhline(thr, color="black", ls="--", lw=1.5)
    axs.set_xlabel("orthogonal residual top-PC (does NOT separate)")
    axs.set_ylabel("concept axis (separates)")
    axs.set_title("concept axis vs residual")
    axs.legend(fontsize=9)
    fig.suptitle("REAL Llama-3.2-1B truthfulqa_mc1, measured-best layer L8 — "
                 f"NURT concept subspace (k={k})\n"
                 "The signal is 1-dimensional, not a manifold/sphere/torus",
                 fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    out = _OUTDIR / "real_true_projection_l8_truthfulqa_mc1.png"
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print(f"wrote {out.name}")
    print(f"Cohen d on concept axis = {cohen_d:.3f}   1D threshold acc = {acc:.3f}")
    print(f"pos_mean_proj={p_proj.mean():.3f}  neg_mean_proj={n_proj.mean():.3f}")


if __name__ == "__main__":
    main()
